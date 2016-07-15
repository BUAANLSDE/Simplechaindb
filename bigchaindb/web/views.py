"""This module provides the blueprint for some basic API endpoints.

For more information please refer to the documentation in Apiary:
 - http://docs.bigchaindb.apiary.io/
"""

import flask
from flask import abort, current_app, request, Blueprint

import bigchaindb
from bigchaindb import util, version
from bigchaindb import crypto

info_views = Blueprint('info_views', __name__)
basic_views = Blueprint('basic_views', __name__)


# Unfortunately I cannot find a reference to this decorator.
# This answer on SO is quite useful tho:
# - http://stackoverflow.com/a/13432373/597097
@basic_views.record
def record(state):
    """This function checks if the blueprint can be initialized
    with the provided state."""

    bigchain_pool = state.app.config.get('bigchain_pool')
    monitor = state.app.config.get('monitor')

    if bigchain_pool is None:
        raise Exception('This blueprint expects you to provide '
                        'a pool of Bigchain instances called `bigchain_pool`')

    if monitor is None:
        raise ValueError('This blueprint expects you to provide '
                         'a monitor instance to record system '
                         'performance.')

@info_views.route('/')
def home():
    return flask.jsonify({
        'software': 'BigchainDB',
        'version': version.__version__,
        'public_key': bigchaindb.config['keypair']['public'],
        'keyring': bigchaindb.config['keyring'],
        'api_endpoint': bigchaindb.config['api_endpoint']
    })


@basic_views.route('/transactions/tx_id=<tx_id>')
def get_transaction(tx_id):
    """API endpoint to get details about a transaction.

    Args:
        tx_id (str): the id of the transaction.

    Return:
        A JSON string containing the data about the transaction.
    """

    pool = current_app.config['bigchain_pool']

    with pool() as bigchain:
        tx = bigchain.get_transaction(tx_id)

    if not tx:
        abort(404)

    return flask.jsonify(**tx)


@basic_views.route('/transactions/', methods=['POST'])
def create_transaction():
    """API endpoint to push transactions to the Federation.

    Return:
        A JSON string containing the data about the transaction.
    """
    pool = current_app.config['bigchain_pool']
    monitor = current_app.config['monitor']

    val = {}

    # `force` will try to format the body of the POST request even if the `content-type` header is not
    # set to `application/json`
    tx = request.get_json(force=True)

    with pool() as bigchain:
        if tx['transaction']['operation'] == 'CREATE':
            tx = util.transform_create(tx)
            tx = bigchain.consensus.sign_transaction(tx, private_key=bigchain.me_private)

        if not bigchain.consensus.validate_fulfillments(tx):
            val['error'] = 'Invalid transaction fulfillments'

        with monitor.timer('write_transaction', rate=bigchaindb.config['statsd']['rate']):
            val = bigchain.write_transaction(tx)

    return flask.jsonify(**tx)


@basic_views.route('/transactions/uuid=<uuid>')
def get_transaction_by_uuid(uuid):
    """API endpoint to get details about a transaction.

        Args:
            uuid (str): the uuid of the transaction's data part.

        Return:
            A JSON string containing the data about the transaction.
        """

    pool = current_app.config['bigchain_pool']

    with pool() as bigchain:
        tx = bigchain.get_tx_by_payload_hash(uuid)

    if not tx:
        abort(404)

    return flask.jsonify(**tx)


@basic_views.route('/transactions/public_key=<public_key>')
def get_transaction_by_public_key(public_key):
    """API endpoint to get details about transactions.

            Args:
                public_key (str): the public_key of the transaction's new owners.

            Return:
                A JSON string containing the data about the transaction.
            """

    pool = current_app.config['bigchain_pool']

    with pool() as bigchain:
        tx_ids = bigchain.get_owned_ids(public_key)

    if not tx_ids:
        abort(404)

    return flask.jsonify(**tx_ids)


# assets api

@basic_views.route('/assets/<public_key>')
def get_assets_by_public_key(public_key):
    """API endpoint to get all assets of someone.

            Args:
                public_key (str): the public_key of the user.

            Return:
                A JSON string containing the data of all assets owned by the user.

            json format:
            {
                "owner":public_key,
                "assets":[
                    "asset1_hash",
                    "asset2_hash",
                    ...
                ]
            }
            """
    pool = current_app.config['bigchain_pool']

    with pool() as bigchain:
        assets = {"owner":public_key, "assets":bigchain.get_owned_asset(public_key)}

    return flask.jsonify(**assets)


@basic_views.route('/assets/owner/<asset_hash>')
def get_owner_of_asset(asset_hash):
    """API endpoint to get the owner of asset.

            Args:
                asset_hash (str): the hash of the asset.

            Return:
                the public key of the user.
            json format:
            {
                "owner":public_key
                "asset":asset_hash
            }
            """
    pool = current_app.config['bigchain_pool']

    with pool() as bigchain:
        owner = bigchain.get_owner(asset_hash);

    if not owner:
        abort(404)

    return flask.jsonify(**owner)


