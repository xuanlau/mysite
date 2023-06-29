import sys
import openpyxl
import datetime


def create_xlsx(info):
    now = datetime.datetime.now()
    file_name = now.strftime("%Y-%m-%d-%H-%M-%S")
    # 创建一个新的Excel工作簿
    wb = openpyxl.Workbook()
    # 使用默认活动表（sheet1）
    ws = wb.active
    # 打开txt文件并读取其中的内容
    with open(info, 'r') as f:
        lines = f.readlines()
    # 遍历每一行数据
    for i, line in enumerate(lines):
        # 以制表符为分隔符，将每一行数据分割成多个字段，并返回一个列表
        line = line.replace('[0m', '').replace('[32m', '').replace('|', '').replace(' / ', '/')
        fields = line.split()
        # 将每个字段填写到对应的单元格中
        for j, field in enumerate(fields):
            ws.cell(row=i + 1, column=j + 1, value=field)
    # 将表格保存为Excel文件
    wb.save("./" + file_name + '.xlsx')


def write_list_to_file(lst):
    # 写入IP到文件里
    with open('/root/scripts/ip', 'w') as f:
        for item in lst:
            f.write('{}\n'.format(item))


# 通过命令行传入列表参数并写入到文件中
if __name__ == '__main__':
    args = sys.argv[:]
    if args[1] == 'ip':
        info = args[2].split(',')[0:-1]
        write_list_to_file(info)
    elif args[1] == 'xlsx':
        info = args[2]
        create_xlsx(info)
    else:
        print('err, there are some errors, check it please!')
        sys.exit(0)
