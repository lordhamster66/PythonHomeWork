#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/10/29
from django import forms
from django.forms import fields
from django.forms import widgets
from repository import models


class ArticleForm(forms.Form):
    title = fields.CharField(
        widget=widgets.TextInput(
            attrs={
                "class": "form-control",
                "id": "title",
                "placeholder": "文章标题",
            })
    )

    summary = fields.CharField(
        widget=widgets.Textarea(
            attrs={
                "class": "form-control",
                "id": "summary",
                "placeholder": "文章简介",
                "rows": "2",
            }
        )
    )

    content = fields.CharField(
        widget=widgets.Textarea(
            attrs={
                "name": "content",
                "id": "content",
                "style": "width: 100%;min-height:500px;visibility:hidden;",
            }
        )
    )

    article_type_id = fields.ChoiceField(
        choices=[],
        widget=widgets.RadioSelect
    )

    category_id = fields.ChoiceField(
        choices=[],
        widget=widgets.RadioSelect
    )

    tags = fields.MultipleChoiceField(
        required=False,
        choices=[],
        widget=widgets.CheckboxSelectMultiple
    )

    top = fields.MultipleChoiceField(
        required=False,
        choices=[("1", "置顶")],
        widget=widgets.CheckboxSelectMultiple
    )

    def __init__(self, request, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        username = request.session.get("username", None)  # 获取session中的用户名
        user_obj = models.UserInfo.objects.filter(username=username).select_related("blog").first()  # 获取用户对象
        self.fields["article_type_id"].choices = models.ArticleType.objects.values_list("nid", "type")  # 获取所有类型
        self.fields["category_id"].choices = models.Category.objects.filter(blog_id=user_obj.blog.nid).values_list(
            "nid",
            "title"
        )  # 获取用户所有分类
        self.fields["tags"].choices = models.Tag.objects.filter(blog_id=user_obj.blog.nid).values_list(
            "nid",
            "title"
        )  # 获取用户所有标签
