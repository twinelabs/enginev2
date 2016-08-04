# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-03 03:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_hstore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0005_auto_20160803_0227'),
        ('dataset', '0002_auto_20160709_1822'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataColumn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('custom_name', models.CharField(max_length=100)),
                ('order_original', models.PositiveIntegerField()),
                ('order_custom', models.PositiveIntegerField()),
                ('n_unique', models.PositiveIntegerField()),
                ('n_nonblank', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DataTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('n_rows', models.PositiveIntegerField()),
                ('n_cols', models.PositiveIntegerField()),
                ('data', django_hstore.fields.DictionaryField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='welcome.Client')),
            ],
        ),
        migrations.RemoveField(
            model_name='alpha',
            name='client',
        ),
        migrations.RemoveField(
            model_name='beta',
            name='client',
        ),
        migrations.DeleteModel(
            name='Alpha',
        ),
        migrations.DeleteModel(
            name='Beta',
        ),
        migrations.AddField(
            model_name='datacolumn',
            name='data_table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataset.DataTable'),
        ),
    ]