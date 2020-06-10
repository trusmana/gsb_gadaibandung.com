from django import forms
from gadai.appgadai.models import Barang,Nasabah
from gadai.appgadai.widgets import MultipleSelectWithPop

class BarangForm(forms.ModelForm):    
    class Meta:
        model = Barang
        fields = ('barang_masuk', 'barang_keluar', 'ruangan', 'no_rak', 'row')

class AgingForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'size': 12,}, format="%Y-%m-%d"))
