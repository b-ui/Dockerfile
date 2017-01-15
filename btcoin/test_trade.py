import os

from app.infrastructure.btc_query import ChanQuery
from app.mod_btcoin.interface.okcoin.OkcoinSpotAPI import OKCoinSpot
from app.mod_finance.trader import OKCoinTrader
from database import client

btc_query = ChanQuery(client, 'btc_chan', 'OKCOIN.SH')

api_key = os.environ.get('API_KEY')
secret_key = os.environ.get('SECRET_KEY')
okcoin_host = 'www.okcoin.cn'
okcoin_spot = OKCoinSpot(okcoin_host, api_key, secret_key)

btc_trader = OKCoinTrader('btc_cny', api_key, secret_key)

