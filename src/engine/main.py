from threading import Thread
import asyncio

from src.engine import raydium
from src.engine import stop_loss_engine
from src.engine.swing import main as swing

def initialize():
  print('Initialize Engine')
 # swing.initialize()
  raydium.initialize()