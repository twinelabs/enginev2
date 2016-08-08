from django import forms

from enginev1.apps.dataset.models import DataTable, DataColumn

class MatchForm(forms.Form):

    def __init__(self, client, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)

        self.fields['data_tables_single'] = forms.ModelChoiceField(
            queryset = DataTable.objects.filter(client=client)
        )
        self.fields['data_tables_multiple'] = forms.ModelMultipleChoiceField(
            queryset = DataTable.objects.filter(client=client)
        )

        self.fields['columns'] = forms.ModelMultipleChoiceField(
            queryset = DataColumn.objects.filter(data_table__client=client),
            widget=forms.CheckboxSelectMultiple
        )


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
