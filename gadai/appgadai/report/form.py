from django import forms
from gadai.appgadai.models import *

class BarangForm(forms.ModelForm):
    #no_rak= forms.ChoiceField(widget=forms.Select(),choices=RAK_CHOICES)
    class Meta:
        model = Barang
