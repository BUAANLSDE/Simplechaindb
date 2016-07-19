__author__ = 'PC-LiNing'

from bigchaindb import tool

payload={"msg" : "i like this video.","issue" : "cost","category" : "currency","amount" : 50.5,"asset":"hash of this video","account":1000}

payload['account']=3000
print(payload)