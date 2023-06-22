import PySimpleGUI as sg

# 定义一个选项列表供下拉框选择
options_list = ['选项1', '选项2', '选项3']

# 定义一个布局
layout = [
    [sg.Text('老化环境', font=('微软雅黑', 10), text_color='white', background_color='purple', size=(10, 1),
             justification='center')],
    [sg.Text("系统盘类型", size=(10, 1)), sg.Combo(options_list,
                                     size=(40, 1), default_value=options_list[0], key="-OS_TYPE-")],
    [sg.Text('CPU压测时间'), sg.InputText('', key='input'), sg.Text('秒')],
    [sg.Text('内存压测时间'), sg.InputText('', key='input'), sg.Text('秒')],
    [sg.Text('硬盘压测时间'), sg.InputText('', key='input'), sg.Text('秒')],
]

# 创建窗口
window = sg.Window('复选框、下拉框和带单位输入框示例', layout)

# 循环读取窗口中的事件
while True:
    event, values = window.read()

    # 如果用户关闭了窗口或点击了取消按钮，则退出程序
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    # 如果用户点击了确定按钮，则获取输入框中的值并输出
    if event == 'OK':
        input_value = values['input']
        sg.popup('您输入的是：' + input_value)

window.close()