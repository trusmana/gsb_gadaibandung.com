from django import forms
from gadai.appgadai.models import *
from chosen import forms as chosenforms

class MateraiMapperForm(forms.ModelForm):
    item = forms.ChoiceField( widget = forms.Select(), choices = ITEM_JURNAL)
    cabang = chosenforms.ChosenModelChoiceField(label = "Gerai",queryset=Tbl_Cabang.objects.all(),required = False)
    coa1 = chosenforms.ChosenModelChoiceField(label = "Kode Account1",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa2 = chosenforms.ChosenModelChoiceField(label = "Kode Account2",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa3 = chosenforms.ChosenModelChoiceField(label = "Kode Account3",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa4 = chosenforms.ChosenModelChoiceField(label = "Kode Account4",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)


    class Meta:
        model = MateraiMapper



class BiayaMapperForm(forms.ModelForm):
    item = forms.ChoiceField( widget = forms.Select(), choices = ITEM_JURNAL)
    cabang = chosenforms.ChosenModelChoiceField(label = "Gerai",queryset=Tbl_Cabang.objects.all(),required = False)
    coa = chosenforms.ChosenModelChoiceField(label = "Kode Account",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
 
    
    class Meta:
        model = BiayaMapper

class PenKasBankMapperForm(forms.ModelForm):
    item = forms.ChoiceField( widget = forms.Select(), choices = ITEM_JURNAL)
    jenis = forms.ChoiceField( widget = forms.Select(), choices = JENIS_PENAMBAHAN)
    cabang = chosenforms.ChosenModelChoiceField(label = "Gerai",queryset=Tbl_Cabang.objects.all(),required = False)
    ke_cabang = chosenforms.ChosenModelChoiceField(label = "Gerai Dituju",queryset=Tbl_Cabang.objects.all(),required = False)
    coa = chosenforms.ChosenModelChoiceField(label = "Kode Account Debet",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)
    coa_kredit = chosenforms.ChosenModelChoiceField(label = "Kode Account Kredit ",queryset=Tbl_Akun.objects.all().order_by('coa'),required = False)

    class Meta:
        model = BiayaMapper
        fields =  ['item','jenis','coa','coa_kredit','cabang','ke_cabang']
