import PySimpleGUI as sg

layout = [[sg.Text('初始文本', key='-TEXT-')],
          [sg.Button('更新文本'), sg.Button('退出')]]

window = sg.Window('示例窗口', layout)

while True:
    event, values = window.read(timeout=0)

    if event == sg.WINDOW_CLOSED or event == '退出':
        break
    elif event == '更新文本':
        # 更新文本内容
        window['-TEXT-'].update('更新后的文本')

    # 手动刷新界面
    window.refresh()

window.close()