"Detect  New Pools Created on Solana Raydium DEX"

#MAnually see transactions of new pairs GThUX1Atko4tqhN2NaiTazWSeFWMuiUvfFnyJyUghFMJ under spl transfer section

from time import sleep
import logging

import asyncio
from typing import List, AsyncIterator, Tuple, Iterator
from asyncstdlib import enumerate

from solders.pubkey import Pubkey # type: ignore
from solders.rpc.config import RpcTransactionLogsFilterMentions # type: ignore

from solana.rpc.websocket_api import connect
from solana.rpc.commitment import Finalized
from solana.rpc.api import Client
from solana.exceptions import SolanaRpcException
from websockets.exceptions import ConnectionClosedError, ProtocolError

# Type hinting imports
from solana.rpc.commitment import Commitment
from solana.rpc.websocket_api import SolanaWsClientProtocol
from solders.rpc.responses import RpcLogsResponse, SubscriptionResult, LogsNotification, GetTransactionResp # type: ignore
from solders.signature import Signature # type: ignore
from solders.transaction_status import UiPartiallyDecodedInstruction, ParsedInstruction # type: ignore
from src.engine.chain.solana.token import is_valid, check_liveness, get_market_data, get_metadata

# Raydium Liquidity Pool V4
RaydiumLPV4 = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"
URI = "https://api.mainnet-beta.solana.com"  # "https://api.devnet.solana.com" | "https://api.mainnet-beta.solana.com"
WSS = "wss://api.mainnet-beta.solana.com"  # "wss://api.devnet.solana.com" | "wss://api.mainnet-beta.solana.com"
solana_client = Client(URI)
# Raydium function call name, look at raydium-amm/program/src/instruction.rs
log_instruction = "initialize2"
seen_signatures = set()


# Init logging
logging.basicConfig(filename='app.log', filemode='a', level=logging.DEBUG)
# Writes responses from socket to messages.json
# Writes responses from http req to  transactions.json

async def main():
  """The client as an infinite asynchronous iterator:"""
  async for websocket in connect(WSS):
    try:
      subscription_id = await subscribe_to_logs(
        websocket,
        RpcTransactionLogsFilterMentions(RaydiumLPV4),
        Finalized
      )
      # Change level debugging to INFO
      logging.getLogger().setLevel(logging.INFO)  # Logging
      async for i, signature in enumerate(process_messages(websocket, log_instruction)):  # type: ignore
        logging.info(f"{i=}")  # Logging
        try:
          get_tokens(signature, RaydiumLPV4)
        except SolanaRpcException as err:
          # Omitting httpx.HTTPStatusError: Client error '429 Too Many Requests'
          # Sleep 5 sec, and try connect again
          # Start logging
          logging.exception(err)
          logging.info("sleep for 5 seconds and try again")
          # End logging
          sleep(5)
          continue
    except (ProtocolError, ConnectionClosedError) as err:
      # Restart socket connection if ProtocolError: invalid status code
      logging.exception(err)  # Logging
      print(f"Danger! Danger!", err)
      continue
    except KeyboardInterrupt:
      if websocket:
        await websocket.logs_unsubscribe(subscription_id)


async def subscribe_to_logs(websocket: SolanaWsClientProtocol, 
              mentions: RpcTransactionLogsFilterMentions,
              commitment: Commitment) -> int:
  await websocket.logs_subscribe(
    filter_=mentions,
    commitment=commitment
  )
  first_resp = await websocket.recv()
  return get_subscription_id(first_resp)  # type: ignore


def get_subscription_id(response: SubscriptionResult) -> int:
  return response[0].result


async def process_messages(websocket: SolanaWsClientProtocol,
               instruction: str) -> AsyncIterator[Signature]:
  """Async generator, main websocket's loop"""
  async for idx, msg in enumerate(websocket):
    value = get_msg_value(msg)
    if not idx % 100:
      pass
      # print(f"{idx=}")
    for log in value.logs:
      if instruction not in log:
        continue
      # Start logging
      logging.info(value.signature)
      logging.info(log)
      # Logging to messages.json
      with open("messages.json", 'a', encoding='utf-8') as raw_messages:  
        raw_messages.write(f"signature: {value.signature} \n")
        raw_messages.write(msg[0].to_json())
        raw_messages.write("\n ########## \n")
      # End logging
      yield value.signature


def get_msg_value(msg: List[LogsNotification]) -> RpcLogsResponse:
  return msg[0].result.value


