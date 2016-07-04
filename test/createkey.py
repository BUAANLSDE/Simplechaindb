__author__ = 'PC-LiNing'

from bigchaindb import crypto


testuser1_priv, testuser1_pub = crypto.generate_key_pair()

print(testuser1_priv, testuser1_pub)

print('#####')

testuser2_priv, testuser2_pub = crypto.generate_key_pair()

print(testuser2_priv, testuser2_pub)