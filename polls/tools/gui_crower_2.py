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
                sg.popup(result, title='结果')
        else:
            result = output
    except Exception as e:
        if command == '/root/scripts/mysql.sh ' + str(password_mysql):
            result = password_mysql + str(e) + '请再次尝试！'
            sg.popup(result, title='结果')
        # elif command == '/root/scripts/mysql.sh ' + str(password_mysql):
        #     sg.popup(result, title='结果')
        result = f'Error: {e}'
    finally:
        client.close()
        # 将输出到文本框的操作封装到函数中，启动子线程时直接将结果输出到文本框
    if command == '/root/scripts/ping.sh':
        window['-OUTPUT-'].update('当前无盘环境:\n' + result)
    elif command == '/root/scripts/mysql.sh 123..com True':
        window['-OUTPUT-'].update('当前无盘环境:\n' + result)
    elif command == '/root/scripts/mysql.sh ' + str(password_mysql):
        window['-FUNC-A-'].update(result)
    else:
        window['-SSH-RESULT-'].print(result)
    return result


# 定义登录界面布局


layout_login = [[sg.Text('请登录', font=('宋体', 20), pad=((250, 0), (50, 10)))],
                [sg.Text('用户名：', size=(8, 1)), sg.InputText(key='-USERNAME-')],
                [sg.Text('密码：', size=(8, 1)), sg.InputText(key='-PASSWORD-', password_char='*')],
                [sg.Button('登录', bind_return_key=True), sg.Button('退出')]]

# 定义主界面布局
menu_def = [['File', ['Exit']],
            ['Help', ['About']]]
layout_main = [[sg.Menu(menu_def, tearoff=False)],
               # [sg.InputText(key='-SEARCH-', size=(50, 1), background_color='#FFFFFF', text_color='#663399')],
               [sg.Button('扫描无盘环境', button_color=('white', '#663399')), sg.Button('查询当前数据库IP数量',
                button_color=('white', '#663399')), sg.Button('导出数据库数据(默认当前路径下)',
                                                              button_color=('white', '#663399'))],
               [sg.Multiline(key='-OUTPUT-', size=(80, 10), autoscroll=True)],
               # 文本选择器，先注释
               # [sg.Column([
               #     [sg.Text('导出数据库数据')],
               #     [sg.FileSaveAs(key='-Directoryselection-', size=(10, 1), button_text='选择保存路径')]])],
               # [sg.FolderBrowse(key='-FILESELECTOR-', size=(10, 1)), sg.InputText(key='-MULTI FILEPATH-', size=(50, 1),
               #                                                                    disabled=True)],
               # [sg.Column([
               #     [sg.Text('选择多个文件')],
               #     [sg.FilesBrowse(key='-MULTIFACTORIALLY-', file_types=(('Text Files', '*.txt'), ('All Files', '*.*')),
               #                     size=(10, 1)), sg.InputText(key='-MULTI FILEPATH-', size=(50, 1), disabled=False)]
               # ], element_justification='center', vertical_alignment='top')],  # justification='right' 靠右
               [sg.Column(layout=[[sg.Button('清空数据库并备份', size=(20, 1))],
                [sg.Multiline(key='-FUNC-A-', size=(40, 6))]], element_justification='left'),
                sg.Column(layout=[[sg.Button('执行远程命令(ssh)', size=(20, 1))], [sg.Multiline(key='-SSH-RESULT-',
                                              size=(40, 6))]], element_justification='right')],
               [sg.Text('注：\n1、点击扫描无盘环境可以看到正在压测的IP。\n2、点击清空数据库并备份即可清空数据库并备份。\n3、执行SSH命令需输入用户'
                        '名、密码、IP地址和命令。\n4、点击查询数据库IP，即可查看当前数据库里的IP。\n5、点击导出数据库数据，即可将数据库数据'
                        '导出到当前路径下。\n6、更改PXE系统功能暂不可用', font=('宋体', 13),
                        pad=((0, 0), (30, 0)), text_color='red')],
               [sg.Text('版权所有 ©2023 Crower Inc.。', font=('宋体', 8), pad=((0, 0), (30, 0)))]]

# 创建主窗口
window = sg.Window('Crower', layout_login, element_justification='center', finalize=True)

while True:
    event, values = window.read(timeout=100)
    if event in (None, '退出', 'Exit'):
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
        # result = ssh_command(ip_address='192.168.2.149', username='root', password='123..com',
        #                      command='/root/scripts/ping.sh', key_filename=None)d
        thread = gui_thread.MyThread(ssh_command, ('192.168.2.149', 'root', '123..com', '/root/scripts/ping.sh',
                                                   None))  # 将获取返回值并输出到文本框的操作封装到函数中，启动子线程时直接将结果输出到文本框
        thread.setDaemon(True)  # True主线程运行结束时不对这个子线程进行检查而直接退出
        thread.start()  # 启动线程
        # window['-OUTPUT-'].update('当前无盘环境:\n' + result)
        # window['-OUTPUT-'].print(result)
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
               [sg.Combo(['centos7.6', 'centos7.9', 'ubuntu20.04.4', 'ubuntu20.04.5'], default_value='centos7.6',
                         key='-OS-'), sg.Button('提交')],]
    if event == '清空数据库并备份':
        result = ''
        window['-FUNC-A-'].update(result)
        layout_mysql_password = [[sg.Text('密码：', size=(10, 1)), sg.InputText(key='-PASSWORD-', password_char='*')],
                                 [sg.Button('提交'), sg.Button('退出')]]
        window_mysql_password = sg.Window('请输入数据库密码',
                                          layout_mysql_password, location=(1200, 300))  # location 定义串口弹出的默认位置
        while True:
            event, values = window_mysql_password.read()
            if event in [None, '退出']:
                break
            if event == '提交':
                password_mysql = values['-PASSWORD-']
                try:
                    # result = ssh_command(ip_address='192.168.2.149', username='root', password='123..com', command=
                    # '/root/scripts/mysql.sh ' + password_mysql)
                    thread = gui_thread.MyThread(ssh_command, ('192.168.2.149', 'root', '123..com',
                             '/root/scripts/mysql.sh' + ' ' + password_mysql, None, password_mysql))
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