@basic_views.route('/assets/<public_key>/<asset_hash>', methods=['POST','GET'])
def create_asset(public_key,asset_hash):
    """API endpoint to push asset to the Federation.

    Return:
        the create transaction.
    """
    pool = current_app.config['bigchain_pool']
    monitor = current_app.config['monitor']

    val = {}

    # `force` will try to format the body of the POST request even if the `content-type` header is not
    # set to `application/json`
    tx = request.get_json(force=True)

    with pool() as bigchain:
        payload = {"msg" : "create_asset","issue" : "create",
         "category" : "asset", "amount" : 0, "asset":asset_hash, "account":0}
        tx = bigchain.create_asset(public_key,payload)

    return flask.jsonify(**tx)


@basic_views.route('/assets/destroy/<public_key>/<asset_hash>', methods=['POST','GET'])
def destroy_asset(public_key,private_key,asset_hash):
    """API endpoint to destroy asset.
    Args:
                public_key (str): the public_key of the user.
                asset_hash (str): the hash of the asset.
    Return:
        transaction.
    """
    pool = current_app.config['bigchain_pool']
    monitor = current_app.config['monitor']
    val = {}
    with pool() as bigchain:
        response = bigchain.destory_asset(public_key,private_key,asset_hash)
    return flask.jsonify(**response)
# accounts api


@basic_views.route('/accounts/<public_key>')
def get_balance(public_key):
    """API endpoint to get the balance of user.

            Args:
                public_key (str): the public_key of the user.

            Return:
                int>=0,balance of the user.
            json format:
            {
                "public_key":public_key,if user Non-existent,the value is None.
                "balance":remain_sum,if user Non-existent,the value is 0 .
            }
            """
    pool = current_app.config['bigchain_pool']

    with pool() as bigchain:
        balance = bigchain.get_current_balance(public_key)

    if not balance:
        abort(404)

    return balance


@basic_views.route('/accounts/<public_key>/<amount>',methods=['POST','GET'])
def recharge(public_key,amount):
    """API endpoint to recharge.

            Args:
                public_key (str): the public_key of the user.
                amount (int): amount of charge

            Returns:
                the charge transaction.
            """
    pool = current_app.config['bigchain_pool']
    monitor = current_app.config['monitor']

    val = {}
    with pool() as bigchain:
        payload = {"msg": "charge", "issue": "charge",
                   "category": "currency", "amount": amount, "asset": "currency", "account": get_balance(public_key)}
        tx = bigchain.charge_currency(public_key, payload)

    return flask.jsonify(**tx)


@basic_views.route('/accounts/history/<public_key>')
def get_account_record(public_key):
    """API endpoint to get account records of the user.

            Args:
                public_key (str): the public_key of the user.

            Returns:
                a json data of account records.
            json format:
            {
                "public_key":public_key,
                "time_start":time_start,
                "time_end":time_end,
                "currency_record":[
                    {
                        "issue":issue,
                        "amount":amount
                    },
                    ...
                ]
            }
            """
    pass


# other api


@basic_views.route('/system/key/')
def generate_key_pair():
    """API endpoint to generate key pair.
            Returns:
                a json data of key pair.
                json format:
                {
                    "public_key":public_key,
                    "private_key":private_key
                }
            """
    return crypto.generate_key_pair()


@basic_views.route('/system/key/<private_key>')
def get_public_key(private_key):
    """API endpoint to get corresponding public key of the private key.
            Returns:
                str,public key.
            json format:
            {
                "public_key":public_key,
                "private_key":private_key
            }
            """
    pass


@basic_views.route('/statistics/transaction')
def stats_transactions():
    """API endpoint to get the number of all transaction.
            Returns:
                a json data of various types transaction numbers .
                json format:
                {
                    "total": total number,
                    "currency_transaction": {
                        "currency_number":currency_number,
                        "charge_transaction":charge_number,
                        "cost_transaction":cost_number,
                        "earn_transaction":earn_number
                    }
                    "asset_transaction": {
                        "asset_number":asset_number,
                        "create_transaction":create_number,
                        "transfer_transaction":transfer_number,
                        "destroy_transaction":destroy_number
                    }
                }
            """
    pass


@basic_views.route('/statistics/transaction/<public_key>')
def stats_transaction_of_owner(public_key):
    """API endpoint to get the number of all transactions for the user .
            Returns:
                a json data of various types transaction numbers .
                json format:
                {
                    "total": total number,
                    "currency_transaction": {
                        "currency_number":currency_number,
                        "charge_transaction":charge_number,
                        "cost_transaction":cost_number,
                        "earn_transaction":earn_number
                    }
                    "asset_transaction": {
                        "asset_number":asset_number,
                        "create_transaction":create_number,
                        "transfer_transaction":transfer_number,
                        "destroy_transaction":destroy_number
                    }
                }
            """
    pass