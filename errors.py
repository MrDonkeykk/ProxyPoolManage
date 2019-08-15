# encoding=utf-8
"""
Date:2019-08-14 16:32
User:LiYu
Email:liyu_5498@163.com
FD:代理不足ERROR

"""


class PoolEmptyError(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理池已经枯竭')
