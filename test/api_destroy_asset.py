import json
import requests


public_key='wreXXdHnbZmpyNxTCBscdtNMutF1VhL7v5n9zc9gyi2'
private_key='8Rwr5SUiE1ijAenpc4DawwWWSK6D2K2Fq4hzdKseXifr'
url='http://10.2.1.22:9984/api/v1/assets/destroy/wreXXdHnbZmpyNxTCBscdtNMutF1VhL7v5n9zc9gyi2?private_key=8Rwr5SUiE1ijAenpc4DawwWWSK6D2K2Fq4hzdKseXifr&asset_hash=915'

r = requests.get(url)
print(r.text)
