import os
from datetime import datetime

import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from interface.okcoin.OkcoinSpotAPI import OKCoinSpot
from model.btcoin import BTCoin

host = os.environ.get('MONGO_DB_ADDR') or '192.168.1.103'
port = os.environ.get('MONGO_DB_PORT') or 27017

client = MongoClient(host, int(port))

api_key = os.environ.get('API_KEY')
secret_key = os.environ.get('SECRET_KEY')
okcoin_host = 'www.okcoin.cn'

okcoin_spot = OKCoinSpot(okcoin_host, api_key, secret_key)

last = client.btcoin.SH_OKCOIN.find().sort('date', pymongo.DESCENDING).limit(1)
if last.count():
    since = int(last[0]['date'].timestamp() * 1000)
else:
    since = int(datetime(2014, 1, 1).timestamp() * 1000)

klines = okcoin_spot.kline(k_type='1_1', since=since)
print(since)
print(datetime.fromtimestamp(since / 1000))
for e in klines[:-1]:
    btc = BTCoin('1_1', *e)
    try:
        client.btcoin.SH_OKCOIN.insert(btc.to_document())
    except DuplicateKeyError:
        pass
print(len(klines))

# print(okcoin_spot.trade('btc_cny', 'buy_market', 100))

# print(okcoin_spot.batchTrade('btc_cny', 'sell', '[{price:7488,amount:0.01}]'))

# print(okcoin_spot.orderinfo('btc_cny', 7733509037))
