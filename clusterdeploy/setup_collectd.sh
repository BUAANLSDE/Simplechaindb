#! /bin/bash

# The set -e option instructs bash to immediately exit
# if any command has a non-zero exit status
set -e

# Install collectd
fab install_collectd
# Configure collectd.conf and restart
fab configure_collectd