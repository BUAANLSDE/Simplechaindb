import time

from unittest.mock import patch

import rethinkdb as r
from multipipes import Pipe, Pipeline


def dummy_tx(b):
    from bigchaindb.models import Transaction
    tx = Transaction.create([b.me], [b.me])
    tx = tx.sign([b.me_private])
    return tx


def dummy_block(b):
    block = b.create_block([dummy_tx(b) for _ in range(10)])
    return block


def test_vote_creation_valid(b):
    from bigchaindb.common import crypto
    from bigchaindb.common.util import serialize

    # create valid block
    block = dummy_block(b)
    # retrieve vote
    vote = b.vote(block.id, 'abc', True)

    # assert vote is correct
    assert vote['vote']['voting_for_block'] == block.id
    assert vote['vote']['previous_block'] == 'abc'
    assert vote['vote']['is_block_valid'] is True
    assert vote['vote']['invalid_reason'] is None
    assert vote['node_pubkey'] == b.me
    assert crypto.VerifyingKey(b.me).verify(serialize(vote['vote']).encode(),
                                            vote['signature']) is True


def test_vote_creation_invalid(b):
    from bigchaindb.common import crypto
    from bigchaindb.common.util import serialize

    # create valid block
    block = dummy_block(b)
    # retrieve vote
    vote = b.vote(block.id, 'abc', False)

    # assert vote is correct
    assert vote['vote']['voting_for_block'] == block.id
    assert vote['vote']['previous_block'] == 'abc'
    assert vote['vote']['is_block_valid'] is False
    assert vote['vote']['invalid_reason'] is None
    assert vote['node_pubkey'] == b.me
    assert crypto.VerifyingKey(b.me).verify(serialize(vote['vote']).encode(),
                                            vote['signature']) is True


def test_vote_ungroup_returns_a_set_of_results(b):
    from bigchaindb.pipelines import vote

    b.create_genesis_block()
    block = dummy_block(b)
    vote_obj = vote.Vote()
    txs = list(vote_obj.ungroup(block.id, block.transactions))

    assert len(txs) == 10


def test_vote_validate_block(b):
    from bigchaindb.pipelines import vote

    b.create_genesis_block()
    tx = dummy_tx(b)
    block = b.create_block([tx])

    vote_obj = vote.Vote()
    validation = vote_obj.validate_block(block.to_dict())
    assert validation[0] == block.id
    for tx1, tx2 in zip(validation[1], block.transactions):
        assert tx1 == tx2

    block = b.create_block([tx])
    # NOTE: Setting a blocks signature to `None` invalidates it.
    block.signature = None

    vote_obj = vote.Vote()
    validation = vote_obj.validate_block(block.to_dict())
    assert validation[0] == block.id
    for tx1, tx2 in zip(validation[1], [vote_obj.invalid_dummy_tx]):
        assert tx1 == tx2


def test_validate_block_with_invalid_id(b):
    from bigchaindb.pipelines import vote

    b.create_genesis_block()
    tx = dummy_tx(b)
    block = b.create_block([tx]).to_dict()
    block['id'] = 'an invalid id'

    vote_obj = vote.Vote()
    block_id, invalid_dummy_tx = vote_obj.validate_block(block)
    assert block_id == block['id']
    assert invalid_dummy_tx == [vote_obj.invalid_dummy_tx]


def test_validate_block_with_invalid_signature(b):
    from bigchaindb.pipelines import vote

    b.create_genesis_block()
    tx = dummy_tx(b)
    block = b.create_block([tx]).to_dict()
    block['signature'] = 'an invalid signature'

    vote_obj = vote.Vote()
    block_id, invalid_dummy_tx = vote_obj.validate_block(block)
    assert block_id == block['id']
    assert invalid_dummy_tx == [vote_obj.invalid_dummy_tx]


def test_vote_validate_transaction(b):
    from bigchaindb.pipelines import vote
    from bigchaindb.models import Transaction

    b.create_genesis_block()
    tx = dummy_tx(b)
    vote_obj = vote.Vote()
    validation = vote_obj.validate_tx(tx, 123, 1)
    assert validation == (True, 123, 1)

    # NOTE: Submit unsigned transaction to `validate_tx` yields `False`.
    tx = Transaction.create([b.me], [b.me])
    validation = vote_obj.validate_tx(tx, 456, 10)
    assert validation == (False, 456, 10)


