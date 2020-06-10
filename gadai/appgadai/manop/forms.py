from django import forms
from django.forms import ModelForm
from gadai.appgadai.models import *
from gadai.appkeuangan.models import *
from chosen import forms as chosenforms
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import UserCreationForm
from gadai.appkeuangan.models import DATACABANG

OTORITAS_STATUS =(
    ('1','KUNCI'),('0','BUKA')
)
OTORITAS_STATUS_TDR =(
    ('1','KUNCI'),('None','BUKA')
)
class BukaStatusForm(forms.Form):
    buka_status_kw = chosenforms.ChosenChoiceField(widget=chosenforms.ChosenSelect({'class': 'id_cabang'}),choices = OTORITAS_STATUS) 
    buka_status_label = chosenforms.ChosenChoiceField(widget=chosenforms.ChosenSelect({'class': 'id_cabang'}),choices = OTORITAS_STATUS) 
    buka_kondisi_barang = chosenforms.ChosenChoiceField(widget=chosenforms.ChosenSelect({'class': 'id_cabang'}),choices = OTORITAS_STATUS) 
    buka_sts_tdr = chosenforms.ChosenChoiceField(widget=chosenforms.ChosenSelect({'class': 'id_cabang'}),choices = OTORITAS_STATUS_TDR) 

class SearchForm(forms.Form):
    start_date = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,}, format="%Y-%m-%d"))
    end_date = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,}, format="%Y-%m-%d"))
    id_cabang = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=DATACABANG,initial='0',required=False)

class ReportForm(forms.Form):
    id_cabang =  forms.ChoiceField(widget=forms.Select(), choices=DATACABANG_GLPUSAT,required = False)
    start_date = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,}, format="%Y-%m-%d"))
    end_date = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,}, format="%Y-%m-%d"))


class FilterForm(forms.Form):
    #report = forms.ChoiceField(widget = forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'id_report'}), choices = JENIS_REPORT)
    id_cabang = chosenforms.ChosenChoiceField(widget=chosenforms.ChosenSelect({'class': 'id_cabang'}),choices = GERAI_PILIH)
    start_date = forms.DateField(initial= datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,'readonly':'false'}, format="%Y-%m-01"))
    end_date = forms.DateField(initial= datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,'readonly':'false'}, format="%Y-%m-%d"))

class HorizRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class Verifikasi_Pelunasan_ManOpForm(ModelForm):
    class Meta:
        model = ManopGadai

class UserForm(UserCreationForm):
    class Meta:
        model = User
        exclude = ('password','date_joined','last_login','user_permissions')
        widgets = {
            'groups': forms.CheckboxSelectMultiple(),
        }        

class UserProfileForm(ModelForm):
    user =chosenforms.ChosenModelChoiceField(label = "User",queryset=User.objects.all().order_by('id'),required = True)
    gerai =chosenforms.ChosenModelChoiceField(label = "Gerai",queryset=Tbl_Cabang.objects.all().order_by('id'),required = True)        
    class Meta:
        model = UserProfile
        exclude = ('rekening')

class GeraiForm(ModelForm):
    parent =chosenforms.ChosenModelChoiceField(label = "Parent",queryset=Tbl_Cabang.objects.all().order_by('id'),required = False)    
    class Meta:
        model = Tbl_Cabang

class Verifikasi_Pelunasan_ManOpForm(ModelForm):
    class Meta:
        model = ManopGadai


GERAI_PILIH =(
    ('500','( GABUNGAN )'),('2','JAKARTA'),('3','SUCI'),('4','DIPATIUKUR'),('5','BALUBUR'),
    ('7','GERLONG HILIR'),('8','KOPO'),('9','CIBIRU'),('10','CIPACING'),('11','JATINANGOR'),
    ('12','CIMAHI'),('13','BUAH BATU'),('14','KORDON'),('15','CIHANJUANG'),('16','MARANATA'),('17','KIARACONDONG'),
    ('18','CIREBON'),('10','CIUMBULEUIT'),('21','UJUNGBERUNG'),
)

JENIS_REPORT =(
    ('1','EXCEL'),('2','PDF'),('3','VIEW'),
)

JENIS_LAPORAN =(
    ('1','RINCIAN PIUTANG'),('2','REKAP PIUTANG')
)
class HorizRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class Filter_PencairanForm(forms.Form):
    report = forms.ChoiceField(widget = forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'id_report'}), choices = JENIS_REPORT)
    id_cabang = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=DATACABANG,initial='0',required=False)
    start_date = forms.DateField(initial= datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,'readonly':'false'}, format="%Y-%m-01"))
    end_date = forms.DateField(initial= datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,'readonly':'false'}, format="%Y-%m-%d"))
    jenis_laporan = chosenforms.ChosenChoiceField(widget=chosenforms.ChosenSelect({'class':'id_jenis_laporan'}),choices = JENIS_LAPORAN)

