import json
import logging
import requests
import xmltodict

API_ENDPOINT = 'http://qzjs.shishigj.com/WeixinMP/WMPWebService/GJ.ShiShiGJ/HandlerX.ashx'


def request_api(url, params):
    for _ in range(3):
        try:
            r = requests.get(url, params=params, verify=False)
        except (ConnectionError, requests.exceptions.Timeout) as e:
            continue
        else:
            print(r)
            return r.text
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

def search(key):
    """
    搜索线路或站点

    :param key: 线路或站点
    :return:
    """
    params = {
        'Action': 'SearchXianLu',
        'KeyWord': key,
    }
    return request_api(API_ENDPOINT, params)

def main():
    lines = search("火车站")
    print(lines)


if __name__ == '__main__':
    main()
