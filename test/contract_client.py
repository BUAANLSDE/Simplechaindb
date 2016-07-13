# -*- coding: utf-8 -*-

import thriftpy
from bigchaindb import crypto
import rethinkdb as r
from thriftpy.rpc import client_context

contract_thrift = thriftpy.load("contract.thrift",
                                module_name="contract_thrift")


def main():

    with client_context(contract_thrift.Contract,
                        '10.2.4.71', 8090) as client:
        keypair = crypto.generate_key_pair()
#        conn=r.connect(host='10.2.4.68',port=28015,db='bigchain') '10.2.4.71'
#        tables = r.db('bigchain').table_list().run(conn)
#        print(tables)
        print(keypair)

        #v1 already exists F
        cv = client.creat_video("v1",10)
        print(cv)

        # new video T
        cv = client.creat_video(keypair[1],10)
        print(cv)

        #u1:[v1] 0 u2:[] 100 T
        tv = client.transfer_video("v1","u1","u2")
        print(tv)

        #u1:[v1] 0 u2:[] 100 F
        tv = client.transfer_video("v2","u1","u2")
        print(tv)

        #T
        cc = client.creat_coin("u1")
        print(cc)

        # u1 ok u3 not T
        tc = client.transfer_coin("u1","u2")
        print(tc)
        # u1 ok u3 not F
        tc = client.transfer_coin("u3", "u2")
        print(tc)

if __name__ == '__main__':
    main()
