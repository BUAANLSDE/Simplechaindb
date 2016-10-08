"""
This module  takes care of all the changes for bigchain and votes.
"""

import time
import logging
from multipipes import Pipeline, Node

from bigchaindb.localdb_pipelines.async_queue import DealQueue
import bigchaindb.localdb.utils as leveldb
from multiprocessing import Process

logger = logging.getLogger(__name__)

class LocalDeal(Node):
    """This class monitor the change for votes.

    Note:
        Methods of this class will be executed in different processes.
    """

    INSERT = 1
    DELETE = 2
    UPDATE = 4

    def __init__(self):
        self.deal_queue = DealQueue()
        self.conn_header = leveldb.get_conn('header')
        self.conn_bigchain = leveldb.get_conn('bigchain')
        self.conn_votes = leveldb.get_conn('votes')

    def get_block(self):
        # blocks_queue = DealQueue().get_blocks_queue()
        blocks_queue = self.deal_queue.get_blocks_queue()
        if blocks_queue.qsize() > 0:
            return self.deal_queue.get_block()
        else:
            time.sleep(3)
        # logger.info('get_block '+ str(self.deal_queue.get_blocks_queue().qsize()))
        return self.deal_queue.get_block()


    def deal_block(self, block):
        block_id = block['id']
        leveldb.insert(self.conn_bigchain, block_id, block)
        block_num = leveldb.get(self.conn_header, 'block_num')
        block_num = int(block_num)
        block_num = block_num + 1
        leveldb.update(self.conn_header, 'block_num', block_num)
        leveldb.update(self.conn_header, 'current_block_id', block_id)
        logger.info('deal_block...' + str(block))
        time.sleep(5)

    def get_vote(self):
        votes_queue = self.deal_queue.get_votes_queue()
        if votes_queue.qsize() > 0:
            return DealQueue.get_vote()
        # logger.info('get_vote ' + str(self.deal_queue.get_votes_queue().qsize()))
        return self.deal_queue.get_vote()

    def deal_vote(self, vote):
        previous_block = vote['vote']['previous_block']
        node_pubkey = vote['node_pubkey']
        vote_key = previous_block + '-' + node_pubkey
        leveldb.insert(self.conn_votes, vote_key, vote)
        logger.info('deal_vote...' + str(vote))


def create_pipeline():
    localDeal = LocalDeal()
    logger.error('create_pipeline...deal')
    localDeal_pipeline = Pipeline([
        Node(localDeal.get_block),
        Node(localDeal.deal_block)
    ])
    return localDeal_pipeline


def start():
    """Create, start, and return the localVote pipeline."""
    pipeline = create_pipeline()
    pipeline.setup()
    pipeline.start()
    return pipeline