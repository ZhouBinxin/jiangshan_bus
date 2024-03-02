import requests


class WX(object):
    def get_access_token(appid, appsecret, force_refresh=False):
        """
        获取微信公众号access_token

        :param appid:
        :param appsecret:
        :param force_refresh: 是否强制刷新，默认False
        :return:
            - tuple: 包含access_token和expires_in的元组，如果获取失败，则返回(None, None)
        """
        url = 'https://api.weixin.qq.com/cgi-bin/stable_token'
        payload = {
            'grant_type': 'client_credential',
            'appid': appid,
            'secret': appsecret,
            'force_refresh': force_refresh
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            if data.get('errcode' != 0):
                print(f"获取失败: {data.get('errcode')}, {data.get('errmsg')}")
                return None, None

            access_token = data.get('access_token')
            # access_token有效时长
            expires_in = data.get('expires_in')
            return access_token, expires_in
        else:
            print(f"获取失败: {response.status_code}, {response.text}")
            return None, None
