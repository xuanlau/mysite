from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    # username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}))
    # password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(
    #     attrs={'class': 'form-control', 'placeholder': "Password"}))
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(
        attrs={'id': 'username', 'placeholder': 'User'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'id': 'password', 'placeholder': 'Password'}))
    # captcha = CaptchaField(label='验证码')


class FormatDisk(forms.Form):
    server_numbers = forms.IntegerField(initial=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'autofocus': ''}))


class RegisterForm(forms.Form):

    # 用于select下拉框
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # 重复两次密码
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)   # select下拉框
    # captcha = CaptchaField(label='验证码')


# class BookKeep(forms.Form):
class autoArrMinionForm(forms.Form):
    cpu_time = forms.IntegerField(label='add_minion_ip', max_value=65535, widget=forms.TextInput(
        attrs={'id': 'add_minion_ip', 'name': 'add_minion_ip', 'class': 'form-control', 'value': 300}))
    # add_os_type = forms.ChoiceField(label='系统盘类型', choices=os_type)
    mem_time = forms.IntegerField(label='', max_value=65535, widget=forms.TextInput(
        attrs={'id': 'add_minion_username', 'class': 'form-control', 'value': 1800}))
    disk_time = forms.IntegerField(label='', max_value=65535, widget=forms.TextInput(
        attrs={'id': 'add_minion_password', 'class': 'form-control', 'value': 1800}))  # placeholder设定默认提示


class AlterForm(forms.Form):
    isactive = [
        (0, '禁用'),
        (1, '启用'),
    ]
    alter_email = forms.EmailField(label='add_email', max_length=20, initial='class', widget=forms.TextInput(
        attrs={'id': 'add_email', 'name': 'add_email', 'placeholder': '请输入您的邮箱'}))
    alter_isactive = forms.IntegerField(widget=forms.Select(choices=isactive))
