__author__ = 'PC-LiNing'

from fabric.api import sudo, env, hosts
from fabric.api import task, parallel
from fabric.context_managers import settings
from fabric.operations import run, put

env['hosts']=['localhost']
env['user']='bc2'
env['password']='bc2'

# Install RethinkDB
@task
@parallel
def install_rethinkdb():
    """Installation of RethinkDB"""
    with settings(warn_only=True):
        # preparing filesystem
        sudo("mkdir -p /data")
        # Locally mounted storage (m3.2xlarge, but also c3.xxx)
        try:
            sudo("umount /mnt")
            sudo("mkfs -t ext4 /dev/xvdb")
            sudo("mount /dev/xvdb /data")
        except:
            pass

        # persist settings to fstab
        sudo("rm -rf /etc/fstab")
        sudo("echo 'LABEL=cloudimg-rootfs	/	 ext4     defaults,discard    0   0' >> /etc/fstab")
        sudo("echo '/dev/xvdb  /data        ext4    defaults,noatime    0   0' >> /etc/fstab")
        # activate deadline scheduler
        with settings(sudo_user='root'):
            sudo("echo deadline > /sys/block/xvdb/queue/scheduler")
        # install rethinkdb
        sudo("echo 'deb http://download.rethinkdb.com/apt trusty main' | sudo tee /etc/apt/sources.list.d/rethinkdb.list")
        sudo("wget -qO- http://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -")
        sudo("apt-get update")
        sudo("apt-get -y install rethinkdb")
        # change fs to user
        sudo('chown -R rethinkdb:rethinkdb /data')
        # copy config file to target system
        #put('conf/rethinkdb.conf','/etc/rethinkdb/instances.d/instance1.conf',mode=0600,use_sudo=True)
        # initialize data-dir
        sudo('rm -rf /data/*')
        # finally restart instance
        #sudo('/etc/init.d/rethinkdb restart')
