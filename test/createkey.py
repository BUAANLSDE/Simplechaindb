__author__ = 'PC-LiNing'


from bigchaindb import  payload
from bigchaindb import  tool
from bigchaindb import Bigchain
p = {
            "msg" : "create_asset",
            "issue" : "create",
            "category" : "asset",
            "amount" : 0,
            "asset":"123456789",
            "account":0,
            "test":''
        }

p.update({'assignee': 'test'})
print(p)
p.pop('assignee')
print(p)

