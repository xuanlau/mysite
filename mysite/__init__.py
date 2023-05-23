import pymysql
# import os
# os.popen("ssh -t -t -L 3306:10.50.50.10:3306 -o ServerAliveInterval=60 root@211.93.22.166 -i ~/.ssh/pfsrsa")
# os.popen("ssh -t -t -L 88:10.50.50.10:22 -o ServerAliveInterval=60 root@211.93.22.166 -i ~/.ssh/pfsrsa")
pymysql.install_as_MySQLdb()

