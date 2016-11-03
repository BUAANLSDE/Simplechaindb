# -*- coding: utf-8 -*-
"""A Fabric fabfile with functionality to prepare, install, and configure
BigchainDB, including its storage backend (RethinkDB).
"""

from __future__ import with_statement, unicode_literals

from os import environ  # a mapping (like a dict)
import sys

from fabric.api import sudo, env, hosts
from fabric.api import task, parallel
from fabric.contrib.files import sed
from fabric.operations import run, put
from fabric.context_managers import settings

from hostlist import public_dns_names

public_hosts = []
public_pwds = []
f=open('blockchain-nodes')
for line in f.readlines():
    temp=line.strip('\r\n').split(" ")
    host=temp[0]
    password=temp[1]
    public_hosts.append(host)
    public_pwds.append(password)
    env['passwords'][host]=password
env['hosts']=env['passwords'].keys()


######################################################################

# DON'T PUT @parallel
@task
def set_host(host_index):
    """A helper task to change env.hosts from the
    command line. It will only "stick" for the duration
    of the fab command that called it.

    Args:
        host_index (int): 0, 1, 2, 3, etc.
    Example:
        fab set_host:4 fab_task_A fab_task_B
        will set env.hosts = [public_dns_names[4]]
        but only for doing fab_task_A and fab_task_B
    """
    env.hosts = [public_hosts[int(host_index)]]
    env.password = [public_pwds[int(host_index)]]


# Install base software
@task
@parallel
def install_base_software():
  # python pip3 :
    with settings(warn_only=True):
        sudo('apt-get -y update')
        sudo('dpkg --configure -a')
        sudo('apt-get -y -f install')
        sudo('apt-get -y install git gcc g++ python3-dev python3-setuptools python3-pip ntp screen')
        sudo('pip3 install --upgrade pip')
        sudo('pip3 --version')

@task
@parallel
def init_localdb(flag='all'):
    with settings(warn_only=True):
        # clear rabbitmq
        # if flag == 'all' or flag == 'rabbitmq':
        #     sudo(" echo 'clear the rabbitmq data' ")
        #     sudo("rabbitmqctl stop_app")
        #     sudo("rabbitmqctl reset")
        #     sudo("rabbitmqctl stop")
        #     sudo("rabbitmqctl start_app")

        # clear leveldb
        if flag == 'all' or flag == 'leveldb':
            sudo(" echo 'clear the leveldb data only' ")
            sudo("rm -rf /localdb/{log,bigchain,votes,header,changefeeds,rethinkdb_changes}/*")



# Install localdb
@task
@parallel
def install_localdb():
    # leveldb & plyvel install
    with settings(warn_only=True):
        user_group = env.user
        sudo(" echo 'leveldb & plyvel install' ")
        sudo("mkdir -p /localdb/{log,bigchain,votes,header,changefeeds,rethinkdb_changes}")
        sudo("chown -R " + user_group + ':' + user_group + ' /localdb')
        sudo('pip3 install leveldb==0.194')
        sudo('apt-get install libleveldb1 libleveldb-dev libsnappy1 libsnappy-dev')
        sudo('apt-get -y -f install')
        sudo('pip3 install plyvel==0.9')

        # ramq & pika install
        sudo(" echo 'ramq & pika install' ")
        sudo('apt-get -y install rabbitmq-server')
        sudo('pip3 install pika==0.10.0')
        #sudo('rabbitmq-server restart')


# Install RethinkDB
@task
@parallel
def install_rethinkdb():
    """Installation of RethinkDB"""
    with settings(warn_only=True):
        sudo("mkdir -p /data")
        # install rethinkdb
        sudo("echo 'deb http://download.rethinkdb.com/apt trusty main' | sudo tee /etc/apt/sources.list.d/rethinkdb.list")
        sudo("wget -qO- http://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -")
        sudo("apt-get update")
        sudo("apt-get -y install rethinkdb")
        # initialize data-dir
        sudo('rm -rf /data/*')

# Configure RethinkDB
@task
@parallel
def confiure_rethinkdb():
    """Confiure of RethinkDB"""
    with settings(warn_only=True):
        # copy config file to target system
        put('conf/rethinkdb.conf',
            '/etc/rethinkdb/instances.d/default.conf',
            mode=0x0600,
            use_sudo=True)
        # finally restart instance
        sudo('/etc/init.d/rethinkdb restart')

