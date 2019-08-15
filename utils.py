# encoding=utf-8
"""
Date:2019-08-14 16:00
User:LiYu
Email:liyu_5498@163.com
FD:页面信息获取   IP测试工具

"""
import telnetlib
import requests
# colorama是一个python专门用来在控制台、命令行输出彩色文字的模块，可以跨平台使用。
from colorama import Fore
from fake_useragent import UserAgent

from db import RedisClient

ua = UserAgent()


def getPage(url):
    print(Fore.GREEN + '[+] 正在抓取', url)

    try:
        # 代理池为空时，屏蔽下面五行，第一次爬取可不使用代理IP，或者手动设置代理IP
        proxyFromRedis = RedisClient().random()
        proxy = {
                'https': proxyFromRedis,
                'http': proxyFromRedis
        }
        # proxy = {
        #         'https': '122.136.212.132:53281',
        #         'http': '122.136.212.132:53281'
        # }
        headers = {
            'User-Agent': ua.random
        }
        response = requests.get(url, headers=headers, proxies=proxy)
        # response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
    except Exception as e:
        print(Fore.RED + '[-] 抓取失败', url)
        return ''
    else:
        print(Fore.GREEN + '[+] 抓取成功', url, response.status_code)
        # print(response.text)
        return response.text


def testProxyVaild(proxy):
    """
    测试代理IP是否可用
    :param proxy: ip:port
    :return:
    """
    ip, port = proxy.split(":")
    try:
        tn = telnetlib.Telnet(ip, int(port))
    except Exception as e:
        # print(Fore.RED + '[-] IP不可用', e)
        return False
    else:
        return True
