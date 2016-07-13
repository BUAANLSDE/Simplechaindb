# -*- coding: utf-8 -*-

import thriftpy

from thriftpy.rpc import make_server

contract_thrift = thriftpy.load("contract.thrift",
                                module_name="contract_thrift")


class ContractHandler(object):
    def __init__(self):
        pass

    def creat_video(self, video_hash,cost):
        if video_hash!="v1":
            return True
        return False

    def transfer_video(self, video_hash, owner_id,buyer_id):
        if video_hash == "v1" and owner_id=="u1":
            return True
        return False

    def creat_coin(self, user_id):
        return True

    def transfer_coin(self, owner_id, buyer_id):
        if owner_id == "u1":
            return True
        return False


def main():
    server = make_server(contract_thrift.Contract, ContractHandler(),
                         '127.0.0.1', 8090)
    print("serving...")
    server.serve()


if __name__ == '__main__':
    main()
