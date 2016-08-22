__author__ = 'PC-LiNing'

from bigchaindb import Bigchain

b=Bigchain()

testuser1_pub='3EQyWna5Gniok73MXdT8m9kgSx6DuRYWUbmehCe4cmXU'
testuser1_priv='EZYk1RJtMkySRwNtpiY7AeGQyYLaeu5XsrJHzzVBL3wn'
testuser2_pub='9ooi6zKXdLVmM2ZyUZjRTWcW3TXt2CtnHSbVZnXLxHJM'
testuser2_priv='AZQ1Y4odynAuYEkSQhVKGqNKU4Zp5QidoLwmkfZCjYqL'

tx_retrieved_id1=b.get_owned_ids(testuser1_pub)
print(tx_retrieved_id1)
print("pop:")
print(tx_retrieved_id1.pop())
print('####')
tx_retrieved_id2=b.get_owned_ids(testuser2_pub)
print(tx_retrieved_id2)
print("pop:")
print(tx_retrieved_id2.pop())