from threading import Thread

from src.engine import raydium
from src.engine.swing import main as swing_engine

def initialize():
  print('Initialize Engine')
  #swing_engine.initialize()
  Thread(target=raydium.initialize).start()