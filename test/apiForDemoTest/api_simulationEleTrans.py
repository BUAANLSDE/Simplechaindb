import requests
import json
import random
import time
import sys
import multiprocessing as mp
import datetime
import uuid

processCount = sys.argv[1]

if not processCount:
    print("please input how many processes do you want to create!")
    sys.exit()

# url = 'http://127.0.0.1:9984/apifordemo/v1/electric_trans/'
# url = 'http://127.0.0.1:9984/apifordemo/v1/electric_trans/test/'
# url = 'http://36.110.115.195:38/apifordemo/v1/electric_trans/'
url = 'http://36.110.115.195:38/api/v1/transactions/test/'
headers = {'content-type': 'application/json'}
# count = 0
# open file
# f = open("./keypair.json", "r")
# load data
# keypairAll = json.load(f)
# start = time.time()
# while (True):
# 此次执行创建多少交易
# random_transactions = random.Random().randint(500, 999)
# # 创建交易后休息多少秒
# sleep_random = random.Random().randint(2, 5)

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
#     data = jdson.dumps(payload)
#     ret = requests.post(url, data=data, headers=headers)
#     count = count + 1
# time.sleep(sleep_random)

def startRun():
    while True:

        random_transactions = random.Random().randint(500, 999)
        sleep_random = random.Random().randint(1, 4)
        print('will create %d transactions and then sleep %ds' % (random_transactions, sleep_random))
        starttimefor = datetime.datetime.now().microsecond
        count = 0
        for i in range(random_transactions):
            payload = {
                "private_key": "7JVZtx9tCQD12HXG2J1QntrhcntNu7Sp3BCPF3H7fUhY"
            }
            data = json.dumps(payload)
            # starttime = datetime.datetime.now().microsecond
            try:
                ret = requests.post(url, data=data, headers=headers)
            except:
                print("post except!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            # endtime = datetime.datetime.now().microsecond
            # responseTime = float(ret.elapsed.microseconds) / 1000  # 获取响应时间，单位ms
            count += 1
            print('count = %d '%(count))
            # print('%d sys %d,one trans cost %d'%(count,ret.status_code,responseTime))
            # print('local %d,one trans cost %d' % (ret.status_code, (endtime-starttime)/1000))
        endtimefor = datetime.datetime.now().microsecond
        print('cost %d ms create %d transactions' % ((endtimefor-starttimefor)/1000,random_transactions))
        time.sleep(sleep_random)


if __name__ == "__main__":
    pool = mp.Pool(processes=int(processCount))
    for i in range(int(processCount)):
        result = pool.apply_async(startRun)
    pool.close()
    pool.join()
    print(result.successful())
