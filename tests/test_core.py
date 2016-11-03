from collections import namedtuple

from rethinkdb.ast import RqlQuery

import pytest


@pytest.fixture
def config(request, monkeypatch):
    config = {
        'database': {
            'host': 'host',
            'port': 28015,
            'name': 'bigchain',
        },
        'keypair': {
            'public': 'pubkey',
            'private': 'privkey',
        },
        'keyring': [],
        'CONFIGURED': True,
        'backlog_reassign_delay': 30
    }

    monkeypatch.setattr('bigchaindb.config', config)

    return config


def test_bigchain_class_default_initialization(config):
    from bigchaindb.core import Bigchain
    from bigchaindb.consensus import BaseConsensusRules
    bigchain = Bigchain()
    assert bigchain.host == config['database']['host']
    assert bigchain.port == config['database']['port']
    assert bigchain.dbname == config['database']['name']
    assert bigchain.me == config['keypair']['public']
    assert bigchain.me_private == config['keypair']['private']
    assert bigchain.nodes_except_me == config['keyring']
    assert bigchain.consensus == BaseConsensusRules


def test_bigchain_class_initialization_with_parameters(config):
    from bigchaindb.core import Bigchain
    from bigchaindb.consensus import BaseConsensusRules
    init_kwargs = {
        'host': 'some_node',
        'port': '12345',
        'dbname': 'atom',
        'public_key': 'white',
        'private_key': 'black',
        'keyring': ['key_one', 'key_two'],
    }
    bigchain = Bigchain(**init_kwargs)
    assert bigchain.host == init_kwargs['host']
    assert bigchain.port == init_kwargs['port']
    assert bigchain.dbname == init_kwargs['dbname']
    assert bigchain.me == init_kwargs['public_key']
    assert bigchain.me_private == init_kwargs['private_key']
    assert bigchain.nodes_except_me == init_kwargs['keyring']
    assert bigchain.consensus == BaseConsensusRules


def test_get_blocks_status_containing_tx(monkeypatch):
    from bigchaindb.db.backends.rethinkdb import RethinkDBBackend
    from bigchaindb.core import Bigchain
    blocks = [
        {'id': 1}, {'id': 2}
    ]
    monkeypatch.setattr(RethinkDBBackend, 'get_blocks_status_from_transaction', lambda x: blocks)
    monkeypatch.setattr(Bigchain, 'block_election_status', lambda x, y, z: Bigchain.BLOCK_VALID)
    bigchain = Bigchain(public_key='pubkey', private_key='privkey')
    with pytest.raises(Exception):
        bigchain.get_blocks_status_containing_tx('txid')


def test_has_previous_vote(monkeypatch):
    from bigchaindb.core import Bigchain
    monkeypatch.setattr(
        'bigchaindb.util.verify_vote_signature', lambda voters, vote: False)
    bigchain = Bigchain(public_key='pubkey', private_key='privkey')
    block = {'votes': ({'node_pubkey': 'pubkey'},)}
    with pytest.raises(Exception):
        bigchain.has_previous_vote(block)


@pytest.mark.parametrize('count,exists', ((1, True), (0, False)))
def test_transaction_exists(monkeypatch, count, exists):
    from bigchaindb.core import Bigchain
    monkeypatch.setattr(RqlQuery, 'run', lambda x, y: count)
    bigchain = Bigchain(public_key='pubkey', private_key='privkey')
    assert bigchain.transaction_exists('txid') is exists
