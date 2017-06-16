#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Breakering"
# Date: 2017/6/4
import json
import os
import sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from lib import public

h1 = {
    "host": '192.168.48.20',
    "port": 22,
    "username": 'root'
}
h1_id = public.creat_id()

h2 = {
    "host": '192.168.48.20',
    "port": 22,
    "username": 'hadoop'
}
h2_id = public.creat_id()

json.dump(h1, open("%s.json" % h1_id, "w", encoding="utf-8"))
json.dump(h2, open("%s.json" % h2_id, "w", encoding="utf-8"))
