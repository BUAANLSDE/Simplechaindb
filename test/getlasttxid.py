__author__ = 'PC-LiNing'

from bigchaindb import tool

backlog_bigchain_list=[ {'txid':"A",'cid':0,'previous':"B"},{'txid':"B",'cid':0,'previous':"C"},
                        {'txid':"C",'cid':0,'previous':"D"},{'txid':"D",'cid':0,'previous':"genesis"}]

print(tool.get_last_txid(backlog_bigchain_list))