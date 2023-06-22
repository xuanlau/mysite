import PySimpleGUI as sg

data = []

layout = [
    [sg.Button('Add Input'), sg.Column([[sg.Input()] for i in range(len(data) + 1)])],
]

window = sg.Window('Add Inputs', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == 'Add Input':
        data.append('')
        layout = [
            [sg.Button('Add Input'), sg.Column([[sg.Input()] for i in range(len(data) + 1)])],
        ]
        window.close()  # 关闭原窗口
        window = sg.Window('Add Inputs', layout)

window.close()