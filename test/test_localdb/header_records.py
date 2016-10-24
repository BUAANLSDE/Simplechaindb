

import plyvel as l
import rapidjson
from localdb import config

parent_dir = config['database']['path']

 # conn['header'] = l.DB(parent_dir + 'header/', create_if_missing=True)
 # conn['bigchain'] = l.DB(parent_dir + 'bigchain/', create_if_missing=True)
 # conn['votes'] = l.DB(parent_dir + 'votes/', create_if_missing=True)

conn_header = l.DB(parent_dir + 'header/').snapshot()



def get_obj_json(str_bytes):

    if str_bytes:
        return rapidjson.loads(bytes(str_bytes).decode('utf-8'))

# parent_dir = config['database']['path']
# conn['header'] = l.DB(parent_dir + 'header/', create_if_missing=False)
# conn['bigchain'] = l.DB(parent_dir + 'bigchain/', create_if_missing=False)
# conn['votes'] = l.DB(parent_dir + 'votes/', create_if_missing=False)

raw_iterator =  conn_header.raw_iterator() # invalid,must move to the first
print('raw_iterator: ' + str(raw_iterator))
# move to the first
raw_iterator.seek_to_first()
print('raw_iterator valid(): ' + str(raw_iterator.valid()))

# move to the last
# raw_iterator.seek_to_last()
# print('raw_iterator valid(): ' + str(raw_iterator.valid()))
# print("\nraw_item " + str(raw_iterator.item()))


count = 0

while raw_iterator.valid() and raw_iterator.item() :
    count = count + 1
    item = raw_iterator.item() # bytes json string
    print('The %dth records is: \n %s\n' %(count,item))
    # print('The %dth records`s key  is: \n %s\n' %(count,str(item[0])))
    # print('The %dth records`s value  is: \n %s\n' %(count,item.value[1]))

    # print('The %dth records is: \n %s\n' %(count,str(item_obj)))

    # Only move ,no returnVal
    raw_iterator.next()

print('The total records is: %d' %count)

