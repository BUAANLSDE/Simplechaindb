
import json
import requests

url='http://127.0.0.1:9984/api/v1/system/key'

# util: generate 100 keypair for 100 users

"""
{
  "keypair": [
    {
      "public_key": "HmUyiGb5nS2Vh35gqTJaWsNyE74zh4PGfEuZ1EZSvRda",
      "private_key": "HmUyiGb5nS2Vh35gqTJaWsNyE74zh4PGfEuZ1EZSvRda"
    },
    {
      "public_key": "wreXXdHnbZmpyNxTCBscdtNMutF1VhL7v5n9zc9gyi2",
      "private_key": "wreXXdHnbZmpyNxTCBscdtNMutF1VhL7v5n9zc9gyi2"
    }
  ]
}
"""

keypairList = []
for i in range(0,100):
    r = requests.get(url)
    json.loads(r.text)
    keypairList.append(json.loads(r.text))

dictJson = {'keypair':keypairList}

f = open('./keypair.json','a')
keypairJson = json.dump(dictJson,f)


