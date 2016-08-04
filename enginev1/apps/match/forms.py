from django import forms

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

    colnames = forms.CharField(
        required=True,
        label="Enter columns to match on (separated by commas)",
        initial="gender,location"
    )

    k_size = forms.CharField(
        required=True,
        label="Enter cluster size.",
        initial="5"
    )
