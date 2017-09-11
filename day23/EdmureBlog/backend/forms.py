#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/9/11
from django.forms import Form
from django.forms import fields
from django.forms import widgets
from repository import models
from django.core.exceptions import ValidationError


class BaseInfoForm(Form):
    """博主个人信息验证Form"""
    nickname = fields.CharField(
        widget=widgets.TextInput(attrs={
            "class": "form-control",
            "id": "nickname",
            "placeholder": "请输入昵称"
        })
    )
    site = fields.CharField(
        widget=widgets.TextInput(attrs={
            "class": "form-control",
            "id": "blogUrl",
            "placeholder": "如：wupeiqi,则个人博客为http://www.xxx.com/wupeiqi.html"
        })
    )
    theme = fields.CharField(
        widget=widgets.Select(
            attrs={
                "class": "form-control",
                "id": "blogTheme"
            },
            choices=[
                ("1", "默认主题"),
                ("2", "红色火焰"),
                ("3", "嘿嘿哈嘿"),
                ("4", "哈哈哈嘿哈"),
                ("5", "编不出来了"),
            ]
        )
    )
    title = fields.CharField(
        widget=widgets.Textarea(attrs={
            "class": "form-control",
            "id": "blogTitle",
            "style": "min-height: 100px",
            "placeholder": "来一杯鸡汤..."
        })
    )