def test_vote_accumulates_transactions(b):
    from bigchaindb.pipelines import vote

    b.create_genesis_block()
    vote_obj = vote.Vote()

    for _ in range(10):
        tx = dummy_tx(b)

    tx = tx
    validation = vote_obj.validate_tx(tx, 123, 1)
    assert validation == (True, 123, 1)

    tx.fulfillments[0].fulfillment.signature = None
    validation = vote_obj.validate_tx(tx, 456, 10)
    assert validation == (False, 456, 10)


def test_valid_block_voting_sequential(b, monkeypatch):
    from bigchaindb.common import crypto, util
    from bigchaindb.pipelines import vote

    monkeypatch.setattr('time.time', lambda: 1)
    genesis = b.create_genesis_block()
    vote_obj = vote.Vote()
    block = dummy_block(b)

    for tx, block_id, num_tx in vote_obj.ungroup(block.id, block.transactions):
        last_vote = vote_obj.vote(*vote_obj.validate_tx(tx, block_id, num_tx))

    vote_obj.write_vote(last_vote)
    vote_rs = b.connection.run(r.table('votes').get_all([block.id, b.me], index='block_and_voter'))
    vote_doc = vote_rs.next()

    assert vote_doc['vote'] == {'voting_for_block': block.id,
                                'previous_block': genesis.id,
                                'is_block_valid': True,
                                'invalid_reason': None,
                                'timestamp': '1'}

    serialized_vote = util.serialize(vote_doc['vote']).encode()
    assert vote_doc['node_pubkey'] == b.me
    assert crypto.VerifyingKey(b.me).verify(serialized_vote,
                                            vote_doc['signature']) is True


def test_valid_block_voting_multiprocessing(b, monkeypatch):
    from bigchaindb.common import crypto, util
    from bigchaindb.pipelines import vote

    inpipe = Pipe()
    outpipe = Pipe()

    monkeypatch.setattr('time.time', lambda: 1)
    genesis = b.create_genesis_block()
    vote_pipeline = vote.create_pipeline()
    vote_pipeline.setup(indata=inpipe, outdata=outpipe)

    block = dummy_block(b)

    inpipe.put(block.to_dict())
    vote_pipeline.start()
    vote_out = outpipe.get()
    vote_pipeline.terminate()

    vote_rs = b.connection.run(r.table('votes').get_all([block.id, b.me], index='block_and_voter'))
    vote_doc = vote_rs.next()
    assert vote_out['vote'] == vote_doc['vote']
    assert vote_doc['vote'] == {'voting_for_block': block.id,
                                'previous_block': genesis.id,
                                'is_block_valid': True,
                                'invalid_reason': None,
                                'timestamp': '1'}

    serialized_vote = util.serialize(vote_doc['vote']).encode()
    assert vote_doc['node_pubkey'] == b.me
    assert crypto.VerifyingKey(b.me).verify(serialized_vote,
                                            vote_doc['signature']) is True


def test_valid_block_voting_with_create_transaction(b, monkeypatch):
    from bigchaindb.common import crypto, util
    from bigchaindb.models import Transaction
    from bigchaindb.pipelines import vote

    genesis = b.create_genesis_block()

    # create a `CREATE` transaction
    test_user_priv, test_user_pub = crypto.generate_key_pair()
    tx = Transaction.create([b.me], [test_user_pub])
    tx = tx.sign([b.me_private])

    monkeypatch.setattr('time.time', lambda: 1)
    block = b.create_block([tx])

    inpipe = Pipe()
    outpipe = Pipe()

    vote_pipeline = vote.create_pipeline()
    vote_pipeline.setup(indata=inpipe, outdata=outpipe)

    inpipe.put(block.to_dict())
    vote_pipeline.start()
    vote_out = outpipe.get()
    vote_pipeline.terminate()

    vote_rs = b.connection.run(r.table('votes').get_all([block.id, b.me], index='block_and_voter'))
    vote_doc = vote_rs.next()
    assert vote_out['vote'] == vote_doc['vote']
    assert vote_doc['vote'] == {'voting_for_block': block.id,
                                'previous_block': genesis.id,
                                'is_block_valid': True,
                                'invalid_reason': None,
                                'timestamp': '1'}

    serialized_vote = util.serialize(vote_doc['vote']).encode()
    assert vote_doc['node_pubkey'] == b.me
    assert crypto.VerifyingKey(b.me).verify(serialized_vote,
                                            vote_doc['signature']) is True


