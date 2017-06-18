#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/14
"""RPC服务器主要模块"""
import pika
import json
import threading
import os
from conf import settings
from core import mylogger

# 生成日志对象
action_logger = mylogger.Mylogger(settings.ACTION_LOGPATH, "action", settings.LOG_LEVEL).get_logger()


class RpcServer(object):
    """RPC服务器类"""

    def __init__(self, rpc_q):
        """初始化"""
        self.rpc_q = rpc_q  # 初始化一个服务器RPC队列
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_IP))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.rpc_q)
        self.task = {}  # 任务结果存放处

    def run(self, data_header, ch, method, props, logger, *args):
        """运行命令功能"""
        cmd = data_header["cmd"]
        task_id = props.message_id
        self.task[task_id] = "任务处理中！"  # 初始化任务状态
        result = os.popen(cmd).read()  # 执行任务并获取任务结果，可能需要点时间
        if len(result) == 0:  # 说明该任务没有返回结果，或者出错
            result = "cmd has no output!"
        self.task[task_id] = result  # 存储任务结果
        logger.info("excute %s" % cmd)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def check_task(self, data_header, ch, method, props, logger, *args):
        task_id = data_header["task_id"]
        if self.task.get(task_id):
            result = self.task.get(task_id)
        else:
            result = "没有此类任务ID!"
        # 给客户端发送信息
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id=props.correlation_id),
            body=result
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def cmd_parser(self, ch, method, props, body):
        """命令解析功能"""
        data_header = json.loads(body.decode())
        if hasattr(self, data_header["action"]):
            func = getattr(self, data_header["action"])
            t = threading.Thread(target=func, args=(data_header, ch, method, props, action_logger))
            t.start()

    def start(self):
        """开启服务器功能"""
        self.channel.basic_consume(self.cmd_parser, queue=self.rpc_q)
        print("\033[32;1m服务器启动，等待客户端指令！\033[0m")
        self.channel.start_consuming()
