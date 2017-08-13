"""MySite URL Configuration

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
from cmdb import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),  # 登录
    url(r'^login_check/', views.login_check),  # 登录检查
    url(r'^index/', views.index),  # 主机管理主页
    url(r'^register/', views.register),  # 注册
    url(r'^register_check/', views.register_check),  # 注册检查
    url(r'^select/', views.select),  # 查询
    url(r'^update/', views.update),  # 更新
    url(r'^insert/', views.insert),  # 添加
    url(r'^delete/', views.delete),  # 删除
    url(r'^init/', views.init),  # 初始化数据库
    url(r'^drop/', views.drop),  # 重置数据库
    url(r'^home/', views.home),  # 首页
]
