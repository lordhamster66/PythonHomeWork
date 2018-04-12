#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2018/3/25
import sys, os, multiprocessing
import paramiko


def file_test(ret):
    with open("multi_task_run.txt", "w") as f:
        f.write(f"{ret}")


def cmd_run(multi_task_detail_obj_id):
    """连上远程主机并执行命令"""
    import django

    django.setup()
    from web import models
    from django.utils.timezone import datetime

    # 获取批量任务详细信息对象
    multi_task_detail_obj = models.MultiTaskDetail.objects.filter(id=multi_task_detail_obj_id).first()
    try:
        # 创建SSH对象
        ssh = paramiko.SSHClient()
        # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        ssh.connect(
            hostname=multi_task_detail_obj.bind_host.host.ip_adr,
            port=multi_task_detail_obj.bind_host.host.port,
            username=multi_task_detail_obj.bind_host.remote_user.username,
            password=multi_task_detail_obj.bind_host.remote_user.password,
            timeout=10  # 10秒超时时间
        )

        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(multi_task_detail_obj.multi_task.content)
        # 获取命令结果(包含标准输出和标准错误)
        result = f"{stdout.read().decode()}\n{stderr.read().decode()}"
        multi_task_detail_obj.result = result
        multi_task_detail_obj.status = 1  # 修改状态为执行成功
        end_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        multi_task_detail_obj.end_time = end_time  # 命令执行的终止时间
        multi_task_detail_obj.save()
        # 关闭连接
        ssh.close()
    except Exception as e:
        multi_task_detail_obj.result = e
        multi_task_detail_obj.status = 2
        end_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        multi_task_detail_obj.end_time = end_time
        multi_task_detail_obj.save()


def file_transfer_run(multi_task_detail_obj_id):
    """连上远程主机并传输文件"""
    import django
    import os
    django.setup()
    from web import models
    from django.utils.timezone import datetime
    from django.conf import settings

    # 获取批量任务详细信息对象
    multi_task_detail_obj = models.MultiTaskDetail.objects.filter(id=multi_task_detail_obj_id).first()
    try:
        transport = paramiko.Transport(
            (multi_task_detail_obj.bind_host.host.ip_adr,
             multi_task_detail_obj.bind_host.host.port)
        )
        transport.connect(
            username=multi_task_detail_obj.bind_host.remote_user.username,
            password=multi_task_detail_obj.bind_host.remote_user.password,
        )
        sftp = paramiko.SFTPClient.from_transport(transport)
        file_path = os.path.join(settings.MULTI_TASK_FILE_TRANSFER_DIR, multi_task_detail_obj.multi_task.content)
        sftp.put(file_path, f'{os.path.basename(file_path)}')
        transport.close()
        multi_task_detail_obj.result = "文件上传成功"
        multi_task_detail_obj.status = 1  # 修改状态为执行成功
        end_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        multi_task_detail_obj.end_time = end_time  # 命令执行的终止时间
        multi_task_detail_obj.save()
    except Exception as e:
        multi_task_detail_obj.result = e
        multi_task_detail_obj.status = 2
        end_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        multi_task_detail_obj.end_time = end_time
        multi_task_detail_obj.save()


if __name__ == '__main__':
    # 定义批量任务字段跟执行函数的关系
    multi_task_run_func_dict = {
        "cmd": cmd_run,
        "file_transfer": file_transfer_run
    }
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(base_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KindFortressMachine.settings")
    import django

    django.setup()
    from web import models

    multi_task_obj_id = sys.argv[1]  # 脚本接收到的批量任务对象ID
    multi_task_obj = models.MultiTask.objects.filter(id=multi_task_obj_id).first()
    task_type = multi_task_obj.get_task_type_display()  # 批量任务类型
    multi_task_run_func = multi_task_run_func_dict[task_type]  # 获取批量任务执行函数
    pool = multiprocessing.Pool()  # 进程池
    for multi_task_detail_obj in multi_task_obj.multitaskdetail_set.all():
        pool.apply_async(multi_task_run_func, args=(multi_task_detail_obj.id,))
    pool.close()
    pool.join()
