from django.shortcuts import render
from django.db.models import Sum
from crm.utils import get_paginator_query_sets
from crm import models


# Create your views here.
def index(request):
    """学员首页"""
    return render(request, "student/index.html")


def my_classes(request):
    """我的班级"""
    my_classes_list = []  # 存储所报班级
    stu_info = request.user.stu_info
    if stu_info:  # 关联学生信息才会有班级显示
        enrollment_list = stu_info.enrollment_set.all()
        my_classes_list = [enrollment_obj.enrolled_class for enrollment_obj in enrollment_list if enrollment_obj]
    my_classes_list = get_paginator_query_sets(request, my_classes_list, 10)  # 获取带分页对象的班级列表
    return render(request, "student/my_classes.html", {"my_classes_list": my_classes_list})


def my_class_course_record(request, class_list_id):
    """我的班级对应上课记录"""
    user_score_info = 0  # 对应班级学习成绩总得分
    course_record_obj_list = []  # 存储对应班级的所有上课记录
    # 获取对应班级
    class_list_obj = models.ClassList.objects.filter(id=class_list_id).first()
    stu_info = request.user.stu_info  # 获取用户的基本信息
    if stu_info:  # 关联学生信息才会有班级显示
        # 获取对应报名对象
        enrollment_obj = models.Enrollment.objects.filter(customer=stu_info, enrolled_class=class_list_obj).first()
        # 获取对应班级的所有上课记录
        raw_course_record_obj_list = models.CourseRecord.objects.filter(
            from_class=class_list_obj
        ).all().order_by("day_num")
        user_score_info = models.StudyRecord.objects.filter(student=enrollment_obj).aggregate(Sum("score"))
        for course_record_obj in raw_course_record_obj_list:
            user_study_record_obj = models.StudyRecord.objects.filter(
                student=enrollment_obj,
                course_record=course_record_obj
            ).first()  # 获取对应上课记录的学习记录
            course_record_obj.user_study_record_obj = user_study_record_obj  # 将该用户本节上课记录的学习记录封装起来
            course_record_obj_list.append(course_record_obj)  # 将封装好的上课记录对象加入上课记录列表中
    # 获取带分页对象的对应班级的所有上课记录
    course_record_obj_list = get_paginator_query_sets(request, course_record_obj_list, 10)
    return render(request, "student/my_class_course_record.html", {
        "user_score_info": user_score_info,  # 总得分
        "class_list_obj": class_list_obj,  # 对应班级
        "course_record_obj_list": course_record_obj_list  # 对应班级所有上课记录
    })
