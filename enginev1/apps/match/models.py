from __future__ import unicode_literals

from django.db import models
from enginev1.apps.welcome.models import Client
from django_hstore import hstore


class Config(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    params = hstore.DictionaryField()
    objects = hstore.HStoreManager()

    class Meta:
        app_label = 'match'

    def __str__(self):
        return self.name


class Result(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    run_start = models.DateTimeField()
    run_end = models.DateTimeField()

    output = hstore.DictionaryField()
    objects = hstore.HStoreManager()

    class Meta:
        app_label = 'match'

    def __str__(self):
        return self.name