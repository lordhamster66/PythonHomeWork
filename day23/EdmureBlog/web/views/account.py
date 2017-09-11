#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import hashlib
from io import BytesIO
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from utils.check_code import create_validate_code
from web.forms import RegisterForm
from web.forms import LoginForm
from utils.encoder import JsonCustomEncoder
from repository import models


def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


def login(request):
    """
    登陆
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        ret = {"status": True, "error": None, "data": None}
        login_obj = LoginForm(request.POST)
        if login_obj.is_valid():  # 登录form验证
            if request.session['CheckCode'].upper() == request.POST.get('check_code').upper():
                username = login_obj.cleaned_data.get("username")  # 获取用户输入的用户名
                password = login_obj.cleaned_data.get("password")  # 获取用户输入的密码
                m_obj = hashlib.md5()  # 获取一个md5加密对象
                m_obj.update(password.encode())
                password = m_obj.hexdigest()  # 加密用户输入的密码
                user_obj = models.UserInfo.objects.filter(username=username, password=password).first()
                if user_obj:
                    request.session.clear_expired()  # 将所有Session失效日期小于当前日期的数据删除
                    request.session["username"] = username  # 创建session
                    remember = login_obj.cleaned_data.get("remember")
                    if remember:  # 用户选择一个月免登录
                        request.session.set_expiry(2592000)  # 设定过期时间在1个月之后
                else:  # 获取不到用户对象，说明密码错误
                    ret["status"] = False
                    ret["error"] = {"password": [{"code": "invalid", "messages": "密码错误"}]}
            else:  # 验证码不通过
                ret["status"] = False
                ret["error"] = {"check_code": [{"code": "invalid", "messages": "验证码错误"}]}
        else:  # form验证不通过
            ret["status"] = False
            ret["error"] = login_obj.errors.as_data()
        result = json.dumps(ret, cls=JsonCustomEncoder)
        return HttpResponse(result)


def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        ret = {"status": True, "error": None, "data": None}  # 定义标准返回格式
        register_obj = RegisterForm(request.POST)  # 实例化注册form对象
        if register_obj.is_valid():  # 注册form验证
            if request.session['CheckCode'].upper() == request.POST.get('check_code').upper():  # 验证码通过
                username = register_obj.cleaned_data.get("username")  # 获取用户输入的用户名
                password = register_obj.cleaned_data.get("password")  # 获取用户输入的密码
                email = register_obj.cleaned_data.get("email")  # 获取用户输入的邮箱
                m_obj = hashlib.md5()  # 获取一个md5加密对象
                m_obj.update(password.encode())
                password = m_obj.hexdigest()  # 加密用户输入的密码
                models.UserInfo.objects.create(
                    username=username,
                    password=password,
                    email=email
                )  # 创建用户
            else:  # 验证码不通过
                ret["status"] = False
                ret["error"] = {"check_code": [{"code": "invalid", "messages": "验证码错误"}]}  # 返回验证码错误信息
        else:  # form验证不通过
            ret["status"] = False
            ret["error"] = register_obj.errors.as_data()
        result = json.dumps(ret, cls=JsonCustomEncoder)
        return HttpResponse(result)


def logout(request):
    """
    注销
    :param request:
    :return:
    """
    request.session.delete(request.session.session_key)
    return redirect("/")
