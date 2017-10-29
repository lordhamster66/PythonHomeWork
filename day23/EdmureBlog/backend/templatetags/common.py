#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/10/29
from django import template
from datetime import datetime

register = template.Library()


@register.simple_tag
def format_time(qtime):
    """格式化日期"""
    return datetime.strftime(qtime, "%Y-%m-%d")
