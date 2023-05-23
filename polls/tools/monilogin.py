import requests
from bs4 import BeautifulSoup
# 登录页面的URL
login_url = 'https://192.168.2.195/bmc/php/processparameter.php'  # 请求登录接口

# login_url = 'https://mes.lexun.ltd:8099/user/login'
# login_url = 'https://36.103.236.129:11179/api/session'
login_data = {
    'check_pwd': 'stor123;',
    'logtype': 0,
    'user_name': 'root',
    'func': 'AddSession'
}
# login_data = {
#     'authType': 'account',
#     'password': 'lxmes123;',
#     'userName': 'liuxuan'
# }
# login_data = {
#     'encrypt_flag': 0,
#     'username': 'admin',
#     'password': 'admin',
#     'login_tag': 996018697
# }
second_data = {
    'token': '4f30dd6d9f8657dd0053b54c354cf8d',
    'func': 'IsSessionTimeout'
}

# 创建Session对象
session = requests.Session()

# 发送POST请求登录
response = session.post(login_url, data=login_data, verify=False)
print(response.status_code)
print(response.cookies.get_dict())
response_secon = session.post('https://192.168.2.195/bmc/php/processparameter.php', data=second_data, verify=False)
print(session.get('https://192.168.2.195/index.php', verify=False).text)

# 检查登录是否成功
if response.status_code == 200:
    # 登录成功，访问需要登录才能访问的页面
    # target_url = 'https://36.103.236.129:11179/#dashboard'
    target_url = 'https://192.168.2.195/index.php'
    response = session.get(target_url, verify=False)

    print(response.text)
    # 解析页面内容，提取需要的信息
    soup = BeautifulSoup(response.text, 'html.parser')
    # info = soup.find('div', {'class': 'info'}).text
    # 输出信息
    # print(info)
else:
    # 登录失败，输出错误信息
    print('Login failed.')
