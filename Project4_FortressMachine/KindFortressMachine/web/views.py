import os
import json
import logging
import shutil
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from web import models
from KindFortressMachine import utils
from django.conf import settings
from django.utils.timezone import datetime, timedelta
from backend import audit
from web import forms
from backend import multi_task_handler

# Create your views here.
logger = logging.getLogger(__name__)  # 生成一个以当前模块名为名字的logger实例
c_logger = logging.getLogger("collect")  # 生成一个名为'collect'的logger实例，用于收集一些需要特殊记录的日志


def acc_login(request):
    """登录"""
    error_msg = ""  # 错误信息
    if request.method == "POST":
        auth_dict = {
            "username": request.POST.get("email"),
            "password": request.POST.get("password")
        }
        user = authenticate(**auth_dict)  # 验证用户登录
        if user:
            next_url = request.POST.get("next", "/")  # 获取用户登录后要跳转的页面地址
            login(request, user)  # 将用户登录
            logger.info(f"用户{user.email}登录成功！")
            return redirect(next_url)  # 登录后直接跳转至首页或者用户想要去的地址
        else:
            error_msg = "用户名或者密码错误！"
    return render(request, "login.html", {"error_msg": error_msg})


@login_required
def acc_logout(request):
    """注销"""
    logout(request)  # 注销用户
    logger.info(f"用户{request.user.email}注销登录成功！")
    return redirect("/login/")


@login_required
def index(request):
    """堡垒机首页"""
    return render(request, "index.html")


@login_required
def web_ssh(request):
    """WEB SSH页面"""
    info_dict = {
        "web_ssh_url": settings.WEB_SSH_URL,
        "web_ssh_user": settings.WEB_SSH_USER,
        "web_ssh_pwd": settings.WEB_SSH_PWD,
    }
    return render(request, "web_ssh.html", {"info_dict": info_dict})


@login_required
def audit_log(request):
    """审计日志页面"""
    condition_dict = {
        "list_per_page": request.GET.get("list_per_page", 10),
        "user": request.GET.get("user", ""),
        "bind_host": request.GET.get("bind_host", ""),
        "start_date": request.GET.get("start_date", ""),
        "end_date": request.GET.get("end_date", ""),
    }  # 查询条件
    audit_log_form_obj = forms.AuditLogForm(data=condition_dict)  # 审计日志页面form对象

    filter_ignore_fields = ["list_per_page", "start_date", "end_date"]  # query_set查询时要忽略的字段
    # 获取查询条件
    filter_dict = {k: v for k, v in condition_dict.items() if k not in filter_ignore_fields and v}
    if condition_dict["start_date"]:
        filter_dict["date__gte"] = condition_dict["start_date"]
    if condition_dict["end_date"]:
        # 例如要想查3月12日的数据，那时间应该是小于3月13日，不能等于，因为等于会把3月13日零点的数据包含进去
        filter_dict["date__lt"] = datetime.strptime(condition_dict["end_date"], "%Y-%m-%d") + timedelta(1)
    session_objs = models.Session.objects.filter(**filter_dict).all()

    order_by_key = request.GET.get("o", "")  # 获取要排序的方法
    if order_by_key:  # 有排序要求才进行排序
        session_objs = session_objs.order_by(order_by_key)
    session_objs = utils.get_paginator_query_sets(request, session_objs, condition_dict.get("list_per_page"))
    return render(request, "audit_log.html", {
        "audit_log_form_obj": audit_log_form_obj,
        "session_objs": session_objs,
        "condition_dict": condition_dict,
        "order_by_key": order_by_key
    })


