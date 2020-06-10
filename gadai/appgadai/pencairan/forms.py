from django import forms
from django.forms import ModelForm
from gadai.appgadai.models import *
from django.core.exceptions import ValidationError
from chosen import forms as chosenforms
from django.utils.safestring import mark_safe

STATUS_OTORISASI_MANOP=(
    ('1','STATUS'),
    ('2','OTORISASI'),
)


CHOICES_AGUNAN=(
    ('1','ELEKTRONIK'),
    ('2','KENDARAAN'),
)


class ParameterForm(forms.Form):
    jenis = forms.ChoiceField( label = "JANGKA WAKTU",widget = forms.Select(), choices = CHOICES_PRODUK_PARAM)
    jenis_barang = forms.ChoiceField(label = "AGUNAN", widget = forms.Select(), choices = JENIS_AGUNAN)
    
    

class HorizRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class Verifikasi_ManOpForm(ModelForm):
    tanggal = forms.DateField(widget=forms.widgets.DateInput(attrs={'size': 12,'readonly':'True'}, format="%d-%m-%Y"))
    class Meta:
        model = ManopGadai

class Edit_AkadForm(ModelForm):
    class Meta:
        model = AkadGadai
        #fields = ('agnasabah','gerai','tanggal','nilai','taksir','barang','bea_materai','jenis_transaksi','jangka_waktu_kendaraan','jatuhtempo')
        widgets = {
            'agnasabah' : forms.HiddenInput(),
            'status_transaksi' : forms.HiddenInput(),
            #'tanggal':forms.HiddenInput(),
            'status_taksir' : forms.HiddenInput(),
            #'jatuhtempo': forms.HiddenInput(),
            'nocoa_titipan': forms.HiddenInput(),
            'nocoa_kas': forms.HiddenInput(),
            'os_pokok': forms.HiddenInput(),
            'status_kw': forms.HiddenInput(),
            'status_kwlunas': forms.HiddenInput(),
            'status_mcc': forms.HiddenInput(),
            'lunas': forms.HiddenInput(),
            'status_transaksi': forms.HiddenInput(),
            'selisih_pelunasan':forms.HiddenInput(),
        }

class AkadGadaiForm(ModelForm):
    agnasabah = forms.ModelChoiceField(label = "NAMA NASABAH",queryset=Nasabah.objects.all())
    tanggal = forms.DateField(label = "Tanggal Akad",widget=forms.TextInput(attrs={'size': 10}))
    gerai = forms.ModelChoiceField(queryset=Tbl_Cabang.objects.all(),empty_label="--- PILIH ---")
    jangka_waktu = forms.ChoiceField( widget = forms.Select(), choices = JANGKA_WAKTU)
    nilai = forms.IntegerField(label="Nilai Taksir",widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    taksir = forms.ModelChoiceField(queryset=Taksir.objects.all(),empty_label="--- PILIH ---")
    denda = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    terlambat = forms.IntegerField(widget=forms.TextInput())
    status_transaksi =forms.ChoiceField(widget=forms.Select(),choices=CHOICES_TRANSAKSI)

    class Meta:
        model = AkadGadai

class PelunasanForm(forms.Form):
    pelunasan = forms.ModelChoiceField(queryset=AkadGadai.objects.filter(lunas__isnull=True))
    tanggal = forms.DateField(initial=datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'true'}, format="%d-%m-%Y"))
    jatuhtempo = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'true'}, format="%d-%m-%Y"))
    tgl_akad = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'true'}, format="%d-%m-%Y"))
    
    nilai = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','size': 9, 'alt': 'integer', 'class': 'rp_nilai uang'}))
    denda = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','size': 9, 'value': '0','alt': 'integer',\
    'class': 'rp_nilai uang','onclick':'total_dibayar()'}))
    terlambat = forms.IntegerField(widget=forms.TextInput(attrs={'size': 2,'value':0}))
    bea_jasa = forms.IntegerField(widget=forms.TextInput(attrs={'size': 9, 'value': '0', 'alt': 'integer', 'class': 'rp_nilai uang','onclick':'total_dibayar()'}))
    jenis_barang =forms.ChoiceField(choices=CHOICES_JENIS_TRANSAKSI,widget=forms.RadioSelect(attrs={'class':'rad','onclick':'total_dibayar()'}))
    denda_kendaraan = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','size': 9, 'value': '0', 'alt': 'integer', 'class': 'rp_nilai uang','onclick':'total_dibayar()'}))
    terlambat_kendaraan = forms.IntegerField(widget=forms.TextInput(attrs={'size': 2,'value':0}))
    bea_jasa_kendaraan = forms.DecimalField(widget=forms.TextInput(attrs={'readonly':'True','size': 9,'class': 'rp_nilai uang','value':0}))
    gerai = forms.ModelChoiceField(queryset=Tbl_Cabang.objects.all())
    status_transaksi =forms.ChoiceField(widget=forms.Select(attrs={'readonly':'True'}),choices=CHOICES_TRANSAKSI) 
    lunas = forms.BooleanField(required=False)
    total = forms.IntegerField(widget=forms.TextInput(attrs={'size': 9, 'alt': 'integer', 'class': 'rp_nilai uang','readonly':True,'onclick':'total_dibayar()'}))
    total_kendaraan = forms.IntegerField(widget=forms.TextInput(attrs={'size': 9, 'alt': 'integer', 'class': 'rp_nilai uang','readonly':True,'onclick':'total_dibayar()','value':0}))
    norek = forms.CharField( widget=forms.TextInput(attrs={'size':20,'readonly':'true'}))
    status = forms.ChoiceField(widget=forms.Select(attrs={'readonly':'False'}),choices=STATUS_OTORISASI)
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Masukan Keterangan Nilai Yg ingin Ada Diskon'}),required=False)
    class Meta:
        model = Pelunasan    

