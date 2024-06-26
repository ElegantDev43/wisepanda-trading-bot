import os
import telebot
from telebot import types

from src.telegram import start, sniper, buyer, token_snipers, positions, bots, hots,seller, limit_order, dca_order, lp_snipers
from src.telegram.settings import main as settings, chains, wallets, keyboards, auto_order
from src.telegram.swing import swing as main_swing, fully_auto, token_mode, manual_mode
from src.telegram.lp_sniper import lp_sniper, lp_auto, lp_manual

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
    elif call.data == 'buyer':
        buyer.handle_buyer(bot, call.message)

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

    elif call.data == 'seller':
        seller.handle_positions(bot, call.message)
    elif call.data == 'seller-limit-orders':
        seller.handle_limit_order(bot, call.message)
    elif call.data == 'seller-market-orders':
        seller.handle_market_order(bot, call.message)
    elif call.data == 'seller-dca-orders':
        seller.handle_dca_order(bot, call.message)

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

    # Market Order
    elif call.data == 'buy-limit-orders':
        buyer.handle_limit_order(bot, call.message)
    elif call.data == 'buy-market-orders':
        buyer.handle_market_order(bot, call.message)
    elif call.data == 'buy-dca-orders':
        buyer.handle_dca_order(bot, call.message)
    elif call.data == 'buyer show more wallets':
        buyer.handle_more_btn(bot, call.message)

    elif call.data == 'create_wallet':
        wallets.handle_create_wallet(bot, call.message)
    elif call.data == 'import_wallet':
        wallets.handle_import_wallet(bot, call.message)
    elif call.data == 'remove_wallet':
        wallets.handle_remove_wallet(bot, call.message)
    elif call.data.startswith('select_remove_wallet '):
        wallets.remove_selected_wallet(bot, call.message, call.data[21:])
        
    elif call.data == 'sniper show more wallets':
        sniper.handle_more_btn(bot, call.message)
    elif call.data.startswith('auto wallet '):
        sniper.handle_toggle_wallet(bot, call.message, call.data[12:])
    elif call.data.startswith('auto buy '):
        amount = call.data[9:]
        if amount == 'x':
            sniper.handle_buy_x(bot, call.message)
        else:
            amount = float(amount)
            sniper.handle_buy(bot, call.message, amount)

    elif call.data.startswith('select buy wallet '):
        buyer.select_buy_wallet(bot, call.message, call.data[18:])
    elif call.data == 'make buy order':
        buyer.handle_buy(bot, call.message)
    elif call.data == 'make sell order':
        seller.handle_sell(bot, call.message)
    elif call.data.startswith('select buy amount '):
        amount = call.data[18:]
        if (amount == 'x'):
            buyer.handle_buy_amount_x(bot, call.message)
        else:
            buyer.select_buy_amount(bot, call.message, call.data[18:])
    elif call.data.startswith('select slippage '):
        amount = call.data[16:]
        if (amount == 'x'):
            buyer.handle_slippage_x(bot, call.message)
        else:
            buyer.handle_select_auto_slippage(bot, call.message, call.data[16:])
    elif call.data.startswith('confirm select slippage '):
        buyer.select_slip_page(bot, call.message, call.data[24:])
    elif call.data.startswith('select stop loss '):
        amount = call.data[17:]
        if (amount == 'x'):
            buyer.handle_stop_loss_x(bot, call.message)
    elif call.data.startswith('select limit token price '):
        amount = call.data[25:]
        if (amount == 'x'):
            buyer.handle_limit_token_price_x(bot, call.message)
        buyer.select_limit_token_price(bot, call.message, call.data[25:])
    elif call.data.startswith('select limit tax '):
        amount = call.data[17:]
        if (amount == 'x'):
            buyer.handle_limit_tax_x(bot, call.message)
        buyer.select_limit_tax(bot, call.message, call.data[17:])
    elif call.data.startswith('select market capital '):
        amount = call.data[22:]
        if (amount == 'x'):
            buyer.handle_market_capital_x(bot, call.message)
        buyer.select_market_capital(bot, call.message, call.data[22:])
    elif call.data.startswith('select liquidity '):
        amount = call.data[17:]
        if (amount == 'x'):
            buyer.handle_liquidity_x(bot, call.message)
        buyer.select_liquidity(bot, call.message, call.data[17:])

    elif call.data.startswith('select interval '):
        amount = call.data[16:]
        if (amount == 'x'):
            buyer.handle_interval_x(bot, call.message)
        buyer.select_interval(bot, call.message, call.data[16:])
    elif call.data.startswith('select duration '):
        amount = call.data[16:]
        if (amount == 'x'):
            buyer.handle_duration_x(bot, call.message)
        buyer.select_duration(bot, call.message, call.data[16:])
    elif call.data.startswith('select max price '):
        amount = call.data[17:]
        if (amount == 'x'):
            buyer.handle_max_price_x(bot, call.message)
        buyer.select_max_price(bot, call.message, call.data[17:])
    elif call.data.startswith('select min price '):
        amount = call.data[17:]
        if (amount == 'x'):
            buyer.handle_min_price_x(bot, call.message)
        buyer.select_min_price(bot, call.message, call.data[17:])


