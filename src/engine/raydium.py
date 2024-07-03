"Detect  New Pools Created on Solana Raydium DEX"

#MAnually see transactions of new pairs GThUX1Atko4tqhN2NaiTazWSeFWMuiUvfFnyJyUghFMJ under spl transfer section

from time import sleep
import logging

import asyncio
from asyncstdlib import enumerate

from solders.pubkey import Pubkey # type: ignore
from solana.rpc.api import Client

from src.engine.chain.solana.token import is_valid, check_liveness, get_market_data, get_metadata
from telethon import TelegramClient, events
import time
from threading import Thread
from src.database import api as database
from src.engine.chain import token as token_engine
from src.engine import token_sniper as token_sniper_engine
from src.engine import lp_sniper as lp_sniper_engine
# Replace these with your own values
api_id = '29719975'
api_hash = '765d9b181ae6998415f8be36b3c4c793'
phone_number = '14846034605'

# Create the client and connect
client = TelegramClient('session', api_id, api_hash)

async def auto_token_sniper():
    # Connect to the client
    await client.start(phone_number)

    # Join the channel
    channel = await client.get_entity('https://t.me/NewPairsSolana')  # Replace with your channel link

    # Define a handler to print new messages
    @client.on(events.NewMessage(chats=channel))
    async def handler(event):
        result_text = event.message.text
        token_start_index = result_text.find('https://solscan.io/account/')
        end_index = result_text.find(')', token_start_index + 27)

        renounce_index = result_text.find('Renounced: ') + 11
        rug_index = result_text.find('Not Rugged ') + 11

        if result_text[renounce_index] == '✅':
            renounce_status = True
        else:
            renounce_status = False
        if result_text[rug_index] == '✅':
            rug_status = True
        else:
            rug_status = False

        token = result_text[(token_start_index+27): end_index]
        print(token)
        print(token_engine.get_metadata(0,token))
        print(token_engine.check_liveness(0, token))
        users = database.get_users()
        for user in users:
          chain = 0
          auto_sniper = user.auto_sniper[chain]

          token_sniper = auto_sniper['token']
          active, amount, slippage, wallet_id, auto_sell, min_market_captial, max_market_captial, stop_loss = (
            token_sniper['active'],
            token_sniper['amount'],
            token_sniper['slippage'],
            token_sniper['wallet_id'],
            token_sniper['auto_sell'],
            token_sniper['min_market_capital'],
            token_sniper['max_market_capital'],
            token_sniper['stop_loss']
          )
          if active:
            market_captial = token_engine.get_market_data(chain, token)['market_capital']
            if market_captial > min_market_captial and market_captial < max_market_captial and rug_status == True and renounce_status == True:
                token_sniper_id = time.time()
                count = 0
                token_snipers = database.get_token_snipers(user.id, chain)
                for sniper in token_snipers:
                  if sniper['is_auto'] == True:
                    count += 1
                print(f'auto count: {count}')
                if count == 0:
                  database.add_token_sniper(user.id, {
                    'id': token_sniper_id,
                    'stage': 'buy',
                    'chain': chain,
                    'token': token,
                    'amount': amount,
                    'slippage': slippage,
                    'wallet_id': wallet_id,
                    'auto_sell': auto_sell,
                    'stop_loss': stop_loss,
                    'is_auto': True
                  })
                  Thread(target=token_sniper_engine.start, args=(user.id, token_sniper_id)).start()
                else:
                  continue
       
          lp_sniper = auto_sniper['lp']
          active, amount, slippage, wallet_id = (
            lp_sniper['active'],
            lp_sniper['amount'],
            lp_sniper['slippage'],
            lp_sniper['wallet_id']
          )
          if active:
            lp_sniper_id = time.time()
            database.add_lp_sniper(user.id, {
              'id': lp_sniper_id,
              'stage': 'buy',
              'chain': chain,
              'token': token,
              'amount': amount,
              'slippage': slippage,
              'wallet_id': wallet_id
            })
            Thread(target=lp_sniper_engine.start, args=(user.id, lp_sniper_id)).start()
    # Run the client until disconnected
    await client.run_until_disconnected()

def run_auto_token_sniper():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(auto_token_sniper())
    loop.close()

def initialize():
    Thread(target=run_auto_token_sniper()).start()