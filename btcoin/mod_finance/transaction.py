from copy import copy
from datetime import datetime

from common.time_util import TZ_SH
from database import client


class Transaction(object):
    def __init__(self, symbol, order_id, trade_type, price, amount, timestamp=None):
        self.symbol = symbol
        self.order_id = order_id
        self.type = trade_type
        self.price = price
        self.amount = int(amount * 100) / 100 if amount else None
        self.timestamp = timestamp or int(datetime.now(tz=TZ_SH).timestamp()) * 1000
        self.date = self._convert_time()

    def __getitem__(self, name):
        return self.__dict__[name]

    def _convert_time(self):
        return datetime.fromtimestamp(self.timestamp / 1000, tz=TZ_SH).replace(tzinfo=None)

    def to_dict(self):
        return copy(self.__dict__)


def create_transaction(symbol, order_id, trade_type, price=None, amount=None):
    transaction = Transaction(
        symbol=symbol,
        order_id=order_id,
        trade_type=trade_type,
        price=price,
        amount=amount
    )
    client.btcoin.transaction.insert(transaction.to_dict())
    return transaction
