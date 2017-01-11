from common.log_util import logger
from mod_btcoin.interface.okcoin.OkcoinSpotAPI import OKCoinSpot
from mod_finance.transaction import create_transaction


class Trader(object):
    OKCOIN_HOST = 'www.okcoin.cn'

    def __init__(self, symbol, api_key, secret_key):
        self.symbol = symbol
        self.okcoin_spot = OKCoinSpot(self.OKCOIN_HOST, api_key, secret_key)

    def buy(self, price='', amount=''):
        res = self.okcoin_spot.trade(self.symbol, 'buy', price, amount)
        order_id = res.get('order_id')
        create_transaction(self.symbol, order_id, 'buy', price, amount)
        return order_id

    def sell(self, price='', amount=''):
        res = self.okcoin_spot.trade(self.symbol, 'sell', price, amount)
        order_id = res.get('order_id')
        create_transaction(self.symbol, order_id, 'sell', price, amount)
        return order_id

    def buy_market(self, price):
        res = self.okcoin_spot.trade(self.symbol, 'buy_market', price)
        order_id = res.get('order_id')
        create_transaction(self.symbol, order_id, 'buy_market', price=price)
        return order_id

    def sell_market(self, amount):
        res = self.okcoin_spot.trade(self.symbol, 'sell_market', amount)
        order_id = res.get('order_id')
        create_transaction(self.symbol, order_id, 'sell_market', amount=amount)
        return order_id

    def cancel_order(self, order_id):
        if not order_id:
            logger.error('order_id cannot be empty')
            return
        self.okcoin_spot.cancelOrder(self.symbol, order_id)

    def order_info(self, order_id):
        if not order_id:
            logger.error('order_id cannot be empty')
            return
        res = self.okcoin_spot.orderinfo(self.symbol, order_id)
        return res['orders'][0] if res['result'] else None
