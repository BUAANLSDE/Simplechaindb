__author__ = 'PC-LiNing'

import time

#convert timestamp to time
def  getTimefromTimestamp(timestamp):
    x=time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',x)

#convert time to timestamp,time format is  2011-09-28 10:00:00
def getTimestampfromTime(t):
    return time.mktime(time.strptime(t,'%Y-%m-%d %H:%M:%S'))

#print(getTimefromTimestamp(time.time()))

print(getTimestampfromTime('2016-07-08 23:37:58'))