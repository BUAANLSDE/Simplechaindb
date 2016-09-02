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


./install_base_software.sh
./install_rethinkdb.sh
./configure_rethinkdb.sh
./install_bigchaindb_from_git_archive.sh
./configure_bigchaindb.sh $1
./clustercontrol.sh start
