__author__="jiuyueqiji"

import rethinkdb as r

from bigchaindb import Bigchain
from bigchaindb import db
from bigchaindb import core

b = Bigchain()

# get transaction by uuid
def get_tx_by_payload_uuid(payload_uuid):
    conn = db.get_conn();
    cursor = r.table('bigchain') \
        .get_all(payload_uuid, index='payload_uuid') \
        .run(conn)

    transactions = list(cursor)
    return transactions


# disregard transactions from invalid blocks
def disregard_tx_from_invalid_blocks(transactions):
    tx_list = []
    for tx in transactions:
        validity = core.get_blocks_status_containing_tx(tx['id'])
        if Bigchain.BLOCK_VALID not in validity.values():
            if Bigchain.BLOCK_UNDECIDED not in validity.values():
                continue

        tx_list.append(tx)
    return tx_list

# get transactions by user public key and operation
def get_tx_by_opt_and_pub(opt, pub):
    if(opt=="CREATE"):
        return get_create_tx_by_pub(pub)
    elif(opt=="TRANSTER"):
        return get_transfer_tx_by_pub(pub)
    else:
        return None;


# get create trasaction by user public key
def get_create_tx_by_pub(pub):

    conn = db.get_conn()

    response = r.table('bigchain') \
        .concat_map(lambda doc: doc['block']['transactions']) \
        .filter(lambda tmp: tmp['transaction']['operation'] == 'CREATE') \
        .filter(lambda tx: tx['transaction']['conditions']
                .contains(lambda c: c['new_owners']
                          .contains(pub))) \
        .run(conn)

    return disregard_tx_from_invalid_blocks(response)


# get transfer transaction by user public key
def get_transfer_tx_by_pub(pub):
    conn = db.get_conn()

    response = r.table('bigchain') \
        .concat_map(lambda doc: doc['block']['transactions']) \
        .filter(lambda tmp: tmp['transaction']['operation'] == 'TRANSFER') \
        .filter(lambda tx: tx['transaction']['conditions']
                .contains(lambda c: c['new_owners']
                          .contains(pub))) \
        .run(conn)

    return disregard_tx_from_invalid_blocks(response)