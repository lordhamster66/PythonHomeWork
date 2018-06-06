# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-03 16:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BindHost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Host', verbose_name='绑定的主机')),
                ('remote_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.RemoteUser', verbose_name='绑定的远程用户')),
            ],
            options={
                'verbose_name_plural': '绑定账号的主机',
            },
        ),
        migrations.AlterUniqueTogether(
            name='bindhost',
            unique_together=set([('host', 'remote_user')]),
        ),
    ]