from django.db import models
from enginev1.apps.welcome.models import Client
from enginev1.apps.dataset.models import DataTable, DataColumn
from django_hstore import hstore


class Match(models.Model):
    """ Match object. Contains match configuration and results.
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    data_tables = models.ManyToManyField(DataTable, related_name='matches')

    config = hstore.SerializedDictionaryField()

    run_start = models.DateTimeField(null=True, blank=True)
    run_end = models.DateTimeField(null=True, blank=True)
    result = hstore.DictionaryField()

    class Meta:
        app_label = 'match'

    def __str__(self):
        return self.name


    def has_results(self):
        return(not(self.result == {}))

