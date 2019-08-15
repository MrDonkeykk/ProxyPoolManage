# encoding=utf-8
"""
Date:2019-08-15 10:08
User:LiYu
Email:liyu_5498@163.com
FD:定时任务  爬取  测试  API

"""
import time
from multiprocessing import Process

from ProxyPoolFilter import PoolTester
from api import app
from config import TESTER_CYCLE, GETTER_CYCLE, API_HOST, API_PORT, API_ENABLED, TESTER_ENABLED, GETTER_ENABLED
from spider import PoolGetter


class Scheduler():
    def scheduleTester(self, cycle=TESTER_CYCLE):
        """定时检测代理IP是否可用？"""
        tester = PoolTester()
        while True:
            tester.run()
            # 每隔指定时间进行测试
            time.sleep(cycle)

    def scheduleGetter(self, cycle=GETTER_CYCLE):
        """
        定期获取代理
        :param cycle:
        :return:
        """
        getter = PoolGetter()
        while True:
            print("开始抓取代理")
            getter.run()
            time.sleep(cycle)

    def scheduleApi(self):
        """
        开启API
        """
        app.run(API_HOST, API_PORT)

    def run(self):

        print("代理池开始运行......")
        if API_ENABLED:
            print("正在启动API........")
            api_process = Process(target=self.scheduleApi())
            api_process.start()

        if TESTER_ENABLED:
            print("正在启动TESTER.......")
            test_process = Process(target=self.scheduleTester)
            test_process.start()

        if GETTER_ENABLED:
            print("正在启动GETTER......")
            getter_process = Process(target=self.scheduleGetter)
            getter_process.start()


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
