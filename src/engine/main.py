from threading import Thread

from src.engine import lp_sniper

from src.engine.swing import main as swing_engine

def initialize():
  print('Initialize Engine')
  
  #swing_engine.initialize()
  
  #Thread(target=lp_sniper.initialize).start()