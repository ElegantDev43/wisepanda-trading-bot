from src.database import user as user_model
from src.database import Htokens as Htokens_model
from src.database import swing as swing_model

def initialize():
  user_model.initialize()
  Htokens_model.initialize()
  swing_model.initialize()