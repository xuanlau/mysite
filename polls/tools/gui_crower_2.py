import PySimpleGUI as sg
import paramiko
import gui_thread
import queue
import threading
import datetime

# 一个用于库房人员压测的工具


def ssh_command(ip_address, username, password, command, key_filename=None, password_mysql=None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=ip_address, username=username, password=password, timeout=1, key_filename=key_filename)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if error:
            result_info = error
        else:
            result_info = output
    except Exception as e:
        result_info = f'Error: {e}'
    finally:
        client.close()
        # 将输出到文本框的操作封装到函数中，启动子线程时直接将结果输出到文本框
    if command == '/root/scripts/ping.sh':
        window['-OUTPUT-'].update('当前无盘环境:\n' + result_info)
    elif command == '/root/scripts/mysql.sh 123..com True':
        window['-OUTPUT-'].update('当前数据库中IP:\n' + result_info)
    elif command == '/root/scripts/mysql.sh ' + str(password_mysql):
        window['-FUNC-A-'].update(result_info)
    else:
        pass
    # return result_info  目前无需返回值


# 定义登录界面布局
def ret_layout_login(time_str):
    layout_login = [[sg.Text('请登录', font=('宋体', 20), pad=((250, 0), (50, 10))), sg.Text(time_str)],
                    [sg.Text('用户名：', size=(8, 1)), sg.InputText(key='-USERNAME-')],
                    [sg.Text('密码：', size=(8, 1)), sg.InputText(key='-PASSWORD-', password_char='*')],
                    [sg.Button('登录', bind_return_key=True), sg.Button('退出')]]
    return layout_login


# 定义主界面布局
menu_def = [['File', ['Exit']],
            ['Help', ['About']]]
raid_options_list = ['default', 'raid0', 'raid1', 'noraid']
os_option_list = ['centos7.6', 'ubuntu20.04', 'debian9.13']
bios_option_list = ['legacy', 'uefi']
yace_size = (13, 1)


def create_custom_(mount_point, key_str):
    return [sg.Text(mount_point, size=yace_size),
            sg.Input('', key=key_str, size=yace_size, pad=(0, 0)), sg.Text('GB', pad=(0, 0))]


def ret_layout_pxe(disabled_str):
    layout_pxe = [[sg.Text('PXE环境', font=('微软雅黑', 10), text_color='white', background_color='purple'), sg.Button('切换用户')],
                  [sg.Text('! 分区大小为1则代表剩余磁盘的容量全部分配(boot/swap除外)', font=('微软雅黑', 10),
                           text_color='red', background_color='white')],
                  [sg.Text("操作系统", size=yace_size), sg.Combo(os_option_list,
                                                                 size=yace_size,
                                                                 key="-OS_TYPE-", pad=(0, 0)), sg.Text('')],
                  [sg.Text("BIOS", size=yace_size), sg.Combo(bios_option_list,
                                                             size=yace_size,
                                                             key="-BIOS_TYPE-", pad=(0, 0)),
                   sg.Text('')],
                  [sg.Text('密码', size=yace_size),
                   sg.InputText('', key='pxe_password', size=yace_size, password_char='*', pad=(0, 0)),
                   sg.Text('')]]
    args_dict = {'/: ': 'r_input', '/boot: ': 'boot_input', 'swap: ': 'swap_input'}
    for k, v in args_dict.items():
        layout_pxe.append(create_custom_(k, v))
    layout_pxe.append([sg.Button('提交PXE数据', size=yace_size, disabled=disabled_str),
                       sg.Button('添加自定义挂载路径', disabled=disabled_str)])
    return layout_pxe
# layout_main必须为列表，且列表中的每一个元素都必须为可迭代的列表或者切片


