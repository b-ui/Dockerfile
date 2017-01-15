import os
from datetime import datetime

import pymongo
from apscheduler.schedulers.background import BlockingScheduler
from mod_btcoin.interface.okcoin.OkcoinSpotAPI import OKCoinSpot
from pymongo.errors import DuplicateKeyError
from pytz import utc

from app.mod_btcoin.model.btcoin import BTCoin
from app.mod_btcoin.model.btcoin import TZ_SH
from database import client

api_key = os.environ.get('API_KEY')
secret_key = os.environ.get('SECRET_KEY')
okcoin_host = 'www.okcoin.cn'

okcoin_spot = OKCoinSpot(okcoin_host, api_key, secret_key)

scheduler = BlockingScheduler()
scheduler.configure(timezone=utc)


def get_last_document(k_type):
    cyc_type = k_type.split('_')[0]
    cyc_def = k_type.split('_')[-1]
    _filter = {'cycType': int(cyc_type), 'cycDef': int(cyc_def)}
    return client.btcoin.SH_OKCOIN.find(_filter).sort('date', pymongo.DESCENDING).limit(1)


def get_okcoin_kline(k_type):
    last = get_last_document(k_type)
    if last.count():
        since = int(TZ_SH.localize(last[0]['date']).timestamp() * 1000)
    else:
        since = int(TZ_SH.localize(datetime(2016, 1, 1)).timestamp() * 1000)
    print(datetime.fromtimestamp(since / 1000))
    klines = okcoin_spot.kline(k_type=k_type, since=since)
    for e in klines:
        btc = BTCoin(k_type, *e)
        try:
            client.btcoin.SH_OKCOIN.update(btc.index, {'$set': btc.to_document()}, upsert=True)
        except DuplicateKeyError:
            pass


@scheduler.scheduled_job('interval', seconds=10, args=['1_1'])
def get_okcoin_kline_1_1(k_type):
    get_okcoin_kline(k_type)


@scheduler.scheduled_job('interval', seconds=10, args=['1_3'])
def get_okcoin_kline_1_3(k_type):
    get_okcoin_kline(k_type)


@scheduler.scheduled_job('interval', seconds=10, args=['1_5'])
def get_okcoin_kline_1_5(k_type):
    get_okcoin_kline(k_type)


@scheduler.scheduled_job('interval', seconds=10, args=['1_15'])
def get_okcoin_kline_1_15(k_type):
    get_okcoin_kline(k_type)


@scheduler.scheduled_job('interval', seconds=10, args=['1_30'])
def get_okcoin_kline_1_30(k_type):
    get_okcoin_kline(k_type)


@scheduler.scheduled_job('interval', seconds=10, args=['1_60'])
def get_okcoin_kline_1_60(k_type):
    get_okcoin_kline(k_type)


@scheduler.scheduled_job('interval', seconds=10, args=['1_120'])
def get_okcoin_kline_1_120(k_type):
    get_okcoin_kline(k_type)


@scheduler.scheduled_job('interval', seconds=10, args=['1_240'])
def get_okcoin_kline_1_240(k_type):
    get_okcoin_kline(k_type)


@scheduler.scheduled_job('interval', seconds=10, args=['1_360'])
def get_okcoin_kline_1_480(k_type):
    get_okcoin_kline(k_type)


@scheduler.scheduled_job('interval', seconds=10, args=['1_720'])
def get_okcoin_kline_1_720(k_type):
    get_okcoin_kline(k_type)


@scheduler.scheduled_job('interval', seconds=10, args=['2_1'])
def get_okcoin_kline_2_1(k_type):
    get_okcoin_kline(k_type)


@scheduler.scheduled_job('interval', seconds=10, args=['2_3'])
def get_okcoin_kline_2_3(k_type):
    get_okcoin_kline(k_type)


@scheduler.scheduled_job('interval', seconds=10, args=['3_1'])
def get_okcoin_kline_3_1(k_type):
    get_okcoin_kline(k_type)
