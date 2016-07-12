from __future__ import unicode_literals

from django.db import models
from enginev1.apps.welcome.models import Client
from django_hstore import hstore


class GenericDatasetObject(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    data = hstore.DictionaryField()
    objects = hstore.HStoreManager()

    class Meta:
        app_label = 'dataset'
        abstract = True

    def __str__(self):
        obj_attrs = [k + ": " + self.data[k] for k in self.data.keys()[:3]]
        return "Data Item [" + ", ".join(obj_attrs) + " ... ]"


class Alpha(GenericDatasetObject):

    class Meta:
        verbose_name_plural = 'Dataset #1 Objects'


class Beta(GenericDatasetObject):

    class Meta:
        verbose_name_plural = 'Dataset #2 Objects'
