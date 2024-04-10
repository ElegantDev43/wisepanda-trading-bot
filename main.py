from dotenv import load_dotenv
load_dotenv()

from src.database import main as database
import globals
from src.telegram import main as telegram

database.initialize()
globals.initialize()
telegram.start_bot()
