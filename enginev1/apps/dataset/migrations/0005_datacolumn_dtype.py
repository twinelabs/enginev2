# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-06 11:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0004_auto_20160804_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='datacolumn',
            name='dtype',
            field=models.CharField(default='object', max_length=100),
            preserve_default=False,
        ),
    ]
