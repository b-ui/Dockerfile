# -*- coding: utf-8 -*-
import os

import flask

basedir = os.path.abspath(os.path.dirname(__file__))


def load_app_mysql_config():
    mysql_username = os.environ.get('MYSQL_USERNAME')
    mysql_password = os.environ.get('MYSQL_PASSWORD')
    mysql_addr = os.environ.get('MYSQL_PORT_3306_TCP_ADDR')
    mysql_port = os.environ.get('MYSQL_PORT_3306_TCP_PORT')
    mysql_db_name = os.environ.get('MYSQL_INSTANCE_NAME_SET')
    mysql_charset = "charset=utf8"

    default_mysql_url = 'mysql://root:password@localhost/app?charset=utf8'

    if mysql_username and mysql_password and mysql_db_name and \
            mysql_addr and mysql_port:
        return 'mysql+pymysql://' + mysql_username + \
               ':' + mysql_password + '@' + mysql_addr + \
               ':' + mysql_port + '/' + mysql_db_name + \
               '?' + mysql_charset
    else:
        return default_mysql_url


def load_app_sqlite_config():
    return os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, '../db/dbAppTest.db')


def load_app_sqlite_memory_config():
    return os.environ.get('TEST_DATABASE_URL') or 'sqlite:///:memory:'


class DevelopmentSqliteConfig(object):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = load_app_sqlite_config()


class DevelopmentSqliteMemoryConfig(object):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = load_app_sqlite_memory_config()


class DevelopmentMysqlConfig(object):
    SQLALCHEMY_DATABASE_URI = load_app_mysql_config()


class TestingConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = load_app_mysql_config()


class ProductionConfig(object):
    SQLALCHEMY_DATABASE_URI = load_app_mysql_config()


class Config(flask.config.Config):
    def __init__(self):
        super(Config, self).__init__(basedir)
