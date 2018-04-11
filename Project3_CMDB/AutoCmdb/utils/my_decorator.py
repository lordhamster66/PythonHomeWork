#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2018/4/11
from django.shortcuts import redirect


def login_decorator(func):
    def inner(request, *args, **kwargs):
        if request.session.get("already_login"):
            return func(request, *args, **kwargs)
        else:
            return redirect("/login.html")

    return inner
