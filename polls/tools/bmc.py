import json
import requests
import urllib3
from bs4 import BeautifulSoup
# 登录页面的URL
login_url = 'https://blog.csdn.net/u010383467'  # 请求登录接口

# login_url = 'https://mes.lexun.ltd:8099/user/login'
# login_data = {
#     'check_pwd': 'stor123;',
#     'logtype': 0,
#     'user_name': 'root',
#     'func': 'AddSession'
# }
# login_data = {
#     'authType': 'account',
#     'password': 'lxmes123;',
#     'userName': 'liuxuan'
# }
login_data = {
    # 'encrypt_flag': 0,
    'username': 'k/W+RDlPybrozOudNN7T60TqYn9+c5DJGy3Wbp6vJFR3T/bRgW8JZnQGatzxsqfYlj9lDWJRarrpAT7Jv9PWkVuQCSKiCnnOiLz36'
                '0CPq8TQABT6qJn+HBIPggEgKdCoqxhxFM5vsiA3ngnY0Q4xR+d2ES4cvXOZoqx5w3OTY2s=',
    'password': 'dGFgHOvJRfmd1u+bdKGQmL3UxEDcPXawCu21df8ZJbj7s3Hj5gTxr8U49ln7WKKN8XGU7miZkX0WC5IdNuP5QWYd69RyOIuHz8sh8y'
                'Xc/Zb20IDBny0jyi9VnQzuhNmxtRNNvCLdU4DweLHA50gy8my6KR9f2HvoNbDKiVYpLug=',
    'log_type': 1
    # "CSRFToken": "jxILxLps"
}
login_header = {
    'Content-Type': 'application/json'
}
# 创建Session对象
sessions = requests.Session()

# 发送POST请求登录
# urllib3.disable_warnings()

response = sessions.post(login_url, data=login_data, verify=False)
# print(response.status_code)
print(response.cookies.get_dict())
print(response.text)
# 检查登录是否成功
if response.status_code == 200:
    # 登录成功，访问需要登录才能访问的页面
    target_url = 'https://192.168.0.51/#dashboard'
    response = sessions.get(target_url, verify=False, cookies=response.cookies, timeout=10)
    response.encoding = 'utf-8'
    print(response.text)
    print(response.cookies.get_dict())
    # 解析页面内容，提取需要的信息
    # soup = BeautifulSoup(response.text, 'html.parser')
    # info = soup.find('div', {'class': 'info'}).text
    # 输出信息
    # print(info)
else:
    # 登录失败，输出错误信息
    print('Login failed.')


