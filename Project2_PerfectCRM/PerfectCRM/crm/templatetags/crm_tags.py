#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2018/1/4
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def get_condition_str(condition_dict):
    """拼接过滤条件"""
    condition_str = ""
    for k, v in condition_dict.items():
        condition_str += "&%s=%s" % (k, v)
    return condition_str


@register.simple_tag
def get_page_ele(query_sets, condition_dict=None, order_by_dict=None):
    """生成想要显示的分页标签"""
    page_ele = ""  # 要返回的分页HTML
    condition_str = ""  # 过滤条件
    current_order_by_key = ""  # 排序条件
    if condition_dict:
        condition_str = get_condition_str(condition_dict)
    if order_by_dict:
        current_order_by_key = order_by_dict.get("current_order_by_key", "")
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
