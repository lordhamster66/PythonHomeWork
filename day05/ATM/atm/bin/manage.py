#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Breakering
import os,sys
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
from core import main

if __name__ == "__main__":
    main.manage_action()
