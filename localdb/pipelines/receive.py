
from localdb.ramq import utils as ramq
from localdb.pipelines.methods import Methods
# from multiprocessing import cpu_count

import logging

logger = logging.getLogger(__name__)

# ramp deal

def callback_blocks(ch, method, properties, body):
    # print('info: ch' + str(ch) + ' , method ' + str(method) + ' \nproperties ' + str(properties)
    #       + ' ,body: ' + str(body))
    # logger.warn('info: ch' + str(ch) + ' , method ' + str(method) + ' \nproperties ' + str(properties))
    # time.sleep(2)
    Methods.deal_block(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def callback_votes(ch, method, properties, body):
    # print('info: ch' + str(ch) + ' , method ' + str(method) + ' \nproperties ' + str(properties)
    # time.sleep(2)
    # logger.warn('info: ch' + str(ch) + ' , method ' + str(method) + ' \nproperties ' + str(properties))
    Methods.deal_vote(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start():
    logger.info('localdb RabbitMQ receive work...')
    # consume_count = cpu_count()
    # if consume_count and consume_count >= 1:
    #     consume_count = int(consume_count / 2) + 1
    # else:
    #     consume_count = 1
    # logger.info("consume count: " + str(consume_count))

    channel_blocks = ramq.consume(callback_blocks, 'blocks', False)
    channel_votes = ramq.consume(callback_votes, 'votes', False)
    ramq.start_consume(channel_blocks)
    ramq.start_consume(channel_votes)