from django import forms
from django.forms import ModelForm
from gadai.appgadai.models import CHOICES_BARANG, CHOICES_KONDISI_BARANG

class HorizRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class DataLapurnaForm(forms.Form):
    charger = forms.ChoiceField(widget =forms.Select(attrs={'class':'radio inline'}), choices=CHOICES_BARANG, initial='2',required=False)
    kondisi_charger = forms.ChoiceField(widget =forms.RadioSelect(attrs={'class':'radio inline'}),
        choices=CHOICES_KONDISI_BARANG,initial='5',required=False)
    batre = forms.ChoiceField(widget =forms.Select(attrs={'class':'radio inline '}), choices=CHOICES_BARANG, initial='2',required=False)
    kondisi_batre = forms.ChoiceField(widget =forms.RadioSelect(attrs={'class':'radio inline'}),
        choices=CHOICES_KONDISI_BARANG,initial='5',required=False)
    keybord = forms.ChoiceField(widget =forms.Select(attrs={'class':'radio inline'}), choices=CHOICES_BARANG, initial='2',required=False)
    kondisi_keybord = forms.ChoiceField(widget =forms.RadioSelect(attrs={'class':'radio inline'}),
        choices=CHOICES_KONDISI_BARANG,initial='5',required=False)
    cassing = forms.ChoiceField(widget =forms.Select(attrs={'class':'radio inline'}), choices=CHOICES_BARANG, initial='2',required=False)
    kondisi_cassing = forms.ChoiceField(widget =forms.RadioSelect(attrs={'class':'radio inline'}),
        choices=CHOICES_KONDISI_BARANG,initial='5',required=False)

    layar = forms.ChoiceField(widget =forms.Select(attrs={'class':'radio inline '}), choices=CHOICES_BARANG, initial='2',required=False)
    kondisi_layar = forms.ChoiceField(widget =forms.RadioSelect(attrs={'class':'radio inline'}),
        choices=CHOICES_KONDISI_BARANG,initial='5',required=False)
    lensa = forms.ChoiceField(widget =forms.Select(attrs={'class':' radio inline'}), choices=CHOICES_BARANG, initial='2',required=False)
    kondisi_lensa = forms.ChoiceField(widget =forms.RadioSelect(attrs={'class':' radio inline'}),
        choices=CHOICES_KONDISI_BARANG,initial='5',required=False)
    batre_kamera = forms.ChoiceField(widget =forms.Select(attrs={'class':' radio inline'}), choices=CHOICES_BARANG,
            initial='2',required=False)
    kondisi_batre_kamera = forms.ChoiceField(widget =forms.RadioSelect(attrs={'class':' radio inline'}),
        choices=CHOICES_KONDISI_BARANG,initial='5',required=False)
    cassing_kamera = forms.ChoiceField(widget =forms.Select(attrs={'class':' radio inline'}), choices=CHOICES_BARANG, initial='2',required=False)
    kondisi_cassing_kamera = forms.ChoiceField(widget =forms.RadioSelect(attrs={'class':' radio inline'}),required=False,
        choices=CHOICES_KONDISI_BARANG,initial='5')

    harddisk  = forms.ChoiceField(widget =forms.Select(attrs={'class':'radio inline formps'}), choices=CHOICES_BARANG,
            initial='2',required=False)
    kondisi_harddisk = forms.ChoiceField(widget =forms.RadioSelect(attrs={'class':'radio inline'}),required=False,
        choices=CHOICES_KONDISI_BARANG,initial='5')
    stick  = forms.ChoiceField(widget =forms.Select(attrs={'class':'radio inline formps'}), choices=CHOICES_BARANG, initial='2',required=False)
    kondisi_stick = forms.ChoiceField(widget =forms.RadioSelect(attrs={'class':'radio inline'}),required=False,
        choices=CHOICES_KONDISI_BARANG,initial='5')
    hdmi  = forms.ChoiceField(widget =forms.Select(attrs={'class':'radio inline formps'}), choices=CHOICES_BARANG, initial='2',required=False)
    kondisi_hdmi = forms.ChoiceField(widget =forms.RadioSelect(attrs={'class':'radio inline'}),required=False,
        choices=CHOICES_KONDISI_BARANG,initial='5')

    layar_tv = forms.ChoiceField(widget =forms.Select(attrs={'class':'radio inline formtv'}), choices=CHOICES_BARANG,
            initial='2',required=False)
    kondisi_layar_tv = forms.ChoiceField(widget =forms.RadioSelect(attrs={'class':'radio inline'}),required=False,
        choices=CHOICES_KONDISI_BARANG,initial='5')
    remote = forms.ChoiceField(widget =forms.Select(attrs={'class':'radio inline formtv'}), choices=CHOICES_BARANG,
            initial='2',required=False)
    kondisi_remote = forms.ChoiceField(widget =forms.RadioSelect(attrs={'class':'radio inline'}),required=False,
        choices=CHOICES_KONDISI_BARANG,initial='5')
    keterangan = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Isi Keterangan'}))



