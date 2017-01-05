import os

from pymongo import MongoClient

host = os.environ.get('MONGO_DB_ADDR') or '172.17.0.2'
port = os.environ.get('MONGO_DB_PORT') or 27017

client = MongoClient(host, int(port))
