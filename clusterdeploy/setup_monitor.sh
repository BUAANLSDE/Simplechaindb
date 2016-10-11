#! /bin/bash
echo deb https://apt.dockerproject.org/repo ubuntu-trusty main > /etc/apt/sources.list.d/docker.list
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
apt-get update
apt-get -y --force-yes install docker docker-engine
wget -O /usr/local/bin/docker-compose https://github.com/docker/compose/releases/download/1.8.0/docker-compose-`uname -s`-`uname -m`
chmod +x /usr/local/bin/docker-compose
wget -q https://raw.githubusercontent.com/BUAANLSDE/Simplechaindb/master/docker-compose-monitor.yml
INFLUXDB_DATA=/data/monitor docker-compose -f docker-compose-monitor.yml up