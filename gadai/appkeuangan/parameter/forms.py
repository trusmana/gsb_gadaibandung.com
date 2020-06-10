from django import forms
from django.forms import ModelForm
from django.forms.formsets import formset_factory
from chosen import forms as chosenforms
from gadai.appgadai.models import *
from django.contrib.admin.widgets import AdminDateWidget
from django.conf import settings
import datetime


class AydaMapperForm(ModelForm):   
    item = forms.ChoiceField( widget = forms.Select(),choices=ITEM_JURNAL_AYDA)
    cabang = chosenforms.ChosenModelChoiceField(required = False,queryset=Tbl_Cabang.objects.all(),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}))
    debet = chosenforms.ChosenModelChoiceField(label = "Debet Pusat Ayda",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    kredit = chosenforms.ChosenModelChoiceField(label = "Kredit Pusat Ayda",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    debet_lawan = chosenforms.ChosenModelChoiceField(label = "Debet Gerai Ayda",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    kredit_lawan = chosenforms.ChosenModelChoiceField(label = "Kredit Gerai Ayda",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    kredit_lawan1 = chosenforms.ChosenModelChoiceField(label = "Kredit1 Gerai Ayda",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    kredit_lawan2 = chosenforms.ChosenModelChoiceField(label = "Kredit2 Gerai Ayda",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    debet_penjualan = chosenforms.ChosenModelChoiceField(label = "Debet Penjualan Ayda",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    debet_penjualan_untung = chosenforms.ChosenModelChoiceField(label = "Debet Penjualan Ayda Rugi",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    debet_penjualan_rugi = chosenforms.ChosenModelChoiceField(label = "Debet Penjualan Ayda",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    kredit_penjualan = chosenforms.ChosenModelChoiceField(label = "Kredit Penjualan Ayda",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    kredit_penjualan_ayda = chosenforms.ChosenModelChoiceField(label = "Kredit Penjualan Ayda Untung",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)

    class Meta:
        model = AydaMapper

class KasirPelunasanRakMapperForm(forms.ModelForm):
    item = forms.ChoiceField( widget = forms.Select(), choices = JENIS_RAK)
    jenis = forms.ChoiceField( widget = forms.Select(), choices = JENIS_TRANS)
    cabang = chosenforms.ChosenModelChoiceField(label = "Cabang",queryset=Tbl_Cabang.objects.all(),required = False)    
    ke_cabang = chosenforms.ChosenModelChoiceField(label = "Ke Cabang",queryset=Tbl_Cabang.objects.all(),required = False)    
    coa_2 = chosenforms.ChosenModelChoiceField(label = "Bank / Kas",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_3 = chosenforms.ChosenModelChoiceField(label = "Pendapatan Lainnya",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_4 = chosenforms.ChosenModelChoiceField(label = "Beban Lainnya",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    debet_rak_cabang = chosenforms.ChosenModelChoiceField(label = "RAK Cabang",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    kredit_rak_pusat = chosenforms.ChosenModelChoiceField(label = "RAK Ke Cabang",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)   
    coa_1 = chosenforms.ChosenModelChoiceField(label = "Titipan Pelunasan",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    rak_debet_pusat1 = chosenforms.ChosenModelChoiceField(label = "RAK Debet Pusat",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    rak_kredit_pusat2 = chosenforms.ChosenModelChoiceField(label = "RAK Kredit Pusat",queryset=Tbl_Akun.objects.all().\
        order_by('coa'),required = False)
    class Meta:
        model = KasirPelunasanRakMapper
        fields = ('item','jenis','cabang','ke_cabang','coa_2','coa_3','coa_4','debet_rak_cabang','kredit_rak_pusat','coa_1','rak_debet_pusat1',\
            'rak_kredit_pusat2')

class RakPusatMapperForm(forms.ModelForm):
    cabang = chosenforms.ChosenModelChoiceField(label = "Gerai",queryset=Tbl_Cabang.objects.all(),required = False)
    coa_rak_cabang = chosenforms.ChosenModelChoiceField(label = "Coa Rak Cabang",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)    
    coa_rak_pusat = chosenforms.ChosenModelChoiceField(label = "Coa Rak Pusat",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)    
    class Meta:
        model = RakPusatMapper

class BiayaPusatMapperForm(forms.ModelForm):
    item = forms.ChoiceField( widget = forms.Select(), choices = ITEM_JURNAL)
    cabang = chosenforms.ChosenModelChoiceField(label = "Gerai",queryset=Tbl_Cabang.objects.all(),required = False)
    cabang_tuju = chosenforms.ChosenModelChoiceField(label = "Gerai Tuju",queryset=Tbl_Cabang.objects.all(),required = False)
    coa_debet = chosenforms.ChosenModelChoiceField(label = "Coa Debet",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa = chosenforms.ChosenModelChoiceField(label = "Coa Kredit",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_uk = chosenforms.ChosenModelChoiceField(label = "Coa Uangmuka",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_debet_tuju = chosenforms.ChosenModelChoiceField(label = "Coa Debet Tuju",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_kredit_tuju = chosenforms.ChosenModelChoiceField(label = "Coa Kredit Tuju",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    class Meta:
        model = BiayaPusatMapper

class MateraiPusatForm(ModelForm):
    coa1 = chosenforms.ChosenModelChoiceField(label ="Kas Gerai",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa2= chosenforms.ChosenModelChoiceField(label ="Persediaan Materai",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)    
    coa_cabang_debet = chosenforms.ChosenModelChoiceField(queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_cabang_kredit= chosenforms.ChosenModelChoiceField(queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    class Meta:
        model = MateraiPusatMapper

class MateraiForm(ModelForm):
    coa1 = chosenforms.ChosenModelChoiceField(label ="Kas Gerai",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa2= chosenforms.ChosenModelChoiceField(label ="Persediaan Materai",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa3 = chosenforms.ChosenModelChoiceField(label ="Biaya Materai",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa4 = chosenforms.ChosenModelChoiceField(label ="Uang Muka",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    class Meta:
        model = MateraiMapper

class UangMukaForm(ModelForm):
    debet_pengembalian_uk = chosenforms.ChosenModelChoiceField(queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    kredit_pengembalian_uk = chosenforms.ChosenModelChoiceField(queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    debet_pengambilan_uk = chosenforms.ChosenModelChoiceField(queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    kredit_pengambilan_uk = chosenforms.ChosenModelChoiceField(queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)

    class Meta:
        model = UangMukaGeraiMapper

class AkunForm(ModelForm):  
    header_parent=chosenforms.ChosenModelChoiceField(label = "Header Parent",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    tanggal = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12}, format="%d-%m-%Y"))
    class Meta:
        model = Tbl_Akun
        widgets = {
            'saldo_mf' : forms.HiddenInput(),
            'saldo_pjb' : forms.HiddenInput(),
            'saldo_krs' : forms.HiddenInput(),
            'saldo_akhir_pjb' : forms.HiddenInput(),
        }


class KasirPelunasanMapperForm(forms.ModelForm):
    item = forms.ChoiceField( widget = forms.Select(), choices = PELUNASAN_KASIR)
    jenis = forms.ChoiceField( widget = forms.Select(), choices = JENIS_TRANS)
    cabang = chosenforms.ChosenModelChoiceField(label = "Cabang",queryset=Tbl_Cabang.objects.all(),required = False)    
    ke_cabang = chosenforms.ChosenModelChoiceField(label = "Ke Cabang",queryset=Tbl_Cabang.objects.all(),required = False)    
    coa_1 = chosenforms.ChosenModelChoiceField(label = "Titipan Pelunasan",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_2 = chosenforms.ChosenModelChoiceField(label = "Bank / Kas",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_3 = chosenforms.ChosenModelChoiceField(label = "Pendapatan Lainnya",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_4 = chosenforms.ChosenModelChoiceField(label = "Beban Lainnya",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_5 = chosenforms.ChosenModelChoiceField(label = "Titipan Kelebihan",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    #debet_rak_cabang = chosenforms.ChosenModelChoiceField(label = "RAK Cabang",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    #kredit_rak_pusat = chosenforms.ChosenModelChoiceField(label = "RAK Pusat",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    #tanggal = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12}, format="%d-%m-%Y"))
    class Meta:
        model = KasirPelunasanMapper

class AdmPelunasanForm(ModelForm):
    item = forms.ChoiceField( widget = forms.Select(), choices = PELUNASAN_ADM)
    coa_1 = chosenforms.ChosenModelChoiceField(label = "Titipan Pelunasan",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False) 
    coa_2 = chosenforms.ChosenModelChoiceField(label = "Pinjaman Anggota/None Anggota",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False) 
    coa_3 = chosenforms.ChosenModelChoiceField(label = "Denda",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_4 = chosenforms.ChosenModelChoiceField(label = "Pendapatan Jasa",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_5 = chosenforms.ChosenModelChoiceField(label = "PPAP",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_6 = chosenforms.ChosenModelChoiceField(label = "Pend Ops Lainnya",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_7 = chosenforms.ChosenModelChoiceField(label = "Beban Ops Lainnya",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)  
    class Meta:
        model = AdmPelunasanMapper

class AdmPencairanForm(ModelForm):  
    item = forms.ChoiceField( widget = forms.Select(), choices = ITEM_ADM_JURNAL)  
    tanggal = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12}, format="%d-%m-%Y"))
    cabang = chosenforms.ChosenModelChoiceField(required = False,queryset=Tbl_Cabang.objects.all(),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}))
    coa1 = chosenforms.ChosenModelChoiceField(label = "Titipan Pencairan",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa2 = chosenforms.ChosenModelChoiceField(label = "Pinjaman Non Anggota/Anggota",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa3 = chosenforms.ChosenModelChoiceField(label = "Adm",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa4 = chosenforms.ChosenModelChoiceField(label = "Jasa",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)    
    coa5 = chosenforms.ChosenModelChoiceField(label = "Bea Simpan",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)    
    coa6 = chosenforms.ChosenModelChoiceField(label = "Materai",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)            
    class Meta:
        model = PencairanAdmMapper

class AdmGadaiUlangForm(forms.ModelForm):
    item = forms.ChoiceField( widget = forms.Select(), choices = AKADBARANGSAMA_ADM)
    coa = chosenforms.ChosenModelChoiceField(label = "Non Anggota/Anggota",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_1 = chosenforms.ChosenModelChoiceField(label = "Titipan Pencairan",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_2 = chosenforms.ChosenModelChoiceField(label = "Jasa",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_3 = chosenforms.ChosenModelChoiceField(label = "Adm",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_4 = chosenforms.ChosenModelChoiceField(label = "Bea simpan",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_5 = chosenforms.ChosenModelChoiceField(label = "Titipan Pelunasan",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_6 = chosenforms.ChosenModelChoiceField(label = "Denda",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_7 = chosenforms.ChosenModelChoiceField(label = "Materai",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    class Meta:
        model = AdmGadaiUlangMapper


class GeraiPenjualanMapperForm(forms.ModelForm):
    cabang = chosenforms.ChosenModelChoiceField(label = "Cabang",queryset=Tbl_Cabang.objects.all(),required = False)    
    coa1 = chosenforms.ChosenModelChoiceField(label = "Coa Satu",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa2 = chosenforms.ChosenModelChoiceField(label = "Coa Dua",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa3 = chosenforms.ChosenModelChoiceField(label = "Coa Tiga",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    class Meta:
        model = GeraiPenjualanMapper

class PnkbMapperForm(forms.ModelForm):
    cabang = chosenforms.ChosenModelChoiceField(label = "Cabang",queryset=Tbl_Cabang.objects.all(),required = False)
    ke_cabang = chosenforms.ChosenModelChoiceField(label = "Ke Cabang",queryset=Tbl_Cabang.objects.all(),required = False)
    coa = chosenforms.ChosenModelChoiceField(label = "Coa Debet",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_kredit = chosenforms.ChosenModelChoiceField(label = "Coa Kredit",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_lawan = chosenforms.ChosenModelChoiceField(label = "Coa Debet Lawan",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_kredit_lawan = chosenforms.ChosenModelChoiceField(label = "Coa Kredit Lawan",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    debet_rak_cabang = chosenforms.ChosenModelChoiceField(label = "Debet Rak Cabang",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    kredit_rak_pusat = chosenforms.ChosenModelChoiceField(label = "Kredit Rak Cabang",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    class Meta:
        model = PenKasBankMapper


class PusatKasBankMapperForm(forms.ModelForm):
    cabang = chosenforms.ChosenModelChoiceField(label = "Gerai",queryset=Tbl_Cabang.objects.all(),required = False)
    coa = chosenforms.ChosenModelChoiceField(label = "Coa Debet",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_kredit = chosenforms.ChosenModelChoiceField(label = "Coa Kredit",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_lawan_debet = chosenforms.ChosenModelChoiceField(label = "Coa Lawan Debet",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_lawan_kredit = chosenforms.ChosenModelChoiceField(label = "Coa Lawan Kredit",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    debet_rak_cabang = chosenforms.ChosenModelChoiceField(label = "Debet Rak Cabang",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    kredit_rak_pusat = chosenforms.ChosenModelChoiceField(label = "Kredit Rak Cabang",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    class Meta:
        model = PusatKasBankMapper

class MateraiMapperForm(forms.ModelForm):
    item = forms.ChoiceField( widget = forms.Select(), choices = ITEM_JURNAL)
    cabang = chosenforms.ChosenModelChoiceField(label = "Gerai",queryset=Tbl_Cabang.objects.all(),required = False)
    coa1 = chosenforms.ChosenModelChoiceField(label = "Kode Account1",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa2 = chosenforms.ChosenModelChoiceField(label = "Kode Account2",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa3 = chosenforms.ChosenModelChoiceField(label = "Kode Account3",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa4 = chosenforms.ChosenModelChoiceField(label = "Kode Account4",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    class Meta:
        model = MateraiMapper

class BiayaMapperForm(forms.ModelForm):
    item = forms.ChoiceField( widget = forms.Select(), choices = ITEM_JURNAL)
    cabang = chosenforms.ChosenModelChoiceField(label = "Gerai",queryset=Tbl_Cabang.objects.all(),required = False)
    coa = chosenforms.ChosenModelChoiceField(label = "Coa Kredit",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_debet = chosenforms.ChosenModelChoiceField(label = "Coa Debet",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_uk = chosenforms.ChosenModelChoiceField(label = "Coa Uangmuka",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    class Meta:
        model = BiayaMapper

class PenKasBankMapperForm(forms.ModelForm):
    item = forms.ChoiceField( widget = forms.Select(), choices = PENAMBAHAN_JURNAL)
    jenis = forms.ChoiceField( widget = forms.Select(), choices = JENIS_PENAMBAHAN)
    cabang = chosenforms.ChosenModelChoiceField(label = "Gerai",queryset=Tbl_Cabang.objects.all(),required = False)
    ke_cabang = chosenforms.ChosenModelChoiceField(label = "Gerai Dituju",queryset=Tbl_Cabang.objects.all(),required = False)
    coa = chosenforms.ChosenModelChoiceField(label = "Kode Account Debet",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_kredit = chosenforms.ChosenModelChoiceField(label = "Kode Account Kredit ",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    debet_rak_cabang = chosenforms.ChosenModelChoiceField(label = "Debet Rak Cabang",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    kredit_rak_pusat = chosenforms.ChosenModelChoiceField(label = "Kredit Rak Cabang",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    class Meta:
        model = BiayaMapper
        fields =  ['item','jenis','coa','coa_kredit','cabang','ke_cabang']

class GadaiUlangForm(ModelForm):    
    tanggal = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12}, format="%d-%m-%Y"))
    cabang = chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}))
    coa_titipan_pelunasan = chosenforms.ChosenModelChoiceField(label='Coa Titipan',queryset=Tbl_Akun.objects.all(),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}))
    coa_kas = chosenforms.ChosenModelChoiceField(label='Coa Kas/ Bank',queryset=Tbl_Akun.objects.all(),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}),required = False)
    coa_pendapatan_lainnya = chosenforms.ChosenModelChoiceField(label='Coa Pendapatan',queryset=Tbl_Akun.objects.all(),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}),required = False)
    coa_beban = chosenforms.ChosenModelChoiceField(label='Coa Beban',queryset=Tbl_Akun.objects.all(),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}),required = False)
    coa_titipan_kelebihan = chosenforms.ChosenModelChoiceField(label='Coa Titipan Kelebihan',queryset=Tbl_Akun.objects.all(),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}),required = False)
    class Meta:
        model = GadaiUlangMapper

class KasirPencairanForm(ModelForm):    
    tanggal = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12}, format="%d-%m-%Y"))
    cabang = chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}))
    coa_debet = chosenforms.ChosenModelChoiceField(label='Coa Debet',queryset=Tbl_Akun.objects.all(),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}),required = False)
    coa_debet_satu = chosenforms.ChosenModelChoiceField(label='Coa Debet Beban',queryset=Tbl_Akun.objects.all(),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}),required = False)
    coa_kredit = chosenforms.ChosenModelChoiceField(label='Coa Kredit',queryset=Tbl_Akun.objects.all(),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}),required = False)
    coa_kredit_satu = chosenforms.ChosenModelChoiceField(label='Coa Kredit',queryset=Tbl_Akun.objects.all(),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}),required = False)
    
    class Meta:
        model = KasirPencairanMapper

class KasirPencairanBankForm(ModelForm):
    tanggal = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12}, format="%d-%m-%Y"))
    cabang = chosenforms.ChosenModelChoiceField(queryset=Tbl_Cabang.objects.all(),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}))
    coa_debet = chosenforms.ChosenModelChoiceField(label='Coa Debet',queryset=Tbl_Akun.objects.all(),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}),required = False)
    coa_debet_satu = chosenforms.ChosenModelChoiceField(label='Coa Debet Beban',queryset=Tbl_Akun.objects.all(),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}),required = False)
    coa_kredit = chosenforms.ChosenModelChoiceField(label='Coa Kredit',queryset=Tbl_Akun.objects.all(),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}),required = False)
    coa_kredit_satu = chosenforms.ChosenModelChoiceField(label='Coa Kredit',queryset=Tbl_Akun.objects.all(),\
        widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}),required = False)

    class Meta:
        model = KasirPencairanBankMapper
