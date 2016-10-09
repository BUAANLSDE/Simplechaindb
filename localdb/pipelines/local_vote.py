"""
This module  takes care of all the changes for bigchain and votes.
"""

from multipipes import Pipeline, Node
from localdb.pipelines.utils import LocalChangeFeed

import logging

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


def create_pipeline():
    localVote = LocalVote()
    localVote_pipeline = Pipeline([])
    return localVote_pipeline


def initial():
    return None

def get_changefeed():
    """Create and return the changefeed for the votes."""
    return LocalChangeFeed('votes',LocalChangeFeed.INSERT | LocalChangeFeed.UPDATE,prefeed=initial())


def start():
    """Create, start, and return the localVote pipeline."""
    pipeline = create_pipeline()
    pipeline.setup(indata=get_changefeed())
    pipeline.start()
    return pipeline