from django import forms
from django.forms import ModelForm
from gadai.appgadai.models import BarangLelang,AkadGadai

class BarangLelangForm(forms.ModelForm):
    aglelang =forms.ModelChoiceField(queryset=AkadGadai.objects.all())
    tgl_lelang = forms.DateTimeField(label = "Tanggal Pelelangan",widget=forms.TextInput(attrs={'size': 10}))
    harga_jual = forms.IntegerField(label="Nilai Taksir",widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    nama_pembeli =forms.CharField(widget=forms.TextInput(attrs={'size': 70}))

    class Meta:
        model = BarangLelang
