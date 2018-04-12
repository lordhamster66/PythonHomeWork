#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2018/3/25
WEB_SSH_URL = "http://192.168.125.181:4200/"  # web ssh服务地址和端口
WEB_SSH_USER = "king"  # 堡垒机服务器的登录账户
WEB_SSH_PWD = "abc000731"  # 堡垒机服务器的登录密码

# Linux和Windows解释器是为测试准备的，正式上线只需一个任务脚本的执行解释器即可
# Linux运行批量任务脚本的解释器(确保该解释器环境已安装paramiko模块)
# MULTI_TASK_RUN_SCRIPT_INTERPRETER = "/opt/anaconda3/envs/py3-dj/bin/python"
# Windows运行批量任务脚本的解释器(确保该解释器环境已安装paramiko模块)
MULTI_TASK_RUN_SCRIPT_INTERPRETER = "C:/Users/lingx/AppData/Local/conda/conda/envs/py3-dj/python.exe"
