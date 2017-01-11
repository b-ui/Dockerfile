import os

from pymongo import MongoClient

host = os.environ.get('MONGO_DB_ADDR') or '192.168.1.103'
port = os.environ.get('MONGO_DB_PORT') or 27017

client = MongoClient(host, int(port))
