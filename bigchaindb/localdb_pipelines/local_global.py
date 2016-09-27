
import queue
import logging
import threading

g_blocks_queue = queue.Queue()

g_votes_queue = queue.Queue()

def async_blocks_queue(function, callback, *args, **kwargs):
    g_blocks_queue.put({
        'function': function,
        'callback': callback,
        'args': args,
        'kwargs':   kwargs
    })


def async_votes_queue(function, callback, *args, **kwargs):
    g_votes_queue.put({
        'function': function,
        'callback': callback,
        'args': args,
        'kwargs':   kwargs
    })


def _g_blocks_queue_consumer():
    while True:
        try:
            task = g_blocks_queue.get(False,timeout=6)
            function = task.get('function')
            callback = task.get('callback')
            args = task.get('args')
            kwargs = task.get('kwargs')
            try:
                if callback:
                    callback(function(*args, **kwargs))
            except Exception as ex:
                if callback:
                    callback(ex)
            finally:
                g_blocks_queue.task_done()
        except Exception as ex:
            logging.warning('asyn blocks queue ... ' + ex)


def _g_votes_queue_consumer():
    while True:
        try:
            task = g_votes_queue.get(False,timeout=6)
            function = task.get('function')
            callback = task.get('callback')
            args = task.get('args')
            kwargs = task.get('kwargs')
            try:
                if callback:
                    callback(function(*args, **kwargs))
            except Exception as ex:
                if callback:
                    callback(ex)
            finally:
                g_votes_queue.task_done()
        except Exception as ex:
            logging.warning('asyn votes queue ... ' + ex)


if __name__ == '__main__':
    t_block = threading.Thread(target=_g_blocks_queue_consumer)
    t_votes = threading.Thread(target=_g_votes_queue_consumer)
    # t.daemon = True
    t_block.start()
    t_votes.start()
    g_blocks_queue.join()
    g_votes_queue.join()