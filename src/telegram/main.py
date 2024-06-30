import os
import telebot
from telebot import types

from src.telegram import start, buyer, token_snipers, manual_buyer, bots, hots,seller, limit_order, dca_order, lp_snipers
from src.telegram.settings import main as settings, chains, wallets, keyboards, auto_order
from src.telegram.swing import swing as main_swing, fully_auto, token_mode, manual_mode
from src.telegram.lp_sniper import lp_sniper, lp_auto, lp_manual
from src.telegram.token_sniper import token_sniper_auto, sniper, token_sniper_manual

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

commands = [
    types.BotCommand("start", "Main menu"),
    types.BotCommand("hots", "List the 10 hot tokens"),
    types.BotCommand("orders", "List all pending orders"),
    types.BotCommand("positions", "Overview of all your holdings"),
    types.BotCommand("chains", "List all supported chains"),
    types.BotCommand("wallets", "List your wallets"),
    types.BotCommand("settings", "Bring up the settings tab"),
    types.BotCommand("criterias", "Customize your ceriterias"),
    types.BotCommand("keyboards", "Select your trading keys"),
    types.BotCommand("bots", "List all available backup bots")
]

chain_titles = ['ethereum', 'solana', 'base']
bot.set_my_commands(commands)


@bot.message_handler(commands=['start'])
def handle_start(message):
    start.handle_start(bot, message)


@bot.message_handler(commands=['hots'])
def handle_hots(message):
    hots.handle_hots(bot, message)


@bot.message_handler(commands=['chains'])
def handle_chain(message):
    chains.handle_chains(bot, message)


@bot.message_handler(commands=['wallets'])
def handle_wallets(message):
    wallets.handle_wallets(bot, message)


@bot.message_handler(commands=['settings'])
def handle_settings(message):
    settings.handle_settings(bot, message)


@bot.message_handler(commands=['bots'])
def handle_bots(message):
    bots.handle_bots(bot, message)


@bot.message_handler(commands=['keyboards'])
def handle_keyboards(message):
    keyboards.handle_keyboards(bot, message)


@bot.message_handler(commands=['criterias'])
def handle_bots(message):
    bots.handle_bots(bot, message)


