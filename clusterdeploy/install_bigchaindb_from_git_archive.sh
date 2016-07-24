#! /bin/bash

# The set -e option instructs bash to immediately exit
# if any command has a non-zero exit status
set -e


cd ..
rm -f bigchaindb-archive.tar.gz
git archive master --format=tar --output=bigchaindb-archive.tar
gzip bigchaindb-archive.tar
mv bigchaindb-archive.tar.gz clusterdeploy
cd clusterdeploy
fab install_bigchaindb_from_git_archive
rm bigchaindb-archive.tar.gz
