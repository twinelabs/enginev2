# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-04 18:59
from __future__ import unicode_literals

from django.db import migrations
import django_hstore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0005_auto_20160804_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='result',
            field=django_hstore.fields.DictionaryField(),
        ),
    ]