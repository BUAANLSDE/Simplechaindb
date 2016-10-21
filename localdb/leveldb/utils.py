"""Utils to initialize and drop the localdb [levelDB]."""
# bytes can only contain ASCII literal characters.

import plyvel as l
import rethinkdb as r
import bigchaindb
import rapidjson
from localdb import config

import logging

logger = logging.getLogger(__name__)


class LocalDBPool(object):
    """Singleton LocalDBPool encapsulates leveldb`s base ops base on plyvel

    Warn:
        1. leveldb [Only a single process (possibly multi-threaded) can access a particular database at a time.]
        2. multi-thread [Singleton can deal.]
        3. multi process [We`ll can only do is that removes the special dir`s LOCK.]

    Attributes:
        conn:   The dict include the dir link config['database']['tables']

    """

    # Only run once with process  start

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            logger.info('init localpool start')
            cls.instance = super(LocalDBPool, cls).__new__(cls)
            database = config['database']
            parent_dir = database['path']
            block_size = database['block_size']
            write_buffer_size = database['write_buffer_size']
            max_open_files = database['max_open_files']
            lru_cache_size = database['lru_cache_size']
            print('leveldb config %s' %(database.items()))
            cls.instance.conn = dict()
            logger.warn('conn info: ' + str(cls.instance.conn.items()))
            cls.instance.conn['header'] = l.DB(parent_dir + 'header/', create_if_missing=True,write_buffer_size=write_buffer_size,
                                               block_size=block_size, max_open_files=max_open_files,lru_cache_size=lru_cache_size)
            cls.instance.conn['bigchain'] = l.DB(parent_dir + 'bigchain/', create_if_missing=True,write_buffer_size=write_buffer_size,
                                                 block_size=block_size,max_open_files=max_open_files,lru_cache_size=lru_cache_size)
            cls.instance.conn['votes'] = l.DB(parent_dir + 'votes/', create_if_missing=True,write_buffer_size=write_buffer_size,
                                              block_size=block_size,max_open_files=max_open_files,lru_cache_size=lru_cache_size)
            logger.info('LocalDBPool conn ' + str(cls.instance.conn.items()))
            logger.info('init localpool end')
        return cls.instance


def init():
    """ Init leveldb database when process.py run"""

    logger.info('leveldb init...')
    conn_bigchain = get_conn('bigchain')
    conn_header = get_conn('header')
    logger.info('leveldb/header init...')
    logger.info('leveldb/header init host...' + str(bigchaindb.config['database']['host']))
    logger.info('leveldb/header init public_key...' + str(bigchaindb.config['keypair']['public']))
    logger.info('leveldb/header init private_key...' + str(bigchaindb.config['keypair']['private']))

    update(conn_header, 'host', bigchaindb.config['database']['host'])
    update(conn_header, 'public_key', bigchaindb.config['keypair']['public'])
    update(conn_header, 'private_key', bigchaindb.config['keypair']['private'])

    block_num = int(get_withdefault(conn_header, 'block_num', 0))
    genesis_block_id = get_withdefault(conn_header,'genesis_block_id','0')
    if block_num == 0 :
        genesis_block = r.db('bigchain').table('bigchain').order_by(r.asc(r.row['block']['timestamp'])).limit(1).run(
            bigchaindb.Bigchain().conn)[0]
        genesis_block_id = genesis_block['id']
        genesis_block_json_str = rapidjson.dumps(genesis_block)
        insert(conn_bigchain, genesis_block_id, genesis_block_json_str)
        insert(conn_header, 'genesis_block_id', genesis_block_id)
        insert(conn_header, 'block_num', 1)
        insert(conn_header, 'current_block_id', genesis_block_id)
    logger.info('leveldb/header genesis_block_id...' + str(genesis_block_id))
    logger.info('leveldb init done')


def close(conn):
    """Close the conn
    Args:
        conn: the leveldb dir pointer

    Returns:

    """

    if conn:
        conn.close()
        logger.info('leveldb close conn ... ' + str(conn))


