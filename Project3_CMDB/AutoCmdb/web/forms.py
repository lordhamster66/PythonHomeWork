#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2018/4/10
import hashlib
from django.forms import Form
from django.forms import fields
from django.forms import widgets
from repository import models


class UserProfileForm(Form):
    name = fields.CharField(
        label="姓名",
        widget=widgets.TextInput(attrs={"class": "form-control"}),
        required=True
    )

    email = fields.EmailField(
        label="邮箱",
        widget=widgets.EmailInput(attrs={"class": "form-control"}),
        required=True,
        error_messages={"invalid": "邮箱格式不正确！"}
    )

    phone = fields.IntegerField(
        label="座机",
        widget=widgets.NumberInput(attrs={"class": "form-control"}),
        required=True,
        error_messages={"invalid": "必须全为数字！"}
    )

    mobile = fields.IntegerField(
        label="手机",
        widget=widgets.NumberInput(attrs={"class": "form-control"}),
        required=True,
        error_messages={"invalid": "必须全为数字！"}
    )

    username = fields.CharField(
        label="用户名",
        widget=widgets.Input(attrs={"class": "form-control"}),
        required=True
    )

    password = fields.CharField(
        label="密码",
        widget=widgets.PasswordInput(attrs={"class": "form-control"}),
        required=True
    )

    password_again = fields.CharField(
        label="确认密码",
        widget=widgets.PasswordInput(attrs={"class": "form-control"}),
        required=True
    )

    def clean_password_again(self):
        password = self.cleaned_data.get("password")
        password_again = self.cleaned_data.get("password_again")
        if password != password_again:
            self.add_error("password_again", "两次密码不一致")
        else:
            return password_again


class LoginForm(Form):
    username = fields.CharField(
        label="用户名",
        widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入用户名"}),
        required=True
    )

    password = fields.CharField(
        label="密码",
        widget=widgets.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入密码"}),
        required=True
    )

    remember = fields.CharField(
        widget=widgets.CheckboxInput(),
        required=False
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user_obj = models.UserProfile.objects.filter(username=username).first()
        if user_obj:
            m_obj = hashlib.md5()
            m_obj.update(password.encode("utf-8"))
            password = m_obj.hexdigest()
            if password != user_obj.password:
                self.add_error("password", "密码错误！")
        else:
            self.add_error("username", "用户名不存在！")
        return self.cleaned_data