class PelunasanDiskonForm(forms.Form):
    pelunasan = forms.ModelChoiceField(queryset=AkadGadai.objects.filter(lunas__isnull=True))
    tanggal = forms.DateField(initial=datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'false'}, format="%d-%m-%Y"))
    jatuhtempo = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'true'}, format="%d-%m-%Y"))
    tgl_akad = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'true'}, format="%d-%m-%Y"))
    nilai = forms.IntegerField(widget=forms.TextInput(attrs={'size': 9, 'alt': 'integer', 'class': 'rp_nilai uang'}))
    denda = forms.IntegerField(widget=forms.TextInput(attrs={'size': 9, 'value': '0','alt': 'integer', 'class': 'rp_nilai uang'}))
    terlambat = forms.IntegerField(widget=forms.TextInput(attrs={'size': 2,'value':0}))
    bea_jasa = forms.IntegerField(widget=forms.TextInput(attrs={'size': 9, 'value': '0', 'alt': 'integer', 'class': 'rp_nilai uang'}))
    jenis_barang =forms.ChoiceField(choices=CHOICES_JENIS_TRANSAKSI,widget=forms.RadioSelect(attrs={'class':'rad'}))
    denda_kendaraan = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','size': 9, 'value': '0', 'alt': 'integer', 'class': 'rp_nilai uang','onclick':'total_dibayar()'}))
    terlambat_kendaraan = forms.IntegerField(widget=forms.TextInput(attrs={'size': 2,'value':0}))
    bea_jasa_kendaraan = forms.DecimalField(widget=forms.TextInput(attrs={'readonly':'True','size': 9,'class': 'rp_nilai uang','alt': 'integer'}))
    gerai = forms.ModelChoiceField(queryset=Tbl_Cabang.objects.all())
    status_transaksi =forms.ChoiceField(widget=forms.Select(attrs={'readonly':'True'}),choices=CHOICES_TRANSAKSI) 
    lunas = forms.BooleanField(required=False)
    total = forms.IntegerField(widget=forms.TextInput(attrs={'size': 9, 'alt': 'integer', 'class': 'rp_nilai uang','readonly':True}))
    total_kendaraan = forms.IntegerField(widget=forms.TextInput(attrs={'size': 9, 'alt': 'integer', 'class': 'rp_nilai uang','readonly':True}))
    norek = forms.CharField( widget=forms.TextInput(attrs={'size':20,'readonly':'true'}))
    status = forms.ChoiceField(widget=forms.Select(attrs={'readonly':'False'}),choices=STATUS_OTORISASI_MANOP, initial='2',required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 10, 'rows': 20}),required=False)

    class Meta:
        model = Pelunasan


