#!/usr/bin/env python
# -*- coding:utf-8 -*-
from repository import models
from utils.response import BaseResponse
from .base import BaseServiceList


class Asset(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'cabinet_num', 'text': '机柜号', 'condition_type': 'input'},
            {'name': 'device_type_id', 'text': '资产类型', 'condition_type': 'select', 'global_name': 'device_type_list'},
            {'name': 'device_status_id', 'text': '资产状态', 'condition_type': 'select',
             'global_name': 'device_status_list'},
        ]
        # 表格的配置
        table_config = [
            {
                'q': 'id',  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])
                'title': "ID",  # 前段表格中显示的标题
                'display': 1,  # 是否在前段显示，0表示在前端不显示, 1表示在前端隐藏, 2表示在前段显示
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}},
                'attr': {'k1': 'v1'}  # 自定义属性
            },
            {
                'q': 'device_type_id',
                'title': "资产类型",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@device_type_list'}},
                'attr': {}
            },
            {
                'q': 'server_title',
                'title': "主机名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@server_title'}},
                'attr': {}
            },
            {
                'q': 'network_title',
                'title': "网络设备标识",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@network_title'}},
                'attr': {}
            },
            {
                'q': 'idc_id',
                'title': "IDC",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@idc_list'}},
                'attr': {'name': 'idc_id', 'id': '@idc_id', 'origin': '@idc_id', 'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'idc_list'}
            },
            {
                'q': 'cabinet_num',
                'title': "机柜号",
                'display': 1,
                'text': {'content': "{cabinet_num}", 'kwargs': {'cabinet_num': '@cabinet_num'}},
                'attr': {'name': 'cabinet_num', 'edit-enable': 'true', 'edit-type': 'input', 'origin': '@cabinet_num', }
            },
            {
                'q': 'cabinet_order',
                'title': "位置",
                'display': 1,
                'text': {'content': "{cabinet_order}", 'kwargs': {'cabinet_order': '@cabinet_order'}},
                'attr': {'name': 'cabinet_order', 'edit-enable': 'true', 'edit-type': 'input',
                         'origin': '@cabinet_order', }
            },
            {
                'q': 'business_unit_id',
                'title': "业务线ID",
                'display': 0,
                'text': {'content': "", 'kwargs': {}},
                'attr': {}
            },
            {
                'q': 'business_unit__name',
                'title': "业务线",
                'display': 1,
                'text': {'content': "{business_unit__name}", 'kwargs': {'business_unit__name': '@business_unit__name'}},
                'attr': {'name': 'business_unit_id', 'id': '@business_unit_id', 'origin': '@business_unit_id',
                         'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'business_unit_list'}
            },
            {
                'q': 'device_status_id',
                'title': "资产状态",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@device_status_list'}},
                'attr': {'name': 'device_status_id', 'id': '@device_status_id', 'origin': '@device_status_id',
                         'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'device_status_list'}
            },
            {
                'q': None,
                'title': "选项",
                'display': 1,
                'text': {
                    'content': "<a href='/asset-{device_type_id}-{nid}.html'>查看详细</a> | <a href='/edit-asset-{device_type_id}-{nid}.html'>编辑</a>",
                    'kwargs': {'device_type_id': '@device_type_id', 'nid': '@id'}},
                'attr': {}
            },
        ]
        # 额外搜索条件
        extra_select = {
            'server_title': 'select hostname from repository_server where repository_server.asset_id=repository_asset.id and repository_asset.device_type_id=1',
            'network_title': 'select management_ip from repository_networkdevice where repository_networkdevice.asset_id=repository_asset.id and repository_asset.device_type_id=2',
        }
        # 全局变量
        global_dict = {
            'device_status_list': self.device_status_list,
            'device_type_list': self.device_type_list,
            'idc_list': self.idc_list,
            'business_unit_list': self.business_unit_list
        }
        # queryset
        queryset = models.Asset.objects.all()

        # 要排除的字段
        exclude_fields = ("latest_date",)
        self.filter_horizontal = ("tag",)
        super(Asset, self).__init__(condition_config, table_config, extra_select, global_dict, queryset, exclude_fields)

    @property
    def device_status_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Asset.device_status_choices)
        return list(result)

    @property
    def device_type_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Asset.device_type_choices)
        return list(result)

    @property
    def idc_list(self):
        values = models.IDC.objects.only('id', 'name', 'floor')
        result = map(lambda x: {'id': x.id, 'name': "%s-%s" % (x.name, x.floor)}, values)
        return list(result)

    @property
    def business_unit_list(self):
        values = models.BusinessUnit.objects.values('id', 'name')
        return list(values)

    @staticmethod
    def assets_detail(device_type_id, asset_id):

        response = BaseResponse()
        try:
            if device_type_id == '1':
                response.data = models.Server.objects.filter(asset_id=asset_id).select_related('asset').first()
            else:
                response.data = models.NetworkDevice.objects.filter(asset_id=asset_id).select_related('asset').first()

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response
