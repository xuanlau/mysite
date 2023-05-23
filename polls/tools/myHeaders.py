import random
import time


# 随机获取请求头

user_agent_list = [
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET'
    ' CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'
]


def get_user_agent():
    user_agent = random.choice(user_agent_list)
    return user_agent


# 随机获取一个代理IP
# proxy_list = [
#    'http':'http://159.224.13.29:61366',
#    'https':'https://159.224.13.29:61366'
# ]
# def get_proxy():
#     proxy_ip = random.choice(proxy_list)
#     return proxy_ip