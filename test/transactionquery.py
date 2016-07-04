__author__ = 'PC-LiNing'

from bigchaindb import Bigchain

b=Bigchain()

### check a transcation is exist
def is_transaction_exists(tx_id):
    exist=b.transaction_exists(tx_id)
    return exist

### get transcation ids list by owner public key
def getTxidsByownerpubkey(pub):
    owned=b.get_owned_ids(pub)
    return owned

