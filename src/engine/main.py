from threading import Thread

from src.engine import raydium
from src.engine.swing import main as swing

def initialize():
  print('Initialize Engine')
  # swing.initialize()
  #Thread(target=raydium.initialize).start()