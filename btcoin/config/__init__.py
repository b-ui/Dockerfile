# coding: UTF-8
import os

from config.config import DevelopmentMysqlConfig, DevelopmentSqliteConfig, DevelopmentSqliteMemoryConfig
from config.config import TestingConfig, ProductionConfig, DevelopmentSqliteConfig
from config.feature_toggle import feature_with

basedir = os.path.abspath(os.path.dirname(__file__))

config = {
    'development_mysql': DevelopmentMysqlConfig,
    'development_sqlite': DevelopmentSqliteConfig,
    'development_memory': DevelopmentSqliteMemoryConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentSqliteConfig
}


def load_config():
    """Load config."""
    mode = os.environ.get('MODE')
    print("mode: " + str(mode))

    try:
        if mode == 'PRODUCTION':
            return 'production'
        elif mode == 'TESTING':
            return 'testing'
        elif mode == 'DEV_MYSQL':
            return 'development_mysql'
        elif mode == 'DEV_SQLITE':
            return 'development_sqlite'
        elif mode == 'DEV_MEM':
            return 'development_memory'
        else:
            return 'default'

    except ImportError:
        return 'default'


def load_db_config():
    return config[load_config()]


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
