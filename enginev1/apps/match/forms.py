from django import forms

from enginev1.apps.dataset.models import DataTable, DataColumn

class MatchForm(forms.Form):

    name = forms.CharField(
        required=True,
        label="Match name"
    )

    CLUSTER_OR_ASSIGN = [
        ('cluster', 'Cluster/Pair (within 1 dataset)'),
        ('assign', 'Assign (across 2 datasets)'),
    ]

    task = forms.ChoiceField(
        choices=CLUSTER_OR_ASSIGN,
        required = True,
        label='Select matching operation.'
    )

    data_tables = forms.ModelMultipleChoiceField(
        queryset=DataTable.objects
    )

    columns = forms.ModelMultipleChoiceField(
        queryset=DataColumn.objects
    )

    k_size = forms.CharField(
        required=True,
        label="Enter cluster size.",
        initial="5"
    )
