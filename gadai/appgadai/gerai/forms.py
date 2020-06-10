from django import forms
from django.forms import ModelForm
from gadai.appgadai.models import *
from django.core.exceptions import ValidationError
from chosen import forms as chosenforms
from django.utils.safestring import mark_safe
from django.forms import ModelForm,Select

class HorizRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

JENIS_REPORT =(
    ('1','PDF'),
)

class aktifasi_userForm(forms.Form):
    id_cabang = chosenforms.ChosenModelChoiceField(label = "Gerai",queryset=Tbl_Cabang.objects.all(),widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}))


class Filter_NeracaForm(forms.Form):
    report = forms.ChoiceField(widget = forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'id_report'}), choices = JENIS_REPORT)
    id_cabang = chosenforms.ChosenModelChoiceField(label = "Gerai",queryset=Tbl_Cabang.objects.all(),widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}))
    start_date = forms.DateField(initial= datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,'readonly':'false'}, format="%Y-%m-01"))


class ManopForm(forms.Form):
    tanggal_manop = forms.DateField(initial=datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'true'}, format="%d-%m-%Y"))
    comment = forms.CharField(widget=forms.TextInput( attrs={'size': 15,'placeholder':'Isi Data Diskon'}))

class PelunasanForm(ModelForm):
    pelunasan = forms.ModelChoiceField(queryset=AkadGadai.objects.filter(lunas__isnull=True),widget=forms.HiddenInput())
    status_pelunasan = forms.ChoiceField(choices=STATUS_LUNAS,widget=forms.RadioSelect(attrs={'class':'rad'}),initial=1,)
    tanggal = forms.DateField(widget=forms.TextInput(attrs={'size': 8}))
    nilai = forms.DecimalField(widget=forms.TextInput(attrs={'readonly':'True','size': 8}))
    denda = forms.DecimalField(widget=forms.TextInput(attrs={'size': 8,'value':0}))
    terlambat = forms.IntegerField(widget=forms.TextInput(attrs={'size': 2,'value': '0'}))
    bea_jasa = forms.DecimalField(widget=forms.TextInput(attrs={'size': 8,'value':0}))
    jenis_barang = forms.ChoiceField(choices=CHOICES_JENIS_TRANSAKSI,widget=forms.RadioSelect(attrs={'class':'rad'}))
    denda_kendaraan = forms.DecimalField(widget=forms.TextInput(attrs={'size': 8,'value': '0'}))
    terlambat_kendaraan = forms.IntegerField(widget=forms.TextInput(attrs={'size': 2}))
    bea_jasa_kendaraan = forms.DecimalField(widget=forms.TextInput(attrs={'size': 8,'value':0}))
    gerai = forms.ModelChoiceField(queryset=Tbl_Cabang.objects.all(),widget=forms.HiddenInput())

    
    class Meta:
        model = Pelunasan 

class HorizRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class BarangBedaOtoForm(forms.Form):
    #pilih_jasa = forms.ChoiceField(widget=forms.Select(attrs={'readonly':'True'}),choices=JASABARU)
    pilih_jasa = forms.ChoiceField(widget = forms.HiddenInput(),choices=JASABARU,initial='1')
    agnasabah = forms.ModelChoiceField(label = "NAMA NASABAH",queryset=Nasabah.objects.filter(id__isnull=False))
    tanggal = forms.DateField(initial=datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'false'}, format="%d-%m-%Y"))
    gerai = forms.ModelChoiceField(queryset=Tbl_Cabang.objects.all())
    
    nilai = forms.IntegerField(label="Nilai",widget=forms.TextInput(attrs={'id':'nilai','alt': 'integer', 'class': 'rp_plafon uang','onkeyup':'hitungJasa(),akumulasi()'}))
    kewajiban_pelunasan = forms.IntegerField(label="Nilai",widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    taksir = chosenforms.ChosenModelChoiceField(label = "Data Taksir",queryset=Taksir.objects.filter(status =2),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}))
    barang = forms.ModelChoiceField(label="Nama Barang",queryset=Barang.objects.all(),widget=forms.Select(attrs={'readonly':'readonly'}))
    bea_materai = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':'0',\
        'id':'materai','onkeyup':'akumulasi()'}))
    jenis_transaksi=forms.ChoiceField(choices=CHOICES_JENIS_TRANSAKSI,widget=forms.RadioSelect(attrs={'class':'rad','id':'jenis_transaksi'}))    
    jangka_waktu = forms.ChoiceField( widget = forms.Select(attrs={'id':'jangka_waktu','onchange':'hitungJasa(),akumulasi()'}),\
        choices = JANGKA_WAKTU)
    ###KENDARAAN
    jangka_waktu_kendaraan = forms.ChoiceField( widget = forms.Select(attrs={'id':'jangka_waktu_kendaraan','onchange':'hitungJasa(),akumulasi()'}),\
        choices = JANGKA_WAKTU_KENDARAAN)
    jenis_kendaraan = forms.ChoiceField(widget=forms.Select(attrs={'id':'id_jenis_kendaraan','onchange':'hitungJasa(),akumulasi()'}), choices=JENIS_KENDARAAN)

    ### Barang ELEKTRONIK###
    jenis_barang = forms.ChoiceField(widget = forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'barang',}), choices = JENIS_BARANG,required=False)
    
    ###new input 1 april
    charger = forms.ChoiceField(widget =forms.Select(attrs={'class':'formhp formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_charger = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formhp formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')    
    batre = forms.ChoiceField(widget =forms.Select(attrs={'class':'formhp formbarang formkamera'}), choices=CHOICES_BARANG, initial='2')
    kondisi_batre = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formhp formbarang formkamera'}), choices=CHOICES_KONDISI_BARANG,initial='5')        
    keybord = forms.ChoiceField(widget =forms.Select(attrs={'class':'formhp formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_keybord = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formhp formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')        
    cassing = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_cassing = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')        
    layar = forms.ChoiceField(widget =forms.Select(attrs={'class':'formhp formbarang '}), choices=CHOICES_BARANG, initial='2')
    kondisi_layar = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formhp formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    password = forms.ChoiceField(widget =forms.Select(attrs={'class':'formhp formbarang '}), choices=CHOICES_BARANG, initial='2')
    password_barang = forms.CharField(label="PASSWORD ", widget=forms.TextInput( attrs={'size': 15,'class':'formhp formbarang ','placeholder':'Isi Sesuai Password','value': '0'}))
    
    lensa = forms.ChoiceField(widget =forms.Select(attrs={'class':'formkamera formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_lensa = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formkamera formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    batre_kamera = forms.ChoiceField(widget =forms.Select(attrs={'class':'formkamera formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_batre_kamera = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formkamera formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    cassing_kamera = forms.ChoiceField(widget =forms.Select(attrs={'class':'formkamera formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_cassing_kamera = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formkamera formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    
    optik_ps = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formps'}), choices=CHOICES_BARANG, initial='2')
    kondisi_optik_ps = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formps'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    harddisk  = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formps'}), choices=CHOICES_BARANG, initial='2')
    kondisi_harddisk = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formps'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    stick  = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formps'}), choices=CHOICES_BARANG, initial='2')
    kondisi_stick = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formps'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    hdmi  = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formps'}), choices=CHOICES_BARANG, initial='2')
    kondisi_hdmi = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formps'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    remote = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formtv'}), choices=CHOICES_BARANG, initial='2')
    kondisi_remote = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formbarang formtv'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    dus = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang'}), choices=CHOICES_BARANG, initial='2')
    tas = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang'}), choices=CHOICES_BARANG, initial='2')
    layar_tv = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formtv'}), choices=CHOICES_BARANG, initial='2')
    kondisi_layar_tv = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formbarang formtv'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    
    accesoris_barang1=forms.CharField(max_length=150,widget=forms.Textarea(attrs={'value': '0'}))
    
    bpkb = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    stnk = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    faktur = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    gesek_nomesin = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    gesek_norangka = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    denda_gu = forms.IntegerField(label="Nilai",widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    nilai_gu = forms.IntegerField(label="Nilai",widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    jasa_gu = forms.IntegerField(label="Nilai",widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))

    pokok = forms.IntegerField(label="Nilai",widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','id':'pokok'}))
    denda = forms.IntegerField(label="Nilai",widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','id':'denda'}))
    denda_keterlambatan = forms.IntegerField(label="Nilai",widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','id':'denda_keterlambatan'}))

    jasa_baru = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'jasa_baru'}))    
    beasimpan_baru = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'beasimpan_baru'}))    
    adm_baru = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'adm_baru'}))
    kewajiban_total_baru = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'kewajiban_total_baru'}))
    total_all = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'total_all'}))
    status = forms.ChoiceField(widget=forms.Select(attrs={'readonly':'False'}),choices=STATUS_OTORISASI)
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Masukan Keterangan Nilai Yg ingin Ada Diskon'}),required=False)



