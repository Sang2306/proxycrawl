import scrapy
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(module)s:%(lineno)d:%(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class ProxyCrawler(scrapy.Spider):
    name = 'proxy_crawler'
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'BOT_NAME': 'ProxyCrawlerBot'
    }

    def start_requests(self):
        yield scrapy.Request('https://spys.one/en/http-proxy-list/', callback=self.parse_proxy)

    def parse_proxy(self, response, **kwargs):
        pass
