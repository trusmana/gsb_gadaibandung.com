from django import forms
from django.forms import ModelForm
from gadai.appgadai.models import *
from django.utils.safestring import mark_safe

class HorizRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

JENIS_REPORT =(
    #('1','EXCEL'),('2','PDF'),
    ('3','VIEW'),
)

class FilterForm(forms.Form):
    report = forms.ChoiceField(widget = forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'id_report'}), choices = JENIS_REPORT)
    gerai = forms.ModelChoiceField(queryset=Tbl_Cabang.objects.all())
    start_date = forms.DateField(initial= datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,'readonly':'false'}, format="%Y-%m-01"))
    end_date = forms.DateField(initial= datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,'readonly':'false'}, format="%Y-%m-%d"))

class AppKeuGuForm(forms.Form):
    status_oto_gerai = forms.ChoiceField(widget=forms.Select(attrs={'readonly':'True'}),choices=STATUS_OTO_TITIPAN,initial='1') 
    nilai = forms.IntegerField(label="Total TItipan",widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true',}))

class AppKeuPusatGuForm(forms.Form):
    status_oto_pusat = forms.ChoiceField(widget=forms.Select(attrs={'readonly':'True'}),choices=APPROVE_OTO_TITIPAN,initial='1') 
    nilai = forms.IntegerField(label="Total TItipan",widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true',}))
    note = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Masukan Keterangan Nilai Yg ingin Ada Diskon'}),required=False)

class PengambilanForm(forms.Form):
    nilai = forms.IntegerField(label="Nilai Yang Setor",widget=forms.TextInput(attrs={'size': 8, 'value': '0','alt': 'integer','class': 'rp_nilai uang'}))
    #jenis_pengambilan =forms.ChoiceField(label="Jenis Pembayaran",choices=JENIS_TRANSAKSI,widget=forms.RadioSelect(attrs={'class':'rad'}))

class DenominasiForm(forms.ModelForm):
    kertas_seratusribu = forms.IntegerField(label="Kertas 100.000",widget=forms.TextInput(attrs={'size': 2, 'value': '0','alt': 'integer','class': 'rp_nilai uang'}))
    kertas_limapuluhribu = forms.IntegerField(label="Kertas 50.000",widget=forms.TextInput(attrs={'size': 2, 'value': '0','alt': 'integer','class': 'rp_nilai uang'}))
    kertas_duapuluhribu = forms.IntegerField(label="Kertas 20.000",widget=forms.TextInput(attrs={'size': 2, 'value': '0','alt': 'integer','class': 'rp_nilai uang'}))
    kertas_sepuluhribu = forms.IntegerField(label="Kertas 10.000",widget=forms.TextInput(attrs={'size': 2, 'value': '0','alt': 'integer','class': 'rp_nilai uang'}))
    kertas_limaribu = forms.IntegerField(label="Kertas 5.000",widget=forms.TextInput(attrs={'size': 2, 'value': '0','alt': 'integer','class': 'rp_nilai uang'}))
    kertas_duaribu = forms.IntegerField(label="Kertas 2.000",widget=forms.TextInput(attrs={'size': 2, 'value': '0','alt': 'integer','class': 'rp_nilai uang'}))
    kertas_seribu = forms.IntegerField(label="Kertas 1.000",widget=forms.TextInput(attrs={'size': 2, 'value': '0','alt': 'integer','class': 'rp_nilai uang'}))
    koin_seribu = forms.IntegerField(label="Logam 1.000",widget=forms.TextInput(attrs={'size': 2, 'value': '0','alt': 'integer','class': 'rp_nilai uang'}))
    koin_limaratus = forms.IntegerField(label="Logam 500",widget=forms.TextInput(attrs={'size': 2, 'value': '0','alt': 'integer','class': 'rp_nilai uang'}))
    koin_duaratus = forms.IntegerField(label="Logam 200",widget=forms.TextInput(attrs={'size': 2, 'value': '0','alt': 'integer','class': 'rp_nilai uang'}))
    koin_seratus = forms.IntegerField(label="Logam 100",widget=forms.TextInput(attrs={'size': 2, 'value': '0','alt': 'integer','class': 'rp_nilai uang'}))
    koin_limapuluh = forms.IntegerField(label="Logam 50",widget=forms.TextInput(attrs={'size': 2, 'value': '0','alt': 'integer','class': 'rp_nilai uang'}))
    koin_dualima = forms.IntegerField(label="Logam 25",widget=forms.TextInput(attrs={'size': 2, 'value': '0','alt': 'integer','class': 'rp_nilai uang'}))
    #gerai = forms.CharField(max_length=35,widget=forms.TextInput(attrs={'size': 2, 'alt': 'integer','class': 'rp_nilai uang'}))
    #tanggal = forms.DateField(label="Tanggal",initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 5,'readonly':'True'},format= "%d-%m-%Y"))

    class Meta:
        model = Denominasi
        widgets = {'gerai': forms.HiddenInput(),
                   'tanggal' : forms.HiddenInput(),
                   'jumlah_kertas_seratusribu': forms.HiddenInput(), 
                   'jumlah_kertas_limapuluhribu': forms.HiddenInput(), 
                   'jumlah_kertas_duapuluhribu': forms.HiddenInput(), 
                   'jumlah_kertas_sepuluhribu': forms.HiddenInput(), 
                   'jumlah_kertas_limaribu': forms.HiddenInput(), 
                   'jumlah_kertas_duaribu': forms.HiddenInput(), 
                   'jumlah_kertas_seribu': forms.HiddenInput(), 
                   'jumlah_koin_seribu': forms.HiddenInput(), 
                   'jumlah_koin_limaratus': forms.HiddenInput(), 
                   'jumlah_koin_duaratus': forms.HiddenInput(), 
                   'jumlah_koin_seratus': forms.HiddenInput(), 
                   'jumlah_koin_limapuluh': forms.HiddenInput(), 
                   'jumlah_koin_dualima': forms.HiddenInput(), 
                  }
'''
class KasirGeraiPelunasanForm(forms.ModelForm):
    nilai_terima_bersih = forms.IntegerField(label="Total Pelunasan",widget=forms.TextInput(attrs={'size': 10,'alt': 'integer',\
        'class': 'rp_nilai uang','readonly':'true',}))
    nilai_pembulatan = forms.IntegerField(label="Nilai Yang Dibayarkan",widget=forms.TextInput(attrs={'size': 10, 'alt': 'integer',\
        'class': 'rp_nilai uang','onkeyup':'total_dibayar()'}))
    selisih  = forms.IntegerField(label="Selisih",widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class':\
        'rp_nilai uang','readonly':'true'})) 
    jenis_transaksi =forms.ChoiceField(label="Jenis Transaksi",choices=JENIS_TRANSAKSI,widget=forms.RadioSelect(attrs={'class':'rad'}))
    tanggal = forms.DateField(label="Tanggal",initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'True'},\
        format= "%d-%m-%Y"))
    nilai_dibayar = forms.IntegerField(label="Titipan Pelunasan",widget=forms.TextInput(attrs={'size': 10,'alt': 'integer',\
        'class': 'rp_nilai uang','readonly':'true'}))
    sisa_bayar =forms.IntegerField(label="Sisa Yang Harus Dibayar",widget=forms.TextInput(attrs={'size': 10,'alt': 'integer',\
        'class': 'rp_nilai uang','readonly':'true'}))
    rek_tab = forms.CharField(max_length=35,required=False,widget=forms.TextInput(attrs={'size': 10,'alt': 'integer',\
        'class': 'formbank' ,'type':'displanone'}))
    class Meta:
        model = KasirGeraiPelunasan
        fields = ('nilai_terima_bersih','nilai_dibayar','sisa_bayar','nilai_pembulatan','selisih','tanggal','jenis_transaksi','rek_tab')
        widgets = {
            'kasir_lunas' : forms.HiddenInput(),
            'nilai' : forms.HiddenInput(),
            'coa_sisa' : forms.HiddenInput(),
            'val' : forms.HiddenInput(),
            'status' : forms.HiddenInput(),
            }
'''
class KasirGeraiPelunasanForm(forms.ModelForm):
    nilai_terima_bersih = forms.IntegerField(label="Total Pelunasan",widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true',}))
    nilai_pembulatan = forms.IntegerField(label="Nilai Yang Di Setor/Di Transfer",widget=forms.TextInput(attrs={'size': 10, 'alt': 'integer','class': 'rp_nilai uang','onkeyup':'total_dibayar()'}))
    selisih  = forms.IntegerField(label="Kurang/lebih Setoran",widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'True','onkeyup':'tes_cuy()'})) 
    jenis_transaksi =forms.ChoiceField(label="Jenis Pembayaran",choices=JENIS_TRANSAKSI,widget=forms.RadioSelect(attrs={'class':'rad','value':0}))
    tanggal = forms.DateField(label="Tanggal",initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 10,'readonly':'True'},format= "%d-%m-%Y"))
    nilai_dibayar = forms.IntegerField(label="Titipan Pelunasan",widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))
    sisa_bayar = forms.IntegerField(label="Sisa Yang Harus Dibayar",widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))
    rek_tab = forms.CharField(label="Keterangan",required=False,widget=forms.Textarea(attrs={'size': 5,'class': 'formbank' }))
    kelebihan = forms.IntegerField(label="Pembulatan",widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang formbank','value':0,'onkeyup':'lebih_bray()'}))
    kelebihan_transfer = forms.IntegerField(label="Pengembalian Ke nasabah",widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang formbank','readonly':'True','value':0}))
    class Meta:
        model = KasirGeraiPelunasan
        fields = ('jenis_transaksi','tanggal','nilai_terima_bersih','nilai_dibayar','sisa_bayar','nilai_pembulatan','selisih',
                  'kelebihan','kelebihan_transfer','rek_tab')
        widgets = {
            'kasir_lunas' : forms.HiddenInput(),
            'nilai' : forms.HiddenInput(),
            'coa_sisa' : forms.HiddenInput(),
            'val' : forms.HiddenInput(),
            'status' : forms.HiddenInput(),

            }
class KasirGeraiForm(forms.ModelForm):
    kasir = forms.ModelChoiceField(queryset=AkadGadai.objects.all())
    #no_pinjaman = forms.CharField(max_length=35)
    nilai = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10, 'value': '0','alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))    
    nilai_terima_bersih = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))
    nilai_pembulatan = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10, 'alt': 'integer','class': 'rp_nilai uang','onkeyup':'total_dibayar()'}))
    selisih  = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'})) 
    jenis_transaksi =forms.ChoiceField(choices=JENIS_TRANSAKSI,widget=forms.RadioSelect(attrs={'class':'rad'}))
    tanggal = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'false'},format= "%d-%m-%Y"))
    nilai_dibayar = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))
    #nilai_yg_bayar  = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'class': 'rp_nilai uang','readonly':'true'}))
    sisa_bayar =forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))

    class Meta:
        model = KasirGerai
        
    #def kasir(self):
        #try:
            #return self.kasir
        #except KasirGerai.DoesNotExist:
            #return None
        
