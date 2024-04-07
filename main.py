from src.database import main as database
from src.telegram import main as telegram

database.initialize()

telegram.start_bot()
