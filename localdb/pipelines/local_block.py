"""
This module  takes care of all the changes for bigchain and votes.
"""

from multipipes import Pipeline, Node
from localdb.pipelines.utils import LocalChangeFeed

import logging

logger = logging.getLogger(__name__)

class LocalBlock(Node):
    """This class monitor the change for block.

    Note:
        Methods of this class will be executed in different processes.
    """

    INSERT = 1
    DELETE = 2
    UPDATE = 4

    def __init__(self):
        pass

def create_pipeline():
    localBlock = LocalBlock()
    localBlock_pipeline = Pipeline([])
    return localBlock_pipeline


def initial():
    return None


def get_changefeed():
    """Create and return the changefeed for the bigchain."""
    return LocalChangeFeed('bigchain',LocalChangeFeed.INSERT | LocalChangeFeed.UPDATE,prefeed=initial())


def start():
    """Create, start, and return the localBlock pipeline."""
    pipeline = create_pipeline()
    pipeline.setup(indata=get_changefeed())
    pipeline.start()
    return pipeline