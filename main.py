from src import database
from src.bot import main as bot

database.initialize()
bot.start_bot()
