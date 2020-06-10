from django import forms
from gadai.appgadai.models import Barang,Nasabah
from gadai.appgadai.widgets import MultipleSelectWithPop
from django.utils.safestring import mark_safe
from gadai.appgadai.models import Barang,CHOICES_JENIS_TRANSAKSI,JENIS_BARANG,JENIS_DOKUMEN,JENIS_KENDARAAN,MERK_KENDARAAN_CHOICES,TAHUN_KENDARAAN_CHOICES,CHOICES_BARANG,CHOICES_KONDISI_BARANG

class BarangForm(forms.ModelForm):    
    class Meta:
        model = Barang
        fields = ('barang_masuk', 'barang_keluar', 'ruangan','lemari', 'no_rak', 'row')
class HorizRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class Edit_BarangForm(forms.ModelForm):
    jenis_kendaraan = forms.ChoiceField(widget=forms.Select(), choices=JENIS_KENDARAAN)
    merk_kendaraan = forms.ChoiceField(widget=forms.Select(), choices=MERK_KENDARAAN_CHOICES)
    jenis_barang = forms.ChoiceField(widget = forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'barang'}), choices = JENIS_BARANG,initial ='0',required=False)
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
    
    bpkb = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    stnk = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    faktur = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    gesek_nomesin = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    gesek_norangka = forms.ChoiceField(widget =forms.Select(), choices=CHOICES_BARANG, initial='2')
    
    layar_tv = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formtv'}), choices=CHOICES_BARANG, initial='2')
    kondisi_layar_tv = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formbarang formtv'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    remote = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang formtv'}), choices=CHOICES_BARANG, initial='2')
    kondisi_remote = forms.ChoiceField(widget =forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'formbarang formtv'}), choices=CHOICES_KONDISI_BARANG,initial='5')
    dus = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang'}), choices=CHOICES_BARANG, initial='2')
    tas = forms.ChoiceField(widget =forms.Select(attrs={'class':'formbarang'}), choices=CHOICES_BARANG, initial='2')
    barang_masuk = forms.DateField(widget=forms.widgets.DateInput(attrs={'size': 12,'readonly':'True'}, format="%d-%m-%Y"))
    #barang_keluar = forms.DateField(widget=forms.widgets.DateInput(attrs={'size': 12,'readonly':'True'}, format="%d-%m-%Y"))
    class Meta:
        model = Barang
        widgets = {
            #'barang_masuk' : forms.HiddenInput(),
            'barang_keluar' : forms.HiddenInput(),
            'ruangan' : forms.HiddenInput(),
            'no_rak' : forms.HiddenInput(),
            'row' : forms.HiddenInput(),
            'lemari' : forms.HiddenInput(),
            'kolom' : forms.HiddenInput(),}
