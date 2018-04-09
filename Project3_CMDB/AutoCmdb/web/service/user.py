#!/usr/bin/env python
# -*- coding:utf-8 -*-
from repository import models
from .base import BaseServiceList


class User(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'name', 'text': '用户名', 'condition_type': 'input'},
            {'name': 'email', 'text': '邮箱', 'condition_type': 'input'},
        ]
        # 表格的配置
        table_config = [
            {
                'q': 'id',  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])
                'title': "ID",  # 前段表格中显示的标题
                'display': 1,  # 是否在前段显示，0表示在前端不显示, 1表示在前端隐藏, 2表示在前段显示
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}},
                'attr': {}  # 自定义属性
            },
            {
                'q': 'name',
                'title': "用户名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@name'}},
                'attr': {'name': 'name', 'id': '@name', 'origin': '@name', 'edit-enable': 'true',
                         'edit-type': 'input', }
            },
            {
                'q': 'email',
                'title': "邮箱",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@email'}},
                'attr': {'name': 'email', 'id': '@email', 'origin': '@email', 'edit-enable': 'true',
                         'edit-type': 'input', }
            },
            {
                'q': 'mobile',
                'title': "手机",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@mobile'}},
                'attr': {'name': 'mobile', 'id': '@mobile', 'origin': '@mobile', 'edit-enable': 'true',
                         'edit-type': 'input', }
            },
            {
                'q': 'phone',
                'title': "电话",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@phone'}},
                'attr': {'name': 'phone', 'id': '@phone', 'origin': '@phone', 'edit-enable': 'true',
                         'edit-type': 'input', }
            },

        ]
        # 额外搜索条件
        extra_select = {}
        global_dict = {}
        queryset = models.UserProfile.objects.all()
        super(User, self).__init__(condition_config, table_config, extra_select, global_dict, queryset)
