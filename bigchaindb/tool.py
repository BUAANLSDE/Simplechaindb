__author__ = 'PC-LiNing'

import time
from bigchaindb import payload

"""Added tools for SimpleChaindb

       1.convert between timestamp and time
       2.extract from payload

"""

def  get_Timefrom_Timestamp(timestamp):
    """convert timestamp to time."""
    x=time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',x)


def get_Timestampfrom_Time(t):
    """convert time to timestamp,time format is  2011-09-28 10:00:00."""
    return time.mktime(time.strptime(t,'%Y-%m-%d %H:%M:%S'))


