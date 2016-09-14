#Simplechaindb

based on [BigchainDB](https://github.com/bigchaindb/bigchaindb)

##Quick Start (Single Node)
A. [Install RethinkDB Server](https://rethinkdb.com/docs/install/ubuntu/)

B. Open a Terminal and run RethinkDB Server with the command:
```text
rethinkdb
```

C. Ubuntu 14.04 already has Python 3.4, so you don't need to install it, but you do need to install a couple other things:
```text
sudo apt-get update
sudo apt-get install g++ python3-dev
```

D. Get the latest version of pip and setuptools:
```text
sudo apt-get install python3-pip
sudo pip3 install --upgrade pip setuptools
```

E. Install the `simplechaindb` Python package from PyPI:
```text
git clone https://git.oschina.net/buaalining/Simplechaindb.git
cd Simplechaindb/clusterdeploy
sudo python3 setup.py install
```

F. Configure and run BigchainDB:
```text
simplechaindb -y configure
simplechaindb start
```

##For Cluster

### Deployment for the first time
```
git clone https://git.oschina.net/buaalining/Simplechaindb.git
cd Simplechaindb/clusterdeploy
vim blockchain-node
./first_setup.sh $NUM_NODES
```

### Deployment for update
```
cd Simplechaindb
git pull
cd clusterdeploy
./update $NUM_NODES
```

### start or stop of cluster
```
cd clusterdeploy
./clustercontrol start|stop
```

## Basic API
* ['GET']  node_info:http://ip:9984/
* ['GET']  get_transaction:http://ip:9984/api/v1/transactions/tx_id=<tx_id>
* ['POST'] create_transaction:http://ip:9984/api/v1/transactions/
* ['GET']  statistics:http://ip:9984/api/v1/statistics/transaction
* ['GET']  generate_key_pair:http://ip:9984/api/v1/system/key/

## Links for BigchainDB
* [BigchainDB.com](https://www.bigchaindb.com/) - the main BigchainDB website, including newsletter signup
