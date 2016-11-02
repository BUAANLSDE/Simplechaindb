"""
电力交易Demo的API。
"""
import logging
import flask
from flask import current_app, request, Blueprint, make_response, abort
# from flask_restful import Resource, Api
import json
import rethinkdb as r

import bigchaindb
from bigchaindb import Bigchain, util
from bigchaindb.web.views.base import make_error

# add import buaa
from bigchaindb import tool
from bigchaindb import crypto

logger = logging.getLogger(__name__)

"""
class ApiForEleDemo(object):
    def __init__(self, host=None, port=None, dbname=None, pub_key=None, priv_key=None, keyring=[],
                 consensus_plugin=None):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.conn = r.connect(host=host, port=port, db=dbname)
        self.bigchain = Bigchain(host=host, port=port, dbname=dbname, public_key=pub_key, private_key=priv_key,
                                 keyring=keyring, consensus_plugin=consensus_plugin)
"""

electric_api = Blueprint('electric_api', __name__)


@electric_api.route('/electric_trans/', methods=['POST'])
def createElectricTrans():
    """API endpoint to push transactions to the Federation.

        Return:
            A JSON string containing the data about the transaction.
        """
    pool = current_app.config['bigchain_pool']
    monitor = current_app.config['monitor']

    val = {}
    payload = request.get_json(force=True)
    # 获取请求的某一个参数的方法
    # asset_hash = request.args.get('owners_before', '')

    # 获取参与者的公钥
    owners_before = payload['owners_before']
    private_key = payload['private_key']
    owners_after = payload['owners_after']
    del payload["private_key"]

    with pool() as bigchain:
        # 根据参与者及payload创建trans
        transaction = util.create_tx(bigchain.me, owners_after, None, 'CREATE', payload=payload)
        # 对trans进行签名
        transaction = bigchain.consensus.sign_transaction(transaction, private_key=bigchain.me_private)
        if not bigchain.consensus.validate_fulfillments(transaction):
            val['error'] = 'Invalid transaction fulfillments'
        with monitor.timer('write_transaction', rate=bigchaindb.config['statsd']['rate']):
            val = bigchain.write_transaction(transaction)

    return flask.jsonify(**transaction)


def get_error_message(err, type, extra):
    """Useful Function getting the error message to return"""
    error_msg = flask.jsonify({
        'error': err,
        'type': type,
        'extra': extra
    })
    return error_msg
