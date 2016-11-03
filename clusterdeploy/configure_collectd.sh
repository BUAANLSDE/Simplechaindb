#! /bin/bash

# The set -e option instructs bash to immediately exit
# if any command has a non-zero exit status
set -e

# Install collectd
# fab install_collectd
# (Re)create the Collectd configuration file conf/collectd.conf
python create_collectd_conf.py
# Configure collectd.conf and restart
fab configure_collectd