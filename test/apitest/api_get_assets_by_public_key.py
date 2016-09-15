import json
import requests


url='http://10.2.1.22:9984/api/v1/assets/wreXXdHnbZmpyNxTCBscdtNMutF1VhL7v5n9zc9gyi2'

r = requests.get(url)
print(r.text)
