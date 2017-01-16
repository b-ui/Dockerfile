# coding:utf-8
# 笔段策略的做空
import os

from app.common.log_util import logger

from app.common.chan import chan_min, chan_max
from app.infrastructure.chan_query import ChanQuery
from app.mod_finance.trader import OKCoinTrader
from database import client

api_key = os.environ.get('API_KEY')
secret_key = os.environ.get('SECRET_KEY')

btc_query = ChanQuery(client, 'btc_chan', 'OKCOIN.SH')
btc_trader = OKCoinTrader('btc_cny', api_key, secret_key)

account = {
    'name': 'short',
    'cny': 1000,
    'btc': 0,
    'state': 0,
    'price': 0,
    'borrow': 0
}


def bi_duan_zk_buy_1_1():
    try:
        last_duan = btc_query.duan(-1, '1_1')
        last_bi = btc_query.bi(-1, '1_1')
        bi_s = btc_query.bi_from('1_1', last_duan.end_time)
    except:
        logger.debug('database error')
        return
    if not last_duan or not last_bi:
        return
    minimal = chan_min(bi_s[:-1], 'low')
    logger.info('last_bi.low:{}, minimal:{}'.format(last_bi.low, minimal))
    if account['state'] == 1 and last_bi.direction == -1 and len(last_bi.fractal_index_list) >= 4:
        btc_trader.simu_buy_market_kong(account, 1)
        account['state'] = 0
        print(account)

    ticker = btc_trader.ticker()
    if account['state'] == 1 and float(ticker['buy']) > account['price']:
        btc_trader.simu_buy_market_kong(account, 1)
        account['state'] = 0
        print(account)


def bi_duan_zk_sell_1_1():
    try:
        last_duan = btc_query.duan(-1, '1_1')
        last_bi = btc_query.bi(-1, '1_1')
        bi_s = btc_query.bi_from('1_1', last_duan.end_time)
    except:
        logger.debug('database error')
        return
    if not last_duan or not last_bi:
        return
    maximal = chan_max(bi_s[:-1], 'high')
    logger.info('last_bi.fractals: {}'.format(last_bi.fractal_index_list))
    if last_duan.direction == -1 and last_bi.direction == 1 and len(
            last_bi.fractal_index_list) >= 4 and last_bi.high > maximal and float(btc_trader.ticker()['buy']) < last_bi.high:
        if account['state'] == 0:
            account['btc'] += 1
            account['borrow'] += 1
            account['price'] = last_bi.high
            account['state'] = 1
            btc_trader.simu_sell_market(account)
            print(account)
