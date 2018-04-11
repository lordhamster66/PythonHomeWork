#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2018/4/10
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from web.service import error_log
from django.utils.decorators import method_decorator
from utils.my_decorator import login_decorator


class ErrorLogListView(View):
    @method_decorator(login_decorator)
    def get(self, request, *args, **kwargs):
        return render(request, 'error_log_list.html')


class ErrorLogJsonView(View):
    def __init__(self, **kwargs):
        self.obj = error_log.ErrorLog()
        super(ErrorLogJsonView, self).__init__(**kwargs)

    @method_decorator(login_decorator)
    def get(self, request):
        response = self.obj.fetch_queryset(request)
        return JsonResponse(response.__dict__)

    @method_decorator(login_decorator)
    def delete(self, request):
        response = self.obj.delete_queryset(request)
        return JsonResponse(response.__dict__)

    @method_decorator(login_decorator)
    def put(self, request):
        response = self.obj.put_queryset(request)
        return JsonResponse(response.__dict__)

    @method_decorator(login_decorator)
    def post(self, request):
        response = self.obj.post_queryset(request)
        return JsonResponse(response.__dict__)


class AddErrorLogView(View):
    @method_decorator(login_decorator)
    def get(self, request, *args, **kwargs):
        service_obj = error_log.ErrorLog()
        model_form_class = service_obj.create_model_form()
        asset_model_form_obj = model_form_class()
        return render(request, 'add_error_log.html', {
            "model_form_obj": asset_model_form_obj,
            "service_obj": service_obj
        })