def test_valid_block_voting_with_transfer_transactions(monkeypatch, b):
    from bigchaindb.common import crypto, util
    from bigchaindb.models import Transaction
    from bigchaindb.pipelines import vote

    genesis = b.create_genesis_block()

    # create a `CREATE` transaction
    test_user_priv, test_user_pub = crypto.generate_key_pair()
    tx = Transaction.create([b.me], [test_user_pub])
    tx = tx.sign([b.me_private])

    monkeypatch.setattr('time.time', lambda: 1)
    block = b.create_block([tx])
    b.write_block(block, durability='hard')

    # create a `TRANSFER` transaction
    test_user2_priv, test_user2_pub = crypto.generate_key_pair()
    tx2 = Transaction.transfer(tx.to_inputs(), [test_user2_pub], tx.asset)
    tx2 = tx2.sign([test_user_priv])

    monkeypatch.setattr('time.time', lambda: 2)
    block2 = b.create_block([tx2])
    b.write_block(block2, durability='hard')

    inpipe = Pipe()
    outpipe = Pipe()

    vote_pipeline = vote.create_pipeline()
    vote_pipeline.setup(indata=inpipe, outdata=outpipe)

    vote_pipeline.start()
    inpipe.put(block.to_dict())
    time.sleep(1)
    inpipe.put(block2.to_dict())
    vote_out = outpipe.get()
    vote2_out = outpipe.get()
    vote_pipeline.terminate()

    vote_rs = b.connection.run(r.table('votes').get_all([block.id, b.me], index='block_and_voter'))
    vote_doc = vote_rs.next()
    assert vote_out['vote'] == vote_doc['vote']
    assert vote_doc['vote'] == {'voting_for_block': block.id,
                                'previous_block': genesis.id,
                                'is_block_valid': True,
                                'invalid_reason': None,
                                'timestamp': '2'}

    serialized_vote = util.serialize(vote_doc['vote']).encode()
    assert vote_doc['node_pubkey'] == b.me
    assert crypto.VerifyingKey(b.me).verify(serialized_vote,
                                            vote_doc['signature']) is True

    vote2_rs = b.connection.run(r.table('votes').get_all([block2.id, b.me], index='block_and_voter'))
    vote2_doc = vote2_rs.next()
    assert vote2_out['vote'] == vote2_doc['vote']
    assert vote2_doc['vote'] == {'voting_for_block': block2.id,
                                 'previous_block': block.id,
                                 'is_block_valid': True,
                                 'invalid_reason': None,
                                 'timestamp': '2'}

    serialized_vote2 = util.serialize(vote2_doc['vote']).encode()
    assert vote2_doc['node_pubkey'] == b.me
    assert crypto.VerifyingKey(b.me).verify(serialized_vote2,
                                            vote2_doc['signature']) is True


def test_unsigned_tx_in_block_voting(monkeypatch, b, user_vk):
    from bigchaindb.common import crypto, util
    from bigchaindb.models import Transaction
    from bigchaindb.pipelines import vote

    inpipe = Pipe()
    outpipe = Pipe()

    monkeypatch.setattr('time.time', lambda: 1)
    genesis = b.create_genesis_block()
    vote_pipeline = vote.create_pipeline()
    vote_pipeline.setup(indata=inpipe, outdata=outpipe)

    # NOTE: `tx` is invalid, because it wasn't signed.
    tx = Transaction.create([b.me], [b.me])
    block = b.create_block([tx])

    inpipe.put(block.to_dict())
    vote_pipeline.start()
    vote_out = outpipe.get()
    vote_pipeline.terminate()

    vote_rs = b.connection.run(r.table('votes').get_all([block.id, b.me], index='block_and_voter'))
    vote_doc = vote_rs.next()
    assert vote_out['vote'] == vote_doc['vote']
    assert vote_doc['vote'] == {'voting_for_block': block.id,
                                'previous_block': genesis.id,
                                'is_block_valid': False,
                                'invalid_reason': None,
                                'timestamp': '1'}

    serialized_vote = util.serialize(vote_doc['vote']).encode()
    assert vote_doc['node_pubkey'] == b.me
    assert crypto.VerifyingKey(b.me).verify(serialized_vote,
                                            vote_doc['signature']) is True


