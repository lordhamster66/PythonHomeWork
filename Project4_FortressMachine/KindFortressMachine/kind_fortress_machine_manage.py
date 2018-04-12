#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2018/3/3
import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KindFortressMachine.settings")
    import django

    django.setup()

    from backend import main
    obj = main.HostManage()
    obj.interactive()
