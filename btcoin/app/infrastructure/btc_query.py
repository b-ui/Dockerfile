# coding: utf-8
import pymongo

from app.infrastructure.model.chan import ChanKline, Trend, Centre, Fractal, Kline


class Query(object):
    def __init__(self, client, db, code, limit=100):
        self.client = client
        self.db = db
        self.code = code
        self.limit = limit

    def get_original_ks(self, ktype):
        condition = {'windCode': self.code, 'ktype': ktype}
        cur = self.client[self.db].chankline.find(condition).sort('index', pymongo.DESCENDING).limit(self.limit)
        return [Kline(e['kline']) for e in cur]

    def get_chan_ks(self, ktype):
        condition = {'windCode': self.code, 'ktype': ktype}
        cur = self.client[self.db].chankline.find(condition).sort('index', pymongo.DESCENDING).limit(self.limit)
        return [ChanKline(e) for e in cur]

    def get_trends(self, ktype, level):
        condition = {'windCode': self.code, 'ktype': ktype, 'level': level}
        cur = self.client[self.db].trend.find(condition).sort('index', pymongo.DESCENDING).limit(self.limit)
        return [Trend(e) for e in cur]

    def get_fractals(self, ktype):
        condition = {'windCode': self.code, 'ktype': ktype}
        cur = self.client[self.db].fractal.find(condition).sort('index', pymongo.DESCENDING).limit(self.limit)
        return [Fractal(e) for e in cur]

    def get_centres(self, ktype, level):
        condition = {'windCode': self.code, 'ktype': ktype, 'level': level}
        cur = self.client[self.db].centre.find(condition).sort('index', pymongo.DESCENDING).limit(self.limit)
        return [Centre(e) for e in cur]


class ChanQuery(Query):
    def __init__(self, client, db, code, limit=100):
        super(ChanQuery, self).__init__(client, db, code, limit)

    def original_k(self, location, ktype):
        abs_location = abs(location)
        original_k_list = self.get_original_ks(ktype)
        res = original_k_list[abs_location - 1] if len(original_k_list) >= abs_location else None
        return res

    def chan_k(self, location, ktype):
        abs_location = abs(location)
        chan_k_list = self.get_chan_ks(ktype)
        res = chan_k_list[abs_location - 1] if len(chan_k_list) >= abs_location else None
        return res

    def chan_k_from(self, ktype, level, date):
        condition = {'windCode': self.code, 'ktype': ktype, 'level': level, 'datetime': {'$gte': date}}
        cur = self.client[self.db].chankline.find(condition).sort('index', pymongo.ASCENDING)
        return [ChanKline(e) for e in cur]

    def trend(self, location, ktype, level):
        abs_location = abs(location)
        trend_list = self.get_trends(ktype, level)
        res = trend_list[abs_location - 1] if len(trend_list) >= abs_location else None
        return res

    def trend_from(self, ktype, level, date):
        condition = {'windCode': self.code, 'ktype': ktype, 'level': level, 'start_time': {'$gte': date}}
        cur = self.client[self.db].trend.find(condition).sort('index', pymongo.ASCENDING)
        return [Trend(e) for e in cur]

    def fractal(self, location, ktype):
        abs_location = abs(location)
        fractal_list = self.get_fractals(ktype)
        res = fractal_list[abs_location - 1] if len(fractal_list) >= abs_location else None
        return res

    def fractal_from(self, ktype, level, date):
        condition = {'windCode': self.code, 'ktype': ktype, 'level': level, 'eigen_chan_kline_datetime': {'$gte': date}}
        cur = self.client[self.db].fractal.find(condition).sort('index', pymongo.ASCENDING)
        return [Fractal(e) for e in cur]

    def centre(self, location, ktype, level):
        abs_location = abs(location)
        centre_list = self.get_centres(ktype, level)
        res = centre_list[abs_location - 1] if len(centre_list) >= abs_location else None
        return res

    def bi(self, location, ktype):
        return self.trend(location, ktype, '-1')

    def duan(self, location, ktype):
        return self.trend(location, ktype, '0')

    def level1(self, location, ktype):
        return self.trend(location, ktype, '1')

    def level2(self, location, ktype):
        return self.trend(location, ktype, '2')

    def bi_from(self, ktype, date):
        return self.trend_from(ktype, '-1', date)

    def duan_from(self, ktype, date):
        return self.trend_from(ktype, '0', date)

    def level1_from(self, ktype, date):
        return self.trend_from(ktype, '1', date)
