import os
from datetime import datetime

import pymongo
from apscheduler.schedulers.background import BlockingScheduler
from pymongo.errors import DuplicateKeyError
from pytz import utc

from database import client
from interface.okcoin.OkcoinSpotAPI import OKCoinSpot
from model.btcoin import BTCoin
from model.btcoin import TZ_SH

api_key = os.environ.get('API_KEY')
secret_key = os.environ.get('SECRET_KEY')
okcoin_host = 'www.okcoin.cn'

okcoin_spot = OKCoinSpot(okcoin_host, api_key, secret_key)

scheduler = BlockingScheduler()
scheduler.configure(timezone=utc)


@scheduler.scheduled_job('interval', seconds=10, args=['1_1'])
def get_okcoin_kline(k_type):
    last = client.btcoin.SH_OKCOIN.find().sort('date', pymongo.DESCENDING).limit(1)
    if last.count():
        since = int(TZ_SH.localize(last[0]['date']).timestamp() * 1000)
    else:
        since = None
    print(datetime.fromtimestamp(since / 1000))
    klines = okcoin_spot.kline(k_type=k_type, since=since)
    for e in klines[:-1]:
        btc = BTCoin(k_type, *e)
        try:
            client.btcoin.SH_OKCOIN.insert(btc.to_document())
        except DuplicateKeyError:
            pass
