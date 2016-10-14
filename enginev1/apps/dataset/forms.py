from django import forms

class UploadCSVForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Name your Data Set",
        initial="(e.g. Employees)"
    )
    csv_file = forms.FileField(
        label='Select a CSV file to upload'
    )
