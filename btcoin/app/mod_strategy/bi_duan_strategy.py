# coding: utf-8
from app.common.chan import chan_min
from app.common.log_util import logger
from app.mod_strategy.base import Strategy
from config import btc_query, btc_trader

account = {
    'name': 'long',
    'cny': 1000,
    'btc': 1,
    'state': 0,
    'price': 0,
    'borrow': 0
}


class bi_duan(Strategy):
    """笔段策略v1.0"""

    def __init__(self, chan_query):
        super(bi_duan, self).__init__(chan_query)

    def buy(self):
        try:
            last_duan = btc_query.duan(-1, '1_1')
            last_bi = btc_query.bi(-1, '1_1')
            bis = btc_query.bi_from('1_1', last_duan.end_time)
        except:
            logger.info('database error')
            return
        # 未解决增量切割，增加额外保护
        if not last_duan or not last_bi:
            return
        minimal = chan_min(bis[:-1], 'low')
        if self.should_buy(last_duan, last_bi, minimal):
            btc_trader.simu_buy_market(account)
            account['price'] = last_bi.low
            account['state'] = 1

    def sell(self):
        try:
            last_duan = btc_query.duan(-1, '1_1')
            last_bi = btc_query.bi(-1, '1_1')
            bis = btc_query.bi_from('1_1', last_duan.end_time)
        except:
            logger.info('database error')
            return
        if not last_duan or not last_bi:
            return
        if self.should_sell(last_bi):
            btc_trader.simu_sell_market(account)

    def cut(self):
        if self.should_cut():
            btc_trader.simu_sell_market(account)
            account['state'] = 0
            account['price'] = 0

    def should_cut(self):
        return account['state'] == 1 and self.is_ticker_sell_lt(account['price'])

    def should_sell(self, bi):
        return bi.is_direction_up() and bi.is_fractal_gte(4)

    def should_buy(self, duan, bi, minimal):
        return duan.is_direction_up() and bi.is_direction_down() and bi.is_fractal_gte(4) \
               and bi.low < minimal and self.is_ticker_sell_gt(bi.low)

    @staticmethod
    def is_ticker_sell_gt(price):
        return float(btc_trader.ticker()['sell']) > price

    @staticmethod
    def is_ticker_sell_lt(price):
        return float(btc_trader.ticker()['sell']) < price
