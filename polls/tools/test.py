import os
import datetime
now = datetime.datetime.now()
real_time = now.strftime("%Y-%m-%d-%H:%M:%S")
print(real_time)
print(os.getcwd())