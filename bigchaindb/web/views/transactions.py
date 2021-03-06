"""This module provides the blueprint for some basic API endpoints.

For more information please refer to the documentation on ReadTheDocs:
 - https://bigchaindb.readthedocs.io/en/latest/drivers-clients/http-client-server-api.html
"""

import flask
from flask import current_app, request, Blueprint, make_response, abort
#from flask_restful import Resource, Api

import bigchaindb
from bigchaindb import util
from bigchaindb.web.views.base import make_error

#add import buaa
from bigchaindb import tool
from bigchaindb import crypto

transaction_views = Blueprint('transaction_views', __name__)
#transaction_api = Api(transaction_views)


# Unfortunately I cannot find a reference to this decorator.
# This answer on SO is quite useful tho:
# - http://stackoverflow.com/a/13432373/597097
@transaction_views.record
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


@transaction_views.route('/transactions/tx_id=<tx_id>')
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
        #abort(404)
        return make_response(get_error_message(
            'Not Found', 'transaction', 'tx_id=' + tx_id), 404)

    return flask.jsonify(**tx)

@transaction_views.route('/transactions/status/tx_id=<tx_id>')
def get_transaction_status(tx_id):
    """API endpoint to get details about the status of a transaction.

    Args:
        tx_id (str): the id of the transaction.

    Return:
        A ``dict`` in the format ``{'status': <status>}``, where ``<status>``
        is one of "valid", "invalid", "undecided", "backlog".
    """

    pool = current_app.config['bigchain_pool']

    with pool() as bigchain:
        status = bigchain.get_status(tx_id)
        statusjson = {'status': status}

    if not status:
        return make_error(404)

    return flask.jsonify(**statusjson)

@transaction_views.route('/transactions/', methods=['POST'])
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


@transaction_views.route('/transactions/uuid=<uuid>')
def get_transaction_by_uuid(uuid):
    """API endpoint to get details about a transaction.

        Args:
            uuid (str): the uuid of the transaction's data part.

        Return:
            A JSON string containing the data about the transaction.
        """

    pool = current_app.config['bigchain_pool']

    with pool() as bigchain:
        tx = bigchain.get_tx_by_payload_uuid(uuid)
        txs = {'tx_list': tx}
    if not tx:
        #abort(404)
        return make_response(get_error_message(
            'Not Found', 'transaction', 'uuid=' + uuid))

    return flask.jsonify(**txs)


@transaction_views.route('/transactions/public_key=<public_key>')
def get_transaction_by_public_key(public_key):
    """API endpoint to get details about transactions.

            Args:
                public_key (str): the public_key of the transaction's new owners.

            Return:
                A JSON string containing the data about the transaction.
            """

    pool = current_app.config['bigchain_pool']

    with pool() as bigchain:
        tx_ids = {"owner": public_key,
                  "tx_list": bigchain.get_owned_ids(public_key)
                  }

    if not tx_ids:
        #abort(404)
        return make_response(get_error_message(
            'Not Found', 'transaction', 'public key: ' + public_key
        ))

    return flask.jsonify(**tx_ids)


# assets api

@transaction_views.route('/assets/<public_key>')
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


@transaction_views.route('/assets/owner/<asset_hash>')
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
        owner={"owner":bigchain.get_owner(asset_hash),"asset":asset_hash}

    return flask.jsonify(**owner)


@transaction_views.route('/assets/create/<public_key>/<asset_hash>', methods=['POST','GET'])
def create_asset(public_key,asset_hash):
    """API endpoint to push asset to the Federation.
    Return:
        the create transaction.
    """
    pool = current_app.config['bigchain_pool']
    monitor = current_app.config['monitor']

    with pool() as bigchain:
        payload = {
            "msg" : "create_asset",
            "issue" : "create",
            "category" : "asset",
            "amount" : 0,
            "asset":asset_hash,
            "account":0,
            "previous":'',
            "trader":''
        }
        tx = bigchain.create_asset(public_key,payload)

    return flask.jsonify(**tx)


@transaction_views.route('/assets/destroy/<public_key>', methods=['POST','GET'])
def destroy_asset(public_key):
    """API endpoint to destroy asset.
    Args:
                public_key (str): the public_key of the user.
                asset_hash (str): the hash of the asset.
        /assets/destroy/<public_key>?private_key=pri_key&asset_hash=hash
    Return:
        transaction.
    """
    asset_hash=request.args.get('asset_hash','')
    private_key=request.args.get('private_key','')

    print('asset_hash is : '+asset_hash)
    print('private_key is : '+private_key)

    pool = current_app.config['bigchain_pool']
    monitor = current_app.config['monitor']
    val = {}
    with pool() as bigchain:
        response = bigchain.destroy_asset(public_key,private_key,asset_hash)
    return flask.jsonify(**response)


