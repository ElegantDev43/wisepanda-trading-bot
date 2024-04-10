from src.database import sniper as sniper_model

auto_sniper_tokens = [1,2]

def initialize():
    global auto_sniper_tokens
    auto_sniper_tokens = sniper_model.get_tokens()
