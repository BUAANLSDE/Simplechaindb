__author__ = 'PC-LiNing'
from bigchaindb import Bigchain

b=Bigchain()

### get blocks ids and status by tx_id
def  getblocksBytx_id(tx_id):
    blocks=b.get_blocks_status_containing_tx(tx_id)
    return blocks


### get block by block_id
def getblockbyid(block_id):
    pass
    return

