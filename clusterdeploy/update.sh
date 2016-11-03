#! /bin/bash

# The set -e option instructs bash to immediately exit
# if any command has a non-zero exit status
set -e

function printErr()
    {
        echo "usage: ./make_confiles.sh <number_of_files>"
        echo "No argument $1 supplied"
    }

if [ -z "$1" ]; then
    printErr "<number_of_files>"
    exit 1
fi

# reconfigure collectd & rethinkdb & bigchaindb
./configure_collectd.sh
./configure_rethinkdb.sh

./install_bigchaindb_from_git_archive.sh
./configure_bigchaindb.sh $1
#Todo 增加节点的话分片修改?
fab set_shards:$1
./clustercontrol.sh stop
./clustercontrol.sh start

