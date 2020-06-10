from django import forms
from django.forms import ModelForm
from gadai.appgadai.models import *
from chosen import forms as chosenforms
from django.utils.safestring import mark_safe

AKUN_PILIH = (
	('519','Beban Transportasi & Perjalan Dinas'),('520','Beban Sewa'),('521','Beban Perlengkapan'),
	('523','Beban Dokumentasi'),('525','Beban Pembinaan Lingkungan'),('526','Beban Konsumsi'),('527','Beban Sumbangan'),
	('528','Beban Iuran & Ijin Lembaga Pemerintah'),('529','Beban Pemeliharaan & Perbaikan Peralatan Kantor'),('530','Beban Pemeliharaan & Perbaikan Peralatan Gedung'),
	('531','Transportasi'),('532','Beban Pemeliharaan & perbaikan Gedung'),('537','Beban Promosi'),('539','Beban Adm % Umum Lain-Lain')
)

JENIS_TRANSAKSI =(
        ('','--------'),
	('1','KAS'),
	('2','UANG MUKA'),
)

JS_TRANSAKSI =(
        ('','--------'),
	('BANK','BANK'),
	('KAS','KAS'),
)

GERAI_PILIH =(
	('1','JAKARTA'),('2','SUCI'),('3','DIPATIUKUR'),('4','BALUBUR'),
	('6','GERLONG HILIR'),('7','KOPO'),('8','CIBIRU'),('9','CIPACING'),('10','JATINANGOR'),
	('11','CIMAHI'),('12','BUAHBATU'),('15','MARANATA'),
	('17','CIREBON PERJUANGAN'),('19','CIUMBULEUIT'),('20','UJUNGBERUNG'),('21','CIWASTRA'),('22','BOJONGSOANG')
)


class HorizRadioRenderer(forms.RadioSelect.renderer):
	def render(self):
		return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class BiayasForm(forms.Form):
    #gerai = forms.ModelChoiceField(queryset=Tbl_Cabang.objects.all())
    tanggal = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'true'}, format="%d-%m-%Y"))
    penambahan_saldo = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}),required = False)
    ket_penambahan_saldo = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    pengembalian_saldo = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))
    ket_pengembalian_saldo = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    antar_gerai =chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
    js_trans = forms.ChoiceField(widget=forms.Select(),choices=JS_TRANSAKSI,required = False)
    antar_gerai_kembali = chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
    js_trans_kembali = forms.ChoiceField(widget=forms.Select(),choices=JS_TRANSAKSI,required = False)


class HorizRadioRenderer(forms.RadioSelect.renderer):
	def render(self):
		return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class BiayaPusatForm(ModelForm):
    tanggal = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'true'}, format="%d-%m-%Y"))
    listrik = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
    ket_listrik = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    #listrik_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)

    #gaji  = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
    #ket_gaji = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    #gaji_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
    
    sewa  = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}),required = False)
    ket_sewa = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    #sewa_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
	
    pdam  = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
    ket_pdam = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    #pdam_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)

    telpon = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
    ket_telpon = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    #telpon_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
	
    majalah = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}),required = False)
    ket_majalah = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    #majalah_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
    	
    pemb_lingkungan = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))
    ket_pemb_lingkungan = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    #lingkungan_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
	
    foto_copy  = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
    ket_foto_copy = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    #fotocopy_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
	
    sumbangan  = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
    ket_sumbangan = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    #sumbangan_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
	
    konsumsi  = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
    ket_konsumsi = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    #konsumsi_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
	
    perlengkapan  = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
    ket_perlengkapan = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    #perlengkapan_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
	
    penerimaan_saldo = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}),required = False)
    	
    ####automatis ketika status barang lunas terjual
    pendapatan_lain = forms.IntegerField(widget=forms.TextInput(attrs={'size':10,'alt': 'integer', 'class': 'uang','value':0}),required = False)
    ket_pendapatan_lain = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    ####automatis ketika status barang lunas terjual
    #saldo_awal = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':sum([p.kredit for p in Tbl_TransaksiKeu.objects.filter(id_coa__coa = '11.01.05').filter(tgl_trans=datetime.date.today())]),'size':10}),required = False)
    #saldo_awal = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}),required = False)
    saldo_awal = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':sum([p.saldo for p in Tbl_TransaksiKeu.objects.filter(id_coa__coa = '11.01.05').filter(tgl_trans=datetime.date.today())]) + sum([p.debet for p in Tbl_Transaksi.objects.filter(id_coa__coa = '11.01.05').filter(tgl_trans=datetime.date.today())]) - sum([p.kredit for p in Tbl_Transaksi.objects.filter(id_coa__coa = '11.01.05').filter(tgl_trans=datetime.date.today())]),'size':10}),required = False)
    saldo_akhir = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}),required = False)

    antar_gerai_kembali = chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
    antar_gerai = chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)	
    js_trans = forms.ChoiceField(widget=forms.Select(),choices=JS_TRANSAKSI,required=False)
    js_trans_kembali = forms.ChoiceField(widget=forms.Select(),choices=JS_TRANSAKSI,required=False)

    jenis_transaksi_gaji = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
    jenis_transaksi_sewa = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
    jenis_transaksi_listrik	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
    jenis_transaksi_pdam	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
    jenis_transaksi_telepon	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
    jenis_transaksi_foto_copy	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
    jenis_transaksi_majalah	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
	
    jenis_transaksi_palkir	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
    	
    jenis_transaksi_pemb_lingkungan= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
    jenis_transaksi_sumbangan= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
    jenis_transaksi_perlengkapan= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
    jenis_transaksi_konsumsi= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)

    ### Tambahan SEPUR
    jenis_transaksi_bbm = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)	
    jenis_transaksi_tol = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
    jenis_transaksi_transport = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
    jenis_transaksi_peralkantor = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
    
    bbm  = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
    ket_bbm = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    #bbm_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)

    tol  = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
    ket_tol = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    #tol_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
 
    transport  = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
    ket_transport = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    #transport_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)

    peralkantor  = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
    ket_peralkantor = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    #peralkantor_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)

    nilai_materai = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))
    keterangan_materai= forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)

    ## Tambahan Uang Muka
    penambahan_uk = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))
    ket_penambahan_uk = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    pengembalian_uk = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))
    ket_pengembalian_uk = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)

    pembelian_materai = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))
    ket_pmb_materai= forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    jenis_pmb_materai = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)

    jual_materai = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))
    ket_jual_materai= forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    jenis_jual_materai = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)

    class Meta:
        model = BiayaPusat

class BiayaPusatGeraiForm(forms.Form):
    jenis_transaksi_telepon	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JS_TRANSAKSI,required = False)
    ket_telpon = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    telpon_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
    telpon = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))
	
    jenis_transaksi_bbm	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JS_TRANSAKSI,required = False)
    ket_bbm = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    bbm_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
    bbm = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))

    jenis_transaksi_sumbangan	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JS_TRANSAKSI,required = False)
    ket_sumbangan = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    sumbangan_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
    sumbangan = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))
    ##ACAN
    jenis_transaksi_listrik	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JS_TRANSAKSI,required = False)
    ket_listrik = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    listrik_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
    listrik = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))

    jenis_transaksi_pdam = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JS_TRANSAKSI,required = False)
    ket_pdam = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    pdam_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
    pdam = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))

    jenis_transaksi_transport = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JS_TRANSAKSI,required = False)
    ket_transport = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    transport_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
    transport = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))

    #jenis_transaksi_palkir = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JS_TRANSAKSI,required = False)
    #ket_palkir = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    #palkir_gerai= chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
    #palkir = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))

