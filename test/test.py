__author__ = 'PC-LiNing'

from bigchaindb import Bigchain

b=Bigchain()

public_key='wreXXdHnbZmpyNxTCBscdtNMutF1VhL7v5n9zc9gyi2'
private_key='8Rwr5SUiE1ijAenpc4DawwWWSK6D2K2Fq4hzdKseXifr'

p = {
                "msg": "charge",
                "issue": "charge",
                "category": "currency",
                "amount": 300,
                "asset": '',
                "account":0,
                "previous":'',
                "trader":''
         }
tx = b.charge_currency(public_key, p)
print(tx)