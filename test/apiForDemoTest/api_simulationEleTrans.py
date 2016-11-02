import requests
import json
import random
import time
import sys
import multiprocessing as mp
import datetime


processCount = sys.argv[1]
print(processCount)
if not processCount:
    print("please input how many processes do you want to create!")
    sys.exit()


url = 'http://127.0.0.1:9984/apifordemo/v1/electric_trans/'
# url = 'http://36.110.115.195:38/apifordemo/v1/electric_trans/'
headers = {'content-type': 'application/json'}
count = 0
# open file
f = open("./keypair.json", "r")
# load data
keypairAll = json.load(f)
# start = time.time()
# while (True):
# 此次执行创建多少交易
random_transactions = random.Random().randint(1, 100)
# 创建交易后休息多少秒
sleep_random = random.Random().randint(0, 3)

print('will create %d transactions and then will sleep %ds' % (random_transactions, sleep_random))

# for j in range(10):
#     id = random.Random().randint(0, 99)
#     owner_before = keypairAll["keypair"][id]["public_key"]
#     private_key = keypairAll["keypair"][id]["private_key"]
#     id = random.Random().randint(0, 99)
#     owner_after = keypairAll["keypair"][id]["public_key"]
#     payload = {
#         "owners_before": owner_before,
#         "owners_after": owner_after,
#         "private_key":private_key,
#         "msg": "create electric transcation!",
#         "info": "for Demo",
#         "count": count
#     }
#     data = json.dumps(payload)
#     ret = requests.post(url, data=data, headers=headers)
#     count = count + 1
#
# time.sleep(sleep_random)

def startRun():
    global count
    print("start Run...............")
    for i in range(1000):
        id = random.Random().randint(0, 99)
        owner_before = keypairAll["keypair"][id]["public_key"]
        private_key = keypairAll["keypair"][id]["private_key"]
        id = random.Random().randint(0, 99)
        owner_after = keypairAll["keypair"][id]["public_key"]
        payload = {
            "owners_before": owner_before,
            "owners_after": owner_after,
            "private_key": private_key,
            "msg": "create electric transcation!",
            "info": "for Demo",
            "count": count
        }
        data = json.dumps(payload)
        ret = requests.post(url, data=data, headers=headers)
        count = count + 1

    return None


if __name__ == "__main__":
  pool = mp.Pool(processes=int(processCount))
  while True:
    print(count)
    pool.apply_async(startRun)
  pool.close()
  pool.join()
  print("Sub-process(es) done.")

