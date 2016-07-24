from django import forms

class MatchConfigForm(forms.Form):

    name = forms.CharField(
        required=True,
        label="Match name"
    )

    CLUSTER_OR_ASSIGN = [
        ('cluster', 'Cluster/Group Objects (within one dataset)'),
        ('assign', 'Assign Objects (across two datasets)'),
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
