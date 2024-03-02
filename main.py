from flask import Flask, render_template, request
from jiangshan_bus import JiangshanBus

# 创建一个 Flask 应用实例
app = Flask(__name__)


# 定义路由和视图函数
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'user_input' in request.form:
            user_input = request.form['user_input']
            return render_template('result.html', user_input=user_input)
        elif 'line' in request.form:
            lines = JiangshanBus.get_run_lines()
            # print(lines)
            return render_template('line.html', lines=lines)
        elif 'station' in request.form:
            stations = JiangshanBus.get_all_stations()
            return render_template('line.html', lines=stations)
    return render_template('index.html')


# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
