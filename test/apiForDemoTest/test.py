# How to read the json file
import json

# open file
f = open("./keypair.json", "r")
# load data
keypairAll = json.load(f)

# get public_key
owner_before = keypairAll["keypair"][0]["public_key"]
print(owner_before)

owner_after = keypairAll["keypair"][1]["public_key"]
print(owner_after)
