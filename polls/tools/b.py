import sys
import xlwt
import time


# 当前的python版本
if sys.version_info >= (3, 0):
    import pymysql as mysql
else:
    import MySQLdb as mysql

# mysql信息
host = '192.168.2.149'
port = 3306
user = 'root'
passwd = '123..com'
db = 'pxe'
charset = 'utf8'

# 连接mysql，获取cursor
conn = mysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
cursor = conn.cursor()
table_list = ['cpu', 'disk', 'hdd', 'mem', 'nvme', 'pcie', 'sign_in', 'ssd']
num = 0
workbook = xlwt.Workbook()


class dump_mysql_data:
    def __init__(self, table_list, cursor):
        self.table_list = table_list
        self.cursor = cursor

    def timemark(self):
        timestamp = int(time.time())
        timestr = time.strftime('%Y%m%d%H%M%S', time.localtime(timestamp))
        return timestr

    def dump_data(self):
        for table in self.table_list:
            count = self.cursor.execute("select * from {table};".format(table=table))
            print(count)

            # 重置游标的位置
            # cursor.scroll(0, mode='absolute')
            # 拿到该条SQL所有结果
            results = self.cursor.fetchall()
            print(results)

            # 拿到该表里面的字段名称
            fields = self.cursor.description
            print(fields)

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
        time_ = self.timemark()
        workbook.save(r'./{time_}-{db}.xlsx'.format(db=db, time_=time_))
