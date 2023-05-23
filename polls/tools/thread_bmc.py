from threading import Thread
import time
import openpyxl
import datetime
from retrying import retry
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait


def h3c(start, end):
    # 临时生成发放：先生成合并单元格表格，在生成信息表格， 最后合并起来，最后调整表格
    # ws = openpyxl.Workbook()
    # wb = ws.active
    for ip in range(start, end):
        read_ip = '192.168.0.' + str(ip)
        # print(read_ip)
        try:
            browser.get('https://' + read_ip + '/#login')
            # browser.maximize_window()
            time.sleep(2)
        except:
            continue
        browser.find_element(By.ID, 'details-button').click()
        browser.find_element(By.ID, 'proceed-link').click()
        time.sleep(5)
        browser.find_element(By.ID, 'login-username').send_keys('admin')
        browser.find_element(By.ID, 'login-password').send_keys('Password@_')
        # @retry(wait_fixed=10, stop_max_attempt_number=1)
        time.sleep(7)
        browser.find_element(By.CLASS_NAME, 'btn-login').click()
        time.sleep(4)
        tancchuang_btn = browser.find_element(By.CLASS_NAME, 'aui_state_highlight')
        # browser.find_element(By.CLASS_NAME, 'aui_state_highlight').click()
        tancchuang_btn.click()
        # alert = browser.switch_to.alert
        # alert.accept()
        time.sleep(5)
        bmcmacs = browser.find_elements(By.XPATH, '//*[@id="mac"]/span')
        for b in bmcmacs:
            # print(b.text)
            if '专用' in b.text:
                print(b.text.split('：')[1])


option = Options()
option.page_load_strategy = 'eager'
driver_path = r"C:\Users\王丽\AppData\Local\Google\Chrome\Application\chrome.exe"
# option.add_experimental_option("detach", True)
browser = webdriver.Chrome(options=option)
start_time = datetime.datetime.now()
# thread_browser()
thead_list = []
t1 = Thread(target=lang_chao, args=(1, 41))
t1.start()
# t2 = Thread(target=h3c, args=(56, 60))
# t2.start()
# t3 = Thread(target=h3c, args=(61, 65))
# t3.start()
# t4 = Thread(target=h3c, args=(66, 72))
# t4.start()
thead_list.append(t1)  # 单线程
# thead_list.append(t2)
# thead_list.append(t3)
# thead_list.append(t4)
for t in thead_list:
    t.join()
end_time = datetime.datetime.now()
print(end_time - start_time)
