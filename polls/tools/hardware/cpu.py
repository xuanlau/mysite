import requests
import bs4
from lxml import etree
import openpyxl
import re

# headers_choice = myHeaders.get_user_agent()
headers = { # 头部信息
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106."
                  "0.0.0 Safari/537.36"
}
# Gecko/20100101 Firefox/70.0"}

def get_html(url, headers):
    " 获取主页html信息 "
    res = requests.get(url=url, headers=headers, cookies=cookie_dict)
    res.encoding = "gbk"
    return res.text


def get_htmlinfo(html):
    "获取页面文字信息"
    # soup = bs4.BeautifulSoup(html, "html.parser")
    et_html = etree.HTML(html)
    cpuinfo = et_html.xpath("//div[@class='pro-intro']/h3/a/text()")
    print(cpuinfo)
    chacaoinfo = et_html.xpath("//div[@class='pro-intro']/div/span/em/text()")
    print(chacaoinfo)


if __name__ == "__main__":
    # url = "http://jobs.51job.com/beijing-ftp/114540578.html"
    url = "https://zj.zol.com.cn/"
    url1 = "https://zj.zol.com.cn/proFilter/sub28_m_gnoPrice__k_1_1_1.html?&time=28"
    headers = {  # 头部信息
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106."
                      "0.0.0 Safari/537.36"
    }
    cookie = 'ip_ck=4sWG4f/+j7QuNTI3NjU5LjE2NDk0MDAzNDk%3D; Hm_lvt_ae5edc2bc4fc71370807f6187f0a2dd0=165" \
             "6672205; lv=1675323166; vn=4; z_pro_city=s_provice%3Dbeijing%26s_city%3Dbeijing; userPr" \
             "ovinceId=1; userCityId=0; userCountyId=0; userLocationId=1; realLocationId=1; userFidLo" \
             "cationId=1; questionnaire_pv=1675296018; Adshow=2'
    cookie_dict = {i.split("=")[0]:i.split("=")[-1] for i in cookie.split("; ")}
    html = get_html(url1, headers)
    get_htmlinfo(html)
