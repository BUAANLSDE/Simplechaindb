#Simplechaindb

based on [BigchainDB](https://github.com/bigchaindb/bigchaindb)

##单节点 Quick Start
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

E. Install the `bigchaindb` Python package from PyPI:
```text
sudo python3 setup.py install
```

F. Configure and run BigchainDB:
```text
simplechaindb -y configure
simplechaindb start
```

##集群

### 初次部署
```
git clone https://git.oschina.net/buaalining/Simplechaindb.git
cd Simplechaindb/clusterdeploy
vim blockchain-node
./first_setup.sh $NUM_NODES
```

### 更新
```
cd Simplechaindb
git pull
cd clusterdeploy
./update $NUM_NODES
```

### 启动|关闭
```
cd clusterdeploy
./clustercontrol start|stop
```

## 基本API
* 节点基础信息：http://ip:9984/
* get_transaction：http://ip:9984/api/v1/transactions/tx_id=<tx_id>
* ['POST']create_transaction：http://ip:9984/api/v1/transactions/
* 统计：http://ip:9984/api/v1/statistics/transaction
* 生成密钥对：http://ip:9984/api/v1//system/key/

## Links for BigchainDB
* [BigchainDB.com](https://www.bigchaindb.com/) - the main BigchainDB website, including newsletter signup
