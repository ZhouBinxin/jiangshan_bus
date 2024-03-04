import json

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
        print(lines)
        return lines

    @classmethod
    def get_run_lines(cls):
        lines = cls.get_line('XianLuList')
        return lines

    @classmethod
    def search(cls, key):
        return api.search(key)

    @classmethod
    def search_line(cls,name):
        for line in cls.get_all_lines():
            if name in line.name:
                yield line
