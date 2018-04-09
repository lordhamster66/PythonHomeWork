#!/usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
from .base import BasePlugin
from lib.response import BaseResponse


class BasicPlugin(BasePlugin):

    def linux(self):
        response = BaseResponse()
        try:
            ret = {
                'os_platform': self.os_platform,
                'os_version': self.os_version,
                'hostname': self.os_hostname,
            }
            response.data = ret
        except Exception as e:
            msg = "%s BasicPlugin Error:%s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())

        return response

    def windows(self):  # todo try to make it
        response = BaseResponse()
        response.status = False
        response.message = "Windows collect function has not been implemented yet"
        return response
