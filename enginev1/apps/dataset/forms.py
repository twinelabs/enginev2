from django import forms

class UploadCSVForm(forms.Form):
    name = forms.CharField(max_length=100)
    csv_file = forms.FileField(label='Select a CSV file to upload')
