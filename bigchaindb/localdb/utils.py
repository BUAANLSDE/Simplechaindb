"""Utils to initialize and drop the localdb [levelDB]."""
# bytes can only contain ASCII literal characters.

import plyvel as l
import logging
import rethinkdb as r
import bigchaindb
logger = logging.getLogger(__name__)

# path should be exist
config = {
    'database': {
        'path': '/data/leveldb/',
        'tables':['header','bigchain','votes']
    },
    'encoding':'utf-8'
}

def init():
    """ init leveldb database by conn"""
    logger.info('leveldb init...')
    conn_bigchain = create_database('bigchain')
    create_database('votes')
    conn_header = create_database('header')

    logger.info('leveldb init...')
    logger.info('leveldb/header init...')
    logger.info('leveldb/header init host...' + str(bigchaindb.config['database']['host']))
    logger.info('leveldb/header init public_key...' + str(bigchaindb.config['keypair']['public']))
    logger.info('leveldb/header init private_key...' + str(bigchaindb.config['keypair']['private']))

    if conn_header is None or conn_header.closed:
        conn_header = get_conn('header')

    update(conn_header, 'host', bigchaindb.config['database']['host'])
    update(conn_header, 'public_key', bigchaindb.config['keypair']['public'])
    update(conn_header, 'private_key', bigchaindb.config['keypair']['private'])

    block_num = int(get_withdefault(conn_header, 'block_num', 0))
    if block_num == 0 :
        genesis_block = r.db('bigchain').table('bigchain').order_by(r.asc(r.row['block']['timestamp'])).limit(1).run(
            bigchaindb.Bigchain().conn)[0]
        genesis_block_id = genesis_block['id']
        insert(conn_bigchain, genesis_block_id, genesis_block)
        insert(conn_header, 'block_num', 1)
        insert(conn_header, 'current_block_id', genesis_block_id)

    logger.info('leveldb init done')


def destroy():
    """ close all databases dir """
    tables = config['database']['tables']
    logger.info('leveldb drop all databases '+str(tables))
    for table in tables:
        if table is not None:
            try:
                dir = config['database']['path']+table+'/'
                l.destroy_db(dir)
            except:
                # print(table + ' is not exist')
                continue
    logger.info('leveldb destroy...')


def close():
    """ close all databases dir """
    tables = config['database']['tables']
    logger.info('leveldb close all databases '+str(tables))
    for table in tables:
        if table is not None:
            try:
                conn = get_conn(table)
                close_database(conn)
                # print('close ' +table + ' successfully')
            except:
                # print(table + ' is not exist')
                continue
    logger.info('leveldb close...')


def get_conn(name,path=config['database']['path']):
    """ get the leveldb """
    return l.DB(path+name+'/')


def create_database(name,path=config['database']['path']):
    """ create leveldb database if missing"""
    if name is None:
        raise  l.Error('database name can`t None!')
    operation = 'open'
    conn = None
    try:
        conn = get_conn(name)
    except  Exception as create_database_except:
        operation = 'create'
        # dir = path + name + '/'
        # isExists =  os.path.exists(path)
        # not exist ,create
        # if not isExists:
        #     try:
        #         os.makedirs(path)
        #     except Exception as create_leveldb_error:
        #         raise  create_leveldb_error
        conn = l.DB(path + name + '/', create_if_missing=True)
    finally:
        # logger.info('dir:' + str(dir) + ',isExists:'+str(create_leveldb_error))
        logger.info('leveldb ' + operation + ' dir '+ name + ',position: ' + path + name + '/')
        return conn


def close_database(conn):
    """ close leveldb database by conn"""
    logger.info('leveldb close...')
    del conn


def insert(conn,key,value):
    # logger.info('leveldb insert...' + str(key) + ":" +str(value))
    conn.put(bytes(str(key),config['encoding']),bytes(str(value),config['encoding']))


def batch_insert(conn,dict):
    with conn.write_batch() as b:
        for key in dict:
            # logger.warn('key: ' + str(key) + ' --- value: ' + str(dict[key]))
            b.put(bytes(str(key),config['encoding']),bytes(str(dict[key]),config['encoding']))


def delete(conn,key):
    # logger.info('leveldb delete...' + str(key) )
    conn.delete(bytes(str(key),config['encoding']))


def batch_delete(conn,dict):
    with conn.write_batch() as b:
        for key,value in dict:
            b.delete(bytes(str(key),config['encoding']))


def update(conn,key,value):
    # logger.info('leveldb update...' + str(key) + ":" +str(value))
    conn.put(bytes(str(key),config['encoding']), bytes(str(value),config['encoding']))


def get(conn,key):
    # logger.info('leveldb get...' + str(key))
    # get the value for the bytes_key,if not exists return None
    # bytes_val = conn.get_property(bytes(key, config['encoding']))
    bytes_val = conn.get(bytes(str(key), config['encoding']))
    return bytes(bytes_val).decode(config['encoding'])


def get_prefix(conn,prefix):
    """
        block-v1=v1
        block-v2=v2
        block-v3=v3
        prefix = 'block'  => {'-v1':'v1','-v2':'v2','-v3':'v3'}
        prefix = 'block-' => {'v1':'v1','v2':'v2','v3':'v3'}
        """
    logger.warn(str(conn) + ' , ' + str(prefix))
    if conn:
        bytes_dict_items = conn.prefixed_db(bytes(str(prefix),config['encoding']))
        result = {}
        for key,value in bytes_dict_items:
            key = bytes(key).decode(config['encoding'])
            value = bytes(value).decode(config['encoding'])
            result[key] = value
        return result
    else:
        return None


def get_withdefault(conn,key,default_value):
    # logger.info('leveldb get...' + str(key) + ",default_value=" + str(default_value))
    # get the value for the bytes_key,if not exists return defaule_value
    bytes_val = conn.get(bytes(str(key),config['encoding']),bytes(str(default_value),config['encoding']))
    # return bytes(bytes_val).decode(config['encoding'])
    # logger.info('leveldb get...' + str(key) + ",default_value=" + bytes(bytes_val).decode(config['encoding']))
    return bytes(bytes_val).decode(config['encoding'])