#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2018/4/9
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse

from web.service import business_unit


class BusinessUnitListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'business_unit_list.html')


class BusinessUnitJsonView(View):
    def __init__(self, **kwargs):
        self.obj = business_unit.BusinessUnit()
        super(BusinessUnitJsonView, self).__init__(**kwargs)

    def get(self, request):
        response = self.obj.fetch_queryset(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = self.obj.delete_queryset(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = self.obj.put_queryset(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = self.obj.post_queryset(request)
        return JsonResponse(response.__dict__)


class AddBusinessUnitView(View):
    def get(self, request, *args, **kwargs):
        service_obj = business_unit.BusinessUnit()
        model_form_class = service_obj.create_model_form()
        asset_model_form_obj = model_form_class()
        return render(request, 'add_business_unit.html', {
            "model_form_obj": asset_model_form_obj,
            "service_obj": service_obj
        })