@transaction_views.route('/assets/circulation/<asset_hash>')
def get_circulation_of_asset(asset_hash):
    """API endpoint to get circulation of asset.

            Args:
                asset_hash (str): the hash of the asset.

            Return:
                the circulation record of asset.
            json format:
            {
                "asset":asset_hash,
                "circulation_record":[
                    {
                        "owners_before":owners_before,
                        "owners_after":owners_after,
                        "time":time
                    },
                    ...
                ]
            }
            """
    pool = current_app.config['bigchain_pool']

    with pool() as bigchain:
        tx_list=bigchain.get_tx_list_by_asset(asset_hash)
        records=tool.get_asset_records(tool.sort_asset_tx_by_timestamp(tx_list))
        asset_records={
            "asset":asset_hash,
            "circulation_record":records
        }
    return flask.jsonify(**asset_records)


@transaction_views.route('/assets/transfer/',methods=['POST'])
def asset_transfer():
    """API endpoint to asset transfer.

            post data json format:
            {
                "sender_public_key":sender public key,
                "sender_private_key":sender private key,
                "receiver_public_key":receiver public key,
                "asset":asset hash
            }
    """

    data=request.get_json(force=True)
    sender=data['sender_public_key']
    sender_priv=data['sender_private_key']
    receiver_pub=data['receiver_public_key']
    # check asset_hash is None
    asset_hash=data['asset']

    pool = current_app.config['bigchain_pool']
    monitor = current_app.config['monitor']

    with pool() as bigchain:
        last_tx=bigchain.get_last_tx_by_asset(asset_hash)
        # check the sender is the asset owner
        tx_input=bigchain.get_tx_input(last_tx,sender)
        tx = bigchain.transfer_asset(sender,sender_priv,receiver_pub,tx_input)

    return flask.jsonify(**tx)

# accounts api


@transaction_views.route('/accounts/<public_key>')
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
        balance={"public_key":public_key,"balance":bigchain.get_current_balance(public_key)}
    if not balance:
        #abort(404)
        return make_response(get_error_message(
            'Not Found', 'user balance', 'public key: ' + public_key
        ))

    return flask.jsonify(**balance)


@transaction_views.route('/accounts/charge/<public_key>/<int:amount>',methods=['POST','GET'])
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

    with pool() as bigchain:
        payload = {
                    "msg": "charge",
                    "issue": "charge",
                    "category": "currency",
                    "amount": amount,
                    "asset": '',
                    "account":0,
                    "previous":'',
                    "trader":''
                  }
        tx = bigchain.charge_currency(public_key, payload)

    return flask.jsonify(**tx)


