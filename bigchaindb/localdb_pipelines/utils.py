"""Utility classes and functions to work with the pipelines."""


import rethinkdb as r
from multipipes import Node

from bigchaindb import Bigchain
import bigchaindb.localdb.utils as leveldb
from bigchaindb.localdb_pipelines.async_queue import DealQueue
from bigchaindb.localdb_pipelines.local_deal import LocalDeal
import bigchaindb.localdb_pipelines.task_queue as task
import logging

logger = logging.getLogger(__name__)

class LocalChangeFeed(Node):

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
        super().__init__(name='localchangefeed')
        self.prefeed = prefeed if prefeed else []
        self.table = table
        self.operation = operation
        self.bigchain = Bigchain()
        self.deal_queue = DealQueue()
        self.conn_header = leveldb.get_conn('header')
        self.conn_bigchain = leveldb.get_conn('bigchain')
        self.conn_votes = leveldb.get_conn('votes')

    def run_forever(self):
        for element in self.prefeed:
            logger.info('prefeed' + str(self.prefeed))
            self.outqueue.put(element)

        for change in r.table(self.table).changes().run(self.bigchain.conn):

            is_insert = change['old_val'] is None
            is_delete = change['new_val'] is None
            is_update = not is_insert and not is_delete

            if is_insert and (self.operation & LocalChangeFeed.INSERT):
                #TODO new block enqueue wx
                if self.table == 'bigchain':
                    block = change['new_val']
                    # task.async_blocks_queue(self.deal_block,task.handle_result,block)
                    self.deal_queue.add_block(block)
                    logger.info('address ... ' + str(self.deal_queue))
                    # self.deal_queue.get_blocks_queue()
                    # self.deal_block(block)
                elif self.table == 'votes':
                    vote = change['new_val']
                    # task.async_votes_queue(self.deal_vote,task.handle_result,vote)
                    self.deal_queue.add_vote(vote)
                    # self.deal_queue.get_votes_queue()
                    # self.deal_vote(vote)
            elif is_delete and (self.operation & LocalChangeFeed.DELETE):
                pass
                # self.outqueue.put(change['old_val'])
            elif is_update and (self.operation & LocalChangeFeed.UPDATE):
                pass
                # self.outqueue.put(change['new_val'])

    # def deal_block(self, block):
    #     logger.info('deal block task...')
    #     block_id = block['id']
    #     leveldb.insert(self.conn_bigchain, block_id, block)
    #     block_num = leveldb.get(self.conn_header, 'block_num')
    #     block_num = int(block_num)
    #     block_num = block_num + 1
    #     leveldb.update(self.conn_header, 'block_num', block_num)
    #     leveldb.update(self.conn_header, 'current_block_id', block_id)
    #     self.get_base_info(self.conn_header,self.conn_bigchain)
    #
    #
    # def deal_vote(self, vote):
    #     logger.info('deal vote task...')
    #     previous_block = vote['vote']['previous_block']
    #     node_pubkey = vote['node_pubkey']
    #     vote_key = previous_block + '-' + node_pubkey
    #     leveldb.insert(self.conn_votes, vote_key, vote)
    #
    # def get_base_info(self,conn_header,conn_bigchain):
    #     current_bid = leveldb.get(conn_header,'current_block_id')
    #     logger.info('block_num: ' + str(leveldb.get(conn_header,'block_num')) + ',\ncurrent_block_id ' +
    #                 current_bid)
    #     # logger.info('current_block: ' + str(leveldb.get(conn_bigchain,current_bid)))
    #
    #
    # def get_votes_for_block(self,conn_votes,block_id):
    #     votess = leveldb.get_prefix(conn_votes,block_id+'-')
    #     # logger.iinfo(str(block_id) + ' votes :\n' + str(votess))