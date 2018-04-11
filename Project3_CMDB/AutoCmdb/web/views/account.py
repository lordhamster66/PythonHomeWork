#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render, redirect
from web.forms import LoginForm


class LoginView(View):
    def get(self, request, *args, **kwargs):
        login_form_obj = LoginForm()
        return render(request, "login.html", locals())

    def post(self, request, *args, **kwargs):
        login_form_obj = LoginForm(request.POST)
        if login_form_obj.is_valid():
            request.session.clear_expired()
            request.session["already_login"] = True
            if request.POST.get("remember"):
                request.session.set_expiry(30 * 24 * 60 * 60)
            return redirect("/index.html")
        else:
            return render(request, "login.html", locals())


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        request.session["already_login"] = False
        request.session.delete(request.session.session_key)
        return redirect("/login.html")
