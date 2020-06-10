from django import forms
from django.forms import ModelForm
from gadai.appgadai.models import *
from gadai.appgadai.monthyearwidget import*

class Approve_MankeuForm(ModelForm):
    class Meta:
        model = ManopKeu

class LabaRugiMonthForm(forms.Form):    
    Bulan_Tahun = forms.DateField(required=False, widget=MonthYearWidget(years=xrange(2010,2050))
    )        