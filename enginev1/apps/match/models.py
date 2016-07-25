from __future__ import unicode_literals

from django.db import models
from enginev1.apps.welcome.models import Client
from django_hstore import hstore

import json


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
    config = models.ForeignKey(Config, on_delete=models.CASCADE, default="")
    name = models.CharField(max_length=100)

    run_start = models.DateTimeField(null=True, blank=True)
    run_end = models.DateTimeField(null=True, blank=True)

    output = hstore.DictionaryField()
    objects = hstore.HStoreManager()

    class Meta:
        app_label = 'match'

    def __str__(self):
        return self.name

    def clusters(self):
        clusters = json.loads(self.output['clusters'])
        return clusters

    def clusters_with_data(self):
        dataset_objs = self.client.alpha_set.all()
        res = [[ str(dataset_objs[i]) for i in cluster] for cluster in self.clusters()]
        return res