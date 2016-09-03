#Simplechaindb

based on BigchainDB

## 初次安装部署
```
git clone https://git.oschina.net/buaalining/Simplechaindb.git
cd Simplechaindb/clusterdeploy
vim blockchain-node
./first_setup.sh $NUM_NODES
```

## 更新
```
cd Simplechaindb
git pull
cd clusterdeploy
./update $NUM_NODES
```
## 基本API
* 节点基础信息：http://ip:9984/
* get_transaction：http://ip:9984/api/v1/transactions/tx_id=<tx_id>
* ['POST']create_transaction：http://ip:9984/api/v1/transactions/
* 统计：http://ip:9984/api/v1/statistics/transaction
* 生成密钥对：http://ip:9984/api/v1//system/key/

## 启动关闭
```
cd clusterdeploy
./clustercontrol start|stop
```


## Links for BigchainDB
* [BigchainDB.com](https://www.bigchaindb.com/) - the main BigchainDB website, including newsletter signup
* [Whitepaper](https://www.bigchaindb.com/whitepaper/) - outlines the motivations, goals and core algorithms of BigchainDB
* [Roadmap](https://github.com/bigchaindb/org/blob/master/ROADMAP.md)
* [Blog](https://medium.com/the-bigchaindb-blog)
* [Twitter](https://twitter.com/BigchainDB)
* [Google Group](https://groups.google.com/forum/#!forum/bigchaindb)

## Links for Developers
* [Documentation](http://bigchaindb.readthedocs.io/en/latest/) - for developers
* [CONTRIBUTING.md](CONTRIBUTING.md) - how to contribute
* [Community guidelines](CODE_OF_CONDUCT.md)
* [Open issues](https://github.com/bigchaindb/bigchaindb/issues)
* [Open pull requests](https://github.com/bigchaindb/bigchaindb/pulls)
* [Gitter chatroom](https://gitter.im/bigchaindb/bigchaindb)

## Legal
* [Licenses](LICENSES.md) - open source & open content
* [Imprint](https://www.bigchaindb.com/imprint/)
* [Contact Us](https://www.bigchaindb.com/contact/)
