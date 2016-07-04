import json
import time

import rapidjson
from line_profiler import LineProfiler

import bigchaindb
from bigchaindb import crypto

def speedtest_create_transaction():
    b=bigchaindb.Bigchain()
    #testuser_priv,testuser_pub=crypto.generate_key_pair()
    time_start=time.time()
    #1000 create transaction
    for i in range(1000):
	    testuser_priv,testuser_pub=crypto.generate_key_pair()
	    msg='create_transaction speed tests in '+str(i)
	    digital_asset_payload={'msg':msg}
	    tx=b.create_transaction(b.me,testuser_pub,None,'CREATE',payload=digital_asset_payload)
	    tx_signed=b.sign_transaction(tx,b.me_private)
	    b.write_transaction(tx_signed)

    time_elapsed=time.time()-time_start
    print('speedtest_create_transaction:{} s'.format(time_elapsed))


def speedtest_validate_transaction():
    # create a transaction
    b = bigchaindb.Bigchain()
    tx = b.create_transaction(b.me, b.me, None, 'CREATE')
    tx_signed = b.sign_transaction(tx, b.me_private)

    # setup the profiler
    #profiler = LineProfiler()
    #profiler.enable_by_count()
    #profiler.add_function(bigchaindb.Bigchain.validate_transaction)
    
    time_start=time.time()

    # validate_transaction 1000 times
    for i in range(1000):
        b.validate_transaction(tx_signed)
   
    time_elapsed=time.time()-time_start

    #profiler.print_stats()
    print('speedtest_validate_transaction:{} s'.format(time_elapsed))


def speedtest_serialize_block_json():
    # create a block
    b = bigchaindb.Bigchain()
    tx = b.create_transaction(b.me, b.me, None, 'CREATE')
    tx_signed = b.sign_transaction(tx, b.me_private)
    block = b.create_block([tx_signed] * 1000)

    time_start = time.time()
    for _ in range(1000):
        _ = json.dumps(block, skipkeys=False, ensure_ascii=False, sort_keys=True)
    time_elapsed = time.time() - time_start

    print('speedtest_serialize_block_json: {} s'.format(time_elapsed))


def speedtest_serialize_block_rapidjson():
    # create a block
    b = bigchaindb.Bigchain()
    tx = b.create_transaction(b.me, b.me, None, 'CREATE')
    tx_signed = b.sign_transaction(tx, b.me_private)
    block = b.create_block([tx_signed] * 1000)

    time_start = time.time()
    for _ in range(1000):
        _ = rapidjson.dumps(block, skipkeys=False, ensure_ascii=False, sort_keys=True)
    time_elapsed = time.time() - time_start

    print('speedtest_serialize_block_rapidjson: {} s'.format(time_elapsed))


def speedtest_deserialize_block_json():
    # create a block
    b = bigchaindb.Bigchain()
    tx = b.create_transaction(b.me, b.me, None, 'CREATE')
    tx_signed = b.sign_transaction(tx, b.me_private)
    block = b.create_block([tx_signed] * 1000)
    block_serialized = json.dumps(block, skipkeys=False, ensure_ascii=False, sort_keys=True)

    time_start = time.time()
    for _ in range(1000):
        _ = json.loads(block_serialized)
    time_elapsed = time.time() - time_start

    print('speedtest_deserialize_block_json: {} s'.format(time_elapsed))


def speedtest_deserialize_block_rapidjson():
    # create a block
    b = bigchaindb.Bigchain()
    tx = b.create_transaction(b.me, b.me, None, 'CREATE')
    tx_signed = b.sign_transaction(tx, b.me_private)
    block = b.create_block([tx_signed] * 1000)
    block_serialized = rapidjson.dumps(block, skipkeys=False, ensure_ascii=False, sort_keys=True)

    time_start = time.time()
    for _ in range(1000):
        _ = rapidjson.loads(block_serialized)
    time_elapsed = time.time() - time_start

    print('speedtest_deserialize_block_rapidjson: {} s'.format(time_elapsed))


if __name__ == '__main__':
    speedtest_create_transaction()
    #speedtest_validate_transaction()
    #speedtest_serialize_block_json()
    #speedtest_serialize_block_rapidjson()
    #speedtest_deserialize_block_json()
    #speedtest_deserialize_block_rapidjson()
