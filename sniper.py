from web3 import Web3
import json
from datetime import datetime
import threading
import time

import config
import contract

def update():
    return

def start(id, flags):
    while flags[id]:
        print(f'{id} is running')
        update()
        time.sleep(1)

    print(f'{id} is stopped')