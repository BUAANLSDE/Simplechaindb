

import localdb.leveldb.utils as leveldb

import logging
import rapidjson

logger = logging.getLogger(__name__)


class Methods:
    conn_header = leveldb.LocalDBPool().conn['header']
    conn_bigchain = leveldb.LocalDBPool().conn['bigchain']
    conn_votes = leveldb.LocalDBPool().conn['votes']

    @staticmethod
    def deal_block(block):
        block = bytes(block).decode()
        block_json_str = block
        block = rapidjson.loads(block)
        logger.info('block deal ing...' + str(block))
        block_id = block['id']
        logger.info('block_id is : ' + str(block_id))
        leveldb.insert(Methods.conn_bigchain, block_id, block_json_str)
        block_num = leveldb.get(Methods.conn_header, 'block_num')
        block_num = int(block_num)
        block_num = block_num + 1
        leveldb.update(Methods.conn_header, 'block_num', block_num)
        leveldb.update(Methods.conn_header, 'current_block_id', block_id)
        # Methods.get_base_info(Methods.conn_header,Methods.conn_bigchain)

    @staticmethod
    def deal_vote(vote):
        vote = bytes(vote).decode()
        vote_json_str = vote
        vote = rapidjson.loads(vote)
        logger.info('vote deal ing... ' + str(vote))
        previous_block = vote['vote']['previous_block']
        node_pubkey = vote['node_pubkey']
        vote_key = previous_block + '-' + node_pubkey
        logger.info('vote_key:\n' + str(vote_key))
        leveldb.insert(Methods.conn_votes, vote_key, vote_json_str)
        # Methods.get_votes_for_block(Methods.conn_votes,previous_block)


    @staticmethod
    def get_base_info(conn_header,conn_bigchain):
        current_bid = leveldb.get(conn_header,'current_block_id')
        logger.info('block_num: ' + str(leveldb.get(conn_header,'block_num')) + ',\ncurrent_block_id ' +
                    current_bid)
        # logger.info('current_block: ' + str(leveldb.get(conn_bigchain,current_bid)))


    @staticmethod
    def get_votes_for_block(conn_votes, block_id):
        votess = leveldb.get_prefix(conn_votes, block_id + '-')
        logger.info(str(block_id) + ' votes :\n' + str(votess))