from django import forms

from enginev1.apps.dataset.models import DataTable, DataColumn

class MatchForm(forms.Form):

    def __init__(self, client, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)

        self.data_tables = [
            (data_table.id, data_table.name) for data_table in DataTable.objects.filter(client=client)
        ]

        self.data_columns = [
            (data_column.data_table.id, data_column.id, data_column.name, data_column.dtype) for data_column in DataColumn.objects.filter(data_table__client=client)
        ]

        self.cluster_rule_string_options = ["Different", "Any", "Similar"]
        self.cluster_rule_numeric_options = ["Maximize", "Any", "Minimize"]
        self.cluster_algos = ["greedy", "greedy_adapt", "random"]

    # Name of match (object field)
    name = forms.CharField(
        required=True,
        label="Match name"
    )

    # Matching task. In config: 'task'
    TASK_CHOICES = [
        ('cluster', 'Cluster/Pair (within 1 dataset)'),
        ('assign', 'Assign (across 2 datasets) - NOT YET IMPLEMENTED'),
    ]

    task = forms.ChoiceField(
        choices=TASK_CHOICES,
        required = True,
        label='Select matching operation.',
        widget= forms.RadioSelect
    )

    # Size of cluster/assign group. In config: 'k_size'
    k_size = forms.IntegerField(
        required=True,
        label="Enter cluster size.",
        max_value=10,
        min_value=1,
        initial=5
    )

    # Direction for assignment. In config: 'assign_direction'
    ASSIGN_DIRECTION_CHOICES = [
        ('onetomany', 'Match each item in Dataset #1 to multiple items in Dataset #2'),
        ('manytoone', 'Match multiple items in Dataset #1 to each item in Dataset #2'),
    ]

    assign_direction = forms.ChoiceField(
        choices=ASSIGN_DIRECTION_CHOICES,
        required = False,
        label='Select direction for assignment.',
        widget= forms.RadioSelect
    )

    # T/F duplicates for assignment. In config: 'assign_duplicates'
    ASSIGN_DUPLICATES_CHOICES = [
        (True, 'Allow duplicates.'),
        (False, 'Do not allow duplicates'),
    ]

    assign_duplicates = forms.ChoiceField(
        choices=ASSIGN_DUPLICATES_CHOICES,
        required = False,
        label='Are duplicates allowed in assignment?',
        widget= forms.RadioSelect
    )





