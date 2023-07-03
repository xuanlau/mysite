import threading
import time
import sys
import xlwt
import pymysql as mysql
import paramiko

# 当前的python版本
# if sys.version_info >= (3, 0):
#     import pymysql as mysql
# else:
#     import MySQLdb as mysql

# mysql信息
# host = '192.168.2.149'
# port = 3306
# user = 'root'
# passwd = '123..com'
# db = 'pxe'
# charset = 'utf8'

# 连接mysql，获取cursor
# conn = mysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
# cursor = conn.cursor()
# table_list = ['cpu', 'disk', 'hdd', 'mem', 'nvme', 'pcie', 'sign_in', 'ssd']
# workbook = xlwt.Workbook()


class dump_mysql_data:
    def __init__(self, args):
        self.args = args

    def timemark(self):
        timestamp = int(time.time())
        timestr = time.strftime('%Y%m%d%H%M%S', time.localtime(timestamp))
        end_path = r'./{time_}-{db}.xlsx'.format(db=self.args[4], time_=timestr)
        return end_path

    def dump_data(self):
        conn = mysql.connect(host=self.args[0], port=self.args[1], user=self.args[2], passwd=self.args[3], db=
        self.args[4], charset=self.args[5], connect_timeout=1)  # 创建连接并设置超时时间
        cursor = conn.cursor()
        table_list = ['cpu', 'disk', 'hdd', 'mem', 'nvme', 'pcie', 'sign_in', 'ssd']
        workbook = xlwt.Workbook()
        for table in table_list:
            count = cursor.execute("select * from {table};".format(table=table))
            print(count)

            # 重置游标的位置
            # cursor.scroll(0, mode='absolute')
            # 拿到该条SQL所有结果
            results = cursor.fetchall()
            # print(results)

            # 拿到该表里面的字段名称
            fields = cursor.description
            # print(fields)
            sheet = workbook.add_sheet(table, cell_overwrite_ok=True)
            # 写上字段信息
            for field in range(0, len(fields)):
                sheet.write(0, field, fields[field][0])

            # 获取并写入数据段信息
            row = 1
            col = 0
            for row in range(1, len(results) + 1):
                for col in range(0, len(fields)):
                    value = results[row - 1][col]
                    if not value:
                        value = ''
                    sheet.write(row, col, '%s' % value)
        end_path = self.timemark()
        workbook.save(end_path)


# MyThread.py线程类
class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        # super(MyThread,self) 首先找到 MyThread 的父类（就是类 Thread），然后把类 MyThread 的对象转换为类 Thread 的对象
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
        self.result = []

    def run(self):
        # self.result = self.func(*self.args) # 获取线程执行的函数的返回值
        self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception as e:
            return e


def my_backend_logging(q, command, event=None, event_list=None):
    # 如果是等待线程，就先阻塞，等其他线程的threading.Event().set()执行后再运行
    if event_list:
        for t in event_list:
            t.wait()  # 阻塞
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname='192.168.2.149', username='root', password='123..com', timeout=100)
        # stdin、stdout 和 stderr。这三个文件对象分别表示了程序的输入、输出和错误输出流。它们是非阻塞的文件对象，
        # 因此可以采用单独的线程或异步模式管理它们的读写操作。如：q.put(line)
        stdin, stdout, stderr = client.exec_command(command)
        if stdout:
            for line in iter(stdout.readline, ""):
                # 单独的线程来读取stdout, readline默认每一个元素包含一个换行符，所以需要去掉(替换为空)
                q.put(line.replace('[0m', '').replace('[32m', '').replace('\n', ''))
        else:
            for line in iter(stderr.readline, ""):
                q.put(line)
    except Exception as e:
        q.put(e)
    finally:
        q.put('结束')
        client.close()
    # 如果是需要先执行的线程，就执行完后再threading.Event().set()
    if event:
        q.put('daozhi')
        event.set()
    else:
        pass


def run_backend(queue, com, event=None, event_list=None):
    thread = threading.Thread(target=my_backend_logging, args=(queue, com, event, event_list))
    thread.setDaemon(True)  # 设置守护进程，主进程退出后，线程自动退出
    # 这里考虑遇到多个线程时，其中一个线程需要等待另外两个线程执行完后，自己才执行,用到了threading.Event()方法中的set()和wait()
    # 如果没有先后顺序的话，就直接start(),反之，返回一个threading.Thread()对象
    if not event and not event_list:
        thread.start()
    return thread