def close_all():
    """Close all databases dir """

    tables = config['database']['tables']
    logger.info('leveldb close all databases '+str(tables))
    result=[]
    for table in tables:
        if table is not None:
            try:
                dir = config['database']['path']+table+'/'
                close(dir)
                result.append(dir)
            except:
                # print(table + ' is not exist')
                continue
    logger.info('leveldb close all...' + str(result))


def get_conn(name):
    """Insert the value with the special key

    Args:
        name: the leveldb dir name

    Returns:
            the leveldb dir pointer
    """

    return LocalDBPool().conn[name]


def insert(conn,key,value,sync=False):
    """Insert the value with the special key

      Args:
          conn: the leveldb dir pointer
          key:
          sync(bool) – whether to use synchronous writes

      Returns:

    """

    # logger.info('leveldb insert...' + str(key) + ":" +str(value))
    conn.put(bytes(str(key),config['encoding']),bytes(str(value),config['encoding']),sync=sync)


def batch_insertOrUpdate(conn,dict,transaction=False,sync=False):
    """Batch insert or update the value with the special key in dict

    Args:
        conn: the leveldb dir pointer
        dict:
        transaction(bool) –  whether to enable transaction-like behaviour when
        the batch is used in a with block
        sync(bool) – whether to use synchronous writes

    Returns:

    """

    with conn.write_batch(transaction=transaction,sync=sync) as b:
        for key in dict:
            # logger.warn('key: ' + str(key) + ' --- value: ' + str(dict[key]))
            b.put(bytes(str(key),config['encoding']),bytes(str(dict[key]),config['encoding']))


def delete(conn,key,sync=False):
    """Delete the value with the special key

    Args:
        conn: the leveldb dir pointer
        key:
        sync(bool) – whether to use synchronous writes

    Returns:

    """

    # logger.info('leveldb delete...' + str(key) )
    conn.delete(bytes(str(key),config['encoding']),sync=sync)


def batch_delete(conn,dict,transaction=False,sync=False):
    """Batch delete the value with the special key in dict

    Args:
        conn: the leveldb dir pointer
        dict:
        transaction(bool) –  whether to enable transaction-like behaviour when
        the batch is used in a with block
        sync(bool) – whether to use synchronous writes

    Returns:

    """

    with conn.write_batch(transaction=transaction,sync=sync) as b:
        for key,value in dict:
            b.delete(bytes(str(key),config['encoding']))


def update(conn,key,value,sync=False):
    """Update the value with the special key

    Args:
        conn: the leveldb dir pointer
        key:
        value(str) – value to set
        sync(bool) – whether to use synchronous writes

    Returns:

    """

    # logger.info('leveldb update...' + str(key) + ":" +str(value))
    conn.put(bytes(str(key),config['encoding']), bytes(str(value),config['encoding']),sync=sync)


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

def get_prefix(conn,prefix):
    """Get the records with the special prefix.

    block-v1=v1
    block-v2=v2
    block-v3=v3
    prefix = 'block'  => {'-v1':'v1','-v2':'v2','-v3':'v3'}
    prefix = 'block-' => {'v1':'v1','v2':'v2','v3':'v3'}

    Args:
        conn: the leveldb dir pointer
        prefix: the key start with,before '-'

    Returns:
         the dict
    """

    if conn:
        # logger.warn(str(conn) + ' , ' + str(prefix))
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
    """Get the value with the key.

    Args:
        conn: the leveldb dir pointer
        key:
        default_value: if value is None,it will return

    Returns:
        the string
    """

    # logger.info('leveldb get...' + str(key) + ",default_value=" + str(default_value))
    # get the value for the bytes_key,if not exists return defaule_value
    bytes_val = conn.get(bytes(str(key),config['encoding']),bytes(str(default_value),config['encoding']))
    # return bytes(bytes_val).decode(config['encoding'])
    # logger.info('leveldb get...' + str(key) + ",default_value=" + bytes(bytes_val).decode(config['encoding']))
    return bytes(bytes_val).decode(config['encoding'])