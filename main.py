import threading
import time

import telegram
import sniper

telegram.start()

# for index in range(3):
#     thread = threading.Thread(target=sniper.start, name=f'Thread {index}')
#     thread.start()