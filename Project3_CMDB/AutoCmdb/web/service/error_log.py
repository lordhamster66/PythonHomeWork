#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2018/4/10
from repository import models
from .base import BaseServiceList


class ErrorLog(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'title', 'text': '标题', 'condition_type': 'input'},
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
                'q': 'asset_obj__idc__name',
                'title': "IDC机房",
                'display': 0,
                'text': {'content': "", 'kwargs': {}},
                'attr': {}
            },
            {
                'q': 'asset_obj__cabinet_num',
                'title': "机柜号",
                'display': 0,
                'text': {'content': "", 'kwargs': {}},
                'attr': {}
            },
            {
                'q': 'asset_obj__cabinet_order',
                'title': "机柜中序号",
                'display': 0,
                'text': {'content': "", 'kwargs': {}},
                'attr': {}
            },
            {
                'q': 'asset_obj',
                'title': "资产",
                'display': 1,
                'text': {
                    'content': "{asset_obj__idc__name}-{asset_obj__cabinet_num}-{asset_obj__cabinet_order}",
                    'kwargs': {
                        'asset_obj__idc__name': '@asset_obj__idc__name',
                        'asset_obj__cabinet_num': '@asset_obj__cabinet_num',
                        'asset_obj__cabinet_order': '@asset_obj__cabinet_order',
                    }
                },
                'attr': {}
            },
            {
                'q': 'title',
                'title': "标题",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@title'}},
                'attr': {'name': 'title', 'id': '@title', 'origin': '@title', 'edit-enable': 'true',
                         'edit-type': 'input', }
            },
            {
                'q': 'content',
                'title': "日志内容",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@content'}},
                'attr': {'name': 'content', 'id': '@content', 'origin': '@content', 'edit-enable': 'true',
                         'edit-type': 'input', }
            },
            {
                'q': 'create_at',
                'title': "日志产生时间",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@create_at'}},
                'attr': {}
            },
        ]
        # 额外搜索条件
        extra_select = {}
        global_dict = {}
        queryset = models.ErrorLog.objects.all()
        # 要排除的字段
        exclude_fields = ()
        super(ErrorLog, self).__init__(condition_config, table_config, extra_select, global_dict, queryset,
                                       exclude_fields)
