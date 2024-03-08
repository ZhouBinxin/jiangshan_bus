import re

from .cache import cache
from .line import BusLine


class JiangshanBus(object):

    @classmethod
    def get_all_lines(cls):
        return BusLine.get_all_lines()

    @classmethod
    def get_run_lines(cls):
        return BusLine.get_run_lines()

    @classmethod
    def search(cls, keyword):
        return BusLine.search(keyword)

    @classmethod
    def search_lines(cls, name):
        return list(BusLine.search(name))

    @classmethod
    @cache.cache_on_arguments()
    def get_all_stations(cls):
        stations_up = []
        stations_down = []
        for line in cls.get_all_lines():
            for station in line.stations_up:
                stations_up.append(station)
            for station in line.stations_down:
                stations_down.append(station)

        return stations_up, stations_down

    @classmethod
    def extract_lines(cls, sentence):
        numbers = re.findall(r'\d+', sentence)
        if not numbers:
            return []

        lines = JiangshanBus.search_lines(numbers[0])
        lines = [line for line in lines if line.num == numbers[0]]
        return lines

    @classmethod
    def extract_stations(cls, sentence):
        original_sentence = sentence
        matches = set()
        for s in cls.get_all_stations():
            if s.name in sentence:
                matches.add(s)
                sentence = sentence.replace(s.name, '')
        # 按在sentence中出现的顺序排序
        return sorted(matches, key=lambda s: original_sentence.find(s.name))

    @classmethod
    def get_bus(cls, station):
        return BusLine.get_realtime_data(station)
