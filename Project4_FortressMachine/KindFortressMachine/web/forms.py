#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2018/3/21
from django.forms import Form
from django.forms import fields
from django.forms import widgets
from web import models


class AuditLogForm(Form):
    """审计日志所需form"""
    list_per_page = fields.ChoiceField(
        choices=((10, 10), (25, 25), (50, 50), (100, 100)),
        widget=widgets.Select(attrs={"id": "list_per_page", "class": "form-control"})
    )

    user = fields.ChoiceField(
        label="用户",
        widget=widgets.Select(attrs={"class": "form-control", "style": "width:100%"}),
        required=False
    )

    bind_host = fields.ChoiceField(
        label="访问的主机",
        widget=widgets.Select(attrs={"class": "form-control", "style": "width:100%"}),
        required=False
    )

    start_date = fields.DateField(
        label="起始日期",
        widget=widgets.DateInput(attrs={"class": "date-picker form-control", "style": "width:100%"}),
        required=False
    )

    end_date = fields.DateField(
        label="终止日期",
        widget=widgets.DateInput(attrs={"class": "date-picker form-control", "style": "width:100%"}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(AuditLogForm, self).__init__(*args, **kwargs)
        user_choices = list(models.UserProfile.objects.values_list("id", "name"))
        user_choices.insert(0, ("", "------------------"))
        self.fields["user"].widget.choices = user_choices

        bind_host_needed_fields = ["id", "host__ip_adr", "remote_user__username"]
        bind_host_choices = list(
            models.BindHost.objects.select_related(*bind_host_needed_fields).values_list(*bind_host_needed_fields))
        bind_host_choices = [(i[0], f"{i[2]}@{i[1]}") for i in bind_host_choices]
        bind_host_choices.insert(0, ("", "------------------"))
        self.fields["bind_host"].widget.choices = bind_host_choices


class AuditLogDetailForm(Form):
    """审计日志详细记录form"""
    list_per_page = fields.ChoiceField(
        choices=((10, 10), (25, 25), (50, 50), (100, 100)),
        widget=widgets.Select(attrs={"id": "list_per_page", "class": "form-control"})
    )

    parse_mark = fields.ChoiceField(
        label="解析方式",
        choices=(("read(5,", "read(5,"), ("read(4,", "read(4,")),
        widget=widgets.Select(attrs={"id": "parse_mark", "class": "form-control", "style": "width:100%"})
    )
