__author__ = 'PC-LiNing'

import logging
import rethinkdb as r
from bigchaindb import crypto,util,Bigchain


logger = logging.getLogger(__name__)

class ChainQuery(object):

    def __init__(self, host=None, port=None, dbname=None,pub_key=None,priv_key=None,keyring=[],
                 consensus_plugin=None):
         self.host = host
         self.port = port
         self.dbname = dbname
         self.conn =r.connect(host=host,port=port,db=dbname)
         self.bigchain=Bigchain(host=host,port=port,dbname=dbname,public_key=pub_key,private_key=priv_key,keyring=keyring,consensus_plugin=consensus_plugin)

    #test
    def test(self):
        tables=r.db('bigchain').table_list().run(self.conn)
        #print(tables)
        return tables

    # create key_pair for user
    def generate_key_pair(self):
        return crypto.generate_key_pair()

    # create asset
    def create_asset(self,public_key, digital_asset_payload):
        tx = self.bigchain.create_transaction(self.bigchain.me, public_key, None, 'CREATE', payload=digital_asset_payload)
        tx_signed = self.bigchain.sign_transaction(tx, self.bigchain.me_private)
        return self.bigchain.write_transaction(tx_signed)

    # get transaction by payload_uuid
    def getTxid_by_payload_uuid(self,payload_uuid):
        cursor = r.table('bigchain') \
            .get_all(payload_uuid, index='payload_uuid') \
            .pluck({'block':{'transactions':'id'}}) \
            .run(self.conn)

        transactions = list(cursor)
        return transactions

    # get transaction by payload
    def getTxid_by_payload(self,payload):
        pass


    # get currentowner of a payload(assert)
    def getOwnerofAssert(self,payload):
        return


    # get one's assert
    def get_owned_asserts(self,pub_key):
        return

    # if tx contains someone
    def tx_contains_one(self,tx,one_pub):
        for condition in tx['conditions']:
            if one_pub in condition['new_owners']:
                return True
        for fullfillment in tx['fulfillments']:
            if one_pub in fullfillment['current_owners']:
                return True


    # transfer assert to another, old_owner create this transaction,so need old_owner's pub/priv key.
    def transfer_assert(self,old_owner_pub,old_owner_priv,new_owner_pub,tx_id):
        tx_transfer=self.bigchain.create_transaction(old_owner_pub,new_owner_pub,tx_id,'TRANSFER')
        tx_transfer_signed=self.bigchain.sign_transaction(tx_transfer,old_owner_priv)
        #check if the transaction is valid
        check=self.bigchain.is_valid_transaction(tx_transfer_signed)
        if check:
            self.bigchain.write_transaction(tx_transfer_signed)
        else:
            logger.info('this transaction is invalid.')

    #

if __name__ == '__main__':
    query=ChainQuery(host='10.2.4.68',port=28015,dbname='bigchain')
    print(query.test())
    print(query.getTxid_by_payload_uuid('f5f90564-9897-493e-8d3b-1a2600bbbc4f'))



