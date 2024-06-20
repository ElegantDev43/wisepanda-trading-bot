from src.engine.swing.main import Control
import threading
import asyncio

async def updateData():
    while True:
        await Control()
    # await Control()


def run_update_data_in_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(updateData())
    loop.close()

def initialize():
    print('Starting the engine...')
    thread  = threading.Thread(target=run_update_data_in_thread)
    thread.start()