from flask import Flask
from flask_caching import Cache

app = Flask(__name__)

# 配置 Flask-Caching
app.config['CACHE_TYPE'] = 'filesystem'
app.config['CACHE_DIR'] = 'offline_data'  # 缓存目录

# 初始化缓存
cache = Cache(app)
