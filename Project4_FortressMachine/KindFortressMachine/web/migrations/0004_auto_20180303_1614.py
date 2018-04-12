# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-03 16:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20180303_1612'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hostgroup',
            name='hosts',
        ),
        migrations.AddField(
            model_name='hostgroup',
            name='bind_hosts',
            field=models.ManyToManyField(blank=True, to='web.BindHost', verbose_name='绑定的带账号的主机'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bind_hosts',
            field=models.ManyToManyField(blank=True, to='web.BindHost', verbose_name='绑定的带账号的主机'),
        ),
    ]
