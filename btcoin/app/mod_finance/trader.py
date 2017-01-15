import uuid

from app.common.log_util import logger
from app.mod_btcoin.interface.okcoin.OkcoinSpotAPI import OKCoinSpot
from app.mod_finance.transaction import create_transaction


class OKCoinTrader(object):
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

    def ticker(self):
        res = self.okcoin_spot.ticker(self.symbol)
        return res['ticker']

    def simu_buy_market(self, account):
        ticker = self.ticker()
        sell_1 = float(ticker['sell'])
        amount = int(account['cny'] / sell_1 * 100) / 100
        if account['cny'] < sell_1 / 100:
            return
        order_id = str(uuid.uuid4())
        create_transaction(self.symbol, order_id, 'simu_buy_market', price=account['cny'], amount=amount,
                           avg_price=ticker['sell'])
        account['btc'] += amount
        account['cny'] -= sell_1 * amount

    def simu_buy_market_kong(self, account, amount):
        ticker = self.ticker()
        sell_1 = float(ticker['sell'])
        if account['cny'] < sell_1 * amount:
            logger.error('not enough free_cny to buy {} btc'.format(amount))
            return
        order_id = str(uuid.uuid4())
        create_transaction(self.symbol, order_id, 'simu_buy_market_kong', price=sell_1 * amount, amount=amount,
                           avg_price=ticker['sell'], account=account)
        account['btc'] = 0
        account['cny'] -= sell_1 * amount
        account['borrow'] = 0

    def simu_sell_market(self, account):
        ticker = self.ticker()
        if account['btc'] <= 0:
            return
        buy_1 = float(ticker['buy'])
        price = account['btc'] * buy_1
        order_id = str(uuid.uuid4())
        create_transaction(self.symbol, order_id, 'simu_sell_market', price=price, amount=account['btc'],
                           avg_price=ticker['buy'], account=account)
        account['btc'] -= account['btc']
        account['cny'] += price
