from . import api
from .cache import cache
class BusLine(object):
    @classmethod
    @cache.cache_on_arguments()
    def get_all_line_ids(cls):
        resp_doc = api.get_line_update_state()
        root = resp_doc['root']
        line_ids = [line['id'] for line in root['lines']['line']]
        return line_ids
    @classmethod
    def get_all_lines(cls):
        line_ids = cls.get_all_line_ids()
        return [cls.get(line_id) for line_id in line_ids]