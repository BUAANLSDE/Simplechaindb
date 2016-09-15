import json
import requests

url='http://10.2.1.22:9984/api/v1/transactions/status/tx_id=099'

r = requests.get(url)
print(r.text)
