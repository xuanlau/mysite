import hashlib
import json
import os

from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from polls.tools import *  # 导入自己写的模块tools
from . import form
from . import models
from .models import Question

# Create your views here.  # 创建视图
dict_args = {}


# 通用视图使用


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question  # 每个通用视图需要知道它将作用于哪个模型。 这由 model 属性提供
    template_name = 'polls/detail.html'  # template_name 属性是用来告诉 Django 使用一个指定的模板名字，而不是自动生成的默认名字。


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # try:
    for choice in question.choice_set.all():
        money = request.POST.get(str(choice.id), None)  # 获取表单数据
        selected_choice = question.choice_set.get(pk=choice.id)  # 获取该分类的子类选项 pk= 为主键
        selected_choice.votes += int(money)  # 记账增加
        selected_choice.save()  # 记账保存
    return HttpResponseRedirect(
        reverse('polls:results', args=(question.id,)))  # 重定向后将进入polls:results对应的视图，并将question.id传递给它


# selected_choice = question.choice_set.get(pk=request.POST['choice'])
# except (KeyError, Choice.DoesNotExist):
# return render(request, 'polls/detail.html', {
#     'question': question,
#     'error_message': "You didn't select a choice.",
# })
# else:
#     selected_choice.votes += 1
#     selected_choice.save()
#     return HttpResponseRedirect(
#         reverse('polls:results', args=(question.id,)))  # 重定向后将进入polls:results对应的视图，并将question.id传递给它
# return HttpResponse("You're voting on question %s." % question_id)


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def zhuye(request):
    if not request.session.get('is_login', None):
        return HttpResponseRedirect("/polls/login/")
    return render(request, 'polls/zhuye.html')


