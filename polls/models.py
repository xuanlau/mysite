import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateField('Date published', default=timezone.now)

    def __str__(self):
        return self.question_text

    # 是否在当前发布的问卷
    def was_published_recently(self):
        now = timezone.now()
        # now = datetime.datetime.now()
        # return (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d") <= self.pub_date <= now  # 修复能发布未来时间的投票的BUG，
        # return (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d") <= self.pub_date.strftime("%Y-%m-%d") <= now
        return (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d") <= self.pub_date.strftime(
            "%Y-%m-%d") <= now.strftime("%Y-%m-%d")  # 修复因时间格式不一致导致的无法比较的BUG

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class File_Model(models.Model):
    # 文件被传至`MEDIA_ROOT/uploads`目录，MEDIA_ROOT由你在settings文件中设置
    upload = models.FileField(upload_to='upload/', max_length=100)
    # upload = models.FileField(upload_to='uploads/%Y/%m/%d/')    # 人性化的自动生成日期目录
    file_Date = models.DateField('File data', default=timezone.now)  # timezone.now 不需要括号


# 创建用户模型，admin.py注册该模型后，可后台管理用户增删改查


class User_info(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女")
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User_info', on_delete=models.CASCADE)  # 一对一
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return self.user.objects.name + ":   " + self.code
        return self.user.name + ":   " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"



