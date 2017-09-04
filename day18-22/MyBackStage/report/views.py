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
            request.session.clear_expired()  # 清空过期的session
            if login_obj.clean().get("remember", None) == "True":
                request.session["username"] = login_obj.clean().get("username")  # 设置session
            return render(request, "index.html")
        else:
            return render(request, "login.html", {"login_obj": login_obj, "register_obj": register_obj})


def register(request):
    """注册功能"""
    if request.method == "GET":
        msg_dic = {'status': False, 'error': "滚!", 'data': None}  # get请求也拒绝
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
            error = register_obj.errors  # 获取所有的错误信息对象，前端可以通过error.username来获取username的错误信息，其他类似
            msg_dic = {'status': False, 'error': error, 'data': None}  # 返回一个字典，前端可以很方便的处理
            return HttpResponse(json.dumps(msg_dic))
    else:
        msg_dic = {'status': False, 'error': "滚!", 'data': None}  # 其他请求则拒绝
        return HttpResponse(json.dumps(msg_dic))


def index(request):
    """后台首页"""
    if request.method == "GET":
        if request.session.get("username", None):
            return render(request, "index.html")
        else:
            return redirect("/report/login/")
    elif request.method == "POST":
        return HttpResponse("滚！")
    else:
        return HttpResponse("滚！")
