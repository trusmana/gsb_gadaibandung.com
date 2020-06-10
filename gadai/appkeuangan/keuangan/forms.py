from django import forms
from django.forms.formsets import formset_factory
from chosen import forms as chosenforms
from gadai.appgadai.models import *
from django.utils.safestring import mark_safe
from django.forms import fields, models, formsets, widgets
from django.contrib.admin.widgets import AdminDateWidget
from django.conf import settings

GERAI_PILIH =(
    ('','-------'),('300','BANDUNG'),('301','JAKARTA'),('302','SUCI'),('303','DIPATIUKUR'),('304','BALUBUR'),
    ('306','GERLONG HILIR'),('307','KOPO'),('308','CIBIRU'),('309','CIPACING'),('310','JATINANGOR'),
    ('311','CIMAHI'),('312','BUAH BATU'),('314','CIHANJUANG'),('315','MARANATA'),('316','KIARACONDONG'),
    ('317','CIREBON'),('319','CIUMBULEUIT'),('320','UJUNGBERUNG'),('321','CIWASTRA'),('322','BOJONGSOANG'),
)


GERAI_PILIH_NEW =(
    ('','-------'),('0','BANDUNG'),('1','JAKARTA'),('2','SUCI'),('3','DIPATIUKUR'),('BALUBUR','BALUBUR'),
    ('GERLONG_HILIR','GERLONG HILIR'),('KOPO','KOPO'),('CIBIRU','CIBIRU'),('CIPACING','CIPACING'),('JATINANGOR','JATINANGOR'),
    ('CIMAHI','CIMAHI'),('BUAH_BATU','BUAH BATU'),('CIHANJUANG','CIHANJUANG'),('MARANATA','MARANATA'),('KIARACONDONG','KIARACONDONG'),
    ('CIREBON','CIREBON'),('CIUMBULEUIT','CIUMBULEUIT'),('UJUNGBERUNG','UJUNGBERUNG'),
)

class PostingAkhirTahunForm(forms.Form):
    tanggal = forms.DateField(label ='Tanggal Perubahan Saldo',widget=forms.widgets.DateInput(attrs={'size': 12}, format="%d-%m-%Y"))
    saldo_shu = forms.FloatField(widget=forms.TextInput(attrs={'size': 20, 'class': 'rp_debet uang', 'value': '0', 'alt': 'integer'}),required = False)

class RevisiPostingForm(forms.Form):
    gerai = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=DATACABANG,initial='0',required=False)
    tgl_trans = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12}, format="%d-%m-%Y"))

class Jurnal_HistoryForm(models.ModelForm):
    class Meta:
        model = Jurnal_History

class Tbl_Transaksi_HistoryForm(models.ModelForm):
    deskripsi = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'size': 50}))
    koderekening = forms.CharField(max_length=60, 
            widget=forms.TextInput(attrs={'class': 'kode_rekening'}),
            required = False)
    debet = forms.FloatField(widget=forms.TextInput(attrs={'size': 9, 'class': 'rp_debet uang', 'value': '0', 'alt': 'integer'}),required = False)
    kredit = forms.FloatField(widget=forms.TextInput(attrs={'size': 9, 'class': 'rp_kredit uang', 'value': '0', 'alt': 'integer'}),required = False)
    class Meta:
        model = Tbl_Transaksi_History
        fields=('id_coa', 'kredit', 'debet','deskripsi')
        
def get_ordereditem_formset(form, formset=models.BaseInlineFormSet, **kwargs):
    return models.inlineformset_factory(Jurnal_History, Tbl_Transaksi_History, form, formset, **kwargs)


class JurnalForm(models.ModelForm):
    class Meta:
        model = Jurnal

class Tbl_TransaksiForm(models.ModelForm):
    debet = forms.FloatField(widget=forms.TextInput(attrs={'size': 9, 'class': 'rp_debet uang', 'value': '0', 'alt': 'integer'}),required = False)
    kredit = forms.FloatField(widget=forms.TextInput(attrs={'size': 9, 'class': 'rp_kredit uang', 'value': '0', 'alt': 'integer'}),required = False)
    class Meta:
        model = Tbl_Transaksi
        fields=('id_coa', 'kredit', 'debet')
        
        #widgets = {
            #"id_coa": chosenwidgets.ChosenModelChoiceField(queryset=Tbl_Akun.objects.all())}
        #fields = '__all__'



class HorizRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
            """Outputs radios"""
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class MainJurnalForm(forms.Form):
    #nobukti = forms.CharField(label = "Nomor Bukti",max_length=12)
    gerai = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=GERAI_PILIH,required = False,initial='BANDUNG')
    tgl_trans = forms.DateTimeField(label = "Tanggal",initial = datetime.date.today)
    diskripsi = forms.CharField(label = "Keterangan",max_length=200, required=False, widget=forms.TextInput(attrs={'size': 50}))
    j_status = forms.ChoiceField(label ="Status",widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=J_STATUS,initial = '0')

