#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2018/3/11
from django.utils.safestring import mark_safe
from django import template
import time

register = template.Library()


def get_condition_str(condition_dict):
    """拼接过滤条件"""
    condition_str = ""
    for k, v in condition_dict.items():
        condition_str += "&%s=%s" % (k, v)
    return condition_str


@register.simple_tag
def get_page_ele(query_sets, condition_dict=None, current_order_by_key=""):
    """生成想要显示的分页标签"""
    page_ele = ""  # 要返回的分页HTML
    condition_str = ""  # 过滤条件
    if condition_dict:
        condition_str = get_condition_str(condition_dict)
    # 上一页
    if query_sets.has_previous():
        page_ele += '''<li><a href="?page=%s%s&o=%s">«</a></li>''' % (
            query_sets.previous_page_number(), condition_str, current_order_by_key
        )
    else:
        page_ele += '''<li class="paginate_button disabled"><a href="javascript:void(0);">«</a></li>'''
    # 显示的页数
    for loop_num in query_sets.paginator.page_range:
        if loop_num < 3 or loop_num > query_sets.paginator.num_pages - 2 or abs(
                loop_num - query_sets.number) < 2:  # 最前2页和最后两页以及当前页及当前页前后两页
            actived = ""
            if loop_num == query_sets.number:
                actived = "active"
            page_ele += '''<li class="%s"><a href="?page=%s%s&o=%s">%s</a></li>''' % (
                actived, loop_num, condition_str, current_order_by_key, loop_num
            )
        elif abs(loop_num - query_sets.number) == 2:
            page_ele += '''<li class="paginate_button disabled"><a>...</a></li>'''
    # 下一页
    if query_sets.has_next():
        page_ele += '''<li><a href="?page=%s%s&o=%s">»</a></li>''' % (
            query_sets.next_page_number(), condition_str, current_order_by_key
        )
    else:
        page_ele += '''<li class="paginate_button disabled"><a href="#">»</a></li>'''
    return mark_safe(page_ele)


@register.simple_tag
def timestamp_to_str(timestamp):
    str_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timestamp)))
    return str_time


@register.simple_tag
def get_th_ele(th_name, field, condition_dict, order_by_key):
    sort_class = "sorting"  # 默认排序样式
    condition_str = get_condition_str(condition_dict)
    next_order_by_key = field  # 下次排序的方式
    if field == order_by_key.strip("-"):
        if order_by_key.startswith("-"):
            next_order_by_key = f"{field}"
            sort_class = "sorting_desc"
        else:
            next_order_by_key = f"-{field}"
            sort_class = "sorting_asc"
    th_ele = f"<th class='{sort_class} text-center' style='white-space: nowrap;'><a href='/audit_log/?o={next_order_by_key}{condition_str}' style='display: block;'>{th_name}</a></th>"
    return mark_safe(th_ele)
