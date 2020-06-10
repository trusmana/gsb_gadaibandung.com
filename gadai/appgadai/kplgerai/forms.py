from django import forms
from django.forms.formsets import formset_factory
from chosen import forms as chosenforms
from gadai.appgadai.models import *
from django.forms.formsets import formset_factory
from django.utils.safestring import mark_safe

class PriceListForm(forms.Form):
    taksir = chosenforms.ChosenModelChoiceField(label = "Price List",queryset=Taksir.objects.filter(status = '2'))

class KepalaGeraiForm(forms.ModelForm):
    tanggal = forms.DateField(initial= datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,'readonly':'true'}, format="%d-%m-%Y"))
    class Meta:
        model = KepalaGerai

GERAI_PILIH =(
    ('','-------'),('BANDUNG','BANDUNG'),('JAKARTA','JAKARTA'),('SUCI','SUCI'),('DIPATIUKUR','DIPATIUKUR'),('BALUBUR','BALUBUR'),
    ('GERLONG_HILIR','GERLONG HILIR'),('KOPO','KOPO'),('CIBIRU','CIBIRU'),('CIPACING','CIPACING'),('JATINANGOR','JATINANGOR'),
    ('CIMAHI','CIMAHI'),('BUAH_BATU','BUAH BATU'),('CIHANJUANG','CIHANJUANG'),('MARANATA','MARANATA'),('KIARACONDONG','KIARACONDONG'),
    ('CIREBON','CIREBON'),('CIUMBULEUIT','CIUMBULEUIT'),('UJUNGBERUNG','UJUNGBERUNG'),
)

class HorizRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
            """Outputs radios"""
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class MainJurnalForm(forms.Form):
    nobukti = forms.CharField(label = "Nomor Bukti",max_length=12)
    tgl_trans = forms.DateTimeField(initial = datetime.date.today)
    diskripsi = forms.CharField(label = "Keterangan",max_length=200, required=False, widget=forms.TextInput(attrs={'size': 50}))
    status_jurnal = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=JENIS_JURNAL)
    #nilai = forms.FloatField(widget=forms.TextInput(attrs={'size': 9, 'class': 'uang', 'value': '0', 'alt': 'integer'}),required = False)

class Tbl_TransaksiForm(forms.Form):
    #is_debet = forms.BooleanField(widget=forms.HiddenInput(), required = False)
    id_coa = chosenforms.ChosenModelChoiceField(label = "Kode Account",queryset=Tbl_Akun.objects.all(),required = False)
    debet = forms.FloatField(widget=forms.TextInput(attrs={'size': 9, 'class': 'rp_debet uang', 'value': '0', 'alt': 'integer'}),required = False)
    kredit = forms.FloatField(widget=forms.TextInput(attrs={'size': 9, 'class': 'rp_kredit uang', 'value': '0', 'alt': 'integer'}),required = False)
    gerai = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=GERAI_PILIH,required = False)
Tbl_TransaksiFormSet = formset_factory(Tbl_TransaksiForm)



class Tbl_AkunForm(forms.Form):
    id_coa = chosenforms.ChosenModelChoiceField(label = "Kode Account",queryset=Tbl_Akun.objects.all())
    id_cabang = chosenforms.ChosenChoiceField(widget=chosenforms.ChosenSelect({'class': 'id_cabang'})) 
    start_date = forms.DateTimeField(initial = datetime.date.today)

class Rugi_LabaForm(forms.Form):
    id_cabang = chosenforms.ChosenChoiceField(widget=chosenforms.ChosenSelect({'class': 'id_cabang'})) 
