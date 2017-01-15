import os

from app.common.log_util import logger

from app.common.chan import chan_max, chan_min
from app.infrastructure.btc_query import SingleQuery
from app.mod_finance.trader import OKCoinTrader
from database import client

api_key = os.environ.get('API_KEY')
secret_key = os.environ.get('SECRET_KEY')

btc_query = SingleQuery(client, 'btc_chan', 'OKCOIN.SH')
btc_trader = OKCoinTrader('btc_cny', api_key, secret_key)

account = {
    'name': 'long',
    'cny': 1000,
    'btc': 1,
    'state': 0,
    'price': 0,
    'borrow': 0
}


def bi_duan_buy():
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


def bi_duan_sell():
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
