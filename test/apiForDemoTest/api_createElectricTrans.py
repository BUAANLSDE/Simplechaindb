import json
import requests

url='http://127.0.0.1:9984/apifordemo/v1/electric_trans/'

values = """{
    "owners_before":"HmUyiGb5nS2Vh35gqTJaWsNyE74zh4PGfEuZ1EZSvRda",
    "owners_after":"wreXXdHnbZmpyNxTCBscdtNMutF1VhL7v5n9zc9gyi2",
    "msg":"create electric transcation!"
}"""


headers = {
  'Content-Type': 'application/json'
}

r=requests.post(url,data=values,headers=headers)
# print(r.text)