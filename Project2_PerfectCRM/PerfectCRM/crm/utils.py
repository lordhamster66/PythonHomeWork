#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/12/30
import random
import string
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_registration_url(enrollment_obj):
    """获取客户填写报名信息的随机URL"""
    random_str = "".join(random.sample(string.ascii_lowercase + string.digits, 6))
    cache.set(enrollment_obj.id, random_str, 60 * 10)  # 设置链接超时时间为10分钟
    registration_url = "http://127.0.0.1:8000/crm/customer/registration/%s/%s/" % (
        enrollment_obj.id, random_str
    )
    return registration_url


def get_paginator_query_sets(request, contact_list, list_per_page):
    """
    获取带分页对象的query_sets
    :param request:
    :param contact_list: query_sets
    :param list_per_page: 每页显示几条
    :return:
    """
    paginator = Paginator(contact_list, list_per_page)  # 获取分页对象
    page = request.GET.get('page')  # 获取当前页码
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        query_sets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        query_sets = paginator.page(paginator.num_pages)
    return query_sets
