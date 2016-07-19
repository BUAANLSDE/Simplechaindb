__author__ = 'PC-LiNing'

import time
from bigchaindb import payload

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
    tx_ids.remove('genesis')
    # cid always 0
    if len(tx_ids) == 1:
        last_id={'txid': tx_ids[0], 'cid':0}
        return last_id
    else:
        # Exception
        return None


def get_current_account(last_tx):
    """get current account from last_tx"""
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

