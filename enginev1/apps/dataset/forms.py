from django import forms

class UploadCSVForm(forms.Form):
    ALPHA_OR_BETA = [
        ('alpha', 'Dataset #1'),
        ('beta', 'Dataset #2'),
    ]
    alpha_or_beta = forms.ChoiceField(choices=ALPHA_OR_BETA, required = True, label='Select data set to upload into.')
    csv_file = forms.FileField()
