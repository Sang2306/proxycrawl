import scrapy
import logging

from crawl.configs import PROXY_POOL

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
        for index, spy1xx in enumerate(response.xpath('//tr[@class="spy1xx"]'), start=1):
            host_port = response.xpath(f'//tr[@class="spy1xx"][{index}]/td[1]/font/text()').getall()
            proxy_type = response.xpath(f'//tr[@class="spy1xx"][{index}]/td[2]/a/font/text()').getall()
            anonymity = response.xpath(f'//tr[@class="spy1xx"][{index}]/td[3]/a/font/text()').get()
            country = response.xpath(f'//tr[@class="spy1xx"][{index}]/td[4]/a/font/text()').get()
            host_name_org = response.xpath(f'//tr[@class="spy1xx"][{index}]/td[5]/font/text()').get()
            latency = response.xpath(f'//tr[@class="spy1xx"][{index}]/td[6]/font/text()').get()
            uptime = response.xpath(f'//tr[@class="spy1xx"][{index}]/td[8]/font/acronym/text()').get()
            check_date = response.xpath(f'//tr[@class="spy1xx"][{index}]/td[9]/font/font/text()').getall()
            check_date = check_date[0] + check_date[1]
            scheme = proxy_type[0]
            if len(proxy_type) >= 2:
                scheme = proxy_type[0] + proxy_type[1]
            PROXY_POOL['proxies'].insert_one({
                'host_post': host_port,
                'scheme': scheme,
                'anonymity': anonymity,
                'country': country,
                'host_name_org': host_name_org,
                'latency': latency,
                'uptime': uptime,
                'check_date': check_date,
            })
