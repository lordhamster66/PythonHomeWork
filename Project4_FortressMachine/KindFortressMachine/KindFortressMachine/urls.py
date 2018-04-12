"""KindFortressMachine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from web import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.acc_login),  # 登录
    url(r'^logout/$', views.acc_logout, name="logout"),  # 注销
    url(r'^$', views.index, name="index"),  # 堡垒机首页
    url(r'^web_ssh/$', views.web_ssh, name="web_ssh"),  # WEB SSH
    url(r'^audit_log/$', views.audit_log, name="audit_log"),  # 审计日志页面
    url(r'^audit_log/(?P<session_id>\d+)/$', views.audit_log_detail, name="audit_log_detail"),  # 详细审计日志
    url(r'^multitask_cmd/$', views.multitask_cmd, name="multitask_cmd"),  # 批量命令
    url(r'^multitask_file/$', views.multitask_file, name="multitask_file"),  # 批量文件
    url(r'^api/multitask/$', views.multitask, name="multitask"),  # 批量任务
    url(r'^api/multitask_ret/$', views.multitask_ret, name="multitask_ret"),  # 获取批量任务结果
    url(r'^api/multitask/upload_file$', views.multitask_upload_file, name="multitask_upload_file"),  # 获取用户上传的文件
]
