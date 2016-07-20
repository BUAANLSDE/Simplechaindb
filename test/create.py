__author__ = 'PC-LiNing'

from bigchaindb import Bigchain
from bigchaindb import  crypto
import time

b=Bigchain()

# user A
testuser1_priv, testuser1_pub = crypto.generate_key_pair()
print("testuser1_priv:"+testuser1_priv)
print("testuser1_pub:"+testuser1_pub)
payload = {
            "msg" : "first charge for user A",
            "issue" : "charge",
            "category" : "currency",
            "amount" : 300,
            "asset":"",
            "account":0,
            "previous":"genesis",
            "trader":""
          }
tx = b.create_transaction(b.me, testuser1_pub, None, 'CREATE', payload=payload)
tx_signed = b.sign_transaction(tx, b.me_private)
if b.is_valid_transaction(tx_signed):
    b.write_transaction(tx_signed)


# user B
testuser2_priv, testuser2_pub = crypto.generate_key_pair()
print("testuser2_priv:"+testuser2_priv)
print("testuser2_pub:"+testuser2_pub)
payload2 = {
            "msg" : "first charge for user B",
            "issue" : "charge",
            "category" : "currency",
            "amount" : 400,
            "asset":"",
            "account":0,
            "previous":"genesis",
            "trader":""
          }
tx2 = b.create_transaction(b.me, testuser2_pub, None, 'CREATE', payload=payload2)
tx_signed2 = b.sign_transaction(tx2, b.me_private)
if b.is_valid_transaction(tx_signed2):
    b.write_transaction(tx_signed2)


