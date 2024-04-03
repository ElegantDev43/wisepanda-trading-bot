# wisepanda-trading-bot

Done:
- Import Wallet
- Sniping Bot Configuration as well as Figma Design
- Integrate PostgreSQL to manage users and save settings
- Toggle activation of Sniper Bot on Telegram
- Implement Multi-threading for users' sniper bots
- Implement initially the logic of auto-buy, auto-sell and stop-loss
- Initially build the layer of interacting with MarketRouter ABI on Sepolia testnet
  * Implement order feature using marketBid function of the contract (smart contract error when transaction is sent)

Telegram Bot: [@wisepandatradingbot](https://t.me/wisepandatradingbot)

### Create a Virtual Environment

```shell script
python -m venv venv
```

### Activate the Virtual Environment

On Windows:
```shell script
venv\Scripts\activate
```

On MacOS and Linux:
```shell script
source venv/bin/activate
```

### Install Packages

```shell script
pip install -r requirements.txt
```

### Start Application

```shell script
python app.py
```