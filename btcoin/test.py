import os

from app.mod_btcoin.interface.okcoin.OkcoinSpotAPI import OKCoinSpot
from app.mod_finance.trader import OKCoinTrader

api_key = os.environ.get('API_KEY')
secret_key = os.environ.get('SECRET_KEY')
okcoin_host = 'www.okcoin.cn'
okcoin_spot = OKCoinSpot(okcoin_host, api_key, secret_key)

btc_trader = OKCoinTrader('btc_cny', api_key, secret_key)

order_id = btc_trader.buy(100, 0)
btc_trader.cancel_order(order_id)
print(btc_trader.order_info(order_id))
