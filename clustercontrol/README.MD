## 总体说明

使用python  fabric进行远程登录、操作 ； 对fabfile.py中的操作进行组合，封装为shell脚本。

控制、监测集群、节点的行为。

##文件说明

blockchain-nodes 为集群节点的信息，每行一条。格式: user@host:port  password

fabfile.py   读取blockchain-nodes信息或用户指定参数，进行集群、节点行为控制。

clustercontrol.sh  集群控制

./clustercontrol.sh  start    启动整个集群
./clustercontrol.sh  stop    关闭整个集群

startnode.sh 、stopnode.sh   节点控制

./startnode.sh  -h user@host   -p password   [ -r ]  [ -b ]   启动指定的节点。 -r 启动 该节点上的rethinkdb ，-b 启动该节点上的bigchaindb。

./stopnode.sh  -h user@host   -p password   [ -r ]  [ -b ]   关闭指定的节点。 -r 关闭 该节点上的rethinkdb ，-b 关闭该节点上的bigchaindb。



目前的功能还不多，编写的还很简陋。
