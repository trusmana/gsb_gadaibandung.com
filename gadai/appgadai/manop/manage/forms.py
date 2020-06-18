from django import forms
from gadai.appkeuangan.models import  MenuItem


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ('id', 'order', 'link_url' )
