from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import create_update, list_detail
from django.template import RequestContext
from django.contrib.auth.models import User,Group
from django.shortcuts import render_to_response
from django import forms
from gadai.appgadai.models import *
import datetime
from django.utils.html import escape###MENU POP UP
from gadai.appgadai.permintaan.views import*
from django.contrib import messages
from gadai.appgadai.manop.forms import FilterForm
from gadai.appgadai.permintaan.forms import *

def reset_status_barang_gudang(request,object_id):
    ag = AkadGadai.objects.get(id=object_id)
    ag.tanggal_pengiriman =None
    ag.status_permintaan = 1
    ag.save()
    messages.add_message(request, messages.INFO,'Reset Status Berhasil.')
    return HttpResponseRedirect("/permintaan/input_permintaan_gudang/") 

def cabang_search(request):
    '''Fasilitas cari kode atau nama COA - ajaxed untuk saat entry jurnal'''
    query = request.GET.get('q', '')
    if query:
        qset = (Q(kode_cabang__icontains=query) or Q(nama_cabang__icontains=query))
        results = Tbl_Cabang.objects.filter(qset).distinct()
        if request.GET.has_key('jurnal'):
            results = [r for r in results if r.is_cabang() == True]
        if request.GET.has_key('ajax'):
            return render_to_response("alat/ajax_cabang.html", {'object_list': results})
    return HttpResponseRedirect("/")


def update_permintaan_gudang(request):
    try :
        f = forms.DateField()
        tanggal_pengiriman = f.clean(request.POST.get('tanggal_pengiriman',''))
        form = forms.CharField()
        status_permintaan = form.clean(request.POST.get('status_permintaan',''))
        
    except :
        return HttpResponseRedirect('/permintaan/arsip/?tgl=%s' % (request.POST.get('tgl', '')))
    if  status_permintaan == '3' :
        for i in request.POST.getlist('id_minta'):
            pk = AkadGadai.objects.get(id=int(i))
            barang = Barang.objects.get(id =pk.barang.id)
            pk.tanggal_pengiriman = tanggal_pengiriman
            pk.status_permintaan = status_permintaan
            #messages.add_message(request, messages.INFO,' Permintan telah di inputkan.')
            pk.save()
            barang = pk.barang
            barang.barang_keluar = pk.tanggal_pengiriman
            barang.save()
            messages.add_message(request, messages.INFO,' TELAH DI INPUTKAN')
    else:
        for i in request.POST.getlist('id_minta'):
            pk = AkadGadai.objects.get(id=int(i))
            barang = Barang.objects.get(id =pk.id)
            pk.status_permintaan = status_permintaan           
            pk.save()
            barang = pk.barang            
            barang.save()
            messages.add_message(request, messages.INFO,' TELAH DI INPUTKAN STATUS TDK DITEMUKAN')

    return HttpResponseRedirect('/permintaan/input_permintaan_gudang/')

