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
    def get_line_stations(cls, line):
        return BusLine.get_stations(line)

    @classmethod
    @cache.cache_on_arguments()
    def get_all_stations(cls):
        stations = []
        for line in cls.get_all_lines():
            for s in cls.get_line_stations(line):
                stations.append(s)
        return stations

    @classmethod
    def extract_stations(cls, sentence):
        """
        从句子中提取出所有的车站

        :param sentence:
        :return:
        """
        original_sentence = sentence
        matches = set()
        for s in cls.get_all_stations():
            if s.name in sentence:
                matches.add(s)
                sentence = sentence.replace(s.name, '')
        # 按在sentence中出现的顺序排序
        return sorted(matches, key=lambda s: original_sentence.find(s.name))