######### Seller#####
    elif call.data.startswith('seller select buy wallet '):
        seller.select_buy_wallet(bot, call.message, call.data[25:])
    elif call.data == 'make order':
        seller.handle_buy(bot, call.message)

    elif call.data.startswith('seller select buy amount '):
        amount = call.data[25:]
        if (amount == 'x'):
            seller.handle_buy_amount_x(bot, call.message)
        else:
            seller.select_buy_amount(bot, call.message, call.data[25:])
    elif call.data.startswith('seller select gas amount '):
        amount = call.data[25:]
        if (amount == 'x'):
            seller.handle_gas_amount_x(bot, call.message)
        seller.select_gas_amount(bot, call.message, call.data[25:])
    elif call.data.startswith('seller select gas price '):
        amount = call.data[24:]
        if (amount == 'x'):
            seller.handle_gas_price_x(bot, call.message)
        seller.select_gas_price(bot, call.message, call.data[24:])
    elif call.data.startswith('seller select slippage '):
        amount = call.data[23:]
        if (amount == 'x'):
            seller.handle_slippage_x(bot, call.message)
        else:
            seller.handle_select_auto_slippage(bot, call.message, call.data[23:])
    elif call.data.startswith('confirm seller select slippage '):
        seller.select_slip_page(bot, call.message, call.data[31:])

    elif call.data.startswith('seller select limit token price '):
        amount = call.data[32:]
        if (amount == 'x'):
            seller.handle_limit_token_price_x(bot, call.message)
            
    elif call.data.startswith('seller select stop loss '):
        amount = call.data[24:]
        if (amount == 'x'):
            seller.handle_stop_loss_x(bot, call.message)
        seller.select_stop_loss(bot, call.message, call.data[24:])

    elif call.data.startswith('seller select limit tax '):
        amount = call.data[24:]
        if (amount == 'x'):
            seller.handle_limit_tax_x(bot, call.message)
        seller.select_limit_tax(bot, call.message, call.data[24:])
    elif call.data.startswith('seller select market capital '):
        amount = call.data[29:]
        if (amount == 'x'):
            seller.handle_market_capital_x(bot, call.message)
        seller.select_market_capital(bot, call.message, call.data[29:])
    elif call.data.startswith('seller select liquidity '):
        amount = call.data[24:]
        if (amount == 'x'):
            seller.handle_liquidity_x(bot, call.message)
        seller.select_liquidity(bot, call.message, call.data[24:])

    elif call.data.startswith('seller select interval '):
        amount = call.data[23:]
        if (amount == 'x'):
            seller.handle_interval_x(bot, call.message)
        seller.select_interval(bot, call.message, call.data[23:])
    elif call.data.startswith('seller select duration '):
        amount = call.data[23:]
        if (amount == 'x'):
            seller.handle_duration_x(bot, call.message)
        seller.select_duration(bot, call.message, call.data[23:])
    elif call.data.startswith('seller select max price '):
        amount = call.data[24:]
        if (amount == 'x'):
            seller.handle_max_price_x(bot, call.message)
        seller.select_max_price(bot, call.message, call.data[24:])
    elif call.data.startswith('seller select min price '):
        amount = call.data[24:]
        if (amount == 'x'):
            seller.handle_min_price_x(bot, call.message)
        seller.select_min_price(bot, call.message, call.data[24:])
    elif call.data.startswith('seller select position '):
        amount = call.data[23:]
        seller.select_position(bot, call.message, call.data[23:])
