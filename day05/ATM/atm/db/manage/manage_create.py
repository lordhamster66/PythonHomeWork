#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:Breakering
import json
import os
path = os.path.dirname(os.path.abspath(__file__))
manage_dict = {
    "id": 1,
    "username": "Breakering",
    "password": "666666",
    "enroll_date": "2017-04-23",
    "expire_date": "2021-01-22",
    "status": 0
}

json.dump(manage_dict, open(os.path.join(path, "%s.json" % manage_dict["username"]), "w", encoding="utf-8"))
