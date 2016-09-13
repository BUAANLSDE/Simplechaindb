import json
import requests

url='http://10.2.1.22:9984/api/v1/transactions/tx_id=c2fefb6a9539df86959af139c4dbb6a0f5552191f603da83696980de653b4cf5'

r = requests.get(url)
print(r.text)
