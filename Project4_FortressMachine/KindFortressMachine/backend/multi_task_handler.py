#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2018/3/25
import os
import json
import subprocess
from web import models
from django.db.transaction import atomic
from django.conf import settings


class MultiTaskHandler(object):
    """批量任务处理类"""

    def __init__(self, request):
        self.status = False  # 批量任务处理状态
        self.request = request  # 用户的请求相关数据
        self.multi_task_obj = None  # 要生成的批量任务对象
        self.errors = []  # 可能会产生的错误
        self.multiTaskData = None  # 批量任务处理的请求数据

    def is_valid(self):
        """验证任务是否符合规范"""
        vaild_ret = False  # 验证结果
        self.multiTaskData = json.loads(self.request.POST.get("multiTaskData"))  # 获取批量任务处理的请求数据
        if self.multiTaskData:
            isCancel = self.multiTaskData.get("isCancel")  # 获取用户是否想要终止任务
            multiTaskType = self.multiTaskData.get("multiTaskType")  # 获取批量任务处理类型
            if multiTaskType and isCancel:
                if hasattr(self, f"{multiTaskType}"):
                    vaild_ret = True
                else:
                    self.errors.append({"invalid": f"{multiTaskType}批量任务处理类型不存在"})
            else:
                self.errors.append({"invalid": "请求参数不全！"})
        return vaild_ret

    def cancel_multi_task(self):
        """取消批量任务"""
        multi_task_obj_id = self.multiTaskData.get("multi_task_obj_id")  # 获取用户要终止的批量任务对象ID
        self.multi_task_obj = models.MultiTask.objects.filter(id=multi_task_obj_id).first()
        if self.multi_task_obj:
            get_multi_task_pids_obj = subprocess.Popen(
                "ps -ef |grep python |grep multi_task_run |grep %s |awk '{ print $2 }'" % multi_task_obj_id,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            ret = get_multi_task_pids_obj.stdout.read().decode()
            multi_task_pids = [i for i in ret.split("\n") if i]
            for multi_task_pid in multi_task_pids:
                subprocess.call(f"kill {multi_task_pid}", shell=True)
            self.status = True  # 终止任务成功
        else:
            self.errors.append({"invalid": "还没执行任务哦！"})

    @atomic
    def cmd(self):
        """批量命令处理"""
        isCancel = self.multiTaskData.get("isCancel")  # 获取用户是否想要终止任务
        if isCancel == "0":
            bind_hosts_ids = self.multiTaskData.get("bind_hosts_ids")  # 获取用户要批量执行的主机ID
            cmd = self.multiTaskData.get("cmd")  # 获取用户要执行的命令
            if bind_hosts_ids and cmd:
                # 创建一个批量任务
                self.multi_task_obj = models.MultiTask.objects.create(
                    user=self.request.user,
                    task_type=0,
                    content=cmd
                )

                # 创建批量任务详细信息
                multi_task_detail_objs = []
                for bind_host_id in set(bind_hosts_ids):
                    multi_task_detail_objs.append(
                        models.MultiTaskDetail(
                            multi_task=self.multi_task_obj,
                            bind_host_id=bind_host_id,
                            result="init",
                        ))
                models.MultiTaskDetail.objects.bulk_create(multi_task_detail_objs)
                subprocess.Popen(
                    f"{settings.MULTI_TASK_RUN_SCRIPT_INTERPRETER} {settings.MULTI_TASK_RUN_SCRIPT} {self.multi_task_obj.id}",
                    shell=True)
                self.status = True  # 批量任务执行成功
            else:
                self.errors.append({"invalid": "批量任务请求参数不全！"})
        if isCancel == "1":
            self.cancel_multi_task()

    @atomic
    def file_transfer(self):
        """批量文件传输"""
        isCancel = self.multiTaskData.get("isCancel")  # 获取用户是否想要终止任务
        if isCancel == "0":
            bind_hosts_ids = self.multiTaskData.get("bind_hosts_ids")  # 获取用户要批量执行的主机ID
            file_name = self.multiTaskData.get("file_name")  # 获取用户要传输的文件名称
            if bind_hosts_ids and file_name:
                ip = self.request.META.get('HTTP_X_FORWARDED_FOR', self.request.META['REMOTE_ADDR'])
                related_file_path = os.path.join(str(self.request.user.id), str(ip), str(file_name))
                # 创建一个批量任务
                self.multi_task_obj = models.MultiTask.objects.create(
                    user=self.request.user,
                    task_type=1,
                    content=related_file_path
                )

                # 创建批量任务详细信息
                multi_task_detail_objs = []
                for bind_host_id in set(bind_hosts_ids):
                    multi_task_detail_objs.append(
                        models.MultiTaskDetail(
                            multi_task=self.multi_task_obj,
                            bind_host_id=bind_host_id,
                            result="init",
                        ))
                models.MultiTaskDetail.objects.bulk_create(multi_task_detail_objs)
                subprocess.Popen(
                    f"{settings.MULTI_TASK_RUN_SCRIPT_INTERPRETER} {settings.MULTI_TASK_RUN_SCRIPT} {self.multi_task_obj.id}",
                    shell=True)
                self.status = True  # 批量任务执行成功
            else:
                self.errors.append({"invalid": "批量任务请求参数不全！"})
        if isCancel == "1":
            self.cancel_multi_task()

    def run(self):
        """执行批量任务"""
        multi_task_func = getattr(self, self.multiTaskData.get("multiTaskType"))
        multi_task_func()
        return self.status, self.multi_task_obj