def input_permintaan_gudang(request):
    kp = []
    blm =[]
    form = FilterPermintaanForm()
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET:
        end_date = request.GET['end_date']
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '1' :
            gerai = AkadGadai.objects.filter(tanggal_permintaan__range=(start_date,end_date)).filter(status_permintaan__in =('1','3','4')).order_by('gerai').order_by('barang')
            for k in gerai:
                kp.append(k)                
            start_date = start_date
            end_date = end_date
            
            template = 'barang/gudang/menu_gudang.html'
            variables = RequestContext(request, {'kp':kp,'end_date':end_date,'form':form})        
            return render_to_response(template, variables)
        else:
            gerai = AkadGadai.objects.filter(tanggal_permintaan__range=(start_date,end_date)).filter(gerai__id= id_cabang).filter(status_permintaan__in =('1','3','4')).order_by('gerai')
            for k in gerai:
                kp.append(k)                
            start_date = start_date
            end_date = end_date
            
            template = 'barang/gudang/menu_gudang.html'
            variables = RequestContext(request, {'kp':kp,'end_date':end_date,'form':form})        
            return render_to_response(template, variables)
    
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        end_date = request.GET['end_date']
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '1' :
            belum = AkadGadai.objects.filter(status_permintaan = '4').order_by('gerai')
            gerai = AkadGadai.objects.filter(tanggal_permintaan__range=(start_date,end_date)).filter(status_permintaan__in =('1','3','4')).order_by('gerai')
            for k in gerai:
                kp.append(k)                
            start_date = start_date
            end_date = end_date
            
            for a in belum:
                blm.append(a)

            template = 'barang/gudang/menu_gudang_pemesanan.html'
            variables = RequestContext(request, {'kp':kp,'end_date':end_date,'start_date':start_date,'blm':blm,'form':form})        
            return render_to_response(template, variables)
        else:
            belum = AkadGadai.objects.filter(status_permintaan = '4').filter(gerai__id = id_cabang)
            gerai = AkadGadai.objects.filter(tanggal_permintaan__range=(start_date,end_date)).filter(gerai__id= id_cabang).filter(status_permintaan__in =('1','3','4')).order_by('gerai')
            for k in gerai:
                kp.append(k)                
            start_date = start_date
            end_date = end_date
            for a in belum:
                blm.append(a)            

            template = 'barang/gudang/menu_gudang_pemesanan.html'
            variables = RequestContext(request, {'kp':kp,'end_date':end_date,'start_date':start_date,'blm':blm,'form':form})        
            return render_to_response(template, variables)
    
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        end_date = request.GET['end_date']
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '1' :
            gerai = AkadGadai.objects.filter(tanggal_pengiriman__range=(start_date,end_date)).filter(status_permintaan__in =('1','3','4')).order_by('gerai')
            for k in gerai:
                kp.append(k)                
            start_date = start_date
            end_date = end_date
            
            template = 'barang/gudang/menu_gudang_pengiriman.html'
            variables = RequestContext(request, {'kp':kp,'end_date':end_date,'form':form})        
            return render_to_response(template, variables)
        else:
            gerai = AkadGadai.objects.filter(tanggal_pengiriman__range=(start_date,end_date)).filter(gerai__id= id_cabang).filter(status_permintaan__in =('1','3','4')).order_by('gerai')
            for k in gerai:
                kp.append(k)
            blm_ketemu = AkadGadai.objects.filter(status_permintaan=int(4)).filter(gerai__id= id_cabang).order_by('gerai')
            for c in blm_ketemu:
                blm.append(c)
            start_date = start_date
            end_date = end_date
            
            template = 'barang/gudang/menu_gudang_pengiriman.html'
            variables = RequestContext(request, {'kp':kp,'blm':blm,'end_date':end_date,'form':form})        
            return render_to_response(template, variables)    
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_empat' in request.GET:
        end_date = request.GET['end_date']
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '1' :
            gerai = AkadGadai.objects.filter(tanggal_pengiriman__range=(start_date,end_date)).order_by('gerai')
            for k in gerai:
                kp.append(k)                
            start_date = start_date
            end_date = end_date
            
            template = 'barang/gudang/edit_menu_gudang_pengiriman.html'
            variables = RequestContext(request, {'kp':kp,'end_date':end_date,'form':form})        
            return render_to_response(template, variables)
        else:
            gerai = AkadGadai.objects.filter(tanggal_pengiriman__range=(start_date,end_date)).filter(gerai__id= id_cabang).order_by('gerai')
            for k in gerai:
                kp.append(k)
            blm_ketemu = AkadGadai.objects.filter(status_permintaan=int(4)).filter(gerai__id= id_cabang).order_by('gerai')
            for c in blm_ketemu:
                blm.append(c)
            start_date = start_date
            end_date = end_date
            
            template = 'barang/gudang/edit_menu_gudang_pengiriman.html'
            variables = RequestContext(request, {'kp':kp,'blm':blm,'end_date':end_date,'form':form})        
            return render_to_response(template, variables)      
        
    else:
        template = 'barang/gudang/menu_gudang.html'
        variables = RequestContext(request, {'kp': kp,'form':form})
        return render_to_response(template, variables)


def permintaan_gudang(request):
    try :
        f = forms.DateField()
        tanggal_pengiriman = f.clean(request.POST.get('tanggal_pengiriman',''))
        form = forms.CharField()
        status_permintaan = form.clean(request.POST.get('status_permintaan',''))
        
    except :
        return HttpResponseRedirect('/permintaan/arsip/?tgl=%s' % (request.POST.get('tgl', '')))
    for i in request.POST.getlist('id_minta'):
        pk = AkadGadai.objects.get(id=int(i))
        pk.tanggal_pengiriman = tanggal_pengiriman
        pk.status_permintaan = status_permintaan
        #messages.add_message(request, messages.INFO,' Permintan telah di inputkan.')
        pk.save()
        barang = pk.barang
        barang.barang_keluar = pk.tanggal_pengiriman
        barang.save()
        messages.add_message(request, messages.INFO,' TELAH DI INPUTKAN')

    return HttpResponseRedirect('/permintaan/arsip/?tgl=%s' % (request.POST.get('tgl', '')))

