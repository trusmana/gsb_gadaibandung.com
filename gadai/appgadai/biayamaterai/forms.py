from django import forms
from django.forms import ModelForm
from gadai.appgadai.models import *
from chosen import forms as chosenforms
from django.utils.safestring import mark_safe



class HorizRadioRenderer(forms.RadioSelect.renderer):
	def render(self):
		return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class Biaya_MateraiForm(ModelForm):
    gerai = forms.ModelChoiceField(queryset=Tbl_Cabang.objects.all())
    tanggal = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'readonly':'true'}, format="%d-%m-%Y"))
    nilai = forms.IntegerField(widget=forms.TextInput(attrs={'alt': 'integer', 'class': 'uang','value':0,'size':10,}))
    #keterangan = forms.CharField( widget=forms.TextInput(attrs={'size':25,'placeholder':'Keterangan'}),required = False)
    antar_gerai = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=GERAI_PILIH,required = False)

    class Meta:
        model = Biaya_Materai
        widgets = {
            'saldo_awal' : forms.HiddenInput(),
            'saldo_akhir' : forms.HiddenInput(),
            'keterangan' : forms.HiddenInput(),
        }

