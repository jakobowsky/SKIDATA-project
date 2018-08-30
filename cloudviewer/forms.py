from django.forms import ModelForm
from django import forms

CHOICES_CLOUD = (('EU_DEMO',"Demo Cloud"),("EU_LIVE","EU_LIVE"),("US_LIVE","US_LIVE"),("EU_PA_LIVE","EU_PA_LIVE"),("AU_Live","AU_Live"))
CHOICES_REPORTS= ((1,'List of tenants'),(2,'List of all products per Cloud, including active/inactive'),(3,'List of all tenants, active/inactive for a products'),(4,'List of tenants and service boxes'))
#class which is used as a form in html and in views.py
#it is used in home page for choosing the cloud and report
class CloudAndReportForm(forms.Form):
    cloud = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=CHOICES_CLOUD
    )
    report = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'class':'form-control'}),
        choices=CHOICES_REPORTS
    )
