from __future__ import unicode_literals

from django.db import models
from enginev1.apps.welcome.models import Client
from django_hstore import hstore


class DataTable(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)

    n_rows = models.PositiveIntegerField()
    n_cols = models.PositiveIntegerField()

    data = hstore.SerializedDictionaryField()
    objects = hstore.HStoreManager()

    class Meta:
        app_label = 'dataset'

    def __str__(self):
        return self.name


class DataColumn(models.Model):
    data_table = models.ForeignKey(DataTable, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    custom_name = models.CharField(max_length=100)
    dtype = models.CharField(max_length=100)

    order_original = models.PositiveIntegerField()
    order_custom = models.PositiveIntegerField()

    n_unique = models.PositiveIntegerField()
    n_nonblank = models.PositiveIntegerField()

    class Meta:
        app_label = 'dataset'

    def __str__(self):
        return self.name
