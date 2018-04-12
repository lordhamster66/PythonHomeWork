#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2018/3/11
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_paginator_query_sets(request, contact_list, list_per_page):
    """获取封装分页功能的query_sets"""
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
