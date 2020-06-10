from django import forms
from gadai.appgadai.models import Barang,Nasabah,Tbl_Cabang
from gadai.appgadai.widgets import MultipleSelectWithPop
from chosen import forms as chosenforms
import datetime
from gadai.appkeuangan.models import Gabungan_Cabang
from django.utils.safestring import mark_safe

class FilterPermintaanForm(forms.Form):
    #report = forms.ChoiceField(widget = forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'id_report'}), choices = JENIS_REPORT)
    id_cabang = forms.ModelChoiceField(label = "CABANG",queryset=Tbl_Cabang.objects.all())
    #id_cabang = chosenforms.ChosenChoiceField(widget=chosenforms.ChosenSelect({'class': 'id_cabang'}),choices = GERAI_PILIH)
    start_date = forms.DateField(initial= datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,'readonly':'false'}, format="%Y-%m-01"))
    end_date = forms.DateField(initial= datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,'readonly':'false'}, format="%Y-%m-%d"))


class HorizRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
            """Outputs radios"""
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self])) 
class BarangForm(forms.ModelForm):    
    class Meta:
        model = Barang
        fields = ('barang_masuk', 'barang_keluar', 'ruangan', 'no_rak', 'row')

class chosen_cabangForm(forms.Form):
    gabungan = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices= Gabungan_Cabang,initial = '0')
    id_cabang = forms.CharField(max_length=60, 
            widget=forms.TextInput(attrs={'class': 'kode_cabang','size':12}),
            required = False)
    end_date  = forms.DateField(initial=datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,'readonly':'true'}, format="%d-%m-%Y"))
    start_date = forms.DateField(initial = datetime.date.today(),widget=forms.widgets.DateInput(attrs={'size': 12,'readonly':'true'}, format="%d-%m-%Y"))
