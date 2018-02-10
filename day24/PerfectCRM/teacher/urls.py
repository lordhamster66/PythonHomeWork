"""PerfectCRM URL Configuration

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
from teacher import views

urlpatterns = [
    url(r'^$', views.index, name="teacher_index"),  # 讲师首页
    url(r'^class_taken/$', views.class_taken, name="class_taken"),  # 所带班级
    url(r'^homework_list/$', views.homework_list, name="homework_list"),  # 返回作业列表，这样讲师可以逐一进行下载
]
