import json
import hashlib
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from report import myforms
from report import models


# Create your views here.


def login(request):
    """登录功能"""
    register_obj = myforms.RegisterForm()  # 获取RegisterForm对象
    if request.method == "GET":
        login_obj = myforms.LoginForm()
        return render(request, "login.html", {"login_obj": login_obj, "register_obj": register_obj})  # 返回登录注册页面
    elif request.method == "POST":
        login_obj = myforms.LoginForm(request.POST)
        if login_obj.is_valid():
            return redirect("/report/index/")
        else:
            return render(request, "login.html", {"login_obj": login_obj, "register_obj": register_obj})


def register(request):
    """注册功能"""
    if request.method == "GET":
        msg_dic = {'status': False, 'error': "滚!", 'data': None}
        return HttpResponse(json.dumps(msg_dic))
    elif request.method == "POST":
        register_obj = myforms.RegisterForm(request.POST)
        if register_obj.is_valid():
            username = register_obj.cleaned_data.get("username")
            pwd = register_obj.cleaned_data.get("pwd")
            qq = register_obj.cleaned_data.get("qq")
            m_obj = hashlib.md5()
            m_obj.update(pwd.encode())
            pwd = m_obj.hexdigest()
            models.User.objects.create(username=username, pwd=pwd, qq=qq)
            msg_dic = {'status': True, 'error': None, 'data': None}
            return HttpResponse(json.dumps(msg_dic))
        else:
            error = register_obj.errors
            msg_dic = {'status': False, 'error': error, 'data': None}
            return HttpResponse(json.dumps(msg_dic))
    else:
        msg_dic = {'status': False, 'error': "滚!", 'data': None}
        return HttpResponse(json.dumps(msg_dic))


def index(request):
    """后台首页"""
    return HttpResponse("Welcome")
