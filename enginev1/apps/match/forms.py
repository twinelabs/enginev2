from django import forms

from enginev1.apps.dataset.models import DataTable, DataColumn

class MatchForm(forms.Form):

    def __init__(self, client, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)

        self.data_tables = [
            (data_table.id, data_table.name) for data_table in DataTable.objects.filter(client=client)
        ]

        self.data_columns = [
            (data_column.id, data_column.name, data_column.dtype) for data_column in DataColumn.objects.filter(data_table__client=client)
        ]

    name = forms.CharField(
        required=True,
        label="Match name"
    )

    CLUSTER_OR_ASSIGN = [
        ('cluster', 'Cluster/Pair (within 1 dataset)'),
        ('assign', 'Assign (across 2 datasets) - NOT YET IMPLEMENTED'),
    ]

    task = forms.ChoiceField(
        choices=CLUSTER_OR_ASSIGN,
        required = True,
        label='Select matching operation.',
        widget= forms.RadioSelect
    )

    k_size = forms.IntegerField(
        required=True,
        label="Enter cluster size.",
        max_value=10,
        min_value=2,
        initial=5
    )


#        self.columns_full = [
#            (column.id, column.name, column.type) for column in DataColumn.objects.filter(data_table__client=client)
#        ]
