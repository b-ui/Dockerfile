# -*- coding: utf-8 -*-
import os

import flask

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(flask.config.Config):
    def __init__(self):
        super(Config, self).__init__(basedir)
