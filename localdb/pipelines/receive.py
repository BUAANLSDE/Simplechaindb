
from localdb.ramq import utils as ramq
from localdb.pipelines.methods import Methods

import logging

logger = logging.getLogger(__name__)

# RabbitMQ deal for bigchaindb ChangeFeedback

def callback_blocks(ch, method, properties, body):
    """Consume methods for blocks

    Args:
        ch:
        method:
        properties:
        body(str) —— json string of bigchain block obj

    Returns:

   """

    # print('info: ch' + str(ch) + ' , method ' + str(method) + ' \nproperties ' + str(properties)
    #       + ' ,body: ' + str(body))
    # logger.warn('info: ch' + str(ch) + ' , method ' + str(method) + ' \nproperties ' + str(properties))
    # time.sleep(2)
    Methods.deal_block(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def callback_votes(ch, method, properties, body):
    """Consume methods for votes

     Args:
         ch:
         method:
         properties:
         body(str) —— json string of bigchain vote obj

     Returns:

    """

    # print('info: ch' + str(ch) + ' , method ' + str(method) + ' \nproperties ' + str(properties)
    # time.sleep(2)
    # logger.warn('info: ch' + str(ch) + ' , method ' + str(method) + ' \nproperties ' + str(properties))
    Methods.deal_vote(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start():
    """RabbitMQ consume start"""

    logger.info('localdb RabbitMQ receive work...')
    channel_blocks = ramq.consume(callback_blocks, 'blocks', False)
    channel_votes = ramq.consume(callback_votes, 'votes', False)
    ramq.start_consume(channel_blocks)
    ramq.start_consume(channel_votes)