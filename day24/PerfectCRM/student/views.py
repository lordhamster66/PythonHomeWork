import json
import os
import time
from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Sum
from crm.utils import get_paginator_query_sets
from crm import models
from PerfectCRM import settings


# Create your views here.
def index(request):
    """学员首页"""
    return render(request, "student/index.html")


def my_classes(request):
    """我的班级"""
    my_classes_list = []  # 存储所报班级
    stu_info = request.user.stu_info  # 获取已经登陆的学员账户所对应的客户信息对象
    if stu_info:  # 关联学生信息才会有班级显示
        enrollment_list = stu_info.enrollment_set.all()  # 由客户信息对象可以找出该客户所有的报名对象
        # 通过报名对象可以找出该学员所有的报名班级，然后返回给前端即可
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
        # 对该学员所报班级的所有上课记录进行分数求和，得出该学员在该班级的总成绩得分
        user_score_info = models.StudyRecord.objects.filter(student=enrollment_obj).aggregate(Sum("score"))
        for course_record_obj in raw_course_record_obj_list:
            user_study_record_obj = models.StudyRecord.objects.filter(
                student=enrollment_obj,
                course_record=course_record_obj
            ).first()  # 获取对应上课记录的学习记录
            course_record_obj.user_study_record_obj = user_study_record_obj  # 将该用户本节上课记录的学习记录封装起来
            # 将封装好的上课记录对象加入上课记录列表中，这样可以在调取上课记录时直接获取到该学员的学习记录
            course_record_obj_list.append(course_record_obj)
    # 获取带分页对象的对应班级的所有上课记录
    course_record_obj_list = get_paginator_query_sets(request, course_record_obj_list, 10)
    return render(request, "student/my_class_course_record.html", {
        "user_score_info": user_score_info,  # 总得分
        "class_list_obj": class_list_obj,  # 对应班级
        "course_record_obj_list": course_record_obj_list  # 对应班级所有上课记录
    })


def homework_detail(request, study_record_id):
    """
    查看作业详情
    :param request: 用户请求内容
    :param study_record_id: 学习记录ID
    :return:
    """
    stu_info = request.user.stu_info  # 获取用户的基本信息
    study_record_obj = models.StudyRecord.objects.filter(
        id=study_record_id,
        student__customer=stu_info
    ).first()  # 获取学习记录
    if study_record_obj:  # 能获取到学习记录对象，才继续下一步操作
        homework_files_dict = {}  # 存放所有作业详情的字典
        # 获取学员作业存放路径
        student_homework_abspath = os.path.join(
            settings.STUDENT_HOMEWORK_DIR, str(request.user.stu_info.id),
            str(study_record_obj.course_record.id), str(study_record_id)
        )
        os.makedirs(student_homework_abspath, exist_ok=True)  # 可以确保目录存在
        all_homework_files_name_list = os.listdir(student_homework_abspath)  # 学员已经上传的本次所有作业文件名称
        for homework_file_name in all_homework_files_name_list:
            homework_file_path = os.path.join(student_homework_abspath, homework_file_name)  # 作业文件绝对路径
            homework_file_stat = os.stat(homework_file_path)  # 获取作业文件的基本信息
            homework_files_dict[homework_file_name] = {
                "file_size": homework_file_stat.st_size,
                "st_mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(homework_file_stat.st_mtime))
            }
        return render(request, "student/homework_detail.html", {
            "study_record_obj": study_record_obj,
            "homework_files_dict": homework_files_dict
        })
    else:
        return redirect("/student/my_classes/")


