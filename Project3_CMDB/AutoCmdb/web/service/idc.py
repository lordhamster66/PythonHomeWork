#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2018/4/9
from repository import models
from .base import BaseServiceList


class IDC(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'name', 'text': '机房', 'condition_type': 'input'},
            {'name': 'floor', 'text': '楼层', 'condition_type': 'input'},
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
                'title': "机房",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@name'}},
                'attr': {'name': 'name', 'id': '@name', 'origin': '@name', 'edit-enable': 'true',
                         'edit-type': 'input', }
            },
            {
                'q': 'floor',
                'title': "楼层",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@floor'}},
                'attr': {'name': 'floor', 'id': '@floor', 'origin': '@floor', 'edit-enable': 'true',
                         'edit-type': 'input', }
            },
        ]
        # 额外搜索条件
        extra_select = {}
        global_dict = {}
        queryset = models.IDC.objects.all()
        # 要排除的字段
        exclude_fields = ()
        super(IDC, self).__init__(condition_config, table_config, extra_select, global_dict, queryset, exclude_fields)
