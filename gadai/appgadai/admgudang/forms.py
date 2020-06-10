from django import forms
from django.forms import ModelForm
from gadai.appgadai.models import *
from chosen import forms as chosenforms

class AdmGudangForm(forms.ModelForm):
    tanggal = forms.DateField(widget=forms.widgets.DateInput(attrs={'readonly':'False'}, format="%d-%m-%Y"))
    class Meta:
        model = AdmGudang
        widgets = {
            'adm' : forms.HiddenInput(),
        }
