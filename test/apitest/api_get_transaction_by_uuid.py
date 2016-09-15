import json
import requests

url='http://10.2.1.22:9984/api/v1/transactions/uuid=b7d58a9b-fc33-4383-b4ad-940aa3c5a6f6'

r = requests.get(url)
print(r.text)
