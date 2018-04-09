import os
import time
import json
from django.shortcuts import render, HttpResponse
from crm.utils import get_paginator_query_sets
from crm import models
from PerfectCRM import settings


# Create your views here.
def index(request):
    """教师首页"""
    return render(request, "teacher/index.html")


def class_taken(request):
    """所带班级"""
    contact_list = request.user.classlist_set.all()
    class_taken_list = get_paginator_query_sets(request, contact_list, 10)  # 获取带分页对象的query_sets
    return render(request, "teacher/class_taken.html", {"class_taken_list": class_taken_list})


def homework_list(request):
    """
    下载某节学习记录下的所有作业文件
    :param request:
    :return:
    """
    if request.method == "POST":
        ret = {"status": False, "error": None, "data": None}  # 要返回的内容
        if request.is_ajax():  # 确保是ajax请求
            study_record_id = request.POST.get("study_record_id")
            study_record_obj = models.StudyRecord.objects.filter(id=study_record_id).first()  # 获取学习记录对象
            if study_record_obj:  # 学习记录存在
                stu_info_id = study_record_obj.student.customer.id  # 学员信息对象ID
                course_record_id = study_record_obj.course_record.id  # 上课记录对象ID
                student_homework_abspath = os.path.join(
                    settings.STUDENT_HOMEWORK_DIR, str(stu_info_id),
                    str(course_record_id), str(study_record_id)
                )  # 获取学员作业存放路径
                os.makedirs(student_homework_abspath, exist_ok=True)  # 可以确保目录存在
                exist_homwork_files_name_list = os.listdir(student_homework_abspath)  # 已经存在的作业
                ret["data"] = {}  # 存放所有作业信息，返回给前端
                for homework_file_name in exist_homwork_files_name_list:
                    homework_file_path = os.path.join(student_homework_abspath, homework_file_name)  # 作业文件绝对路径
                    homework_file_stat = os.stat(homework_file_path)  # 获取作业文件的基本信息
                    ret["data"][homework_file_name] = {
                        "file_size": homework_file_stat.st_size,
                        "st_mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(homework_file_stat.st_mtime)),
                        "download_url": "/student/download_homework/?stu_info_id={stu_info_id}&course_record_id={course_record_id}&study_record_id={study_record_id}&homework_file_name={homework_file_name}".format(
                            stu_info_id=stu_info_id,
                            course_record_id=course_record_id,
                            study_record_id=study_record_id,
                            homework_file_name=homework_file_name
                        )
                    }
                ret["status"] = True
            else:
                ret["error"] = "学习记录不存在"
        else:
            ret["error"] = "非Ajax请求"
        return HttpResponse(json.dumps(ret))
