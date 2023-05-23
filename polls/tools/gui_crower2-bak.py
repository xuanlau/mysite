import time
import os
import socket
import threading
import PySimpleGUI as sg
import paramiko
import gui_thread
import uuid


def ssh_command(ip_address, username, password, command, key_filename=None, password_mysql=None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=ip_address, username=username, password=password, timeout=1, key_filename=key_filename)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if error:
            result = error
            if command == '/root/scripts/mysql.sh ' + password_mysql:
                result = password_mysql + str(error) + '请再次尝试！'
                sg.popup(result, auto_close=True, title='结果')
        else:
            result = output
    except Exception as e:
        if command == '/root/scripts/mysql.sh ' + str(password_mysql):
            result = password_mysql + str(e) + '请再次尝试！'
            sg.popup(result, auto_close=False, title='结果')
        result = f'Error: {e}'
    finally:
        client.close()
        # 将输出到文本框的操作封装到函数中，启动子线程时直接将结果输出到文本框
    if command == '/root/scripts/ping.sh':
        window['-OUTPUT-'].update('当前无盘环境:\n' + result)
    else:
        window['-SSH-RESULT-'].print(result)
    return result


# 接收服务端发送的消息
def recv_msg(sock):
    while True:
        try:
            data = sock.recv(2048)
            # print(data.decode())
            if not data:
                break
                # pass
            # 处理消息
            else:
                # 显示文字消息
                # 即只要在子线程里调用Window对象的write_event_value()方法，主线程监听到子线程发出的事件就更新UI
                window_chat.write_event_value('接受消息', data.decode())  # 必须 放在线程队列里面
        except Exception as e:
            print('尝试重新连接' + str(e))
            break
    # 关闭连接
    sock.close()
    print('断开连接')
    window_chat.write_event_value('-EXIT-', '')


def history_msg():
    history = clientSocket.recv(2048).decode()
    if history:
        print('history')
        window_chat.write_event_value('历史', history)


# 发送消息给服务端
def send_msg(sock, msg):
    # print('this')
    sock.sendall(msg.encode())


def get_mac_address():  # 由于用户名可以随时换，用MAC地址作为标识了
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ':'.join([mac[e:e + 2] for e in range(0, 11, 2)])


def timemark():
    timestamp = int(time.time())
    timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
    return '[' + timestr + ']'

# 定义登录界面布局


layout_login = [[sg.Text('请登录', font=('宋体', 20), pad=((250, 0), (50, 10)))],
                [sg.Text('用户名：', size=(8, 1)), sg.InputText(key='-USERNAME-')],
                [sg.Text('密码：', size=(8, 1)), sg.InputText(key='-PASSWORD-', password_char='*')],
                [sg.Button('登录', bind_return_key=True), sg.Button('退出')]]

# 定义主界面布局
layout_main = [[sg.Checkbox('legacy', key='-LEGACY-'), sg.Checkbox('uefi', key='-UEFI-'), sg.Button('提交')],
               [sg.Combo(['centos7.6', 'centos7.9', 'ubuntu20.04.4', 'ubuntu20.04.5'], default_value='centos7.6',
                         key='-OS-'), sg.Button('提交')],
               [sg.InputText(key='-SEARCH-', size=(50, 1), background_color='#FFFFFF', text_color='#663399'),
                sg.Button('扫描无盘环境', button_color=('white', '#663399'))],
               [sg.Multiline(key='-OUTPUT-', size=(80, 10), autoscroll=True)],
               [sg.Column([
                   [sg.Text('选择单个文件')],
                   [sg.FileBrowse(key='-FILESELECTOR-', file_types=(('Text Files', '*.txt'), ('All Files', '*.*')),
                                  size=(10, 1)), sg.InputText(key='-FILEPATH-', size=(50, 1), disabled=False)]],
                   element_justification='center', vertical_alignment='top')],
               [sg.Column([
                   [sg.Text('选择多个文件')],
                   [sg.FilesBrowse(key='-MULTIFACTORIALLY-', file_types=(('Text Files', '*.txt'), ('All Files', '*.*')),
                                   size=(10, 1)), sg.InputText(key='-MULTI FILEPATH-', size=(50, 1), disabled=False)]
               ], element_justification='center', vertical_alignment='top')],  # justification='right' 靠右
               [sg.Column(layout=[[sg.Button('清空数据库并备份')], [sg.Button('执行远程命令(ssh)')],
                                  [sg.Button('进入聊天室')]],
                          element_justification='left'),
                sg.Column(layout=[[sg.Multiline(key='-FUNC-A-', size=(50, 5))],
                                  [sg.Multiline(key='-SSH-RESULT-', size=(50, 5))]], element_justification='right')],
               [sg.Text('注：1、点击扫描无盘环境可以看到正在压测的IP。2、点击清空数据库并备份即可清空数据库。3、执行SSH命令需输入用户'
                        '名、密码、IP地址和命令。4、更改PXE系统功能暂不可用', font=('宋体', 10),
                        pad=((0, 0), (20, 0)), text_color='red')],
               [sg.Text('版权所有 ©2023 Crower Inc.。', font=('宋体', 8), pad=((0, 0), (30, 0)))]]

