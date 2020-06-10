from django import forms
from django.contrib.auth.models import Group

from gadai.appgadai.models import Tbl_Cabang

groups = ['ADM_GERAI','pusat']
rsgroup = Group.objects.filter(name__in=groups)
class UserForm(forms.Form):
    username = forms.CharField()
    firstname = forms.CharField()
    lastname = forms.CharField(required=False )
    email = forms.EmailField(required=False)
    rekening = forms.CharField(help_text="Nomor rekening bank", required=False)
    #gerai = forms.ChoiceField(choices=[('', '-----')]+[(k.id, k.nama_cabang) for k in Tbl_Cabang.objects.all() if k.is_gerai()], required=False)
    gerai = forms.ChoiceField(choices=[('', '-----')]+[(k.id, k.nama_cabang) for k in Tbl_Cabang.objects.all()], required=False)
    group = forms.ModelChoiceField(queryset=rsgroup)
