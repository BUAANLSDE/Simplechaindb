# -*- coding: utf-8 -*-\n
"""A list of the public DNS names of all the nodes in this
BigchainDB cluster/federation.
blockchain-nodes：user@xxx.xxx.xxx.xxx:port passwd
public_dns_names:[xxx.xxx.xxx.xxx,yyy.yyy.yyy.yyy,......]
"""
from __future__ import unicode_literals
public_dns_names = []
f=open('blockchain-nodes')
for line in f.readlines():
    temp=line.strip('\r\n').split(" ")
    temp2=temp[0].strip('\r\n').split("@")
    temp3=temp2[1].strip('\r\n').split(":")
    public_dns_name=temp3[0]
    public_dns_names.append(public_dns_name)
