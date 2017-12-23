#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/12/21
import re
from kind_admin import kind_admin

# url_type: 0 代表相对路径，1代表绝对路径, 2代表模糊路径使用正则进行匹配
PermissionDict = {
    # crm项目权限
    # 可以访问销售首页
    "crm.can_access_sales_index": {
        "url_type": 0,  # 路径类型
        "url": "sales_index",  # 路径名称,根据路径类型判断是绝对还是相对路径或者模糊路径
        "method": "GET",  # 请求方法
        "args": [],  # 请求参数
        "hooks": []  # 预留钩子,or 和 and 为关键字代表或和与的关系,只有此列表全为真才会通过验证
    },

    # kind_admin项目权限
    # 可以访问kind_admin下注册的客户库
    "crm.can_access_customer_table": {
        "url_type": 1,
        "url": "/kind_admin/crm/customer/",
        "method": "GET",
        "args": [],
        "hooks": []
    },
    # 可以访问在kind_admin下注册的客户库添加客户页面
    "crm.can_access_customer_add": {
        "url_type": 1,
        "url": "/kind_admin/crm/customer/add/",
        "method": "GET",
        "args": [],
        "hooks": []
    },
    # 可以在kind_admin下注册的客户库添加客户
    "crm.can_add_customer": {
        "url_type": 1,
        "url": "/kind_admin/crm/customer/add/",
        "method": "POST",
        "args": [],
        "hooks": []
    },
    # 可以访问在kind_admin下注册的客户库所生成的客户修改页
    "crm.can_access_customer_change": {
        "url_type": 2,
        "url": "/kind_admin/crm/customer/\d+/change/$",
        "method": "GET",
        "args": [],
        "hooks": []
    },
    # 可以修改在kind_admin下注册的客户库中的客户,且只能修改自己的客户
    "crm.can_change_customer": {
        "url_type": 2,
        "url": "/kind_admin/crm/customer/\d+/change/$",
        "method": "POST",
        "args": [],
        "hooks": ["only_change_your_own_customer"]
    },
    # 可以访问密码修改页
    "crm.can_access_change_password": {
        "url_type": 0,
        "url": "change_password",
        "method": "GET",
        "args": [],
        "hooks": []
    },
    # 可以修改自己的密码
    "crm.can_change_own_password": {
        "url_type": 2,
        "url": "/kind_admin/crm/userprofile/\d+/change/password/$",
        "method": "POST",
        "args": [],
        "hooks": ["only_change_own_password"],
    },
}


def only_change_own_password(request, *args, **kwargs):
    """验证只能修改自己的密码"""
    ret = {"status": False, "errors": [], "data": None}  # 要返回的内容
    matched_ret = re.match("/kind_admin/crm/userprofile/(?P<user_id>\d+)/change/password/$", request.path)
    if matched_ret:
        if matched_ret.groupdict().get("user_id") == str(request.user.id):
            ret["status"] = True
        else:
            ret["errors"].append("因为，您只能修改自己的用户密码！")
    return ret


def only_change_your_own_customer(request, *args, **kwargs):
    """销售只能修改自己下面的客户信息"""
    ret = {"status": False, "errors": [], "data": None}  # 要返回的内容
    admin_class = kind_admin.enabled_admins[kwargs.get('app_name')][kwargs.get('table_name')]  # 获取admin_class
    customer_obj = admin_class.model.objects.filter(id=kwargs.get('obj_id')).first()  # 获取要修改的对象
    if customer_obj.consultant == request.user:  # 说明销售在修改自己下面的客户
        ret["status"] = True
    else:
        ret["errors"].append("因为，您只能修改自己下面的客户信息！")
    return ret
