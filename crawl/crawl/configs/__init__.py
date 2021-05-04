import urllib.parse
from pymongo import MongoClient

DB_HOST = "0.0.0.0"

mg_client = MongoClient(
    f'mongodb://root:{urllib.parse.quote("root")}@{DB_HOST}:27017/?authMechanism=SCRAM-SHA-256'
)

PROXY_API_VENDOR = "http://pubproxy.com/api/proxy"

PROXY_CHECKER = 'https://proxy-checker.net/api/proxy-checker/'

PROXY_POOL = mg_client['proxy-pool']
