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


def get_all_lines():
    """
    获取所有线路
    :return:
    """
    logging.info('获取所有线路')
    params = {
        'Action': 'GetAllRunningXianLu'
    }
    return request_api(API_ENDPOINT, params)


def get_line_condition(line):
    """
    获取指定线路车辆情况

    :return:
    """
    logging.info('Fetching line: %s' % line)
    params = {
        'Action': 'GetXianLuCheKuang',
        'XianLu': line,
    }
    return request_api(API_ENDPOINT, params)


def get_line_site(line):
    """
    获取指定线路站点信息

    :return:
    """
    logging.info('Fetching line: %s' % line)
    params = {
        'Action': 'GetXianLuZhanDian',
        'XianLu': line,
    }
    return request_api(API_ENDPOINT, params)


def main():
    lines = get_line_condition(101)
    print(lines)


if __name__ == '__main__':
    main()
