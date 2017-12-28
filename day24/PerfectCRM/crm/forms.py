#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/12/23
from crm import models
from django.forms import ModelForm


class EnrollmentForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs["class"] = "form-control"
        return ModelForm.__new__(cls)

    class Meta:
        model = models.Enrollment
        fields = ("enrolled_class",)


class CustomerModelForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs["class"] = "form-control"
            field_obj.widget.attrs["required"] = "true"
        return ModelForm.__new__(cls)

    class Meta:
        model = models.Customer
        fields = "__all__"
        exclude = ("qq", "consultant", "source", "referral_from", "consult_course", "content", "tags", "memo", "status")
