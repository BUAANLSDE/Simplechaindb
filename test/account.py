__author__ = 'PC-LiNing'

from bigchaindb import Bigchain

# b=Bigchain()

public_key='wreXXdHnbZmpyNxTCBscdtNMutF1VhL7v5n9zc9gyi2'
private_key='8Rwr5SUiE1ijAenpc4DawwWWSK6D2K2Fq4hzdKseXifr'

# tx = b.get_current_balance(public_key)
# print(tx)

tx={'version': 1, 'id': '8ddabf38984f640ff73ea47c416f57d53386233dd68d81cd833863ccedae41cb', 'transaction': {'operation': 'CREATE', 'conditions': [{'condition': {'uri': 'cc:4:20:Dg1_7t9By2clG9zcMfy0OxYWFyF284brzpHcStQi4-M:96', 'details': {'type_id': 4, 'type': 'fulfillment', 'public_key': 'wreXXdHnbZmpyNxTCBscdtNMutF1VhL7v5n9zc9gyi2', 'signature': None, 'bitmask': 32}}, 'cid': 0, 'new_owners': ['wreXXdHnbZmpyNxTCBscdtNMutF1VhL7v5n9zc9gyi2']}], 'timestamp': '1469021068', 'data': {'payload': {'account': 0, 'amount': 0, 'asset': '123456789', 'previous': '', 'msg': 'create_asset', 'category': 'asset', 'issue': 'create', 'trader': ''}, 'uuid': '1b48553a-cfb4-46f6-bee3-aad87064914f'}, 'fulfillments': [{'input': None, 'current_owners': ['FxvxFdL9TJmAd1bDQVg3bs5zvS36Vs2jsd79ww2e7dLc'], 'fid': 0, 'fulfillment': 'cf:4:3leQ3nILy2ktD6h1hv3QNHZtvzJAZ6ptl0vkLk_mf-Fh1iuScYT6rGON_dNONGdcE2K_BQ1LqqdmJfDWjVfZ34mPFpEp9lfND1kU9secf8r_-2bvXdcfcC6d9HrsVJ4M'}]}}

print(tx['id'])
print(tx['transaction']['conditions'][0]['new_owners'])