class BarangBedaForm(forms.Form):
    #pilih_jasa = forms.ChoiceField(widget=forms.Select(attrs={'readonly':'False'}),choices=JASABARU)
    pilih_jasa = forms.ChoiceField(widget = forms.HiddenInput(),choices=JASABARU,initial='1')
    agnasabah = forms.ModelChoiceField(label = "NAMA NASABAH",queryset=Nasabah.objects.filter(id__isnull=False))
    tanggal = forms.DateField(initial=datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'false'}, format="%d-%m-%Y"))
    gerai = forms.ModelChoiceField(queryset=Tbl_Cabang.objects.all())
    
    nilai = forms.IntegerField(label="Nilai",widget=forms.TextInput(attrs={'id':'nilai','alt': 'integer', 'class': 'rp_plafon uang','onkeyup':'hitungJasa(),akumulasi()'}))
    kewajiban_pelunasan = forms.IntegerField(label="Nilai",widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    taksir = chosenforms.ChosenModelChoiceField(label = "Data Taksir",queryset=Taksir.objects.filter(status =2),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}))
    barang = forms.ModelChoiceField(label="Nama Barang",queryset=Barang.objects.all(),widget=forms.Select(attrs={'readonly':'readonly'}))
    bea_materai = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':'0',\
        'id':'materai','onkeyup':'akumulasi()'}))
    jenis_transaksi=forms.ChoiceField(choices=CHOICES_JENIS_TRANSAKSI,widget=forms.RadioSelect(attrs={'class':'rad','id':'jenis_transaksi'}))    
    jangka_waktu = forms.ChoiceField( widget = forms.Select(attrs={'id':'jangka_waktu','onchange':'hitungJasa(),akumulasi()'}),\
        choices = JANGKA_WAKTU)
    ###KENDARAAN
    jangka_waktu_kendaraan = forms.ChoiceField( widget = forms.Select(attrs={'id':'jangka_waktu_kendaraan','onchange':'hitungJasa(),akumulasi()'}),\
        choices = JANGKA_WAKTU_KENDARAAN)
    jenis_kendaraan = forms.ChoiceField(widget=forms.Select(attrs={'id':'id_jenis_kendaraan','onchange':'hitungJasa(),akumulasi()'}),\
        choices=JENIS_KENDARAAN)

    ### Barang ELEKTRONIK###
    jenis_barang = forms.ChoiceField(widget = forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'barang',}), choices = JENIS_BARANG,required=False)
    
    ###new input 1 april
    charger = forms.ChoiceField(widget =forms.Select(attrs={'class':'formhp formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_charger = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formhp formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')    
    batre = forms.ChoiceField(widget =forms.Select(attrs={'class':'formhp formbarang formkamera'}), choices=CHOICES_BARANG, initial='2')
    kondisi_batre = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formhp formbarang formkamera'}), choices=CHOICES_KONDISI_BARANG,initial='5')        
    keybord = forms.ChoiceField(widget =forms.Select(attrs={'class':'formhp formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_keybord = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formhp formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')        
    cassing = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_cassing = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')        
    layar = forms.ChoiceField(widget =forms.Select(attrs={'class':'formhp formbarang '}), choices=CHOICES_BARANG, initial='2')
    kondisi_layar = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formhp formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    password = forms.ChoiceField(widget =forms.Select(attrs={'class':'formhp formbarang '}), choices=CHOICES_BARANG, initial='2')
    password_barang = forms.CharField(label="PASSWORD ", widget=forms.TextInput( attrs={'size': 15,'class':'formhp formbarang ','placeholder':'Isi Sesuai Password','value': '0'}))
    
    lensa = forms.ChoiceField(widget =forms.Select(attrs={'class':'formkamera formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_lensa = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formkamera formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    batre_kamera = forms.ChoiceField(widget =forms.Select(attrs={'class':'formkamera formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_batre_kamera = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formkamera formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    cassing_kamera = forms.ChoiceField(widget =forms.Select(attrs={'class':'formkamera formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_cassing_kamera = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formkamera formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    
    optik_ps = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formps'}), choices=CHOICES_BARANG, initial='2')
    kondisi_optik_ps = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formps'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    harddisk  = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formps'}), choices=CHOICES_BARANG, initial='2')
    kondisi_harddisk = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formps'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    stick  = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formps'}), choices=CHOICES_BARANG, initial='2')
    kondisi_stick = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formps'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    hdmi  = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formps'}), choices=CHOICES_BARANG, initial='2')
    kondisi_hdmi = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formps'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    remote = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formtv'}), choices=CHOICES_BARANG, initial='2')
    kondisi_remote = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formbarang formtv'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    dus = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang'}), choices=CHOICES_BARANG, initial='2')
    tas = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang'}), choices=CHOICES_BARANG, initial='2')
    layar_tv = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formtv'}), choices=CHOICES_BARANG, initial='2')
    kondisi_layar_tv = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formbarang formtv'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    
    accesoris_barang1=forms.CharField(max_length=150,widget=forms.Textarea(attrs={'value': '0'}))
    
    bpkb = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    stnk = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    faktur = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    gesek_nomesin = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    gesek_norangka = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    denda_gu = forms.IntegerField(label="Nilai",widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    nilai_gu = forms.IntegerField(label="Nilai",widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    jasa_gu = forms.IntegerField(label="Nilai",widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))

    pokok = forms.IntegerField(label="Nilai",widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','id':'pokok'}))
    denda = forms.IntegerField(label="Nilai",widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','id':'denda'}))
    denda_keterlambatan = forms.IntegerField(label="Nilai",widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','id':'denda_keterlambatan'}))

    jasa_baru = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'jasa_baru'}))    
    beasimpan_baru = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'beasimpan_baru'}))    
    adm_baru = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'adm_baru'}))
    kewajiban_total_baru = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'kewajiban_total_baru'}))
    total_all = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'total_all'}))
    
    
