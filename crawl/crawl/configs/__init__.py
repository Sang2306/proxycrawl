import urllib.parse
from pymongo import MongoClient

DB_HOST = "0.0.0.0"

mg_client = MongoClient(
    f'mongodb://root:{urllib.parse.quote("root")}@{DB_HOST}:27017/?authMechanism=SCRAM-SHA-256'
)

PROXY_POOL = mg_client['proxy-pool']
