#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib.log import Logger
from config import settings


class BasePlugin(object):
    def __init__(self, hostname=''):
        self.logger = Logger()
        self.test_mode = settings.TEST_MODE
        self.mode_list = ['agent', 'salt', 'ssh']
        if hasattr(settings, 'MODE'):
            self.mode = settings.MODE
        else:
            self.mode = 'agent'
        self.hostname = hostname

    def salt(self, cmd, ):
        import salt.client

        local = salt.client.LocalClient()
        result = local.cmd(self.hostname, 'cmd.run', [cmd])
        return result[self.hostname]

    def ssh(self, cmd):
        import paramiko

        private_key = paramiko.RSAKey.from_private_key_file(settings.SSH_PRIVATE_KEY)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, port=settings.SSH_PORT, username=settings.SSH_USER, pkey=private_key)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        ssh.close()
        return result

    def agent(self, cmd):
        import subprocess

        output = subprocess.getoutput(cmd)
        return output

    @property
    def os_platform(self):
        """
        获取系统平台
        :return:
        """
        if self.test_mode:
            output = 'linux'
        else:
            output = self.exec_shell_cmd('uname')
        return output.strip()

    @property
    def os_version(self):
        """
        获取系统版本
        :return:
        """
        if self.test_mode:
            output = """CentOS release 6.6 (Final)\nKernel \r on an \m"""
        else:
            output = self.exec_shell_cmd('cat /etc/issue')
        result = output.strip().split('\n')[0]
        return result

    @property
    def os_hostname(self):
        """
        获取主机名
        :return:
        """
        if self.test_mode:
            output = 'c1.com'
        else:
            output = self.exec_shell_cmd('hostname')
        return output.strip()

    def exec_shell_cmd(self, cmd):
        if self.mode not in self.mode_list:
            raise Exception("settings.mode must be one of ['agent', 'salt', 'ssh']")
        func = getattr(self, self.mode)
        output = func(cmd)
        return output

    def execute(self):
        if hasattr(self, self.os_platform):
            execute_func = getattr(self, self.os_platform)
            return execute_func()
        else:
            raise Exception("There is no execute function for this os platform!Please make it")

    def linux(self):
        raise Exception('You must implement linux method.')

    def windows(self):
        raise Exception('You must implement windows method.')
