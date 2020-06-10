from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gadai.appgadai.models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
import xlwt
import io
import xlsxwriter
from gadai.xlsxwriter.workbook import Workbook
from gadai.appgadai.admgudang.forms import *
from gadai.appgadai.permintaan.forms import *

def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['manop','baranglapur','admops','abh'])

#@login_required
#@user_passes_test(lambda u: u.groups.filter(name='gudang'))
def verifikasi_datagudang(request, object_id):
    ag = AkadGadai.objects.get(id=object_id)
    a = datetime.date.today()
    form = AdmGudangForm(initial={'adm': ag.id,'tanggal': a})
    form.fields['adm'].widget = forms.HiddenInput()
    template = 'admgudang/verifikasi_datagudang.html'
    variable = RequestContext(request, {
        'ag': ag,
        'form': form})
    return render_to_response(template,variable) 
    
#@login_required
#@user_passes_test(lambda u: u.groups.filter(name='gudang'))
def verifikasi_dataretur(request, object_id):
    ag = AkadGadai.objects.get(id=object_id)
    barang = Barang.objects.get(id =ag.barang.id)
    if request.method == 'POST':
        f = AdmGudangForm(request.POST)
        if f.is_valid():
            adm = f.cleaned_data['adm']   
            tanggal = f.cleaned_data['tanggal']
            status = f.cleaned_data['status']
            note = f.cleaned_data['note']
            f = AdmGudang(adm=ag, tanggal=tanggal, status=status, note = note)
            f.save()
            h_barang = HistoryBarang(agbarang= ag.barang,tgl_barang_masuk =ag.barang.barang_masuk,tgl_barang_keluar =ag.barang.barang_keluar ,\
                    ruang_barang = ag.barang.ruangan,lemari_barang = ag.barang.lemari,row_barang = ag.barang.row,rak_barang = ag.barang.no_rak)
            h_barang.save()
            if f.status == '1':
                ag.tanggal_pengiriman = None
                ag.status_permintaan = None
                ag.tanggal_permintaan = None
                ag.save()
                barang.barang_masuk = f.tanggal
                barang.barang_keluar = None
                barang.ruangan = None
                barang.no_rak = None
                barang.row = None
                barang.lemari = None
                barang.save()
                messages.add_message(request, messages.INFO,'### BARANG ADA DI GUDANG ###')    
            else: 
                ag.tanggal_pengiriman = f.tanggal
                ag.status_permintaan = 3
                ag.save()    
                messages.add_message(request, messages.INFO,'### BARANG MASIH DI GERAI ###')            
            return HttpResponseRedirect(ag.get_absolute_url_adm())
    else:
        f = AdmGudangForm()
    variables = RequestContext(request, {'ag': ag, 'form': f})
    return render_to_response('admgudang/verifikasi_datagudang.html', variables)

def data_retur_gaktif(request):
    kp = []
    blm =[]
    form = FilterPermintaanForm()
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET:
        end_date = request.GET['end_date']
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '1' :
            gerai = AkadGadai.objects.filter(tanggal_permintaan__range=(start_date,end_date)).filter(status_permintaan=('2')).order_by('gerai')
            for k in gerai:
                kp.append(k)                
            start_date = start_date
            end_date = end_date
            
            template = 'admgudang/data_retur_gaktif.html'
            variables = RequestContext(request, {'kp':kp,'end_date':end_date,'form': form})        
            return render_to_response(template, variables)
        else:
            gerai = AkadGadai.objects.filter(tanggal_permintaan__range=(start_date,end_date)).filter(gerai__id= id_cabang).filter(status_permintaan=('2')).order_by('gerai')
            for k in gerai:
                kp.append(k)                
            start_date = start_date
            end_date = end_date
            
            template = 'admgudang/data_retur_gaktif.html'
            variables = RequestContext(request, {'kp':kp,'end_date':end_date,'form': form})        
            return render_to_response(template, variables)
    else:
        template = 'admgudang/data_retur_gaktif.html'
        variables = RequestContext(request, {'kp': kp,'form':form})
        return render_to_response(template, variables)
