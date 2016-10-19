


import plyvel as l
import rapidjson
from localdb import config

parent_dir = config['database']['path']


conn_bigchain = l.DB(parent_dir + 'bigchain/').snapshot()


def get_obj_json(str_bytes):

    if str_bytes:
        return rapidjson.loads(bytes(str_bytes).decode('utf-8'))

def get(conn, key):
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



raw_iterator =  conn_bigchain.raw_iterator() # invalid,must move to the first
print('raw_iterator: ' + str(raw_iterator))
# move to the first
if raw_iterator:
    raw_iterator.seek_to_first()
else:
    print('None')
    #
#   print('raw_iterator valid(): ' + str(raw_iterator.valid()))

    # move to the last
    # raw_iterator.seek_to_last()
    # print('raw_iterator valid(): ' + str(raw_iterator.valid()))
    # print("\nraw_item " + str(raw_iterator.item()))


count = 0

while raw_iterator.valid() and raw_iterator.item() :
    count = count + 1
    item = raw_iterator.item() # bytes json string
    item_obj = get_obj_json(item[1])
    # print('The %dth records is: \n %s\n' %(count,item))
    # print('The %dth records`s key  is: \n %s\n' %(count,str(item[0])))
    # print('The %dth records`s value  is: \n %s\n' %(count,item.value[1]))

    print('The current id is : %s' %str(item_obj['id']))
    # print('The %dth records is: \n %s\n' %(count,str(item_obj)))

    # Only move ,no returnVal
    raw_iterator.next()

print('The total records is: %d' %count)

