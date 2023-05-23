import argparse
import requests
from lxml import etree
from requests.adapters import HTTPAdapter
import myHeaders
import html2text
import os


def get_zhuanlan_url(id):  # 获取大分类url信息
    url = "https://blog.csdn.net/" + id
    proxies = {
        "http": "http://211.93.22.166:82",
        "https": "https://211.93.22.166:82"
    }
    headers_choice = myHeaders.get_user_agent()
    header = {
        'User-Agent': headers_choice
    }
    # TODO ssl证书报错，参数 verify=False，同时，requests默认是keep-alive的，可能没有释放，加参数
    sess = requests.Session()
    sess.mount('http://', HTTPAdapter(max_retries=3))
    sess.mount('https://', HTTPAdapter(max_retries=3))
    sess.keep_alive = False  # 关闭多余连接
    response = requests.get(url=url, headers=header, proxies=proxies)
    response.encoding = "utf-8"
    et_html = etree.HTML(response.text)
    csdn_blog_user = et_html.xpath('//*[@id="userSkin"]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[1]/div[1]/text()')[0]
    zhuanlan_urls = et_html.xpath("//*[@id='userSkin']/div[2]/div/div[1]/div/div[3]/div[2]/div/ul//@href")
    response.close()
    return zhuanlan_urls, csdn_blog_user


def get_blog_urls(id):  # 获取小分类url信息
    headers_choice = myHeaders.get_user_agent()
    header = {
        'User-Agent': headers_choice
    }
    blog_urls_end = []
    zhuanlan_urls = get_zhuanlan_url(id)[0]

    for zhuanlan_url in zhuanlan_urls:
        zhuanlan_text = requests.get(url=zhuanlan_url, headers=header)
        zhuanlan_text.encoding = 'utf-8'
        et_html = etree.HTML(zhuanlan_text.text)
        blog_urls = et_html.xpath('//*[@id="column"]/ul//@href')
        zhuanlan_text.close()
        for blog_url in blog_urls:
            blog_urls_end.append(blog_url)
    return blog_urls_end, get_zhuanlan_url(id)[1]


def get_blog_text_end_markdown(id):  # 根据大小类url地址，获取文章内容，转换为markdown格式
    headers_choice = myHeaders.get_user_agent()
    header = {
        'User-Agent': headers_choice
    }
    csdn_blog_user = get_blog_urls(id)[1]
    blog_urls = get_blog_urls(id)[0]
    if not os.path.exists(csdn_blog_user):
        os.mkdir(csdn_blog_user)
    for blog_url in blog_urls:
        blog_text = requests.get(url=blog_url, headers=header)
        blog_text.encoding = 'utf-8'
        et_html = etree.HTML(blog_text.text)
        blog_text_end = et_html.xpath('//*[@id="mainBox"]/main/div[1]')[0]  # 获取指定div或其他的内容
        blog_class_name = et_html.xpath('//*[@id="mainBox"]/main/div[1]/div[1]/div/div[2]/div[2]/div/a[1]/text()')[0]
        blog_name = et_html.xpath('//*[@id="articleContentId"]/text()')[0].replace('/', '')  # 去掉 / 防止路径冲突
        if not os.path.exists(csdn_blog_user + '/' + blog_class_name):
            os.mkdir(csdn_blog_user + '/' + blog_class_name)
        result = etree.tostring(blog_text_end, encoding='utf-8').decode()  # 将指定内容转化为html内容  etree.tostring
        markdown = html2text.html2text(result)  # 转换为markdown格式
        end_path = csdn_blog_user + '/' + blog_class_name + '/' + blog_name
        try:
            with open(end_path + '.md', 'w', encoding='utf-8') as file:  # 写入数据到markdown文件
                file.write(markdown)
        except Exception as e:
            print(e)
            print(end_path + ' 无法下载')
        print(end_path)
        blog_text.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id', dest='id', type=str,  required=True, help='csdn name')
    args = parser.parse_args()
    csdn_id = args.id
    get_zhuanlan_url(csdn_id)
    get_blog_urls(csdn_id)
    get_blog_text_end_markdown(csdn_id)

