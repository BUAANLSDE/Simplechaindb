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
    if len(tx_ids) == 1:
        return tx_ids[0]
    else:
        # Exception
        return None




