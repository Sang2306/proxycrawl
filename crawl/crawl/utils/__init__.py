import requests

from crawl.crawl.configs import PROXY_CHECKER


def check_proxy(host, port):
    # Check proxy validity
    check_proxy_response = requests.post(PROXY_CHECKER, data={'post_list': f'{host}:{port}'})
    return check_proxy_response.json()[0].get(
        'valid') if check_proxy_response.status_code == 200 else False
