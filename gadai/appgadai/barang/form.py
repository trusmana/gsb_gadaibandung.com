from django import forms
from gadai.appgadai.models import *

class NonLunasForm(forms.Form):
    start_date = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,}, format="%Y-%m-%d"))
    end_date = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,}, format="%Y-%m-%d"))

class BarangGudangForm(forms.ModelForm):
    tgl_barang_masuk = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'false'}, format="%d-%m-%Y")) 
    tgl_barang_keluar = forms.DateField(required=False,initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'false'}, format="%d-%m-%Y"))
    class Meta:
        model = HistoryBarang
        widgets = {
            'agbarang' : forms.HiddenInput()            
        }

class BarangForm(forms.ModelForm):
    #no_rak= forms.ChoiceField(widget=forms.Select(),choices=RAK_CHOICES)
    class Meta:
        model = Barang
        widgets = {
            'jenis_barang' : forms.HiddenInput(),'merk' : forms.HiddenInput(),'type' : forms.HiddenInput(),\
            'sn': forms.HiddenInput(),'warna': forms.HiddenInput(),\
            'tahun_pembuatan': forms.HiddenInput(),\
            'bulan_produksi':forms.HiddenInput(),'accesoris_barang1':forms.HiddenInput(),'lampiran_dokumen':forms.HiddenInput(),\
            'jenis_kendaraan':forms.HiddenInput(),'merk_kendaraan':forms.HiddenInput(),'type_kendaraan':forms.HiddenInput(),\
            'no_polisi':forms.HiddenInput(),'no_rangka':forms.HiddenInput(),'no_mesin':	forms.HiddenInput(),\
            'tahun_pembuatan_kendaraan':forms.HiddenInput(),'Warna kendaraan':forms.HiddenInput(),'no_bpkb':forms.HiddenInput(),\
            'stnk_atas_nama':forms.HiddenInput(),'no_faktur':forms.HiddenInput(),'fungsi_sistem':forms.HiddenInput(),\
            'charger':forms.HiddenInput(),'kondisi_charger':forms.HiddenInput(),'batre':forms.HiddenInput(),\
            'kondisi_batre':forms.HiddenInput(),'keybord':forms.HiddenInput(),'kondisi_keybord':forms.HiddenInput(),\
            'cassing':forms.HiddenInput(),'kondisi_cassing':forms.HiddenInput(),'layar':forms.HiddenInput(),\
            'kondisi_layar':forms.HiddenInput(),'password':forms.HiddenInput(),'password barang':forms.HiddenInput(),\
            'lensa':forms.HiddenInput(),'kondisi_lensa':forms.HiddenInput(),'batre_kamera':forms.HiddenInput(),\
            'kondisi_batre_kamera':forms.HiddenInput(),'cassing_kamera':forms.HiddenInput(),'kondisi_cassing_kamera':forms.HiddenInput(),\
            'optik_ps':forms.HiddenInput(),'kondisi_optik_ps':forms.HiddenInput(),'harddisk':forms.HiddenInput(),\
            'kondisi_harddisk':forms.HiddenInput(),'stick':forms.HiddenInput(),'kondisi_stick':forms.HiddenInput(),\
            'hdmi':forms.HiddenInput(),'kondisi_hdmi':forms.HiddenInput(),'layar_tv':forms.HiddenInput(),\
            'kondisi_layar_tv':forms.HiddenInput(),'remote':forms.HiddenInput(),'kondisi_remote':forms.HiddenInput(),\
            'bpkb':forms.HiddenInput(),'stnk':forms.HiddenInput(),'faktur':forms.HiddenInput(),\
            'gesek_norangka':forms.HiddenInput(),'dus':forms.HiddenInput(),'tas':forms.HiddenInput(),'akad_ulang':forms.HiddenInput(),\
            'kolom':forms.HiddenInput(),'warna_kendaraan':forms.HiddenInput(),'password_barang':forms.HiddenInput(),'gesek_nomesin':forms.HiddenInput(),
            }
