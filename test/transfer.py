__author__ = 'PC-LiNing'

from bigchaindb import Bigchain

b=Bigchain()

testuser1_pub='3EQyWna5Gniok73MXdT8m9kgSx6DuRYWUbmehCe4cmXU'
testuser1_priv='EZYk1RJtMkySRwNtpiY7AeGQyYLaeu5XsrJHzzVBL3wn'
testuser2_pub='9ooi6zKXdLVmM2ZyUZjRTWcW3TXt2CtnHSbVZnXLxHJM'
testuser2_priv='AZQ1Y4odynAuYEkSQhVKGqNKU4Zp5QidoLwmkfZCjYqL'

# node create transaction for A,-50

testuser1_last=b.get_owned_ids(testuser1_pub).pop()

payload_A = {
            "msg" : "node send -50 to A,is -50",
            "issue" : "cost",
            "category" : "currency",
            "amount" : 50,
            "asset":"",
            # final owner 's account
            "account":300,
            "previous":testuser1_last['txid'],
            "trader":testuser2_pub
          }

tx_create= b.create_transaction(b.me, testuser1_pub, None, 'CREATE', payload=payload_A)
tx_create_signed = b.sign_transaction(tx_create, b.me_private)
if b.is_valid_transaction(tx_create_signed):
    b.write_transaction(tx_create_signed)

# node create transaction for b,
testuser2_last=b.get_owned_ids(testuser2_pub).pop()
payload_B = {
            "msg" : "node send +50 to B,is +50",
            "issue" : "earn",
            "category" : "currency",
            "amount" : 50,
            "asset":"",
            # final owner 's account
            "account":400,
            "previous":testuser2_last['txid'],
            "trader":testuser1_pub
          }

tx_transfer= b.create_transaction(b.me, testuser2_pub, None, 'CREATE', payload=payload_B)
tx_transfer_signed = b.sign_transaction(tx_transfer, b.me_private)
if b.is_valid_transaction(tx_transfer_signed):
    b.write_transaction(tx_transfer_signed)


