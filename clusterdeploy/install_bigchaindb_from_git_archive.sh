#! /bin/bash

# The set -e option instructs bash to immediately exit
# if any command has a non-zero exit status
set -e

GITBRANCH=master
cd ..
rm -f bigchaindb-archive.tar.gz
git archive $GITBRANCH --format=tar --output=bigchaindb-archive.tar
gzip bigchaindb-archive.tar
mv bigchaindb-archive.tar.gz deploy-cluster-aws
cd deploy-cluster-aws
fab install_bigchaindb_from_git_archive
rm bigchaindb-archive.tar.gz
