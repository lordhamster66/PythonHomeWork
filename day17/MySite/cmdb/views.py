from django.shortcuts import render
from django.shortcuts import HttpResponse
import json

# Create your views here.


def login(request):
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")


def login_check(request):
    if request.method == "POST":
        loginObj = request.POST.get("loginObj")
        # ret = json.dumps({"accountMsg": "用户名不存在"})
        # ret = json.dumps({"pwdMsg": "用户名密码错误"})
        ret = json.dumps({"user": "111"})
        return HttpResponse(ret)


def index(request):
    if request.method == "POST":
        accountNo = request.POST.get("accountNo")
        pwd = request.POST.get("pwd")
        print(accountNo, pwd)
        return HttpResponse("ok!")