# 创建主窗口
window = sg.Window('Crower', layout_login, element_justification='center', finalize=True)

while True:
    event, values = window.read(timeout=100)
    if event in (None, '退出'):
        break
    # 登录验证
    if event == '登录':
        if values['-USERNAME-'] == 'admin' and values['-PASSWORD-'] == '123..com':
            window.close()
            window = sg.Window('Crower', layout_main, element_justification='center', finalize=True)
        else:
            sg.popup('用户名或密码错误！')
    if event == '扫描无盘环境':
        window['-OUTPUT-'].update('')
        window['-OUTPUT-'].update('正在扫描地址...')
        # sg.popup_auto_close('正在扫描请稍等')
        try:
            # result = ssh_command(ip_address='192.168.2.149', username='root', password='123..com',
            #                      command='/root/scripts/ping.sh', key_filename=None)d
            thread = gui_thread.MyThread(ssh_command, ('192.168.2.149', 'root', '123..com', '/root/scripts/ping.sh',
                                                       None))  # 将获取返回值并输出到文本框的操作封装到函数中，启动子线程时直接将结果输出到文本框
            thread.setDaemon(True)  # True主线程运行结束时不对这个子线程进行检查而直接退出
            thread.start()  # 启动线程
        except Exception as e:
            result = e
        # window['-OUTPUT-'].update('当前无盘环境:\n' + result)
        # window['-OUTPUT-'].print(result)

    if event == '清空数据库并备份':
        result = ''
        window['-FUNC-A-'].update(result)
        layout_mysql_password = [[sg.Text('密码：', size=(10, 1)), sg.InputText(key='-PASSWORD-', password_char='*')],
                                 [sg.Button('提交'), sg.Button('退出')]]
        window_mysql_password = sg.Window('请输入数据库密码',
                                          layout_mysql_password, location=(1200, 300))  # location 定义串口弹出的默认位置
        while True:
            event_password, values_password = window_mysql_password.read()
            if event_password in [None, '退出']:
                break
            if event_password == '提交':
                password_mysql = values_password['-PASSWORD-']
                try:
                    # result = ssh_command(ip_address='192.168.2.149', username='root', password='123..com', command=
                    # '/root/scripts/mysql.sh ' + password_mysql)
                    thread = gui_thread.MyThread(ssh_command, ('192.168.2.149', 'root', '123..com',
                                                               '/root/scripts/mysql.sh ' + password_mysql, None,
                                                               password_mysql))
                    thread.setDaemon(True)
                    thread.start()  # 启动线程
                except Exception as e:
                    result = str(password_mysql) + str(e) + '请再次尝试！'
        window_mysql_password.close()  # 关闭子窗口

    if event == 'clear':
        window['-FUNC-A-'].update('')
    # SSH远程登录并执行命令
    if event == '执行远程命令(ssh)':
        layout_ssh = [[sg.Text('用户名：', size=(8, 1)), sg.InputText(key='-USER-')],
                      [sg.Text('密码：', size=(8, 1)), sg.InputText(key='-PASSWORD-', password_char='*')],
                      [sg.Text('IP地址：', size=(8, 1)), sg.InputText(key='-IP-')],
                      [sg.Text('命令：', size=(8, 1)), sg.InputText(key='-COMMAND-')],
                      # [sg.Text('密钥', size=(8, 1)), sg.InputText(key='-密钥-')],
                      [sg.FileBrowse(button_text='密钥选择', key='-密钥-',
                                     file_types=(('All Files', '*.*'), ('Text Files', '*.txt')), size=(8, 1))],
                      [sg.Button('提交'), sg.Button('退出')]]

        window_ssh = sg.Window('SSH远程登录', layout_ssh)
        while True:
            event_ssh, values_ssh = window_ssh.read()
            if event_ssh in [None, '退出']:
                break
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
                try:
                    thread = gui_thread.MyThread(ssh_command, (ip, username, password, command))
                    # 下面是设置守护线程：如果在程序中将子线程设置为守护线程，则该子线程会在主线程结束时自动退出
                    thread.setDaemon(True)
                    thread.start()  # 启动线程并将结果输出到文本框
                except Exception as e:
                    result = e
                # window['-SSH-RESULT-'].print(result)
        window_ssh.close()  # 关闭子窗口
    if event == '进入聊天室':
        serverName = '211.93.22.166'  # 服务器外网IP
        serverPort = 12001
        # 创建保存图片的目录
        if not os.path.exists("images"):
            os.makedirs("images")
        # 创建PySimpleGUI窗口
        layout_chat = [
            [sg.Multiline(size=(80, 18), key="-OUTPUT-", disabled=True, background_color='#d2b48c',
                          text_color='#fdf4e3')],
            [sg.Input(size=(50, 2), key="-INPUT-"),
             sg.Input(size=(10, 2), key="-USERINPUT-"),
             sg.FileBrowse(file_types=(("JPEG Files", "*.jpg"), ("All Files", "*.*")), key="-BROWSE-"),
             sg.Button("Send", key="-SEND_MSG-")]
        ]
        window_chat = sg.Window("Chat Room", layout_chat, return_keyboard_events=True)
        socket.setdefaulttimeout(0.5)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('正在连接...')
        try:
            clientSocket.connect((serverName, serverPort))
            print('连接成功!')
            thread_his = gui_thread.MyThread(history_msg, ())
            thread_his.setDaemon(True)
            thread_his.start()
            QT_ENTER_KEY1 = 'special 16777220'
            QT_ENTER_KEY2 = 'special 16777221'
            # 启动接收消息的线程
            thread_chat_recv = gui_thread.MyThread(recv_msg, (clientSocket, ))
            thread_chat_recv.setDaemon(True)
            thread_chat_recv.start()
            while True:
                event_chat, values_chat = window_chat.read(timeout=100)
                if event_chat == sg.WIN_CLOSED or event_chat == "-EXIT-":
                    # 关闭连接
                    print(event_chat)
                    # send_msg(clientSocket, "exit")
                    break
                # elif event_chat == "-SEND_MSG-":
                elif event_chat in ('\r', "-SEND_MSG-", QT_ENTER_KEY1, QT_ENTER_KEY2):  # 监听回车事件
                    # 发送消息
                    msg = values_chat["-INPUT-"]
                    msg_user = values_chat['-USERINPUT-']
                    msg_end = (timemark() + ' ' + get_mac_address() + ' - ' + msg_user + '\n    ' + msg)
                    if not values_chat["-INPUT-"]:
                        window_chat['-OUTPUT-'].print("消息不能为空")
                    elif not values_chat["-USERINPUT-"]:
                        window_chat['-OUTPUT-'].print("用户名不能为空")
                    else:
                        # 发送文字消息
                        send_msg(clientSocket, msg_end)
                    window_chat["-INPUT-"].update("")
                elif event_chat == "接受消息":
                    window_chat['-OUTPUT-'].print(values_chat["接受消息"])
                    # print('接收消息')
                elif event_chat == '历史':
                    window_chat['-OUTPUT-'].print(values_chat["历史"])
            print('err')
            # # 关闭窗口
            window_chat.close()
            print('end')
            clientSocket.close()  # 窗口消失，关闭连接
        except Exception as err:
            sg.popup_error(err)
