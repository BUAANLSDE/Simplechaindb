__author__ = 'PC-LiNing'

from fabric.api import sudo, env, hosts
from fabric.api import task, parallel
from fabric.contrib.files import sed
from fabric.operations import run, put
from fabric.context_managers import settings

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


@task
@parallel
def test():
    with settings(warn_only=True):
        sudo("hostname")


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



#bigchaindb

#Start BigchainDB using screen
@task
def start_bigchaindb():
    sudo("screen -d -m simplechaindb start &",pty=False)

@task
def stop_bigchaindb():
    sudo("kill `ps -ef|grep simplechaindb | grep -v grep|awk '{print $2}'` ")


# install tools
@task
@parallel
def  install_screen():
    sudo("apt-get -y install screen")
