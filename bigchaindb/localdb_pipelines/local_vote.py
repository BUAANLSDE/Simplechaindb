"""
This module  takes care of all the changes for bigchain and votes.
"""

import logging
from multipipes import Pipeline, Node
from bigchaindb.localdb_pipelines.utils import ChangeFeed

logger = logging.getLogger(__name__)


class LocalVote(Node):
    """This class monitor the change for votes.

    Note:
        Methods of this class will be executed in different processes.
    """

    INSERT = 1
    DELETE = 2
    UPDATE = 4

    def __init__(self):
        pass


    def set_votes_queue(self,block):
        self.votes_queue.put(block)


    def get_votes_queue(self):
        return self.votes_queue


def create_pipeline():
    localVote = LocalVote()
    localVote__pipeline = Pipeline([])
    return localVote__pipeline


def initial():
    return None

def get_changefeed():
    """Create and return the changefeed for the votes."""
    return ChangeFeed('votes',ChangeFeed.INSERT | ChangeFeed.UPDATE,prefeed=initial())


def start():
    """Create, start, and return the localVote pipeline."""
    pipeline = create_pipeline()
    pipeline.setup(indata=get_changefeed())
    pipeline.start()
    return pipeline
