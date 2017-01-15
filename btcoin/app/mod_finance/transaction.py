from copy import copy
from datetime import datetime

from app.common.time_util import TZ_SH
from database import client


class Transaction(object):
    def __init__(self, symbol, order_id, trade_type, price, amount, avg_price, timestamp=None, account=None):
        self.symbol = symbol
        self.order_id = order_id
        self.type = trade_type
        self.price = price
        self.avg_price = avg_price
        self.amount = int(amount * 100) / 100 if amount else None
        self.timestamp = timestamp or int(datetime.now(tz=TZ_SH).timestamp()) * 1000
        self.account = account
        self.date = self._convert_time()

    def __getitem__(self, name):
        return self.__dict__[name]

    def _convert_time(self):
        return datetime.fromtimestamp(self.timestamp / 1000, tz=TZ_SH).replace(tzinfo=None)

    def to_dict(self):
        return copy(self.__dict__)


def create_transaction(symbol, order_id, trade_type, price=None, amount=None, avg_price=None, account=None):
    transaction = Transaction(
        symbol=symbol,
        order_id=order_id,
        trade_type=trade_type,
        price=price,
        amount=amount,
        avg_price=avg_price,
        account=account
    )
    client.btcoin.transaction.insert(transaction.to_dict())
    return transaction
