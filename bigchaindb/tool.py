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


# when user_A transfer currency to user_B, this transaction will appeared in user_B currency transaction stack.
# this transaction will change  amount of user_B's account.
# In order to maintain correct of  the accounts,we need to generate a corresponding transaction which will appeared in
# user_A 's currency transaction stack and will change amount of user_A's account .
# obviously, the two transactions are twins,which  means can only be right or wrong at the same time.

def construct_tx(payload,pubkey_A,pubkey_B):
    """construct corresponding transaction """

    pass

