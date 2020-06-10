from django import forms
from django.forms.formsets import formset_factory
from chosen import forms as chosenforms
from gadai.appgadai.models import *
from django.utils.safestring import mark_safe
from django.forms import fields, models, formsets, widgets
from django.contrib.admin.widgets import AdminDateWidget
from django.conf import settings
from gadai.appkeuangan.models import DATACABANG_GLPUSAT

class HorizRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
            """Outputs radios"""
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))
GERAI_PILIH =(
    ('','-------'),('BANDUNG','BANDUNG'),('JAKARTA','JAKARTA'),('SUCI','SUCI'),('DIPATIUKUR','DIPATIUKUR'),('BALUBUR','BALUBUR'),
    ('GERLONG_HILIR','GERLONG HILIR'),('KOPO','KOPO'),('CIBIRU','CIBIRU'),('CIPACING','CIPACING'),('JATINANGOR','JATINANGOR'),
    ('CIMAHI','CIMAHI'),('BUAH_BATU','BUAH BATU'),('CIHANJUANG','CIHANJUANG'),('MARANATA','MARANATA'),('KIARACONDONG','KIARACONDONG'),
    ('CIREBON','CIREBON'),('CIUMBULEUIT','CIUMBULEUIT'),('UJUNGBERUNG','UJUNGBERUNG'),
)

GERAI_PILIH_NEW =(
    ('','-------'),('0','BANDUNG'),('1','JAKARTA'),('2','SUCI'),('3','DIPATIUKUR'),('BALUBUR','BALUBUR'),
    ('GERLONG_HILIR','GERLONG HILIR'),('KOPO','KOPO'),('CIBIRU','CIBIRU'),('CIPACING','CIPACING'),('JATINANGOR','JATINANGOR'),
    ('CIMAHI','CIMAHI'),('BUAH_BATU','BUAH BATU'),('CIHANJUANG','CIHANJUANG'),('MARANATA','MARANATA'),('KIARACONDONG','KIARACONDONG'),
    ('CIREBON','CIREBON'),('CIUMBULEUIT','CIUMBULEUIT'),('UJUNGBERUNG','UJUNGBERUNG'),
)

J_STATUS_KOREKSI =(
    ('3','KOREKSI'),
)

class MainJurnalKoreksiForm(forms.Form):
    tgl_trans = forms.DateField(label="Tanggal",initial=datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'true'}, format="%d-%m-%Y"))
    j_status = forms.ChoiceField(label ="Status",widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=J_STATUS_KOREKSI,initial = '3',required = False)

class Tbl_Transaksi_KoreksiForm(models.ModelForm):
    deskripsi = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'size': 30}))
    koderekening = forms.CharField(max_length=60, 
            widget=forms.TextInput(attrs={'class': 'kode_rekening','size':40}),
            required = False)
    id_cabang = forms.ChoiceField(widget=forms.Select(), choices=DATACABANG_GLPUSAT,required = False)
    debet = forms.FloatField(widget=forms.TextInput(attrs={'size': 9, 'class': 'rp_debet uang', 'value': '0', 'alt': 'integer'}),required = False)
    kredit = forms.FloatField(widget=forms.TextInput(attrs={'size': 9, 'class': 'rp_kredit uang', 'value': '0', 'alt': 'integer'}),required = False)
    class Meta:
        model = Tbl_Transaksi
        fields=('id_coa', 'kredit', 'debet','deskripsi')

class SearchForm(forms.Form):
    start_date = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,}, format="%Y-%m-%d"))
    end_date = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,}, format="%Y-%m-%d"))

class Tbl_Transaksi_History_glForm(models.ModelForm):
    deskripsi = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'size': 30}))
    koderekening = forms.CharField(max_length=60, 
            widget=forms.TextInput(attrs={'class': 'kode_rekening','size':40}),
            required = False)
    
    debet = forms.FloatField(widget=forms.TextInput(attrs={'size': 9, 'class': 'rp_debet uang', 'value': '0', 'alt': 'integer'}),required = False)
    kredit = forms.FloatField(widget=forms.TextInput(attrs={'size': 9, 'class': 'rp_kredit uang', 'value': '0', 'alt': 'integer'}),required = False)
    class Meta:
        model = Tbl_Transaksi_History
        fields=('id_coa', 'kredit', 'debet','deskripsi')

class MainJurnalglForm(forms.Form):
    tgl_trans = forms.DateField(initial=datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'true'}, format="%d-%m-%Y"))

class Jurnal_HistoryForm(models.ModelForm):
    class Meta:
        model = Jurnal_History

class Tbl_Transaksi_HistoryForm(models.ModelForm):
    deskripsi = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'size': 30}))
    koderekening = forms.CharField(max_length=60, 
            widget=forms.TextInput(attrs={'class': 'kode_rekening','size':40}),
            required = False)
    id_cabang = forms.ChoiceField(widget=forms.Select(), choices=DATACABANG_GLPUSAT,required = False)
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
    #gerai = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=DATACABANG,required = False)
    tgl_trans = forms.DateField(label="Tanggal",initial=datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'true'}, format="%d-%m-%Y"))
    #diskripsi = forms.CharField(label = "Keterangan",max_length=200, required=False, widget=forms.TextInput(attrs={'size': 50}))
    j_status = forms.ChoiceField(label ="Status",widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=J_STATUS,initial = '0',required = False)

class Tbl_AkunForm(forms.Form):
    id_coa = chosenforms.ChosenModelChoiceField(label = "Kode Account",queryset=Tbl_Akun.objects.all())
    id_cabang = chosenforms.ChosenChoiceField(widget=chosenforms.ChosenSelect({'class': 'id_cabang'})) 
    start_date = forms.DateTimeField(initial = datetime.date.today)

class Rugi_LabaForm(forms.Form):
    id_cabang = chosenforms.ChosenChoiceField(widget=chosenforms.ChosenSelect({'class': 'id_cabang'})) 


