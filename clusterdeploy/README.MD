#clusterdeploy
##shell+fabric+python

###部署（顺序）
```
配置blockchain-nodes
chmod +x *.sh
sed -i 's/\r$//' *.sh(如果出现^M问题)

./install_base_software.sh
./install_rethinkdb.sh
./configure_rethinkdb.sh
./install_bigchaindb_from_git_archive.sh
./configure_bigchaindb.sh confiles $NUM_NODES($1=<dir> $2=num)
```