class KasirGeraiOtoForm(forms.ModelForm):
    kasir = forms.ModelChoiceField(queryset=AkadGadai.objects.all())
    #no_pinjaman = forms.CharField(max_length=35)
    nilai = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10, 'value': '0','alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))    
    nilai_terima_bersih = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))
    nilai_pembulatan = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10, 'alt': 'integer','class': 'rp_nilai uang','onkeyup':'total_dibayar()'}))
    selisih  = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang'})) 
    jenis_transaksi =forms.ChoiceField(choices=JENIS_TRANSAKSI,widget=forms.RadioSelect(attrs={'class':'rad'}))
    tanggal = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'false'},format= "%d-%m-%Y"))
    nilai_dibayar = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))
    #nilai_yg_bayar  = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'class': 'rp_nilai uang','readonly':'true'}))
    sisa_bayar =forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))

    class Meta:
        model = KasirGerai



class KasirGeraiCairForm(forms.ModelForm):
    kasir = forms.ModelChoiceField(queryset=AkadGadai.objects.all())
    #no_pinjaman = forms.CharField(max_length=35)
    nilai = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10, 'value': '0','alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))    
    nilai_terima_bersih = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))
    nilai_pembulatan = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10, 'alt': 'integer','class': 'rp_nilai uang','onkeyup':'total_dibayar()'}))
    selisih  = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang'})) 
    jenis_transaksi =forms.ChoiceField(choices=JENIS_TRANSAKSI,widget=forms.RadioSelect(attrs={'class':'rad'}))
    tanggal = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'false'}, format="%d-%m-%Y"))
    rek_tab = forms.CharField(max_length=35,required=False)

    class Meta:
        model = KasirGerai
        
    def kasir(self):
        try:
            return self.kasir
        except KasirGerai.DoesNotExist:
            return None       

