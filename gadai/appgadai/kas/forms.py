from django import forms
from gadai.appgadai.models import KasBank, MutasiKas

class FormPindahbuku(forms.Form):
    rekening_asal = forms.ModelChoiceField(queryset=KasBank.objects.all())
    rekening_tujuan = forms.ModelChoiceField(queryset=KasBank.objects.all())
    tanggal = forms.DateField(widget=forms.TextInput(attrs={'size': 10}))
    nilai = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    keterangan = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}))
    nomor = forms.CharField(max_length=20, required=False)


class MutasiKasForm(forms.ModelForm):
    pengeluaran = forms.BooleanField(required=False, help_text="Beri Check jika Pengeluaran kas")
    tanggal = forms.DateField(widget=forms.TextInput(attrs={'size': 10}))
    keterangan = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}))
    nilai = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    class Meta:
        model = MutasiKas
        fields = ['pengeluaran','tanggal', 'kasbank','nilai','keterangan','nobukti','akun']

