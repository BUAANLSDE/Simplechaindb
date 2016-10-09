
from localdb.ramq import utils as ramq
from localdb.pipelines.methods import Methods

import time
import logging

logger = logging.getLogger(__name__)

# ramp deal

def callback_blocks(ch, method, properties, body):
    # print('info: ch' + str(ch) + ' , method ' + str(method) + ' \nproperties ' + str(properties)
    #       + ' ,body: ' + str(body))
    # time.sleep(2)
    Methods.deal_block(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def callback_votes(ch, method, properties, body):
    # print('info: ch' + str(ch) + ' , method ' + str(method) + ' \nproperties ' + str(properties)
    #       + ' ,body: ' + str(body))
    # time.sleep(2)
    Methods.deal_vote(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start():
    logger.info('localdb RabbitMQ receive work...')
    channel_blocks = ramq.consume(callback_blocks, 'blocks', False)
    channel_votes = ramq.consume(callback_votes, 'votes', False)
    ramq.start_consume(channel_blocks)
    ramq.start_consume(channel_votes)