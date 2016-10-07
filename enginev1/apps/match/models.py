from django.db import models
from enginev1.apps.welcome.models import Client
from enginev1.apps.dataset.models import DataTable, DataColumn
from django_hstore import hstore

from .entwine import entwine

import json


class Match(models.Model):
    """ Match object. Contains match configuration and results.
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    task = models.CharField(max_length=100)

    data_tables = models.ManyToManyField(DataTable, related_name='matches')

    config = hstore.SerializedDictionaryField()

    run_start = models.DateTimeField(null=True, blank=True)
    run_end = models.DateTimeField(null=True, blank=True)
    result = hstore.DictionaryField()

    class Meta:
        app_label = 'match'

    def __str__(self):
        return self.name


    def run(self):
        result = entwine.run_from_config(self.config)
        self.result = result
        self.save()


    def data_table_names(self):
        return [dt.name for dt in self.data_tables.all()]


    def results(self):
        if self.result == {}:
            return None

        if self.task == "assign":
            return self.assign_results()
        else:
            return self.group_results()


    def group_results(self):
        results = json.loads(self.result['results'])
        dt = self.data_tables.all()[0]
        data = dt.data['data']

        matched_columns = [c['columns'][0] for c in self.config['match']['components']]

        all_group_data = []
        for i_group, group in enumerate(results):
            this_group_data = []

            for i_member, member_row in enumerate(group):
                member_data = data[member_row]
                unmatched_columns = [col for col in member_data.keys() if col not in matched_columns]

                this_member_data = [[col_name, member_data[col_name]] for col_name in matched_columns]
                this_member_data += [[col_name, member_data[col_name]] for col_name in unmatched_columns]

                this_group_data.append(this_member_data)

            all_group_data.append(this_group_data)

        return all_group_data


    def assign_results(self):
        return True