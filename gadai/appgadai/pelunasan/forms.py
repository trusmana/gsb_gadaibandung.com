from django import forms
from django.forms import ModelForm
from gadai.appgadai.models import*

class Edit_PelunasanForm(ModelForm):
    
    class Meta:
        model = Pelunasan
        
        fields = ('pelunasan','tanggal','nilai','terlambat','denda','bea_jasa','jenis_barang',
        'terlambat_kendaraan','denda_kendaraan','bea_jasa_kendaraan')
        widgets = {
            'pelunasan' : forms.HiddenInput(),
            
        }

