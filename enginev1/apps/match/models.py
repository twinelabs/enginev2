from django.db import models
from enginev1.apps.welcome.models import Client
from enginev1.apps.dataset.models import DataTable
from django_hstore import hstore

from .entwine import entwine

import json
import pdb

class Match(models.Model):
    """ Match object. Contains match configuration and results.
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    task = models.CharField(max_length=100)

    data_tables = models.ManyToManyField(
        DataTable,
        through='MatchDataTable',
        related_name='matches'
    )

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
        """ List of names of related data tables, ordered.
        """
        mdts = MatchDataTable.objects.filter(match=self).order_by('data_table_order')
        data_table_names = [mdt.data_table.name for mdt in mdts]
        return data_table_names


    def result_data(self):
        """ Match results, structured for viewing/manipulation.
        """
        if self.result == {}:
            return None

        if self.task == "assign":
            return self.assign_result_data()
        else:
            return self.group_result_data()


    def group_result_data(self):
        """ Match results for GROUP matching, with following structure:
        [
            [
                [ [attr0, val0], [attr1, val1], ... ],  # --> group0_member0
                [ [attr0, val0], [attr1, val1], ... ],  # --> group0_member1
                ...
            ],
            [
                [ [attr0, val0], [attr1, val1], ... ],  # --> group1_member0
                ...
            ],
            ...
        ]
        """

        results = json.loads(self.result['results'])
        dt = self.data_tables.all()[0]
        data = dt.data['data']

        matched_columns = [c['columns'][0] for c in self.config['match']['components']]

        result_data = []
        for i_group, group in enumerate(results):
            this_group_data = []

            for i_member, member_row in enumerate(group):
                member_data = data[member_row]
                unmatched_columns = [col for col in member_data.keys() if col not in matched_columns]

                this_member_data = [["Group #", str(i_group + 1)]]
                this_member_data += [[col_name, member_data[col_name]] for col_name in matched_columns]
                this_member_data += [[col_name, member_data[col_name]] for col_name in unmatched_columns]

                this_group_data.append(this_member_data)

            result_data.append(this_group_data)

        return result_data


    def assign_result_data(self):
        """ Match results for ASSIGN matching, with following structure:
        [
            [
                [ [attr_A, val_A], [attr_B, val_B], ... ],  # --> B_member0
                [ [attr_X, val_X], [attr_Y, val_Y], ... ],  # --> matched A_member0
                [ [attr_X, val_X], [attr_Y, val_Y], ... ],  # --> matched A_member1
                ...
            ],
            [
                [ [attr_A, val_A], [attr_B, val_B], ... ],  # --> B_member1
                [ [attr_X, val_X], [attr_Y, val_Y], ... ],  # --> matched A_member0
                ...
            ],
            ...
        ]
        """

        results = json.loads(self.result['results'])

        dt_A = self.data_tables.all()[0]
        data_A = dt_A.data['data']
        columns_A = dt_A.header()

        dt_B = self.data_tables.all()[1]
        data_B = dt_B.data['data']
        columns_B = dt_B.header()

        result_data = []
        for i_group, group in enumerate(results):
            elem_B = [[colname, data_B[i_group][colname]] for colname in columns_B]
            this_assignment_data = [elem_B]

            for i_member, member_row in enumerate(group):
                elem_A = [[colname, data_A[member_row][colname]] for colname in columns_A]
                this_assignment_data.append(elem_A)

            result_data.append(this_assignment_data)

        return result_data


    def result_header(self):
        if self.result == {}:
            return None

        if self.task == "assign":
            return self.assign_result_header()
        else:
            return self.group_result_header()


    def group_result_header(self):
        """ Header for GROUP results: data table column headers.
        """
        result_data = self.result_data()
        first_member = result_data[0][0]
        header = [col_val[0] for col_val in first_member]
        return header


    def assign_result_header(self):
        """ Header for ASSIGN results: dataset_B columns + "" + dataset_A columns.
        """
        dt_A = self.data_tables.all()[0]
        columns_A = dt_A.header()

        dt_B = self.data_tables.all()[1]
        columns_B = dt_B.header()

        header = columns_B + [""] + columns_A
        return header


class MatchDataTable(models.Model):
    """ ManyToMany Through model between Match and DataTable to preserve DataTable order
    """

    match = models.ForeignKey(Match)
    data_table = models.ForeignKey(DataTable)

    data_table_order = models.PositiveIntegerField()

    class Meta:
        ordering = ('data_table_order',)