def test_invalid_id_tx_in_block_voting(monkeypatch, b, user_vk):
    from bigchaindb.common import crypto, util
    from bigchaindb.models import Transaction
    from bigchaindb.pipelines import vote

    inpipe = Pipe()
    outpipe = Pipe()

    monkeypatch.setattr('time.time', lambda: 1)
    genesis = b.create_genesis_block()
    vote_pipeline = vote.create_pipeline()
    vote_pipeline.setup(indata=inpipe, outdata=outpipe)

    # NOTE: `tx` is invalid, because its id is not corresponding to its content
    tx = Transaction.create([b.me], [b.me])
    tx = tx.sign([b.me_private])
    block = b.create_block([tx]).to_dict()
    block['block']['transactions'][0]['id'] = 'an invalid tx id'

    inpipe.put(block)
    vote_pipeline.start()
    vote_out = outpipe.get()
    vote_pipeline.terminate()

    vote_rs = b.connection.run(r.table('votes').get_all([block['id'], b.me], index='block_and_voter'))
    vote_doc = vote_rs.next()
    assert vote_out['vote'] == vote_doc['vote']
    assert vote_doc['vote'] == {'voting_for_block': block['id'],
                                'previous_block': genesis.id,
                                'is_block_valid': False,
                                'invalid_reason': None,
                                'timestamp': '1'}

    serialized_vote = util.serialize(vote_doc['vote']).encode()
    assert vote_doc['node_pubkey'] == b.me
    assert crypto.VerifyingKey(b.me).verify(serialized_vote,
                                            vote_doc['signature']) is True


def test_invalid_content_in_tx_in_block_voting(monkeypatch, b, user_vk):
    from bigchaindb.common import crypto, util
    from bigchaindb.models import Transaction
    from bigchaindb.pipelines import vote

    inpipe = Pipe()
    outpipe = Pipe()

    monkeypatch.setattr('time.time', lambda: 1)
    genesis = b.create_genesis_block()
    vote_pipeline = vote.create_pipeline()
    vote_pipeline.setup(indata=inpipe, outdata=outpipe)

    # NOTE: `tx` is invalid, because its content is not corresponding to its id
    tx = Transaction.create([b.me], [b.me])
    tx = tx.sign([b.me_private])
    block = b.create_block([tx]).to_dict()
    block['block']['transactions'][0]['id'] = 'an invalid tx id'

    inpipe.put(block)
    vote_pipeline.start()
    vote_out = outpipe.get()
    vote_pipeline.terminate()

    vote_rs = b.connection.run(r.table('votes').get_all([block['id'], b.me], index='block_and_voter'))
    vote_doc = vote_rs.next()
    assert vote_out['vote'] == vote_doc['vote']
    assert vote_doc['vote'] == {'voting_for_block': block['id'],
                                'previous_block': genesis.id,
                                'is_block_valid': False,
                                'invalid_reason': None,
                                'timestamp': '1'}

    serialized_vote = util.serialize(vote_doc['vote']).encode()
    assert vote_doc['node_pubkey'] == b.me
    assert crypto.VerifyingKey(b.me).verify(serialized_vote,
                                            vote_doc['signature']) is True


def test_invalid_block_voting(monkeypatch, b, user_vk):
    from bigchaindb.common import crypto, util
    from bigchaindb.pipelines import vote

    inpipe = Pipe()
    outpipe = Pipe()

    monkeypatch.setattr('time.time', lambda: 1)
    genesis = b.create_genesis_block()
    vote_pipeline = vote.create_pipeline()
    vote_pipeline.setup(indata=inpipe, outdata=outpipe)

    block = dummy_block(b).to_dict()
    block['block']['id'] = 'this-is-not-a-valid-hash'

    inpipe.put(block)
    vote_pipeline.start()
    vote_out = outpipe.get()
    vote_pipeline.terminate()

    vote_rs = b.connection.run(r.table('votes').get_all([block['id'], b.me], index='block_and_voter'))
    vote_doc = vote_rs.next()
    assert vote_out['vote'] == vote_doc['vote']
    assert vote_doc['vote'] == {'voting_for_block': block['id'],
                                'previous_block': genesis.id,
                                'is_block_valid': False,
                                'invalid_reason': None,
                                'timestamp': '1'}

    serialized_vote = util.serialize(vote_doc['vote']).encode()
    assert vote_doc['node_pubkey'] == b.me
    assert crypto.VerifyingKey(b.me).verify(serialized_vote,
                                            vote_doc['signature']) is True


