import PySimpleGUI as sg
import queue
import threading
import time


# 模拟后端程序并输出日志
def simulate_backend_logging(the_queue):
    for i in range(10):
        msg = f'log message {i}'
        the_queue.put(msg)
        time.sleep(1)


# 创建GUI界面
layout = [
    [sg.Multiline(size=(80, 30), key='-LOG-', autoscroll=True)],
    [sg.Button('Start'), sg.Button('Stop')],
]


# 开始模拟后端程序
def run_backend(queue):
    thread = threading.Thread(target=simulate_backend_logging, args=(queue,))
    thread.start()


# 创建GUI窗口并进入事件循环
queue = queue.Queue()
window = sg.Window(title='Log Viewer', layout=layout, finalize=True)
while True:
    event, values = window.read(timeout=300)

    # 检查是否点击关闭按钮
    if event == sg.WIN_CLOSED:
        break

    # 用户点击Start按钮
    if event == 'Start':
        run_backend(queue)

    # 用户点击Stop按钮
    if event == 'Stop':
        break

    # 从日志队列中读取数据并显示到GUI窗口中
    while True:
        try:
            msg = queue.get_nowait()
            window['-LOG-'].print(msg)
        except:
            break

window.close()