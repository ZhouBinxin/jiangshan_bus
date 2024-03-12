import json
import re
from datetime import datetime
from . import api, cache


class BusLine(object):
    def __init__(self, **kwargs):
        self.name = None
        self.stations_up = []
        self.stations_down = []
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __repr__(self):
        return '<Line: %s>' % self.name

    @classmethod
    @cache.cache_on_arguments()
    def create_line(cls, bus_line):
        line = cls(**{
            'name': bus_line['XianLu'],
            'type': bus_line['XLCatgory'],
            'display_name': bus_line['XLDisplayName'],
            'notice': bus_line['XLNoticeTxt'],
            'style': bus_line['XLNoticeStyle'],
            'num': bus_line['OrderNum'],
            'sort_num': bus_line['XLParmDefOrderNum'],
            'time': bus_line['XianLuPingJunHaoShi']
        })

        stations = api.get_line_site(line.name)
        up_bound = json.loads(stations['RetData']['XianLuList'][0]['XianLuZD'])
        for station in up_bound['xianluzhandian']:
            line.stations_up.append(station['name'])
        down_bound = json.loads(stations['RetData']['XianLuList'][1]['XianLuZD'])
        for station in down_bound['xianluzhandian']:
            line.stations_down.append(station['name'])

        # print(line.stations_up)
        # print(line.stations_down)

        return line

    @classmethod
    @cache.cache_on_arguments()
    def get_line(cls, type):
        resp_doc = api.get_all_lines()
        bus_lines = resp_doc['RetData'][type]

        return [cls.create_line(bus_line) for bus_line in bus_lines]

    @classmethod
    def get_all_lines(cls):
        lines = cls.get_line('XianLuListAll')
        return lines

    @classmethod
    def get_run_lines(cls):
        lines = cls.get_line('XianLuList')
        return lines

    @classmethod
    def search(cls, key):
        return api.search(key)

    @classmethod
    def search_line(cls, name):
        for line in cls.get_all_lines():
            if name in line.name:
                yield line

    @classmethod
    def get_realtime_data(cls, name):
        resp_doc = api.get_line_condition(name)
        # print(resp_doc)
        bus_up = json.loads(resp_doc['RetData']['XianLuList'][0]['XianLuZT'])
        bus_up = bus_up['ZT']
        print(bus_up)
        bus_down = json.loads(resp_doc['RetData']['XianLuList'][1]['XianLuZT'])
        bus_down = bus_down['ZT']
        up = []
        down = []
        for bus in bus_up:
            up.append(cls._format_realtime_data(bus))
        for bus in bus_down:
            down.append(cls._format_realtime_data(bus))

        return up, down

    @classmethod
    def _format_realtime_data(cls, data):
        def num(string):
            result = re.search(r'\d+', string)

            if result:
                extracted_number = int(result.group())
                return extracted_number
            else:
                print(f"提取公交车位置出现错误{string}")

        return {
            'name': data['XianLuName'],
            'postion': num(data['postionId']),
            'state': data['zhuangtai'],
            'next_station_name': datetime.strptime(data['LastValid_Time'], "%Y-%m-%dT%H:%M:%S"),
            'lat': data['LastValid_Latitude'],
            'lon': data['LastValid_Longitude'],
            'angle': data['LastValid_MoveAngle'],
            'speed': data['LastValid_MoveSpeed'],
            'id': data['CheLiangID'],
            "cph": data['CheLiangCPH']
        }
