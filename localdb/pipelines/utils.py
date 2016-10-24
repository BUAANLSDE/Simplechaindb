"""Utility classes and functions to work with the pipelines."""


import rethinkdb as r
from multipipes import Node
from bigchaindb import Bigchain

from localdb.ramq import utils as ramq
import rapidjson

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

    def run_forever(self):
        for element in self.prefeed:
            logger.info('prefeed' + str(self.prefeed))
            self.outqueue.put(element)

        for change in r.table(self.table).changes().run(self.bigchain.conn):

            is_insert = change['old_val'] is None
            is_delete = change['new_val'] is None
            is_update = not is_insert and not is_delete

            if is_insert and (self.operation & LocalChangeFeed.INSERT):
                if self.table == 'bigchain':
                    block = rapidjson.dumps(change['new_val'])
                    ramq.publish('blocks',block)
                elif self.table == 'votes':
                    vote = rapidjson.dumps(change['new_val'])
                    ramq.publish('votes', vote)
            elif is_delete and (self.operation & LocalChangeFeed.DELETE):
                pass
                # self.outqueue.put(change['old_val'])
            elif is_update and (self.operation & LocalChangeFeed.UPDATE):
                pass
                # self.outqueue.put(change['new_val'])