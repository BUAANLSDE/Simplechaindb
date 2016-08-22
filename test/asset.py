__author__ = 'PC-LiNing'

from bigchaindb import Bigchain

b=Bigchain()

public_key='wreXXdHnbZmpyNxTCBscdtNMutF1VhL7v5n9zc9gyi2'
private_key='8Rwr5SUiE1ijAenpc4DawwWWSK6D2K2Fq4hzdKseXifr'

node_public='FxvxFdL9TJmAd1bDQVg3bs5zvS36Vs2jsd79ww2e7dLc'

tx = b.get_tx_by_asset('123456789')
print(tx)
print('----------------')

txid=b.get_tx_input(tx,public_key)
print(txid)
print('----------------')

response=b.transfer_asset(public_key,private_key,node_public,txid)

print(response)

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
# tx = b.create_asset(public_key,p)
# print(tx)


# response = b.destory_asset(public_key,private_key,'123456789')
# print(response)
