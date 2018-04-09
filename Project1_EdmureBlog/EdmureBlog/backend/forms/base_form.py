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
                ("default", "默认主题"),
                ("warm", "温暖"),
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


class TagForm(Form):
    tagname = fields.CharField(
        widget=widgets.TextInput(attrs={
            "class": "form-control",
            "id": "tagname",
            "placeholder": "请输入标签名"
        }),
        error_messages={"required": "标签名不能为空！"}
    )


class CategoryForm(Form):
    category = fields.CharField(
        widget=widgets.TextInput(attrs={
            "class": "form-control",
            "id": "category",
            "placeholder": "请输入分类名称"
        }),
        error_messages={"required": "分类名称不能为空！"}
    )
