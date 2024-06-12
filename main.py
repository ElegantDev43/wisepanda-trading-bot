from dotenv import load_dotenv
load_dotenv()

from src.database import main as database
from src.telegram import main as telegram

database.initialize()
telegram.initialize()

# import test
# test.initialize()