# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-13 18:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_hstore.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dataset', '0005_datacolumn_dtype'),
        ('welcome', '0006_auto_20160804_0028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('task', models.CharField(max_length=100)),
                ('config', django_hstore.fields.SerializedDictionaryField()),
                ('run_start', models.DateTimeField(blank=True, null=True)),
                ('run_end', models.DateTimeField(blank=True, null=True)),
                ('result', django_hstore.fields.DictionaryField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='welcome.Client')),
            ],
        ),
        migrations.CreateModel(
            name='MatchDataTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_table_order', models.PositiveIntegerField()),
                ('data_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataset.DataTable')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='match.Match')),
            ],
            options={
                'ordering': ('data_table_order',),
            },
        ),
        migrations.AddField(
            model_name='match',
            name='data_tables',
            field=models.ManyToManyField(related_name='matches', through='match.MatchDataTable', to='dataset.DataTable'),
        ),
    ]
