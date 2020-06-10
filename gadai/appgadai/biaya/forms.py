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
        ('','---'),
	('1','KAS'),
	('2','UANG MUKA'),
)
##Coiches untuk Materai Aja
JENIS_TRANSAKSI_MATERAI =( 
        ('','---'),
	('1','KAS'),
	('2','BIAYA'),
	('3','UANG MUKA'),
)
##akhir choices untuk Materai Aja
JS_TRANSAKSI =(
        ('','-------'),
	('BANK','BANK'),
	('KAS','KAS'),
)

##Coiches untuk Adm Bank Aja
JENIS_TRANSAKSI_BANK =( 
    ('','---'),
	('1','BANK'),

)

GERAI_PILIH =(
        ('','------'),
	('PUSAT','PUSAT'),('JAKARTA','JAKARTA'),('SUCI','SUCI'),('DIPATIUKUR','DIPATIUKUR'),('BALUBUR','BALUBUR'),
	('HILIR','GERLONG HILIR'),('KOPO','KOPO'),('CIBIRU','CIBIRU'),('CIPACING','CIPACING'),('JATINANGOR','JATINANGOR'),
	('CIMAHI','CIMAHI'),('BUAHBATU','BUAHBATU'),
	('MARANATA','MARANATA'),
	('CIREBON','CIREBON PERJUANGAN'),('CIUMBULEUIT','CIUMBULEUIT'),('UJUNGBERUNG','UJUNGBERUNG'),('CIWASTRA','CIWASTRA'),
)


class HorizRadioRenderer(forms.RadioSelect.renderer):
	def render(self):
		return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class BiayaForm(ModelForm):
	#gerai = forms.ModelChoiceField(queryset=Tbl_Cabang.objects.all())
	tanggal = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'true'}, format="%d-%m-%Y"))
	
	listrik = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
	ket_listrik = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
	
	pdam  = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
	ket_pdam = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
	
	telpon = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
	ket_telpon = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
	
	majalah = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
	ket_majalah = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
	
	
	penambahan_saldo = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}),required = False)
	ket_penambahan_saldo = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
	pengembalian_saldo = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))
	ket_pengembalian_saldo = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
	penambahan_uk = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))
	ket_penambahan_uk = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
	pengembalian_uk = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))
	ket_pengembalian_uk = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
	
	palkir = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))
	ket_palkir = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
	
	bbm = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))
	ket_bbm = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
	
	materai = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))
	ket_materai = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
	
	pemb_lingkungan = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))
	ket_pemb_lingkungan = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
	
	foto_copy  = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
	ket_foto_copy = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
	
	sumbangan  = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
	ket_sumbangan = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
	
	konsumsi  = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
	ket_konsumsi = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
	
	perlengkapan  = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
	ket_perlengkapan = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
	
	lain_lain = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=AKUN_PILIH,required = False)
	ket_lain_lain = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
	
	penerimaan_saldo = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}),required = False)
	
	#nilai_lain_lain = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))
	
	####automatis ketika status barang lunas terjual

	####automatis ketika status barang lunas terjual
	saldo_awal = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}),required = False)
	saldo_akhir = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}),required = False)
	
	#antar_gerai = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=GERAI_PILIH,required = False)
	js_trans = forms.ChoiceField(widget=forms.Select(),choices=JS_TRANSAKSI,required=False)
	#antar_gerai_kembali = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=GERAI_PILIH,required = False)
        antar_gerai_kembali = chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
        antar_gerai = chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),required = False)
	js_trans_kembali = forms.ChoiceField(widget=forms.Select(),choices=JS_TRANSAKSI,required=False)
	
	jenis_transaksi_listrik	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
	jenis_transaksi_pdam	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
	jenis_transaksi_telepon	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
	jenis_transaksi_foto_copy	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
	jenis_transaksi_majalah	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
	#jenis_transaksi_iuran_keamanan	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
	#jenis_transaksi_iuran_kebersihan	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
	#jenis_transaksi_air_minum	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
	jenis_transaksi_palkir	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
	jenis_transaksi_bbm	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
	#jenis_transaksi_pulsa	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
	jenis_transaksi_materai	= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI_MATERAI,required = False)
	jenis_transaksi_nilai_lain_lain= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
	jenis_transaksi_pemb_lingkungan= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
	jenis_transaksi_sumbangan= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
	jenis_transaksi_perlengkapan= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
	jenis_transaksi_konsumsi= chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)

        jenis_transaksi_biaya_bank = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI_BANK,required = False)
        biaya_bank = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))
        ket_biaya_bank = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)

        jenis_transaksi_pengiriman = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_TRANSAKSI,required = False)
        pengiriman = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10}))
        ket_pengiriman = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
	class Meta:
		model = Biaya

