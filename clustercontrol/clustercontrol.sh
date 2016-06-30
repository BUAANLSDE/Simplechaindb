
#! /bin/bash


if [ $# != 1 ]
then
   echo "Usage: startcluster start|stop "
   exit 1
fi

# start or stop cluster

if [ $1 == "start" ]
then
   echo "start cluster..."
   fab set_allnodes start_rethinkdb start_bigchaindb
elif [ $1 == "stop" ]
then
   echo "stop cluster..."
   fab set_allnodes stop_bigchaindb stop_rethinkdb
fi




