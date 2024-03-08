# -*-coding:utf-8-*-
from collections import defaultdict

from flask import Flask, render_template, request, jsonify
from jiangshan_bus import JiangshanBus

# 查询示例
QUERY_EXAMPLE = '查询示例： 从西坝河到将台路口西'

# 用户关注公众号时给他推送一条消息
ON_FOLLOW_MESSAGE = {
    'title': '使用说明',
    'description': '',
    'picurl': 'http://doora.qiniudn.com/H9v9n.jpg',
    'url': 'http://t.cn/Rz0J1V6',
}

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def index():
    names = defaultdict(list)
    run_names = []
    for line in JiangshanBus.get_all_lines():
        names[line.type].append(line.name)
    for line in JiangshanBus.get_run_lines():
        run_names.append(line.name)
    return render_template('index.html', names=names, run_names=run_names)


@app.route('/lines/<line>')
def show_bus_line(line):
    stations_up = []
    stations_down = []
    for lines in JiangshanBus.get_all_lines():
        if lines.name == line:
            stations_up = lines.stations_up
            stations_down = lines.stations_down
    return render_template('line.html', line=line, stations_up=stations_up, stations_down=stations_down)


@app.route('/stations/<station>')
def show_bus(station):
    stations = JiangshanBus.get_bus(station)
    print(stations)


if __name__ == '__main__':
    app.run(debug=True, port=8484)
