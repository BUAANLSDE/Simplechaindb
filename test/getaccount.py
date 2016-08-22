__author__ = 'PC-LiNing'

from bigchaindb import tool
from collections import deque

#currency_list=[ {'txid':"B",'payload':{'previous':'C'}},{'txid':"A",'payload':{'previous':'B'}},{'txid':"C",'payload':{'previous':'D'}},{'txid':"D",'payload':{'previous':'genesis'}}]

currency_list=[ {'payload': {'account': 0, 'trader': 'node', 'previous': 'genesis', 'issue': 'charge', 'category': 'currency', 'amount': 300, 'msg': 'charge', 'asset': ''}, 'txid': 'bdc3f3e746fa8462c85a539a357cac3669c8e83f1f58721e2bd04c91c234057a', 'timestamp': '1469011573'}, {'payload': {'account': 300, 'trader': 'node', 'previous':'bdc3f3e746fa8462c85a539a357cac3669c8e83f1f58721e2bd04c91c234057a', 'issue': 'charge', 'category': 'currency', 'amount': 300, 'msg': 'charge', 'asset': ''}, 'txid': '7bbbc03c59c2ad39bf2d1bbda0a905e9ee5f7a19d56cedca6b1d6807cee966a1', 'timestamp': '1469015677'}]
print(tool.get_currency_records(tool.sort_currency_list(currency_list)))
