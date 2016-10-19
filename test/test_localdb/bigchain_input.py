

import plyvel as l
import rapidjson
from localdb import config

parent_dir = config['database']['path']


conn_bigchain = l.DB(parent_dir + 'bigchain/').snapshot()


def get_obj_json(str_bytes):

    if str_bytes:
        return rapidjson.loads(bytes(str_bytes,encoding='utf-8').decode('utf-8'))

def get(conn,key):
    """Get the value with the special key

    Args:
        conn: the leveldb dir pointer
        key:

    Returns:
         the string
    """

    # logger.info('leveldb get...' + str(key))
    # get the value for the bytes_key,if not exists return None
    # bytes_val = conn.get_property(bytes(key, config['encoding']))
    bytes_val = conn.get(bytes(str(key), config['encoding']))
    if bytes_val:
        return bytes(bytes_val).decode(config['encoding'])
    else:
        return None

while True:
    block_id = input('please input the block_id:')
    if block_id is None:
        break

    print('type ' + str(type(block_id)) + ' val ' + str(block_id))
    block = get(conn_bigchain,block_id)
    if block:
        block_obj = get_obj_json(block)
        print('block ' + str(block_obj))
    else:
        print('block is None')

