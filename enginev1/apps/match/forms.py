from django import forms

class MatchGroupForm(forms.Form):

    # Name of match (object field)
    name = forms.CharField(
        required=True,
        label="Match name"
    )

    # Cluster algorithm
    ALGO_CHOICES = [
        ('greedy', 'Quick and simple result'),
        ('greedy_adaptive', 'Thorough search'),
        ('random', 'Ignore rules - random assignment')
    ]

    algo = forms.ChoiceField(
        choices = ALGO_CHOICES,
        required = True,
        label = 'Select algorithm.',
        widget= forms.RadioSelect
    )

    # Size of cluster/assign group
    k_size = forms.IntegerField(
        required = True,
        label = "Enter group size",
        max_value = 10,
        min_value = 1,
        initial = 5
    )


class MatchAssignForm(forms.Form):

    # Name of match (object field)
    name = forms.CharField(
        required=True,
        label="Match name"
    )

    # Direction for assignment. In config: 'assign_direction'
    DIRECTION_CHOICES = [
        ('onetomany', 'Match each item in Dataset #1 to multiple items in Dataset #2'),
        ('manytoone', 'Match multiple items in Dataset #1 to each item in Dataset #2'),
    ]

    direction = forms.ChoiceField(
        choices=DIRECTION_CHOICES,
        required = False,
        label='Select direction for assignment.',
        widget= forms.RadioSelect
    )

    # T/F duplicates for assignment. In config: 'assign_duplicates'
    DUPLICATES_CHOICES = [
        (True, 'Allow duplicates.'),
        (False, 'Do not allow duplicates'),
    ]

    duplicates = forms.ChoiceField(
        choices=DUPLICATES_CHOICES,
        required = False,
        label='Are duplicates allowed in assignment?',
        widget= forms.RadioSelect
    )





