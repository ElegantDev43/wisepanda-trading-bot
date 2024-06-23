from threading import Thread

from src.engine.chain.solana import raydium

def initialize():
  print('Initialize Engine')
  # Thread(target=raydium.initialize).start()