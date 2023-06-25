import openpyxl

# 创建一个新的Excel工作簿
wb = openpyxl.Workbook()

# 使用默认活动表（sheet1）
ws = wb.active

# 打开txt文件并读取其中的内容
with open(r'C:\Users\11298\Desktop\1.log', 'r') as f:
    lines = f.readlines()

# 遍历每一行数据
for i, line in enumerate(lines):
    # 以制表符为分隔符，将每一行数据分割成多个字段，并返回一个列表
    fields = line.split()

    # 将每个字段填写到对应的单元格中
    for j, field in enumerate(fields):
        ws.cell(row=i+1, column=j+1, value=field)

# 将表格保存为Excel文件
wb.save(r'C:\Users\11298\Desktop\1.xlsx')