# Install BigchainDB from a Git archive file
# named bigchaindb-archive.tar.gz
@task
@parallel
def install_bigchaindb_from_git_archive():
    put('bigchaindb-archive.tar.gz')
    run('tar xvfz bigchaindb-archive.tar.gz')
    sudo('pip3 install -i http://pypi.douban.com/simple --upgrade setuptools')
    # sudo('pip3 install . --upgrade')
    sudo('python3 setup.py install')
    run('rm bigchaindb-archive.tar.gz')


# Configure BigchainDB
@task
@parallel
def configure_bigchaindb():
    run('simplechaindb -y configure', pty=False)


# Send the specified configuration file to
# the remote host and save it there in
# ~/.bigchaindb
# Use in conjunction with set_host()
# No @parallel
@task
def send_confile(confile):
    put('confiles/' + confile, 'tempfile')
    run('mv tempfile ~/.bigchaindb')
    print('For this node, bigchaindb show-config says:')
    run('simplechaindb show-config')


@task
@parallel
def send_client_confile(confile):
    put(confile, 'tempfile')
    run('mv tempfile ~/.bigchaindb')
    print('For this node, bigchaindb show-config says:')
    run('simplechaindb show-config')


# Initialize BigchainDB
# i.e. create the database, the tables,
# the indexes, and the genesis block.
# (The @hosts decorator is used to make this
# task run on only one node. See http://tinyurl.com/h9qqf3t )
@task
@hosts(public_hosts[0])

def init_bigchaindb():
    with settings(warn_only=True):
        run('simplechaindb -y drop',pty=False)
        run('simplechaindb init', pty=False)
        #must set_shards
        # num_shards = len(public_hosts)
        # run('simplechaindb set-shards {}'.format(num_shards))


# Set the number of shards (tables[bigchain,votes,backlog])
@task
@hosts(public_hosts[0])

def set_shards(num_shards):
    run('simplechaindb set-shards {}'.format(num_shards))


# Set the number of replicas (tables[bigchain,votes,backlog])
@task
@hosts(public_hosts[0])

def set_replicas(num_replicas):
    run('simplechaindb set-replicas {}'.format(num_replicas))


# Start BigchainDB using screen
@task
@parallel
def start_bigchaindb():
    with settings(warn_only=True):
        sudo('screen -d -m simplechaindb -y start &', pty=False,user=env.user)

@task
@parallel
def stop_bigchaindb():
    with settings(warn_only=True):
        sudo("kill `ps -ef|grep simplechaindb | grep -v grep|awk '{print $2}'` ")

@task
@parallel
def start_bigchaindb_load():
    sudo('screen -d -m simplechaindb load &', pty=False)

@task
@parallel
def start_bigchaindb_load_processes_counts(m=None,c=None):
    if m is None and c is None:
        sudo('screen -d -m simplechaindb load &', pty=False)
    flag = None
    v = None
    if m and isinstance(m,int):
        flag=flag+'m'
        v = m
    if c and isinstance(c,int):
        flag=flag+'c'
        v = c
    if len(flag) == 1:
        sudo('screen -d -m simplechaindb load -' + flag + ' ' + v + ' &', pty=False)

    if len(flag) == 2:
        sudo('screen -d -m simplechaindb load -m ' + m + ' -c ' + c + ' &', pty=False)


# rethinkdb
@task
def start_rethinkdb():
    sudo("service rethinkdb  start")

@task
def stop_rethinkdb():
    sudo("service rethinkdb stop")

@task
def restart_rethinkdb():
    sudo("service rethinkdb restart")

@task
def rebuild_rethinkdb():
    sudo("service rethinkdb index-rebuild -n 2")


# Install and run New Relic
@task
@parallel
def install_newrelic():
    newrelic_license_key = environ.get('NEWRELIC_KEY')
    if newrelic_license_key is None:
        sys.exit('The NEWRELIC_KEY environment variable is not set')
    else:
        # Andreas had this "with settings(..." line, but I'm not sure why:
        # with settings(warn_only=True):
        # Use the installation instructions from NewRelic:
        # http://tinyurl.com/q9kyrud
        # ...with some modifications
        sudo("echo 'deb http://apt.newrelic.com/debian/ newrelic non-free' >> "
             "/etc/apt/sources.list.d/newrelic.list")
        sudo('wget -O- https://download.newrelic.com/548C16BF.gpg | '
             'apt-key add -')
        sudo('apt-get update')
        sudo('apt-get -y --force-yes install newrelic-sysmond')
        sudo('nrsysmond-config --set license_key=' + newrelic_license_key)
        sudo('/etc/init.d/newrelic-sysmond start')


