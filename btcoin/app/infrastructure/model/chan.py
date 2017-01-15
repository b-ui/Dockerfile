# coding:utf-8
from bson.json_util import dumps
from database import client


class Base(object):
    def __init__(self, document):
        self._document = document
        if document is None:
            raise ValueError('document should not be None')

    def __str__(self):
        return dumps(self._document, indent=4, sort_keys=True)

    def __getitem__(self, item):
        return self.__dict__[item]


class Kline(Base):
    def __init__(self, document):
        """
        :type document: dict
        """
        super(Kline, self).__init__(document)
        self._id = document['_id']
        self.refillFlag = document['refillFlag']
        self.volume = document['volume']
        self.code = document['code']
        self.name = document['name']
        self.open = document['open']
        self.transNum = document['transNum']
        self.high = document['high']
        self.amount = document['amount']
        self.low = document['low']
        self.cycDef = document['cycDef']
        self.close = document['close']
        self.datetime = document['date']
        self.windCode = document['windCode']
        self.cycType = document['cycType']
        self.market = document['market']


class ChanKline(Base):
    def __init__(self, document):
        """
        :type document: dict
        """
        super(ChanKline, self).__init__(document)
        self._id = document['_id']
        self.index = document['index']
        self.chan_index = document['chan_index']
        self.datetime = document['datetime']
        self.ktype = document['ktype']
        self.windCode = document['windCode']
        self.kline = Kline(document['kline'])
        self.inclusive = document['inclusive']
        """
        - Non Inclusive: 0
        - Up Inclusive: 1
        - Down Inclusive: -1
        """
        self.direction = document['direction']
        """
        - Up: 1
        - Down: -1
        """
        self.shaped_high = document['shaped_high']
        self.shaped_low = document['shaped_low']
        self.has_gap = document['has_gap']
        self.chankline_flag = document['chankline_flag']
        if document['trend_owner_dict'] is None: document['trend_owner_dict'] = {}
        self.trend_owner_dict = document['trend_owner_dict']

    def __sub__(self, other):
        if isinstance(other, ChanKline):
            return self.index - other.index
        else:
            return self.index - other.chan_k_index


class Fractal(Base):
    def __init__(self, document):
        """
        :type document: dict
        """
        super(Fractal, self).__init__(document)
        self._id = document['_id']
        self.index = document['index']
        self.ktype = document['ktype']
        self.windCode = document['windCode']
        self.fractal_flag = document['fractal_flag']
        self.chan_kline_index_list = document['chan_kline_index_list']
        self.eigen_chan_kline_index = document['eigen_chan_kline_index']
        self.fractal_interval = document['fractal_interval']
        condition = {'windCode': self.windCode, 'ktype': self.ktype, 'index': self.eigen_chan_kline_index}
        # new properties
        self.datetime = client.chan.chankline.find(condition).limit(1)[0]['datetime']


class Trend(Base):
    def __init__(self, document):
        """
        :type document: dict
        """
        super(Trend, self).__init__(document)
        self._id = document['_id']
        self.index = document['index']
        self.ktype = document['ktype']
        self.windCode = document['windCode']
        self.level = document['level']
        self.type = document['type']
        """
        - TREND_TYPE_1_1 = 1
        - TREND_TYPE_1_2 = 2
        - TREND_TYPE_1_3 = 3
        - TREND_TYPE_2_1_front = 4
        - TREND_TYPE_2_1_back = 5
        - TREND_TYPE_2_2_front = 6
        - TREND_TYPE_2_2_back = 7
        - TREND_TYPE_2_3 = 8
        - TREND_TYPE_2_4 = 9
        """
        self.direction = document['direction']
        """
        - Up: 1
        - Down: -1
        """
        self.flag = document['flag']
        self.inclusive = document['inclusive']
        """
        - Non Inclusive: 0
        - Up Inclusive: 1
        - Down Inclusive: -1
        - Up Reverse Inclusive: 2
        - Down Reverse Inclusive: -2
        """
        self.high = document['high']
        self.low = document['low']
        self.shaped_high = document['shaped_high']
        self.shaped_low = document['shaped_low']
        self.has_gap = document['has_gap']
        self.left_subtrend_index = document['left_subtrend_index']
        self.eigen_subtrend_index = document['eigen_subtrend_index']
        self.right_subtrend_index = document['right_subtrend_index']
        self.chankline_index_list = document['chankline_index_list']
        self.fractal_index_list = document['fractal_index_list']
        if document['subtrend_index_dict'] is None: document['subtrend_index_dict'] = {}
        self.subtrend_index_dict = document['subtrend_index_dict']
        if document['centre_index_dict'] is None: document['centre_index_dict'] = {}
        self.centre_index_dict = document['centre_index_dict']
        self.start_time = document['start_time']
        self.end_time = document['end_time']
        # new properties
        # if self.direction == 1:
        #     self.ratio = (self.high - self.low) / float(self.low)
        # else:
        #     self.ratio = (self.high - self.low) / float(self.high)
        self.count_kline = len(self.chankline_index_list)
        self.count_fractal = len(self.fractal_index_list)
        # count_subtrend todo:
        self.count_subtrend = len(self.subtrend_index_dict.get('-1', []))
        self.ratio = (self.shaped_high - self.shaped_low) / self.count_kline
        self.start_chan_k = self.chankline_index_list[0]
        self.end_chan_k = self.chankline_index_list[-1]

    @property
    def chan_k_index(self):
        return self.chankline_index_list[-1]


class Centre(Base):
    def __init__(self, document):
        """
        :type document: dict
        """
        super(Centre, self).__init__(document)
        self._id = document['_id']
        self.index = document['index']
        self.ktype = document['ktype']
        self.windCode = document['windCode']
        self.level = document['level']
        self.type = document['type']
        """
        - CENTRE_TYPE_STANDARD: 0
        - CENTRE_TYPE_SIMILAR: 1
        - CENTRE_TYPE_FAKE: 2
        """
        self.direction = document['direction']
        self.zg_index = document['zg_index']
        self.zd_index = document['zd_index']
        self.gg_index = document['gg_index']
        self.dd_index = document['dd_index']
        self.zn_index_list = document['zn_index_list']
        self.owner_trend_index = document['owner_trend_index']
        self.zg = document['zg']
        self.zd = document['zd']
        self.gg = document['gg']
        self.dd = document['dd']
        self.start_time = document['start_time']
        self.end_time = document['end_time']
        self.trend_num = document['trend_num']
