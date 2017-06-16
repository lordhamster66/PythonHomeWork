#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Breakering
import os
import sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
atm_path = os.path.join(path,"atm")
sys.path.append(path)
sys.path.append(atm_path)
from atm.core import main
user_info = {
            "user_dict":{"username":"aa"}
            }
ret = main.consume(user_info,100)
print(ret)