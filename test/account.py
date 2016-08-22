__author__ = 'PC-LiNing'

from bigchaindb import Bigchain

b=Bigchain()

public_key='ECP3CFJAWpfB3xn7CzFDN4QCJ1Kh1dtbbSUWGTRYaQer'

tx = b.get_current_balance(public_key)
print(tx)

