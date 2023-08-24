import pymysql
import openpyxl

db = pymysql.connect(host="192.168.2.149", user="root", passwd="123..com",
                     database="pxe", charset="utf8")

cursor = db.cursor()  # 数据库交互状态链接

sql = "select * from cpu;"

cursor.execute(sql)

res = cursor.fetchall()

for i in res:
    for j in i:
        print(j)

db.commit()

cursor.close()

db.close()

