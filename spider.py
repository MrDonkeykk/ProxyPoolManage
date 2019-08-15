# encoding=utf-8
"""
Date:2019-08-14 14:37
User:LiYu
Email:liyu_5498@163.com
FD:爬虫模块，包含 爬取，存储到代理池

"""

import re
import sys
from config import POOL_UPPER_THRESHOLD, PAGES, PROXY_THREAD_COUNT
from concurrent.futures import ThreadPoolExecutor
from utils import *


class ProxyMetaClass(type):
    """
    自定义元类，获取目标类中所有爬取IP的函数信息
    """

    def __new__(cls, name, bases, attrs):
        """
        :param name: Crawler, 被装饰的类名
        :param bases: (<class 'object'>,), 被装饰的类的父类
        :param attrs:{'属性名': '属性值', '方法名': '方法对象'}， 被装饰的类的详细信息
        :return:
        """
        count = 0
        # 给被装饰的类新增两个属性
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaClass):
    def getProxies(self, callback):
        # print(callback)
        for proxy in eval("self.{}()".format(callback)):
            yield proxy

    def crawlXicidaili(self):
        for page in range(1, PAGES + 1):
            startUrl = 'https://www.xicidaili.com/nt/%s' % page
            html = getPage(startUrl)
            if html:
                findtrs = re.compile(r'<tr class=.*?>(.*?)</tr>', re.S)
                trs = findtrs.findall(html)
                findip = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')
                findport = re.compile(r'<td>(\d+)</td>')
                for tr in trs:
                    # print(tr)
                    ip = findip.findall(tr)[0]
                    port = findport.findall(tr)[0]
                    addressPort = ip + ':' + port
                    yield addressPort
            else:
                yield ''


class PoolGetter(object):
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def isOverThreshold(self):
        """
         判断是否达到了代理池限制
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def testProxyAdd(self, proxy):
        """检测是否可用， 可用添加到redis中"""
        if testProxyVaild(proxy):
            print(Fore.GREEN + '成功获取到代理', proxy)
            self.redis.add(proxy)

    def run(self):
        print(Fore.GREEN + "[-] 代理池获取器开始执行......")
        if not self.isOverThreshold():
            for callbackLabel in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callbackLabel]
                # 获取代理
                proxies = self.crawler.getProxies(callback)
                # 刷新输出
                sys.stdout.flush()
                with ThreadPoolExecutor(PROXY_THREAD_COUNT) as pool:
                    pool.map(self.testProxyAdd, proxies)


def isPoolGetterOK():
    pool = PoolGetter()
    pool.run()
    print(pool.redis.count())


def isCrawlerOK():
    """
    测试爬虫代码
    :return:
    """
    crawler = Crawler()
    # print(crawler.__CrawlFuncCount__)
    for callbackLabel in range(crawler.__CrawlFuncCount__):
        # print(callbackLabel)
        callback = crawler.__CrawlFunc__[callbackLabel]
        proxies = crawler.getProxies(callback)
        # print(proxies)
        for i in proxies:
            print(i)


if __name__ == '__main__':
    # isCrawlerOK()
    isPoolGetterOK()
