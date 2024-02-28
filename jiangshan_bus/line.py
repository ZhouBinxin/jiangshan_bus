import json

from . import api


class BusLine(object):
    def __init__(self):
        pass

    @classmethod
    def get_all_lines(cls):
        """
        获取所有公交线路

        :return:
        """
        lines_data = api.get_all_lines()
        lines = []
        for line_data in lines_data['RetData']['XianLuListAll']:
            lines.append(line_data['XianLu'])

        return lines

    @classmethod
    def get_run_lines(cls):
        """
        获取所有正在运行的公交线路

        :return:
        """
        lines_data = api.get_all_lines()
        lines = []
        for line_data in lines_data['RetData']['XianLuList']:
            lines.append(line_data['XianLu'])

        return lines

    @classmethod
    def get_stations(cls, line):
        """
        获取公交线路的所有站点

        :param line: 公交线路
        :return:
        """
        stations_data = api.get_line_site(line)
        stations_data = json.loads(stations_data['RetData']['XianLuList'][0]['XianLuZD'])
        print(stations_data)
        stations = []
        for station_data in stations_data['xianluzhandian']:
            stations.append(station_data['name'])

        return stations


def main():
    bus_line = BusLine()
    lines = bus_line.get_all_lines()
    # print('所有线路', lines)
    lines = bus_line.get_run_lines()
    # print('正在运行的线路', lines)
    station = bus_line.get_stations(lines[0])
    print(station)


if __name__ == '__main__':
    main()
