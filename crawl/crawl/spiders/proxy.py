import scrapy
import logging
import re

from ..configs import PROXY_POOL

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
        PROXY_POOL['proxies'].delete_many({})
        for url in [
            'https://spys.one/en/free-proxy-list/',
            'https://spys.one/en/http-proxy-list/',
            'https://spys.one/en/anonymous-proxy-list/'
        ]:
            yield scrapy.Request(url, callback=self.parse_proxy)

    def parse_proxy(self, response, **kwargs):
        for index, spy1xx in enumerate(response.xpath('//tr[@class="spy1xx"]'), start=1):
            # get port dynamically gen code
            port_code = response.xpath("/html/body/script/text()").get()
            exec(port_code)
            host = response.xpath(f'//tr[@class="spy1xx"][{index}]/td[1]/font/text()').get()
            port_raw_text = response.xpath(f'//tr[@class="spy1xx"][{index}]/td[1]/font/script/text()').get()
            port_number_code_raw, port_number_code = re.findall("[^+(]+[a-z0-9][)]", port_raw_text), []
            port = ''
            for code in port_number_code_raw:
                port += str(eval(code[:-1]))

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
                'host_post': f'{host}:{port}',
                'scheme': scheme,
                'anonymity': anonymity,
                'country': country,
                'host_name_org': host_name_org,
                'latency': latency,
                'uptime': uptime,
                'check_date': check_date,
            })

        for index, spy1x in enumerate(response.xpath('//tr[@class="spy1x"]'), start=1):
            # get port dynamically gen code
            if index <= 1:
                continue
            port_code = response.xpath("/html/body/script/text()").get()
            exec(port_code)
            host = response.xpath(f'//tr[@class="spy1x"][{index}]/td[1]/font/text()').get()
            port_raw_text = response.xpath(f'//tr[@class="spy1x"][{index}]/td[1]/font/script/text()').get()
            port_number_code_raw, port_number_code = re.findall("[^+(]+[a-z0-9][)]", port_raw_text), []
            port = ''
            for code in port_number_code_raw:
                port += str(eval(code[:-1]))

            proxy_type = response.xpath(f'//tr[@class="spy1x"][{index}]/td[2]/a/font/text()').getall()
            anonymity = response.xpath(f'//tr[@class="spy1x"][{index}]/td[3]/a/font/text()').get()
            country = response.xpath(f'//tr[@class="spy1x"][{index}]/td[4]/a/font/text()').get()
            host_name_org = response.xpath(f'//tr[@class="spy1x"][{index}]/td[5]/font/text()').get()
            latency = response.xpath(f'//tr[@class="spy1x"][{index}]/td[6]/font/text()').get()
            uptime = response.xpath(f'//tr[@class="spy1x"][{index}]/td[8]/font/acronym/text()').get()
            check_date = response.xpath(f'//tr[@class="spy1x"][{index}]/td[9]/font/font/text()').getall()
            check_date = check_date[0] + check_date[1]
            scheme = proxy_type[0]
            if len(proxy_type) >= 2:
                scheme = proxy_type[0] + proxy_type[1]
            PROXY_POOL['proxies'].insert_one({
                'host_post': f'{host}:{port}',
                'scheme': scheme,
                'anonymity': anonymity,
                'country': country,
                'host_name_org': host_name_org,
                'latency': latency,
                'uptime': uptime,
                'check_date': check_date,
            })
