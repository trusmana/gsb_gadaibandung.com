from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import date_based
from django.http import HttpResponseRedirect
from gadai.appgadai.biayamaterai.forms import Biaya_MateraiForm
from gadai.appgadai.models import *
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.shortcuts import render_to_response, get_object_or_404

def add(request,object_id):
    sekarang = datetime.date.today()
    bea = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=object_id).filter(status_jurnal = 1L).\
        filter(jenis=( u'PERSEDIAN_MATERAI'))
    if request.method == 'POST':
        f = Biaya_MateraiForm(request.POST)
        if f.is_valid():
            gerai = f.cleaned_data['gerai']
            nilai = f.cleaned_data['nilai']
            tanggal = f.cleaned_data['tanggal']
            antar_gerai = f.cleaned_data['antar_gerai']
            #keterangan = f.cleaned_data['keterangan']
            pusat =Biaya_Materai(gerai=gerai,tanggal=tanggal,nilai=nilai,antar_gerai=antar_gerai,keterangan='PENAMBAHAN_SALDO_MATERAI')
            pusat.save()
            materai_cab = Biaya_Materai_Cab(gerai_id=int(pusat.antar_gerai),nilai=pusat.nilai,tanggal=pusat.tanggal,keterangan='SALDO_AWAL')
            materai_cab.save()
            jurnal_materai(pusat, request.user)
            messages.add_message(request, messages.INFO,"INPUT BIAYA MATERAI BERHASIL - INPUT JURNAL BERHASIL")
            return HttpResponseRedirect('/biayamaterai/%s/add/' % (object_id))
        else:
            f = Biaya_MateraiForm()
            f.fields['gerai'].queryset = Tbl_Cabang.objects.filter(kode_cabang=object_id)
        variables = RequestContext(request, {'form': f,'bea':bea})
        return HttpResponseRedirect('/biayamaterai/%s/add/' % (object_id))
    else:
        f = Biaya_MateraiForm()
        f.fields['gerai'].queryset = Tbl_Cabang.objects.filter(kode_cabang=object_id)
        #f.fields['saldo_awal'].widget = f.HiddenInput()
    variables = RequestContext(request, { 'form': f,'bea':bea })
    return render_to_response('biayamaterai/addbiaya.html', variables)

def jurnal_materai(pusat, user):
    D = decimal.Decimal
    a_persedian_materai = get_object_or_404(Tbl_Akun, id=231L)
    a_kas_kecil = get_object_or_404(Tbl_Akun, id=8L)

    jurnal = Jurnal.objects.create(
        diskripsi= 'Persediaan Materai',tgl_trans = pusat.tanggal,cu = user, mu = user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("PERSEDIAN_MATERAI"), id_coa = a_persedian_materai,deskripsi= pusat.keterangan,
        kredit = 0,debet = D((pusat.nilai)),id_product = '4',status_jurnal ='1',tgl_trans =pusat.tanggal,
        id_cabang = pusat.gerai.kode_cabang,id_unit= 200)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("PERSEDIAN_MATERAI"), id_coa = a_kas_kecil,deskripsi= pusat.keterangan,
        debet = 0,kredit = D((pusat.nilai)),id_product = '4',status_jurnal ='1',tgl_trans =pusat.tanggal,
        id_cabang =pusat.gerai.kode_cabang,id_unit= 200)

