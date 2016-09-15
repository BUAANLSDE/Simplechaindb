import json
import requests

url='http://10.2.1.22:9984/api/v1/accounts/transfer/'

values={
            "sender_public_key":"wreXXdHnbZmpyNxTCBscdtNMutF1VhL7v5n9zc9gyi2",
            "sender_private_key":"8Rwr5SUiE1ijAenpc4DawwWWSK6D2K2Fq4hzdKseXifr",
            "receiver_public_key":"6HtWNXvTXCnnSAgVq3FBtjD36Jrc1ibfX979j26kiBXo",
            "data":{
                    "msg": "currency transfer",
                    "issue": "transfer",
                    "category": "currency",
                    "amount": 300,
                    "asset": 'test',
                    "account":0,
                    "previous":'',
                    "trader":''
                   }
         }

headers = {
  'content-type': 'application/json',"Accept": "application/json"
}

r=requests.post(url,data=json.dumps(values),headers=headers)
print(r.text)
