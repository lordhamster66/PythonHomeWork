from django.db import models


# Create your models here.

class User(models.Model):
    """用户表"""
    username = models.CharField(max_length=16, unique=True, verbose_name="用户名")
    pwd = models.CharField(max_length=64, verbose_name="密码")
    qq = models.IntegerField(verbose_name="QQ号")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"
