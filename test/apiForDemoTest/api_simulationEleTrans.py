import requests
import json
import random
import time
import datetime

url = 'http://127.0.0.1:9984/apifordemo/v1/electric_trans/'

headers = {'content-type': 'application/json'}


count = 0

# open file
f = open("./keypair.json", "r")
# load data
keypairAll = json.load(f)

# start = time.time()

while (True):
    # 此次执行创建多少交易
    random_transactions = random.Random().randint(1, 100)
    # 创建交易后休息多少秒
    sleep_random = random.Random().randint(0, 3)

    print('will create %d transactions and then will sleep %ds' % (random_transactions, sleep_random))

    # _start = time.time()
    # _start = datetime.datetime.now().microsecond
    for j in range(random_transactions):
        id = random.Random().randint(0, 99)
        owner_before = keypairAll["keypair"][id]["public_key"]
        private_key = keypairAll["keypair"][id]["private_key"]
        id = random.Random().randint(0, 99)
        owner_after = keypairAll["keypair"][id]["public_key"]
        payload = {
            "owners_before": owner_before,
            "owners_after": owner_after,
            "private_key":private_key,
            "msg": "create electric transcation!",
            "info": "for Demo",
            "count": count
        }
        data = json.dumps(payload)
        ret = requests.post(url, data=data, headers=headers)
        count = count + 1

    # _end = time.time()
    # _end = datetime.datetime.now().microsecond

    # print('cost time %ds' % (_end - _start))

    time.sleep(sleep_random)
