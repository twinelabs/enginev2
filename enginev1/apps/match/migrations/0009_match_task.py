# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-07 18:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0008_auto_20160819_0441'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='task',
            field=models.CharField(default='assign', max_length=100),
            preserve_default=False,
        ),
    ]
