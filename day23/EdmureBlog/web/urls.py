"""EdmureBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from .views import home
from .views import account

urlpatterns = [
    url(r'^login.html$', account.login),  # 登录
    url(r'^register.html$', account.register),  # 注册
    url(r'^logout.html$', account.logout),  # 注销
    url(r'^check_code.html$', account.check_code),  # 获取验证码
    url(r'^(?P<site>\w+).html', home.home),  # 某人博客首页
    url(r'^(?P<site>\w+)/(?P<condition>((tag)|(date)|(category)))/(?P<val>\w+-*\w+).html', home.filter),  # 博文过滤
    url(r'^(?P<site>\w+)/(?P<nid>\d+).html', home.detail),  # 博文详细页面
    url(r'^', home.index),  # 博客首页
]
