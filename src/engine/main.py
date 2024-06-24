from threading import Thread

from src.engine import raydium

def initialize():
  print('Initialize Engine')
  
  Thread(target=raydium.initialize).start()