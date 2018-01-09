from django.shortcuts import render
from crm.utils import get_paginator_query_sets


# Create your views here.
def index(request):
    """学员首页"""
    return render(request, "student/index.html")


def my_classes(request):
    """我的班级"""
    enrollment_list = request.user.stu_info.enrollment_set.all()
    my_classes_list = [enrollment_obj.enrolled_class for enrollment_obj in enrollment_list]
    my_classes_list = get_paginator_query_sets(request, my_classes_list, 10)  # 获取带分页对象的班级列表
    return render(request, "student/my_classes.html", {"my_classes_list": my_classes_list})
