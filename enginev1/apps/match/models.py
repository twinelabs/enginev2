from __future__ import unicode_literals

from django.db import models
from enginev1.apps.welcome.models import Client
from enginev1.apps.dataset.models import DataTable
from django_hstore import hstore


class Match(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    data_tables = models.ManyToManyField(DataTable)

    config = hstore.DictionaryField()

    run_start = models.DateTimeField(null=True, blank=True)
    run_end = models.DateTimeField(null=True, blank=True)
    result = hstore.DictionaryField()

    class Meta:
        app_label = 'match'

    def __str__(self):
        return self.name