def list(request):    
    tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC")[0]     
    return HttpResponseRedirect("/permintaan/arsip/?tgl=%s" % tanggal.strftime('%Y-%m-%d') )


def list_day(request):
    try :
        f = forms.DateField()
        tanggal_permintaan = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC").filter(tanggal_permintaan__month=tanggal.month)
        except:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    gerai = []
    
    for (b,k) in GERAI:
        
        bn = AkadGadai.objects.filter(gerai = b ).filter(tanggal_permintaan = tanggal_permintaan).order_by('no').order_by('status_permintaan')
    
        for akadgadai in bn :
            gerai.append(akadgadai)    
           
        
        
    template = 'permintaan/permintaan_day.html'
    variables = RequestContext(request, {
        'tanggal_permintaan' : tanggal_permintaan,
        'day_list' : AkadGadai.objects.dates('tanggal_permintaan', 'day', order="DESC").filter(tanggal_permintaan__month=tanggal_permintaan.month),
        'month_list': AkadGadai.objects.dates('tanggal_permintaan', 'month', order="DESC").filter(tanggal_permintaan__year=tanggal_permintaan.year),
        'year_list' : AkadGadai.objects.dates('tanggal', 'year', order="DESC"),
        'gerai' : gerai,
    })    
    return render_to_response(template, variables)

def list_month(request):
    try :
        f = forms.DateField()
        tanggal_permintaan = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC").filter(tanggal_permintaan__month=tanggal.month)
        except:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    gerai = []
    
    for (b,k) in GERAI:
        
        bn = AkadGadai.objects.filter(gerai = b ).filter(tanggal_permintaan__month = tanggal_permintaan.month).order_by('no').order_by('status_permintaan')
    
        for akadgadai in bn :
            gerai.append(akadgadai)    
    template = 'permintaan/permintaan_month.html'
    variables = RequestContext(request, {
        'tanggal_permintaan' : tanggal_permintaan,
        'day_list' : AkadGadai.objects.dates('tanggal_permintaan', 'day', order="DESC").filter(tanggal_permintaan__month=tanggal_permintaan.month),
        'month_list': AkadGadai.objects.dates('tanggal_permintaan', 'month', order="DESC").filter(tanggal_permintaan__year=tanggal_permintaan.year),
        'year_list' : AkadGadai.objects.dates('tanggal', 'year', order="DESC"),
        'gerai' : gerai,
    })    
    return render_to_response(template, variables)

def list_year(request):
    try :
        f = forms.DateField()
        tanggal_permintaan = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal_permintaan =  AkadGadai.objects.dates('tanggal_permintaan', 'day', order="DESC").filter(tanggal_permintaan__month=tanggal.month)[0] 
        except:
            tanggal_permintaan =  AkadGadai.objects.dates('tanggal_permintaan', 'day', order="DESC")[0] 
    
    gerai = []
    
    for (b,k) in GERAI:
        
        bn = AkadGadai.objects.filter(gerai = b ).filter(tanggal_permintaan__year=tanggal_permintaan.year).order_by('no').order_by('status_permintaan')
    

        for akadgadai in bn :
            gerai.append(akadgadai)  
        
    
    template = 'permintaan/permintaan_year.html'

    variables = RequestContext(request, {
        'tanggal_permintaan' : tanggal_permintaan,
        'day_list' : AkadGadai.objects.dates('tanggal_permintaan', 'day', order="DESC").filter(tanggal_permintaan__month=tanggal_permintaan.month),
        'month_list': AkadGadai.objects.dates('tanggal_permintaan', 'month', order="DESC").filter(tanggal_permintaan__year=tanggal_permintaan.year),
        'year_list' : AkadGadai.objects.dates('tanggal_permintaan', 'year', order="DESC"),
        'gerai' : gerai ,
        })    
    return render_to_response(template, variables)

def rekapkirimhari(request, object_id):
    tanggal_pengiriman = forms.DateField().clean(request.GET.get('tgl',''))
    barang = AkadGadai.objects.filter(gerai= str(object_id)).filter(tanggal_pengiriman = tanggal_pengiriman).order_by('gerai') 
    template = 'permintaan/rekaphari.html'
    variables = RequestContext(request, {
        'barang': barang,
        'tanggal_pengiriman' : tanggal_pengiriman,
        'nilai': sum([b.nilai for b in barang ]),
        'jasa': sum([b.jasa for b in barang ]),
        'adm': sum([b.adm for b in barang ]),
        'simpan': sum([b.biayasimpan for b in barang ]),
        'bersih' : sum([b.terima_bersih for b in barang ]),
    })    
    return render_to_response(template, variables)
    
