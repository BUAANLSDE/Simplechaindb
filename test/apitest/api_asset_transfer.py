import json
import requests

url='http://10.2.1.22:9984/api/v1/assets/transfer/'

values = """
{
    "sender_public_key":"wreXXdHnbZmpyNxTCBscdtNMutF1VhL7v5n9zc9gyi2",
    "sender_private_key":"8Rwr5SUiE1ijAenpc4DawwWWSK6D2K2Fq4hzdKseXifr",
    "receiver_public_key":"FxvxFdL9TJmAd1bDQVg3bs5zvS36Vs2jsd79ww2e7dLc",
    "asset":"914"
}
"""

headers = {
  'Content-Type': 'application/json'
}

r=requests.post(url,data=values,headers=headers)
print(r.text)
