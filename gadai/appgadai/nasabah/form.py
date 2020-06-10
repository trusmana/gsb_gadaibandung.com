from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from gadai.appgadai.models import Nasabah,KELAMIN,JENIS_PEKERJAAN,AKTIFASI_PARAMETER,STS_NSB

BUKA_OTO =(
    ('99','KUNCI'),('0','BUKA')
)
class BlacklistForm(forms.Form):
    status_nasabah = forms.ChoiceField(widget=forms.Select(), choices=STS_NSB)

class EditBarangGuForm(forms.Form):
    buka_akad_ulang = forms.ChoiceField(label="Buka Otorisasi GU ",widget=forms.Select(), choices=BUKA_OTO)

class EditParamForm(forms.Form):
    jml_akad = forms.IntegerField( widget=forms.TextInput( attrs={'size': 5}))
    tanggal = forms.DateField(widget=forms.widgets.DateInput(attrs={'size': 5,'placeholder':'Tanggal'}, format="%d-%m-%Y"))
    aktif = forms.ChoiceField(label="Aktifasi ",widget=forms.Select(), choices=AKTIFASI_PARAMETER)

class NasabahForm(forms.Form):
    nama = forms.CharField(max_length=35)
    tgl_lahir = forms.DateField(widget=forms.TextInput(attrs={'size': 10}))
    tempat = forms.CharField(label="Tempat lahir",max_length=15)
    no_ktp = forms.CharField( widget=forms.TextInput( attrs={'size': 20}))
    alamat_ktp = forms.CharField(widget=forms.TextInput(attrs={'size': 30}))
    rt_ktp = forms.CharField( widget=forms.TextInput( attrs={'size': 4}))
    rw_ktp = forms.CharField( widget=forms.TextInput( attrs={'size': 4}))
    telepon_ktp = forms.CharField( widget=forms.TextInput(attrs={'size':30}))
    hp_ktp = forms.CharField( widget=forms.TextInput(attrs={'size':30}))
    kelurahan_ktp = forms.CharField(widget=forms.TextInput(attrs={'size': 15}))
    kecamatan_ktp = forms.CharField(widget=forms.TextInput(attrs={'size': 15}))

    jenis_pekerjaan = forms.ChoiceField(widget=forms.Select(),choices=JENIS_PEKERJAAN)
 
    alamat_kantor =forms.CharField(widget=forms.TextInput(attrs={'size': 30}))
    kode_pos = forms.CharField( widget=forms.TextInput( attrs={'size': 10}))
    telepon_kantor =forms.CharField(widget=forms.TextInput(attrs={'size':30}))
    email = forms.CharField(widget=forms.TextInput(attrs={'size': 30}))
    jenis_kelamin = forms.ChoiceField(widget=forms.Select(), choices=KELAMIN)

class EditNasabahForm(forms.ModelForm):
    class Meta:
        model = Nasabah
        widgets = {
        #'nama' : forms.HiddenInput(),
        }

class EditNasabahGeraiForm(forms.ModelForm):
    tgl_lahir = forms.DateField(widget=forms.widgets.DateInput(attrs={'readonly':'true'}, format="%d-%m-%Y"))
    jekel_pasangan=forms.ChoiceField(widget=forms.Select(attrs={'readonly':'True'}),choices=KELAMIN) 
    class Meta:
        model = Nasabah
        widgets = {
        'nama' : forms.HiddenInput(),
        'no_ktp' : forms.HiddenInput(),
        'no_sim' : forms.HiddenInput(),
        'cu' : forms.HiddenInput(),
        'mu' : forms.HiddenInput(),
        'cdate' : forms.HiddenInput(),
        'mdate' : forms.HiddenInput(),
        'jenis_keanggotaan' : forms.HiddenInput(),
        'status_nasabah' : forms.HiddenInput(),
	#'tgl_lahir' : forms.HiddenInput(),
	'tempat' : forms.HiddenInput(),
	'no_ktp' : forms.HiddenInput(),
	'alamat_ktp' : forms.HiddenInput(),
	'no_rumah_ktp' : forms.HiddenInput(),
	'rt_ktp' : forms.HiddenInput(),
        'rw_ktp' : forms.HiddenInput(),
	#'telepon_ktp' : forms.HiddenInput(),
	#'hp_domisili' : forms.HiddenInput(),
	'kelurahan_ktp' : forms.HiddenInput(),
	'kecamatan_ktp' : forms.HiddenInput(),
	'kotamadya_ktp' : forms.HiddenInput(),
	'kabupaten_ktp' : forms.HiddenInput(),
	'no_sim' : forms.HiddenInput(),
	'alamat_sim' : forms.HiddenInput(),
	'rt_sim' : forms.HiddenInput(),
	'rw_sim' : forms.HiddenInput(),
	'kelurahan_sim' : forms.HiddenInput(),
	'kecamatan_sim' : forms.HiddenInput(),
	'jenis_pekerjaan' : forms.HiddenInput(),
	'alamat_kantor' : forms.HiddenInput(),
	'kode_pos' : forms.HiddenInput(),
	'telepon_kantor' : forms.HiddenInput(),
	'email' : forms.HiddenInput(),

	'jenis_kelamin' : forms.HiddenInput(),
	'jenis_keanggotaan' : forms.HiddenInput(),
	# Data Pasangan
	'nama_pasangan' : forms.HiddenInput(),
	'alamat_pasangan' : forms.HiddenInput(),
	#'jekel_pasangan' : forms.HiddenInput(),
	'tlp_pasangan' : forms.HiddenInput(),
	'no_rumah_pas' : forms.HiddenInput(),
	'no_rt_pas' : forms.HiddenInput(),
	'no_rw_pas' : forms.HiddenInput(),
        }