# sniper
    elif call.data.startswith('sniper select buy wallet '):
        sniper.select_buy_wallet(bot, call.message, call.data[25:])

    elif call.data == 'sniper select auto mode':
        sniper.handle_auto_mode(bot, call.message)
    elif call.data == 'sniper select manual mode':
        sniper.handle_manual_mode(bot, call.message) 
    elif call.data == 'make sniper order':
        sniper.handle_set_sniper(bot, call.message)
    elif call.data == 'sniper set auto_sell':
        sniper.handle_auto_sell(bot, call.message)
    elif call.data == 'sniper add auto params':
        sniper.add_auto_param(bot, call.message)
    elif call.data.startswith('sniper select buy amount '):
        amount = call.data[25:]
        if (amount == 'x'):
            sniper.handle_buy_amount_x(bot, call.message)
        else:
            sniper.select_buy_amount(bot, call.message, call.data[25:])
    elif call.data.startswith('sniper select slippage '):
        amount = call.data[23:]
        if (amount == 'x'):
            sniper.handle_slippage_x(bot, call.message)
        else:
            sniper.handle_select_auto_slippage(bot, call.message, call.data[23:])
    elif call.data.startswith('sniper confirm select slippage '):
        sniper.select_slip_page(bot, call.message, call.data[31:])
    elif call.data.startswith('sniper select profit '):
        amount = call.data[21:]
        if (amount == 'x'):
            sniper.handle_profit_x(bot, call.message)
        sniper.select_profit(bot, call.message, call.data[21:])
    elif call.data.startswith('sniper select token count '):
        amount = call.data[26:]
        if (amount == 'x'):
            sniper.handle_token_count_x(bot, call.message)
        sniper.select_token_count(bot, call.message, call.data[26:])
    elif call.data.startswith('sniper select stop-loss '):
        amount = call.data[24:]
        if (amount == 'x'):
            sniper.handle_stop_loss_x(bot, call.message)
    elif call.data.startswith('sniper input market capital '):
        amount = call.data[28:]
        sniper.input_market_cap(bot, call.message, amount)

    elif call.data.startswith('sniper select auto amount '):
        amount = call.data[26:]
        sniper.handle_auto_amount_value(bot, call.message, call.data[26:])
    elif call.data.startswith('sniper select auto price '):
        amount = call.data[25:]
        sniper.handle_auto_price_value(bot, call.message, call.data[25:])
    elif call.data.startswith('sniper remove auto params '):
        amount = call.data[26:]
        sniper.handle_remove_auto_params(bot, call.message, call.data[26:])
    
    elif call.data == 'swing':
        main_swing.handle_start(bot, call.message)
    elif call.data == 'swing mode auto':
        fully_auto.handle_start(bot, call.message)
    elif call.data == 'swing mode manual':
        manual_mode.handle_start(bot, call.message)
    elif call.data.startswith('fully_auto swing select buy amount '):
        amount = call.data[35:]
        if (amount == 'x'):
            fully_auto.handle_buy_amount_x(bot, call.message)
        else:
            fully_auto.select_buy_amount(bot, call.message, call.data[35:])
    elif call.data.startswith('fully_auto swing select buy wallet '):
        fully_auto.select_buy_wallet(bot, call.message, call.data[35:])
    elif call.data == 'start swing auto mode':
        fully_auto.start_trading(bot, call.message)
    elif call.data == 'handle swing auto mode status':
        fully_auto.handle_trading_status(bot, call.message)
    elif call.data == 'swing auto show more wallets':
        fully_auto.handle_more_btn(bot, call.message)
        
    elif call.data == 'swing mode manual':
        manual_mode.handle_start(bot, call.message)
    elif call.data == 'manual swing make buy order':
        manual_mode.handle_buy(bot, call.message)
    elif call.data.startswith('manual swing select buy amount '):
        amount = call.data[31:]
        if (amount == 'x'):
            manual_mode.handle_buy_amount_x(bot, call.message)
        else:
            manual_mode.select_buy_amount(bot, call.message, call.data[31:])
    elif call.data.startswith('manual swing select buy wallet '):
        manual_mode.select_buy_wallet(bot, call.message, call.data[31:])
        
    elif call.data.startswith('manual swing select slippage '):
        amount = call.data[29:]
        if (amount == 'x'):
            manual_mode.handle_slippage_x(bot, call.message)
        else:
            manual_mode.handle_select_auto_slippage(bot, call.message, call.data[23:])
    elif call.data.startswith('manual swing confirm select slippage '):
        manual_mode.select_slip_page(bot, call.message, call.data[43:])
    elif call.data == 'swing manual show more wallets':
        manual_mode.handle_more_btn(bot, call.message)
    elif call.data == 'start swing manual':
        manual_mode.start_trading(bot, call.message)
def initialize():
    print('Starting the bot...')
    bot.infinity_polling(restart_on_change=False)
