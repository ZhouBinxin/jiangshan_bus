import logging
import requests

API_ENDPOINT = 'http://qzjs.shishigj.com/WeixinMP/WMPWebService/GJ.ShiShiGJ/HandlerX.ashx'


def request_api(url, params):
    for _ in range(3):
        try:
            r = requests.get(url, params=params, verify=False)
            return r.json()
        except (ConnectionError, requests.exceptions.Timeout) as e:
            continue
    raise e


def get_line_update_state():
    logging.info('获取所有线路')
    params = {
        'Action': 'GetAllRunningXianLu',
        'KeyWord': '',
    }
    return request_api(API_ENDPOINT, params)


def main():
    lines = get_line_update_state()
    print(lines)


if __name__ == '__main__':
    main()
