#!/bin/bash

echo "开始爬取CPU信息到表格"

python3 cpunew.py 

tar -czvf  cpu.tar.gz *xlsx



echo "爬取完成！"