@bot.callback_query_handler(func=lambda _: True)
def handle_callback_query(call):
    if call.data == 'start':
        start.handle_start(bot, call.message)
    elif call.data == 'hots':
        hots.handle_hots(bot, call.message)
    elif call.data.startswith('hot '):
        token = call.data[4:]
        call.message.text = token
        buyer.handle_input_token(bot, call.message)
    elif call.data == 'sniper':
        sniper.handle_sniper(bot, call.message)
    elif call.data == 'lp sniper':
        lp_sniper.handle_lp_sniper(bot, call.message)
    elif call.data == 'lp sniper select auto mode':
        lp_auto.handle_start(bot, call.message)
    elif call.data == 'lp sniper select manual mode':
        lp_manual.handle_start(bot, call.message)

    elif call.data == 'lp auto show more wallets':
        lp_auto.handle_more_btn(bot, call.message)
    elif call.data == 'make lp sniper auth order':
        lp_auto.handle_set_sniper(bot, call.message)
    elif call.data == 'lmake lp sniper order':
        lp_auto.handle_set_sniper(bot, call.message)
    elif call.data.startswith('lp auto select buy wallet '):
        lp_auto.select_buy_wallet(bot, call.message, call.data[26:])
    elif call.data.startswith('lp auto select buy amount '):
        amount = call.data[26:]
        if (amount == 'x'):
            lp_auto.handle_buy_amount_x(bot, call.message)
        else:
            lp_auto.select_buy_amount(bot, call.message, call.data[26:])
    elif call.data.startswith('lp auto select slippage '):
        amount = call.data[24:]
        if (amount == 'x'):
            lp_auto.handle_slippage_x(bot, call.message)
        else:
            lp_auto.handle_select_auto_slippage(bot, call.message, call.data[24:])
    elif call.data.startswith('lp auto confirm select slippage '):
        lp_auto.select_slip_page(bot, call.message, call.data[32:])
    elif call.data == 'make lp auto order':
        lp_auto.handle_set_sniper(bot, call.message)    

    elif call.data.startswith('lp manual select buy wallet '):
        lp_manual.select_buy_wallet(bot, call.message, call.data[28:])
    elif call.data.startswith('lp manual select buy amount '):
        amount = call.data[28:]
        if (amount == 'x'):
            lp_manual.handle_buy_amount_x(bot, call.message)
        else:
            lp_manual.select_buy_amount(bot, call.message, call.data[28:])
    elif call.data.startswith('lp manual select slippage '):
        amount = call.data[26:]
        if (amount == 'x'):
            lp_manual.handle_slippage_x(bot, call.message)
        else:
            lp_manual.handle_select_auto_slippage(bot, call.message, call.data[26:])
    elif call.data.startswith('lp manual confirm select slippage '):
        lp_manual.select_slip_page(bot, call.message, call.data[34:])
    elif call.data == 'make lp manual order':
        lp_manual.handle_set_sniper(bot, call.message)   
    elif call.data == 'lp manual show more wallets':
        lp_manual.handle_more_btn(bot, call.message)
  #  elif call.data == 'buyer':
  #      buyer.handle_buyer(bot, call.message)

    elif call.data == 'settings':
        settings.handle_settings(bot, call.message)
    elif call.data == 'bots':
        bots.handle_bots(bot, call.message)
    elif call.data == 'close':
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
    elif call.data == 'chains':
        chains.handle_chains(bot, call.message)
    elif call.data in chain_titles:
        chains.handle_select_chain(bot, call.message, call.data)
        # New api
    elif call.data == 'auto-orders':
        auto_order.handle_auto_orders(bot, call.message)
    elif call.data == 'auto_buy_order_status_change':
        auto_order.handle_buy_status(bot, call.message)
    elif call.data == 'auto_sell_order_status_change':
        auto_order.handle_sell_status(bot, call.message)
    elif call.data.startswith('handle_input_auto_buy_order '):
        item = call.data[28:]
        auto_order.handle_buy_input(bot, call.message, item)
    elif call.data.startswith('handle_input_auto_sell_order '):
        item = call.data[29:]
        auto_order.handle_sell_input(bot, call.message, item)
    elif call.data == 'handle update auto order':
        auto_order.handle_update(bot, call.message)
    elif call.data == 'wallets':
        wallets.handle_wallets(bot, call.message)
  #  elif call.data in config.BUY_AMOUNT:
   #     keyboards.handle_select_buy_amount(bot, call.message, call.data)
   # elif call.data in config.GAS_AMOUNT:
   #     keyboards.handle_select_gas_amount(bot, call.message, call.data)
   # elif call.data in config.SELL_AMOUNT:
   #     keyboards.handle_select_sell_amount(bot, call.message, call.data)
   # elif call.data == 'remove_wallet':

    elif call.data.startswith('select keyboard buy amount '):
        keyboards.handle_default_values(
            bot, call.message, call.data[16:19], call.data[27:])
    elif call.data.startswith('select keyboard gas amount '):
        keyboards.handle_default_values(
            bot, call.message, call.data[16:19], call.data[27:])
    elif call.data.startswith('select keyboard sell amount '):
        keyboards.handle_default_values(
            bot, call.message, call.data[16:20], call.data[28:])

    elif call.data == 'manage-limit-orders':
        limit_order.handle_orders(bot, call.message)
    elif call.data == 'handle_next_limit_order':
        limit_order.handle_next_order(bot, call.message)
    elif call.data == 'handle_prev_limit_order':
        limit_order.handle_prev_order(bot, call.message)
    elif call.data == 'handle_remove_limit_order':
        limit_order.handle_remove_order(bot, call.message)
    elif call.data == 'handle_update_limit_order':
        limit_order.handle_update_order(bot, call.message)
    elif call.data.startswith('handle_limit_input '):
        item = call.data[19:]
        limit_order.handle_input(bot, call.message, item)

    elif call.data == 'manage-token-snipers':
        token_snipers.handle_orders(bot, call.message)
    elif call.data == 'handle_next_token_sniper':
        token_snipers.handle_next_order(bot, call.message)
    elif call.data == 'handle_prev_token_sniper':
        token_snipers.handle_prev_order(bot, call.message)
    elif call.data == 'handle_remove_token_sniper':
        token_snipers.handle_remove_order(bot, call.message)
    elif call.data == 'handle_update_token_sniper':
        token_snipers.handle_update_order(bot, call.message)
    elif call.data == 'handle_sniper_add_auto_param':
        token_snipers.handle_add_auto_param(bot, call.message)
    elif call.data.startswith('handle_sniper_remove_auto_params '):
        item = call.data[32:]
        token_snipers.handle_remove_auto_param(bot, call.message, item)
    elif call.data.startswith('handle_sniper_auto_amount '):
        item = call.data[26:]
        token_snipers.handle_input_auto_amount(bot, call.message, item)
    elif call.data.startswith('handle_sniper_auto_price '):
        item = call.data[25:]
        token_snipers.handle_input_auto_price(bot, call.message, item)
    elif call.data.startswith('handle_token_sniper_input '):
        item = call.data[26:]
        token_snipers.handle_input(bot, call.message, item)


    elif call.data == 'manage-lp-snipers':
        lp_snipers.handle_orders(bot, call.message)
    elif call.data == 'handle_next_lp_sniper':
        lp_snipers.handle_next_order(bot, call.message)
    elif call.data == 'handle_prev_lp_sniper':
        lp_snipers.handle_prev_order(bot, call.message)
    elif call.data == 'handle_remove_lp_sniper':
        lp_snipers.handle_remove_order(bot, call.message)
    elif call.data == 'handle_update_lp_sniper':
        lp_snipers.handle_update_order(bot, call.message)
    elif call.data.startswith('handle_lp_sniper_input '):
        item = call.data[23:]
        lp_snipers.handle_input(bot, call.message, item)


    elif call.data == 'manage-dca-orders':
        dca_order.handle_orders(bot, call.message)
    elif call.data == 'handle_next_dca_order':
        dca_order.handle_next_order(bot, call.message)
    elif call.data == 'handle_prev_dca_order':
        dca_order.handle_prev_order(bot, call.message)
    elif call.data == 'handle_remove_dca_order':
        dca_order.handle_remove_order(bot, call.message)
    elif call.data == 'handle_update_dca_order':
        dca_order.handle_update_order(bot, call.message)
    elif call.data.startswith('handle_dca_input '):
        item = call.data[17:]
        dca_order.handle_input(bot, call.message, item)


    elif call.data == 'create_wallet':
        wallets.handle_create_wallet(bot, call.message)
    elif call.data == 'import_wallet':
        wallets.handle_import_wallet(bot, call.message)
    elif call.data == 'remove_wallet':
        wallets.handle_remove_wallet(bot, call.message)
    elif call.data.startswith('select_remove_wallet '):
        wallets.remove_selected_wallet(bot, call.message, call.data[21:])
        
