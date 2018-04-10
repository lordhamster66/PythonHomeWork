#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2018/4/9

from repository import models
from .base import BaseServiceList


class BusinessUnit(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'name', 'text': '业务线', 'condition_type': 'input'},
            {'name': 'contact', 'text': '业务联系人', 'condition_type': 'select', 'global_name': 'contact_list'},
            {'name': 'manager', 'text': '系统管理员', 'condition_type': 'select', 'global_name': 'manager_list'},
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
                'title': "业务线",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@name'}},
                'attr': {'name': 'name', 'id': '@name', 'origin': '@name', 'edit-enable': 'true',
                         'edit-type': 'input', }
            },
            {
                'q': 'contact_id',
                'title': "业务联系人ID",
                'display': 0,
                'text': {'content': "", 'kwargs': {}},
                'attr': {}
            },
            {
                'q': 'contact__name',
                'title': "业务联系人",
                'display': 1,
                'text': {'content': "{contact__name}", 'kwargs': {'contact__name': '@contact__name'}},
                'attr': {'name': 'contact_id', 'id': '@contact_id', 'origin': '@contact_id',
                         'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'contact_list'}
            },
            {
                'q': 'manager_id',
                'title': "系统管理员ID",
                'display': 0,
                'text': {'content': "", 'kwargs': {}},
                'attr': {}
            },
            {
                'q': 'manager__name',
                'title': "系统管理员",
                'display': 1,
                'text': {'content': "{manager__name}", 'kwargs': {'manager__name': '@manager__name'}},
                'attr': {'name': 'manager_id', 'id': '@manager_id', 'origin': '@manager_id',
                         'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'manager_list'}
            },

        ]
        # 额外搜索条件
        extra_select = {}
        global_dict = {
            'contact_list': self.contact_list,
            'manager_list': self.manager_list,
        }

        queryset = models.BusinessUnit.objects.all()

        # 要排除的字段
        exclude_fields = ()
        super(BusinessUnit, self).__init__(condition_config, table_config, extra_select, global_dict, queryset,
                                           exclude_fields)

    @property
    def contact_list(self):
        result = models.UserGroup.objects.values("id", "name")
        return list(result)

    @property
    def manager_list(self):
        result = models.UserGroup.objects.values("id", "name")
        return list(result)
