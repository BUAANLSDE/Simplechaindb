__author__ = 'PC-LiNing'

from bigchaindb import  payload
from bigchaindb import  tool
from bigchaindb import Bigchain

response1={
    "deleted": 0,
    "errors": 0,
    "inserted": 1,
    "replaced": 0,
    "skipped": 0,
    "unchanged": 0
    }

response2={
    "deleted": 0,
    "errors": 0,
    "inserted": 1,
    "replaced": 0,
    "skipped": 0,
    "unchanged": 0
    }
response1.update(response2)
print(response1)

test='init'
print(test['id'])