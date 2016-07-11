#! /bin/bash

# The set -e option instructs bash to immediately exit
# if any command has a non-zero exit status
set -e

# (Re)create the RethinkDB configuration file conf/rethinkdb.conf
python create_rethinkdb_conf.py
# Rollout storage backend (RethinkDB) and start it
fab confiure_rethinkdb
