# -*- coding: utf-8 -*-

import os
from datetime import timedelta

from flask import Flask, jsonify

from app.common.log_util import stream_handler, logger
from app.mod_strategy.task import scheduler
from config import load_db_config, load_apscheduler_config


def create_app():
    app = Flask(__name__)
    app.config.from_object(load_db_config())
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(app.root_path), 'downloads')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
    app.config['SECRET_KEY'] = r'\xff\x9a\x00\x03\xf1\xf2\x06\x9f\x95\xdfNn\xb9\xcde' \
                               r'\xa0a<Z\x89?\xba\x80\x809\x8c\x90\xc2\xc79\xd5\x17'
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=36000)
    app.config.from_object(load_apscheduler_config())
    stream_handler.push_application()
    scheduler.init_app(app)
    scheduler.start()

    @app.route('/api/help', methods=['GET'])
    def get_help():
        endpoints = [rule.rule for rule in app.url_map.iter_rules() if rule.endpoint != 'static']
        return jsonify(dict(api_endpoints=endpoints))

    return app