class Tbl_AkunForm(forms.Form):
    id_coa = chosenforms.ChosenModelChoiceField(label = "Kode Account",queryset=Tbl_Akun.objects.all())
    id_cabang = chosenforms.ChosenChoiceField(widget=chosenforms.ChosenSelect({'class': 'id_cabang'})) 
    start_date = forms.DateTimeField(initial = datetime.date.today)

class Rugi_LabaForm(forms.Form):
    id_cabang = chosenforms.ChosenChoiceField(widget=chosenforms.ChosenSelect({'class': 'id_cabang'})) 

class KeuanganPusatForm(forms.ModelForm):
    tanggal = forms.DateField(label ='Tanggal Perubahan Saldo',initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12}, format="%d-%m-%Y"))
    #saldo = forms.FloatField(widget=forms.TextInput(attrs={'size': 9, 'class': 'rp_debet uang', 'alt': 'integer'}),required = False)
    tanggal_sbl = forms.DateField(label ='Tanggal Transaksi',widget=forms.widgets.DateInput(attrs={'size': 12}), required = False)
    class Meta:
        model = KeuanganPusat
        #widgets = {'keuangan_pusat'  : forms.HiddenInput(),}
        widgets = {'keuangan_pusat'  : forms.HiddenInput(),'saldo':forms.HiddenInput(),
            'kode_cabang':forms.HiddenInput(),'note':forms.HiddenInput()}

class Tbl_TransForm(forms.Form):
    tgl_trans = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12}, format="%d-%m-%Y"))
    diskripsi = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_DESKRIPSI,required = False) 
    #kode_cabang = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=GERAI_PILIH,required = False,initial='300')    
    kode_cabang = chosenforms.ChosenModelChoiceField(label = "Kode Cabang",queryset=Tbl_Cabang.objects.filter(status_aktif = 1),widget=chosenforms.ChosenMultipleChoiceField(),required = False,initial='300')

    id_coa = chosenforms.ChosenModelChoiceField(label = "COA",queryset=Tbl_Akun.objects.all(),widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}))
    jenis = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=JENIS_DESKRIPSI,required = False)
    debet = forms.IntegerField(label="Debet",initial = 0,widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','readonly':'True'}))
    kredit = forms.IntegerField(label="Kredit",initial = 0,widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','readonly':'True'}))
    id_unit = forms.IntegerField(label="ID Unit",initial = 300,widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','readonly':'True'}))
    id_product = forms.IntegerField(label="ID Product",initial = 0,widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','readonly':'True'}))    
    status_jurnal = forms.IntegerField(label="Status Jurnal",initial = 2,widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','readonly':'True'}))
    saldo = forms.IntegerField(label="SALDO",widget=forms.TextInput(attrs={'size':'16','alt': 'integer', 'class': 'uang'}))
    class Meta:
        widgets = {
            'nobukti' : forms.HiddenInput(),'no_akad' : forms.HiddenInput(),'object_id' : forms.HiddenInput(),
            'no_trans' : forms.HiddenInput(),'id_cabang' : forms.HiddenInput(),'id_cabang_tuju' : forms.HiddenInput(),
            'status_posting' : forms.HiddenInput(),'deskripsi': forms.HiddenInput(),
        }

class TbTransForm(forms.ModelForm):
    debet = forms.IntegerField(label="Debet",initial = 0,widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','readonly':'True'}))
    kredit = forms.IntegerField(label="Kredit",initial = 0,widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','readonly':'True'}))
    saldo = forms.IntegerField(label="SALDO",widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang'}))
    tgl_trans = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12}, format="%d-%m-%Y"))
    id_coa = chosenforms.ChosenModelChoiceField(label = "COA",queryset=Tbl_Akun.objects.all(),widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}))
    id_unit = forms.IntegerField(label="ID Unit",initial = 0,widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','readonly':'True'}))
    id_product = forms.IntegerField(label="ID Product",initial = 300,widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','readonly':'True'}))    
    status_jurnal = forms.IntegerField(label="Status Jurnal",initial = 2,widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','readonly':'True'}))
    jenis = forms.CharField(max_length=35,widget=forms.TextInput(attrs={'placeholder':'jenis','readonly':'True'}),initial ='SALDOKASGERAI')
    jurnal = chosenforms.ChosenModelChoiceField(queryset=JurnalKeuangan.objects.all(),widget=chosenforms.ChosenMultipleChoiceField({'class': 'kode_account'}))
    class Meta:
        model=Tbl_Transaksi
        widgets = {
            'deskripsi': forms.HiddenInput(),'id_cabang_tuju': forms.HiddenInput(),'status_posting': forms.HiddenInput(),'no_trans': forms.HiddenInput(),
        }