def ret_layout_main(disabled_str, layout_pxe_str):  # 此处改为函数化，返回一个layout列表，最终目的是为了用户权限的区分，disabled_str定义了按钮是否可以点击，从而定义权限
    return [[sg.Menu(menu_def, tearoff=False)],
            # sg.Column 方法，提供了控制整体元素位置的参数：justification
            [sg.Column(
                layout=[[sg.Text('老化环境', font=('微软雅黑', 10), text_color='white', background_color='purple')],
                        [sg.Text("系统盘类型", size=yace_size), sg.Combo(raid_options_list, size=yace_size,
                                                                         default_value=raid_options_list[0],
                                                                         key="-RAID_TYPE-"), sg.Text('')],
                        [sg.Text('CPU压测时间', size=yace_size),
                         sg.Input('', key='cpu_input', size=yace_size), sg.Text('秒')],
                        [sg.Text('内存压测时间', size=yace_size),
                         sg.Input('', key='mem_input', size=yace_size), sg.Text('秒')],
                        [sg.Text('硬盘压测时间', size=yace_size),
                         sg.Input('', key='disk_input', size=yace_size), sg.Text('秒')],
                        [sg.Button('提交老化数据', size=yace_size, disabled=disabled_str)]],  # disabled=True使得按钮不可点击
                justification='left'), sg.Column(layout=layout_pxe_str, justification='right')],
            # [sg.InputText(key='-SEARCH-', size=(50, 1), background_color='#FFFFFF', text_color='#663399')],
            [sg.Button('扫描无盘环境', button_color=('white', '#663399')), sg.Button('查询当前数据库IP数量',
                                                                                     button_color=(
                                                                                         'white', '#663399')),
             sg.Button('导出数据库数据(默认当前路径下)', button_color=('white', '#663399')),
             sg.Button('显卡环境部署/压测', button_color=('white', '#663399'))],
            [sg.Multiline(key='-OUTPUT-', size=(80, 8), autoscroll=True, disabled=True)],
            [sg.Column(layout=[[sg.Button('清空数据库并备份', size=(20, 1))],
                               [sg.Multiline(key='-FUNC-A-', size=(40, 6))]], element_justification='left'),
             sg.Column(layout=[[sg.Button('执行远程命令(ssh)', size=(20, 1))], [sg.Multiline(key='-SSH-RESULT-',
                                                                                             size=(40, 6))]],
                       element_justification='right')],
            [sg.Text('注：\n1、新增老化压测提交。\n2、新增PXE环境数据提交。\n3、点击扫描无盘环境可以看到正在压测的IP。\n4、点击清空数据库并备份即可清空数据库并备份。\n5、执行SSH命令需输入用户'
                     '名、密码、IP地址和命令。\n6、点击查询数据库IP，即可查看当前数据库里的IP。\n7、点击导出数据库数据，即可将数据库数据导出到当前路径下。\n8、新增显卡环境部署和压测。'
                     , font=('宋体', 13),
                     pad=((0, 0), (30, 0)), text_color='red')],
            [sg.Text('版权所有 ©2023 Crower Inc.。', font=('宋体', 8), pad=((0, 0), (30, 0)))]]


# 创建主窗口
time_str = now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
layout_login = ret_layout_login(time_str)
window = sg.Window('运维管理系统', layout_login, finalize=True)
win_mysql_active = False
win_ssh_active = False
window_pxe_custom_active = False
win_xianka_active = False
window_mysql_password = ''
window_ssh = ''
window_pxe_custom = ''
window_xianka = ''
q = queue.Queue()
custom_data = []
user_xianka = ''
password_xianka = ''


def create_custom(custom_data):
    return [
        # [sg.Button('添加一行数据'), sg.Column([[sg.Input(), sg.Input()] for i in range(len(custom_data) + 1)])],# 旧
        [sg.Text('挂载点', size=20), sg.Text('分区大小', size=20)],
        [[sg.Input('', size=20, key=f'mount_{j}'), sg.Input('', size=20, key=f'size_{j}')]
         for j in range(len(custom_data) + 1)],
    ]


