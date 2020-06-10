from django import forms
from django.forms import fields, models, formsets, widgets
from gadai.appgadai.models import Taksir,STATUS_AKTIFASI

class TaksirForm(forms.Form):
    #type = forms.CharField(max_length=500,widget=forms.TextInput(attrs={'size':20}))
    type = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 20}),max_length=500)
    spesifikasi = forms.CharField(max_length=250)
    harga_baru = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    harga_pasar = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    maxpinjaman = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    tglupdate =forms.DateField(widget=forms.TextInput(attrs={'size': 10}))
    status = forms.ChoiceField(widget=forms.Select(),choices=STATUS_AKTIFASI)

class TaksirEditForm(models.ModelForm):
    class Meta:
        model = Taksir
