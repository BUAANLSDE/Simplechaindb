

import pika
import logging

logger = logging.getLogger(__name__)

class RamqUtils(object):

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost'))
    channel = dict()
    blocks_channel = connection.channel()
    blocks_channel.queue_declare(queue='blocks')

    votes_channel = connection.channel()
    votes_channel.queue_declare(queue='votes')

    channel['blocks'] = blocks_channel
    channel['votes'] = votes_channel

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RamqUtils, cls).__new__(cls)
            logger.info('init RamqUtils ...')
        return cls.instance


def get_channel(queue_name):
    if queue_name in ['blocks','votes']:
        return RamqUtils.channel[queue_name]


def publish(queue_name,body='Hello World!',exchange=''):
    channel = get_channel(queue_name)
    if channel:
        channel.basic_publish(exchange=exchange,
                                     routing_key=queue_name,
                                     body=body,properties=pika.BasicProperties(delivery_mode=2))
    # logger.info('ramq publish queue_name: ' + str(queue_name) + ' ,body: \n' + str(body) + '\n')
    # print(" [x] Sent " + body)


# def callback(ch, method, properties, body):
#     print(" [x] Received %r" % body)
#     # print(str(body))


def consume(callback,queue_name,no_ack=True):
    channel = get_channel(queue_name)
    if channel:
        channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=no_ack)
        # logger.info('ramq receive [init]  queue_name: ' + str(queue_name) + ' ,no_ack: \n' + str(no_ack) + '\n')
        return channel


def start_consume(channel):
    if channel:
        channel.start_consuming()

def close(reply_code=200, reply_text='Normal shutdown'):
    RamqUtils.connection.close(reply_code=reply_code, reply_text=reply_text)






