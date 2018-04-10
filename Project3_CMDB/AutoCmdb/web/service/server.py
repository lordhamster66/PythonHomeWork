#!/usr/bin/env python
# -*- coding:utf-8 -*-
from repository import models
from .base import BaseServiceList


class Server(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = []
        # 表格的配置
        table_config = []
        # 额外搜索条件
        extra_select = {}
        # 全局变量
        global_dict = {}
        # queryset
        queryset = models.Server.objects.all()

        # 要排除的字段
        exclude_fields = ()
        self.filter_horizontal = ()
        super(Server, self).__init__(condition_config, table_config, extra_select, global_dict, queryset,
                                     exclude_fields)
