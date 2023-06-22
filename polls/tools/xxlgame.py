import random
import PySimpleGUI as sg

# 设置游戏区域尺寸和小图标列表
ROW = 8
COL = 8
ICONS = ["*", "o", "x", "^", "#", "%"]

# 初始化游戏区域
board = []
for i in range(ROW):
    row = [random.choice(ICONS) for j in range(COL)]
    board.append(row)


# 定义消除函数
def eliminate(board, x1, y1, x2, y2):
    if board[x1][y1] != board[x2][y2]:
        return False
    dx = x1 - x2
    dy = y1 - y2
    if dx != 0 and dy != 0:
        return False
    elif dx == 0:
        start, end = min(y1, y2), max(y1, y2)
        if all(board[x1][j] == "-" for j in range(start + 1, end)):
            for j in range(start, end + 1):
                board[x1][j] = "-"
            return True
    else:
        start, end = min(x1, x2), max(x1, x2)
        if all(board[i][y1] == "-" for i in range(start + 1, end)):
            for i in range(start, end + 1):
                board[i][y1] = "-"
            return True
    return False


# 定义GUI窗口布局
layout = [[sg.Text("消消乐小游戏")],
          [sg.Text("游戏区域：", size=(20, 1)), sg.Text("", key="-BOARD-", size=(40, ROW * 2))],
          [sg.Text("请在下面输入两个坐标，如“2,3 4,5”，空格隔开（坐标从0开始）。")],
          [sg.InputText(key="-POS1-", size=(6, 1)), sg.InputText(key="-POS2-", size=(6, 1)), sg.Button("消除")],
          [sg.Button("重新开始游戏"), sg.Button("退出游戏")]]
input_rows = [[sg.Input(size=(15, 1), pad=(0,0)) for col in range(4)] for row in range(10)]
# 创建GUI窗口并运行游戏
window = sg.Window("消消乐小游戏", layout + input_rows)
while True:
    # 更新游戏区域显示
    board_str = ""
    for row in board:
        row_str = " ".join(row)
        for icon in ICONS:
            row_str = row_str.replace(icon, f"[{icon}]")
        board_str += f"{row_str}\n"
    window["-BOARD-"].update(board_str)

    # 获取用户输入
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "退出游戏":
        break
    elif event == "消除":
        try:
            x1, y1 = map(int, values["-POS1-"].strip().split(","))
            x2, y2 = map(int, values["-POS2-"].strip().split(","))
        except:
            sg.popup("无效的输入，请重新输入。")
            continue
        if not (0 <= x1 < ROW and 0 <= y1 < COL and 0 <= x2 < ROW and 0 <= y2 < COL):
            sg.popup("坐标超出范围，请重新输入。")
            continue
        if eliminate(board, x1, y1, x2, y2):
            sg.popup("消除成功！")
        else:
            sg.popup("无法消除，请重新输入。")

    # 判断是否重新开始游戏
    if event == "重新开始游戏":
        board = []
        for i in range(ROW):
            row = [random.choice(ICONS) for j in range(COL)]
            board.append(row)

window.close()