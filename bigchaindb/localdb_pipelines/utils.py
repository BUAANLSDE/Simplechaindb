"""Utility classes and functions to work with the pipelines."""


import rethinkdb as r
from multipipes import Node

from bigchaindb import Bigchain
import bigchaindb.localdb.utils as leveldb
import bigchaindb.localdb_pipelines.local_global as lg

import logging

logger = logging.getLogger(__name__)

class ChangeFeed(Node):

    INSERT = 1
    DELETE = 2
    UPDATE = 4

    def __init__(self, table, operation, prefeed=None):
        """Create a new RethinkDB ChangeFeed.

        Args:
            table (str): name of the table to listen to for changes.
            operation (int): can be ChangeFeed.INSERT, ChangeFeed.DELETE, or
                ChangeFeed.UPDATE. Combining multiple operation is possible using
                the bitwise ``|`` operator
                (e.g. ``ChangeFeed.INSERT | ChangeFeed.UPDATE``)
            prefeed (iterable): whatever set of data you want to be published
                first.
        """

        super().__init__(name='local_changefeed')
        self.prefeed = prefeed if prefeed else []
        self.table = table
        self.operation = operation
        self.bigchain = Bigchain()

    def run_forever(self):
        for element in self.prefeed:
            logger.info('prefeed' + str(self.prefeed))
            self.outqueue.put(element)

        for change in r.table(self.table).changes().run(self.bigchain.conn):

            is_insert = change['old_val'] is None
            is_delete = change['new_val'] is None
            is_update = not is_insert and not is_delete

            if is_insert and (self.operation & ChangeFeed.INSERT):
                #TODO new block enqueue wx
                if self.table == 'bigchain':
                    lg.async_blocks_queue(self.deal_block(change['new_val']),None)
                elif self.table == 'votes':
                    lg.async_votes_queue(self.deal_vote(change['new_val']), None)
                    #no pipe process ,no outqueue
                    # self.outqueue.put(change['new_val'])
            elif is_delete and (self.operation & ChangeFeed.DELETE):
                pass
                # self.outqueue.put(change['old_val'])
            elif is_update and (self.operation & ChangeFeed.UPDATE):
                pass
                # self.outqueue.put(change['new_val'])

    def deal_block(self, block):
        conn_header = leveldb.get_conn('header')
        conn_bigchain = leveldb.get_conn('bigchain')
        block_id = block['id']
        leveldb.insert(conn_bigchain, block_id, block)
        block_num = leveldb.get(conn_header, 'block_num')
        block_num = int(block_num)
        block_num = block_num + 1

        leveldb.update(conn_header, 'block_num', block_num)
        leveldb.update(conn_header, 'current_block_id', block_id)
        # self.get_base_info(conn_header,conn_bigchain)

    def deal_vote(self, vote):
        conn_votes = leveldb.get_conn('votes')
        previous_block = vote['vote']['previous_block']
        node_pubkey = vote['node_pubkey']
        vote_key = previous_block + '-' + node_pubkey
        # logger.info('vote_key:\n' + str(vote_key))
        leveldb.insert(conn_votes, vote_key, vote)
        # self.get_votes_for_block(conn_votes,previous_block)

    def get_base_info(self,conn_header,conn_bigchain):
        current_bid = leveldb.get(conn_header,'current_block_id')
        logger.info('block_num: ' + str(leveldb.get(conn_header,'block_num')) + ',\ncurrent_block_id ' +
                    current_bid)
        # logger.info('current_block: ' + str(leveldb.get(conn_bigchain,current_bid)))


    def get_votes_for_block(self,conn_votes,block_id):
        votess = leveldb.get_prefix(conn_votes,block_id+'-')
        # logger.iinfo(str(block_id) + ' votes :\n' + str(votess))
