# import config

import secrets
from eth_account import Account
from src.database import api as database

from src.engine import token_sniper as token_sniper_engine
from src.engine import limit_order as limit_order_engine
from src.engine import dca_order as dca_order_engine

from src.engine.chain import wallet as wallet_engine
from src.engine.chain import token as token_engine
from src.engine.chain import amm as amm_engine
from src.engine.chain import hot as hot_engine

from solders.keypair import Keypair
import threading
import time
chains = ['ethereum', 'solana', 'base']


def get_supported_chains():
    return chains


def add_user_by_chat_id(chat_id):
    database.add_user_by_chat_id(chat_id)


def get_keyboards(chat_id):
    return database.get_keyboards(chat_id)


def get_user_by_chat_id(chat_id):
    return database.get_user_by_chat_id(chat_id)


def update_keyboards(chat_id, keyboards):
    database.update_keyboards(chat_id, keyboards)


def get_current_chain_index(chat_id):
    return database.get_current_chain_index(chat_id)


def update_current_chain_index(chat_id, index):
    database.update_current_chain_index(chat_id, index)


def get_wallets(chat_id):
    return database.get_wallets(chat_id)


def create_wallet(chat_id):
    chain_index = get_current_chain_index(chat_id)
    address, private_key = wallet_engine.create_wallet(chain_index)
    database.add_wallet(chat_id, chain_index, address, private_key)
    return address, private_key


def import_wallet(chat_id, private_key):
    chain_index = get_current_chain_index(chat_id)
    address, balance = wallet_engine.import_wallet(chain_index, private_key)
    # balance = wallet_engine.get_balance(chain_index, address)
    database.import_wallet(chat_id, chain_index, address, private_key, balance)
    return address, balance


def remove_wallet(chat_id, wallet_index):
    chain_index = get_current_chain_index(chat_id)
    database.remove_wallet(chat_id, chain_index, wallet_index)


def get_information(chat_id, token):
    chain_index = get_current_chain_index(chat_id)
    data = token_engine.get_information(chain_index, token)
    return data


def check_liveness(chat_id, token):
    chain_index = get_current_chain_index(chat_id)
    liveness = token_engine.check_liveness(chain_index, token)
    return liveness


def market_order(chat_id, data):
    # time.sleep(10)
    chain_index = get_current_chain_index(chat_id)
    tx_hash = amm_engine.market_order(chain_index, data['type'], data['token'],
                                      data['buy_amount'], data['gas_amount'],
                                      data['slippage'], data['wallet'])
    criterias = {'slippage': data['slippage'],
                 'gas_amount': data['gas_amount'], 'gas_price': data['gas_price']}
    database.add_pending_order(
        chat_id, data['type'], tx_hash, data['token'], data['buy_amount'], data['wallet'], criterias)

    remove_thread = threading.Thread(
        target=remove_pending_order, args=(chat_id, tx_hash))
    remove_thread.start()
    remove_thread.join()


def limit_order(chat_id, data):
    chain_index = get_current_chain_index(chat_id)
    # amm_engine.market_order(chain_index, data['type'], data['token'],
    #                       data['buy_amount'], data['gas_amount'], data['slippage'], data['wallet'])
    keypair = Keypair()
    thread_id = str(keypair)
    thread_type = 0

    criterias = {'limit_token_price': data['limit_token_price'], 'stop-loss': data['stop-loss'],
                 'market_cap': data['market_cap'], 'liquidity': data['liquidity'], 'tax': data['tax']}
    database.add_limit_order(
        chat_id, thread_id, data['type'], thread_id, data['token'], data['buy_amount'], data['wallet'], criterias)
    tx_hash = amm_engine.limit_order(chain_index, thread_id, chat_id, data['type'], data['token'],
                                     data['buy_amount'], data['limit_token_price'],
                                     data['tax'], data['market_cap'], data['liquidity'], data['wallet'])


def dca_order(chat_id, data):
    chain_index = get_current_chain_index(chat_id)
    keypair = Keypair()
    thread_id = str(keypair)
    criterias = {'interval': data['interval'],
                 'duration': data['duration'], 'max_dca_price': data['max_dca_price'],
                 'min_dca_price': data['min_dca_price']}
    database.add_dca_order(
        chat_id, thread_id, data['type'], thread_id, data['token'], data['buy_amount'], data['wallet'], criterias)
    tx_hash = amm_engine.dca_order(chain_index, thread_id, chat_id, data['type'], data['token'],
                                   data['buy_amount'], data['interval'],
                                   data['duration'], data['max_dca_price'], data['min_dca_price'], data['wallet'])


def get_pending_orders(chat_id):
    data = database.get_pending_orders(chat_id)
    return data


def get_limit_orders(chat_id):
    data = database.get_limit_orders(chat_id)
    return data


def get_dca_orders(chat_id):
    data = database.get_dca_orders(chat_id)
    return data


def remove_pending_order(chat_id, hash):
    time.sleep(5)
    database.remove_pending_order(chat_id, hash)


def remove_limit_order(chat_id, hash):
    database.remove_limit_order(chat_id, hash)


def remove_dca_order(chat_id, hash):
    database.remove_dca_order(chat_id, hash)


def update_limit_order(chat_id, data):
    chain_index = get_current_chain_index(chat_id)
    thread_type = 2
    criterias = {'limit_token_price': data['limit_token_price'], 'stop-loss': data['stop-loss'],
                 'market_cap': data['market_cap'], 'liquidity': data['liquidity'], 'tax': data['tax']}
    database.update_limit_order(
        chat_id, data['type'], data['tx_hash'], data['token'], data['buy_amount'], criterias)


def update_dca_order(chat_id, data):
    criterias = {'interval': data['interval'],
                 'duration': data['duration'], 'min_dca_price': data['min_dca_price'],
                 'max_dca_price': data['max_dca_price']}
    database.update_dca_order(
        chat_id, data['type'], data['tx_hash'], data['token'], data['buy_amount'], criterias)


def generate_hash():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    address = acct.address
    return address


def token_sniper(chat_id, data):
    chain_index = get_current_chain_index(chat_id)
    tx_hash = generate_hash()

    criterias = {'limit_token_price': data['limit_token_price'],
                 'market_cap': data['market_cap'], 'liquidity': data['liquidity'], 'tax': data['tax']}
    database.add_token_sniper(
        chat_id, tx_hash, data['token'], data['buy_amount'], data['gas_price'], data['slippage'], data['wallet'], criterias)


def get_token_snipers(chat_id):
    data = database.get_token_snipers(chat_id)
    return data


def update_token_sniper(chat_id, data):
    criterias = {'limit_token_price': data['limit_token_price'],
                 'market_cap': data['market_cap'], 'liquidity': data['liquidity'], 'tax': data['tax']}
    database.update_token_sniper(
        chat_id, data['tx_hash'], data['token'], data['buy_amount'], data['gas'], data['slippage'], criterias)


def remove_token_sniper(chat_id, tx_hash):
    database.remove_token_sniper(chat_id, tx_hash)
