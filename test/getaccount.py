__author__ = 'PC-LiNing'

from bigchaindb import tool

currency_list=[ {'txid':"B",'payload':{'previous':'C'}},{'txid':"A",'payload':{'previous':'B'}},
                        {'txid':"C",'payload':{'previous':'D'}},{'txid':"D",'payload':{'previous':'genesis'}}]

print(tool.sort_currency_list(currency_list))