__author__ = 'PC-LiNing buaa'

import time
from bigchaindb import payload
from collections import deque
from cryptoconditions import  crypto
from bigchaindb import exceptions


"""Added tools for SimpleChaindb

       1.convert between timestamp and time
       2.operations with payload
       3.construct  transaction
"""

def  get_Timefrom_Timestamp(timestamp):
    """convert timestamp to time."""
    x=time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',x)


def get_Timestampfrom_Time(t):
    """convert time to timestamp,time format is  2011-09-28 10:00:00."""
    return time.mktime(time.strptime(t,'%Y-%m-%d %H:%M:%S'))


def get_payload_type(tx):
    """get tx's payload type"""
    pd=tx['transaction']['data']['payload']
    if payload.validate_payload_format(pd):
        return pd['category']
    else:
        return None


def get_last_txid(backlog_bigchain_list):
    """get last txid from backlog-bigchain-list
       item's format is:
       {
            'txid':tx-id,
            'cid':cid,
            'previous':previous-txid
       }
    """
    # check list is empty
    # the user account is initial
    if len(backlog_bigchain_list) == 0:
        return 'init'

    tx_ids=[]
    for item in backlog_bigchain_list:
        if item['txid'] in tx_ids:
            tx_ids.remove(item['txid'])
        else:
            tx_ids.append(item['txid'])
        if item['previous'] in tx_ids:
            tx_ids.remove(item['previous'])
        else:
            tx_ids.append(item['previous'])

    if len(tx_ids) == 2:
        tx_ids.remove('genesis')
    else:
        raise exceptions.CurrencyListError('currency list invalid')

    # cid always 0
    if len(tx_ids) == 1:
        last_id={'txid': tx_ids[0], 'cid':0}
        return last_id
    else:
        # Exception
        return None


def get_current_account(last_tx):
    """get current account from last_tx"""
    # check last_tx is 'init'
    if last_tx == 'init':
        return 0
    pd=last_tx['transaction']['data']['payload']
    account=pd['account']
    # cost/earn/charge
    if pd['issue'] == 'cost':
        account=account-pd['amount']
    elif pd['issue'] == 'earn' or pd['issue'] == 'charge':
        account=account+pd['amount']
    else:
        # Exception
        return None
    return account

def get_pair_payload(transfer_payload):
    """construct a pair of payloads by given currency transfer payload"""
    sender_payload={
        'msg':transfer_payload['msg'],
        'issue':'cost',
        'category':'currency',
        'amount':transfer_payload['amount'],
        'asset':transfer_payload['asset'],
        'account':None,
        'previous':None,
        'trader':None
    }
    receiver_payload={
        'msg':transfer_payload['msg'],
        'issue':'earn',
        'category':'currency',
        'amount':transfer_payload['amount'],
        'asset':transfer_payload['asset'],
        'account':None,
        'previous':None,
        'trader':None
    }
    return sender_payload,receiver_payload

# find after
def find_next_currency(current_currency_id,currency_list):
    """get currency contain current currency id in given currency list"""
    for item in currency_list:
        if(item['payload']['previous'] == current_currency_id):
            return item
    return None

# find before
def find_before_currency(current_currency_previous_id,currency_list):
    """get currency contain current currency previous id in given currency list"""
    for item in currency_list:
        if(item['txid'] == current_currency_previous_id):
            return item
    return None

def sort_currency_list(currency_list):
    """sort currency list"""
    queue = deque()
    queue.append(currency_list[0])
    start=currency_list[0]
    end=currency_list[0]
    currency_list.remove(currency_list[0])
    while len(currency_list) > 0:
        # search next
        next=find_next_currency(end['txid'],currency_list)
        if next != None:
            queue.append(next)
            currency_list.remove(next)
            end=next
        else:
            break

    while len(currency_list) > 0:
        # search before
        before=find_before_currency(start['payload']['previous'],currency_list)
        if before != None:
            queue.appendleft(before)
            currency_list.remove(before)
            start=before
        else:
            break

    if len(currency_list) > 0:
        # Exception
        return None
    else:
        return queue


def get_currency_records(currency_queue):
    """get currency records from currency queue
       record format:
       {
            "msg":additional message
            "issue":issue,
            "trader":trader,
            "asset":asset,
            "amount":amount,
            "time":time
        }
    """
    records=[]
    while currency_queue is not None and len(currency_queue) > 0 :
        item=currency_queue.popleft()
        record={
            "msg":item['payload']['msg'],
            "issue":item['payload']['issue'],
            "trader":item['payload']['trader'],
            "asset":item['payload']['asset'],
            "amount":item['payload']['amount'],
            "time":get_Timefrom_Timestamp(int(item['timestamp']))
        }
        records.append(record)
    return records


def get_public_key(private_key):
    """get corresponding public key """
    public_key=crypto.Ed25519SigningKey(private_key).get_verifying_key().to_ascii()
    return public_key.decode()


def sort_asset_tx_by_timestamp(tx_list):
    """sort the transaction list of asset by tx_timestamp desc """
    for i in range(0,len(tx_list)-1):
        for j in range(i+1,len(tx_list)):
            if float(tx_list[i]['transaction']['timestamp']) \
                    < float(tx_list[j]['transaction']['timestamp']):
                tmp = tx_list[i]
                tx_list[i] = tx_list[j]
                tx_list[j] = tmp

    return deque(tx_list)


def get_asset_records(asset_queue):
    """get asset records from asset queue
       record format:
       {
            "owners_before":owners_before,
            "owners_after":owners_after,
            "time":time
       }
    """
    records=[]
    while asset_queue is not None and len(asset_queue) > 0 :
        item=asset_queue.pop()
        record={
            "owners_before":item['transaction']['fulfillments'][0]['owners_before'],
            "owners_after":item['transaction']['conditions'][0]['owners_after'],
            "time":get_Timefrom_Timestamp(int(item['transaction']['timestamp']))
        }
        records.append(record)
    return records
