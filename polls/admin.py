from django.contrib import admin

from .models import Choice, Question, File_Model, User_info, ConfirmString


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  # 默认提供三个足够的选项字段


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),    # 字段标题为None,  question_text字段名
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]   # Choice 对象要在 Question 后台页面编辑， 默认提供 3 个足够的选项字段
    list_display = ('question_text', 'pub_date', 'was_published_recently')   # 一个包含要显示的字段名的元组，在更改列表页中以列的形式展示这个对象：
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.AdminSite.site_header = "What fuck man ?"  # 设置自定义网页标题


class FileAdmin(admin.ModelAdmin):
    list_display = ('upload', 'File_Date')


admin.site.register(File_Model)    # 实现文件上传模型

admin.site.register(User_info)

admin.site.register(ConfirmString)
