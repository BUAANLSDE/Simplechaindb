__author__ = 'PC-LiNing'

import requests
from flask import json

values={
         "sender_public_key":"wreXXdHnbZmpyNxTCBscdtNMutF1VhL7v5n9zc9gyi2",
         "sender_private_key":"8Rwr5SUiE1ijAenpc4DawwWWSK6D2K2Fq4hzdKseXifr",
         "receiver_public_key":"ECP3CFJAWpfB3xn7CzFDN4QCJ1Kh1dtbbSUWGTRYaQer",
         "asset":'testasset'
        }
headers = {'content-type': 'application/json',"Accept": "application/json"}
r = requests.post('http://10.2.4.109:9984/api/v1/assets/transfer/',json.dumps(values),headers)
print(r.text)