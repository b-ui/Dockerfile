# coding:utf-8
from datetime import datetime

from app.common.time_util import TZ_SH


class BTCoin:
    def __init__(self, k_type, *args):
        self.cycType = int(k_type.split('_')[0])
        self.cycDef = int(k_type.split('_')[1])
        self.timestamp = args[0]
        self.date = self._convert_time()
        self.open = args[1]
        self.high = args[2]
        self.low = args[3]
        self.close = args[4]
        self.volume = args[5]
        self.amount = None
        self.name = u'比特币'
        self.code = 'OKCOIN'
        self.windCode = 'OKCOIN.SH'
        self.market = 'OKCOIN'
        self.refillFlag = None
        self.transNum = None

    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.date, self.open, self.high, self.low, self.close, self.volume)

    def _convert_time(self):
        return datetime.fromtimestamp(self.timestamp / 1000, tz=TZ_SH).replace(tzinfo=None)

    def to_document(self):
        return self.__dict__

    @property
    def index(self):
        return {'cycType': self.cycType, 'cycDef': self.cycDef, 'date': self.date}