######### Seller#####
# sniper

    elif call.data == 'sniper select auto mode':
        token_sniper_auto.handle_start(bot, call.message)
    elif call.data.startswith('token_sniper_auto amount '):
      data = call.data[25:]
      if data == 'default':
        token_sniper_auto.handle_default_values(bot, call.message, 'amount')
      elif data == 'x':
        token_sniper_auto.handle_x_values(bot, call.message, 'amount')
    elif call.data.startswith('token_sniper_auto slippage '):
      data = call.data[27:]
      if data == 'default':
        token_sniper_auto.handle_confirm_auto_slippage(bot, call.message)
      elif data == 'x':
        token_sniper_auto.handle_x_values(bot, call.message, 'slippage')
      elif data == 'confirm':
        token_sniper_auto.handle_default_slippage(bot, call.message)
    elif call.data.startswith('token_sniper_auto select buy wallet '):
        token_sniper_auto.select_wallet(bot, call.message, call.data[36:])
    elif call.data == 'token_sniper_auto show more wallets':
        token_sniper_auto.handle_show_more_wallets(bot, call.message)
    elif call.data == 'token_sniper_auto stop-loss':
        token_sniper_auto.handle_x_values(bot, call.message, 'stop-loss')
    elif call.data == 'token_sniper_auto min_market_cap':
        token_sniper_auto.handle_x_values(bot, call.message, call.data[18:])
    elif call.data == 'token_sniper_auto max_market_cap':
        token_sniper_auto.handle_x_values(bot, call.message, call.data[18:])
    elif call.data == 'token_sniper_auto set auto_sell':
        token_sniper_auto.handle_auto_sell_status(bot, call.message)
    elif call.data == 'token_sniper_auto add auto params':
        token_sniper_auto.handle_add_auto_sell_param(bot, call.message)
    elif call.data == 'token_sniper_auto remove auto params':
        token_sniper_auto.handle_remove_auto_sell_param(bot, call.message)
    elif call.data.startswith('token_sniper_auto auto_sell '):
        token_sniper_auto.handle_auto_sell_input_values(bot, call.message, call.data[28:])
    elif call.data.startswith('token_sniper_auto auto_profit '):
        token_sniper_auto.handle_auto_profit_input_values(bot, call.message, call.data[30:])
    elif call.data == 'make sniper auto order':
        token_sniper_auto.handle_sniper_status(bot, call.message)

    elif call.data == 'sniper select manual mode':
        token_sniper_manual.handle_start(bot, call.message)
    elif call.data == 'token_sniper_manual make order':
        token_sniper_manual.handle_make_order(bot, call.message)
    elif call.data.startswith('token_sniper_manual amount '):
      data = call.data[27:]
      if data == 'default':
        token_sniper_manual.handle_default_values(bot, call.message, 'amount')
      elif data == 'x':
        token_sniper_manual.handle_x_values(bot, call.message, 'amount')
    elif call.data.startswith('token_sniper_manual slippage '):
      data = call.data[29:]
      if data == 'default':
        token_sniper_manual.handle_confirm_auto_slippage(bot, call.message)
      elif data == 'x':
        token_sniper_manual.handle_x_values(bot, call.message, 'slippage')
      elif data == 'confirm':
        token_sniper_manual.handle_default_slippage(bot, call.message)
    elif call.data.startswith('token_sniper_manual select buy wallet '):
        token_sniper_manual.select_wallet(bot, call.message, call.data[38:])
    elif call.data == 'token_sniper_manual show more wallets':
        token_sniper_manual.handle_show_more_wallets(bot, call.message)
    elif call.data == 'token_sniper_manual stop-loss':
        token_sniper_manual.handle_x_values(bot, call.message, 'stop-loss')
    elif call.data == 'token_sniper_manual set auto_sell':
        token_sniper_manual.handle_auto_sell_status(bot, call.message)
    elif call.data == 'token_sniper_manual add auto params':
        token_sniper_manual.handle_add_auto_sell_param(bot, call.message)
    elif call.data == 'token_sniper_manual remove auto params':
        token_sniper_manual.handle_remove_auto_sell_param(bot, call.message)
    elif call.data.startswith('token_sniper_manual auto_sell '):
        token_sniper_manual.handle_auto_sell_input_values(bot, call.message, call.data[30:])
    elif call.data.startswith('token_sniper_manual auto_profit '):
        token_sniper_manual.handle_auto_profit_input_values(bot, call.message, call.data[32:])
    elif call.data == 'make sniper manual order':
        token_sniper_manual.handle_make_order(bot, call.message)
        
    elif call.data == 'buyer':
        manual_buyer.handle_start(bot, call.message)
    elif call.data.startswith('buyer amount '):
      data = call.data[13:]
      if data == 'default':
        manual_buyer.handle_default_values(bot, call.message, 'amount')
      elif data == 'x':
        manual_buyer.handle_x_values(bot, call.message, 'amount')
    elif call.data.startswith('buyer slippage '):
      data = call.data[15:]
      if data == 'default':
        manual_buyer.handle_confirm_auto_slippage(bot, call.message)
      elif data == 'x':
        manual_buyer.handle_x_values(bot, call.message, 'slippage')
      elif data == 'confirm':
        manual_buyer.handle_default_slippage(bot, call.message)
    elif call.data.startswith('buyer select buy wallet '):
        manual_buyer.select_wallet(bot, call.message, call.data[24:])
    elif call.data == 'buyer show more wallets':
        manual_buyer.handle_show_more_wallets(bot, call.message)
    elif call.data == 'buyer stop-loss':
        manual_buyer.handle_x_values(bot, call.message, 'stop-loss')
    elif call.data == 'buyer max_market_capital':
        manual_buyer.handle_x_values(bot, call.message, 'max_market_capital')
    elif call.data == 'buyer interval':
        manual_buyer.handle_x_values(bot, call.message, 'interval')
    elif call.data == 'buyer count':
        manual_buyer.handle_x_values(bot, call.message, 'count')
    elif call.data == 'buyer market_order':
        manual_buyer.handle_market_order(bot, call.message)
    elif call.data == 'buyer limit_order':
        manual_buyer.handle_limit_order(bot, call.message)
    elif call.data == 'buyer dca_order':
        manual_buyer.handle_dca_order(bot, call.message)
    elif call.data == 'buyer make order':
        manual_buyer.handle_make_order(bot, call.message)


    elif call.data == 'seller':
        seller.handle_start(bot, call.message)
    elif call.data.startswith('seller amount '):
      data = call.data[14:]
      if data == 'default':
        seller.handle_default_values(bot, call.message, 'amount')
      elif data == 'x':
        seller.handle_x_values(bot, call.message, 'amount')
    elif call.data.startswith('seller slippage '):
      data = call.data[16:]
      if data == 'default':
        seller.handle_confirm_auto_slippage(bot, call.message)
      elif data == 'x':
        seller.handle_x_values(bot, call.message, 'slippage')
      elif data == 'confirm':
        seller.handle_default_slippage(bot, call.message)
    elif call.data == 'seller profit':
        seller.handle_x_values(bot, call.message, 'profit')
    elif call.data == 'seller interval':
        seller.handle_x_values(bot, call.message, 'interval')
    elif call.data == 'seller count':
        seller.handle_x_values(bot, call.message, 'count')
    elif call.data == 'seller market_order':
        seller.handle_market_order(bot, call.message)
    elif call.data == 'seller limit_order':
        seller.handle_limit_order(bot, call.message)
    elif call.data == 'seller dca_order':
        seller.handle_dca_order(bot, call.message)
    elif call.data == 'seller make order':
        seller.handle_make_order(bot, call.message)
    elif call.data == 'buyer make order':
        seller.handle_make_order(bot, call.message)
    elif call.data.startswith('seller select position '):
        seller.handle_select_position(bot, call.message, call.data[23:])
        
    elif call.data == 'swing':
        main_swing.handle_start(bot, call.message)
    elif call.data == 'swing mode auto':
        fully_auto.handle_start(bot, call.message)
    elif call.data == 'swing mode manual':
        manual_mode.handle_start(bot, call.message)
    elif call.data.startswith('swing_auto amount '):
      data = call.data[18:]
      if data == 'default':
        fully_auto.handle_default_values(bot, call.message, 'amount')
      elif data == 'x':
        fully_auto.handle_x_values(bot, call.message, 'amount')
    elif call.data.startswith('swing_auto slippage '):
      data = call.data[20:]
      if data == 'default':
        fully_auto.handle_confirm_auto_slippage(bot, call.message)
      elif data == 'x':
        fully_auto.handle_x_values(bot, call.message, 'slippage')
      elif data == 'confirm':
        fully_auto.handle_default_slippage(bot, call.message)
    elif call.data.startswith('swing_auto select buy wallet '):
        fully_auto.select_wallet(bot, call.message, call.data[29:])
    elif call.data == 'swing_auto show more wallets':
        fully_auto.handle_show_more_wallets(bot, call.message)
    elif call.data == 'swing_auto stop-loss':
        fully_auto.handle_x_values(bot, call.message, 'stop-loss')
    elif call.data == 'swing_auto market_capital':
        fully_auto.handle_x_values(bot, call.message, 'market_capital')
    elif call.data == 'swing_auto take-profit':
        fully_auto.handle_x_values(bot, call.message, 'take-profit')
    elif call.data == 'swing_auto start trading':
        fully_auto.handle_trading_tatus(bot, call.message)

    elif call.data == 'swing mode manual':
        manual_mode.handle_start(bot, call.message)
    elif call.data.startswith('swing_manual amount '):
      data = call.data[20:]
      if data == 'default':
        manual_mode.handle_default_values(bot, call.message, 'amount')
      elif data == 'x':
        manual_mode.handle_x_values(bot, call.message, 'amount')
    elif call.data.startswith('swing_manual slippage '):
      data = call.data[22:]
      if data == 'default':
        manual_mode.handle_confirm_auto_slippage(bot, call.message)
      elif data == 'x':
        manual_mode.handle_x_values(bot, call.message, 'slippage')
      elif data == 'confirm':
        manual_mode.handle_default_slippage(bot, call.message)
    elif call.data.startswith('swing_manual select buy wallet '):
        manual_mode.select_wallet(bot, call.message, call.data[31:])
    elif call.data == 'swing_manual show more wallets':
        manual_mode.handle_show_more_wallets(bot, call.message)
    elif call.data == 'swing_manual stop-loss':
        manual_mode.handle_x_values(bot, call.message, 'stop-loss')
def initialize():
    print('Starting the bot...')
    bot.infinity_polling(restart_on_change=False)
