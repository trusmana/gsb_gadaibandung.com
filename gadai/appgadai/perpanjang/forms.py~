from django import forms
from django.forms import ModelForm
from gadai.appgadai.models import Perpanjang

class Edit_PerpanjangForm(ModelForm):
    class Meta:
        model = Perpanjang
        fields = ('agkredit','gerai','tanggal','nilai','terlambat','hitung_hari','jenis_barang','bea_simpan','status','jw',
        'jw_kendaraan','terlambat_kendaraan','beasimpan_kendaraan','hitung_hari_kendaraan','bunga_denda','bunga_jasa')
        widgets = {
            'agkredit' : forms.HiddenInput(),           
        }

class KwitansiReturForm(forms.ModelForm):
    retur = forms.BooleanField(required=False)

    class Meta:
        model = Perpanjang
        exclude = ('agkredit')