def get_tokens(signature: Signature, RaydiumLPV4: Pubkey) -> None:
  """httpx.HTTPStatusError: Client error '429 Too Many Requests' 
  for url 'https://api.mainnet-beta.solana.com'
  For more information check: https://httpstatuses.com/429

  """
  # if signature not in seen_signatures:
  #     seen_signatures.add(signature)
  transaction = solana_client.get_transaction(
    signature,
    encoding="jsonParsed",
    max_supported_transaction_version=0
  )
  # Start logging to transactions.json
  with open("transactions.json", 'a', encoding='utf-8') as raw_transactions:
    raw_transactions.write(f"signature: {signature}\n")
    raw_transactions.write(transaction.to_json())        
    raw_transactions.write("\n ########## \n")
  # End logging
  instructions = get_instructions(transaction)
  filtred_instuctions = instructions_with_program_id(instructions, RaydiumLPV4)
  logging.info(filtred_instuctions)
  for instruction in filtred_instuctions:
    tokens = get_tokens_info(instruction)
    print_table(tokens)
    # print(f"True, https://solscan.io/tx/{signature}")



def get_instructions(
  transaction: GetTransactionResp
) -> List[UiPartiallyDecodedInstruction | ParsedInstruction]:
  instructions = transaction \
           .value \
           .transaction \
           .transaction \
           .message \
           .instructions
  return instructions


def instructions_with_program_id(
  instructions: List[UiPartiallyDecodedInstruction | ParsedInstruction],
  program_id: str
) -> Iterator[UiPartiallyDecodedInstruction | ParsedInstruction]:
  return (instruction for instruction in instructions
      if instruction.program_id == program_id)


def get_tokens_info(
  instruction: UiPartiallyDecodedInstruction | ParsedInstruction
) -> Tuple[Pubkey, Pubkey, Pubkey]:
  accounts = instruction.accounts
  Pair = accounts[4]
  Token0 = accounts[8]
  Token1 = accounts[9]
  # Start logging
  logging.info("find LP !!!")
  logging.info(f"\n Token0: {Token0}, \n Token1: {Token1}, \n Pair: {Pair}")
  # End logging
  return (Token0, Token1, Pair)


def print_table(tokens: Tuple[Pubkey, Pubkey, Pubkey]) -> None:
  data = [
    {'Token_Index': 'Token0', 'Account Public Key': tokens[0]},  # Token0
    {'Token_Index': 'Token1', 'Account Public Key': tokens[1]},  # Token1
    {'Token_Index': 'LP Pair', 'Account Public Key': tokens[2]}  # LP Pair
  ]
  # print("============NEW POOL DETECTED====================")
  # header = ["Token_Index", "Account Public Key"]
  # print("│".join(f" {col.ljust(15)} " for col in header))
  # print("|".rjust(18))
  # for row in data:
  #   print("│".join(f" {str(row[col]).ljust(15)} " for col in header))
  if str(tokens[0]) == 'So11111111111111111111111111111111111111112':
    token = tokens[1]
  else:
    token = tokens[0]
  
  token = str(token)
  
  from src.engine.chain import token as token_engine
  metadata = token_engine.get_metadata(0, token)
  market_data = token_engine.get_market_data(0, token)
  
  token_symbol = metadata['symbol']
  token_mc = market_data['market_capital']
  
  print('Raydium Launch', token, token_symbol, token_mc)
  print('Is valid', is_valid(token))
  print('Liveness', check_liveness(token))
  print('Market', get_market_data(token))
  print('MetaData', get_metadata(token))
  
  import time
  from threading import Thread
  
  from src.database import api as database
  from src.engine.chain import token as token_engine
  from src.engine import token_sniper as token_sniper_engine
  from src.engine import lp_sniper as lp_sniper_engine
  
  users = database.get_users()
  for user in users:
    chain = 0
    auto_sniper = user.auto_sniper[chain]

    token_sniper = auto_sniper['token']
    active, amount, slippage, wallet_id, auto_sell, min_market_captial, max_market_captial, limit, count = (
      token_sniper['active'],
      token_sniper['amount'],
      token_sniper['slippage'],
      token_sniper['wallet_id'],
      token_sniper['auto_sell'],
      token_sniper['min_market_capital'],
      token_sniper['max_market_capital'],
      token_sniper['limit'],
      token_sniper['count']
    )
    if active:
      market_captial = token_engine.get_market_data(chain, token)['market_capital']
      if market_captial > min_market_captial and market_captial < max_market_captial:
        if limit != 0 and count != limit:
          token_sniper_id = time.time()
          database.add_token_sniper(user.id, {
            'id': token_sniper_id,
            'stage': 'buy',
            'chain': chain,
            'token': token,
            'amount': amount,
            'slippage': slippage,
            'wallet_id': wallet_id,
            'auto_sell': auto_sell
          })
          Thread(target=token_sniper_engine.start, args=(user.id, token_sniper_id)).start()
          
          count += 1
          token_sniper['count'] = count
          if count == limit:
            token_sniper['active'] = False
          auto_sniper['token'] = token_sniper
          database.set_auto_sniper(user.id, chain, auto_sniper)
    
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

def initialize():
  global RaydiumLPV4
  RaydiumLPV4 = Pubkey.from_string(RaydiumLPV4)
  asyncio.run(main())