class AkadForm(forms.Form):
    
    agnasabah = forms.ModelChoiceField(label = "NAMA NASABAH",queryset=Nasabah.objects.filter(id__isnull=False))
    tanggal = forms.DateTimeField(initial = datetime.date.today,widget=forms.DateTimeInput(attrs={'readonly':'true'}))
    gerai = forms.ModelChoiceField(queryset=Tbl_Cabang.objects.all(),empty_label="--- PILIH ---")
    jangka_waktu = forms.ChoiceField( widget = forms.Select(), choices = JANGKA_WAKTU)
    nilai = forms.IntegerField(label="Nilai Taksir",widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    taksir = chosenforms.ChosenModelChoiceField(label = "Data Taksir",queryset=Taksir.objects.all(),widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}))
    bea_materai = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    barang = chosenforms.ChosenModelChoiceField(queryset=Barang.objects.all(),widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_barang'}))
    jenis_transaksi=forms.ChoiceField(choices=CHOICES_JENIS_TRANSAKSI,widget=forms.RadioSelect(attrs={'class':'rad'}))
    jenis_kendaraan = forms.ChoiceField(widget=forms.Select(), choices=JENIS_KENDARAAN)
    ###KENDARAAN
    jangka_waktu_kendaraan = forms.ChoiceField( widget = forms.Select(), choices = JANGKA_WAKTU_KENDARAAN)
 
class AGForm(forms.Form):
    jenis = forms.CharField(widget=forms.TextInput( attrs={'size': 4,'id':'jenis','readonly':'True'}))
    ### nasabah ###
    jenis_keanggotaan = forms.ChoiceField(widget=forms.Select(attrs={'readonly':'True'}),choices=JENIS_KEANGGOTAAN,initial='2')
    #jenis_keanggotaan =forms.ChoiceField(widget=forms.Select(attrs={'readonly':'True'}),choices=JENIS_KEANGGOTAAN,initial='1')
    nama = forms.CharField(max_length=35,widget=forms.TextInput(attrs={'placeholder':'Nama Jelas','class': 'r_nama'}))
    tgl_lahir = forms.DateField(widget=forms.TextInput(attrs={'placeholder':'(Tanggal-Bulan-Tahun)'}))
    tempat = forms.CharField(max_length=15,widget=forms.TextInput(attrs={'placeholder':'Tempat Lahir'}))
    jenis_identitas =forms.ChoiceField(choices=CHOICES_JENIS_IDENTITAS,widget=forms.RadioSelect(attrs={'class':'identitas'}))
        
    no_ktp = forms.CharField(max_length=16,widget=forms.TextInput( attrs={'size': 16,'class': 'r_ktp'}))
    alamat_ktp = forms.CharField(widget=forms.TextInput(attrs={'size': 30}))
    no_rumah_ktp = forms.CharField(max_length=4,widget=forms.TextInput( attrs={'size': 5}),required=True)
    rt_ktp = forms.CharField(max_length=4,widget=forms.TextInput( attrs={'size': 4,'placeholder':'RT',}),required=True)
    rw_ktp = forms.CharField(max_length=4,widget=forms.TextInput( attrs={'size': 4,'placeholder':'RW',}),required=True)
    telepon_ktp = forms.CharField( widget=forms.TextInput(attrs={'size':30}),required=True)
    hp_ktp = forms.CharField( widget=forms.TextInput(attrs={'size':30}),required=True)
    kelurahan_ktp = forms.CharField(max_length=18,widget=forms.TextInput(attrs={'size': 20}),required=True)
    kecamatan_ktp = forms.CharField(max_length=18,widget=forms.TextInput(attrs={'size': 20}),required=True)
    kotamadya_ktp = forms.CharField(max_length=8,widget=forms.TextInput( attrs={'size': 20}),required=True)
    kabupaten_ktp = forms.CharField(max_length=8,widget=forms.TextInput( attrs={'size': 20}),required=True)
    ##Domisili
    alamat_domisili = forms.CharField(widget=forms.TextInput(attrs={'size': 30}))
    no_rumah_domisili = forms.CharField(max_length=4,widget=forms.TextInput( attrs={'size': 5}),required=True)
    rt_domisili = forms.CharField(max_length=4,widget=forms.TextInput( attrs={'placeholder':'RT','size': 4}),required=True)
    rw_domisili = forms.CharField(max_length=4,widget=forms.TextInput( attrs={'placeholder':'RW','size': 4}),required=True)
    telepon_domisili = forms.CharField(max_length=13, widget=forms.TextInput(attrs={'size':30}),required=True)
    hp_domisili = forms.CharField(max_length=13,widget = forms.HiddenInput(),required=False)
    kelurahan_domisili = forms.CharField(max_length=18,widget=forms.TextInput(attrs={'size': 20}),required=True)
    kecamatan_domisili = forms.CharField(max_length=18,widget=forms.TextInput(attrs={'size': 20}),required=True)
    kotamadya_domisili = forms.CharField(max_length=8,widget=forms.TextInput( attrs={'size': 20}),required=True)
    kabupaten_domisili = forms.CharField(max_length=8,widget=forms.TextInput( attrs={'size': 20}),required=True)
    ###SIM
    no_sim = forms.CharField(max_length=12,widget=forms.TextInput( attrs={'size': 16,'value': '0','class':'r_ktp'}))
    alamat_sim = forms.CharField(widget=forms.TextInput(attrs={'size': 30,'value': '0'}))
    rt_sim = forms.CharField(max_length=4, widget=forms.TextInput( attrs={'size': 4,'value': '0'}))
    rw_sim = forms.CharField(max_length=4, widget=forms.TextInput( attrs={'size': 4,'value': '0'}))#,required=True)
    kelurahan_sim = forms.CharField(max_length=18,widget=forms.TextInput(attrs={'size': 20,'value': '0'}))#,required=True)
    kecamatan_sim = forms.CharField(max_length=18,widget=forms.TextInput(attrs={'size': 20,'value': '0'}))#,required=True)
    
    jenis_pekerjaan = forms.ChoiceField(widget=forms.Select(),choices=JENIS_PEKERJAAN,required=True)
 
    alamat_kantor =forms.CharField(widget=forms.TextInput(attrs={'size': 30}))
    kode_pos = forms.CharField(max_length=6, widget=forms.TextInput( attrs={'size': 10}))
    telepon_kantor =forms.CharField(max_length=13,widget=forms.TextInput(attrs={'size':30}),required=True)
    email = forms.CharField(widget=forms.TextInput(attrs={'size': 30}),required=False)
    jenis_kelamin = forms.ChoiceField(widget=forms.Select(), choices=KELAMIN)
    # Data Pasangan
    nama_pasangan = forms.CharField(max_length=35,widget=forms.TextInput(attrs={'placeholder':'Nama Pasangan','class': 'r_nama'}))
    alamat_pasangan = forms.CharField(widget=forms.TextInput(attrs={'size': 30}))
    jekel_pasangan = forms.ChoiceField(widget=forms.Select(), choices=KELAMIN)
    tlp_pasangan = forms.CharField(max_length=13,widget=forms.TextInput(attrs={'size':30}))
    no_rumah_pas = forms.CharField(max_length=4,widget=forms.TextInput(attrs={'size':5,'placeholder':'Nomor',}))
    no_rt_pas = forms.CharField(max_length=4,widget=forms.TextInput(attrs={'size':4,'placeholder':'RT',}))
    no_rw_pas = forms.CharField(max_length=4,widget=forms.TextInput(attrs={'size':4,'placeholder':'RW',}))



    ### Barang ELEKTRONIK###
    #jenis_barang = forms.ChoiceField(widget=forms.Select(), choices=JENIS_BARANG,initial='0',required=False)
    jenis_barang = forms.CharField(required=False,widget=forms.TextInput( attrs={'size': 4,'id':'jenis_barang','readonly':'True'}))
    #merk = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'value': '0'}))
    #type =forms.CharField(max_length=70,widget=forms.TextInput(attrs={'value': '0','size':50}))
    sn = forms.CharField(label="S/N - Imei  ", widget=forms.TextInput( attrs={'size': 30,'value': '0'}))
    warna = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'value': '0'}))
    tahun_pembuatan=forms.CharField(max_length=4,widget=forms.TextInput(attrs={'value': '0'}))
    bulan_produksi =forms.CharField(max_length=10,widget=forms.TextInput(attrs={'value': '0'}))
    lampiran_dokumen = forms.ChoiceField(widget =forms.Select(), choices=JENIS_DOKUMEN)    
    accesoris_barang1=forms.CharField(max_length=150,widget=forms.TextInput(attrs={'value': '0','class': 'r_nama'}))
    fungsi_system = forms.CharField(required=False,max_length=70,widget=forms.TextInput(attrs={'value': '0'}))
    
    ### KENDARAAN ####
    jenis_kendaraan = forms.ChoiceField(required=False,widget=forms.Select(attrs={'id':'id_jenis_kendaraan','onchange':'hitungJasa(),akumulasi()'}), choices=JENIS_KENDARAAN)
    merk_kendaraan = forms.ChoiceField(required=False,widget=forms.Select(), choices=MERK_KENDARAAN_CHOICES)
    type_kendaraan =forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'value': '0'}))
    tahun_pembuatan_kendaraan =forms.ChoiceField(required=False,widget=forms.Select(), choices=TAHUN_KENDARAAN_CHOICES)
    no_polisi = forms.CharField(required=False,max_length=15,widget=forms.TextInput(attrs={}))
    no_rangka = forms.CharField(required=False,max_length=15,widget=forms.TextInput(attrs={}))
    no_mesin  = forms.CharField(required=False,max_length=15,widget=forms.TextInput(attrs={}))
    warna_kendaraan = forms.CharField(required=False,max_length=30,widget=forms.TextInput(attrs={}))
    no_bpkb = forms.CharField(required=False,max_length=30,widget=forms.TextInput(attrs={}))
    stnk_atas_nama = forms.CharField(required=False,max_length=30,widget=forms.TextInput(attrs={'value': '0'}))
    no_faktur = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'value': '0'}))
    
    
    
    ### AkadGadai ###
    #tanggal = forms.DateField(initial = datetime.date.today,widget=forms.DateTimeInput(attrs={'readonly':'true'}))
    tanggal = forms.SplitDateTimeField(initial = datetime.datetime.now)

    #gerai = forms.ModelChoiceField(queryset=Tbl_Cabang.objects.all(),empty_label="--- PILIH ---")
    #jangka_waktu = forms.ChoiceField( widget = forms.Select(attrs={'id':'jangka_waktu','onchange':'hitungJasa(),akumulasi()'}),\
        #choices = JANGKA_WAKTU)
    jangka_waktu = forms.CharField(widget=forms.TextInput( attrs={'readonly':'True','size': 4,'id':'jangka_waktu','onchange':'hitungJasa();akumulasi()'}))

    ###KENDARAAN
    jangka_waktu_kendaraan = forms.ChoiceField( widget = forms.Select(attrs={'readonly':'True','id':'jangka_waktu_kendaraan','onchange':'hitungJasa();akumulasi()'}),\
        choices = JANGKA_WAKTU_KENDARAAN)
    nilai = forms.IntegerField(label="Nilai Pinjaman",widget=forms.TextInput(attrs={'id':'nilai','alt': 'integer', 'class': 'rp_plafon uang','onkeyup':'hitungJasa();akumulasi()'}))
    #taksir = forms.ModelChoiceField(queryset=Taksir.objects.all(),label="TAKSIR",empty_label="--- PILIH ---")
    taksir = chosenforms.ChosenModelChoiceField(label = "Data Taksir",queryset=Taksir.objects.all(),widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}))
    bea_materai = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':'0',\
        'id':'materai','onkeyup':'akumulasi()'}))
    #jenis_transaksi =forms.ChoiceField(choices=CHOICES_JENIS_TRANSAKSI,widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'rad','id':'jenis_transaksi','readonly':'True'}))
    jenis_transaksi =forms.CharField(widget=forms.TextInput( attrs={'size': 4,'id':'jenis_transaksi','readonly':'True'}))
    tanda_tangan = forms.FileField()
    foto_nasabah = forms.FileField()
    berkas_barang = forms.FileField()
    
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
    fungsi_sistem = forms.CharField(required=False,label="FUNGSI SYSTEM ", widget=forms.TextInput( attrs={'size': 30,'class':'formhp formbarang '}))
    
    lensa = forms.ChoiceField(required=False,widget =forms.Select(attrs={'class':'formkamera formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_lensa = forms.ChoiceField(required=False,widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formkamera formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    batre_kamera = forms.ChoiceField(required=False,widget =forms.Select(attrs={'class':'formkamera formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_batre_kamera = forms.ChoiceField(required=False,widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formkamera formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    cassing_kamera = forms.ChoiceField(required=False,widget =forms.Select(attrs={'class':'formkamera formbarang'}), choices=CHOICES_BARANG, initial='2')
    kondisi_cassing_kamera = forms.ChoiceField(required=False,widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formkamera formbarang'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    
    optik_ps = forms.ChoiceField(required=False,widget =forms.Select(attrs={'class':'formbarang formps'}), choices=CHOICES_BARANG, initial='2')
    kondisi_optik_ps = forms.ChoiceField(required=False,widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formps'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    harddisk  = forms.ChoiceField(required=False,widget =forms.Select(attrs={'class':'formbarang formps'}), choices=CHOICES_BARANG, initial='2')
    kondisi_harddisk = forms.ChoiceField(required=False,widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formps'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    stick  = forms.ChoiceField(required=False,widget =forms.Select(attrs={'class':'formbarang formps'}), choices=CHOICES_BARANG, initial='2')
    kondisi_stick = forms.ChoiceField(required=False,widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formps'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    hdmi  = forms.ChoiceField(required=False,widget =forms.Select(attrs={'class':'formbarang formps'}), choices=CHOICES_BARANG, initial='2')
    kondisi_hdmi = forms.ChoiceField(required=False,widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formps'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    
    dus = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang'}), choices=CHOICES_BARANG, initial='2')
    tas = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang'}), choices=CHOICES_BARANG, initial='2')
    layar_tv = forms.ChoiceField(required=False,widget =forms.Select(attrs={'class':'formbarang formtv'}), choices=CHOICES_BARANG, initial='2')
    kondisi_layar_tv = forms.ChoiceField(required=False,widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formbarang formtv'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    remote = forms.ChoiceField(required=False,widget =forms.Select(attrs={'class':'formbarang formtv'}), choices=CHOICES_BARANG, initial='2')
    kondisi_remote = forms.ChoiceField(required=False,widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formbarang formtv'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    
    jasa_baru = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'jasa_baru'}))    
    beasimpan_baru = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'beasimpan_baru'}))    
    adm_baru = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'adm_baru'}))
    total_all = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'total_all'}))
    #####BARU PARAMETER PRODUK
    nilai_jasa = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'nilai_jasa'}))
    nilai_biayasimpan = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'nilai_biayasimpan'}))
    nilai_adm = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'nilai_adm'}))
    nilai_materai = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'nilai_materai'}))
    nilai_pembagi = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'True','alt': 'integer', 'class': 'uang','id':'nilai_pembagi'}))
    ###validasi no ktp
    
    def clean_no_ktp(self):
        no_ktp = self.cleaned_data['no_ktp']
        if Nasabah.objects.filter(no_ktp=no_ktp).exists():
            raise ValidationError("Pengajuan ini sudah terdaftar")
        return no_ktp
    
    def cek_number_ktp(value):
        if value % 2 != 0:
            raise ValidationError(u'%s nomor ktp terlalu banyak' % value)

    

