# encoding=utf-8
"""
Date:2019-08-15 11:08
User:LiYu
Email:liyu_5498@163.com
FD:API部署

"""
from flask import Flask

from config import API_HOST, API_PORT
from db import RedisClient

app = Flask(__name__)


@app.route('/')
def index():
    html = """
        <h1 style='color: green'>欢迎来到代理池监控维护器</h1>
        <hr/>
        <ul>
            <li><a href= "/getProxy">获取代理IP</a></li>
            <li><a href= "/count">代理IP个数</a></li>
        </ul>
    """
    return html

@app.route('/getProxy')
def getProxy():
    return RedisClient().random()


@app.route('/count/')
def count():
    return str(RedisClient().count())


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT)
