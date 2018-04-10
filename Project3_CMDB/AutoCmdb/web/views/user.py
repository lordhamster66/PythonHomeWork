#!/usr/bin/env python
# -*- coding:utf-8 -*-
import hashlib
from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse

from web.service import user
from web.forms import UserProfileForm
from repository import models


class UserListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_list.html')


class UserJsonView(View):
    def __init__(self, **kwargs):
        self.obj = user.User()
        super(UserJsonView, self).__init__(**kwargs)

    def get(self, request):
        response = self.obj.fetch_queryset(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = self.obj.delete_queryset(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = self.obj.put_queryset(request)
        return JsonResponse(response.__dict__)


class AddUserView(View):
    def get(self, request, *args, **kwargs):
        form_obj = UserProfileForm()
        return render(request, 'add_user.html', {
            "form_obj": form_obj,
        })

    def post(self, request):
        form_obj = UserProfileForm(request.POST)
        if form_obj.is_valid():
            m_obj = hashlib.md5()
            form_obj.cleaned_data.pop("password_again")  # 去掉确认密码
            password = form_obj.cleaned_data.get("password")  # 获取用户输入的密码
            m_obj.update(password.encode("utf-8"))
            form_obj.cleaned_data["password"] = m_obj.hexdigest()
            data_dict = form_obj.cleaned_data
            models.UserProfile.objects.create(**data_dict)
            return redirect('/user.html')
        else:
            return render(request, 'add_user.html', {
                "form_obj": form_obj,
            })
