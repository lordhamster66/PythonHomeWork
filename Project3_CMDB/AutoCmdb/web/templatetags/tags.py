#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2018/4/10
from django import template

register = template.Library()


@register.simple_tag
def get_m2m_available_objs(service_obj, field_name, model_form_obj):
    """获取所有多对多的对象"""
    m2m_available_objs = []  # 要返回的待选对象
    obj = model_form_obj.instance  # 要修改的对象或者为空
    try:
        field_obj = getattr(obj, field_name)  # 获取多对多字段对象
        m2m_chosen_objs = field_obj.all()
    except Exception as e:
        m2m_chosen_objs = []
    m2m = getattr(service_obj.queryset.model, field_name)
    m2m_objs = m2m.rel.to.objects.all()
    for i in m2m_objs:
        if i not in m2m_chosen_objs:
            m2m_available_objs.append(i)
    return m2m_available_objs


@register.simple_tag
def get_m2m_chosen_objs(model_form_obj, field_name):
    """获取已经选择的多对多对象"""
    obj = model_form_obj.instance
    try:
        field_obj = getattr(obj, field_name)
        m2m_chosen_objs = field_obj.all()
    except Exception as e:
        m2m_chosen_objs = []
    return m2m_chosen_objs
