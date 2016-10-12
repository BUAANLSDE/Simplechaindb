# -*- coding: utf-8 -*-
"""(Re)create the collectd configuration file conf/collectd.conf
Start with conf/collectd.conf.template
then append additional configuration setting, ie. monitor server.
"""

from __future__ import unicode_literals
import os
import shutil
from monitor_server import gMonitorServer

# cwd = current working directory
old_cwd = os.getcwd()
os.chdir('conf')
# Remove the old one
if os.path.isfile('collectd.conf'):
    os.remove('collectd.conf')

# Create the initial collectd.conf using collectd.conf.backup
shutil.copy2('collectd.conf.template', 'collectd.conf')

# Append additional lines to rethinkdb.conf
with open('collectd.conf', 'a') as f:
    f.write('''
<Plugin network>
    Server "''' + gMonitorServer + '''" "25826"
</Plugin>
    ''')

os.chdir(old_cwd)