def test_voter_considers_unvoted_blocks_when_single_node(monkeypatch, b):
    from bigchaindb.pipelines import vote

    outpipe = Pipe()

    monkeypatch.setattr('time.time', lambda: 1)
    b.create_genesis_block()

    # insert blocks in the database while the voter process is not listening
    # (these blocks won't appear in the changefeed)
    monkeypatch.setattr('time.time', lambda: 2)
    block_1 = dummy_block(b)
    b.write_block(block_1, durability='hard')
    monkeypatch.setattr('time.time', lambda: 3)
    block_2 = dummy_block(b)
    b.write_block(block_2, durability='hard')

    vote_pipeline = vote.create_pipeline()
    vote_pipeline.setup(indata=vote.get_changefeed(), outdata=outpipe)
    vote_pipeline.start()

    # We expects two votes, so instead of waiting an arbitrary amount
    # of time, we can do two blocking calls to `get`
    outpipe.get()
    outpipe.get()

    # create a new block that will appear in the changefeed
    monkeypatch.setattr('time.time', lambda: 4)
    block_3 = dummy_block(b)
    b.write_block(block_3, durability='hard')

    # Same as before with the two `get`s
    outpipe.get()

    vote_pipeline.terminate()

    # retrieve blocks from bigchain
    blocks = list(b.connection.run(
                r.table('bigchain')
                .order_by(r.asc((r.row['block']['timestamp'])))))

    # FIXME: remove genesis block, we don't vote on it
    # (might change in the future)
    blocks.pop(0)
    vote_pipeline.terminate()

    # retrieve vote
    votes = b.connection.run(r.table('votes'))
    votes = list(votes)

    assert all(vote['node_pubkey'] == b.me for vote in votes)


def test_voter_chains_blocks_with_the_previous_ones(monkeypatch, b):
    from bigchaindb.pipelines import vote

    outpipe = Pipe()

    monkeypatch.setattr('time.time', lambda: 1)
    b.create_genesis_block()

    monkeypatch.setattr('time.time', lambda: 2)
    block_1 = dummy_block(b)
    b.write_block(block_1, durability='hard')

    monkeypatch.setattr('time.time', lambda: 3)
    block_2 = dummy_block(b)
    b.write_block(block_2, durability='hard')

    vote_pipeline = vote.create_pipeline()
    vote_pipeline.setup(indata=vote.get_changefeed(), outdata=outpipe)
    vote_pipeline.start()

    # We expects two votes, so instead of waiting an arbitrary amount
    # of time, we can do two blocking calls to `get`
    outpipe.get()
    outpipe.get()
    vote_pipeline.terminate()

    # retrive blocks from bigchain
    blocks = list(b.connection.run(
                     r.table('bigchain')
                     .order_by(r.asc((r.row['block']['timestamp'])))))

    # retrieve votes
    votes = list(b.connection.run(r.table('votes')))

    assert votes[0]['vote']['voting_for_block'] in (blocks[1]['id'], blocks[2]['id'])
    assert votes[1]['vote']['voting_for_block'] in (blocks[1]['id'], blocks[2]['id'])


def test_voter_checks_for_previous_vote(monkeypatch, b):
    from bigchaindb.pipelines import vote

    inpipe = Pipe()
    outpipe = Pipe()

    monkeypatch.setattr('time.time', lambda: 1)
    b.create_genesis_block()

    monkeypatch.setattr('time.time', lambda: 2)
    block_1 = dummy_block(b)
    inpipe.put(block_1.to_dict())

    assert b.connection.run(r.table('votes').count()) == 0

    vote_pipeline = vote.create_pipeline()
    vote_pipeline.setup(indata=inpipe, outdata=outpipe)
    vote_pipeline.start()

    # wait for the result
    outpipe.get()

    # queue block for voting AGAIN
    monkeypatch.setattr('time.time', lambda: 3)
    inpipe.put(block_1.to_dict())

    # queue another block
    monkeypatch.setattr('time.time', lambda: 4)
    inpipe.put(dummy_block(b).to_dict())

    # wait for the result of the new block
    outpipe.get()

    vote_pipeline.terminate()

    assert b.connection.run(r.table('votes').count()) == 2


@patch.object(Pipeline, 'start')
def test_start(mock_start, b):
    # TODO: `block.start` is just a wrapper around `vote.create_pipeline`,
    #       that is tested by `test_full_pipeline`.
    #       If anyone has better ideas on how to test this, please do a PR :)
    from bigchaindb.pipelines import vote

    b.create_genesis_block()

    vote.start()
    mock_start.assert_called_with()
