import os
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives


os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == '__main__':

    # send_mail(
    #     '来自xxx的测试邮件',
    #     '欢迎访问www.liujiangblog.com，这里是刘江的博客和教程站点，本站专注于Python、Django和机器学习技术的分享！',
    #     'xiwangzu_byte@sina.com',   # 发送邮件的人，需要和settings中的一致
    #     ['1129843061@qq.com'],  # 接受邮件的列表
    # )
    # 如下为html格式文本

    subject, from_email, to = '来自www.liujiangblog.com的测试邮件', 'xiwangzu_byte@sina.com', '1129843061@qq.com'
    text_content = '欢迎访问www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！'

    html_content = '<p>欢迎访问<a href="http://127.0.0.1:8000/polls/login" target=blank>127.0.0.1:8000/polls/login</a>，这里是刘旋</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


