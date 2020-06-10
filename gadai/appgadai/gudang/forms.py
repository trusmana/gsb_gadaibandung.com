from gadai.appkeuangan.models import DATACABANG
from django.forms import ModelForm,Select
from django import forms
from django.forms import ModelForm
from gadai.appgadai.models import *
from django.core.exceptions import ValidationError
from chosen import forms as chosenforms
import datetime
from django.utils.safestring import mark_safe

JENIS_BARANG = (
	('500','GABUNGAN'),
	('1','HP'),('2','LAPTOP'),('3','KAMERA'),('4','PS'),
	('5','TV LCD'),('6','MOTOR'),('7','MOBIL'),
)

class HorizRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self ]))

class SearchGudangForm(forms.Form):
    start_date = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,}, format="%Y-%m-%d"))
    end_date = forms.DateField(initial = datetime.date.today,widget=forms.widgets.DateInput(attrs={'size': 12,}, format="%Y-%m-%d"))
    id_cabang = chosenforms.ChosenChoiceField(widget=forms.Select(), choices=DATACABANG,initial='0',required=False)
    id_barang = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer,attrs={'class':'id_pilih'}),choices = JENIS_BARANG)
