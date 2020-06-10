from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gadai.appgadai.gerai.views import*
from gadai.appgadai.models import *
import datetime
from gadai.appgadai.templatetags.number_format import number_format
from gadai.appgadai.models import *
from django import forms
from gadai.appgadai.templatetags.terbilang import terbilang


###cetak Rekap bulanan###
def piutang_bulan(request, object_id):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  AkadGadai.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    #tanggal = forms.DateField()
    gr =GeraiGadai.objects.get(id = object_id)
    gerai = gr.akadgadai_set.order_by('gerai')
        
    template = 'gerai/piutang.html'
    variables = RequestContext(request, {
        'gr':gr,
        'gerai':gerai,
        'tanggal':tanggal,
        'nilai': sum([b.terima_bersih for b in gerai ]),
        'jasa': sum([b.jasa for b in gerai ]),
        'adm': sum([b.adm for b in gerai ]),
        'simpan': sum([b.biayasimpan for b in gerai ]),
        'bersih': sum([b.terima_bersih for b in gerai ]),
        #'simpanprpj': sum([b.bea_simpanprpj for b in gerai]),
    })
    return render_to_response(template,variables)
###teddy
def rekappiutang(request):
    gerai = GeraiGadai.objects.all()
    kp = []
    for k in gerai:
        if k.akadgadai_set.filter(lunas__isnull= True).count() > 0:
            kp.append(k)
    
    total_piutang = total_akad = total_nilai  = total_piutang_a = total_pelunasan=total_aktif= total_piutang_jasa = total_piutang_beasimpan=total_piutang_denda=total_banyak_lunas=total_all_aktif=0
    total_piutang_perbulan = 0
    for k in kp :
        total_aktif += k.aktif()
        total_piutang += k.piutang()
        total_piutang_a += k.piutang_a()
        total_nilai += k.get_jumlah_nilai_harian()
        total_akad += k.aktif_harian()
        total_pelunasan += k.nilai_pelunasan()
        total_piutang_jasa += k.total_piutang_jasa()
        total_piutang_beasimpan += k.total_piutang_beasimpan()
        total_piutang_denda += k.total_piutang_denda()
        total_banyak_lunas +=k.get_banyak_lunas()
        total_all_aktif +=k.all_aktif()
    
    template = 'piutang/rekappiutang.html'
    variables = RequestContext(request, {
    'kp': kp ,
    'nkp' : len(kp),
    'aktif' : total_aktif,
    'npk' : total_akad,
    'piutang' : total_piutang,
    'piutang_a' : total_piutang_a,
    'lunas' : total_pelunasan,
    'jasa': total_piutang_jasa,
    'denda': total_piutang_denda,
    'beasimpan': total_piutang_beasimpan,
    'akadlunas':total_banyak_lunas,
    'totalakad':total_all_aktif
    })
    return render_to_response(template, variables)


