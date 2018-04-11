#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2018/4/9
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from web.service import idc
from django.utils.decorators import method_decorator
from utils.my_decorator import login_decorator


class IDCListView(View):
    @method_decorator(login_decorator)
    def get(self, request, *args, **kwargs):
        return render(request, 'idc_list.html')


class IDCJsonView(View):
    def __init__(self, **kwargs):
        self.obj = idc.IDC()
        super(IDCJsonView, self).__init__(**kwargs)

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


class AddIDCView(View):
    @method_decorator(login_decorator)
    def get(self, request, *args, **kwargs):
        service_obj = idc.IDC()
        model_form_class = service_obj.create_model_form()
        asset_model_form_obj = model_form_class()
        return render(request, 'add_idc.html', {
            "model_form_obj": asset_model_form_obj,
            "service_obj": service_obj
        })
