__author__ = 'PC-LiNing'

from bigchaindb import Bigchain
from bigchaindb import tool

b=Bigchain()

public_key='wreXXdHnbZmpyNxTCBscdtNMutF1VhL7v5n9zc9gyi2'
private_key='8Rwr5SUiE1ijAenpc4DawwWWSK6D2K2Fq4hzdKseXifr'

currency_list=b.get_bigchain_currency_list(public_key)
currency_queue=tool.sort_currency_list(currency_list)
print(currency_queue)