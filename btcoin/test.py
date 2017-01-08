import os
from datetime import datetime

import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from interface.okcoin.OkcoinSpotAPI import OKCoinSpot
from model.btcoin import BTCoin
from model.btcoin import TZ_SH

host = os.environ.get('MONGO_DB_ADDR') or '172.17.0.3'
port = os.environ.get('MONGO_DB_PORT') or 27017

client = MongoClient(host, int(port))

api_key = os.environ.get('API_KEY')
secret_key = os.environ.get('SECRET_KEY')
okcoin_host = 'www.okcoin.cn'
okcoin_spot = OKCoinSpot(okcoin_host, api_key, secret_key)

k_type = '1_360'


def get_last_document(k_type):
    cyc_type = k_type.split('_')[0]
    cyc_def = k_type.split('_')[-1]
    _filter = {'cycType': int(cyc_type), 'cycDef': int(cyc_def)}
    print(_filter)
    return client.btcoin.SH_OKCOIN.find(_filter).sort('date', pymongo.DESCENDING).limit(1)


last = get_last_document(k_type)
print(last.count())
if last.count():
    since = int(TZ_SH.localize(last[0]['date']).timestamp() * 1000)
else:
    since = int(TZ_SH.localize(datetime(2016, 1, 1)).timestamp() * 1000)

klines = okcoin_spot.kline(k_type=k_type, since=since)
print(since)
print(datetime.fromtimestamp(since / 1000))
for e in klines:
    btc = BTCoin(k_type, *e)
    print(btc.date)
    try:
        client.btcoin.SH_OKCOIN.update(btc.index, {'$set': btc.to_document()}, upsert=True)
    except DuplicateKeyError:
        pass
print(len(klines))

# print(okcoin_spot.trade('btc_cny', 'buy_market', 100))

# print(okcoin_spot.batchTrade('btc_cny', 'sell', '[{price:7488,amount:0.01}]'))

# print(okcoin_spot.orderinfo('btc_cny', 7733509037))
