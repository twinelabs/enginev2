from __future__ import unicode_literals

from django.db import models
from enginev1.apps.welcome.models import Client
from django_hstore import hstore


class Alpha(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    data = hstore.DictionaryField()
    objects = hstore.HStoreManager()

    class Meta:
        verbose_name_plural = 'Dataset #1 Objects'
        app_label = 'dataset'

    def __str__(self):
        return "Dataset #1 Object with keys: " #+ ", ".join(self.data.keys[:5])


class Beta(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    data = hstore.DictionaryField()
    objects = hstore.HStoreManager()

    class Meta:
        verbose_name_plural = 'Dataset #2 Objects'
        app_label = 'dataset'

    def __str__(self):
        return "Dataset #2 Object with keys: " #+ ", ".join(self.data.keys[:5])