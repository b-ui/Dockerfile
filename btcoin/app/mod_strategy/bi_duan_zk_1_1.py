# coding:utf-8
# 和做多相反
# 增加条件：
# 1. 融币做空点就是第3或4个1分钟k线内，即离特征k线距离<=2
# 2. 考虑中继分型在一笔中分布，最后一笔的下半部分有反向的中继分型(底分型) >=1
# 3. 买币还币，最后一笔的后半部分出现顶分型， >=1；顶分型必须属于这个笔
# 4. 最后一个比中枢的重心，判断中枢到当下的位置，zg zd的平均值，在未完成段的位置

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
        # 买入判断分型位置
        bi_mid_price = (last_bi.high - last_bi.low) / 2
        last_2nd_frac = btc_query.fractal(-2, '1_1')
        eigen_chan_k = btc_query.get_chan_k('1_1', last_2nd_frac.eigen_chan_kline_index)
        if last_2nd_frac.fractal_flag > 0 and eigen_chan_k.kline.low < bi_mid_price \
            and eigen_chan_k.index < last_bi.end_chan_k:
            btc_trader.simu_buy_market_kong(account, 1)
            account['state'] = 0

    ticker = btc_trader.ticker()
    if account['state'] == 1 and float(ticker['buy']) > account['price']:
        btc_trader.simu_buy_market_kong(account, 1)
        account['state'] = 0


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
            # 当前距离特征K线的距离<=2
            last_chan_k = btc_query.chan_k(-1, '1_1')
            if last_chan_k.index - last_bi.end_chan_k <= 2:
                # 最后一笔的倒数第二个分型是底分型
                bi_mid_price = (last_bi.high - last_bi.low) / 2
                last_2nd_frac = btc_query.fractal(-2, '1_1')
                eigen_chan_k = btc_query.get_chan_k('1_1', last_2nd_frac.eigen_chan_kline_index)
                if last_2nd_frac.fractal_flag < 0 and eigen_chan_k.kline.high > bi_mid_price:
                    account['btc'] += 1
                    account['borrow'] += 1
                    account['price'] = last_bi.high
                    account['state'] = 1
                    btc_trader.simu_sell_market(account)
