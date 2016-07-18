__author__ = 'PC-LiNing'

from bigchaindb import crypto

import ed25519
import base58
import json
import flask
private,public=crypto.generate_key_pair()
print("public key is : "+public)

dict={
    "public_key":public,
    "private_key":private
}

print(json.dumps(dict))


#private.encode().decode('ascii').

# sk,vk=ed25519.create_keypair()
# private_value_base58 = crypto.Ed25519SigningKey(base58.b58encode(sk.to_bytes())).to_ascii()
# print("private key generate public key is : "+str(sk.get_verifying_key().to_ascii(encoding="hex")))
