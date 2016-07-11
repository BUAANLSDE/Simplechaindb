__author__ = 'PC-LiNing'

import thriftpy

pingpong_thrift = thriftpy.load("UserService.thrift", module_name="UserService_thrift")

from thriftpy.rpc import make_client

#client = make_client(pingpong_thrift.UserService, '127.0.0.1', 7911)
#print(client.whatIsName("thrift!"))

from thriftpy.transport import TFramedTransport
from thriftpy.transport import TSocket
from thriftpy.protocol  import TCompactProtocol
from thriftpy.protocol  import TCompactProtocolFactory
from thriftpy.transport import TFramedTransportFactory
from thriftpy.rpc import client_context

Tframe=TFramedTransportFactory()
Pcompact=TCompactProtocolFactory()

with client_context(service=pingpong_thrift.UserService,host='127.0.0.1',port=7911,proto_factory=Pcompact,trans_factory=Tframe,timeout=100*1000) as client:
    print(client.whatIsName("thrift!"))
