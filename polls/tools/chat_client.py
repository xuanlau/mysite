import os
import uuid
import time
import threading
from socket import *
from tkinter import *

serverName = '211.93.22.166'#服务器外网IP
serverPort = 12001

root = Tk()
root.title('聊天室')

text = Text(root,width = 100,height = 20)

scroll = Scrollbar(root)
scroll.pack(side = RIGHT,fill = Y)
scroll.config(command = text.yview)
text.config(yscrollcommand = scroll.set)
text.pack()

entry = Entry(root,bd = 5,width = 70)
entry.pack(side = LEFT)
entry2 = Entry(root,bd = 5,width = 20)

clientSocket = socket(AF_INET, SOCK_STREAM)
print('正在连接...')
clientSocket.connect((serverName, serverPort))
print('连接成功!')

msg = clientSocket.recv(2048)  # 先接收历史记录

if msg.decode() != 'NO_MESSAGE':  # 有历史记录时
    text.insert(END,msg.decode() + '\n----以上是历史记录----\n')
text.see(END)


def get_mac_address():#由于用户名可以随时换，用MAC地址作为标识了
    mac = uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ':'.join([mac[e:e+2] for e in range(0,11,2)])


def timemark():
    timestamp = int(time.time())
    timestr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(timestamp))
    return '[' + timestr + ']'


def send():
    if entry2.get().replace(' ','') == '':
        text.config(state = 'normal')
        text.insert(END,'请输入用户名！\n')
        text.see(END)
        text.config(state = 'disabled')
        return
    if entry.get() == '':
        text.config(state = 'normal')
        text.insert(END,'发送内容不能为空！\n')
        text.see(END)
        text.config(state = 'disabled')
    else:
        clientSocket.send((timemark() + ' ' + get_mac_address() + ' - ' +
                           entry2.get() + '\n    ' + entry.get()).encode())
        entry.delete(0,'end')


button = Button(root,text = 'SEND',command = send)
button.pack(side = RIGHT)

entry2.pack(side = RIGHT)
class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            msg = clientSocket.recv(2048)
            text.config(state = 'normal')
            text.insert(END,msg.decode() + '\n')
            text.see(END)
            text.config(state = 'disabled')
textThread = myThread()
textThread.start()

root.mainloop()
clientSocket.close()
