__author__ = 'PC-LiNing'

# from bigchaindb import crypto
from  cryptoconditions import crypto
import ed25519
import base58
import json
import flask
from bigchaindb import  tool
# private,public=crypto.generate_key_pair()

# public key is : 63KuD28oMB6ew8HSA6ZY6WanEn483J8GooVr1AUv9gF9
# private key is : A7iqWL6eNkgbZy1RRdywVtNHEdujYfyJShoHxRL7QwU8

# print("public key is : "+public)
# print("private key is : "+private)

private_key='A7iqWL6eNkgbZy1RRdywVtNHEdujYfyJShoHxRL7QwU8'
# signkey=crypto.Ed25519SigningKey(private_key)
# public_key=signkey.get_verifying_key().to_ascii()
# print(public_key)

print(tool.get_public_key(private_key).decode())
