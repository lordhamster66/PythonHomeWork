#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from io import BytesIO
from django.shortcuts import HttpResponse
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
        if login_obj.is_valid():
            if request.session['CheckCode'].upper() == request.POST.get('check_code').upper():
                username = login_obj.cleaned_data.get("username")
                password = login_obj.cleaned_data.get("password")
                user_obj = models.UserInfo.objects.filter(username=username, password=password).first()
                if user_obj:
                    request.session.clear_expired()  # 将所有Session失效日期小于当前日期的数据删除
                    remember = login_obj.cleaned_data.get("remember")
                    if remember:
                        request.session["username"] = username
                        request.session.set_expiry(2592000)
                else:
                    ret["status"] = False
                    ret["error"] = {"password": [{"code": "invalid", "messages": "密码错误"}]}
            else:
                ret["status"] = False
                ret["error"] = {"check_code": [{"code": "invalid", "messages": "验证码错误"}]}
        else:
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
        ret = {"status": True, "error": None, "data": None}
        register_obj = RegisterForm(request.POST)
        if register_obj.is_valid():
            if request.session['CheckCode'].upper() == request.POST.get('check_code').upper():
                models.UserInfo.objects.create(
                    username=register_obj.cleaned_data.get("username"),
                    password=register_obj.cleaned_data.get("password"),
                    email=register_obj.cleaned_data.get("email")
                )
            else:
                ret["status"] = False
                ret["error"] = {"check_code": [{"code": "invalid", "messages": "验证码错误"}]}
        else:
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
    pass
