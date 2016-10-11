
import os

curren_uid = os.getuid()
curren_gid = os.getgid()

paths = ["/localdb/bigchain","/localdb/votes","/localdb/header"]

for path in paths:
    # if not os.path.exists(path):
        print("path " + str(path) + " ,uid=" + str(curren_uid) + " ,gid=" + str(curren_gid))
        os.makedirs(path+"/go",curren_uid,curren_gid)

