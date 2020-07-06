from django import forms
from django.forms import ModelForm
from gadai.appgadai.models import *
from django.core.exceptions import ValidationError
from chosen import forms as chosenforms
from django.utils.safestring import mark_safe
from django.forms import ModelForm,Select
from gadai.appkeuangan.models import *
from gadai.appkeuangan.models import DATACABANG

JENIS_REPORT =(
    ('1','EXCEL'),('2','PDF'),('3','VIEW'),
)

JENIS_DATA =(
    ('1','NONPOSTING'),('2','POSTING'),('3','CETAK POSTING'),('4','EXCEL')
)
JENIS_LAPORAN =(
    ('1','VIEW'),
)

STATUS_BARANG = (
    ('1','AYDA'),('2','TERJUAL'),('3','Pinjam'),
    )

class HorizRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self ]))

class FilterNewForm(forms.Form):
    report = chosenforms.ChosenChoiceField(widget=chosenforms.ChosenSelect({'class':'id_report'}), choices = JENIS_REPORT)
    barang = chosenforms.ChosenChoiceField(widget=chosenforms.ChosenSelect({'class':'id_barang'}),choices = JENIS_BARANG)
    kendaraan = chosenforms.ChosenChoiceField(widget=chosenforms.ChosenSelect({'class':'id_kendaraan'}),choices =JENIS_KENDARAAN)
    id_cabang = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=DATACABANG,initial='0',required=False) 
    start_date = forms.DateField(initial= datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12}, format="%Y-%m-01"))
    end_date = forms.DateField(initial= datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12}, format="%Y-%m-%d"))
    jenis_laporan = chosenforms.ChosenChoiceField(widget=chosenforms.ChosenSelect({'class':'id_jenis_laporan'}),choices = JENIS_LAPORAN)
    status_barang = chosenforms.ChosenChoiceField(widget=chosenforms.ChosenSelect({'class':'id_status_barang'}),choices =
            STATUS_BARANG)


class Format_laporanForm(forms.Form):
    id_cabang = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=DATACABANG,initial='0',required=False)
    start_date = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,}, format="%Y-%m-%d"))
    end_date = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,}, format="%Y-%m-%d"))
    jenis = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'id_pilih'}),choices = JENIS_LAPORAN)

class KeuanganPusatForm(forms.ModelForm):
    tanggal = forms.DateField(label ='Tanggal Perubahan Saldo',initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12}, format="%d-%m-%Y"))
    saldo = forms.FloatField(widget=forms.TextInput(attrs={'size': 9, 'class': 'rp_debet uang', 'alt': 'integer'}),required = False)
    tanggal_sbl = forms.DateField(label ='Tanggal Transaksi',widget=forms.widgets.DateInput(attrs={'size': 12}), required = False)
    class Meta:
        model = KeuanganPusat
        widgets = {'keuangan_pusat'  : forms.HiddenInput(),}

class SearchForm(forms.Form):
    start_date = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,}, format="%Y-%m-%d"))
    end_date = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,}, format="%Y-%m-%d"))
    id_cabang = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=DATACABANG,initial='0',required=False)
    id_coa = chosenforms.ChosenModelChoiceField(label = "Kode Account",queryset=Tbl_Akun.objects.all())
    jenis = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'id_pilih'}),choices = JENIS_DATA)

class RefisiJurnalForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'size': 12,'readonly':'True'}, format="%d-%m-%Y"))
    id_cabang = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=DATACABANG,initial='0',required=False)

class Tbl_TransaksiRefForm(ModelForm):
    debet = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    kredit = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    tgl_trans = forms.DateField(widget=forms.widgets.DateInput(attrs={'size': 12,'readonly':'True'}, format="%d-%m-%Y"))
    class Meta:
        model = Tbl_Transaksi
        widgets = {
            'no_trans' : forms.HiddenInput(),'id_cabang_tuju' : forms.HiddenInput(),'status_posting' : forms.HiddenInput(),
            'nocoa_titipan': forms.HiddenInput(),'deskripsi': forms.HiddenInput(),'saldo': forms.HiddenInput(),
            'posting': forms.HiddenInput(),'id_product': forms.HiddenInput(),'status_jurnal': forms.HiddenInput(),
            'id_unit': forms.HiddenInput(),
        }
