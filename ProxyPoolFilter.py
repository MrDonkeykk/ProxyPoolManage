# encoding=utf-8
"""
Date:2019-08-15 09:19
User:LiYu
Email:liyu_5498@163.com
FD:检测代理池内代理IP状态

"""
from colorama import Fore

from db import RedisClient, FILTER_THREAD_COUNT
from utils import testProxyVaild
from concurrent.futures import ThreadPoolExecutor


class PoolTester(object):
    def __init__(self):
        self.redis = RedisClient()

    def testSingleProxy(self, proxy):
        """
        测试单个代理
        :param proxy:
        :return:
        """
        if testProxyVaild(proxy):
            self.redis.max(proxy)
            print(Fore.GREEN + "[+] 代理可用", proxy)
        else:
            self.redis.drop(proxy)
            print(Fore.RED + "[-] 代理不可用", proxy)

    def run(self):
        """
        测试的主函数
        :return:
        """
        print(Fore.GREEN + "测试器开始运行.......")
        try:
            count = self.redis.count()
            print(Fore.GREEN + "当前剩余%d个代理" % count)
            # 使用线程池, 快速检测proxy是否可用
            with ThreadPoolExecutor(FILTER_THREAD_COUNT) as pool:
                pool.map(self.testSingleProxy, self.redis.all())
        except Exception as e:
            print(Fore.RED + "测试器发生错误", e)


if __name__ == '__main__':
    tester = PoolTester()
    tester.run()
