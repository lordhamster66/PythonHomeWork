#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2018/4/10
from django.forms import Form
from django.forms import fields
from django.forms import widgets


class UserProfileForm(Form):
    name = fields.CharField(
        label="姓名",
        widget=widgets.Input(attrs={"class": "form-control"}),
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
