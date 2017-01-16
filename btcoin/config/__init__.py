# coding: UTF-8
import os

from app.infrastructure.chan_query import ChanQuery
from app.mod_finance.trader import OKCoinTrader
from config.feature_toggle import feature_with
from database import client

basedir = os.path.abspath(os.path.dirname(__file__))

api_key = os.environ.get('API_KEY')
secret_key = os.environ.get('SECRET_KEY')

btc_query = ChanQuery(client, 'btc_chan', 'OKCOIN.SH')
btc_trader = OKCoinTrader('btc_cny', api_key, secret_key)


class ApschedulerConfig(object):
    JOBS = []

    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 1
    }

    SCHEDULER_API_ENABLED = True
    SCHEDULER_VIEWS_ENABLED = True


def load_apscheduler_config():
    return ApschedulerConfig()


@feature_with('sentry')
def init_sentry(app):
    from raven.contrib.flask import Sentry
    _dsn = os.environ.get('SENTRY_DSN')
    Sentry(app, dsn=_dsn)
