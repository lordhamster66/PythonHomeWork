#!/usr/bin/env python
# -*- coding:utf-8 -*-
from src.client import AutoAgent
from src.client import AutoSSH
from src.client import AutoSalt
from config import settings

# 资产采集模式
ASSET_COLLECT_MODE = {
    "agent": AutoAgent,
    "ssh": AutoSSH,
    "salt": AutoSalt,
}


def client():
    if settings.MODE in ASSET_COLLECT_MODE:
        cli = ASSET_COLLECT_MODE[settings.MODE]()
    else:
        raise Exception('请配置资产采集模式，如：ssh、agent、salt')
    cli.process()
