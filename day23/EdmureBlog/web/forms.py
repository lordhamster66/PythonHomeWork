#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/9/10
from django.forms import Form
from django.forms import fields
from django.forms import widgets
from repository import models
from django.core.exceptions import ValidationError


class LoginForm(Form):
    """登录验证Form"""
    username = fields.CharField(
        error_messages={"required": "用户名不能为空！"}
    )
    password = fields.CharField(
        min_length=6,
        error_messages={
            "required": "密码不能为空！",
            "min_length": "密码至少6位!"
        }
    )

    check_code = fields.CharField(
        min_length=4,
        max_length=4,
        error_messages={
            "required": "验证码不能为空！",
            "min_length": "验证码至少4位!",
            "max_length": "验证码至多4位!",
        }
    )

    remember = fields.CharField(
        required=False
    )

    def clean_username(self):
        """验证用户名"""
        username = self.cleaned_data.get("username")
        user_obj = models.UserInfo.objects.filter(username=username).count()
        if not user_obj:
            raise ValidationError("用户名不存在!", "invalid")
        else:
            return username


class RegisterForm(Form):
    """注册验证Form"""
    username = fields.CharField(
        error_messages={"required": "用户名不能为空！"}
    )
    email = fields.EmailField(
        error_messages={
            "required": "邮箱不能为空！",
            "invalid": "邮箱格式不正确"
        }
    )
    password = fields.CharField(
        min_length=6,
        error_messages={
            "required": "密码不能为空！",
            "min_length": "密码至少6位!"
        }
    )
    confirm_password = fields.CharField(
        min_length=6,
        error_messages={
            "required": "密码不能为空！",
            "min_length": "密码至少6位!"
        }
    )
    check_code = fields.CharField(
        min_length=4,
        max_length=4,
        error_messages={
            "required": "验证码不能为空！",
            "min_length": "验证码至少4位!",
            "max_length": "验证码至多4位!",
        }
    )

    def clean_username(self):
        """验证用户名"""
        username = self.cleaned_data.get("username")
        user_obj = models.UserInfo.objects.filter(username=username).count()
        if user_obj:
            raise ValidationError("用户名已经存在!", "invalid")
        else:
            return username

    def clean(self):
        """总验证"""
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise ValidationError("两次输入的密码不一致!", "invalid")
        else:
            return self.cleaned_data