class AKADBARANGForm(forms.Form):
    agnasabah = forms.ModelChoiceField(label = "NAMA NASABAH",queryset=Nasabah.objects.filter(id__isnull=False))
    #tanggal = forms.DateField(label = "Tanggal Akad",widget=forms.TextInput(attrs={'size': 10,'readonly':'True'}))
    tanggal = forms.DateField(widget=forms.widgets.DateInput(attrs={'size': 12,'readonly':'False'}, format="%d-%m-%Y"))
    gerai = forms.ModelChoiceField(queryset=Tbl_Cabang.objects.all(),empty_label="--- PILIH ---")   
    nilai = forms.IntegerField(label="Nilai Pinjaman",widget=forms.TextInput(attrs={'id':'nilai','alt': 'integer',\
        'class': 'rp_plafon uang','onkeyup':'hitungJasa(),akumulasi()'})) 
    taksir = chosenforms.ChosenModelChoiceField(label = "Data Taksir",queryset=Taksir.objects.filter(status =2),widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}))    
    #bea_materai = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':'6000'}))
    bea_materai =forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':'0',\
        'id':'materai','onkeyup':'akumulasi()'}))
    jenis_transaksi =forms.ChoiceField(choices=CHOICES_JENIS_TRANSAKSI,widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'rad',\
        'id':'jenis_transaksi'}), initial='')
    jangka_waktu = forms.ChoiceField( widget = forms.Select(attrs={'id':'jangka_waktu','onchange':'hitungJasa(),akumulasi()'}),\
        choices = JANGKA_WAKTU)
    ###KENDARAAN
    jangka_waktu_kendaraan = forms.ChoiceField( widget = forms.Select(attrs={'id':'jangka_waktu_kendaraan','onchange':'hitungJasa(),akumulasi()'}),\
        choices = JANGKA_WAKTU_KENDARAAN)
    jenis_kendaraan = forms.ChoiceField(widget=forms.Select(), choices=JENIS_KENDARAAN)
    ### Barang ELEKTRONIK###
    
    
    ###new input 1 april
    charger = forms.ChoiceField(widget =forms.Select(attrs={'class':'formhp formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_charger = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formhp formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')    
    batre = forms.ChoiceField(widget =forms.Select(attrs={'class':'formhp formbarang formkamera'}), choices=CHOICES_BARANG, initial='2')
    kondisi_batre = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formhp formbarang formkamera'}), choices=CHOICES_KONDISI_BARANG,initial='5')        
    keybord = forms.ChoiceField(widget =forms.Select(attrs={'class':'formhp formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_keybord = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formhp formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')        
    cassing = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_cassing = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')        
    layar = forms.ChoiceField(widget =forms.Select(attrs={'class':'formhp formbarang '}), choices=CHOICES_BARANG, initial='2')
    kondisi_layar = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formhp formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    password = forms.ChoiceField(widget =forms.Select(attrs={'class':'formhp formbarang '}), choices=CHOICES_BARANG, initial='2')
    password_barang = forms.CharField(label="PASSWORD ", widget=forms.TextInput( attrs={'size': 15,'class':'formhp formbarang ','placeholder':'Isi Sesuai Password','value': '0'}))
    
    lensa = forms.ChoiceField(widget =forms.Select(attrs={'class':'formkamera formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_lensa = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formkamera formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    batre_kamera = forms.ChoiceField(widget =forms.Select(attrs={'class':'formkamera formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_batre_kamera = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formkamera formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    cassing_kamera = forms.ChoiceField(widget =forms.Select(attrs={'class':'formkamera formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_cassing_kamera = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formkamera formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    
    optik_ps = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formps'}), choices=CHOICES_BARANG, initial='2')
    kondisi_optik_ps = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formps'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    harddisk  = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formps'}), choices=CHOICES_BARANG, initial='2')
    kondisi_harddisk = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formps'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    stick  = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formps'}), choices=CHOICES_BARANG, initial='2')
    kondisi_stick = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formps'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    hdmi  = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formps'}), choices=CHOICES_BARANG, initial='2')
    kondisi_hdmi = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formps'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    remote = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formtv'}), choices=CHOICES_BARANG, initial='2')
    kondisi_remote = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formbarang formtv'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    dus = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang'}), choices=CHOICES_BARANG, initial='2')
    tas = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang'}), choices=CHOICES_BARANG, initial='2')
    layar_tv = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formtv'}), choices=CHOICES_BARANG, initial='2')
    kondisi_layar_tv = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formbarang formtv'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    
    accesoris_barang1=forms.CharField(max_length=150,widget=forms.Textarea(attrs={'value': '0','placeholder':'Wajib Diisi'}))
    
    bpkb = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    stnk = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    faktur = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    gesek_nomesin = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    gesek_norangka = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    
    ### Barang ELEKTRONIK###
    jenis_barang = forms.ChoiceField(widget = forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'barang'}), choices = JENIS_BARANG,initial ='0',required=False)
    #pilih_jasa = forms.ChoiceField(widget=forms.Select(attrs={'readonly':'False'}),choices=JASABARU) 
    pilih_jasa = forms.ChoiceField(widget = forms.HiddenInput(),choices=JASABARU,initial='1')

    sn = forms.CharField(label="S/N - Imei  ", widget=forms.TextInput( attrs={'size': 30,'value': '0'}))
    warna = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'value': '0'}))
    tahun_pembuatan=forms.CharField(max_length=10,widget=forms.TextInput(attrs={'value': '0'}))
    bulan_produksi =forms.CharField(max_length=10,widget=forms.TextInput(attrs={'value': '0'}))
    lampiran_dokumen = forms.ChoiceField(widget =forms.Select(), choices=JENIS_DOKUMEN)    
    
    
    ### KENDARAAN ####
    merk_kendaraan = forms.ChoiceField(widget=forms.Select(), choices=MERK_KENDARAAN_CHOICES)
    type_kendaraan =forms.CharField(max_length=200,widget=forms.TextInput(attrs={'value': '0'}))
    tahun_pembuatan_kendaraan =forms.ChoiceField(widget=forms.Select(), choices=TAHUN_KENDARAAN_CHOICES)
    no_polisi = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'value': '0'}))
    no_rangka = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'value': '0'}))
    no_mesin  = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'value': '0'}))
    warna_kendaraan = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'value': '0'}))
    no_bpkb = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'value': '0'}))
    stnk_atas_nama = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'value': '0'}))
    no_faktur = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'value': '0'}))
    jasa_baru = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'jasa_baru'}))    
    beasimpan_baru = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'beasimpan_baru'}))    
    adm_baru = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'adm_baru'}))
    total_all = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'total_all'}))     

    tanda_tangan = forms.FileField()
    foto_nasabah = forms.FileField()
    berkas_barang = forms.FileField()

