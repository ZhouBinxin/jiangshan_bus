import logging

from flask import Flask, render_template
from flask_weixin import Weixin

from jiangshan_bus import JiangshanBus

# 查询示例
QUERY_EXAMPLE = '查询示例： 从凤林路口到江山站'

# 用户关注公众号时给他推送一条消息
ON_FOLLOW_MESSAGE = {
    'title': '使用说明',
    'description': '',
    'picurl': '',
    'url': '',
}

app = Flask(__name__)
app.config.from_object('config')

weixin = Weixin(app)
app.add_url_rule('/weixin', view_func=weixin.view_func)

# 配置日志记录器
log_file = 'error.log'
logging.basicConfig(filename=log_file, level=logging.ERROR)  # 将日志级别设置为 ERROR


@weixin.register('*')
def query(**kwargs):
    username = kwargs.get('sender')
    sender = kwargs.get('receiver')
    message_type = kwargs.get('type')

    def r(content):
        return weixin.reply(
            username, sender=sender, content=content
        )

    if message_type == 'event' and kwargs.get('event') == 'subscribe':
        return weixin.reply(
            username, type='news', sender=sender, articles=[ON_FOLLOW_MESSAGE]
        )

    content = kwargs.get('content')
    if not content:
        reply = '我好笨笨哦，还不懂你在说什么。\n%s' % QUERY_EXAMPLE
        return r(reply)

    if isinstance(content, str):
        content = content.encode('utf-8')

    stations = JiangshanBus.extract_stations(content)
    lines = BeijingBus.extract_lines(content)
    if len(stations) < 2:
        reply = '没有结果，可能还不支持这条线路呢~ \n%s' % QUERY_EXAMPLE
        return r(reply)

    from_station, to_station = stations[:2]
    lines = match_stations_with_lines(from_station, to_station, lines)
    if not lines:
        reply = '没有结果，可能还不支持这条线路呢~ \n%s' % QUERY_EXAMPLE
        return r(reply)

    reply = get_realtime_message(lines, from_station)
    return r(reply)


if __name__ == '__main__':
    app.run(debug=True, port=8484)
