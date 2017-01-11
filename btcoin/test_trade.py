import os
import time

from database import client
from infrastructure.btc_query import SingleQuery
from mod_btcoin.interface.okcoin.OkcoinSpotAPI import OKCoinSpot
from mod_finance.trader import Trader

btc_query = SingleQuery(client, 'btc_chan', 'OKCOIN.SH')

api_key = os.environ.get('API_KEY')
secret_key = os.environ.get('SECRET_KEY')
okcoin_host = 'www.okcoin.cn'
okcoin_spot = OKCoinSpot(okcoin_host, api_key, secret_key)

btc_trader = Trader('btc_cny', api_key, secret_key)


def chan_min(objs, key):
    return min([getattr(e, key) for e in objs])


def chan_max(objs, key):
    return max([getattr(e, key) for e in objs])


balance = 10000.0
coin = 0

while True:
    try:
        time.sleep(1)
        last_duan = btc_query.duan(-1, '1_1')
        last_bi = btc_query.bi(-1, '1_1')
        bi_s = btc_query.bi_from('1_1', last_duan.end_time)
        minimal = chan_min(bi_s[:-1], 'low')
        maximal = chan_max(bi_s[:-1], 'high')
        if len(bi_s) < 3:
            continue
        if last_duan.direction == 1 and last_bi.direction == -1 and last_bi.low < minimal:
            print('buy')
            btc_trader.buy(100, 1)
        if last_duan.direction == -1 and last_bi.direction == 1 and last_bi.high > maximal:
            print('sell')
            btc_trader.buy(200, 1)
    except Exception as e:
        pass
