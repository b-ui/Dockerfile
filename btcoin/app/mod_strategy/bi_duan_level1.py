# coding: utf-8
# 增加条件：
# 1. 买入点就是第3或4个1分钟k线内，离特征k线距离<=2
# 2. 考虑中继分型在一笔中分布，一笔中的下半部分有反向的中继分型(顶分型) >=1
# 3. 卖，一笔的后半部分出现底分型， >=1
# 4. 最后一个level1是1，最后一个段的低点，是level1结束时间以来的新低，其他同笔段；


import os

from app.common.log_util import logger

from app.common.chan import chan_max, chan_min
from app.infrastructure.chan_query import ChanQuery
from app.mod_finance.trader import OKCoinTrader
from database import client

api_key = os.environ.get('API_KEY')
secret_key = os.environ.get('SECRET_KEY')

btc_query = ChanQuery(client, 'btc_chan', 'OKCOIN.SH')
btc_trader = OKCoinTrader('btc_cny', api_key, secret_key)

account = {
    'name': 'long',
    'cny': 1000,
    'btc': 1,
    'state': 0,
    'price': 0,
    'borrow': 0
}


def bi_duan_buy_1_1():
    try:
        last_duan = btc_query.duan(-1, '1_1')
        last_bi = btc_query.bi(-1, '1_1')
        bi_s = btc_query.bi_from('1_1', last_duan.end_time)
    except:
        logger.info('database error')
        return
    if not last_duan or not last_bi:
        return
    minimal = chan_min(bi_s[:-1], 'low')
    logger.info('last_bi.low:{}, minimal:{}'.format(last_bi.low, minimal))
    if last_duan.direction == 1 and last_bi.direction == -1 and len(
            last_bi.fractal_index_list) >= 4 and last_bi.low < minimal and float(btc_trader.ticker()['sell']) > last_bi.low:
        btc_trader.simu_buy_market(account)
        account['price'] = last_bi.low
        account['state'] = 1


def bi_duan_sell_1_1():
    try:
        last_duan = btc_query.duan(-1, '1_1')
        last_bi = btc_query.bi(-1, '1_1')
        bi_s = btc_query.bi_from('1_1', last_duan.end_time)
    except:
        logger.info('database error')
        return
    if not last_duan or not last_bi:
        return
    maximal = chan_max(bi_s[:-1], 'high')
    logger.info('last_bi.high:{}, max:{}'.format(last_bi.high, maximal))
    if last_bi.direction == 1 and len(last_bi.fractal_index_list) >= 4:
        btc_trader.simu_sell_market(account)
    ticker = btc_trader.ticker()
    if account['state'] == 1 and float(ticker['sell']) < account['price']:
        btc_trader.simu_sell_market(account)
        account['state'] = 0
        account['price'] = 0
