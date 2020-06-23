from django import forms
from gadai.appkeuangan.models import  MenuItem
from django.contrib.auth.models import User,Group


class MenuItemForm(forms.ModelForm):
    user = forms.ModelMultipleChoiceField(queryset=User.objects.filter(groups__name__in =("ADM_GERAI","KASIR_GERAI")).\
        exclude(groups__name = "NON_AKTIF"))
    class Meta:
        model = MenuItem
        fields = ('id','order', 'judul','link_url','status_aktif','user','login_required' )



