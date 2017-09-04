#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/9/4
from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class IPparser(MiddlewareMixin):
    """IP过滤中间件"""

    def process_request(self, request):
        if request.environ.get("REMOTE_ADDR") == "128.0.0.1":
            return HttpResponse("滚！")

    def process_view(self, request, view_func, view_func_args, view_func_kwargs):
        pass

    def process_response(self, request, response):
        pass
        return response
