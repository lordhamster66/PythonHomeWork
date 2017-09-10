#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/9/10
"""自定义序列化模块"""
import json
from django.core.exceptions import ValidationError


class JsonCustomEncoder(json.JSONEncoder):
    def default(self, field):
        if isinstance(field, ValidationError):
            return {"code": field.code, "messages": field.messages}
        else:
            return json.JSONEncoder.default(self, field)
