import json
import requests

url='http://10.2.1.22:9984/api/v1/accounts/charge/3j9BC3URnA8mVv2Do9xiK4PfbvDFAbWi5NRpckQ1Tey9/100'

r = requests.get(url)
print(r.text)
