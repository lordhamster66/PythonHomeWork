from django.shortcuts import render
from crm.utils import get_paginator_query_sets


# Create your views here.
def index(request):
    """教师首页"""
    return render(request, "teacher/index.html")


def class_taken(request):
    """所带班级"""
    contact_list = request.user.classlist_set.all()
    class_taken_list = get_paginator_query_sets(request, contact_list, 10)  # 获取带分页对象的query_sets
    return render(request, "teacher/class_taken.html", {"class_taken_list": class_taken_list})
