from src.database import user as user_model

def initialize():
  print('Intialize Database')
  user_model.initialize()