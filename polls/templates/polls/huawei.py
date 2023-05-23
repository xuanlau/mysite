# coding: utf-8
import os
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcph.v1.region.cph_region import CphRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcph.v1 import *

if __name__ == "__main__":

    ak = "X064ZOPRWRIJRFNWJP3J"
    sk = "1qKpcsCbzqwykYMDqT4BpnQrnDntVaPOxGn0vXnl"

    credentials = BasicCredentials(ak, sk)
    client = CphClient.new_builder().with_credentials(credentials).with_region(CphRegion.value_of("cn-east-3")) .build()

def get_listPhonesbody():
    try:
        phone_id = []
        listPhonesbody = []
        filename = "test.txt"
        request = ListCloudPhonesRequest()
        response = client.list_cloud_phones(request)
        f = open(filename, 'w')
        f.write(str(response))
        f = open(filename, 'r')
        a = eval(f.read())
        for i in a.get("phones"):
            phone_id.append(i.get("phone_id"))
        f.close()
        for i in phone_id:
            a = PhoneProperty(phone_id=i)
            listPhonesbody.append(a)
        os.remove(filename)
        return listPhonesbody, phone_id
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)


def install_apk(args, phone_id):
    content = '-t -r '
    if args.find(',') != -1:
        a = args.split(',')
        for i in a:
            content = content + 'obs://test-8cef/' + i + ' '
    else:
        print("输入格式错误！")
        exit(1)
    try:
        request = InstallApkRequest()
        listPhoneIdsbody = phone_id
        request.body = InstallApkRequestBody(
            phone_ids=listPhoneIdsbody,
            content=content,
            command='install'
        )
        response = client.install_apk(request)
        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)


def restart_phone(listPhonesbody, xxx):
    # Restart
    try:
        if xxx == "restart":
            request = RestartCloudPhoneRequest()
            listPhonesbody = listPhonesbody
            request.body = RestartCloudPhoneRequestBody(
                phones=listPhonesbody
            )
        else:
            request = ResetCloudPhoneRequest()
            listPhonesbody = listPhonesbody
            request.body = ResetCloudPhoneRequestBody(
                phones=listPhonesbody
            )
            # response = client.restart_cloud_phone(request)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)


print("""
1.安装apk
2.重启
3.恢复出厂设置
""")
num = input("请输入对应的序号")
if str.isdigit(num):
    if int(num) == 1:
        print("输入你要安装的apk(qq.apk)")
        packer = input("多个请用逗号分割")
        install_apk(packer, get_listPhonesbody()[1])
    elif int(num) == 2:
        try:
            restart_phone(get_listPhonesbody()[0], "restart")
        except Exception as e:
            print("restart错误")
    elif int(num) == 3:
        try:
            restart_phone(get_listPhonesbody()[0], "reset")
        except Exception as e:
            print("reset错误")
else:
    print("请输入正确的序号")