class BarangLelangForm(forms.ModelForm):
    aglelang =forms.ModelChoiceField(queryset=AkadGadai.objects.all())
    tgl_lelang = forms.DateTimeField(label = "Tanggal Pelelangan", widget=forms.DateInput(attrs={'size': 10,'readonly':'True'},format="%d-%m-%Y"))
    harga_jual = forms.IntegerField(label="Nilai Penjualan",widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    nama_pembeli =forms.CharField(widget=forms.TextInput(attrs={'size': 20}))
    no_identitas =forms.CharField(widget=forms.TextInput(attrs={'size': 16}))
    alamat_pembeli =forms.CharField(widget=forms.TextInput(attrs={'size': 20}))
    no_telp =forms.CharField(widget=forms.TextInput(attrs={'size': 20}))
    jenis =forms.ChoiceField( widget = forms.Select(), choices = JENIS_PNC)
    class Meta:
        model = BarangLelang

        
class PelunasanManopForm(ModelForm):
    pelunasan = forms.ModelChoiceField(queryset=AkadGadai.objects.filter(lunas__isnull=True),widget=forms.HiddenInput())
    tanggal = forms.DateField(widget=forms.TextInput(attrs={'size': 8}))
    nilai = forms.DecimalField(widget=forms.TextInput(attrs={'readonly':'True','size': 8}))
    denda = forms.DecimalField(widget=forms.TextInput(attrs={'size': 8,'value':0}))
    terlambat = forms.IntegerField(widget=forms.TextInput(attrs={'size': 2,'value': '0'}))
    bea_jasa = forms.DecimalField(widget=forms.TextInput(attrs={'size': 8,'value':0}))
    jenis_barang =forms.ChoiceField(choices=CHOICES_JENIS_TRANSAKSI,widget=forms.RadioSelect(attrs={'class':'rad'}))
    denda_kendaraan = forms.DecimalField(widget=forms.TextInput(attrs={'size': 8,'value': '0'}))
    terlambat_kendaraan = forms.IntegerField(widget=forms.TextInput(attrs={'size': 2}))
    bea_jasa_kendaraan = forms.DecimalField(widget=forms.TextInput(attrs={'size': 8,'value':0}))
    gerai = forms.ModelChoiceField(queryset=Tbl_Cabang.objects.all(),widget=forms.HiddenInput())
    #status_transaksi =forms.ChoiceField(widget=forms.Select(),choices=CHOICES_TRANSAKSI) 
    #lunas = forms.BooleanField(required=False)
    
    class Meta:
        model = Pelunasan    

class MyForm(forms.ModelForm):
    tanggal = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'true'}, format="%d-%m-%Y"))
    nilai = forms.IntegerField(widget=forms.TextInput(attrs={'size': 9, 'alt': 'integer', 'class': 'rp_nilai uang'}))
    denda = forms.IntegerField(widget=forms.TextInput(attrs={'size': 9, 'alt': 'integer', 'class': 'rp_nilai uang'}))
    bea_jasa = forms.IntegerField(widget=forms.TextInput(attrs={'size': 9, 'alt': 'integer', 'class': 'rp_nilai uang'}))
    terlambat = forms.IntegerField(widget=forms.TextInput(attrs={'size': 9,'readonly':'true'}))
    status =forms.ChoiceField(choices=STATUS_OTORISASI,initial = '1')
    #jenis_barang =forms.ChoiceField(choices=CHOICES_JENIS_TRANSAKSI,widget=forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'rad'}))
    class Meta:
        model = ManopPelunasan
        fields =('tanggal','nilai','terlambat','denda','bea_jasa','status','note')
        widgets = {
            'pelunasan' : forms.HiddenInput(),'status' : forms.HiddenInput(),
        }

class MyGuForm(forms.ModelForm):
    tanggal = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'true'}, format="%d-%m-%Y"))
    nilai = forms.IntegerField(widget=forms.TextInput(attrs={'size': 9, 'alt': 'integer', 'class': 'rp_nilai uang'}))
    denda = forms.IntegerField(widget=forms.TextInput(attrs={'size': 9, 'alt': 'integer', 'class': 'rp_nilai uang'}))
    bea_jasa = forms.IntegerField(widget=forms.TextInput(attrs={'size': 9, 'alt': 'integer', 'class': 'rp_nilai uang'}))
    status =forms.ChoiceField(choices=STATUS_OTORISASI,initial = '1')    
    class Meta:
        model = ManopPelunasanGu
        fields =('tanggal','nilai','denda','bea_jasa','status','note')
        widgets = {
            'gu' : forms.HiddenInput(),'status' : forms.HiddenInput(),
        }