@transaction_views.route('/accounts/history/<public_key>')
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
                        "msg":additional message,
                        "issue":issue,
                        "trader":trader,
                        "asset":asset,
                        "amount":amount,
                        "time":time
                    },
                    ...
                ]
            }
            """
    pool = current_app.config['bigchain_pool']
    monitor = current_app.config['monitor']
    with pool() as bigchain:
        currency_list=bigchain.get_bigchain_currency_list(public_key)
        records=tool.get_currency_records(tool.sort_currency_list(currency_list))
        account_records={
            "public_key":public_key,
            "currency_record":records
        }

    return flask.jsonify(**account_records)


@transaction_views.route('/accounts/transfer/',methods=['POST'])
def currency_transfer():
    """API endpoint to currency transfer.

            post data json format:
            {
                "sender_public_key":sender public key,
                "sender_private_key":sender private key,
                "receiver_public_key":receiver public key,
                "data":{
                    "msg": "additional message",
                    "issue": "transfer",
                    "category": "currency",
                    "amount": amount,
                    "asset": 'asset_hash',
                    "account":0,
                    "previous":'',
                    "trader":''
                }
            }
    """

    data=request.get_json(force=True)
    sender=data['sender_public_key']
    sender_priv=data['sender_private_key']
    receiver_pub=data['receiver_public_key']
    # check payload format and values
    payload=data['data']

    pool = current_app.config['bigchain_pool']
    monitor = current_app.config['monitor']

    with pool() as bigchain:
        tx = bigchain.transfer_currency(sender,sender_priv,receiver_pub,payload)

    return flask.jsonify(**tx)

# other api


@transaction_views.route('/system/key/')
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
    private_key,public_key=crypto.generate_key_pair()
    dict={
        "public_key":public_key,
        "private_key":private_key
    }
    return flask.jsonify(**dict)


@transaction_views.route('/system/key/<private_key>')
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
    key_pair={
        "public_key":tool.get_public_key(private_key),
        "private_key":private_key
    }
    return flask.jsonify(**key_pair)


@transaction_views.route('/statistics/transaction')
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
    pool = current_app.config['bigchain_pool']

    with pool() as bigchain:
        stats = {
            "total": bigchain.get_total_tx_number(),
            "currency_transaction": {
                "currency_number": bigchain.get_currency_tx_number(),
                "charge_transaction": bigchain.get_currency_tx_number_by_type("charge"),
                "cost_transaction": bigchain.get_currency_tx_number_by_type("cost"),
                "earn_transaction": bigchain.get_currency_tx_number_by_type("earn")
            },
            "asset_transaction": {
                "asset_number": bigchain.get_asset_tx_number(),
                "create_transaction": bigchain.get_asset_tx_number_by_type("create"),
                "transfer_transaction": bigchain.get_asset_tx_number_by_type("transfer"),
                "destroy_transaction": bigchain.get_asset_tx_number_by_type("destroy")
            }
        }

    return flask.jsonify(**stats)


@transaction_views.route('/statistics/transaction/<public_key>')
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
    pool = current_app.config['bigchain_pool']

    with pool() as bigchain:
        stats = {
            "total": bigchain.get_total_tx_number(public_key),
            "currency_transaction": {
                "currency_number": bigchain.get_currency_tx_number(public_key),
                "charge_transaction": bigchain.get_currency_tx_number_by_type("charge",public_key),
                "cost_transaction": bigchain.get_currency_tx_number_by_type("cost",public_key),
                "earn_transaction": bigchain.get_currency_tx_number_by_type("earn",public_key)
            },
            "asset_transaction": {
                "asset_number": bigchain.get_asset_tx_number(public_key),
                "create_transaction": bigchain.get_asset_tx_number_by_type("create",public_key),
                "transfer_transaction": bigchain.get_asset_tx_number_by_type("transfer",public_key),
                "destroy_transaction": bigchain.get_asset_tx_number_by_type("destroy",public_key)
            }
        }

    return flask.jsonify(**stats)


def get_error_message(err, type, extra):
    """Useful Function getting the error message to return"""
    error_msg = flask.jsonify({
        'error': err,
        'type' : type,
        'extra': extra
    })
    return error_msg


'''
class TransactionApi(Resource):
    def get(self, tx_id):
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
            return make_error(404)

        return tx


class TransactionStatusApi(Resource):
    def get(self, tx_id):
        """API endpoint to get details about the status of a transaction.

        Args:
            tx_id (str): the id of the transaction.

        Return:
            A ``dict`` in the format ``{'status': <status>}``, where ``<status>``
            is one of "valid", "invalid", "undecided", "backlog".
        """

        pool = current_app.config['bigchain_pool']

        with pool() as bigchain:
            status = bigchain.get_status(tx_id)

        if not status:
            return make_error(404)

        return {'status': status}


class TransactionListApi(Resource):
    def post(self):
        """API endpoint to push transactions to the Federation.

        Return:
            A ``dict`` containing the data about the transaction.
        """
        pool = current_app.config['bigchain_pool']
        monitor = current_app.config['monitor']

        # `force` will try to format the body of the POST request even if the `content-type` header is not
        # set to `application/json`
        tx = request.get_json(force=True)

        with pool() as bigchain:
            if tx['transaction']['operation'] == 'CREATE':
                tx = util.transform_create(tx)
                tx = bigchain.consensus.sign_transaction(tx, private_key=bigchain.me_private)

            if not bigchain.is_valid_transaction(tx):
                return make_error(400, 'Invalid transaction')

            with monitor.timer('write_transaction', rate=bigchaindb.config['statsd']['rate']):
                bigchain.write_transaction(tx)

        return tx

transaction_api.add_resource(TransactionApi,
                             '/transactions/<string:tx_id>',
                             strict_slashes=False)
transaction_api.add_resource(TransactionStatusApi,
                             '/transactions/<string:tx_id>/status',
                             strict_slashes=False)
transaction_api.add_resource(TransactionListApi,
                             '/transactions',
                             strict_slashes=False)
'''