'''
class Kasir_App_GU_Form(forms.Form):
    #kasir = forms.ModelChoiceField(queryset=AkadGadai.objects.all())
    #no_pinjaman = forms.CharField(max_length=35)
    nilai = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10, 'value': '0','alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))    
    nilai_terima_bersih = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))
    nilai_pembulatan = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10, 'alt': 'integer','class': 'rp_nilai uang','onkeyup':'total_dibayar()'}))
    selisih  = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'})) 
    jenis_transaksi =forms.ChoiceField(choices=JENIS_TRANSAKSI,widget=forms.RadioSelect(attrs={'class':'rad'}))
    tanggal = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput( format="%d-%m-%Y"))
    nilai_dibayar = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))
    #nilai_yg_bayar  = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'class': 'rp_nilai uang','readonly':'true'}))
    sisa_bayar =forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))
    nilai_kewajiban_pelunasan = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))
    biaya_gu = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))
    rek_tab = forms.CharField(max_length=35,required=False,widget=forms.TextInput(attrs={'size': 20,'class': 'formbank'}))
    kelebihan = forms.IntegerField(label="Pembulatan",widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang formbank','value':0,'onkeyup':'lebih_bray()'}))
    kelebihan_transfer = forms.IntegerField(label="Pengembalian Ke nasabah",widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang formbank','readonly':'True','value':0}))
'''
class Kasir_App_GU_Form(forms.Form):
    #kasir = forms.ModelChoiceField(queryset=AkadGadai.objects.all())
    #no_pinjaman = forms.CharField(max_length=35)
    jenis_transaksi =forms.ChoiceField(choices=JENIS_TRANSAKSI,widget=forms.RadioSelect(attrs={'class':'rad'}))
    nilai = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10, 'value': '0','alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))    
    nilai_terima_bersih = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))
    nilai_pembulatan = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10, 'alt': 'integer','class': 'rp_nilai uang','onkeyup':'total_dibayar(),tes_cuy()'}))
    selisih  = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'})) 
    
    tanggal = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput( format="%d-%m-%Y"))
    nilai_dibayar = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))
    #nilai_yg_bayar  = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'class': 'rp_nilai uang','readonly':'true'}))
    sisa_bayar =forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))
    nilai_kewajiban_pelunasan = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))
    biaya_gu = forms.IntegerField(widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang','readonly':'true'}))
    rek_tab = forms.CharField(max_length=35,required=False,widget=forms.TextInput(attrs={'size': 20,'class': 'formbank'}))
    kelebihan = forms.IntegerField(label="Pembulatan",widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang formbank','value':0}))
    kelebihan_transfer = forms.IntegerField(label="Pengembalian Ke nasabah",widget=forms.TextInput(attrs={'size': 10,'alt': 'integer','class': 'rp_nilai uang formbank','readonly':'True','value':0}))
    class Meta:
        model = KasirGerai
        
    def kasir(self):
        try:
            return self.kasir
        except KasirGerai.DoesNotExist:
            return None 

