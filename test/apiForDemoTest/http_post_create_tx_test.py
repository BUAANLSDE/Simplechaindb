import requests
import json
import random
import time
url = 'http://localhost:9984/api/v1/transactions/'
# url = 'http://36.110.115.195:9984/api/v1/transactions/'
payload =  \
{
    "id": "16cd78bc53fc64c2bcbe8e991da1b88f57ba852c62734bcd9ea9e65b55cf75a9",
    "transaction": {
        "conditions": [
            {
                "cid": 0,
                "condition": {
                    "details": {
                        "bitmask": 32,
                        "public_key": "Bc4TEit6zNLvxnxmUqSGYTdx5T1aMifrT5dK2AiD9Lk",
                        "signature": None,
                        "type": "fulfillment",
                        "type_id": 4
                    },
                "uri": "cc:4:20:ArdzNIYG9bOxt0GLV97gfY5GSlrCC6oLiCOzZQ_PQOk:96"
            },
        "owners_after": [
          "Bc4TEit6zNLvxnxmUqSGYTdx5T1aMifrT5dK2AiD9Lk"
        ]
      }
    ],
    "data": {
      "payload": {
        "msg": "Hello BigchainDB!"
      },
      "uuid": "f5f90564-9897-493e-8d3b-1a2600bbbc4f"
    },
    "fulfillments": [
      {
        "owners_before": [
          "GcxoTqtGPTEcRguvwABHtJ6DVEBPoetBCPgi6Tw6zrDd"
        ],
        "fid": 0,
        "fulfillment": "cf:4:6BW6COlYhti0ZkgOqtPSBDyaVkEFooD29pKUSrkXELgeL-qR8wIpNgPipn1gC3HDMWG21K2kCR07HgiMp7o5XLxiHbhdVMHnpswa1L0oIkI6xxHV5h77dgyV-f1LCdAF",
        "input": None
      }
    ],
    "operation": "CREATE"
  },
  "version": 1
}
headers = {'content-type': 'application/json'}

count = 0
i_random = random.Random().randint(20,100)
data = json.dumps(payload)
start = time.time()
for i in range(i_random):
    random_transactions = random.Random().randint(1,1100)
    sleep_random = random.Random().randint(0,4)
    print('will run %d times\t the %dth\t produce %d transactions after will sleep %ds\t' % (i_random, i + 1, random_transactions,sleep_random))
    _start = time.time()
    for j in range(random_transactions):
        count = count + 1
        ret = requests.post(url, data=data, headers=headers)
    _end = time.time()
    print('cost time %ds' %(_end - _start))
    time.sleep(sleep_random)
# print(ret.text)
# print(ret.cookies)
end = time.time()
print('txs is %d\t cost time %d\t' %(count,end-start))
print('finish...')