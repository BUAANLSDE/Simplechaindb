__author__ = 'PC-LiNing'

import logging
import rethinkdb as r

class ChainQuery(object):

    def __init__(self, host=None, port=None, dbname=None):
         self.host = host
         self.port = port
         self.dbname = dbname
         self.conn =r.connect(host=host,port=port,db=dbname)

    ##test
    def test(self):
        tables=r.db('bigchain').table_list().run(self.conn)
        #print(tables)
        return tables

    ## get transaction by payload_uuid
    def getTxid_by_payload_uuid(self,payload_uuid):
        cursor = r.table('bigchain') \
            .get_all(payload_uuid, index='payload_uuid') \
            .pluck({'block':{'transactions':'id'}}) \
            .run(self.conn)

        transactions = list(cursor)
        return transactions

    ## get currentowner of a payload(assert)
    def getOwnerofAssert(self,payload):
        return

    ## 

if __name__ == '__main__':
    query=ChainQuery(host='10.2.4.68',port=28015,dbname='bigchain')
    print(query.test())
    print(query.getTxid_by_payload_uuid('f5f90564-9897-493e-8d3b-1a2600bbbc4f'))



