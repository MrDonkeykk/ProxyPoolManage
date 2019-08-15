# encoding=utf-8
"""
Date:2019-08-14 16:44
User:LiYu
Email:liyu_5498@163.com
FD:配置信息

"""
# 爬取时测试代理IP的线程数
PROXY_THREAD_COUNT = 200
# 筛选代理IP的线程数
FILTER_THREAD_COUNT = 100
# 最大爬取页数
PAGES = 5
# Redis数据库地址
REDIS_HOST = '127.0.0.1'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = None

REDIS_KEY = 'proxies_2'

# 代理分数
MAX_SCORE = 3
MIN_SCORE = 0
INITIAL_SCORE = 1

VALID_STATUS_CODES = [200, 302]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 200

# 检查周期
TESTER_CYCLE = 20
# 获取周期
GETTER_CYCLE = 300

# 测试API，建议抓哪个网站测哪个
TEST_URL = 'http://www.baidu.com'

# API配置
API_HOST = '0.0.0.0'
API_PORT = 7777

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 10
