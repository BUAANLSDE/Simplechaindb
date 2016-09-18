"""Utils to initialize and drop the localdb [levelDB]."""
# bytes can only contain ASCII literal characters.

import os
import plyvel as l
import logging

logger = logging.getLogger(__name__)
# path should be exist
config = {
    'database': {
        'path': '/data/leveldb/',
        'tables':['header','bigchain','votes']
    },
    'encoding':'utf-8'
}
    # default_path = "/tmp/leveldb_data/"
def init():
    """ init leveldb database by conn"""
    logger.info('leveldb init...')
    local_header = create_database('header')
    local_bigchain = create_database('bigchain')
    local_votes = create_database('votes')
    logger.info('leveldb init done')

def destroy():
    """ drop all databases dir """
    tables = config['database']['tables']
    logger.info('leveldb drop all databases '+str(tables))
    for table in tables:
        if table is not None:
            try:
                conn = get_conn(table)
                drop_database(conn)
                # print('drop ' +table + ' successfully')
            except:
                # print(table + ' is not exist')
                continue
    logger.info('leveldb create...')

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
        logger.info('leveldb ' + operation + ' table '+ name + ',position: ' + path + name + '/')
        return conn


def drop_database(conn):
    """ drop leveldb database by conn"""
    logger.info('leveldb delete...')
    del conn

def insert(conn,key,value):
    # logger.info('leveldb inisert...' + str(key) + ":" +str(value))
    conn.put(bytes(key,config['encoding']),bytes(value,config['encoding']))

def batch_insert(conn,dict):
    with conn.write_batch() as b:
        for key in dict:
            # logger.warn('key: ' + str(key) + ' --- value: ' + str(dict[key]))
            b.put(bytes(key,config['encoding']),bytes(str(dict[key]),config['encoding']))

def delete(conn,key):
    # logger.info('leveldb delete...' + str(key) )
    conn.delete(bytes(key,config['encoding']))

def batch_delete(conn,dict):
    with conn.write_batch() as b:
        for key,value in dict:
            b.delete(bytes(key,config['encoding']))

def update(conn,key,value):
    # logger.info('leveldb update...' + str(key) + ":" +str(value))
    conn.put(bytes(key,config['encoding']), bytes(value,config['encoding']))

def get(conn,key):
    # logger.info('leveldb get...' + str(key))
    # get the value for the bytes_key,if not exists return None
    bytes_val = conn.get_property(bytes(key, config['encoding']))
    return bytes(bytes_val).decode(config['encoding'])

def get(conn,key,*default_value):
    # logger.info('leveldb get...' + str(key) + ",default_value=" + str(default_value))
    # get the value for the bytes_key,if not exists return defaule_value
    bytes_val = conn.get(bytes(key,config['encoding']),default_value)
    return bytes(bytes_val).decode(config['encoding'])