def upload_homework(request):
    """
    学员上传作业
    :param request: 请求内容
    :return:
    """
    ret = {"status": False, "error": None, "data": None}  # 要返回的内容
    course_record_id = request.POST.get("course_record_id")  # 获取上课记录ID
    study_record_id = request.POST.get("study_record_id")  # 获取学习记录ID
    if course_record_id and study_record_id:
        # 获取学员本次作业应该存放的路径
        student_homework_abspath = os.path.join(
            settings.STUDENT_HOMEWORK_DIR, str(request.user.stu_info.id),
            str(course_record_id), str(study_record_id)
        )
        os.makedirs(student_homework_abspath, exist_ok=True)  # 可以确保目录存在
        exist_homwork_files_name_list = os.listdir(student_homework_abspath)  # 已经存在的作业
        if len(exist_homwork_files_name_list) >= 5:
            ret["error"] = "只能存放5个作业文件！如需增加，可以删除现有作业，并选择打包的方式上传！"
        else:
            ret["data"] = {}  # 存放所有作业信息，返回给前端
            for k, file_obj in request.FILES.items():  # 存储文件
                with open(os.path.join(student_homework_abspath, file_obj.name), "wb") as f:
                    for line in file_obj:
                        f.write(line)
            all_homework_files_name_list = os.listdir(student_homework_abspath)  # 学员已经上传的本次所有作业文件名称
            for homework_file_name in all_homework_files_name_list:
                homework_file_path = os.path.join(student_homework_abspath, homework_file_name)  # 作业文件绝对路径
                homework_file_stat = os.stat(homework_file_path)  # 获取作业文件的基本信息
                ret["data"][homework_file_name] = {
                    "file_size": homework_file_stat.st_size,
                    "st_mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(homework_file_stat.st_mtime))
                }
            ret["status"] = True
    return HttpResponse(json.dumps(ret))


def delete_homework(request):
    """
    删除作业
    :param request:
    :return:
    """
    ret = {"status": False, "error": None, "data": None}  # 要返回的内容
    course_record_id = request.POST.get("course_record_id")  # 获取上课记录ID
    study_record_id = request.POST.get("study_record_id")  # 获取学习记录ID
    homework_file_name = request.POST.get("homework_file_name")  # 获取要删除的作业文件名称
    if course_record_id and study_record_id:
        # 获取学员作业存放路径
        student_homework_abspath = os.path.join(
            settings.STUDENT_HOMEWORK_DIR, str(request.user.stu_info.id),
            str(course_record_id), str(study_record_id)
        )
        homework_file_path = os.path.join(student_homework_abspath, homework_file_name)
        os.remove(homework_file_path)
        ret["status"] = True
    return HttpResponse(json.dumps(ret))


def download_homework(request):
    """
    下载作业
    :param request:
    :return:
    """
    if request.method == "GET":
        stu_info_id = request.GET.get("stu_info_id")  # 获取学员信息对象ID
        course_record_id = request.GET.get("course_record_id")  # 获取上课记录ID
        study_record_id = request.GET.get("study_record_id")  # 获取学习记录ID
        homework_file_name = request.GET.get("homework_file_name")  # 获取要删除的作业文件名称
        if course_record_id and study_record_id and stu_info_id and homework_file_name:
            # 获取学员作业存放路径
            student_homework_abspath = os.path.join(
                settings.STUDENT_HOMEWORK_DIR, str(request.user.stu_info.id),
                str(course_record_id), str(study_record_id)
            )
            homework_file_path = os.path.join(student_homework_abspath, homework_file_name)
            if os.path.isfile(homework_file_path):
                with open(homework_file_path, "rb") as f:
                    file_obj = f.read()
                # 设定文件头，这种设定可以让任意文件都能正确下载，而且已知文本文件不是本地打开
                response = HttpResponse(file_obj, content_type='APPLICATION/OCTET-STREAM')
                # 设定传输给客户端的文件名称
                response['Content-Disposition'] = 'attachment; filename=' + homework_file_name
                response['Content-Length'] = os.path.getsize(homework_file_path)  # 传输给客户端的文件大小
                return response
            else:
                return HttpResponse("文件不存在！")
        else:
            return HttpResponse("参数错误！")