###########################
# Security / Firewall Stuff
###########################

@task
def harden_sshd():
    """Security harden sshd.
    """
    # Disable password authentication
    sed('/etc/ssh/sshd_config',
        '#PasswordAuthentication yes',
        'PasswordAuthentication no',
        use_sudo=True)
    # Deny root login
    sed('/etc/ssh/sshd_config',
        'PermitRootLogin yes',
        'PermitRootLogin no',
        use_sudo=True)


@task
def disable_root_login():
    """Disable `root` login for even more security. Access to `root` account
    is now possible by first connecting with your dedicated maintenance
    account and then running ``sudo su -``.
    """
    sudo('passwd --lock root')


@task
def set_fw():
    # snmp
    sudo('iptables -A INPUT -p tcp --dport 161 -j ACCEPT')
    sudo('iptables -A INPUT -p udp --dport 161 -j ACCEPT')
    # dns
    sudo('iptables -A OUTPUT -p udp -o eth0 --dport 53 -j ACCEPT')
    sudo('iptables -A INPUT -p udp -i eth0 --sport 53 -j ACCEPT')
    # rethinkdb
    sudo('iptables -A INPUT -p tcp --dport 28015 -j ACCEPT')
    sudo('iptables -A INPUT -p udp --dport 28015 -j ACCEPT')
    sudo('iptables -A INPUT -p tcp --dport 29015 -j ACCEPT')
    sudo('iptables -A INPUT -p udp --dport 29015 -j ACCEPT')
    sudo('iptables -A INPUT -p tcp --dport 8080 -j ACCEPT')
    sudo('iptables -A INPUT -i eth0 -p tcp --dport 8080 -j DROP')
    sudo('iptables -I INPUT -i eth0 -s 127.0.0.1 -p tcp --dport 8080 -j ACCEPT')
    # save rules
    sudo('iptables-save >  /etc/sysconfig/iptables')


#########################################################
# Some helper-functions to handle bad behavior of cluster
#########################################################
#
#read blockchain-nodes and set all nodes
@task
@parallel
def  set_allnodes():
    #read by line
    f=open('blockchain-nodes')
    for line in f.readlines():
        temp=line.strip('\r\n').split(" ")
        host=temp[0]
        password=temp[1]
        env['passwords'][host]=password

    # order
    env['hosts']=env['passwords'].keys()


#set on node
@task
@parallel
def  set_node(host,password):
    env['passwords'][host]=password
    env['hosts']=env['passwords'].keys()


###################
# Install Collectd
@task
@parallel
def install_collectd():
    """Installation of Collectd"""
    with settings(warn_only=True):
        sudo("echo 'collectd install' ")
        sudo("echo 'deb http://http.debian.net/debian wheezy-backports-sloppy main contrib non-free' | sudo tee /etc/apt/sources.list.d/backports.list")
        sudo("apt-get update")
        sudo("apt-get install -y --force-yes -t wheezy-backports-sloppy collectd")

# Configure Collectd
@task
@parallel
def configure_collectd():
    """Confiure of Collectd"""
    with settings(warn_only=True):
        # fix: lib version too high
        sudo('ln -sf /lib/x86_64-linux-gnu/libudev.so.?.?.? /lib/x86_64-linux-gnu/libudev.so.0')
        sudo('ldconfig')
        # copy config file to target system
        put('conf/collectd.conf',
            '/etc/collectd/collectd.conf',
            mode=0x0600,
            use_sudo=True)
        # finally restart instance
        sudo('service collectd restart', pty=False)

@task
@parallel
def init_all_nodes():
    with settings(warn_only=True):
         sudo('killall -9 rethinkdb')
         sudo('killall -9 bigchaindb')
         sudo('apt-get purge rabbitmq-server')
         sudo('pip3 uninstall bigchaindb')
         sudo('pip3 uninstall simplechaindb')
         sudo('rm -rf /data/*')
         sudo('rm -rf /localdb/*')

@task
@parallel
def kill_all():
    with settings(warn_only=True):
         sudo('killall -9 rethinkdb')
         sudo('killall -9 simplechaindb')

@task
@parallel
def uninstall_bigchaindb():
    with settings(warn_only=True):
         sudo('pip3 uninstall bigchaindb')
         sudo('pip3 uninstall simplechaindb')