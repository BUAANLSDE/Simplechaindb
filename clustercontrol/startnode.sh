
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
		    echo "Usage: startnode -h user@host -p password [-r] [-b]"
		    exit 1
		    ;;
        esac
done

hostandport=${host}":22"

# start rethinkdb 
if [ $rethinkdb != false ]
then
    echo "start rethinkdb..."
    fab set_node:$hostandport,password=$password start_rethinkdb
fi

#start bigchaindb
if [ $bigchaindb != false ]
then
    echo "start bigchaindb..."
    fab set_node:$hostandport,password=$password start_bigchaindb
fi