def lo_gin(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return HttpResponseRedirect('/polls/index/')
    """
    新登录界面
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if request.method == 'GET':
        uf = form.UserForm()
        return render(request, 'polls/login_new.html', {'uf': uf, 'nowtime': nowtime})
    """
    request.session.set_expiry(0)  # 设置用户登录超时时间
    if request.method == 'POST':
        login_form = form.UserForm(request.POST)
        message = '请检查填写的内容！'
        if not login_form.is_valid():
            return render(request, 'polls/login.html', locals())
        else:
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            # print(username, password)
            try:
                user = models.User_info.objects.get(name=username)
            except:
                message = '用户不存在！'
                return render(request, 'polls/login.html', locals())
                # return HttpResponseRedirect('polls/login/')
            # 与数据库中的密码的哈希值进行比较
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return HttpResponseRedirect('/polls/index/')  # 跳转到主页
            else:
                message = '密码不正确！'
                return render(request, 'polls/login.html', locals())

    login_form = form.UserForm()
    return render(request, 'polls/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return HttpResponseRedirect('/polls/index/')

    if request.method == 'POST':
        register_form = form.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'polls/register.html', locals())
            else:
                same_name_user = models.User_info.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'polls/register.html', locals())
                same_email_user = models.User_info.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'polls/register.html', locals())
                # 检查注册信息合法后， 插入注册信息到数据库
                new_user = models.User_info()
                new_user.name = username  # 注册用户名到数据库
                new_user.password = hash_code(password1)  # 密码以哈希值得形式插入数据库
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                # code = make_confirm_string(new_user)
                # send_email(email, code)

                return HttpResponseRedirect('/polls/login/')
        else:
            return render(request, 'polls/register.html', locals())
    register_form = form.RegisterForm()
    return render(request, 'polls/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return HttpResponseRedirect("/polls/login/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return HttpResponseRedirect("/polls/login/")


def file_server_login(request):
    if not request.session.get('is_login', None):
        return HttpResponseRedirect("/polls/login/")
    return render(request, 'polls/filelogin.html')


def filelist(request):
    if not request.session.get('is_login', None):
        return HttpResponseRedirect("/polls/login/")
    if request.method == 'POST':
        dict_args["hostname"] = request.POST.get("hostname", None)
        dict_args["user"] = request.POST.get("user", None)
        dict_args["password"] = request.POST.get("password", None)
        dict_args["port"] = int(request.POST.get("port", None))
        dict_args["key"] = request.FILES.get("key", None)
        if dict_args["key"]:
            key_path = os.path.join(os.getcwd(), dict_args["key"].name)  # 拼接密钥文件的保存路径
            key_data = open(key_path, 'wb+')  # 打开文件流
            for chunk in dict_args["key"].chunks():  # 分块写入文件
                key_data.write(chunk)
            key_data.close()
            dict_args["key"] = key_path
    file_list_ = ssh.lx_ssh(dict_args)  # 实例化lx_ssh
    try:
        file_list_.chu_shi_hua_sftp()  # 初始化sftp客户端
    except Exception as e:
        return render(request, 'polls/502.html', {"e": e})
    file_list = file_list_.lx_sftp_client(remote_dir="/")  # 返回三个返回值，目录，文件，路径
    file_list_.close()
    return render(request, 'polls/filelist.html', {"dic_list": file_list[0], "file_list": file_list[1],
                                                   "path": file_list[2], "ipaddr": file_list[3]})


# 递归实现浏览服务器上的目录和文件
def filenewlist(request, path_name, endname):
    if not request.session.get('is_login', None):
        return HttpResponseRedirect("/polls/login/")
    print(dict_args["hostname"])
    try:
        dict_args["hostname"]
    except:
        return render(request, 'polls/502.html', {"e": "登录信息失效"})
    file_list_ = ssh.lx_ssh(dict_args)  # 实例化lx_ssh
    file_list_.chu_shi_hua_sftp()  # 初始化sftp客户端
    file_list = file_list_.lx_sftp_client(remote_dir=path_name + endname + "/")  # 返回三个返回值，目录，文件，路径
    file_list_.close()
    return render(request, 'polls/filelist.html', {"dic_list": file_list[0], "file_list": file_list[1],
                                                   "path": file_list[2], "ipaddr": file_list[3]})


def exit_sftp(request):
    if not request.session.get('is_login', None):
        return HttpResponseRedirect("/polls/login/")
    dict_args["hostname"] = ''
    print(dict_args)
    return HttpResponseRedirect("/polls/filelogin/")
    # auth.logout(request)


def get_vs_pt(request):
    if not request.session.get('is_login', None):
        return HttpResponseRedirect("/polls/login/")
    return render(request, "polls/getvcpt.html")


def vc_pt(request):
    if not request.session.get('is_login', None):
        return HttpResponseRedirect("/polls/login/")
    if request.GET.get('password', None):  # None 为默认值，取不到值时为None值
        cmd = "/root/scripts/mysql.sh" + ' ' + request.GET.get('password', None)
        # os.system(cmd)
        vs_pt = ssh.lx_ssh(**{"hostname": "192.168.2.149", "user": "root", "password": "123..com", "key": None})
        vs_pt.lx_ssh_client(cmd)
        return HttpResponse("已清除数据并备份！")
    try:
        vs_pt = ssh.lx_ssh(**{"hostname": "127.0.0.1", "user": "root", "password": "123..com", "key": None})
        res = vs_pt.lx_ssh_client("/root/scripts/test.sh")
        # res = os.system("/root/scripts/ping.sh")
        res = res.split("\n")
    except:
        res = ["请求出错，请检查网络连接！"]
        # res = ['德玛西亚', '艾欧尼亚', '祖安狂人']
    # print(res)
    # return HttpResponse(res)  # 只响应返回一个字符串，不参与渲染模板
    return JsonResponse(res, safe=False)  # 返回响应一个json对象


def formatdisk(request):
    if not request.session.get('is_login', None):
        return HttpResponseRedirect("/polls/login/")
    if request.method == 'POST':
        format_disk_form = form.FormatDisk(request.POST)
        message = '请检查填写的内容！'
        if format_disk_form.is_valid():
            server_numbers = format_disk_form.cleaned_data.get('server_numbers')
            print(server_numbers)
            return render(request, "polls/formatdisk.html", locals())  # locals () 函数会以字典类型返回当前位置的全部局部变量
    format_disk_form = form.FormatDisk()  # 如果不是POST请求，直接渲染页面
    return render(request, "polls/formatdisk.html", locals())


def getMonitor(request):
    if not request.session.get('is_login', None):
        return HttpResponseRedirect("/polls/login/")
    monitor_dict = {}
    return render(request, 'polls/Monitor.html', monitor_dict)


def serverList(request):
    # 服务器列表
    if not request.session.get('is_login', None):
        return HttpResponseRedirect("/polls/login/")
    if request.method == "POST":
        # print(request.POST.get('pageSize'))
        vs_pt = ssh.lx_ssh(**{"hostname": "127.0.0.1", "user": "root", "password": "123..com", "key": None})
        res = vs_pt.lx_ssh_client("cd /root/scripts && ./for.sh c sss get")
        res = res.split("\n")
        # 两次请求，影响速度
        all_records_count = vs_pt.lx_ssh_client("cd /root/scripts && ./for.sh c sss get |wc -l").split("\n")[0]
        # all_records_count = res[-1]  # 优化获取速度
        response_data = {'total': all_records_count, 'rows': []}  # row键对应一个数组，该数组为一个列表，该列表每个元素为一个字典
        for server_li in res[:-2]:
            response_data['rows'].append({
                "id": server_li.split()[0] if server_li.split()[0] else "",
                "hostname": server_li.split()[1] if server_li.split()[1] else "",
                "IP": server_li.split()[2] if server_li.split()[2] else "",
                "Mem": server_li.split()[3] if server_li.split()[3] else "",
                "CPU": server_li.split()[4] if server_li.split()[4] else "",
                "CPUS": server_li.split()[5] if server_li.split()[5] else "",
                "OS": server_li.split()[6] if server_li.split()[6] else "",
                "virtual1": server_li.split()[7] if server_li.split()[7] else "",
                "status": server_li.split()[8] if server_li.split()[8] else "",
            })
        return HttpResponse(json.dumps(response_data))
    return render(request, 'polls/serverlist.html')


def bzPerf(request):
    if not request.session.get('is_login', None):
        return HttpResponseRedirect("/polls/login/")
    if request.method == 'POST':
        perf = form.autoArrMinionForm(request.POST)
        if perf.is_valid():
            os_type = request.POST.get('select')
            cpu_time = perf.cleaned_data.get('cpu_time')
            mem_time = perf.cleaned_data.get('mem_time')
            disk_time = perf.cleaned_data.get('disk_time')
            # command_str = "/root/scripts/replace.sh " + str(os_type) + ' ' + str(cpu_time) + ' ' + str(mem_time) +
            # ' ' +\ str(disk_time)
            command_str_test = "cat /root/scripts/replace.sh"
            bz_perf = ssh.lx_ssh(**{"hostname": "127.0.0.1", "user": "root", "password": "123..com", "key": None})
            result = bz_perf.lx_ssh_client(command_str_test)  # 测试
            # result = command_str
        return render(request, 'polls/bzperf.html', locals())

    perf = form.autoArrMinionForm()
    result = "朝着梦想前进！"
    return render(request, 'polls/bzperf.html', locals())


def userList(request):
    if not request.session.get('is_login', None):
        return HttpResponseRedirect("/polls/login/")
    '''
    用户列表
    '''
    # if id != 1:
    #     models.User_info.objects.filter(id=id).delete()
    users = models.User_info.objects.all()  # 导入User表
    after_range_num = 2  # 当前页前显示2页
    befor_range_num = 2  # 当前页后显示2页
    try:  # 如果请求的页码少于1或者类型错误，则跳转到第1页
        page = int(request.GET.get("page", 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    paginator = Paginator(users, 11)  # 每页显示11
    try:  # 跳转到请求页面，如果该页不存在或者超过则跳转到尾页
        users_list = paginator.page(page)
    except(EmptyPage, InvalidPage, PageNotAnInteger):
        users_list = paginator.page(paginator.num_pages)
    if page >= after_range_num:
        page_range = paginator.page_range[page - after_range_num:page + befor_range_num]
    else:
        page_range = paginator.page_range[0:int(page) + befor_range_num]
    return render(request, 'polls/userlist.html', {'user_list': users_list, 'page_range': page_range})


def userAlter(request):
    if not request.session.get('is_login', None):
        return HttpResponseRedirect("/polls/login/")
    user_alter = form.AlterForm(request.POST)
    if request.method == "POST":
        if user_alter.is_valid():
            alter_data = user_alter.cleaned_data
            print(alter_data)
            alter_email = alter_data.get('alter_email')
            alter_isactive = alter_data.get('alter_isactive')
            alt = models.User_info.objects.get(id=id)
            alt.email = alter_email
            alt.is_active = alter_isactive
            alt.save()
            return HttpResponseRedirect('/polls/user/list/')
        else:
            errors = user_alter.errors
            return render(request, 'polls/useralter.html', {'alter_FormInput': user_alter, 'errors': errors})
    else:
        try:
            UpdateUser = models.User_info.objects.only('username').get(id=id).username
            old_eamil = models.User_info.objects.only('email').get(id=id).email
            old_is_active = models.User_info.objects.only('is_active').get(id=id).is_active
            if old_is_active:
                old_is_active = 1
            else:
                old_is_active = 0

            form = form.AlterForm(
                initial={'alter_email': old_eamil}
            )
            return render(request, 'polls/useralter.html', {'alter_FormInput': form, 'UpdateUser': UpdateUser, 'alter_is_active':old_is_active})
        except:
            post = get_object_or_404(models.User_info, id=id)
            endform = form.AlterForm(instance=post)
            return render(request, 'polls/useralter.html', {'form': endform})
