from django.urls import path
import mysite.settings
from . import views

app_name = 'polls'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.lo_gin, name='login'),
    path('login/', views.lo_gin, name='login'),
    path('index/', views.zhuye, name='zhuye'),
    path('user/list/', views.userList, name='user_list'),
    path('user/list/(.+)/', views.userList, name='user_listcc'),
    path('user/', views.userList),
    path('user/alter/(.+)/', views.userAlter, name='user_alter'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('toupiao/', views.IndexView.as_view(), name='toupiao'),
    path('filelogin/', views.file_server_login, name='filelogin'),
    path('filelist/', views.filelist, name='filelist'),
    path('filelist<path:path_name><str:endname>/', views.filenewlist,
         name='filenewlist'),
    path('fileexit/', views.exit_sftp, name='fileexit'),
    path('getvcpt/', views.get_vs_pt, name='getvcpt'),
    path('formatdisk/', views.formatdisk, name='formatdisk'),
    path('vcpt/', views.vc_pt, name='vcpt'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name="results"),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('cmdb/monitor/', views.getMonitor, name='monitor'),
    path('cmdb/serverlist/', views.serverList, name='server_list'),
    path('cmdb/serverlist/(.+)/', views.serverList, name='server_listcc'),
    path('cmdb/bzperf/', views.bzPerf, name='bz_Perf'),
    # path('^cmdb/hostadmin/$', views.hostAdmin, name='hostadmin'),
    # path('^cmdb/monitor/$', views.getMonitor, name='monitor'),
    # path('^cmdb/$', views.serverList),
    # path('^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': mysite.settings.STATIC_ROOT}),
]


# 类视图，实现view视图的重用

# urlpatterns = [
#     path('', views.IndexView.as_view(), name='index'),
#     path('<int:pk>/', views.DetailView.as_view(), name='detail'),
#     path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]