while True:
    event, values = window.read(timeout=100)
    if event in (None, '退出', 'Exit'):
        break
    # 登录验证, 实现用户权限的区分，基于按钮是否可以点击。
    if event == '登录':
        if values['-USERNAME-'] == 'admin' and values['-PASSWORD-'] == '123..com':
            window.close()
            # 登录验证成功后，渲染新的界面，此为admin用户，权限不足，有些按钮无法点击，pxe界面的layout改为参数传入到函数
            layout_pxe = ret_layout_pxe(True)
            layout_main = ret_layout_main(True, layout_pxe)
            window = sg.Window('运维管理系统', layout_main, element_justification='center', finalize=True)
        elif values['-USERNAME-'] == 'root' and values['-PASSWORD-'] == '123..com':
            window.close()
            layout_pxe = ret_layout_pxe(False)
            layout_main = ret_layout_main(False, layout_pxe)
            window = sg.Window('运维管理系统', layout_main, element_justification='center', finalize=True)
        else:
            sg.popup('用户名或密码错误！')
    if event == '切换用户':
        window.close()
        time_str = now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")  # layout不可被重复使用(只可以使用一次)
        window = sg.Window('运维管理系统', ret_layout_login(time_str), finalize=True)
    if event == '提交老化数据':
        # 拼接老化环境数据, 使用.format方法格式化数据，丝滑
        com = '/root/scripts/replace.sh {} {} {} {}'.format(values['-RAID_TYPE-'], values['cpu_input'],
                                                            values['mem_input'], values['disk_input'])
        gui_thread.run_backend(q, com)
    if event == '提交PXE数据':
        # 拼接所有PXE装机所需的数据，目前还剩自定义挂载的数据
        custom_str = ''
        if len(custom_data) >= 1:
            for i in custom_data:
                for k, v in i.items():
                    custom_str += (k + ':' + v)
                custom_str += ' '
        com = '/root/scripts/pxe.sh -o {} -B {} -p {} ' \
              '-r {} -b {} -s {} -c "{}"'.format(values['-OS_TYPE-'], values['-BIOS_TYPE-'], values['pxe_password'],
                                                 values['r_input'],
                                                 values['boot_input'], values['swap_input'], custom_str)
        window['-OUTPUT-'].print(com)
        thread = gui_thread.MyThread(ssh_command, ('192.168.2.149', 'root', '123..com', com,
                                                   None))  # 将获取返回值并输出到文本框的操作封装到函数中，启动子线程时直接将结果输出到文本框
        thread.setDaemon(True)  # True主线程运行结束时不对这个子线程进行检查而直接退出
        thread.start()  # 启动线程
    if event == '添加自定义挂载路径' and not window_pxe_custom_active:
        window_pxe_custom_active = True
        custom_data.append('')
        layout_pxe_custom = create_custom(custom_data) + [[sg.Button('提交自定义挂载数据', size=15)]]
        # [sg.Text('挂载点'), sg.Text('分区大小')]
        window_pxe_custom = sg.Window('PXE高级选项', layout_pxe_custom, finalize=True)
        custom_data = []
    if window_pxe_custom_active:
        event_pxe, values_pxe = window_pxe_custom.read(timeout=100)
        if event_pxe in [None, '退出']:
            window_pxe_custom_active = False
            window_pxe_custom.close()  # 关闭子窗口
        if event_pxe == '提交自定义挂载数据':
            mount_one = {values_pxe['mount_0']: values_pxe['size_0']}
            mount_two = {values_pxe['mount_1']: values_pxe['size_1']}
            custom_data.append(mount_one)
            custom_data.append(mount_two)
            print(custom_data)
            window_pxe_custom.close()
    if event == '扫描无盘环境':
        window['-OUTPUT-'].update('')
        window['-OUTPUT-'].update('正在扫描地址...')
        thread = gui_thread.MyThread(ssh_command, ('192.168.2.149', 'root', '123..com', '/root/scripts/ping.sh',
                                                   None))  # 将获取返回值并输出到文本框的操作封装到函数中，启动子线程时直接将结果输出到文本框
        thread.setDaemon(True)  # True主线程运行结束时不对这个子线程进行检查而直接退出
        thread.start()  # 启动线程
    if event == '查询当前数据库IP数量':
        window['-OUTPUT-'].update('')
        window['-OUTPUT-'].update('正在查询当前数据库IP数量...')
        try:
            thread = gui_thread.MyThread(ssh_command, ('192.168.2.149', 'root', '123..com',
                                                       '/root/scripts/mysql.sh 123..com True', None))
            thread.setDaemon(True)  # True主线程运行结束时不对这个子线程进行检查而直接退出
            thread.start()  # 启动线程
        except Exception as e:
            result = e
    if event == '导出数据库数据(默认当前路径下)':
        args = ['192.168.2.149', 3306, 'root', '123..com', 'pxe', 'utf8']
        hanshu = gui_thread.dump_mysql_data(args=args)
        # thread_dump = gui_thread.MyThread(hanshu.dump_data, ())  # 考虑时间长的任务情况下用多线程
        # thread_dump.setDaemon(True)
        # thread_dump.start()
        try:
            hanshu.dump_data()  # 导出
            end_path = '路径：' + hanshu.timemark()
            sg.popup(end_path, title='导出完成')
        except Exception as e:
            sg.popup(e, title='导出失败！')
    if event == '切换无盘环境':
        layout_wupan = [[sg.Checkbox('legacy', key='-LEGACY-'), sg.Checkbox('uefi', key='-UEFI-'), sg.Button('提交')],
                        [sg.Combo(['centos7.6', 'centos7.9', 'ubuntu20.04.4', 'ubuntu20.04.5'],
                                  default_value='centos7.6',
                                  key='-OS-'), sg.Button('提交')], ]
    if event == '显卡环境部署/压测':
        win_xianka_active = True
        layout_xianka = [[sg.Column(
            layout=[[sg.Text('目标机器用户名'), sg.Input(key='user_xk', size=(15, 1), default_text='ubuntu'),
                     sg.Text('目标机器密码'), sg.Input(key='password_xk', password_char='*', size=(15, 1),
                                                       default_text='123..com'),
                     sg.Button('提交用户名密码')],
                    [sg.Multiline(key='-xiankaip-', size=(150, 30), text_color='purple')],
                    [sg.Button('提交IP', size=(8, 1)), sg.Button('测试IP连通性', size=(10, 1)),
                     sg.Button('部署显卡环境', size=(10, 1)), sg.Button('环境检查', size=(8, 1)),
                     sg.Button('显卡压测', size=(8, 1)),
                     sg.Button('检测压测是否正常', size=(14, 1)),
                     sg.Button('开始定时收集日志', size=(14, 1)),
                     sg.Button('停止压测', size=(8, 1)),
                     sg.Button('清空窗口', size=(10, 1), button_color='pink'), ]], element_justification='left')]]
        window_xianka = sg.Window('请输入压测节点IP', layout_xianka)
    if win_xianka_active:
        event_xianka, values_xianka = window_xianka.read(timeout=100)
        if event_xianka in [None, '退出', sg.WIN_CLOSED]:
            win_xianka_active = False
            window_xianka.close()  # 关闭子窗口
        if event_xianka == '提交用户名密码':
            user_xianka = values_xianka['user_xk']
            password_xianka = values_xianka['password_xk']
        if event_xianka == '提交IP':
            end_xian_ip = ''
            xianka_iplist = values_xianka['-xiankaip-'].split('\n')  # 将文本框中的IP格式化为列表
            for i in xianka_iplist:  # 拼接指定格式的字符串 ip,ip,ip...
                if i:
                    i = i + ','
                end_xian_ip += i
            window_xianka['-xiankaip-'].update('')
            com = 'python3' + ' ' + '/root/scripts/xianka_ip.py' + ' ' + 'ip' + ' ' + end_xian_ip
            gui_thread.run_backend(q, com)
        if event_xianka == '测试IP连通性':
            # com = '/root/scripts/for.sh u ss ls'
            com = '/root/scripts/for.sh-new -o u -s ss -u {} -p {} -c ls'.format(user_xianka, password_xianka)
            gui_thread.run_backend(q, com)
        if event_xianka == '部署显卡环境':
            com1 = '/root/scripts/for.sh -o u -s sc -u {} -p {} -c /root/aleo/gpu_deploy/'.format(
                user_xianka, password_xianka)  # 传输安装包
            com2 = "/root/scripts/for.sh -o u -s ss -u {} -p {} -c 'echo 111111 | sudo -S apt update --fix-missing -y &&" \
                   "echo 1111111 | sudo -S apt-get install nvidia-cuda-toolkit g++ make -y'".format(user_xianka, password_xianka)
            com3 = "/root/scripts/for.sh -o u -s ss -u {} -p {} -c 'cd gpu_deploy ; echo 111111 | sudo -S " \
                   "./NVIDIA-3090-Linux-x86_64-515.57.run -a -s --no-x-check; cd ./gpu_burn ; make ; cd ~'".format(user_xianka, password_xianka)
            # 创建两个event
            event1 = threading.Event()
            event2 = threading.Event()
            t1 = gui_thread.run_backend(q, com1, event=event1)
            t2 = gui_thread.run_backend(q, com2, event=event2)
            t3 = gui_thread.run_backend(q, com3, event_list=[event1, event2])  # 该线程检测到event1/2时间即运行
            t1.start()
            t2.start()
            # 最后执行线程3
            t3.start()
        if event_xianka == '环境检查':
            com = "/root/scripts/for.sh -o u -s ss -u {} -p {} -c 'nvidia-smi > /dev/null || echo 驱动安装异常'".format(user_xianka, password_xianka)
            gui_thread.run_backend(q, com)
        if event_xianka == '显卡压测':
            com = "/root/scripts/for.sh -o u -s ss -u {} -p {} -c 'cd gpu_deploy/gpu_burn/  ; nohup ./gpu_burn 10800 > gpu.log 2>&1 &'".format(user_xianka, password_xianka)
            gui_thread.run_backend(q, com)
        if event_xianka == '开始定时收集日志':
            com = "/root/scripts/for.sh -o u -s x -u {} -p {} -c 'nvidia-smi'".format(user_xianka, password_xianka)
            gui_thread.run_backend(q, com)
        if event_xianka == '停止压测':
            com = "/root/scripts/for.sh -o u -s k -u {} -p {} -c 'kill'".format(user_xianka, password_xianka)
            gui_thread.run_backend(q, com)
        if event_xianka == '清空窗口':
            window_xianka['-xiankaip-'].update('')
        while True:
            try:
                msg = q.get_nowait()  # 从线程中读取数据
                window_xianka['-xiankaip-'].print(msg)  # 将日志输出到对应key(xiankaip)的界面上
            except:
                break
    if event == '清空数据库并备份' and not win_ssh_active:
        win_mysql_active = True
        window['-FUNC-A-'].update('')
        layout_mysql_password = [[sg.Text('密码：', size=(10, 1)), sg.InputText(key='-PASSWORD-', password_char='*')],
                                 [sg.Button('提交'), sg.Button('退出')]]
        window_mysql_password = sg.Window('请输入数据库密码',
                                          layout_mysql_password, location=(1200, 300))  # location 定义串口弹出的默认位置
    if win_mysql_active:
        # while True:  # 子窗口和主窗口都激活的情况下，子窗口不进入自己的死循环！子窗口运行时不影响主窗口的事件点击
        event, values = window_mysql_password.read(timeout=100)
        if event in [None, '退出']:
            # break
            win_mysql_active = False
            window_mysql_password.close()  # 关闭子窗口
        if event == '提交':
            password_mysql = values['-PASSWORD-']
            try:
                # result = ssh_command(ip_address='192.168.2.149', username='root', password='123..com', command=
                # '/root/scripts/mysql.sh ' + password_mysql)
                thread = gui_thread.MyThread(ssh_command, ('192.168.2.149', 'root', '123..com',
                                                           '/root/scripts/mysql.sh' + ' ' + password_mysql, None,
                                                           password_mysql))
                thread.setDaemon(True)
                thread.start()  # 启动线程
            except Exception as e:
                result = str(password_mysql) + str(e) + '请再次尝试！'
    if event == 'clear':
        window['-FUNC-A-'].update('')
    # SSH远程登录并执行命令
    if event == '执行远程命令(ssh)' and not win_ssh_active:
        win_ssh_active = True
        layout_ssh = [[sg.Text('用户名：', size=(8, 1)), sg.InputText(key='-USER-')],
                      [sg.Text('密码：', size=(8, 1)), sg.InputText(key='-PASSWORD-', password_char='*')],
                      [sg.Text('IP地址：', size=(8, 1)), sg.InputText(key='-IP-')],
                      [sg.Text('命令：', size=(8, 1)), sg.InputText(key='-COMMAND-')],
                      # [sg.Text('密钥', size=(8, 1)), sg.InputText(key='-密钥-')],
                      [sg.FileBrowse(button_text='密钥选择', key='-密钥-',
                                     file_types=(('All Files', '*.*'), ('Text Files', '*.txt')), size=(8, 1))],
                      [sg.Button('提交'), sg.Button('退出')]]
        window_ssh = sg.Window('SSH远程登录', layout_ssh)
    if win_ssh_active:
        event_ssh, values_ssh = window_ssh.read(timeout=100)
        if event_ssh in [None, '退出']:
            win_ssh_active = False
            window_ssh.close()  # 关闭子窗口
        if event_ssh == '提交':
            window['-SSH-RESULT-'].update('')
            window['-SSH-RESULT-'].update('正在执行远程命令...\n')
            username = values_ssh['-USER-']
            password = values_ssh['-PASSWORD-']
            ip = values_ssh['-IP-']
            command = values_ssh['-COMMAND-']
            key_filename = values_ssh['-密钥-']
            # 执行SSH命令并返回结果
            # 这里需要使用实际的SSH库和函数来执行SSH登录并执行命令
            # 将输出到文本框的操作封装到函数中，启动子线程时直接将结果输出到文本框
            thread = gui_thread.MyThread(ssh_command, (ip, username, password, command))
            # 下面是设置守护线程：如果在程序中将子线程设置为守护线程，则该子线程会在主线程结束时自动退出
            thread.setDaemon(True)
            thread.start()  # 启动线程并将结果输出到文本框
            # window['-SSH-RESULT-'].print(result)
    while True:
        try:
            msg = q.get_nowait()  # 从线程中读取数据
            window['-OUTPUT-'].print(msg)  # 将日志输出到对应key(xiankaip)的界面上
        except:
            break