@login_required
def audit_log_detail(request, session_id):
    """
    详细审计日志查看页面
    :param request:
    :param session_id: session对象ID
    :return:
    """
    condition_dict = {
        "list_per_page": request.GET.get("list_per_page", 100),
        "parse_mark": request.GET.get("parse_mark")
    }
    audit_log_detail_form_obj = forms.AuditLogDetailForm(data=condition_dict)
    session_obj = models.Session.objects.filter(id=session_id).first()  # 获取session对象
    audit_log_detail_path = os.path.join(
        settings.AUDIT_LOG_DIR,
        datetime.strftime(session_obj.date, "%Y-%m-%d"),
        f"strace_{session_obj.id}.log"
    )
    if os.path.exists(audit_log_detail_path):
        audit_log_parser = audit.AuditLogHandler(audit_log_detail_path, condition_dict.get("parse_mark"))
        cmd_list = audit_log_parser.parse()
        cmd_list = utils.get_paginator_query_sets(request, cmd_list, condition_dict.get("list_per_page"))
        return render(request, "audit_log_detail.html", {
            "audit_log_detail_form_obj": audit_log_detail_form_obj,
            "cmd_list": cmd_list
        })
    else:
        return HttpResponse("Sorry the file is not exist!")


@login_required
def multitask_cmd(request):
    """批量命令"""
    return render(request, "multitask_cmd.html")


@login_required
def multitask_file(request):
    """批量文件"""
    return render(request, "multitask_file.html")


@login_required
def multitask(request):
    """批量任务汇总处理"""
    if request.is_ajax():  # 是ajax请求
        ret = {"status": False, "errors": [], "data": None}
        multi_task_handler_obj = multi_task_handler.MultiTaskHandler(request)
        if multi_task_handler_obj.is_valid():  # 验证批量任务是否符合规范
            multi_task_run_status, multi_task_obj = multi_task_handler_obj.run()  # 运行批量任务
            if multi_task_run_status:
                # {"multi_task_obj_id": 1, "multi_task_detail_info": [{"id": 1, "bind_host": "root@192.168.122.10"}]}
                multi_task_detail_info = []
                for multi_task_detail_obj in multi_task_obj.multitaskdetail_set.all():
                    multi_task_detail_info.append({
                        "id": multi_task_detail_obj.id,
                        "status": multi_task_detail_obj.status,
                        "bind_host": f"{multi_task_detail_obj.bind_host.remote_user.username}@{multi_task_detail_obj.bind_host.host.ip_adr}",
                    })
                ret["status"] = True
                ret["data"] = {
                    "multi_task_obj_id": multi_task_obj.id,
                    "multi_task_detail_info": multi_task_detail_info
                }
            else:
                ret["errors"] = multi_task_handler_obj.errors
        else:
            ret["errors"] = multi_task_handler_obj.errors
        return HttpResponse(json.dumps(ret))


@login_required
def multitask_ret(request):
    """获取批量任务执行结果"""
    if request.is_ajax():
        ret = {"status": False, "errors": [], "data": None}
        multi_task_obj_id = request.POST.get("multi_task_obj_id")
        # 获取此批量任务ID的所有详细批量任务对象
        multi_task_detail_objs = models.MultiTaskDetail.objects.filter(multi_task_id=multi_task_obj_id).all()
        ret["status"] = True
        multi_task_detail_info = []
        for multi_task_detail_obj in multi_task_detail_objs:
            multi_task_detail_info.append({
                "id": multi_task_detail_obj.id,
                "result": multi_task_detail_obj.result,
                "status": multi_task_detail_obj.status,
            })

        ret["data"] = {
            "multi_task_detail_info": multi_task_detail_info
        }
        return HttpResponse(json.dumps(ret))


@login_required
def multitask_upload_file(request):
    """获取用户上传的文件"""
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    ret = {"status": False, "errors": None, "data": None}
    user_multi_task_file_transfer_dir = os.path.join(
        settings.MULTI_TASK_FILE_TRANSFER_DIR,
        str(request.user.id),
        str(ip)
    )
    if os.path.exists(user_multi_task_file_transfer_dir):
        shutil.rmtree(user_multi_task_file_transfer_dir)
    # 重新创建用户存文件的目录
    os.makedirs(user_multi_task_file_transfer_dir, exist_ok=True)
    file_obj = request.FILES.get("file")
    file_path = os.path.join(user_multi_task_file_transfer_dir, file_obj.name)
    with open(file_path, "wb") as f:
        for line in file_obj:
            f.write(line)
    ret["status"] = True
    return HttpResponse(json.dumps(ret))
