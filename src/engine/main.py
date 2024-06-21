from threading import Thread

from src.engine import lp_sniper

def initialize():
  print('Initialize Engine')
  
  Thread(target=lp_sniper.initialize).start()