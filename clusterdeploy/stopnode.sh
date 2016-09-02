
#! /bin/bash

host=
password=
rethinkdb=false
bigchaindb=false

while getopts "h:p:rb" arg 
do
	case $arg in
		h)
		    host=$OPTARG
		    #echo "h's arg:$OPTARG"
		    ;;
	        p)
                    password=$OPTARG
		    #echo "p's arg:$OPTARG"
       		    ;;
	        r)
                    rethinkdb=true
		    ;;
	        b)
                    bigchaindb=true
                    ;;

	        ?) 
		    echo "Usage: stopnode -h user@host -p password [-r] [-b]"
		    exit 1
		    ;;
        esac
done

hostandport=${host}":22"

# stop  bigchaindb
if [ $bigchaindb != false ]
then
    echo "stop bigchaindb..."
    fab set_node:$hostandport,password=$password stop_bigchaindb
fi

# stop rethinkdb 
if [ $rethinkdb != false ]
then
    echo "stop rethinkdb..."
    fab set_node:$hostandport,password=$password stop_rethinkdb
fi







