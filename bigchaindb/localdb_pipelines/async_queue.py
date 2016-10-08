

# from asyncio import Queue
from queue import Queue
import time
import logging

from bigchaindb.localdb import utils as leveldb

logger = logging.getLogger(__name__)

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


@singleton
class DealQueue(object):

    def __init__(self,blocks_queue=None,votes_queue=None):
        leveldb.init()
        self.blocks_queue = Queue()
        self.votes_queue = Queue()

    @staticmethod
    def add_block(block):
        # logger.warn('block info add_block :\n' + str(block) + '\n')
        logger.info('add_blocks_queue....class address ' + str(DealQueue()))
        logger.info('add_blocks_queue....address ' + str(DealQueue().blocks_queue))
        if block:
            DealQueue().blocks_queue.put(block)
        logger.info('add_blocks_queue....size ' + str(DealQueue().blocks_queue.qsize()))

        blocks_queue = DealQueue().blocks_queue
        logger.info('add_blocks_queue blocks_queue....size ' + str(blocks_queue.qsize()))
        # show(DealQueue().blocks_queue)

    @staticmethod
    def get_blocks_queue():
        time.sleep(2)
        logger.info('get_blocks_queue....class address ' + str(DealQueue()))
        logger.info('get_blocks_queue....address ' + str(DealQueue().blocks_queue))
        blocks_queue = DealQueue().blocks_queue
        logger.info('get_blocks_queue blocks_queue....size ' + str(blocks_queue.qsize()))
        logger.info('get_blocks_queue....size ' + str(DealQueue().blocks_queue.qsize()))
        return blocks_queue


    def get_block(self, block=False, timeout=None):
        if self.blocks_queue.qsize() > 0:
            out_block = self.blocks_queue.get(block, timeout)
            return out_block

    def add_vote(self,vote):
        if vote:
            self.votes_queue.put(vote)
        logger.info('add_votes_queue....size ' + str(self.votes_queue.qsize()))


    def get_votes_queue(self):
        return DealQueue.votes_queue


    def get_vote(self, block=False, timeout=None):
        if self.votes_queue.qsize() > 0:
            out_vote = self.votes_queue.get(block, timeout)
            return out_vote
    # def get_block(self,block=False,timeout=None):
    #     logger.info('get_blocks_queue....size ooo ' + str(self.blocks_queue.qsize()))
    #     time.sleep(2)
    #     if DealQueue.blocks_queue.qsize() > 0:
    #         logger.info('get_blocks_queue....size before' + str(self.blocks_queue.qsize()))
    #         out_block = self.blocks_queue.get(block,timeout)
    #     logger.info('get_blocks_queue....size after' + str(self.blocks_queue.qsize()))


def show(queues):
    tempqueues = queues
    for i in range(tempqueues.qsize()):
        logger.info('.........size.......' + str(tempqueues.qsize()))
        # logger.info('...queues:\n' + str(tempqueues.get()))