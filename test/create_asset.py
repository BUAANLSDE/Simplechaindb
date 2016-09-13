from bigchaindb import Bigchain

b=Bigchain()

public_key='wreXXdHnbZmpyNxTCBscdtNMutF1VhL7v5n9zc9gyi2'

p = {
            "msg" : "create_asset",
            "issue" : "create",
            "category" : "asset",
            "amount" : 0,
            "asset":'123456789',
            "account":0,
            "previous":'',
            "trader":''
        }
tx = b.create_asset(public_key,p)
print(tx)
