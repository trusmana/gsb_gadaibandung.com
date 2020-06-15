from django.contrib.auth import logout
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404,render
from django import forms
import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required, user_passes_test
from gadai.appgadai.kasirgerai.forms import *
from gadai.appgadai.jurnal.forms import *
from django.contrib import messages
from gadai.appgadai.models import *

import httplib, urllib
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import timedelta

import httplib, urllib
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import timedelta
import os, string
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

from gadai.appgadai.templatetags.terbilang import terbilang
from gadai.appgadai.templatetags.number_format import number_format

from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm
D = decimal.Decimal

###BUAT KAS PUSAT

def cetak_transaksi_kas_pusat(request,object_id):
    kocab = Tbl_Cabang.objects.get(kode_cabang=object_id)
    cab = object_id
    sekarang = datetime.date.today()
    bray_posting = PostingGerai.objects.filter(kode_cabang=object_id,tanggal =sekarang)
    tes_posting = bray_posting.count()

    tgl = timedelta(days=1)
    tanggal = sekarang - tgl
    a = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang).filter(id_coa__coa__startswith ='11.01').filter(jenis='SALDOKASGERAI').latest('id')

    c = a.tgl_trans
    d = sekarang - c

    s_awal = Tbl_TransaksiKeu.objects.filter(id_cabang=300).filter(id_coa__coa ='11.01.01').filter(tgl_trans=sekarang).\
        filter(jenis='SALDOKASGERAI')
    s_awal_lates = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang).filter(id_coa__coa ='11.01.01').filter(jenis='SALDOKASGERAI').filter(tgl_trans=c)

    pendapatan = Tbl_Transaksi.objects.filter(id_unit = 300).filter(debet__gt =0).filter(id_coa__id=4).filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran = Tbl_Transaksi.objects.filter(id_unit = 300).filter(kredit__gt =0).filter(id_coa__id=4).filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    jrn_pendapatan = Tbl_Transaksi.objects.filter(jenis__in=('GL_GL_PUSAT','AYDA_PUSAT')).filter(status_jurnal=2).filter(id_cabang=object_id).filter(tgl_trans= sekarang).filter(debet__gt=0).filter(id_coa_id=4)
    jrn_pengeluaran = Tbl_Transaksi.objects.filter(id_cabang=object_id).filter(kredit__gt= 0).filter(status_jurnal=2).filter(id_coa_id=4).filter(tgl_trans= sekarang).filter(jenis='GL_GL_PUSAT').filter(tgl_trans= sekarang)

    saldo_awal = sum([p.saldo for p  in s_awal]) 
    total_penerimaan = sum([p.debet for p  in pendapatan]) + sum([p.debet for p  in jrn_pendapatan])
    total_pengeluaran = sum([p.kredit for p  in pengeluaran]) + sum([p.kredit for p  in jrn_pengeluaran])

    saldo_akhir = (sum([p.saldo for p  in s_awal]) + (sum([p.debet for p  in pendapatan]) + sum([p.debet for p  in jrn_pendapatan]))) - (sum([p.kredit for p  in pengeluaran]) + sum([p.kredit for p  in jrn_pengeluaran]))
    variables = RequestContext(request,{'pendapatan':pendapatan,'kocab':kocab,'pengeluaran':pengeluaran,
      'total_saldo':saldo_awal,'total_penerimaan':total_penerimaan,'total_pengeluaran':total_pengeluaran,
      'jrn_pengeluaran':jrn_pengeluaran,'jrn_pendapatan':jrn_pendapatan,'saldo_akhir':saldo_akhir,'sekarang':sekarang})
    template='kasir/view/cetak_transaksi_kas_pusat.html'
    return render_to_response(template,variables)

def transaksi_kas_pusat(request,object_id):
    kocab = Tbl_Cabang.objects.get(kode_cabang=object_id)
    cab = object_id
    sekarang = datetime.date.today()
    bray_posting = PostingGerai.objects.filter(kode_cabang=object_id,tanggal =sekarang)
    tes_posting = bray_posting.count()

    tgl = timedelta(days=1)
    tanggal = sekarang - tgl
    a = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang).filter(id_coa__coa__startswith ='11.01').filter(jenis='SALDOKASGERAI').latest('id')

    c = a.tgl_trans
    d = sekarang - c

    s_awal = Tbl_TransaksiKeu.objects.filter(id_cabang=300).filter(id_coa__coa ='11.01.01').filter(tgl_trans=sekarang).\
        filter(jenis='SALDOKASGERAI')
    s_awal_lates = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang).filter(id_coa__coa ='11.01.01').filter(jenis='SALDOKASGERAI').filter(tgl_trans=c)

    pendapatan = Tbl_Transaksi.objects.filter(id_unit = 300).filter(debet__gt =0).filter(id_coa__id=4).filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran = Tbl_Transaksi.objects.filter(id_unit = 300).filter(kredit__gt =0).filter(id_coa__id=4).filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    jrn_pendapatan = Tbl_Transaksi.objects.filter(jenis__in=('GL_GL_PUSAT','AYDA_PUSAT')).filter(status_jurnal=2).filter(id_cabang=object_id).filter(tgl_trans= sekarang).filter(debet__gt=0).filter(id_coa_id=4)
    jrn_pengeluaran = Tbl_Transaksi.objects.filter(id_cabang=object_id).filter(kredit__gt= 0).filter(status_jurnal=2).filter(id_coa_id=4).filter(tgl_trans= sekarang).filter(jenis='GL_GL_PUSAT').filter(tgl_trans= sekarang)

    saldo_awal = sum([p.saldo for p  in s_awal]) 
    total_penerimaan = sum([p.debet for p  in pendapatan]) + sum([p.debet for p  in jrn_pendapatan])
    total_pengeluaran = sum([p.kredit for p  in pengeluaran]) + sum([p.kredit for p  in jrn_pengeluaran])

    saldo_akhir = (sum([p.saldo for p  in s_awal]) + (sum([p.debet for p  in pendapatan]) + sum([p.debet for p  in jrn_pendapatan]))) - (sum([p.kredit for p  in pengeluaran]) + sum([p.kredit for p  in jrn_pengeluaran]))
    variables = RequestContext(request,{'pendapatan':pendapatan,'kocab':kocab,'pengeluaran':pengeluaran,
      'total_saldo':saldo_awal,'total_penerimaan':total_penerimaan,'total_pengeluaran':total_pengeluaran,
      'jrn_pengeluaran':jrn_pengeluaran,'jrn_pendapatan':jrn_pendapatan,'saldo_akhir':saldo_akhir})
    template='kasir/view/transaksi_kas_pusat.html'
    return render_to_response(template,variables)
###AKHIR KAS PUSAT

###BUAT BANK PUSAT
def transaksi_bank_pusat(request,object_id):
    kocab = Tbl_Cabang.objects.get(kode_cabang=object_id)
    cab = object_id
    gr = Tbl_Cabang.objects.filter(status_aktif = 1)
    sekarang = datetime.date.today()
    tgl = timedelta(days=1)
    tanggal = sekarang - tgl
    a = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang).filter(id_coa__coa__startswith ='11.05.01').filter(jenis='SALDOKASGERAI').latest('id')

    c = a.tgl_trans
    d = sekarang - c
    s_awal = Tbl_TransaksiKeu.objects.filter(id_cabang=300).filter(id_coa__coa ='11.05.01').filter(tgl_trans=sekarang).\
        filter(jenis='SALDOKASGERAI')
    s_awal_lates = Tbl_TransaksiKeu.objects.filter(id_cabang=object_id).filter(id_coa__coa ='11.05.01').filter(jenis='SALDOKASGERAI')#.filter(tgl_trans=c)

    tbl = Tbl_Cabang.objects.filter(kode_unit = 300)
    jrn_pendapatan = Tbl_Transaksi.objects.filter(id_cabang = object_id).filter(debet__gt =0).filter(tgl_trans = sekarang).filter(id_coa__coa__startswith='11.05').filter(jenis__in=('GL_GL_PUSAT_BANK','AYDA_PUSAT_BANK','GL_GL_PUSAT'))
    jrn_pengeluaran = Tbl_Transaksi.objects.filter(id_cabang=object_id).filter(kredit__gt =0).filter(tgl_trans= sekarang).filter(id_coa__coa__startswith='11.05').filter(jenis__in=('GL_GL_PUSAT','AYDA_PUSAT_BANK'))
    
    pengeluaran_1 = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(kredit__gt =0).filter(id_coa_id =(132)).filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)
    pendapatan_1 = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(debet__gt =0).filter(id_coa_id__in =(4,132)).filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)

    saldo_awal = sum([p.saldo for p  in s_awal]) 
    total_penerimaan = sum([p.debet for p in pendapatan_1]) + sum([p.debet for p  in jrn_pendapatan])
    total_pengeluaran = sum([p.kredit for p in pengeluaran_1]) + sum([p.kredit for p  in jrn_pengeluaran])
    

    pdp_all_debet = Tbl_Transaksi.objects.filter(jenis__in=('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(debet__gt= 0).filter(tgl_trans= sekarang)
    pdp_all_kredit = Tbl_Transaksi.objects.filter(jenis='GL_GL_PENGELUARAN_PUSAT_BANK').filter(kredit__gt =0).filter(tgl_trans= sekarang)

    saldo_akhir = (sum([p.saldo for p  in s_awal]) + (sum([p.debet for p  in pendapatan_1]) + sum([p.debet for p  in jrn_pendapatan]))) - (sum([p.kredit for p  in pengeluaran_1]) + sum([p.kredit for p  in jrn_pengeluaran]))

    template = 'kasir/view/transaksi_bank_pusat.html'
    variables = RequestContext(request, {'pendapatan_1':pendapatan_1,'kocab':kocab,'pengeluaran_1':pengeluaran_1,
      'total_saldo':saldo_awal,'total_penerimaan':total_penerimaan,'total_pengeluaran':total_pengeluaran,
      'jrn_pengeluaran':jrn_pengeluaran,'jrn_pendapatan':jrn_pendapatan,'sekarang':sekarang,'saldo_akhir':saldo_akhir})

    return render_to_response(template,variables)

def cetak_transaksi_bank_pusat(request,object_id):
    kocab = Tbl_Cabang.objects.get(kode_cabang=object_id)
    cab = object_id
    gr = Tbl_Cabang.objects.filter(status_aktif = 1)
    sekarang = datetime.date.today()
    tgl = timedelta(days=1)
    tanggal = sekarang - tgl
    a = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang).filter(id_coa__coa__startswith ='11.05.01').filter(jenis='SALDOKASGERAI').latest('id')

    c = a.tgl_trans
    d = sekarang - c
    s_awal = Tbl_TransaksiKeu.objects.filter(id_cabang=300).filter(id_coa__coa ='11.05.01').filter(tgl_trans=sekarang).\
        filter(jenis='SALDOKASGERAI')
    s_awal_lates = Tbl_TransaksiKeu.objects.filter(id_cabang=object_id).filter(id_coa__coa ='11.05.01').filter(jenis='SALDOKASGERAI')#.filter(tgl_trans=c)

    tbl = Tbl_Cabang.objects.filter(kode_unit = 300)
    jrn_pendapatan = Tbl_Transaksi.objects.filter(id_cabang = object_id).filter(debet__gt =0).filter(tgl_trans = sekarang).filter(id_coa__coa__startswith='11.05').filter(jenis__in=('GL_GL_PUSAT_BANK','AYDA_PUSAT_BANK','GL_GL_PUSAT'))
    jrn_pengeluaran = Tbl_Transaksi.objects.filter(id_cabang=object_id).filter(kredit__gt =0).filter(tgl_trans= sekarang).filter(id_coa__coa__startswith='11.05').filter(jenis__in=('GL_GL_PUSAT','AYDA_PUSAT_BANK'))
    
    pengeluaran_1 = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(kredit__gt =0).filter(id_coa_id =(132)).filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)
    pendapatan_1 = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(debet__gt =0).filter(id_coa_id__in =(4,132)).filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)

    saldo_awal = sum([p.saldo for p  in s_awal]) 
    total_penerimaan = sum([p.debet for p in pendapatan_1]) + sum([p.debet for p  in jrn_pendapatan])
    total_pengeluaran = sum([p.kredit for p in pengeluaran_1]) + sum([p.kredit for p  in jrn_pengeluaran])
    

    pdp_all_debet = Tbl_Transaksi.objects.filter(jenis__in=('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(debet__gt= 0).filter(tgl_trans= sekarang)
    pdp_all_kredit = Tbl_Transaksi.objects.filter(jenis='GL_GL_PENGELUARAN_PUSAT_BANK').filter(kredit__gt =0).filter(tgl_trans= sekarang)


    template = 'kasir/view/cetak_transaksi_bank_pusat.html'
    variables = RequestContext(request, {'pendapatan_1':pendapatan_1,'kocab':kocab,'pengeluaran_1':pengeluaran_1,
      'total_saldo':saldo_awal,'total_penerimaan':total_penerimaan,'total_pengeluaran':total_pengeluaran,
      'jrn_pengeluaran':jrn_pengeluaran,'jrn_pendapatan':jrn_pendapatan,'sekarang':sekarang})

    return render_to_response(template,variables)
###AKHIR BANK PUSAT

def all_transaksi_bank_pusat(request,object_id):
    kocab = Tbl_Cabang.objects.get(kode_cabang=object_id)
    sekarang = datetime.date.today()
    tgl = timedelta(days=1)
    tanggal = sekarang - tgl
    a = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang).filter(id_coa__coa__startswith ='11.05').filter(jenis='SALDOKASGERAI').latest('id')
    #b = a[0]
    c = a.tgl_trans
    d = sekarang - c
    print'c', c, 'd',d,'tanggal',tanggal
    s_awal = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang).filter(id_coa__coa__startswith ='11.05').filter(tgl_trans=sekarang).\
        filter(jenis='SALDOKASGERAI')
    s_awal_lates = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang).filter(id_coa__coa__startswith ='11.05').filter(jenis='SALDOKASGERAI').filter(tgl_trans=c)

    kocab = Tbl_Cabang.objects.get(kode_cabang=object_id)
    cab = object_id
    sekarang = datetime.date.today()
    #s_awal =Tbl_Transaksi.objects.filter(id_cabang=kocab.kode_cabang).filter(tgl_trans=sekarang).filter(id_coa__coa__contains ='11.05').\
        #filter(jenis='SALDOKASGERAI')
    #s_awal =Tbl_Transaksi.objects.filter(jurnal__kode_cabang=kocab.kode_cabang).filter(id_coa__coa__contains ='11.05').\
        #filter(jenis='SALDOKASGERAI').latest('id')
    tampil =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(status_posting__isnull = True).\
        filter(jurnal__kode_cabang=kocab.kode_cabang)
    setoran_bank_gerai = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis__in = (u'GL_GL_PENGELUARAN_BANK','GL_GL_PENAMBAHAN_BANK_RAK',u'Pelunasan_kasir_bank_rak')).\
        filter(id_cabang=cab).filter(status_jurnal=2)
    #setoran_kas_gerai = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENAMBAHAN_KAS').\
        #filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_uk_bank = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGELUARAN_BANK').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_bank_pusat = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('GL_GL_PENGEMBALIAN_PUSAT_BANK','GL_GL_PENGEMBALIAN_PUSAT_BANK_RAK','GL_GL_PENGEMBALIAN_BANK_CABANG_RAK')).\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_kas_pusat = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGELUARAN_KAS_PUSAT').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_bank = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in =('GL_GL_PENAMBAHAN_BANK','GL_GL_PENGELUARAN_BANK_RAK')).\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_kas = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGELUARAN_KAS_PUSAT').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    uang_muka_gerai = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PUSAT_UK').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pencairan_kasir = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pencairan_kasir_bank',\
        'Pencairan_kasir_lebih_bank','Pencairan_kasir_kurang_bank')).\
        filter(id_cabang=cab).filter(status_jurnal=2).filter(id_coa = 298L)
    pencairan_kasir_sisa = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pencairan_kasir_bank',\
        'Pencairan_kasir_lebih_bank','Pencairan_kasir_kurang_bank','Pelunasan_kasir_bank','Pelunasan_gu_kasir_nilai_sblm_kurang_bank',\
        'Pelunasan_gu_kasir_nilai_sblm_lebih_bank','Pelunasan_Gadai_Ulang_kasir_bank','Pelunasan_Gadai_Ulang_kasir_bank',\
        'Pelunasan_gu_kasir_nilai_sblm_kurang_bank_bol','Pelunasan_kasir_bank_rak',\
        'Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer',\
        'Pelunasan_Gadai_ulang_kasir_bank_kelebihan_pendapatan','Pencairan_kasir_sisa','Pelunasan_gu_bank_nilai_sblm_lebih_pol',\
        'Pendapatan_Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan','Pendapatan_Pelunasan_Gadai_ulang_kasir_bank_kelebihan_pendapatan')).filter(id_cabang=cab).filter(status_jurnal=2).filter(id_coa__in= (448L,546L))    
    pengembalian_uk = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGEMBALIAN_UK').\
        filter(id_cabang=cab).filter(status_jurnal=2)    
    saldo_yang_dikirim = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').\
        filter(id_cabang=cab).filter(status_jurnal=2)#.filter(jurnal__status_jurnal = u'3')
    transaksi_jurnal = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pencairan_kasir_kurang_bank_kecil','Pelunasan_gu_kasir_nilai_sblm_kurang_bol_bank','Pelunasan_gu_kasir_nilai_sblm_lebih_bank_10_bol',\
        'Pelunasan_kasir_bank_bol','GL_GL_CABANG_ADM_BANK')).filter(id_cabang=cab).filter(status_jurnal=2)
    saldo_awal_hari = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_BIAYA_GERAI').\
        filter(id_cabang=cab).filter(status_jurnal=2)#.filter(jurnal__status_jurnal = u'2')
    saldo_uang_muka_hari = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT_UK').\
        filter(id_cabang=cab).filter(status_jurnal=2)#.filter(jurnal__status_jurnal = u'2')
    jurnal_list = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'Pencairan_kasir_bank').\
        filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa= 7L)
    pndptn_lainnya = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis__in =('Pencairan_kasir_bank','Pelunasan_kasir','Pelunasan_kasir_bank')).filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa= 448L)
    tbl = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = (u'Pelunasan_kasir_bank',u'Pelunasan_kasir_bank_rak')).\
        filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa__in= (287L,651L,635L))
    tbl_beban =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').\
        filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa= 516L)
    rakp =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').\
        filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa= 378L)    
    #penjualan = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = ('Penjualan_lelang_kasir')).\
        #filter(id_cabang=object_id).filter(status_jurnal=2)
    ak_ulang = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pelunasan_gu_kasir_nilai_sblm_lebih_bank',\
        'Pelunasan_Gadai_Ulang_kasir_bank','Pelunasan_gu_kasir_nilai_sblm_kurang_bank','Pelunasan_gu_bank_nilai_sblm_lebih',\
        'Penerimaan Gadai Ulang','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_pendapatan')).filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa__in= (448L,287L,298L))

    akad_ulang_pengeluaran = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
         filter(jenis = ('Pelunasan_Gadai_Ulang_kasir_pinjaman_besar')).filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa= 298L)

    pengeluaran_gadai_ulang = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis__in=( u'Pelunasan_Gadai_Ulang_Kasir_nilai_pinjaman_lebih','Pelunasan_gu_kasir_nilai_sblm_kurang_bank',\
        'Pelunasan_Gadai_Ulang_kasir_bank','Pelunasan_gu_kasir_nilai_sblm_lebih_bank_10')).filter(id_cabang=object_id).\
        filter(status_jurnal=2).filter(id_coa =298L)

    pelunasan_kelebihan_kasir = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'Pelunasan_kasir_bank').filter(id_cabang=cab).filter(status_jurnal=2).filter(id_coa= 771)

    gadai_ulang_kelebihan_kasir = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_pendapatan','Pendapatan1_Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan','Pendapatan1_Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer')).filter(id_cabang=cab).filter(status_jurnal=2).filter(id_coa= 771)
    hitung_a = sum ([a.kredit for a in ak_ulang]) + sum ([a.kredit for a in setoran_bank_gerai]) \
        + sum ([a.kredit for a in pencairan_kasir_sisa]) + sum ([a.kredit for a in tbl]) + sum([a.kredit for a in pelunasan_kelebihan_kasir])\
        + sum ([a.kredit for a in gadai_ulang_kelebihan_kasir])
    hitung_b = sum ([a.debet for a in pengembalian_bank])\
        + sum ([a.debet for a in pencairan_kasir])\
        + sum([a.debet for a in pengeluaran_gadai_ulang])\
        + sum([a.debet for a in transaksi_jurnal])
    saldo_awal = sum([p.saldo for p  in s_awal])   
    saldo_awal_lates =  sum([p.saldo for p in s_awal_lates])

    if d > datetime.timedelta(1) :
        variables = RequestContext(request,{'pelunasan_kelebihan_kasir':pelunasan_kelebihan_kasir,'kocab':kocab,'transaksi_jurnal':transaksi_jurnal,'a':jurnal_list,\
            'gadai_ulang_kelebihan_kasir':gadai_ulang_kelebihan_kasir,
            'total_pencairan':sum ([a.kredit for a in jurnal_list]),\
            'setoran_bank_gerai' : sum ([a.kredit for a in setoran_bank_gerai]),\
            'pengembalian_bank_pusat_pjb' :sum ([a.debet for a in pengembalian_bank_pusat]) ,
            'pengembalian_bank' :sum ([a.debet for a in pengembalian_bank]) + sum ([a.kredit for a in pengembalian_kas]),\
            'uang_muka':sum ([a.kredit for a in uang_muka_gerai]),'saldo_awal':saldo_awal,
            #'saldo_awal': sum([a.saldo for a in s_awal]),
            'total_penerimaan':hitung_a,
            'total_pengeluaran': hitung_b ,
            'saldo_akhir': saldo_awal + int(hitung_a) - int(hitung_b),
            'saldo_keseluruhan': (saldo_awal + hitung_a - hitung_b) - sum ([a.kredit for a in pengembalian_bank_pusat]),             
            'pencairan':sum ([a.debet for a in pencairan_kasir]),\
            'pencairan_kasir_sisa':pencairan_kasir_sisa,\
            'saldo_awal_hari':sum ([a.debet for a in saldo_awal_hari]),\
            'saldo_uangmuka_hari':sum ([a.debet for a in saldo_uang_muka_hari]),\
            'total_pelunasan':tbl,\
            'total_pendapatan_lainnya':sum ([a.kredit for a in pndptn_lainnya]),'sekarang':datetime.date.today(),\
            'beban_listrik':(sum ([a.debet for a in tbl_beban])),\
            'total_rakp':sum ([a.kredit for a in rakp]), \
            'total_transaksi_jurnal': sum ([a.debet for a in transaksi_jurnal]),\
            'total_saldo' :  saldo_awal ,'ak_ulang':ak_ulang,
            #'penjualan': penjualan,
            'pengeluaran_gadai_ulang': pengeluaran_gadai_ulang,'pengembalian_kas_pusat':pengembalian_kas_pusat,\
            'pengembalian_bank_pusat':pengembalian_kas_pusat,\
            'saldo_yang_di_kirim':sum ([a.debet for a in saldo_yang_dikirim]), 'pengembalian_kas':pengembalian_kas,\
            't_kasir':pencairan_kasir,'tampil':tampil,
            'pengembalian_bank':pengembalian_bank,'setoran_bank_gerai':setoran_bank_gerai,'cabang':kocab,
            'pengembalian_uk_bank':pengembalian_uk_bank})

    if d <= datetime.timedelta(1) :
        variables = RequestContext(request,{'pelunasan_kelebihan_kasir':pelunasan_kelebihan_kasir,'kocab':kocab,'transaksi_jurnal':transaksi_jurnal,'a':jurnal_list,\
            'gadai_ulang_kelebihan_kasir':gadai_ulang_kelebihan_kasir,
            'total_pencairan':sum ([a.kredit for a in jurnal_list]),\
            'setoran_bank_gerai' : sum ([a.kredit for a in setoran_bank_gerai]),\
            'pengembalian_bank_pusat_pjb' :sum ([a.debet for a in pengembalian_bank_pusat]) ,
            'pengembalian_bank' :sum ([a.debet for a in pengembalian_bank]) + sum ([a.kredit for a in pengembalian_kas]),\
            'uang_muka':sum ([a.kredit for a in uang_muka_gerai]),'saldo_awal':saldo_awal,
            #'saldo_awal': sum([a.saldo for a in s_awal]),
            'total_penerimaan':hitung_a,
            'total_pengeluaran': hitung_b ,
            'saldo_akhir': saldo_awal_lates + int(hitung_a) - int(hitung_b),
            'saldo_keseluruhan': (saldo_awal_lates + hitung_a - hitung_b) - sum ([a.kredit for a in pengembalian_bank_pusat]),             
            'pencairan':sum ([a.debet for a in pencairan_kasir]),\
            'pencairan_kasir_sisa':pencairan_kasir_sisa,\
            'saldo_awal_hari':sum ([a.debet for a in saldo_awal_hari]),\
            'saldo_uangmuka_hari':sum ([a.debet for a in saldo_uang_muka_hari]),\
            'total_pelunasan':tbl,\
            'total_pendapatan_lainnya':sum ([a.kredit for a in pndptn_lainnya]),'sekarang':datetime.date.today(),\
            'beban_listrik':(sum ([a.debet for a in tbl_beban])),\
            'total_rakp':sum ([a.kredit for a in rakp]), \
            'total_transaksi_jurnal': sum ([a.debet for a in transaksi_jurnal]),\
            'total_saldo' :  saldo_awal ,'ak_ulang':ak_ulang,
            #'penjualan': penjualan,
            'pengeluaran_gadai_ulang': pengeluaran_gadai_ulang,'pengembalian_kas_pusat':pengembalian_kas_pusat,\
            'pengembalian_bank_pusat':pengembalian_kas_pusat,\
            'saldo_yang_di_kirim':sum ([a.debet for a in saldo_yang_dikirim]), 'pengembalian_kas':pengembalian_kas,\
            't_kasir':pencairan_kasir,'tampil':tampil,
            'pengembalian_bank':pengembalian_bank,'setoran_bank_gerai':setoran_bank_gerai,'cabang':kocab,
            'pengembalian_uk_bank':pengembalian_uk_bank})

    template='kasir/view/all_transaksi_bank_pusat.html'
    return render_to_response(template,variables)   

def all_transaksi_kas_pusat(request,object_id):
    kocab = Tbl_Cabang.objects.get(kode_cabang=object_id)
    cab = object_id
    sekarang = datetime.date.today()
    tgl = timedelta(days=1)
    tanggal = sekarang - tgl
    a = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang).filter(id_coa__coa__startswith ='11.01').filter(jenis='SALDOKASGERAI').latest('id')
    #b = a[0]
    c = a.tgl_trans
    d = sekarang - c
    print'c', c, 'd',d,'tanggal',tanggal
    s_awal = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang).filter(id_coa__coa__startswith ='11.01').filter(tgl_trans=sekarang).\
        filter(jenis='SALDOKASGERAI')
    s_awal_lates = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang).filter(id_coa__coa__startswith ='11.01').filter(jenis='SALDOKASGERAI').filter(tgl_trans=c)
    #s_awal =Tbl_Transaksi.objects.filter(jurnal__kode_cabang=kocab.kode_cabang).filter(id_coa__coa__contains ='11.01').\
        #filter(jenis='SALDOKASGERAI').latest('id')
    tampil =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(status_posting__isnull = True).\
        filter(jurnal__kode_cabang=kocab.kode_cabang)
    setoran_bank_gerai = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PENAMBAHAN_BANK').\
        filter(jurnal__kode_cabang=cab).filter(status_jurnal=2)
    setoran_kas_gerai = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in =( 'GL_GL_PENAMBAHAN_KAS',u'Pelunasan_kasir_rak')).\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_uk_bank = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGELUARAN_BANK').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_bank_pusat = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGEMBALIAN_SALDO_GERAI').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_kas_pusat = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGELUARAN_KAS_PUSAT').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_bank = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGELUARAN_BANK').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_kas = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis__in =('GL_GL_PENGELUARAN_KAS_PUSAT','PENGELUARAN_KE_GERAI')).filter(id_cabang=cab).filter(status_jurnal=2)
    uang_muka_gerai = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PUSAT_UK').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pencairan_kasir = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'Pencairan_kasir').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pencairan_kasir_sisa = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pencairan_kasir',\
        'Pelunasan_kasir','Pelunasan_gu_kasir_nilai_sblm_lebih_pol','Pelunasan_gu_kasir_nilai_sblm_kurang_pdl','Pencairan_kasir_sisa',\
        'Pelunasan_kasir_rak','Pencairan_Kasir')).\
        filter(id_cabang=cab).filter(status_jurnal=2).filter(id_coa__in= (448L,546L))
    pengembalian_uk = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGEMBALIAN_UK').\
        filter(id_cabang=cab).filter(status_jurnal=2)    
    saldo_yang_dikirim = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').\
        filter(id_cabang=cab).filter(status_jurnal=2)#.filter(jurnal__status_jurnal = u'3')
    transaksi_jurnal = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = (u'GL_GL_CABANG',\
        u'Pelunasan_gu_kasir_nilai_sblm_lebih_bl',u'Pencairan_kasir_kurang','Pelunasan_gu_kasir_nilai_sblm_kurang_bol',\
        'Pelunasan_kasir_kurang_rak','Pelunasan_kasir_kurang')).filter(id_cabang=cab).filter(status_jurnal=2)#.filter(jurnal__status_jurnal = u'1')
    saldo_awal_hari = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_BIAYA_GERAI').\
        filter(id_cabang=cab).filter(status_jurnal=2)#.filter(jurnal__status_jurnal = u'2')
    saldo_uang_muka_hari = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT_UK').\
        filter(id_cabang=cab).filter(status_jurnal=2)#.filter(jurnal__status_jurnal = u'2')
    jurnal_list = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'Pencairan_kasir').\
        filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa= 7L)
    pndptn_lainnya = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in =('Pencairan_kasir')).\
        filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa= 448L)
    tbl = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = (u'Pelunasan_kasir',\
        u'Pelunasan_kasir',u'Pelunasan_kasir_kas_rak')).filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa__in= (651L,287L,635L,378L))
    tbl_beban =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').\
        filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa= 516L)
    rakp =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').\
        filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa= 378L)    
    #penjualan = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = ('Penjualan_lelang_kasir')).filter(id_cabang=object_id).filter(status_jurnal=2)
    ak_ulang = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pelunasan_gu_kasir_nilai_sblm_lebih',\
        'Pelunasan_Gadai_Ulang_kasir','Pelunasan_gu_kasir_nilai_sblm_kurang')).filter(id_cabang=object_id).filter(status_jurnal=2).\
        filter(id_coa__in= (448L,287L,298L))
    akad_ulang_pengeluaran = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis = ('Pelunasan_Gadai_Ulang_kasir_pinjaman_besar')).filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa= 298L)

    pengeluaran_gadai_ulang = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis__in = (u'Pelunasan_Gadai_Ulang_Kasir_nilai_pinjaman_lebih',u'Pelunasan_Gadai_Ulang_kasir_pinjaman_besar_tp',\
        u'Pelunasan_gu_kasir_nilai_sblm_lebih_tp',u'Pelunasan_gu_kasir_nilai_sblm_kurang','Pelunasan_Gadai_Ulang_kasir_pinjaman_besar')).\
        filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa=298L)                                                                                                                                                                                                                           
    pengembalian_nasabah = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis__in = ('Pengembalian_titipan_kelebihan','Pengembalian_titipan_kelebihan_gu')).\
        filter(id_cabang=cab).filter(status_jurnal=2) 
    hitung_a = sum ([a.kredit for a in ak_ulang]) +sum ([a.kredit for a in setoran_kas_gerai]) + sum ([a.kredit for a in setoran_bank_gerai])\
        +  sum ([a.kredit for a in pencairan_kasir_sisa]) + sum ([a.kredit for a in tbl]) 
    hitung_b = sum ([a.debet for a in transaksi_jurnal]) + sum ([a.debet for a in pengembalian_nasabah]) + \
            sum ([a.debet for a in pencairan_kasir]) +\
            sum ([a.kredit for a in pengembalian_kas]) +\
            sum ([a.debet for a in pengeluaran_gadai_ulang])
    saldo_awal =  sum([p.saldo for p in s_awal])
    saldo_awal_lates =  sum([p.saldo for p in s_awal_lates])
    poston = Tbl_Transaksi.objects.filter(id_cabang=kocab.kode_cabang).filter(tgl_trans=sekarang)
    postingon = sum([a.jurnal.postingon for a in poston])
    postingoff = sum([a.jurnal.postingoff for a in poston])
    postingonoff = sum([a.jurnal.postingonoff for a in poston])
    if d > datetime.timedelta(1) :
        variables = RequestContext(request,{'kocab':kocab,'transaksi_jurnal':transaksi_jurnal,\
            'a':jurnal_list,'total_pencairan':sum ([a.kredit for a in jurnal_list]),\
            'setoran_bank_kas_gerai' :sum ([a.kredit for a in setoran_kas_gerai]) + sum ([a.kredit for a in setoran_bank_gerai]),\
            'pengembalian_bank_pusat_pjb' :sum ([a.debet for a in pengembalian_bank_pusat]) ,
            'pengembalian_bank' :sum ([a.kredit for a in pengembalian_bank]) + sum ([a.kredit for a in pengembalian_kas]),\
            'uang_muka':sum ([a.kredit for a in uang_muka_gerai]),'saldo_awal':saldo_awal_lates,
            #'saldo_awal': sum([a.saldo for a in s_awal]),
            'total_penerimaan':hitung_a,
            'total_pengeluaran': hitung_b ,
            'saldo_akhir': saldo_awal + int(hitung_a) - int(hitung_b),
            'saldo_keseluruhan': (saldo_awal + hitung_a - hitung_b) - sum ([a.kredit for a in pengembalian_bank_pusat]),             
            'pencairan':sum ([a.debet for a in pencairan_kasir]),\
            'pencairan_kasir_sisa':pencairan_kasir_sisa,\
            'saldo_awal_hari':sum ([a.debet for a in saldo_awal_hari]),\
            'saldo_uangmuka_hari':sum ([a.debet for a in saldo_uang_muka_hari]),\
            'total_pelunasan':tbl,\
            'total_pendapatan_lainnya':sum ([a.kredit for a in pndptn_lainnya]),'sekarang':datetime.date.today(),\
            'beban_listrik':(sum ([a.debet for a in tbl_beban])),\
            'total_rakp':sum ([a.kredit for a in rakp]), \
            'total_transaksi_jurnal': sum ([a.debet for a in transaksi_jurnal]),\
            'total_saldo' :  saldo_awal ,'ak_ulang':ak_ulang,
            #'penjualan': penjualan,
            'pengeluaran_gadai_ulang': pengeluaran_gadai_ulang,'pengembalian_kas_pusat':pengembalian_kas_pusat,\
            'pengembalian_bank_pusat':pengembalian_kas_pusat,\
            'saldo_yang_di_kirim':sum ([a.debet for a in saldo_yang_dikirim]), 'pengembalian_kas':pengembalian_kas,\
            't_kasir':pencairan_kasir,'tampil':saldo_awal,'postingon':postingon,'postingonoff':postingonoff,'postingoff':postingoff,
            'pengembalian_bank':pengembalian_bank,'setoran_kas_gerai':setoran_kas_gerai,
            'pengembalian_kenasabah':pengembalian_nasabah,
            'setoran_bank_gerai':setoran_bank_gerai,'cabang':kocab})
    if d <= datetime.timedelta(1) :
        variables = RequestContext(request,{'kocab':kocab,'transaksi_jurnal':transaksi_jurnal,\
            'a':jurnal_list,'total_pencairan':sum ([a.kredit for a in jurnal_list]),\
            'setoran_bank_kas_gerai' :sum ([a.kredit for a in setoran_kas_gerai]) + sum ([a.kredit for a in setoran_bank_gerai]),\
            'pengembalian_bank_pusat_pjb' :sum ([a.debet for a in pengembalian_bank_pusat]) ,
            'pengembalian_bank' :sum ([a.kredit for a in pengembalian_bank]) + sum ([a.kredit for a in pengembalian_kas]),\
            'uang_muka':sum ([a.kredit for a in uang_muka_gerai]),'saldo_awal':saldo_awal,
            #'saldo_awal': sum([a.saldo for a in s_awal]),
            'total_penerimaan':hitung_a,
            'total_pengeluaran': hitung_b ,
            'saldo_akhir': saldo_awal_lates + int(hitung_a) - int(hitung_b),
            'saldo_keseluruhan': (saldo_awal_lates + hitung_a - hitung_b) - sum ([a.kredit for a in pengembalian_bank_pusat]),  
             
            'pencairan':sum ([a.debet for a in pencairan_kasir]),\
            'pencairan_kasir_sisa':pencairan_kasir_sisa,\
            'saldo_awal_hari':sum ([a.debet for a in saldo_awal_hari]),\
            'saldo_uangmuka_hari':sum ([a.debet for a in saldo_uang_muka_hari]),\
            'total_pelunasan':tbl,\
            'total_pendapatan_lainnya':sum ([a.kredit for a in pndptn_lainnya]),'sekarang':datetime.date.today(),\
            'beban_listrik':(sum ([a.debet for a in tbl_beban])),\
            'total_rakp':sum ([a.kredit for a in rakp]), \
            'total_transaksi_jurnal': sum ([a.debet for a in transaksi_jurnal]),\
            'total_saldo' :  saldo_awal ,'ak_ulang':ak_ulang,
            #'penjualan': penjualan,
            'pengeluaran_gadai_ulang': pengeluaran_gadai_ulang,'pengembalian_kas_pusat':pengembalian_kas_pusat,\
            'pengembalian_bank_pusat':pengembalian_kas_pusat,\
            'saldo_yang_di_kirim':sum ([a.debet for a in saldo_yang_dikirim]), 'pengembalian_kas':pengembalian_kas,\
            't_kasir':pencairan_kasir,'tampil':saldo_awal,'postingon':postingon,'postingonoff':postingonoff,'postingoff':postingoff,
            'pengembalian_bank':pengembalian_bank,'setoran_kas_gerai':setoran_kas_gerai,
            'pengembalian_kenasabah':pengembalian_nasabah,
            'setoran_bank_gerai':setoran_bank_gerai,'cabang':kocab})      
    template='kasir/view/all_transaksi_kas_pusat.html'
    return render_to_response(template,variables)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def kembaligu(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    ag = AkadGadai.objects.filter(gerai__kode_cabang = cab)
    titip = TitipanAkadUlang.objects.filter(norek__in = ag).filter(status = 2)

    ttp =titip.count()
    total_titip = sum([a.nilai for a in titip])
    template = 'kasir/laporan/show_kembaligu.html'
    variable = RequestContext(request, {
        'ag': ag,'total_titip':total_titip,'titip':titip})
    return render_to_response(template,variable)

def tampil_pengembalian_gu(request, object_id):
    sekarang = datetime.date.today()
    kasir = AkadGadai.objects.get(id=object_id)
    titip = TitipanAkadUlang.objects.filter(norek = object_id).filter(status = 2)

    ttp =titip.count()
    nilai_titipan = sum([a.nilai for a in titip])
    form = PengambilanForm(initial={'nilai':int(nilai_titipan)})
    template = 'kasir/pengembaliangu.html'
    variable = RequestContext(request, {'kasir': kasir,'form':form,'titip':titip,'nilai_titipan':nilai_titipan,'ttp':ttp})
    return render_to_response(template,variable)

def input_pengembalian_gu(request, object_id):
    kasir = AkadGadai.objects.get(id=object_id)
    user = request.user
    appkembali = kasir.apptitipankeu
    d = decimal.Decimal
    titip = TitipanAkadUlang.objects.filter(norek=object_id).filter(status =2)
    sekarang = datetime.date.today()
    if request.method == 'POST':
        form= PengambilanForm(request.POST)
        if form.is_valid():
            nilai = form.cleaned_data['nilai']

            titip.update(status = '3')
            appkembali.tanggal_eksekusi = sekarang
            appkembali.nilai_eksekusi = nilai
            appkembali.save()

            jurnal_pengembalian_titipan_gu_kas(kasir, nilai, request.user)
            messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING LEBIH KAS TITIPAN 1 ###.')
            return HttpResponseRedirect('/')
        else:
            variables = RequestContext(request, {'form': form,'titip':titip,'kasir':kasir, 'nilai':nilai})
            return render_to_response('kasir/pengembaliangu.html', variables)

############# BBAARUUU Kasir
def tampil_app_keu_gu(request, object_id):
    sekarang = datetime.date.today()
    kasir = AkadGadai.objects.get(id=object_id)
    titip = TitipanAkadUlang.objects.filter(norek = object_id).filter(status = 2)
    ttp =titip.count()
    nilai_titipan = sum([a.nilai for a in titip])
    form = AppKeuGuForm(initial={'status':1,'nilai':int(nilai_titipan)})
    template = 'kasir/show_titip_gu_keu.html'
    variable = RequestContext(request, {'kasir': kasir,'form':form})
    return render_to_response(template,variable)

def app_keu_gu(request, object_id):    
    user = request.user
    sekarang = datetime.date.today()
    kasir = AkadGadai.objects.get(pk = object_id)
    titip = TitipanAkadUlang.objects.filter(norek = object_id).filter(status = 2)
    ttp =titip.count()
    nilai_titipan = sum([a.nilai for a in titip])
    if request.method == 'POST':
        form= AppKeuGuForm(request.POST)
        if form.is_valid():
            status_oto_gerai = form.cleaned_data['status_oto_gerai']
            nilai = form.cleaned_data['nilai']
            keu = AppTitipanKeu(titip_gu = kasir,tanggal_oto_gerai = sekarang, status_oto_gerai= status_oto_gerai, nilai = nilai_titipan)
            keu.save()
            messages.add_message(request, messages.INFO,'### Ororisasi Telah DI simpan ###.')
            return HttpResponseRedirect('/rreport/%s/kembali_gu/' % user.profile.gerai.kode_cabang)
        else:
            template = 'kasir/show_titip_gu_keu_pusat.html'
            variable = RequestContext(request, {'kasir': kasir,'form':form})
            return render_to_response(template,variable)
############# BBAARUUU APP KEUANGAN
def list_app_keu_gu(request):
    sekarang = datetime.date.today()
    kasir = AppTitipanKeu.objects.filter(status_oto_pusat = None)
    form = AppKeuGuForm(initial={'status':1})
    template = 'kasir/laporan/show_oto_titipan.html'
    variable = RequestContext(request, {'kasir': kasir,'form':form})
    return render_to_response(template,variable)

def oto_app_keu_gu(request, object_id):
    sekarang = datetime.date.today()
    kasir = AppTitipanKeu.objects.get(id=object_id)
    form = AppKeuPusatGuForm(initial={'status':1,'nilai':int(kasir.nilai)})
    template = 'kasir/show_titip_gu_keu_pusat.html'
    variable = RequestContext(request, {'kasir': kasir,'form':form})
    return render_to_response(template,variable)

def eksekusi_app_keu_gu(request, object_id):    
    user = request.user
    sekarang = datetime.date.today()
    kasir = AppTitipanKeu.objects.get(id = object_id)
    if request.method == 'POST':
        form= AppKeuPusatGuForm(request.POST)
        if form.is_valid():
            status_oto_pusat = form.cleaned_data['status_oto_pusat']
            note = form.cleaned_data['note']
            nilai = form.cleaned_data['nilai']

            kasir.status_oto_pusat = int(status_oto_pusat)
            kasir.tanggal_oto_pusat = sekarang
            kasir.note = note
            kasir.save()
            messages.add_message(request, messages.INFO,'### Ororisasi Telah DI simpan ###.')
            return HttpResponseRedirect('/kasirgerai/list_app_keu_gu/')

        else:
            template = 'kasir/show_titip_gu_keu_pusat.html'
            variable = RequestContext(request, {'kasir': kasir,'form':form})
            return render_to_response(template,variable)

def laporan_permintaan_titipan_gu(request):
    start_date = None
    end_date = None
    gerai = None
    form = FilterForm()
    plns = []
    if 'start_date' in request.GET and request.GET['start_date'] and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        gerai = request.GET['gerai']
        if gerai == '500':
            plns = []
            rekap = AppTitipanKeu.objects.filter(status_oto_gerai = 1).filter(tanggal_oto_gerai__range=(start_date,end_date))
            form = FilterForm()
            template = 'kasir/show_permintaan_titip_gu.html'
            variables = RequestContext(request, {'rekap': rekap ,'start_date':start_date,'end_date':end_date,'id_cabang':gerai,'form':form})
            return render_to_response(template, variables)
        else:            
            rekap = AppTitipanKeu.objects.filter(status_oto_gerai = 1).filter(tanggal_oto_gerai__range=(start_date,end_date)).filter(titip_gu__gerai__id = gerai)
            start_date = start_date
            end_date = end_date
            gerai = gerai
            template = 'kasir/show_permintaan_titip_gu.html'
            form = FilterForm()
            variables = RequestContext(request, {'rekap': rekap ,'start_date':start_date,'end_date':end_date,'id_cabang':gerai,'form':form})
            return render_to_response(template, variables)
    else:
        template= 'kasir/show_permintaan_titip_gu.html'
        form = FilterForm()
        variable = RequestContext(request,{'form':form})
        return render_to_response(template,variable)

def jurnal_pengembalian_titipan_gu_kas(kasir, nilai, user):
    D = decimal.Decimal
    bm = PengembalianTitipanGadaiUlangMapper.objects.get(item='1', cabang=user.profile.gerai)
    a_titipan = bm.coa_1
    a_kas = bm.coa_2
    sekarang = datetime.date.today()

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengembalian Kelebihan Titipan GU: NoRek: %s an: %s  ' % (kasir.norek(), kasir.agnasabah.nama),
        tgl_trans = sekarang,nobukti=kasir.norek(),object_id = kasir.id,kode_cabang = user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pengembalian_titipan_kelebihan_gu"), id_coa = a_kas,
        debet = 0,kredit = nilai,id_product = '4',status_jurnal ='2',tgl_trans = sekarang,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pengembalian_titipan_kelebihan_gu"), id_coa = a_titipan,
        debet = nilai,kredit = 0,id_product = '4',status_jurnal ='2',tgl_trans = sekarang,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

def jurnal_pengembalian_titipan_gu_bank(kasir, nilai, user):
    D = decimal.Decimal
    bm = PengembalianTitipanGadaiUlangMapper.objects.get(item='2', cabang=user.profile.gerai)
    a_titipan = bm.coa_1
    a_kas = bm.coa_2
    sekarang = datetime.date.today()

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengembalian Kelebihan Titipan GU: NoRek: %s an: %s  ' % (kasir.norek(), kasir.agnasabah.nama),
        tgl_trans = sekarang,nobukti=kasir.norek(),object_id = kasir.id,kode_cabang = user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pengembalian_titipan_kelebihan_gu"), id_coa = a_kas,
        kredit = 0,debet = nilai,id_product = '4',status_jurnal ='2',tgl_trans = sekarang,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pengembalian_titipan_kelebihan_gu"), id_coa = a_titipan,
        kredit = nilai,debet = 0,id_product = '4',status_jurnal ='2',tgl_trans = sekarang,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)


def slip_setoran_titipan_pelunasan(request, object_id):
    user = request.user
    pk = TitipanPelunasan.objects.get(id=object_id)
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s.pdf' % pk.norek
    c = canvas.Canvas(response, pagesize=(9.5*inch, 11*inch))
    c.setTitle("kwitansi %s" % pk.norek)
    atas = 1
    sekarang=datetime.datetime.now()
    h=sekarang.day
    m=sekarang.month
    y=sekarang.year
    if m+1 <= 12:
        b=m+1
        t=y
    else  :
        b=1
        t=y+1
        patokan=datetime.date(int(t),int(b),int(h))
        trk=p.tanggal
        dd=patokan.month-trk.month
        yy=patokan.year-trk.year


    header1=(4.25 *inch, (5.3 + 5.5) * inch)
    colom1 = (0.5*inch, (4.3 + 5.5) *inch)
            #ke kiri  ke atas ke bawah
    colom2 = (6.7*inch, (4.5 + 5.5) *inch)
    colom3 = (6.0*inch, (4.8 + 4.5) *inch)
    colom4 = (0.5*inch, (3.7 + 4.2) *inch)

    header2=(8.25 *inch, (2.75 + 2.5) * inch)    
    header3=(4.25 *inch, (2.8 + 2.65) * inch)        
    #header2=(4.25 *inch, (5.3 + 5.5) * inch)
    colom5 = (0.5*inch, (2.15 + 2.3) *inch)
    #ke kiri  ke atas ke bawah
    colom6 = (6.7*inch, (2.15 + 2.5) *inch)
    colom7 = (0.5*inch, (3.0 + 1.5) *inch)
    colom8 = (0.5*inch, (1.5 + 1.1) *inch)
    tb=terbilang(pk.nilai)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/logoksu_hitamputih.png'), 1.0*inch, (5.5 + 1.5) * inch, width=200.5/17.5*0.51*inch,height=120/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 0.5*inch, (4.85 + 5.5) * inch, width=30/17.5*0.51*inch,height=25/17.5*0.51*inch,mask=None)
    
    x,y = header1
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Courier-Bold", 14)
    c.drawString(5.8 * inch , y-0.35* inch, "SLIP SETORAN TITIPAN PELUNASAN")
    c.line( 5.8 * inch , y-0.39* inch , 9.3 * inch ,y-0.39* inch ) ; y -=y1
    c.setFont("Courier-Bold", 11)
    c.drawString(5.8 * inch , y-0.42*inch,"%s" % (pk.akad_gerai())); y -=y1    
    c.setFont("Courier-Bold", 16)
    c.drawString(x-2.8*inch, y+0.20*inch, "KSU RIZKY ABADI"); y -=y1
    c.setFont("Courier",8)
    c.drawString(x-2.8*inch, y+0.20*inch, "Badan Hukum No.518/BH.88-DISKOP/THN.2007 Tgl 27 Desember 2007"); y -=y1
    c.drawString(x-2.8*inch, y+0.20*inch, "Jln Cisaranten Kulon IV No.55 Bandung Tlp: 022-7808443"); y -=y1
    kb = str.upper(str(pk.akad_gerai()))
  
    c.setFont("Courier",8)
    # garis Paling atas
    c.line( x-3.75* inch , y+0.172* inch , 5.5 * inch ,y+0.172* inch) ; y -=y1
    #garis Paling Bawah
    c.line( x-3.75* inch , y-0.0* inch , 5.5 * inch ,y-0.0* inch) ; y -=y1
    #garis paling kiri
    c.line( x-3.75* inch , y+0.37* inch , x-3.75* inch ,y+0.1* inch) 
    #garis paling kanan
    c.line( 5.5 * inch , y+0.37* inch , 5.5 * inch ,y+0.1* inch)   
    

    ####KOLOM 2 Dua Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    ## Barcode
    c.setFont("Courier", 7)
    c.drawString(600, 785, "%s" % sekarang.strftime('[%-b][%Y]') )
    barcode = code128.Code128("%s" % pk.akad_norek())
    barcode.drawOn(c, 195*mm, 268*mm)
               
            
    c.setFont("Courier", 11)
    x,y = colom2
    y1 = 0.165 * inch
    c.setFont("Courier", 9)
    c.drawString(x, y, "No PK"); 
    c.drawString(x+1.2*inch, y, ": %s" % (pk.akad_norek())); y -=y1
    c.drawString(x, y, "Tgl Transaksi");
    c.drawString(x+1.2*inch, y, ": %s" % (pk.tanggal.strftime('%d %b %Y'))); y -=2*y1
    
    ####KOLOM 3 Tilu Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    c.setFont("Courier-Bold", 14)
               
            
    c.setFont("Courier", 11)
    x,y = colom3
    y1 = 0.165 * inch
    c.setFont("Courier-Bold", 9)
    ####AKHiR KOLOM 3 Tilu Coy

    ####KOLOM 1 hiji Coy
    x,y = colom1
    y1 = 0.165 * inch
    
    c.setFont("Courier", 11)
    c.drawString(x, y+0.0*inch, "KSU RIZKY ABADI sudah menerima," ); y -=2*y1
    c.drawString(x, y, "Titipan Setoran Pelunasan Jaminan" )
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s|%s|%s" % (pk.akad_merk_barang(),pk.akad_type_barang(),pk.akad_sn_barang()  )); y -=1*y1
    c.drawString(x, y, "Titipan Sebesar")
    c.drawString(x+3.1*inch, y,": Rp.")
    c.drawRightString(x+4.5*inch, y,"%s"% (number_format(pk.nilai))); y -=2*y1
    c.drawString(x, y, "Nomor Debitur")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s" % (pk.akad_nonas())); y -=1*y1
    c.drawString(x, y, "Nama")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s" % (pk.nama())); y -=y1
    c.drawString(x, y, "Alamat")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s, No. %s RT/RW %s/%s " % (pk.akad_alamat(), pk.akad_no_rumah(),pk.akad_rt(),pk.akad_rt())); y -=y1    
    c.drawString(x+3.3*inch, y,"Kel. %s, Kec. %s Kota/Kab %s/%s " % (pk.akad_kelurahan_ktp(), pk.akad_kecamatan_ktp(),pk.akad_kotamadya_ktp(),pk.akad_kabupaten_ktp())); y -=y1    
    c.drawString(x, y, "Jenis Pinjaman")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"Titipan Setoran Pelunasan Jaminan"); y -=1.5*y1    


    ####KOLOM 4 Opat Coy
    x,y = colom4
    y1 = 0.165 * inch

    c.setFont("Courier-Bold", 11)
    c.drawString(x,y,  " ## %s Rupiah ##"  % tb.title()); y -=10*y1
    
    # garis Paling atas
    c.line( x, y+1.8*inch , 9.0 * inch , y+1.8*inch )
    #garis Paling Bawah
    c.line( x, y+1.55*inch , 9.0 * inch , y+1.55*inch )
    #garis paling kiri
    c.line( x, y+1.8*inch , x , y+1.55*inch )
    #garis paling kanan
    c.line( 9.0 * inch, y+1.8*inch ,9.0 * inch , y+1.55*inch )
    
    c.setFont("Courier",11)
    c.drawString(x+6.9*inch, y+1.4*inch, "Bandung, %s" % sekarang.strftime('%d %b %Y') )
    c.drawString(x, y+1.2*inch, "Kasir Gerai,")
    c.drawString(x+6.9*inch, y+1.2*inch, "Debitur,") ; 
    #c.line(410, 488, 500, 488)
    c.drawString(x,y+0.3*inch, "%s"%(user.profile.gerai.nama_kasir))
    c.drawString(x+6.9*inch,y+0.3*inch,"%s"%(pk.nama())) 
    #c.line(550, 488, 650, 488)
    c.setFont("Courier",8)
    c.drawString(x, y, "*Kwitansi ini sah apabila telah di validasi di tanda tangan dan di stample*"); y -=y1
    c.drawString(x, y, " Lembar 1/3 Gerai, Asli "); y -=y1
    c.drawString(x-2.5 * inch, y," - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - " )

    #######BARUUUU 123
    tb=terbilang(pk.nilai)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/logoksu_hitamputih.png'), 1.0*inch, (0.2 + 1.5) * inch, width=200.5/17.5*0.51*inch,height=120/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 0.5*inch, (-0.5 + 5.5) * inch, width=30/17.5*0.51*inch,height=25/17.5*0.51*inch,mask=None)
    
    x,y = header3
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Courier-Bold", 14)
    c.drawString(5.8 * inch , y-0.35* inch, "SLIP SETORAN TITIPAN PELUNASAN")
    c.line( 5.8 * inch , y-0.39* inch , 9.3 * inch ,y-0.39* inch ) ; y -=y1
    c.setFont("Courier-Bold", 11)
    c.drawString(5.8 * inch , y-0.42*inch,"%s" % (pk.akad_gerai())); y -=y1    
    c.setFont("Courier-Bold", 16)
    c.drawString(x-2.8*inch, y+0.20*inch, "KSU RIZKY ABADI"); y -=y1
    c.setFont("Courier",8)
    c.drawString(x-2.8*inch, y+0.20*inch, "Badan Hukum No.518/BH.88-DISKOP/THN.2007 Tgl 27 Desember 2007"); y -=y1
    c.drawString(x-2.8*inch, y+0.20*inch, "Jln Cisaranten Kulon IV No.55 Bandung Tlp: 022-7808443"); y -=y1
    kb = str.upper(str(pk.akad_gerai()))
  
    c.setFont("Courier",8)
    # garis Paling atas
    c.line( x-3.75* inch , y+0.172* inch , 5.5 * inch ,y+0.172* inch) ; y -=y1
    #garis Paling Bawah
    c.line( x-3.75* inch , y-0.0* inch , 5.5 * inch ,y-0.0* inch) ; y -=y1
    #garis paling kiri
    c.line( x-3.75* inch , y+0.37* inch , x-3.75* inch ,y+0.1* inch) 
    #garis paling kanan
    c.line( 5.5 * inch , y+0.37* inch , 5.5 * inch ,y+0.1* inch)   
    

    ####KOLOM 2 Dua Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    ## Barcode
    c.setFont("Courier", 7)
    c.drawString(600, 400, "%s" % sekarang.strftime('[%-b][%Y]') )
    barcode = code128.Code128("%s" % pk.akad_norek())
    barcode.drawOn(c, 195*mm, 132*mm)
               
            
    c.setFont("Courier", 11)
    x,y = colom6
    y1 = 0.165 * inch
    c.setFont("Courier", 9)
    c.drawString(x, y, "No PK"); 
    c.drawString(x+1.2*inch, y, ": %s" % (pk.akad_norek())); y -=y1
    c.drawString(x, y, "Tgl Transaksi");
    c.drawString(x+1.2*inch, y, ": %s" % (pk.tanggal.strftime('%d %b %Y'))); y -=2*y1
    
    ####KOLOM 3 Tilu Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    c.setFont("Courier-Bold", 14)
               
            
    c.setFont("Courier", 11)
    x,y = colom3
    y1 = 0.165 * inch
    c.setFont("Courier-Bold", 9)
    ####AKHiR KOLOM 3 Tilu Coy

    ####KOLOM 1 hiji Coy
    x,y = colom7
    y1 = 0.165 * inch
    
    c.setFont("Courier", 11)
    c.drawString(x, y+0.0*inch, "KSU RIZKY ABADI sudah menerima," ); y -=2*y1
    c.drawString(x, y, "Titipan Setoran Pelunasan Jaminan" )
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s|%s|%s" % (pk.akad_merk_barang(),pk.akad_type_barang(),pk.akad_sn_barang()  )); y -=1*y1
    c.drawString(x, y, "Titipan Sebesar")
    c.drawString(x+3.1*inch, y,": Rp.")
    c.drawRightString(x+4.5*inch, y,"%s"% (number_format(pk.nilai))); y -=2*y1
    c.drawString(x, y, "Nomor Debitur")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s" % (pk.akad_nonas())); y -=1*y1
    c.drawString(x, y, "Nama")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s" % (pk.nama())); y -=y1
    c.drawString(x, y, "Alamat")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s, No. %s RT/RW %s/%s " % (pk.akad_alamat(), pk.akad_no_rumah(),pk.akad_rt(),pk.akad_rt())); y -=y1    
    c.drawString(x+3.3*inch, y,"Kel. %s, Kec. %s Kota/Kab %s/%s " % (pk.akad_kelurahan_ktp(), pk.akad_kecamatan_ktp(),pk.akad_kotamadya_ktp(),pk.akad_kabupaten_ktp())); y -=y1    
    c.drawString(x, y, "Jenis Pinjaman")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"Titipan Setoran Pelunasan Jaminan"); y -=1.5*y1    


    ####KOLOM 4 Opat Coy
    x,y = colom8
    y1 = 0.165 * inch

    c.setFont("Courier-Bold", 11)
    c.drawString(x,y,  " ## %s Rupiah ##"  % tb.title()); y -=10*y1
    
    # garis Paling atas
    c.line( x, y+1.8*inch , 9.0 * inch , y+1.8*inch )
    #garis Paling Bawah
    c.line( x, y+1.55*inch , 9.0 * inch , y+1.55*inch )
    #garis paling kiri
    c.line( x, y+1.8*inch , x , y+1.55*inch )
    #garis paling kanan
    c.line( 9.0 * inch, y+1.8*inch ,9.0 * inch , y+1.55*inch )
    
    c.setFont("Courier",11)
    c.drawString(x+6.9*inch, y+1.4*inch, "Bandung, %s" % sekarang.strftime('%d %b %Y') )
    c.drawString(x, y+1.2*inch, "Kasir Gerai,")
    c.drawString(x+6.9*inch, y+1.2*inch, "Debitur,") ; 
    #c.line(410, 488, 500, 488)
    c.drawString(x,y+0.3*inch, "%s"%(user.profile.gerai.nama_kasir))
    c.drawString(x+6.9*inch,y+0.3*inch,"%s"%(pk.nama())) 
    #c.line(550, 488, 650, 488)
    c.setFont("Courier",8)
    c.drawString(x, y, "*Kwitansi ini sah apabila telah di validasi di tanda tangan dan di stample*"); y -=y1
    c.drawString(x, y, " Lembar 2/3 Pusat, Copy "); y -=y1

    c.showPage()
    c.save()


#################################################################    
    header1=(4.25 *inch, (5.3 + 5.5) * inch)
    colom1 = (0.5*inch, (4.3 + 5.5) *inch)
            #ke kiri  ke atas ke bawah
    colom2 = (6.7*inch, (4.5 + 5.5) *inch)
    colom3 = (6.0*inch, (4.8 + 4.5) *inch)
    colom4 = (0.5*inch, (3.7 + 4.2) *inch)

    header2=(8.25 *inch, (2.75 + 2.5) * inch)    
    header3=(4.25 *inch, (2.8 + 2.65) * inch)        
    #header2=(4.25 *inch, (5.3 + 5.5) * inch)
    colom5 = (0.5*inch, (2.15 + 2.3) *inch)
            #ke kiri  ke atas ke bawah
    colom6 = (6.7*inch, (2.15 + 2.3) *inch)
    colom7 = (0.5*inch, (3.0 + 1.5) *inch)
    colom8 = (0.5*inch, (1.5 + 1.1) *inch)
    tb=terbilang(pk.nilai)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/logoksu_hitamputih.png'), 1.0*inch, (5.5 + 1.5) * inch, width=200.5/17.5*0.51*inch,height=120/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 0.5*inch, (4.85 + 5.5) * inch, width=30/17.5*0.51*inch,height=25/17.5*0.51*inch,mask=None)
    
    x,y = header1
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Courier-Bold", 14)
    c.drawString(5.8 * inch , y-0.35* inch, "SLIP SETORAN TITIPAN PELUNASAN")
    c.line( 5.8 * inch , y-0.39* inch , 9.3 * inch ,y-0.39* inch ) ; y -=y1
    c.setFont("Courier-Bold", 11)
    c.drawString(5.8 * inch , y-0.42*inch,"%s" % (pk.akad_gerai())); y -=y1    
    c.setFont("Courier-Bold", 16)
    c.drawString(x-2.8*inch, y+0.20*inch, "KSU RIZKY ABADI"); y -=y1
    c.setFont("Courier",8)
    c.drawString(x-2.8*inch, y+0.20*inch, "Badan Hukum No.518/BH.88-DISKOP/THN.2007 Tgl 27 Desember 2007"); y -=y1
    c.drawString(x-2.8*inch, y+0.20*inch, "Jln Cisaranten Kulon IV No.55 Bandung Tlp: 022-7808443"); y -=y1
    kb = str.upper(str(pk.akad_gerai()))
  
    c.setFont("Courier",8)
    # garis Paling atas
    c.line( x-3.75* inch , y+0.172* inch , 5.5 * inch ,y+0.172* inch) ; y -=y1
    #garis Paling Bawah
    c.line( x-3.75* inch , y-0.0* inch , 5.5 * inch ,y-0.0* inch) ; y -=y1
    #garis paling kiri
    c.line( x-3.75* inch , y+0.37* inch , x-3.75* inch ,y+0.1* inch) 
    #garis paling kanan
    c.line( 5.5 * inch , y+0.37* inch , 5.5 * inch ,y+0.1* inch)   
    

    ####KOLOM 2 Dua Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    ## Barcode
    c.setFont("Courier", 7)
    c.drawString(600, 785, "%s" % sekarang.strftime('[%-b][%Y]') )
    barcode = code128.Code128("%s" % pk.akad_norek())
    barcode.drawOn(c, 195*mm, 268*mm)
               
            
    c.setFont("Courier", 11)
    x,y = colom2
    y1 = 0.165 * inch
    c.setFont("Courier", 9)
    c.drawString(x, y, "No PK"); 
    c.drawString(x+1.2*inch, y, ": %s" % (pk.akad_norek())); y -=y1
    c.drawString(x, y, "Tgl Transaksi");
    c.drawString(x+1.2*inch, y, ": %s" % (pk.tanggal.strftime('%d %b %Y'))); y -=2*y1
    
    ####KOLOM 3 Tilu Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    c.setFont("Courier-Bold", 14)
               
            
    c.setFont("Courier", 11)
    x,y = colom3
    y1 = 0.165 * inch
    c.setFont("Courier-Bold", 9)
    ####AKHiR KOLOM 3 Tilu Coy

    ####KOLOM 1 hiji Coy
    x,y = colom1
    y1 = 0.165 * inch
    
    c.setFont("Courier", 11)
    c.drawString(x, y+0.0*inch, "KSU RIZKY ABADI sudah menerima," ); y -=2*y1
    c.drawString(x, y, "Titipan Setoran Pelunasan Jaminan" )
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s|%s|%s" % (pk.akad_merk_barang(),pk.akad_type_barang(),pk.akad_sn_barang()  )); y -=1*y1
    c.drawString(x, y, "Titipan Sebesar")
    c.drawString(x+3.1*inch, y,": Rp.")
    c.drawRightString(x+4.5*inch, y,"%s"% (number_format(pk.nilai))); y -=2*y1
    c.drawString(x, y, "Nomor Debitur")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s" % (pk.akad_nonas())); y -=1*y1
    c.drawString(x, y, "Nama")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s" % (pk.nama())); y -=y1
    c.drawString(x, y, "Alamat")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s, No. %s RT/RW %s/%s " % (pk.akad_alamat(), pk.akad_no_rumah(),pk.akad_rt(),pk.akad_rt())); y -=y1    
    c.drawString(x+3.3*inch, y,"Kel. %s, Kec. %s Kota/Kab %s/%s " % (pk.akad_kelurahan_ktp(), pk.akad_kecamatan_ktp(),pk.akad_kotamadya_ktp(),pk.akad_kabupaten_ktp())); y -=y1    
    c.drawString(x, y, "Jenis Pinjaman")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"Titipan Setoran Pelunasan Jaminan"); y -=1.5*y1    


    ####KOLOM 4 Opat Coy
    x,y = colom4
    y1 = 0.165 * inch

    c.setFont("Courier-Bold", 11)
    c.drawString(x,y,  " ## %s Rupiah ##"  % tb.title()); y -=10*y1
    
    # garis Paling atas
    c.line( x, y+1.8*inch , 9.0 * inch , y+1.8*inch )
    #garis Paling Bawah
    c.line( x, y+1.55*inch , 9.0 * inch , y+1.55*inch )
    #garis paling kiri
    c.line( x, y+1.8*inch , x , y+1.55*inch )
    #garis paling kanan
    c.line( 9.0 * inch, y+1.8*inch ,9.0 * inch , y+1.55*inch )
    
    c.setFont("Courier",11)
    c.drawString(x+6.9*inch, y+1.4*inch, "Bandung, %s" % sekarang.strftime('%d %b %Y') )
    c.drawString(x, y+1.2*inch, "Kasir Gerai,")
    c.drawString(x+6.9*inch, y+1.2*inch, "Debitur,") ; 
    #c.line(410, 488, 500, 488)
    c.drawString(x,y+0.3*inch, "%s"%(user.profile.gerai.nama_kasir))
    c.drawString(x+6.9*inch,y+0.3*inch,"%s"%(pk.nama())) 
    #c.line(550, 488, 650, 488)
    c.setFont("Courier",8)
    c.drawString(x, y, "*Kwitansi ini sah apabila telah di validasi di tanda tangan dan di stample*"); y -=y1
    c.drawString(x, y, " Lembar 3/3 Nasabah, Copy "); y -=y1
    c.drawString(x-2.5 * inch, y," - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - " )
    c.showPage()
    c.save()
    return response

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def data_titipan_pelunasan(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    sekarang = datetime.date.today()
    akad = AkadGadai.objects.all()
    titip = TitipanPelunasan.objects.filter(status = 2,tanggal = sekarang, gerai = user.profile.gerai).filter(norek__in = akad)
    ttp =titip.count()
    total_titip = sum([a.nilai for a in titip])
    template = 'kasir/laporan/show_titipan.html'
    variable = RequestContext(request, {
        'skr':sekarang,'total_titip':total_titip,'titip':titip})
    return render_to_response(template,variable)


def show_kembali(request, object_id):
    sekarang = datetime.date(2016, 9, 3)
    ag = AkadGadai.objects.filter(status_transaksi =1).filter(gerai__kode_cabang = object_id).filter(lunas = sekarang)
    titip = TitipanPelunasan.objects.filter(status = 3)

    ttp =titip.count()
    total_titip = sum([a.nilai for a in titip])
    template = 'kasir/laporan/show_kembali.html'
    variable = RequestContext(request, {
        'ag': ag,'skr':sekarang,'total_titip':total_titip,'titip':titip})
    return render_to_response(template,variable)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def cari(request):
    akad = AkadGadai.objects.all()
    template='kasir/laporan/cari_kembali.html'
    variable = RequestContext(request,{'akad': akad})
    return render_to_response(template,variable)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def carikembalian(request):
    rekening=request.GET['rekening']
    barcode = rekening[11:]
    try:
        akad=AkadGadai.objects.get(id=int(barcode))
        return HttpResponseRedirect("/kasirgerai/%s/pengembalian/" % akad.id)
    except:
        messages.add_message(request, messages.INFO,'No rekening tidak ditemukan.')
        return HttpResponseRedirect("/kasir/cari/")

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def pengembalian(request, object_id):
    sekarang = datetime.date.today()
    kasir = AkadGadai.objects.get(id=object_id)
    titip = TitipanPelunasan.objects.filter(norek = object_id).filter(status = 2)

    ttp =titip.count()
    nilai_titipan = sum([a.nilai for a in titip])
    form = PengambilanForm(initial={'nilai':int(nilai_titipan)})
    template = 'kasir/pengembalian.html'
    variable = RequestContext(request, {'kasir': kasir,'form':form,'titip':titip,'nilai_titipan':nilai_titipan,'ttp':ttp})
    return render_to_response(template,variable)

def input_pengembalian(request, object_id):
    kasir = AkadGadai.objects.get(id=object_id)
    user = request.user
    d = decimal.Decimal
    titip = TitipanPelunasan.objects.filter(norek=object_id).filter(status =2)
    
    if request.method == 'POST':
        form= PengambilanForm(request.POST)
        if form.is_valid():
            nilai = form.cleaned_data['nilai']
            #jenis_pengambilan = form.cleaned_data['jenis_pengambilan']

            titip.update(status = '3')
            #if nilai > 0 and kasir.gerai == user.profile.gerai and jenis_pengambilan == '1' :
            jurnal_pengembalian_titipan_kas(kasir, nilai, request.user)
            messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING LEBIH KAS TITIPAN 1 ###.')
            #elif nilai > 0 and kasir.gerai == user.profile.gerai and jenis_pengambilan == '2' :
                #jurnal_pengembalian_titipan_bank(kasir, nilai, request.user)
                #messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING LEBIH BANK TITIPAN 2 ###.')
            messages.add_message(request, messages.INFO, 'Pengembalian Titipan OK')
            return HttpResponseRedirect('/')
        else:
            variables = RequestContext(request, {'form': form,'titip':titip,'kasir':kasir, 'nilai':nilai})
            return render_to_response('kasir/pengembalian.html', variables) 

def jurnal_pengembalian_titipan_kas(kasir, nilai, user):
    D = decimal.Decimal
    bm = PengembalianTitipanMapper.objects.get(item='1', cabang=user.profile.gerai)
    a_titipan = bm.coa_1
    a_kas = bm.coa_2
    sekarang = datetime.date.today()

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengembalian Kelebihan Titipan: NoRek: %s an: %s  ' % (kasir.norek(), kasir.agnasabah.nama),
        tgl_trans = sekarang,nobukti=kasir.norek(),object_id = kasir.id,kode_cabang = user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pengembalian_titipan_kelebihan"), id_coa = a_titipan,
        kredit = 0,debet = nilai,id_product = '4',status_jurnal ='2',tgl_trans = sekarang,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pengembalian_titipan_kelebihan"), id_coa = a_kas,
        kredit = nilai,debet = 0,id_product = '4',status_jurnal ='2',tgl_trans = sekarang,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

def jurnal_pengembalian_titipan_bank(kasir, nilai, user):
    D = decimal.Decimal
    bm = PengembalianTitipanMapper.objects.get(item='2', cabang=user.profile.gerai)
    a_titipan = bm.coa_1
    a_kas = bm.coa_2
    sekarang = datetime.date.today()

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengembalian Kelebihan Titipan: NoRek: %s an: %s  ' % (kasir.norek(), kasir.agnasabah.nama),
        tgl_trans = sekarang,nobukti=kasir.norek(),object_id = kasir.id,kode_cabang = user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pengembalian_titipan_kelebihan"), id_coa = a_kas,
        kredit = 0,debet = nilai,id_product = '4',status_jurnal ='2',tgl_trans = sekarang,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pengembalian_titipan_kelebihan"), id_coa = a_titipan,
        kredit = nilai,debet = 0,id_product = '4',status_jurnal ='2',tgl_trans = sekarang,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='ADM_GERAI'))
def mastertiket_ayda_gerai(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    cabang = Tbl_Cabang.objects.get(kode_cabang=cab)
    sekarang = datetime.date.today()
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang,id_cabang=cab,status_jurnal=u'2',jenis='PENJUALAN_AYDA_CABANG')
    return render(request,'kasir/tiket/mastertiket_ayda_gerai.html', {'cabang':cabang,'user':user,'g':gr,
        'total_debet': sum([p.debet for p in gr]),'total_kredit': sum([p.kredit for p in gr])})


def denominasi(request,object_id):
    sekarang = datetime.date.today()
    den = Denominasi.objects.filter(gerai=object_id)
    den.delete()
    gr = Tbl_Cabang.objects.filter(kode_cabang=object_id)
    cabang = Tbl_Cabang.objects.get(kode_cabang=object_id)
    user = request.user
    D = decimal.Decimal
    if request.method == "POST":
        form = DenominasiForm(request.POST,request.FILES)
        if form.is_valid():
            kertas_seratusribu = form.cleaned_data['kertas_seratusribu']
            kertas_limapuluhribu = form.cleaned_data['kertas_limapuluhribu']
            kertas_duapuluhribu = form.cleaned_data['kertas_duapuluhribu']
            kertas_sepuluhribu = form.cleaned_data['kertas_sepuluhribu']
            kertas_limaribu = form.cleaned_data['kertas_limaribu']
            kertas_duaribu = form.cleaned_data['kertas_duaribu']
            kertas_seribu = form.cleaned_data['kertas_seribu']
            koin_seribu = form.cleaned_data['koin_seribu']
            koin_limaratus = form.cleaned_data['koin_limaratus']
            koin_duaratus = form.cleaned_data['koin_duaratus']
            koin_seratus = form.cleaned_data['koin_seratus']
            koin_limapuluh = form.cleaned_data['koin_limapuluh']
            koin_dualima = form.cleaned_data['koin_dualima']
            gerai = form.cleaned_data['gerai']
            tanggal = form.cleaned_data['tanggal']
            
            denok = Denominasi(gerai = user.profile.gerai.kode_cabang,tanggal = sekarang,kertas_seratusribu = kertas_seratusribu,kertas_limapuluhribu = kertas_limapuluhribu,
                kertas_duapuluhribu = kertas_duapuluhribu,kertas_sepuluhribu = kertas_sepuluhribu,kertas_limaribu = kertas_limaribu,
                kertas_duaribu = kertas_duaribu,kertas_seribu = kertas_seribu,koin_seribu = koin_seribu,koin_limaratus = koin_limaratus,
                koin_duaratus = koin_duaratus,koin_seratus = koin_seratus,koin_limapuluh = koin_limapuluh,koin_dualima = koin_dualima,
                jumlah_kertas_seratusribu = kertas_seratusribu * int(100000),
                jumlah_kertas_limapuluhribu = kertas_limapuluhribu * int(50000),
                jumlah_kertas_duapuluhribu = kertas_duapuluhribu * int(20000),
                jumlah_kertas_sepuluhribu = kertas_sepuluhribu * int(10000),
                jumlah_kertas_limaribu = kertas_limaribu * int(5000),
                jumlah_kertas_duaribu = kertas_duaribu * int(2000),
                jumlah_kertas_seribu = kertas_seribu * int(1000),
                jumlah_koin_seribu = koin_seribu * int(1000),
                jumlah_koin_limaratus = koin_limaratus * int(500),
                jumlah_koin_duaratus = koin_duaratus * int(200),
                jumlah_koin_seratus = koin_seratus * int(100),
                jumlah_koin_limapuluh = koin_limapuluh * int(50),
                jumlah_koin_dualima = koin_dualima * int(25),
                )
            denok.save()
            messages.add_message(request, messages.INFO, 'Denominasi Telah tersimpan')
            return HttpResponseRedirect('/')
    else:
        form  = DenominasiForm() 
    variables = RequestContext(request, {'form': form,'gerai':gr,'cabang':cabang})
    return render_to_response('kasir/inputdenominasi.html', variables)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def mastertiket_gabungan_kasir(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    sekarang = datetime.date.today()
    kocab = Tbl_Cabang.objects.get(kode_cabang=cab)
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=cab).filter(status_jurnal=u'2').\
        filter(jenis__in=('Pencairan_kasir','Pencairan_kasir_sisa','Pencairan_kasir_kurang','Pencairan_kasir_bank',\
            'Pencairan_kasir_lebih_bank','Pencairan_kasir_kurang_bank_kecil','Pencairan_kasir_kurang_bank',u'Pelunasan_kasir',\
            u'Pelunasan_kasir_kurang',u'Pelunasan_kasir_bank','Pelunasan_kasir_bank_bol','Pelunasan_kasir_kurang_rak',\
            'GL_GL_PUSAT','GL_GL_NON_KAS','GL_GL_CABANG','GL_GL_PUSAT_UK','GL_GL_CABANG_UK','GL_GL_PENGEMBALIAN_UK',\
            'GL_GL_PENAMBAHAN_KAS','GL_GL_PENGELUARAN_KAS_PUSAT','GL_GL_PENAMBAHAN_GERAI','GL_GL_PENAMBAHAN_BANK',\
            'GL_GL_RAK_CABANG ','GL_GL_PENAMBAHAN_BANK_RAK','GL_GL_PENGELUARAN_BANK_RAK','GL_GL_PENGEMBALIAN_PUSAT_BANK_RAK',\
            'PENGELUARAN_KE_GERAI','GL_GL_PENGELUARAN_BANK','GL_GL_PENGELUARAN_BANK_PUSAT','GL_GL_PENGELUARAN_KAS',\
            'GL_GL_PENGEMBALIAN_PUSAT','GL_GL_PENGEMBALIAN_PUSAT_BANK',u'Pelunasan_kasir_rak','GL_GL_RAK_PUSAT_CABANG',\
            u'Pelunasan_kasir_bank_rak',u'Penjualan_lelang_kasir',u'Penjualan_lelang_kasir_bank','GL_GL_CABANG_REVISI',\
            u'Pelunasan_gu_kasir_nilai_sblm_kurang_bol',u'Pelunasan_gu_kasir_nilai_sblm_lebih_pol',u'Pelunasan_Gadai_Ulang_kasir',\
            u'Pelunasan_Gadai_Ulang_kasir_nilai_pinjaman_lebih',u'Pelunasan_gu_kasir_nilai_sblm_lebih',\
            u'Pelunasan_gu_kasir_nilai_sblm_kurang',u'Pelunasan_Gadai_Ulang_kasir_pinjaman_besar_tp',\
            u'Pelunasan_Gadai_Ulang_kasir_pinjaman_besar',u'Pelunasan_gu_kasir_nilai_sblm_lebih_tp',\
            u'Pelunasan_gu_kasir_nilai_sblm_lebih_bl',u'Pelunasan_gu_kasir_nilai_sblm_lebih',\
            u'Pelunasan_gu_kasir_nilai_sblm_kurang_kas',u'Pelunasan_gu_kasir_nilai_sblm_kurang_pdl',u'Pelunasan_Gadai_Ulang_kasir_bank',\
            u'Pelunasan_gu_bank_nilai_sblm_lebih',u'Pelunasan_gu_bank_nilai_sblm_lebih_pol','Pelunasan_gu_kasir_nilai_sblm_kurang_bank',\
            'Pelunasan_gu_kasir_nilai_sblm_kurang_bol_bank','Pelunasan_gu_kasir_nilai_sblm_lebih_bank_10_bol',\
            'Pelunasan_gu_kasir_nilai_sblm_kurang_bank_bol','Pelunasan_gu_kasir_nilai_sblm_lebih_bank_10',\
            'GL_GL_PENGEMBALIAN_SALDO_GERAI','GL_GL_PENGEMBALIAN_BANK_CABANG_RAK','Pencairan_kasir',\
            'Pencairan_kasir_sisa','Pencairan_kasir_kurang','Pencairan_kasir_bank','Pengembalian_titipan_kelebihan',\
            'Pengembalian_titipan_kelebihan_gu','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan',\
            'Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_pendapatan','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_pendapatan_lbh',\
            'Pencairan_kasir_lebih_bank','Pencairan_kasir_kurang_bank_kecil','Pencairan_kasir_kurang_bank','GL_GL_JUNAL_PENDAPATAN',\
            'Pendapatan1_Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan','Pendapatan_Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan','Pendapatan1_Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer','GL_GL_CABANG_ADM_BANK','GL_GL_JUNAL_KOREKSI'))
    template = 'kasir/tiket/mastertiket_gabungan_kasir.html'
    variables = RequestContext(request, {'kocab':kocab,'user':User,'g':gr,'total_debet': sum([p.debet for p in gr]),'total_kredit': sum([p.kredit for p in gr])})
    return render_to_response(template, variables)

def posting_akhir_hari(request, object_id):
    usr = request.user
    gerai_user =usr.profile.gerai

    sekarang = datetime.date.today()   

    cabang = Tbl_Cabang.objects.get(kode_cabang=object_id)
    jurnal = Tbl_Transaksi.objects.filter(id_cabang = cabang.kode_cabang).filter(status_jurnal = 2).filter(tgl_trans=datetime.date.today())
    jurnal.update(status_posting = 1,posting=1)

    PostingGerai.objects.create(status_posting = 1, kode_cabang = cabang.kode_cabang,gerai=cabang.nama_cabang, tanggal = sekarang,cu = usr, mu =usr)
    kunci = User.objects.filter(userprofile__gerai = gerai_user)
    usr.is_active = False
    usr.save()
    messages.add_message(request, messages.INFO, 'POSTING TRANSAKSI HARIAN TELAH BERHASIL DI LAKSANAKAN')
    logout(request)
    return HttpResponseRedirect('/')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def app_gu(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    sekarang = datetime.date.today()
    kocab = Tbl_Cabang.objects.get(kode_cabang=cab)
    gr = KasirGerai.objects.filter(status = 2).filter(kasir__gerai__kode_cabang=kocab.kode_cabang)
    template = 'kasir/laporan/gadai_ulang.html'
    variables = RequestContext(request, {'user':User,'gr':gr,'kocab':kocab})
    return render_to_response(template, variables)

def app(request,object_id):
    sekarang = datetime.date.today()
    D = decimal.Decimal
    nas = KasirGerai.objects.get(id=object_id)
    #kpl = AkadGadai.objects.get(id=object_id)
    
    form = Kasir_App_GU_Form(initial={'nilai':int(nas.kasir.nilai),'tanggal': sekarang,
    'nilai_terima_bersih':(int(nas.kasir.kewajiban_pelunasan) - int(nas.kasir.nilai))+ int(nas.kasir.jasa_kwitansi())\
     + (int(nas.kasir.beasimpan_all())) + int(nas.kasir.bea_materai)+ int(nas.kasir.adm_all()),
    'nilai_kewajiban_pelunasan':int(nas.kasir.kewajiban_pelunasan),
    'sisa_bayar':(int(nas.kasir.kewajiban_pelunasan) - int(nas.kasir.nilai)) + int(nas.kasir.jasa_kwitansi()) + (int(nas.kasir.beasimpan_all()))\
    + int(nas.kasir.bea_materai)+ int(nas.kasir.adm_all()),
    'nilai_dibayar':0,
    #'biaya_gu': int(nas.kasir.jasa_kwitansi()) + (int(nas.kasir.beasimpan_all())),
    'biaya_gu': int(nas.kasir.jasa_kwitansi()) + (int(nas.kasir.beasimpan_all())) + int(nas.kasir.bea_materai) + int(nas.kasir.adm_all()),
    })
    template = 'kplgerai/approve_pelunasan.html'
    variable = RequestContext(request, {'form':form,'nas':nas})
    return render_to_response(template,variable)

def verifikasi_kasir_gu(request, object_id):
    user = request.user
    nas = KasirGerai.objects.get(id=object_id)
    a = nas.kasir.agnasabah
    b = a.akadgadai_set.filter(status_transaksi=1).filter(barang__id = nas.kasir.barang.id)
    c = b.latest()
    d = c.pelunasan_terakhir()
    e = d.id
    if request.method == 'POST':
        form = Kasir_App_GU_Form(request.POST)
        if form.is_valid():
            #kasir = form.cleaned_data['kasir']
            nilai = form.cleaned_data['nilai']
            nilai_terima_bersih = form.cleaned_data['nilai_terima_bersih']
            nilai_pembulatan = form.cleaned_data['nilai_pembulatan']
            selisih  = form.cleaned_data['selisih']
            jenis_transaksi = form.cleaned_data['jenis_transaksi']
            tanggal = form.cleaned_data['tanggal']
            nilai_dibayar = form.cleaned_data['nilai_dibayar']
            sisa_bayar = form.cleaned_data['sisa_bayar']
            rek_tab = form.cleaned_data['rek_tab']
            kelebihan_transfer = form.cleaned_data['kelebihan_transfer']
            kelebihan = form.cleaned_data['kelebihan']
            nas.status = 1
            nas.jenis_transaksi = jenis_transaksi
            nas.nilai_pembulatan_lunas = nilai_pembulatan
            nas.sisa_bayar_lunas = sisa_bayar
            nas.tanggal_lunas = tanggal
            nas.selisih_lunas = selisih
            nas.jenis_transaksi_lunas = jenis_transaksi
            nas.kasir_lunas_id = e
            nas.rek_tab = rek_tab
            nas.save()
            ## TRANSAKSI MELALUI KAS
            ### UNTUK MEMBUAT JURNAL GU JAKARTA DENGAN KONDIS TRANSAKSI KAS,PINJAMAN SEBELUM <= NILAI GU


            if nas.kasir.nilai <= nas.kasir.nilai_gu and kelebihan > 0 and kelebihan_transfer > 0 and nas.jenis_transaksi_lunas == u'2' and nas.selisih_lunas > 0 and nas.kasir.gerai == user.profile.gerai:
                jurnal_bank_akad_ulang_kelebihan_transfer_pendapatan(nas,kelebihan,kelebihan_transfer, request.user)
                if kelebihan_transfer > 0 :
                    lebih = TitipanAkadUlang(norek = nas.kasir.id,gerai = nas.kasir.gerai,nilai=kelebihan_transfer,status = 2,\
                        tanggal=tanggal,cu=user,mu=user)
                    lebih.save()
                messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING LEBIH BANK TITIPAN 749 ###.')
            ### udah fix
            if nas.kasir.nilai <= nas.kasir.nilai_gu and kelebihan == 0 and kelebihan_transfer > 0 and nas.jenis_transaksi_lunas == u'2' and nas.selisih_lunas > 0 and nas.kasir.gerai == user.profile.gerai:
                jurnal_bank_akad_ulang_kelebihan_transfer(nas,kelebihan,kelebihan_transfer, request.user)
                if kelebihan_transfer > 0 :
                    lebih = TitipanAkadUlang(norek = nas.kasir.id,gerai = nas.kasir.gerai,nilai=kelebihan_transfer,status = 2,\
                        tanggal=tanggal,cu=user,mu=user)
                    lebih.save()
                messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING LEBIH BANK TITIPAN 757###.')
            #cek lagi
            if nas.kasir.nilai <= nas.kasir.nilai_gu and kelebihan > 0 and kelebihan_transfer == 0 and nas.jenis_transaksi_lunas == u'2' and nas.selisih_lunas > 0 and nas.kasir.gerai == user.profile.gerai:
                jurnal_bank_akad_ulang_pendapatan(nas,kelebihan,kelebihan_transfer, request.user)
                if kelebihan_transfer > 0 :
                    lebih = TitipanAkadUlang(norek = nas.kasir.id,gerai = nas.kasir.gerai,nilai=kelebihan_transfer,status = 2,\
                        tanggal=tanggal,cu=user,mu=user)
                    lebih.save()
                messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING LEBIH BANK TITIPAN 765 ###.')
            
            ###mapper
            if nas.jenis_transaksi_lunas == u'1' and nas.selisih_lunas > 0 and nas.kasir.nilai <= nas.kasir.nilai_gu:
                jurnal_kas_jkt_gu_nilai_lebih(nas, request.user)
                messages.add_message(request, messages.INFO,'### MAPPER JURNAL TELAH TERPOSTING LEBIH 1###.')
            elif nas.jenis_transaksi_lunas == u'1' and nas.selisih_lunas == 0 and nas.kasir.nilai <= nas.kasir.nilai_gu:
                jurnal_kas_jkt_gu_nilai_sama(nas, request.user)
                messages.add_message(request, messages.INFO,'### MAPPER PENGAJUAN BERHASIL 2 ###')   
            elif nas.jenis_transaksi_lunas == u'1' and nas.selisih_lunas < 0 and nas.kasir.nilai <= nas.kasir.nilai_gu:
                jurnal_kas_jkt_gu_nilai_kurang(nas, request.user)
                messages.add_message(request, messages.INFO,'### MAPPER JURNAL TELAH TERPOSTING JURNAL TITIPAN 3###.')
            ### UNTUK MEMBUAT JURNAL GU JAKARTA DENGAN KONDIS TRANSAKSI KAS,PINJAMAN SEBELUM <= NILAI GU
            elif nas.jenis_transaksi_lunas == u'1' and nas.selisih_lunas > 0 and nas.kasir.nilai > nas.kasir.nilai_gu:
                jurnal_kas_jkt_gu_nilai_lebih_pinjaman_lebih(nas, request.user)
                messages.add_message(request, messages.INFO,'### MAPPER JURNAL TELAH TERPOSTING LEBIH BESAR 4###.')
            elif nas.jenis_transaksi_lunas == u'1' and nas.selisih_lunas == 0 and nas.kasir.nilai > nas.kasir.nilai_gu:
                jurnal_kas_jkt_gu_nilai_sama_pinjaman_lebih(nas, request.user)
                messages.add_message(request, messages.INFO,'### MAPPER PENGAJUAN BERHASIL BESAR 5###')   
            elif nas.jenis_transaksi_lunas == u'1' and nas.selisih_lunas < 0 and nas.kasir.nilai > nas.kasir.nilai_gu:
                jurnal_kas_jkt_gu_nilai_kurang_pinjaman_lebih(nas, request.user)
                messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING JURNAL TITIPAN LEBIH 6 ###.')
            ## AKHIR TRANSAKSI MELALUI KAS
            elif nas.jenis_transaksi_lunas == u'2' and nas.selisih_lunas > 0 and nas.kasir.nilai <= nas.kasir.nilai_gu and kelebihan <= 0 and kelebihan_transfer <= 0:
                jurnal_bank_jkt_gu_nilai_lebih(nas, request.user)
                messages.add_message(request, messages.INFO,'### MAPPER JURNAL TELAH TERPOSTING LEBIH BANK 7 ###.')
            elif nas.jenis_transaksi_lunas == u'2' and nas.selisih_lunas == 0 and nas.kasir.nilai <= nas.kasir.nilai_gu and kelebihan <= 0 and kelebihan_transfer <= 0:
                jurnal_bank_jkt_gu_nilai_sama(nas, request.user)
                messages.add_message(request, messages.INFO,'### PENGAJUAN BANK BERHASIL  8 ###')   
            elif nas.jenis_transaksi_lunas == u'2' and nas.selisih_lunas < 0 and nas.kasir.nilai <= nas.kasir.nilai_gu and kelebihan <= 0 and kelebihan_transfer <= 0:
                jurnal_bank_jkt_gu_nilai_kurang(nas, request.user)
                messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING JURNAL TITIPAN BANK 9###.')
            ### UNTUK MEMBUAT JURNAL GU JAKARTA DENGAN KONDIS TRANSAKSI BANK,PINJAMAN SEBELUM <= NILAI GU
            elif nas.jenis_transaksi_lunas == u'2' and nas.selisih_lunas > 0 and nas.kasir.nilai > nas.kasir.nilai_gu:
                jurnal_bank_jkt_gu_nilai_lebih_pinjaman_lebih(nas, request.user)
                messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING LEBIH BANK 10###.')
            elif nas.jenis_transaksi_lunas == u'2' and nas.selisih_lunas == 0 and nas.kasir.nilai > nas.kasir.nilai_gu:
                jurnal_bank_jkt_gu_nilai_sama_pinjaman_lebih(nas, request.user)
                messages.add_message(request, messages.INFO,'### PENGAJUAN BERHASIL 11###')   
            elif nas.jenis_transaksi_lunas == u'2' and nas.selisih_lunas < 0 and nas.kasir.nilai > nas.kasir.nilai_gu:
                jurnal_bank_jkt_gu_nilai_kurang_pinjaman_lebih(nas, request.user)
                messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING JURNAL TITIPAN BANK 12###.')

           
            return HttpResponseRedirect('/')   
        else:
            messages.add_message(request, messages.INFO,'### PENGAJUAN GAGAL ###')
            return HttpResponseRedirect('/')  
    else:
        #return HttpResponseRedirect('/')
        form = Kasir_App_GU_Form()
    variables = RequestContext(request, {'form': form,'nas':nas})
    template = 'kplgerai/approve_pelunasan.html'
    return render_to_response(template, variables)

def jurnal_bank_akad_ulang_kelebihan_transfer_pendapatan(nas,kelebihan,kelebihan_transfer, user):
    D = decimal.Decimal
    bank = GadaiUlangMapper.objects.get(item ='jurnal_bank_gu_nilai_lebih_pendapatan_titipan',cabang = user.profile.gerai)
    a_titipan_pelunasan = bank.coa_titipan_pelunasan
    a_bank = bank.coa_kas
    a_pend_lainnya= bank.coa_pendapatan_lainnya
    a_kelebihan_pend= bank.coa_titipan_kelebihan

    jurnal = Jurnal.objects.create(
        diskripsi= 'Gadai Ulang: NoRek: %s an: %s  ' % (nas.kasir.norek(), nas.kasir.agnasabah.nama),
        tgl_trans =nas.tanggal,nobukti=nas.kasir.norek(),cu = user,mu =user,object_id = nas.id,
        kode_cabang =  user.profile.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        ##id_nilai_pembulatan##
        jenis = '%s' % ("Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan"), id_coa = a_bank,
        kredit = 0,debet = nas.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)


    jurnal.tbl_transaksi_set.create(
        ##id_sisa_bayar##
        jenis = '%s' % ("Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = nas.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = nas.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        #id_kelebihan_transfer
        jenis = '%s' % ("Pendapatan1_Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan"), id_coa = a_kelebihan_pend,
        debet = 0,kredit = (kelebihan_transfer),id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        ##id_kelebihan
        jenis = '%s' % ("Pendapatan_Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan"), id_coa = a_pend_lainnya,
        debet = 0,kredit = (kelebihan),id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
    
def jurnal_bank_akad_ulang_kelebihan_transfer(nas,kelebihan,kelebihan_transfer, user):
    D = decimal.Decimal
    bank = GadaiUlangMapper.objects.get(item ='jurnal_bank_gu_nilai_lebih_pendapatan_titipan',cabang = user.profile.gerai)
    a_titipan_pelunasan = bank.coa_titipan_pelunasan
    a_bank = bank.coa_kas
    a_pend_lainnya= bank.coa_pendapatan_lainnya
    a_kelebihan_pend= bank.coa_titipan_kelebihan

    jurnal = Jurnal.objects.create(
        diskripsi= 'Gadai Ulang: NoRek: %s an: %s  ' % (nas.kasir.norek(), nas.kasir.agnasabah.nama),
        tgl_trans =nas.tanggal,nobukti=nas.kasir.norek(),cu = user,mu =user,object_id = nas.id,
        kode_cabang =  user.profile.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        ##id_nilai_pembulatan##
        jenis = '%s' % ("Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer"), id_coa = a_bank,
        kredit = 0,debet = nas.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)


    jurnal.tbl_transaksi_set.create(
        ##id_sisa_bayar##
        jenis = '%s' % ("Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = nas.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = nas.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        #id_kelebihan_transfer
        jenis = '%s' % ("Pendapatan1_Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer"), id_coa = a_kelebihan_pend,
        debet = 0,kredit = (kelebihan_transfer),id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_akad_ulang_pendapatan(nas,kelebihan,kelebihan_transfer, user):
    D = decimal.Decimal
    bank = GadaiUlangMapper.objects.get(item ='jurnal_bank_gu_nilai_lebih_pendapatan_titipan',cabang = user.profile.gerai)
    a_titipan_pelunasan = bank.coa_titipan_pelunasan
    a_bank = bank.coa_kas
    a_pend_lainnya= bank.coa_pendapatan_lainnya
    a_kelebihan_pend= bank.coa_titipan_kelebihan

    jurnal = Jurnal.objects.create(
        diskripsi= 'Gadai Ulang: NoRek: %s an: %s  ' % (nas.kasir.norek(), nas.kasir.agnasabah.nama),
        tgl_trans =nas.tanggal,nobukti=nas.kasir.norek(),cu = user,mu =user,object_id = nas.id,
        kode_cabang =  user.profile.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        ##id_nilai_pembulatan##
        jenis = '%s' % ("Pelunasan_Gadai_ulang_kasir_bank_kelebihan_pendapatan"), id_coa = a_bank,
        kredit = 0,debet = nas.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)


    jurnal.tbl_transaksi_set.create(
        ##id_sisa_bayar##
        jenis = '%s' % ("Pelunasan_Gadai_ulang_kasir_bank_kelebihan_pendapatan"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = nas.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = nas.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        ##id_kelebihan
        jenis = '%s' % ("Pelunasan_Gadai_ulang_kasir_bank_kelebihan_pendapatan_lbh"), id_coa = a_pend_lainnya,
        debet = 0,kredit = (kelebihan),id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

## JURNAL TRANSAKSI MELALUI KAS
###jurnal gadai ulang (pinjaman sama dan lebih kecil,tanpa ada selisih dalam pembayaran) kas
####PENGAJUAN BERHASIL
def jurnal_kas_jkt_gu_nilai_sama(nas, user):
    D = decimal.Decimal
    bm = GadaiUlangMapper.objects.get(item='pinjaman_sama_bayar_sama', cabang=user.profile.gerai)
    a_titipan_pelunasan = bm.coa_titipan_pelunasan
    a_kas = bm.coa_kas
    #a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
    #a_kas = get_object_or_404(Tbl_Akun, id=7L)
    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (nas.kasir.norek(), nas.kasir.agnasabah.nama),
        tgl_trans =nas.tanggal,nobukti=nas.kasir.norek(),object_id = nas.id,kode_cabang = user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Gadai_Ulang_kasir"), id_coa = a_kas,
        kredit = 0,debet = nas.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Gadai_Ulang_kasir"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = nas.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = nas.tanggal_lunas,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

###jurnal gadai ulang (pinjaman sama dan lebih kecil, ada selisih lebih besar dalam pembayaran) kas    
#### JURNAL TELAH TERPOSTING LEBIH
def jurnal_kas_jkt_gu_nilai_lebih(nas, user):
    D = decimal.Decimal
    bm = GadaiUlangMapper.objects.get(item='pinjaman_sama_bayar_lebih', cabang=user.profile.gerai)
    a_titipan_pelunasan = bm.coa_titipan_pelunasan
    a_kas = bm.coa_kas
    a_pend_lainnya= bm.coa_pendapatan_lainnya

    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (nas.kasir.norek(), nas.kasir.agnasabah.nama),
        tgl_trans =nas.tanggal,nobukti=nas.kasir.norek(),cu =user,mu=user,object_id = nas.id,kode_cabang = user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_lebih"), id_coa = a_kas,
        kredit = 0,debet = (nas.nilai_pembulatan_lunas),id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_lebih_pol"), id_coa = a_pend_lainnya,
        debet = 0,kredit = (nas.selisih_lunas),id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_lebih"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = nas.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = nas.tanggal_lunas,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

###jurnal gadai ulang (pinjaman sama dan lebih kecil, ada selisih lebih kecil dalam pembayaran) kas    
####JURNAL TELAH TERPOSSTING JURNAL TITIPAN
def jurnal_kas_jkt_gu_nilai_kurang(nas, user):
    D = decimal.Decimal
    bm = GadaiUlangMapper.objects.get(item='pinjaman_sama_bayar_kurang', cabang=user.profile.gerai)
    a_titipan_pelunasan = bm.coa_titipan_pelunasan
    a_beban_lainnya = bm.coa_beban
    a_kas = bm.coa_kas

    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (nas.kasir.norek(), nas.kasir.agnasabah.nama),
        tgl_trans =nas.tanggal_lunas,nobukti=nas.kasir.norek(),cu =user,mu=user,object_id = nas.id,kode_cabang = user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_kurang"), id_coa = a_kas,
        kredit = 0,debet = nas.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_kurang_bol"), id_coa = a_beban_lainnya,
        debet = -1 * (nas.selisih_lunas),kredit = 0,id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_kurang"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = nas.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

###jurnal gadai ulang (pinjaman lebih Besar,tanpa ada selisih dalam pembayaran) kas
#### PENGAJUAN BERHASIL BESAR
def jurnal_kas_jkt_gu_nilai_sama_pinjaman_lebih(nas, user):
    D = decimal.Decimal
    bm = GadaiUlangMapper.objects.get(item='pinjaman_lebih_bayar_sama', cabang=user.profile.gerai)
    a_titipan_pencairan = bm.coa_titipan_pelunasan
    a_kas = bm.coa_kas
    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (nas.kasir.norek(), nas.kasir.agnasabah.nama),
        tgl_trans =nas.tanggal,nobukti=nas.kasir.norek(),cu =user,mu=user,object_id = nas.id,kode_cabang = user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Gadai_Ulang_kasir_pinjaman_besar_tp"), id_coa = a_titipan_pencairan,
        debet = nas.sisa_bayar_lunas,kredit = 0,id_product = '4',status_jurnal ='2',tgl_trans = nas.tanggal_lunas,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)    

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Gadai_Ulang_kasir_pinjaman_besar"), id_coa = a_kas,
        kredit = nas.nilai_pembulatan_lunas,debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)
    
###jurnal gadai ulang (pinjaman lebih Besar, ada selisih lebih besar dalam pembayaran) kas   
####jurnal telah terposting lebih besar 
def jurnal_kas_jkt_gu_nilai_lebih_pinjaman_lebih(nas, user):
    D = decimal.Decimal
    bm = GadaiUlangMapper.objects.get(item='pinjaman_lebih_bayar_lebih', cabang=user.profile.gerai)
    a_titipan_pencairan = bm.coa_titipan_pelunasan
    a_kas = bm.coa_kas
    a_beban_lainnya = bm.coa_beban
    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (nas.kasir.norek(), nas.kasir.agnasabah.nama),
        tgl_trans =nas.tanggal,nobukti=nas.kasir.norek(),cu =user,mu=user,object_id = nas.id,kode_cabang = user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_lebih_tp"), id_coa = a_titipan_pencairan,
        debet = nas.sisa_bayar_lunas,kredit = 0,id_product = '4',status_jurnal ='2',tgl_trans = nas.tanggal_lunas,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)  

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_lebih_bl"), id_coa = a_beban_lainnya,
        debet = 1 * (nas.selisih_lunas),kredit = 0,id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_lebih"), id_coa = a_kas,
        kredit = (nas.nilai_pembulatan_lunas),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

###jurnal gadai ulang (pinjaman lebih Besar, ada selisih lebih kecil dalam pembayaran) kas   
####JURNAL TELAH TERPOSTING JURNAL TITIPAN LEBIH 
def jurnal_kas_jkt_gu_nilai_kurang_pinjaman_lebih(nas, user):
    D = decimal.Decimal
    bm = GadaiUlangMapper.objects.get(item='pinjaman_lebih_bayar_kurang', cabang=user.profile.gerai)
    a_titipan_pencairan = bm.coa_titipan_pelunasan
    a_pend_lainnya= bm.coa_pendapatan_lainnya
    a_kas = bm.coa_kas

    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (nas.kasir.norek(), nas.kasir.agnasabah.nama),
        tgl_trans =nas.tanggal_lunas,nobukti=nas.kasir.norek(),cu =user,mu=user,object_id = nas.id,kode_cabang = user.profile.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_kurang"), id_coa = a_titipan_pencairan,
        debet = nas.sisa_bayar_lunas,kredit = 0,id_product = '4',status_jurnal ='2',tgl_trans = nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_kurang_pdl"), id_coa = a_pend_lainnya,
        debet = 0,kredit = -1 * (nas.selisih_lunas),id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_kurang_kas"), id_coa = a_kas,
        kredit = nas.nilai_pembulatan_lunas,debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang =nas.kasir.gerai.kode_cabang,id_unit= 300)
    
# AKHIR JURNAL TRANSAKSI MELALUI KAS      

## JURNAL TRANSAKSI MEMALULI BANK
###jurnal gadai ulang (pinjaman sama dan lebih kecil,tanpa ada selisih dalam pembayaran) kas
def jurnal_bank_jkt_gu_nilai_lebih(nas, user):
    D = decimal.Decimal
    bm = GadaiUlangMapper.objects.get(item='jurnal_bank_gu_nilai_lebih', cabang=user.profile.gerai)
    a_titipan_pelunasan = bm.coa_titipan_pelunasan
    a_kas = bm.coa_kas
    a_pend_lainnya= bm.coa_pendapatan_lainnya

    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (nas.kasir.norek(), nas.kasir.agnasabah.nama),
        tgl_trans =nas.tanggal,nobukti=nas.kasir.norek(),cu =user,mu=user,object_id = nas.id,kode_cabang = user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_bank_nilai_sblm_lebih"), id_coa = a_kas,
        kredit = 0,debet = (nas.nilai_pembulatan_lunas),id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_bank_nilai_sblm_lebih_pol"), id_coa = a_pend_lainnya,
        debet = 0,kredit = (nas.selisih_lunas),id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_bank_nilai_sblm_lebih"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = nas.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = nas.tanggal_lunas,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_jkt_gu_nilai_sama(nas, user):
    D = decimal.Decimal
    gu = GadaiUlangMapper.objects.get(item='jurnal_bank_gu_nilai_sama',cabang= user.profile.gerai)
    a_titipan_pelunasan = gu.coa_titipan_pelunasan
    a_bank = gu.coa_kas

    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (nas.kasir.norek(), nas.kasir.agnasabah.nama),
        tgl_trans =nas.tanggal,nobukti=nas.kasir.norek(),cu =user,mu=user,object_id = nas.id,kode_cabang = user.profile.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Gadai_Ulang_kasir_bank"), id_coa = a_bank,
        kredit = 0,debet = nas.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Gadai_Ulang_kasir_bank"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = nas.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = nas.tanggal_lunas,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

###jurnal gadai ulang (pinjaman lebih Besar,tanpa ada selisih dalam pembayaran) kas
def jurnal_bank_jkt_gu_nilai_sama_pinjaman_lebih(nas, user):
    D = decimal.Decimal
    gu = GadaiUlangMapper.objects.get(item= 'jurnal_bank_jkt_gu_nilai_sama_pinjaman_lebih',cabang=user.profile.gerai)
    a_titipan_pencairan = gu.coa_titipan_pelunasan
    a_bank = gu.coa_kas
    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (nas.kasir.norek(), nas.kasir.agnasabah.nama),
        tgl_trans =nas.tanggal,nobukti=nas.kasir.norek(),cu =user,mu=user,object_id = nas.id,kode_cabang = user.profile.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Gadai_Ulang_kasir_bank"), id_coa = a_titipan_pencairan,
        debet = nas.sisa_bayar_lunas,kredit = 0,id_product = '4',status_jurnal ='2',tgl_trans = nas.tanggal_lunas,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Gadai_Ulang_kasir_bank"), id_coa = a_bank,
        kredit = nas.nilai_pembulatan_lunas,debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

###jurnal gadai ulang (pinjaman lebih Besar, ada selisih lebih besar dalam pembayaran) kas    
def jurnal_bank_jkt_gu_nilai_lebih_pinjaman_lebih(nas, user):
    D = decimal.Decimal
    gu = GadaiUlangMapper.objects.get(item = 'jurnal_bank_jkt_gu_nilai_lebih_pinjaman_lebih',cabang=user.profile.gerai)
    a_titipan_pencairan = gu.coa_titipan_pelunasan
    a_bank = gu.coa_kas
    a_beban_lainnya = gu.coa_beban

    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (nas.kasir.norek(), nas.kasir.agnasabah.nama),
        tgl_trans =nas.tanggal,nobukti=nas.kasir.norek(),object_id = nas.id,kode_cabang = user.profile.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_lebih_bank_10"), id_coa = a_titipan_pencairan,
        debet = nas.sisa_bayar_lunas,kredit = 0,id_product = '4',status_jurnal ='2',tgl_trans = nas.tanggal_lunas,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_lebih_bank_10_bol"), id_coa = a_beban_lainnya,
        debet = (nas.selisih_lunas),kredit = 0,id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_lebih_bank_10"), id_coa = a_bank,
        kredit = (nas.nilai_pembulatan_lunas),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

###jurnal gadai ulang (pinjaman lebih Besar, ada selisih lebih kecil dalam pembayaran) kas    
def jurnal_bank_jkt_gu_nilai_kurang_pinjaman_lebih(nas, user):
    D = decimal.Decimal
    gu = GadaiUlangMapper.objects.get(item = 'jurnal_bank_jkt_gu_nilai_kurang_pinjaman_lebih',cabang=nas.kasir.gerai)
    a_titipan_pencairan = gu.coa_titipan_pelunasan
    a_pend_lainnya = gu.coa_pendapatan_lainnya
    a_bank = gu.coa_kas
    #a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    #a_pend_lainnya= get_object_or_404(Tbl_Akun, id = 448L)
    #a_bank = get_object_or_404(Tbl_Akun, id=133L)

    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (nas.kasir.norek(), nas.kasir.agnasabah.nama),
        tgl_trans =nas.tanggal_lunas,nobukti=nas.kasir.norek(),cu =user,mu=user,object_id = nas.id,kode_cabang = user.profile.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_kurang_bank"), id_coa = a_titipan_pencairan,
        debet = nas.sisa_bayar_lunas,kredit = 0,id_product = '4',status_jurnal ='2',tgl_trans = nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_kurang_bank_bol"), id_coa = a_pend_lainnya,
        debet = 0,kredit = -1 * (nas.selisih_lunas),id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_kurang_bank"), id_coa = a_bank,
        kredit = nas.nilai_pembulatan_lunas,debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_jkt_gu_nilai_kurang(nas, user):
    D = decimal.Decimal
    gu=  GadaiUlangMapper.objects.get(item='jurnal_bank_gu_nilai_kurang',cabang=nas.kasir.gerai)
    a_titipan_pencairan = gu.coa_titipan_pelunasan
    a_pend_lainnya = gu.coa_beban
    a_bank = gu.coa_kas

    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (nas.kasir.norek(), nas.kasir.agnasabah.nama),
        tgl_trans =nas.tanggal_lunas,nobukti=nas.kasir.norek(),object_id = nas.id,kode_cabang = user.profile.gerai.kode_cabang,
        cu =user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_kurang_bank"), id_coa = a_bank,
        debet = nas.nilai_pembulatan_lunas,kredit = 0,id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_kurang_bol_bank"), id_coa = a_pend_lainnya,
        kredit = 0, debet = -1 * (nas.selisih_lunas),id_product = '4',status_jurnal ='2',tgl_trans =nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_gu_kasir_nilai_sblm_kurang_bank"), id_coa = a_titipan_pencairan,
        kredit = nas.sisa_bayar_lunas,debet = 0,id_product = '4',status_jurnal ='2',tgl_trans = nas.tanggal_lunas,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)
@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def laporan_pelunasan_titipan(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    sekarang = datetime.date.today()
    kocab = Tbl_Cabang.objects.get(kode_cabang=cab)
    gr = Pelunasan.objects.filter(tanggal=sekarang,gerai__kode_cabang=kocab.kode_cabang)
    template = 'kasir/laporan/laporan_pelunasan_titipan.html'
    variables = RequestContext(request, {'user':User,'gr':gr,'kocab':kocab})
    return render_to_response(template, variables)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def laporan_pelunasan(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    sekarang = datetime.date.today()
    kocab = Tbl_Cabang.objects.get(kode_cabang=cab)
    gr = Pelunasan.objects.filter(tanggal=sekarang,gerai__kode_cabang=kocab.kode_cabang,status_pelunasan = u'1')
    template = 'kasir/laporan/laporan_pelunsan.html'
    variables = RequestContext(request, {'user':User,'gr':gr,'kocab':kocab})
    return render_to_response(template, variables)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def laporan_pencairan(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    sekarang = datetime.date.today()
    kocab = Tbl_Cabang.objects.get(kode_cabang=cab)
    gr = AkadGadai.objects.filter(tanggal=sekarang,gerai__kode_cabang=kocab.kode_cabang,kasirgerai__val=1)
    template = 'kasir/laporan/laporan_pencairan.html'
    variables = RequestContext(request, {'user':User,'gr':gr,'kocab':kocab})
    return render_to_response(template, variables)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def mastertiket_antargerai(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    cabang = Tbl_Cabang.objects.get(kode_cabang=cab)
    sekarang = datetime.date.today()
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=cab).filter(status_jurnal=u'2').\
        filter(jenis__in=('GL_GL_PENAMBAHAN_KAS','GL_GL_PENGELUARAN_KAS_PUSAT','GL_GL_PENAMBAHAN_GERAI','GL_GL_PENAMBAHAN_BANK','GL_GL_RAK_CABANG ',\
        'GL_GL_PENAMBAHAN_BANK_RAK','GL_GL_PENGELUARAN_BANK_RAK','GL_GL_PENGEMBALIAN_PUSAT_BANK_RAK','PENGELUARAN_KE_GERAI',\
        'GL_GL_PENGELUARAN_BANK','GL_GL_PENGELUARAN_BANK_PUSAT','GL_GL_PENGELUARAN_KAS','GL_GL_PENGEMBALIAN_PUSAT',\
        'GL_GL_PENGEMBALIAN_BANK_CABANG_RAK','GL_GL_PENGEMBALIAN_PUSAT_BANK',u'Pelunasan_kasir_rak','GL_GL_RAK_PUSAT_CABANG',\
        u'Pelunasan_kasir_bank_rak','GL_GL_PENGEMBALIAN_SALDO_GERAI'))
    template = 'kasir/tiket/mastertiket_antargerai.html'
    variables = RequestContext(request, {'cabang':cabang,'user':User,'g':gr,'total_debet': sum([p.debet for p in gr]),\
        'total_kredit': sum([p.kredit for p in gr])})
    return render_to_response(template, variables)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def mastertiket_uangmuka(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    cabang = Tbl_Cabang.objects.get(kode_cabang=cab)
    sekarang = datetime.date.today()
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=cab).filter(status_jurnal=u'2').\
        filter(jenis__in=('GL_GL_PUSAT_UK','GL_GL_CABANG_UK','GL_GL_PENGEMBALIAN_UK'))  
    template = 'kasir/tiket/mastertiket_uangmuka.html'
    variables = RequestContext(request, {'cabang':cabang,'user':User,'g':gr,'total_debet': sum([p.debet for p in gr]),\
        'total_kredit': sum([p.kredit for p in gr])})
    return render_to_response(template, variables)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def uangmuka(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    kocab = Tbl_Cabang.objects.get(kode_cabang=cab)
    saldo_uangmuka_awal = 0
    transaksi_jurnal = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today(),jenis =
        (u'GL_GL_CABANG_UK'),id_cabang=cab,status_jurnal=2)
    uang_muka_gerai = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today(),jenis = 'GL_GL_PUSAT_UK',id_cabang=cab,status_jurnal=2)
    pengembalian_uk = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today(),jenis =
        'GL_GL_PENGEMBALIAN_UK',id_cabang=cab,status_jurnal=2)
    variables = RequestContext(request,{'kocab':kocab,'uang_muka':sum ([a.debet for a in uang_muka_gerai]),'transaksi_jurnal':transaksi_jurnal,
            'uang_muka_sum':sum ([a.debet for a in transaksi_jurnal]),'pengembalian_uk':sum ([a.kredit for a in pengembalian_uk]),
            'saldo_uk_akhir': sum ([a.debet for a in uang_muka_gerai]) - sum ([a.debet for a in transaksi_jurnal]) - sum ([a.kredit for a in pengembalian_uk])})
    template='kasir/view/all_transaksi_uangmuka.html'
    return render_to_response(template,variables)


### ASLI
@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def all_transaksi_kas(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    kocab = Tbl_Cabang.objects.get(kode_cabang=cab)
    sekarang = datetime.date.today()
    bray_posting = PostingGerai.objects.filter(kode_cabang=cab,tanggal =sekarang)
    tes_posting = bray_posting.count()

    tgl = timedelta(days=1)
    tanggal = sekarang - tgl
    a = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang).filter(id_coa__coa__startswith ='11.01').filter(jenis='SALDOKASGERAI').latest('id')
    c = a.tgl_trans
    d = sekarang - c
    s_awal = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang).filter(id_coa__coa__startswith ='11.01').filter(tgl_trans=sekarang).\
        filter(jenis='SALDOKASGERAI')
    s_awal_lates = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang).filter(id_coa__coa__startswith ='11.01').filter(jenis='SALDOKASGERAI').filter(tgl_trans=c)
    tampil =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(status_posting__isnull = True).\
        filter(jurnal__kode_cabang=kocab.kode_cabang)
    setoran_bank_gerai = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PENAMBAHAN_BANK').\
        filter(jurnal__kode_cabang=cab).filter(status_jurnal=2)
    setoran_kas_gerai = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in =( 'GL_GL_PENAMBAHAN_KAS',u'Pelunasan_kasir_rak')).\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_uk_bank = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGELUARAN_BANK').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_bank_pusat = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGEMBALIAN_SALDO_GERAI').\
        filter(id_cabang=cab,status_jurnal=2)
    pengembalian_kas_pusat = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGELUARAN_KAS_PUSAT').\
        filter(id_cabang=cab,status_jurnal=2)
    pengembalian_bank = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGELUARAN_BANK').\
        filter(id_cabang=cab,status_jurnal=2)
    pengembalian_kas = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis__in =('GL_GL_PENGELUARAN_KAS_PUSAT','PENGELUARAN_KE_GERAI')).filter(id_cabang=cab).filter(status_jurnal=2)
    uang_muka_gerai = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PUSAT_UK').\
        filter(id_cabang=cab,status_jurnal=2)
    pencairan_kasir = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'Pencairan_kasir').\
        filter(id_cabang=cab,status_jurnal=2)
    pencairan_kasir_sisa = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pencairan_kasir',\
        'Pelunasan_kasir','Pelunasan_gu_kasir_nilai_sblm_lebih_pol','Pelunasan_gu_kasir_nilai_sblm_kurang_pdl','Pencairan_kasir_sisa',\
        'Pelunasan_kasir_rak','Pencairan_Kasir')).\
        filter(id_cabang=cab,status_jurnal=2,id_coa__in= (448L,546L))
    pengembalian_uk = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGEMBALIAN_UK').\
        filter(id_cabang=cab,status_jurnal=2)
    saldo_yang_dikirim = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    transaksi_jurnal = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = (u'GL_GL_CABANG',\
        u'Pelunasan_gu_kasir_nilai_sblm_lebih_bl',u'Pencairan_kasir_kurang','Pelunasan_gu_kasir_nilai_sblm_kurang_bol',\
        'Pelunasan_kasir_kurang_rak','Pelunasan_kasir_kurang')).filter(id_cabang=cab).filter(status_jurnal=2)#.filter(jurnal__status_jurnal = u'1')
    saldo_awal_hari = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_BIAYA_GERAI').\
        filter(id_cabang=cab).filter(status_jurnal=2)#.filter(jurnal__status_jurnal = u'2')
    saldo_uang_muka_hari = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT_UK').\
        filter(id_cabang=cab,status_jurnal=2)#.filter(jurnal__status_jurnal = u'2')
    jurnal_list = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'Pencairan_kasir').\
        filter(id_cabang=cab).filter(status_jurnal=2).filter(id_coa= 7L)
    pndptn_lainnya = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in =('Pencairan_kasir')).\
        filter(id_cabang=cab,status_jurnal=2,id_coa= 448L)
    tbl = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = (u'Pelunasan_kasir',\
        u'Pelunasan_kasir',u'Pelunasan_kasir_kas_rak')).filter(id_cabang=cab,status_jurnal=2,id_coa__in= (651L,287L,635L,378L))
    tbl_beban =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').\
        filter(id_cabang=cab).filter(status_jurnal=2).filter(id_coa= 516L)
    rakp =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').\
        filter(id_cabang=cab,status_jurnal=2,id_coa= 378L)
    ak_ulang = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pelunasan_gu_kasir_nilai_sblm_lebih',\
        'Pelunasan_Gadai_Ulang_kasir','Pelunasan_gu_kasir_nilai_sblm_kurang')).filter(id_cabang=cab).filter(status_jurnal=2).\
        filter(id_coa__in= (448L,287L,298L))
    akad_ulang_pengeluaran = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis = ('Pelunasan_Gadai_Ulang_kasir_pinjaman_besar')).filter(id_cabang=cab).filter(status_jurnal=2).filter(id_coa= 298L)

    pengeluaran_gadai_ulang = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis__in = (u'Pelunasan_Gadai_Ulang_Kasir_nilai_pinjaman_lebih',u'Pelunasan_Gadai_Ulang_kasir_pinjaman_besar_tp',\
        u'Pelunasan_gu_kasir_nilai_sblm_lebih_tp',u'Pelunasan_gu_kasir_nilai_sblm_kurang','Pelunasan_Gadai_Ulang_kasir_pinjaman_besar')).\
        filter(id_cabang=cab,status_jurnal=2,id_coa=298L)
    ###
    titipan_kas = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = ('GL_GL_JUNAL_PENDAPATAN')).filter(id_cabang=cab).filter(status_jurnal=2)
   ###
    pengembalian_nasabah = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis__in = ('Pengembalian_titipan_kelebihan','Pengembalian_titipan_kelebihan_gu')).\
        filter(id_cabang=cab).filter(status_jurnal=2) 
    hitung_a = sum(a.debet for a in titipan_kas) + sum ([a.kredit for a in ak_ulang]) +sum ([a.kredit for a in setoran_kas_gerai]) + sum ([a.kredit for a in setoran_bank_gerai])\
        +  sum ([a.kredit for a in pencairan_kasir_sisa]) + sum ([a.kredit for a in tbl]) 
    hitung_b = sum ([a.debet for a in transaksi_jurnal]) + sum ([a.debet for a in pengembalian_nasabah]) + \
            sum ([a.debet for a in pencairan_kasir]) +\
            sum ([a.kredit for a in pengembalian_kas]) +\
            sum ([a.debet for a in pengeluaran_gadai_ulang])
    saldo_awal =  sum([p.saldo for p in s_awal])
    saldo_awal_lates =  sum([p.saldo for p in s_awal_lates])
    poston = Tbl_Transaksi.objects.filter(id_cabang=kocab.kode_cabang).filter(tgl_trans=sekarang)
    postingon = sum([a.jurnal.postingon for a in poston])
    postingoff = sum([a.jurnal.postingoff for a in poston])
    postingonoff = sum([a.jurnal.postingonoff for a in poston])
    if d > datetime.timedelta(1) :
        variables = RequestContext(request,{'tes_posting':tes_posting,'kocab':kocab,'transaksi_jurnal':transaksi_jurnal,\
            'a':jurnal_list,'total_pencairan':sum ([a.kredit for a in jurnal_list]),'titipan_kas':titipan_kas,\
            'setoran_bank_kas_gerai' :sum ([a.kredit for a in setoran_kas_gerai]) + sum ([a.kredit for a in setoran_bank_gerai]),\
            'pengembalian_bank_pusat_pjb' :sum ([a.debet for a in pengembalian_bank_pusat]) ,
            'pengembalian_bank' :sum ([a.kredit for a in pengembalian_bank]) + sum ([a.kredit for a in pengembalian_kas]),\
            'uang_muka':sum ([a.kredit for a in uang_muka_gerai]),'saldo_awal':saldo_awal_lates,
            #'saldo_awal': sum([a.saldo for a in s_awal]),
            'total_penerimaan':hitung_a,
            'total_pengeluaran': hitung_b ,
            'saldo_akhir': saldo_awal + int(hitung_a) - int(hitung_b),
            'saldo_keseluruhan': (saldo_awal + hitung_a - hitung_b) - sum ([a.kredit for a in pengembalian_bank_pusat]),             
            'pencairan':sum ([a.debet for a in pencairan_kasir]),\
            'pencairan_kasir_sisa':pencairan_kasir_sisa,\
            'saldo_awal_hari':sum ([a.debet for a in saldo_awal_hari]),\
            'saldo_uangmuka_hari':sum ([a.debet for a in saldo_uang_muka_hari]),\
            'total_pelunasan':tbl,\
            'total_pendapatan_lainnya':sum ([a.kredit for a in pndptn_lainnya]),'sekarang':datetime.date.today(),\
            'beban_listrik':(sum ([a.debet for a in tbl_beban])),\
            'total_rakp':sum ([a.kredit for a in rakp]), \
            'total_transaksi_jurnal': sum ([a.debet for a in transaksi_jurnal]),\
            'total_saldo' :  saldo_awal ,'ak_ulang':ak_ulang,
            #'penjualan': penjualan,
            'pengeluaran_gadai_ulang': pengeluaran_gadai_ulang,'pengembalian_kas_pusat':pengembalian_kas_pusat,\
            'pengembalian_bank_pusat':pengembalian_kas_pusat,\
            'saldo_yang_di_kirim':sum ([a.debet for a in saldo_yang_dikirim]), 'pengembalian_kas':pengembalian_kas,\
            't_kasir':pencairan_kasir,'tampil':saldo_awal,'postingon':postingon,'postingonoff':postingonoff,'postingoff':postingoff,
            'pengembalian_bank':pengembalian_bank,'setoran_kas_gerai':setoran_kas_gerai,
            'pengembalian_kenasabah':pengembalian_nasabah,
            'setoran_bank_gerai':setoran_bank_gerai,'cabang':kocab})
    if d <= datetime.timedelta(1) :
        variables = RequestContext(request,{'tes_posting':tes_posting,'kocab':kocab,'transaksi_jurnal':transaksi_jurnal,\
            'a':jurnal_list,'total_pencairan':sum ([a.kredit for a in jurnal_list]),'titipan_kas':titipan_kas,\
            'setoran_bank_kas_gerai' :sum ([a.kredit for a in setoran_kas_gerai]) + sum ([a.kredit for a in setoran_bank_gerai]),\
            'pengembalian_bank_pusat_pjb' :sum ([a.debet for a in pengembalian_bank_pusat]) ,
            'pengembalian_bank' :sum ([a.kredit for a in pengembalian_bank]) + sum ([a.kredit for a in pengembalian_kas]),\
            'uang_muka':sum ([a.kredit for a in uang_muka_gerai]),'saldo_awal':saldo_awal,
            #'saldo_awal': sum([a.saldo for a in s_awal]),
            'total_penerimaan':hitung_a,
            'total_pengeluaran': hitung_b ,
            'saldo_akhir': saldo_awal_lates + int(hitung_a) - int(hitung_b),
            'saldo_keseluruhan': (saldo_awal_lates + hitung_a - hitung_b) - sum ([a.kredit for a in pengembalian_bank_pusat]),  
             
            'pencairan':sum ([a.debet for a in pencairan_kasir]),\
            'pencairan_kasir_sisa':pencairan_kasir_sisa,\
            'saldo_awal_hari':sum ([a.debet for a in saldo_awal_hari]),\
            'saldo_uangmuka_hari':sum ([a.debet for a in saldo_uang_muka_hari]),\
            'total_pelunasan':tbl,\
            'total_pendapatan_lainnya':sum ([a.kredit for a in pndptn_lainnya]),'sekarang':datetime.date.today(),\
            'beban_listrik':(sum ([a.debet for a in tbl_beban])),\
            'total_rakp':sum ([a.kredit for a in rakp]), \
            'total_transaksi_jurnal': sum ([a.debet for a in transaksi_jurnal]),\
            'total_saldo' :  saldo_awal ,'ak_ulang':ak_ulang,
            #'penjualan': penjualan,
            'pengeluaran_gadai_ulang': pengeluaran_gadai_ulang,'pengembalian_kas_pusat':pengembalian_kas_pusat,\
            'pengembalian_bank_pusat':pengembalian_kas_pusat,\
            'saldo_yang_di_kirim':sum ([a.debet for a in saldo_yang_dikirim]), 'pengembalian_kas':pengembalian_kas,\
            't_kasir':pencairan_kasir,'tampil':saldo_awal,'postingon':postingon,'postingonoff':postingonoff,'postingoff':postingoff,
            'pengembalian_bank':pengembalian_bank,'setoran_kas_gerai':setoran_kas_gerai,
            'pengembalian_kenasabah':pengembalian_nasabah,
            'setoran_bank_gerai':setoran_bank_gerai,'cabang':kocab})      
    template='kasir/view/all_transaksi_kas.html'
    return render_to_response(template,variables)

## AKHIR ALL TRANSAKSI KAS ASLI
@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def cetak_all_transaksi_kas(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    kocab = Tbl_Cabang.objects.get(kode_cabang=cab)
    sekarang = datetime.date.today()
    tgl = timedelta(days=1)
    tanggal = sekarang - tgl
    a = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang,id_coa__coa__startswith ='11.01',jenis='SALDOKASGERAI').latest('id')
    c = a.tgl_trans
    d = sekarang - c
    s_awal = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang,id_coa__coa__startswith ='11.01',tgl_trans=sekarang,jenis='SALDOKASGERAI')
    s_awal_lates = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang,id_coa__coa__startswith
            ='11.01',jenis='SALDOKASGERAI',tgl_trans=c)
    tampil =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today(),status_posting__isnull = True,jurnal__kode_cabang=kocab.kode_cabang)
    setoran_bank_gerai = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today(),jenis = u'GL_GL_PENAMBAHAN_BANK').\
        filter(jurnal__kode_cabang=cab).filter(status_jurnal=2)
    setoran_kas_gerai = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today(),jenis__in =( 'GL_GL_PENAMBAHAN_KAS',u'Pelunasan_kasir_rak')).\
        filter(id_cabang=cab,status_jurnal=2)
    pengembalian_uk_bank = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today(),jenis = 'GL_GL_PENGELUARAN_BANK').\
        filter(id_cabang=cab,status_jurnal=2)
    pengembalian_bank_pusat = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGEMBALIAN_SALDO_GERAI').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_kas_pusat = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGELUARAN_KAS_PUSAT').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_bank = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGELUARAN_BANK').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_kas = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis__in =('GL_GL_PENGELUARAN_KAS_PUSAT','PENGELUARAN_KE_GERAI')).filter(id_cabang=cab).filter(status_jurnal=2)
    uang_muka_gerai = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PUSAT_UK').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pencairan_kasir = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'Pencairan_kasir').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pencairan_kasir_sisa = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pencairan_kasir',\
        'Pelunasan_kasir','Pelunasan_gu_kasir_nilai_sblm_lebih_pol','Pelunasan_gu_kasir_nilai_sblm_kurang_pdl','Pencairan_kasir_sisa',\
        'Pelunasan_kasir_rak','Pencairan_Kasir')).\
        filter(id_cabang=cab).filter(status_jurnal=2).filter(id_coa__in= (448L,546L))
    pengembalian_uk = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGEMBALIAN_UK').\
        filter(id_cabang=cab).filter(status_jurnal=2)    
    saldo_yang_dikirim = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').\
        filter(id_cabang=cab).filter(status_jurnal=2)#.filter(jurnal__status_jurnal = u'3')
    transaksi_jurnal = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = (u'GL_GL_CABANG',\
        u'Pelunasan_gu_kasir_nilai_sblm_lebih_bl',u'Pencairan_kasir_kurang','Pelunasan_gu_kasir_nilai_sblm_kurang_bol',\
        'Pelunasan_kasir_kurang_rak','Pelunasan_kasir_kurang')).filter(id_cabang=cab).filter(status_jurnal=2)#.filter(jurnal__status_jurnal = u'1')
    saldo_awal_hari = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_BIAYA_GERAI').\
        filter(id_cabang=cab).filter(status_jurnal=2)#.filter(jurnal__status_jurnal = u'2')
    saldo_uang_muka_hari = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT_UK').\
        filter(id_cabang=cab).filter(status_jurnal=2)#.filter(jurnal__status_jurnal = u'2')
    jurnal_list = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'Pencairan_kasir').\
        filter(id_cabang=cab,status_jurnal=2,id_coa= 7L)
    pndptn_lainnya = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in =('Pencairan_kasir')).\
        filter(id_cabang=cab,status_jurnal=2,id_coa= 448L)
    tbl = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = (u'Pelunasan_kasir',\
        u'Pelunasan_kasir',u'Pelunasan_kasir_kas_rak'),id_cabang=cab,status_jurnal=2,id_coa__in= (651L,287L,635L,378L))
    tbl_beban =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').\
        filter(id_cabang=cab,status_jurnal=2,id_coa= 516L)
    rakp =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today(),jenis = u'GL_GL_PUSAT').\
        filter(id_cabang=cab,status_jurnal=2,id_coa= 378L)
    ak_ulang = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today(),jenis__in = ('Pelunasan_gu_kasir_nilai_sblm_lebih',\
        'Pelunasan_Gadai_Ulang_kasir','Pelunasan_gu_kasir_nilai_sblm_kurang'),id_cabang=cab,status_jurnal=2,\
        id_coa__in= (448L,287L,298L))
    akad_ulang_pengeluaran = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis = ('Pelunasan_Gadai_Ulang_kasir_pinjaman_besar'),id_cabang=cab,status_jurnal=2,id_coa= 298L)
    pengeluaran_gadai_ulang = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis__in = (u'Pelunasan_Gadai_Ulang_Kasir_nilai_pinjaman_lebih',u'Pelunasan_Gadai_Ulang_kasir_pinjaman_besar_tp',\
        u'Pelunasan_gu_kasir_nilai_sblm_lebih_tp',u'Pelunasan_gu_kasir_nilai_sblm_kurang','Pelunasan_Gadai_Ulang_kasir_pinjaman_besar')).\
        filter(id_cabang=cab,status_jurnal=2,id_coa=298L)
   ###
    titipan_kas = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = ('GL_GL_JUNAL_PENDAPATAN')).filter(id_cabang=cab).filter(status_jurnal=2)
   ###
    pengembalian_nasabah = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis__in = ('Pengembalian_titipan_kelebihan','Pengembalian_titipan_kelebihan_gu')).\
        filter(id_cabang=cab).filter(status_jurnal=2)
    hitung_a = sum(a.debet for a in titipan_kas) + sum ([a.kredit for a in ak_ulang]) +sum ([a.kredit for a in setoran_kas_gerai]) \
        + sum ([a.kredit for a in setoran_bank_gerai]) +  sum ([a.kredit for a in pencairan_kasir_sisa]) + sum ([a.kredit for a in tbl]) 
    hitung_b = sum ([a.debet for a in transaksi_jurnal]) + sum ([a.debet for a in pengembalian_nasabah]) + \
            sum ([a.debet for a in pencairan_kasir]) + sum ([a.kredit for a in pengembalian_kas]) +\
            sum ([a.debet for a in pengeluaran_gadai_ulang])
    saldo_awal =  sum([p.saldo for p in s_awal])
    saldo_awal_lates =  sum([p.saldo for p in s_awal_lates])
    poston = Tbl_Transaksi.objects.filter(id_cabang=kocab.kode_cabang).filter(tgl_trans=sekarang)
    postingon = sum([a.jurnal.postingon for a in poston])
    postingoff = sum([a.jurnal.postingoff for a in poston])
    postingonoff = sum([a.jurnal.postingonoff for a in poston])
    if d > datetime.timedelta(1) :
        variables = RequestContext(request,{'kocab':kocab,'transaksi_jurnal':transaksi_jurnal,'titipan_kas':titipan_kas,\
            'a':jurnal_list,'total_pencairan':sum ([a.kredit for a in jurnal_list]),\
            'setoran_bank_kas_gerai' :sum ([a.kredit for a in setoran_kas_gerai]) + sum ([a.kredit for a in setoran_bank_gerai]),\
            'pengembalian_bank_pusat_pjb' :sum ([a.debet for a in pengembalian_bank_pusat]) ,
            'pengembalian_bank' :sum ([a.kredit for a in pengembalian_bank]) + sum ([a.kredit for a in pengembalian_kas]),\
            'uang_muka':sum ([a.kredit for a in uang_muka_gerai]),'saldo_awal':saldo_awal_lates,
            #'saldo_awal': sum([a.saldo for a in s_awal]),
            'total_penerimaan':hitung_a,
            'total_pengeluaran': hitung_b ,
            'saldo_akhir': saldo_awal + int(hitung_a) - int(hitung_b),
            'saldo_keseluruhan': (saldo_awal + hitung_a - hitung_b) - sum ([a.kredit for a in pengembalian_bank_pusat]),             
            'pencairan':sum ([a.debet for a in pencairan_kasir]),\
            'pencairan_kasir_sisa':pencairan_kasir_sisa,\
            'saldo_awal_hari':sum ([a.debet for a in saldo_awal_hari]),\
            'saldo_uangmuka_hari':sum ([a.debet for a in saldo_uang_muka_hari]),\
            'total_pelunasan':tbl,\
            'total_pendapatan_lainnya':sum ([a.kredit for a in pndptn_lainnya]),'sekarang':datetime.date.today(),\
            'beban_listrik':(sum ([a.debet for a in tbl_beban])),\
            'total_rakp':sum ([a.kredit for a in rakp]), \
            'total_transaksi_jurnal': sum ([a.debet for a in transaksi_jurnal]),\
            'total_saldo' :  saldo_awal ,'ak_ulang':ak_ulang,
            #'penjualan': penjualan,
            'pengeluaran_gadai_ulang': pengeluaran_gadai_ulang,'pengembalian_kas_pusat':pengembalian_kas_pusat,\
            'pengembalian_bank_pusat':pengembalian_kas_pusat,\
            'saldo_yang_di_kirim':sum ([a.debet for a in saldo_yang_dikirim]), 'pengembalian_kas':pengembalian_kas,\
            't_kasir':pencairan_kasir,'tampil':saldo_awal,'postingon':postingon,'postingonoff':postingonoff,'postingoff':postingoff,
            'pengembalian_bank':pengembalian_bank,'setoran_kas_gerai':setoran_kas_gerai,
            'pengembalian_kenasabah':pengembalian_nasabah,
            'setoran_bank_gerai':setoran_bank_gerai,'cabang':kocab})
    if d <= datetime.timedelta(1) :
        variables = RequestContext(request,{'kocab':kocab,'transaksi_jurnal':transaksi_jurnal,'titipan_kas':titipan_kas,\
            'a':jurnal_list,'total_pencairan':sum ([a.kredit for a in jurnal_list]),\
            'setoran_bank_kas_gerai' :sum ([a.kredit for a in setoran_kas_gerai]) + sum ([a.kredit for a in setoran_bank_gerai]),\
            'pengembalian_bank_pusat_pjb' :sum ([a.debet for a in pengembalian_bank_pusat]) ,
            'pengembalian_bank' :sum ([a.kredit for a in pengembalian_bank]) + sum ([a.kredit for a in pengembalian_kas]),\
            'uang_muka':sum ([a.kredit for a in uang_muka_gerai]),'saldo_awal':saldo_awal,
            #'saldo_awal': sum([a.saldo for a in s_awal]),
            'total_penerimaan':hitung_a,
            'total_pengeluaran': hitung_b ,
            'saldo_akhir': saldo_awal_lates + int(hitung_a) - int(hitung_b),
            'saldo_keseluruhan': (saldo_awal_lates + hitung_a - hitung_b) - sum ([a.kredit for a in pengembalian_bank_pusat]),  
             
            'pencairan':sum ([a.debet for a in pencairan_kasir]),\
            'pencairan_kasir_sisa':pencairan_kasir_sisa,\
            'saldo_awal_hari':sum ([a.debet for a in saldo_awal_hari]),\
            'saldo_uangmuka_hari':sum ([a.debet for a in saldo_uang_muka_hari]),\
            'total_pelunasan':tbl,\
            'total_pendapatan_lainnya':sum ([a.kredit for a in pndptn_lainnya]),'sekarang':datetime.date.today(),\
            'beban_listrik':(sum ([a.debet for a in tbl_beban])),\
            'total_rakp':sum ([a.kredit for a in rakp]), \
            'total_transaksi_jurnal': sum ([a.debet for a in transaksi_jurnal]),\
            'total_saldo' :  saldo_awal ,'ak_ulang':ak_ulang,
            #'penjualan': penjualan,
            'pengeluaran_gadai_ulang': pengeluaran_gadai_ulang,'pengembalian_kas_pusat':pengembalian_kas_pusat,\
            'pengembalian_bank_pusat':pengembalian_kas_pusat,\
            'saldo_yang_di_kirim':sum ([a.debet for a in saldo_yang_dikirim]), 'pengembalian_kas':pengembalian_kas,\
            't_kasir':pencairan_kasir,'tampil':saldo_awal,'postingon':postingon,'postingonoff':postingonoff,'postingoff':postingoff,
            'pengembalian_bank':pengembalian_bank,'setoran_kas_gerai':setoran_kas_gerai,
            'pengembalian_kenasabah':pengembalian_nasabah,
            'setoran_bank_gerai':setoran_bank_gerai,'cabang':kocab})      
    template='kasir/view/cetak_transaksi_all_harian.html'
    return render_to_response(template,variables)


def jurnal_umum(request,object_id): 
    jurnal_list = Tbl_Transaksi.objects.all()
    kobar=object_id
    trans=[]
    form = Tbl_AkunForm()
    start_date = None
    end_date = None
    id_cabang = None
    if 'start_date' in request.GET and request.GET['end_date']  and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(status_jurnal=2)   
        trans = []
        for l in ledger_search:           
            trans.append(l)
        start_date = start_date
        end_date = end_date

        template='kasir/jurnal_umum.html'
        variable = RequestContext(request, {'jurnal_list': trans,'total_debet': sum([p.debet for p in trans]),'total_kredit': sum([p.kredit for p in trans]),
                'start_date':start_date,'end_date':start_date,'kobar':kobar})
        return render_to_response(template,variable)

    elif 'start_date' in request.GET and request.GET['end_date']  and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(status_jurnal=2)
        trans = []
        for l in ledger_search:
            trans.append(l)
        start_date = start_date
        end_date = end_date

        template1= 'kasir/cetak_jurnal_umum.html'
        variable = RequestContext(request, {'jurnal_list': trans,'total_debet': sum([p.debet for p in trans]),'total_kredit': sum([p.kredit for p in trans]),
                'start_date':start_date,'end_date':start_date,'kobar':kobar})
        return render_to_response(template1,variable)
    else:
        template = 'kasir/jurnal_umum.html'
        variable = RequestContext(request, {'jurnal_list': trans,'total_debet': sum([p.debet for p in trans]),'total_kredit': sum([p.kredit for p in trans]),
            'start_date':start_date,'end_date':start_date,'kobar':kobar})
        return render_to_response(template,variable)

def gl_val(request,object_id):
    gr = Tbl_Transaksi.objects.get(id=object_id)
    template = 'kasir/gl_validasi.html'
    variable = RequestContext(request, {'gr':gr,})
    return render_to_response(template,variable)

def cetak_all_transaksi(request,object_id):
    kocab = Tbl_Cabang.objects.get(kode_cabang=object_id)
    saldo_awal = 0
    saldo_yang_dikirim = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').filter(id_cabang=object_id).filter(status_jurnal=1)
    transaksi_jurnal = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').filter(id_cabang=object_id).filter(status_jurnal=1)
    saldo_awal_hari = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_BIAYA_GERAI').filter(id_cabang=object_id).filter(status_jurnal=1)
    jurnal_list = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'Pencairan_kasir').filter(id_cabang=object_id).filter(status_jurnal=1).filter(id_coa= 7L)
    pndptn_lainnya = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in =('Pencairan_kasir','Pelunasan_kasir')).filter(id_cabang=object_id).filter(status_jurnal=1).filter(id_coa= 448L)
    tbl = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis =u'Pelunasan_kasir').filter(id_cabang=object_id).filter(status_jurnal=1).filter(id_coa= 287L)
    tbl_beban =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').filter(id_cabang=object_id).filter(status_jurnal=1).filter(id_coa= 516L)
    rakp =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').filter(id_cabang=object_id).filter(status_jurnal=1).filter(id_coa= 378L)
    variables = RequestContext(request,{'kocab':kocab,'transaksi_jurnal':transaksi_jurnal,'a':jurnal_list,'total_pencairan':sum ([a.kredit for a in jurnal_list]),\
        'saldo_awal_hari':sum ([a.debet for a in saldo_awal_hari]),\
        'total_pelunasan':sum ([a.kredit for a in tbl]),\
        'total_pendapatan_lainnya':sum ([a.kredit for a in pndptn_lainnya]),'sekarang':datetime.date.today(),\
        'total_penerimaan':(sum ([a.kredit for a in tbl]) + sum ([a.kredit for a in pndptn_lainnya])),\
        'total_pengeluaran':(sum ([a.kredit for a in jurnal_list])+ sum ([a.debet for a in transaksi_jurnal])),\
        'beban_listrik':(sum ([a.debet for a in tbl_beban])),\
        'total_rakp':sum ([a.kredit for a in rakp]), \
        'total_transaksi_jurnal': sum ([a.debet for a in transaksi_jurnal]),\
        'total_saldo' :  sum ([a.debet for a in saldo_awal_hari]) + saldo_awal,
        'saldo_akhir':( (sum ([a.kredit for a in rakp]) + (sum ([a.debet for a in tbl])\
            + sum ([a.kredit for a in pndptn_lainnya]))) - (sum ([a.kredit for a in jurnal_list])+ sum ([a.debet for a in tbl_beban]))),
        'saldo_keseluruhan': (sum ([a.debet for a in saldo_awal_hari])) + ((sum ([a.kredit for a in tbl])\
            + sum ([a.kredit for a in pndptn_lainnya])))- ((sum ([a.kredit for a in jurnal_list]) \
            + sum ([a.debet for a in transaksi_jurnal]))),
        'saldo_yang_di_kirim':sum ([a.debet for a in saldo_yang_dikirim]),
        'saldo_akhir': ((sum ([a.debet for a in saldo_awal_hari])) + ((sum ([a.kredit for a in tbl]) \
            + sum ([a.kredit for a in pndptn_lainnya])))- ((sum ([a.kredit for a in jurnal_list]) \
            + sum ([a.debet for a in transaksi_jurnal]))))- sum ([a.debet for a in saldo_yang_dikirim]),
    })
    template='kasir/view/cetak_transaksi_all_harian.html'
    return render_to_response(template,variables)

def all_transaksi(request,object_id):
    kocab = Tbl_Cabang.objects.get(kode_cabang=object_id)
    cab = object_id
    saldo_awal = 0
    saldo_yang_dikirim = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').filter(id_cabang=cab).filter(status_jurnal=1)#.filter(jurnal__status_jurnal = u'3')
    transaksi_jurnal = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = (u'GL_GL_CABANG')).filter(id_cabang=cab).filter(status_jurnal=1)#.filter(jurnal__status_jurnal = u'1')
    saldo_awal_hari = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_BIAYA_GERAI').filter(id_cabang=cab).filter(status_jurnal=1)#.filter(jurnal__status_jurnal = u'2')
    saldo_uang_muka_hari = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT_UK').filter(id_cabang=cab).filter(status_jurnal=1)#.filter(jurnal__status_jurnal = u'2')
    jurnal_list = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'Pencairan_kasir').filter(id_cabang=object_id).filter(status_jurnal=1).filter(id_coa= 7L)
    pndptn_lainnya = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in =('Pencairan_kasir','Pelunasan_kasir')).filter(id_cabang=object_id).filter(status_jurnal=1).filter(id_coa= 448L)
    tbl = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 
u'Pelunasan_kasir').filter(id_cabang=object_id).filter(status_jurnal=1).filter(id_coa= 287L)
    tbl_beban =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 
u'GL_GL_PUSAT').filter(id_cabang=object_id).filter(status_jurnal=1).filter(id_coa= 516L)
    rakp =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').filter(id_cabang=object_id).filter(status_jurnal=1).filter(id_coa= 378L)
    
    variables = RequestContext(request,{'kocab':kocab,'transaksi_jurnal':transaksi_jurnal,'a':jurnal_list,'total_pencairan':sum ([a.kredit for a in 
jurnal_list]),\
        'saldo_awal_hari':sum ([a.debet for a in saldo_awal_hari]),\
        'saldo_uangmuka_hari':sum ([a.debet for a in saldo_uang_muka_hari]),\
        'total_pelunasan':sum ([a.kredit for a in tbl]),\
        'total_pendapatan_lainnya':sum ([a.kredit for a in pndptn_lainnya]),'sekarang':datetime.date.today(),\
        'total_penerimaan':(sum ([a.kredit for a in tbl]) + sum ([a.kredit for a in pndptn_lainnya])),\
        'total_pengeluaran':(sum ([a.kredit for a in jurnal_list])+ sum ([a.debet for a in transaksi_jurnal])),\
        'beban_listrik':(sum ([a.debet for a in tbl_beban])),\
        'total_rakp':sum ([a.kredit for a in rakp]), \
        'total_transaksi_jurnal': sum ([a.debet for a in transaksi_jurnal]),\
        'total_saldo' :  sum ([a.debet for a in saldo_awal_hari]) + saldo_awal + sum ([a.debet for a in saldo_uang_muka_hari]),
        'saldo_akhir':( (sum ([a.kredit for a in rakp]) + (sum ([a.debet for a in tbl])\
            + sum ([a.kredit for a in pndptn_lainnya]))) - (sum ([a.kredit for a in jurnal_list])+ sum ([a.debet for a in tbl_beban]))),
        'saldo_keseluruhan': (sum ([a.debet for a in saldo_awal_hari])) + ((sum ([a.kredit for a in tbl]) + sum ([a.debet for a in saldo_uang_muka_hari])\
            + sum ([a.kredit for a in pndptn_lainnya])))- ((sum ([a.kredit for a in jurnal_list])  \
            + sum ([a.debet for a in transaksi_jurnal]))),
        'saldo_yang_di_kirim':sum ([a.debet for a in saldo_yang_dikirim]),
        'saldo_akhir': ((sum ([a.debet for a in saldo_awal_hari])) + ((sum ([a.kredit for a in tbl]) + sum ([a.debet for a in saldo_uang_muka_hari])\
            + sum ([a.kredit for a in pndptn_lainnya])))- ((sum ([a.kredit for a in jurnal_list]) \
            + sum ([a.debet for a in transaksi_jurnal]))))- sum ([a.debet for a in saldo_yang_dikirim]),
    })
    template='kasir/view/all_transaksi.html'
    return render_to_response(template,variables)

def slip_validasi(request, object_id):
    gr = KasirGerai.objects.get(id = object_id)
    gr.val = 1
    gr.save()
    template = 'kasir/view/kw_val.html'
    variable = RequestContext(request, {'gr':gr,})
    return render_to_response(template,variable)

def all_approve(request,object_id):
    sekarang= datetime.date.today()
    ka = KasirGerai.objects.filter(kasir__gerai__kode_cabang=object_id)        
    #kasir = ka.filter(tanggal=sekarang)
    kasir = ka.all()
    template='kasir/view/data_approve_kasir.html'
    variable = RequestContext(request,{'ka': ka,'kasir':kasir})
    return render_to_response(template,variable)
    

def all_transaksi_jurnal(request,object_id):
    form = KasirGeraiForm()
    if 'start_date' in request.GET and request.GET['start_date']:
        start_date = request.GET['start_date']
        jurnal_list = Tbl_Transaksi.objects.filter(tgl_trans= start_date).filter(id_cabang=object_id).filter(status_jurnal=1)
        b = Tbl_Akun.objects.all()
        trans =[]
        for l in jurnal_list:
            trans.append(l)
        variables = RequestContext(request, {'cabang':Tbl_Cabang.objects.get(kode_cabang=object_id),'jurnal_list': trans,'kode':b,'sekarang':start_date,
            'total_debet':sum([p.debet for p in jurnal_list]),'total_kredit':sum([p.kredit for p in jurnal_list])})
        return render_to_response('kasir/view/all_transaksi_jurnal.html', variables)
    else:
        template='kasir/view/all_transaksi_jurnal.html'
        variable = RequestContext(request,{'cabang':Tbl_Cabang.objects.get(kode_cabang=object_id),'form':form})
        return render_to_response(template,variable)

def postting_all_jurnal(request):
    for i in request.POST.getlist('id_pilih'):
        gl = Tbl_Transaksi.objects.get(id=int(i))
        gl.status_jurnal = 2
        gl.save()
    messages.add_message(request, messages.INFO,' POSTING TRANSAKSI JUNAL SUKSES.')
    return HttpResponseRedirect("/")

def view_cabang(request,object_id):
    sekarang = datetime.date.today()
    akumulasi_kredit =0
    akumulasi_debet =0    
    jurnal_list = Tbl_Transaksi.objects.filter(id_coa__id=7).filter(tgl_trans= sekarang).filter(id_cabang=object_id)
    b = Tbl_Akun.objects.get(id=7)
    trans =[]
    for l in jurnal_list:
        for t in l.jurnal.tbl_transaksi_set.filter():
            akumulasi_kredit += t.kredit
            akumulasi_debet += t.debet
            trans.append({'debet':t.debet,'kredit':t.kredit,'saldo_awal':  (t.id_coa.saldo_pjb + akumulasi_debet) - akumulasi_kredit ,'deskripsi': t.id_coa.deskripsi,\
                'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,
                'id':t.id_coa.id})
            #saldo = saldo_awal
    variables = RequestContext(request, {'jurnal_list': trans,'kode':b,'saldo_kas':(b.saldo_pjb + sum([p.debet for p in jurnal_list])) - sum([p.kredit for p in jurnal_list]),
        'total_debet':sum([p.debet for p in jurnal_list]),'total_kredit':sum([p.kredit for p in jurnal_list])})
    return render_to_response('kasir/view/viewcabang.html', variables)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def master_tiket_kasir_pelunasan(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    cabang = Tbl_Cabang.objects.get(kode_cabang=cab)
    sekarang = datetime.date.today()
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=cab).filter(status_jurnal=2).\
        filter(jenis__in = (u'Pelunasan_kasir',u'Pelunasan_kasir_kurang',u'Pelunasan_kasir_bank','Pelunasan_kasir_bank_bol',\
        'Pelunasan_kasir_kurang_rak'))
    template = 'kasir/tiket/mastertiket_pelunasan_kasir.html'
    variables = RequestContext(request, {'user':User,'g':gr,'total_debet': sum([p.debet for p in gr]),\
        'total_kredit': sum([p.kredit for p in gr]),'cabang':cabang})
    return render_to_response(template, variables)

def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['ADM_GERAI','SUPERUSER','KASIR_GERAI','KPLGERAI','MANOP'])
@login_required
@user_passes_test(is_in_multiple_groups)
def mcc(request, object_id):
    gadai = AkadGadai.objects.get(id=object_id)
    gadai.status_mcc = '0'
    gadai.save()
   
    template = 'kasir/view/showmcc.html'
    variable = RequestContext(request, {'gadai': gadai})
    return render_to_response(template,variable)

def print_loan(request, object_id):
    gadai = AkadGadai.objects.get(id=object_id)
    template = 'kasir/view/cetak_loan_file.html'
    variable = RequestContext(request, {'gadai': gadai})
    return render_to_response(template,variable)

def cetak_data_kredit(request, object_id):
    gadai = AkadGadai.objects.get(id=object_id)
    template = 'kasir/view/loan_file.html'
    variable = RequestContext(request, {'ag': gadai})
    return render_to_response(template,variable)

def mcc_image(request, object_id):
    gadai = AkadGadai.objects.get(id=object_id)
    template = 'kasir/view/showmcc_image.html'
    variable = RequestContext(request, {'gadai': gadai})
    return render_to_response(template,variable)


def approve_pelunasan_kasir(request,object_id):
    a = Pelunasan.objects.all()
    #kasir = a.filter(gerai__kode_cabang=object_id).filter(kasirgerai__kasir_lunas=None)
    kasir = a.filter(gerai__kode_cabang=object_id)
    template='kasir/view/data_pelunasan_kasir.html'
    variable = RequestContext(request,{'a': a,'kasir':kasir})
    return render_to_response(template,variable)

####PELUNASAN KASIR
@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def lunas_kasir(request):
    akad = AkadGadai.objects.all()
    template='kasir/pelunasan/plns.html'
    variable = RequestContext(request,{'akad': akad})
    return render_to_response(template,variable)

def cariplns(request):
    rekening=request.GET['rekening']
    barcode = rekening[11:]
    try:
        akad=AkadGadai.objects.get(id=int(barcode))
        return HttpResponseRedirect("/kasirgerai/%s/kasir_pelunasan/" % akad.id)
    except:
        messages.add_message(request, messages.INFO,'No rekening tidak ditemukan.')
        return HttpResponseRedirect("/kasirgerai/lunas_kasir/")

def kasir_pelunasan(request, object_id):
    sekarang = datetime.date.today()
    kasir = AkadGadai.objects.get(id=object_id)
    plns = Pelunasan.objects.filter(status_pelunasan__in = (u'2',u'1')).filter(pelunasan__id=kasir.id)
    status = Pelunasan.objects.filter(status_pelunasan = u'1').filter(pelunasan__id=kasir.id)
    pembayaran = Pelunasan.objects.filter(pelunasan__id=kasir.id)
    titip = TitipanPelunasan.objects.filter(norek = object_id).filter(status = 1)
    ttp =titip.count()
    nilai_titipan = sum([a.nilai for a in titip])
    bayar =(int(kasir.nilai) + int(kasir.hitung_denda_pelunasan()) + int(kasir.hitung_jasa_pelunasan()))
    pengembalian = nilai_titipan - bayar

    if kasir.status_oto_plns == '3' :
        form = KasirGeraiPelunasanForm(initial={'status': 1,'nilai':int(kasir.nilai_lunas),'kasir':kasir,'tanggal':sekarang,
            'nilai_terima_bersih': (int(kasir.total_pelunasan_otorisasi())),
            'nilai_dibayar':int(sum([a.nilai for a in plns])),
            'sisa_bayar': (int(kasir.total_pelunasan_otorisasi()))})

    elif ttp >= 1: 
        form = KasirGeraiPelunasanForm(initial={'status': 1,'nilai':int(kasir.nilai),'kasir':kasir,'tanggal':sekarang,
            'nilai_terima_bersih': (int(kasir.nilai) + int(kasir.hitung_jasa_pelunasan()) + int(kasir.hitung_denda_pelunasan()) \
                - int(kasir.nilai_pelunasan()) + int(kasir.lunas_denda_all()) + int(kasir.lunas_jasa_all())),
            'nilai_yg_dibayar':int(kasir.selisih_pelunasan),
            'nilai_dibayar':int(nilai_titipan),
            'sisa_bayar': (int(kasir.nilai) + int(kasir.hitung_jasa_pelunasan()) + int(kasir.hitung_denda_pelunasan()))\
                 - (int(kasir.nilai_pelunasan()) + int(kasir.lunas_jasa_all()) + int(kasir.lunas_denda_all())) - int(nilai_titipan)})
    else: 
        form = KasirGeraiPelunasanForm(initial={'status': 1,'nilai':int(kasir.nilai),'kasir':kasir,'tanggal':sekarang,
            'nilai_terima_bersih': (int(kasir.nilai) + int(kasir.hitung_jasa_pelunasan()) + int(kasir.hitung_denda_pelunasan()) \
                - int(kasir.nilai_pelunasan()) + int(kasir.lunas_denda_all()) + int(kasir.lunas_jasa_all())),
            #'nilai_terima_bersih': (int(kasir.nilai) + int(kasir.denda_plns_baru()) + int(kasir.hitung_jasa_pelunasan())),
            'nilai_yg_dibayar':int(kasir.selisih_pelunasan),
            'nilai_dibayar':int(sum([a.nilai for a in plns])),
            'sisa_bayar': (int(kasir.nilai) + int(kasir.hitung_jasa_pelunasan()) + int(kasir.hitung_denda_pelunasan()))\
                 - (int(kasir.nilai_pelunasan()) + int(kasir.lunas_jasa_all()) + int(kasir.lunas_denda_all()))})
    template = 'kasir/kasir_pelunasan.html'
    variable = RequestContext(request, {'kasir': kasir,'form':form,'plns':plns,'pembayaran':pembayaran,'titip':titip,'nilai_titipan':nilai_titipan,
        'status':status,'pengembalian':pengembalian,'bayar':bayar,'total': int(sum([a.nilai for a in plns]))})
    return render_to_response(template,variable)

def inputkasir_pelunasan(request, object_id):
    user = request.user
    sekarang = datetime.date.today()
    kasir = AkadGadai.objects.get(id=object_id)
    plns = Pelunasan.objects.filter(pelunasan_id = kasir.id)
    titip = TitipanPelunasan.objects.filter(norek = object_id)
    ttp = titip.count()
    nilai_titipan = sum([a.nilai for a in titip])
    if request.method == 'POST':
        f =  KasirGeraiPelunasanForm(request.POST)
        if f.is_valid():
            tanggal = f.cleaned_data['tanggal']
            jenis_transaksi = f.cleaned_data['jenis_transaksi']
            nilai_terima_bersih = f.cleaned_data['nilai_terima_bersih']            
            selisih = f.cleaned_data['selisih']
            nilai_pembulatan = f.cleaned_data['nilai_pembulatan']
            nilai_dibayar = f.cleaned_data['nilai_dibayar']
            kelebihan_transfer = f.cleaned_data['kelebihan_transfer']
            kelebihan = f.cleaned_data['kelebihan']
           
            sisa_bayar = f.cleaned_data['sisa_bayar']
            kasir.selisih_pelunasan = selisih
            kasir.status_kwlunas  = 0
            kasir.save()

            if ttp == 0 : 
                ks = KasirGeraiPelunasan(kasir_lunas_id = kasir.id, status = 1, tanggal =tanggal, nilai_pembulatan_lunas = nilai_pembulatan,\
                    selisih_lunas = selisih, jenis_transaksi_lunas = jenis_transaksi, coa_sisa = '0', val_lunas =0,\
                    sisa_bayar_lunas = sisa_bayar, rek_tab = 0, cu = user, mu = user,nilai_titipan = nilai_pembulatan)
                ks.save()
                ####COBA
                if kelebihan > 0 and kelebihan_transfer > 0 and ks.jenis_transaksi_lunas == u'2' and ks.selisih_lunas > 0 and ks.kasir_lunas.gerai == user.profile.gerai:
                    jurnal_bank_jkt_plns_kelebihan_transfer_pendapatan(ks,kelebihan,kelebihan_transfer, request.user)
                    akad = AkadGadai.objects.get(id = ks.kasir_lunas.id)
                    akad.status_kwlunas  = 0
                    akad.save()
                    if kelebihan_transfer > 0 :
                        lebih = TitipanPelunasan(norek = ks.kasir_lunas_id,gerai = ks.kasir_lunas.gerai,nilai=kelebihan_transfer,status = 2,\
                            tanggal=tanggal,cu=user,mu=user)
                        lebih.save()

                    messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING LEBIH BANK TITIPAN 1283 ###.')
                if kelebihan == 0 and kelebihan_transfer > 0 and ks.jenis_transaksi_lunas == u'2' and ks.selisih_lunas > 0 and ks.kasir_lunas.gerai == user.profile.gerai:
                    jurnal_bank_jkt_plns_kelebihan_transfer(ks,kelebihan,kelebihan_transfer, request.user)
                    akad = AkadGadai.objects.get(id = ks.kasir_lunas.id)
                    akad.status_kwlunas  = 0
                    akad.save()
                    if kelebihan_transfer > 0 :
                        lebih = TitipanPelunasan(norek = ks.kasir_lunas_id,gerai = ks.kasir_lunas.gerai,nilai=kelebihan_transfer,status = 2,\
                            tanggal=tanggal,cu=user,mu=user)
                        lebih.save()

                    messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING LEBIH BANK TITIPAN 1295 ###.')
                if kelebihan > 0 and kelebihan_transfer == 0 and ks.jenis_transaksi_lunas == u'2' and ks.selisih_lunas > 0 and ks.kasir_lunas.gerai == user.profile.gerai:
                    jurnal_bank_jkt_plns_pendapatan(ks,kelebihan,kelebihan_transfer, request.user)
                    akad= AkadGadai.objects.get(id = ks.kasir_lunas.id)
                    akad.status_kwlunas  = 0
                    akad.save()
                    if kelebihan_transfer > 0 :
                        lebih = TitipanPelunasan(norek = ks.kasir_lunas_id,gerai = ks.kasir_lunas.gerai,nilai=kelebihan_transfer,status = 2,\
                            tanggal=tanggal,cu=user,mu=user)
                        lebih.save()

                    messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING LEBIH BANK TITIPAN 1306 ###.')
                ###AKHIR COBA
                ###jurnal Pelunasan Bank
                if kelebihan <= 0 and kelebihan_transfer <= 0 and ks.jenis_transaksi_lunas == u'2' and ks.selisih_lunas > 0 and ks.kasir_lunas.gerai == user.profile.gerai:
                    jurnal_bank_jkt_plns_lebih(ks, request.user)
                    akad = AkadGadai.objects.get(id = ks.kasir_lunas.id)
                    akad.status_kwlunas  = 0
                    akad.save()
                    messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING LEBIH BANK 1031###.')
                elif ks.jenis_transaksi_lunas == u'2' and ks.selisih_lunas == 0  and ks.kasir_lunas.gerai == user.profile.gerai:
                    jurnal_bank_jkt_plns_sama(ks, request.user)
                    akad = AkadGadai.objects.get(id = ks.kasir_lunas.id)
                    akad.status_kwlunas  = 0
                    akad.save()
                    messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING SAMA BANK 1037###.')
                elif ks.jenis_transaksi_lunas == u'2' and ks.selisih_lunas < 0  and ks.selisih_lunas >= -1000  and \
                    ks.kasir_lunas.gerai == user.profile.gerai:
                    jurnal_kas_jkt_plns_kurang_eror(ks, request.user)
                    #jurnal_bank_jkt_plns_kurang(ks, request.user)
                    akad = AkadGadai.objects.get(id = ks.kasir_lunas.id)
                    akad.status_kwlunas  = 0
                    akad.save()
                    messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING KURANG BANK 1043 ###.')
                elif ks.jenis_transaksi_lunas == u'2' and ks.selisih_lunas < 0  and ks.selisih_lunas < -1000 and \
                    ks.kasir_lunas.gerai == user.profile.gerai:
                    #####titipan pelunasan
                    titip=TitipanPelunasan(norek = ks.kasir_lunas_id,gerai = ks.kasir_lunas.gerai,nilai=nilai_pembulatan,status = 1,\
                        tanggal=tanggal,cu=user,mu=user)
                    titip.save()
                    akad = AkadGadai.objects.get(id = ks.kasir_lunas.id)
                    akad.status_kwlunas  = ''
                    akad.save()
                    jurnal_bank_jkt_plns_rpp(ks, request.user)

                    if kelebihan_transfer > 0 :
                        lebih = TitipanPelunasan(norek = ks.kasir_lunas_id,gerai = ks.kasir_lunas.gerai,nilai=kelebihan_transfer,status = 2,\
                            tanggal=tanggal,cu=user,mu=user)
                        lebih.save()
                    messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING KURANG BANK 1053###.')

                ###coba RAK
                if kelebihan > 0 and kelebihan_transfer > 0 and ks.jenis_transaksi_lunas == u'2' and ks.selisih_lunas > 0 and ks.kasir_lunas.gerai != user.profile.gerai:
                    jurnal_bank_jkt_plns_barakatak(ks,kelebihan,kelebihan_transfer, request.user)
                    akad = AkadGadai.objects.get(id = ks.kasir_lunas.id)
                    akad.status_kwlunas  = 0
                    akad.save()
                    if kelebihan_transfer > 0 :
                        lebih = TitipanPelunasan(norek = ks.kasir_lunas_id,gerai = ks.kasir_lunas.gerai,nilai=kelebihan_transfer,status = 2,\
                            tanggal=tanggal,cu=user,mu=user)
                        lebih.save()

                    messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING LEBIH BANK TITIPAN RAK 1356 ###.')
                if kelebihan == 0 and kelebihan_transfer > 0 and ks.jenis_transaksi_lunas == u'2' and ks.selisih_lunas > 0 and ks.kasir_lunas.gerai != user.profile.gerai:
                    jurnal_bank_jkt_plns_barakatak2(ks,kelebihan,kelebihan_transfer, request.user)
                    akad = AkadGadai.objects.get(id = ks.kasir_lunas.id)
                    akad.status_kwlunas  = 0
                    akad.save()
                    if kelebihan_transfer > 0 :
                        lebih = TitipanPelunasan(norek = ks.kasir_lunas_id,gerai = ks.kasir_lunas.gerai,nilai=kelebihan_transfer,status = 2,\
                            tanggal=tanggal,cu=user,mu=user)
                        lebih.save()

                    messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING LEBIH BANK TITIPAN RAK 1367 ###.')
                if kelebihan > 0 and kelebihan_transfer == 0 and ks.jenis_transaksi_lunas == u'2' and ks.selisih_lunas > 0 and ks.kasir_lunas.gerai != user.profile.gerai:
                    jurnal_bank_jkt_plns_barakatak3(ks,kelebihan,kelebihan_transfer, request.user)
                    akad= AkadGadai.objects.get(id = ks.kasir_lunas.id)
                    akad.status_kwlunas  = 0
                    akad.save()
                    if kelebihan_transfer > 0 :
                        lebih = TitipanPelunasan(norek = ks.kasir_lunas_id,gerai = ks.kasir_lunas.gerai,nilai=kelebihan_transfer,status = 2,\
                            tanggal=tanggal,cu=user,mu=user)
                        lebih.save()

                    messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING LEBIH BANK TITIPAN RAK 1378 ###.')

                ###AKHIR COBA
                ###jurnal Pelunasan RAK KASIR BANK
                if kelebihan <= 0 and kelebihan_transfer <= 0 and ks.jenis_transaksi_lunas == u'2' and ks.kasir_lunas.gerai != user.profile.gerai:
                    jurnal_bank_jkt_plns_lebih_rak(ks, request.user)
                    akad = AkadGadai.objects.get(id = ks.kasir_lunas.id)
                    akad.status_kwlunas  = 0
                    akad.save()
                    messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING LEBIH BANK 1063###.')                                       
                          
                ###jurnal Pelunasan kas
                elif ks.jenis_transaksi_lunas == u'1' and ks.selisih_lunas > 0  and ks.kasir_lunas.gerai == user.profile.gerai:
                    jurnal_kas_jkt_plns_lebih(ks, request.user)
                    messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING LEBIH KAS 1060###.')
                elif ks.jenis_transaksi_lunas == u'1' and ks.selisih_lunas == 0  and ks.kasir_lunas.gerai == user.profile.gerai:
                    jurnal_kas_jkt_plns_sama(ks, request.user)
                    messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING SAMA KAS 1063 ###.')
                elif ks.jenis_transaksi_lunas == u'1' and ks.selisih_lunas < 0  and ks.selisih_lunas >= -1000 \
                    and ks.kasir_lunas.gerai == user.profile.gerai:
                    jurnal_kas_jkt_plns_kurang(ks, request.user)
                    messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING KURANG KAS 1066###.')
                elif ks.jenis_transaksi_lunas == u'1' and ks.selisih_lunas < 0  and ks.selisih_lunas < -1000 \
                    and ks.kasir_lunas.gerai == user.profile.gerai:
                    #####titipan pelunasan
                    titip=TitipanPelunasan(norek = ks.kasir_lunas_id,gerai = user.profile.gerai,nilai=nilai_pembulatan,status = 1,\
                        tanggal=tanggal,cu=user,mu=user)
                    titip.save()
                    kasir.status_kwlunas  = ''
                    kasir.save()
                    jurnal_kas_jkt_plns_rpp(ks, request.user)
                    if kelebihan_transfer > 0 :
                        lebih = TitipanPelunasan(norek = ks.kasir_lunas_id,gerai = ks.kasir_lunas.gerai,nilai=kelebihan_transfer,status = 2,\
                            tanggal=tanggal,cu=user,mu=user)
                        lebih.save()
                    messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING KURANG KAS 1075###.')

                ###jurnal Pelunasan kas RAK
                elif ks.jenis_transaksi_lunas == u'1' and ks.kasir_lunas.gerai != user.profile.gerai:
                    jurnal_kas_jkt_plns_lebih_rak(ks, request.user)
                    messages.add_message(request, messages.INFO,'### JURNAL TELAH TERPOSTING LEBIH KAS 1117###.')
                            
            elif ttp > 0 : 
                ks = KasirGeraiPelunasan.objects.get(kasir_lunas = kasir.id)
                ks.kasir_lunas_id = kasir.id
                ks.status = 1
                ks.tanggal =tanggal
                ks.nilai_pembulatan_lunas= nilai_pembulatan #+ nilai_titipan
                ks.selisih_lunas = selisih
                ks.jenis_transaksi_lunas = jenis_transaksi
                ks.coa_sisa = '0'
                ks.val_lunas =0
                ks.sisa_bayar_lunas = sisa_bayar
                ks.nilai_titipan = nilai_pembulatan
                ks.rek_tab = 0
                ks.kasir_lunas.status_kwlunas  = ''
                ks.save()

                titip=TitipanPelunasan(norek = ks.kasir_lunas_id,gerai =user.profile.gerai,nilai=nilai_pembulatan,status = 1,
                    tanggal=tanggal,cu=user,mu=user)
                titip.save()

                if kelebihan_transfer > 0 :
                    lebih = TitipanPelunasan(norek = ks.kasir_lunas_id,gerai = ks.kasir_lunas.gerai,nilai=kelebihan_transfer,status = 2,\
                        tanggal=tanggal,cu=user,mu=user)
                    lebih.save()

                ### Titipan sudah tidak ada atau sudah sama dengan Nol (= 0) Udah
                if ks.selisih_lunas == 0  and ks.kasir_lunas.gerai == user.profile.gerai:
                    if ks.jenis_transaksi_lunas == u'1':
                        jurnal_kas_jkt_plns_titipan_sama(ks, request.user)
                        kasir.status_kwlunas  = 0
                        kasir.save()
                        messages.add_message(request, messages.INFO,'### JURNAL TITIPAN TELAH TERPOSTING KURANG 1103 ###.')
                    elif ks.jenis_transaksi_lunas == u'2' and ks.kasir_lunas.gerai == user.profile.gerai:
                        jurnal_bank_jkt_plns_titipan_sama(ks, request.user)
                        kasir.status_kwlunas  = 0
                        kasir.save()
                        messages.add_message(request, messages.INFO,'### JURNAL TITIPAN BANK TELAH TERPOSTING KURANG 1108 ###.')

                ### Titipan sudah tidak,malah ada Pendapatan Operasional Lainnya atau titipan lebih dari Nol (= 0) Udah
                elif ks.selisih_lunas > 0:
                    if ks.jenis_transaksi_lunas == u'1' and ks.kasir_lunas.gerai == user.profile.gerai:
                        jurnal_kas_jkt_plns_titipan_lebih(ks, request.user)
                        kasir.status_kwlunas  = 0
                        kasir.save()
                        messages.add_message(request, messages.INFO,'### JURNAL TITIPAN TELAH TERPOSTING KURANG 1116 ###.')
                    elif ks.jenis_transaksi_lunas == u'2'  and ks.kasir_lunas.gerai == user.profile.gerai:
                        jurnal_bank_jkt_plns_titipan_lebih(ks, request.user)
                        kasir.status_kwlunas  = 0
                        kasir.save()
                        messages.add_message(request, messages.INFO,'### JURNAL TITIPAN BANK TELAH TERPOSTING KURANG 1121 ###.')
                ### Udah Dianggap Lunas

                elif ks.selisih_lunas < 0  and ks.selisih_lunas >= -1000 and ks.kasir_lunas.gerai == user.profile.gerai:
                    if ks.jenis_transaksi_lunas == u'1':
                        jurnal_kas_jkt_plns_titipan_kurang(ks, request.user)
                        messages.add_message(request, messages.INFO,'### JURNAL TITIPAN TELAH TERPOSTING KURANG 1127 ###.')
                        kasir.status_kwlunas  = 0
                        kasir.save()
                    elif ks.jenis_transaksi_lunas == u'2'  and ks.kasir_lunas.gerai == user.profile.gerai:
                        jurnal_bank_jkt_plns_titipan_kurang(ks, request.user)
                        messages.add_message(request, messages.INFO,'### JURNAL TITIPAN BANK TELAH TERPOSTING KURANG 1132 ###.')
                        kasir.status_kwlunas  = 0
                        kasir.save()
                
                ### Masih ada titipan di atas -1000
                else:
                    if ks.jenis_transaksi_lunas == u'1'  and ks.kasir_lunas.gerai == user.profile.gerai:
                        jurnal_kas_jkt_plns_rpp(ks, request.user)
                        messages.add_message(request, messages.INFO,'### JURNAL TITIPAN TELAH TERPOSTING KURANG 1140 ###.')
                        kasir.status_kwlunas  = ''
                        kasir.save()
                    if ks.jenis_transaksi_lunas == u'2' and ks.kasir_lunas.gerai == user.profile.gerai:
                        jurnal_bank_jkt_plns_rpp(ks, request.user)
                        messages.add_message(request, messages.INFO,'### JURNAL TITIPAN BANK TELAH TERPOSTING KURANG 1145 ###.')
                        kasir.status_kwlunas  = ''
                        kasir.save()
            #messages.add_message(request, messages.INFO,'### DATA KASIR TERPOSTING ###.')
            return HttpResponseRedirect('/')
        else:
            variables = RequestContext(request,{ 'form': f,'kasir':kasir})
            return render_to_response('kasir/kasir_pelunasan.html', variables)
    else:
        form  = KasirGeraiPelunasanForm()
        form.fields['gerai'].queryset = Tbl_Cabang.objects.for_user(user) 
    variables = RequestContext(request, {'form': f,'kasir':kasir,'ks':ks})
    return render_to_response('kasir/kasir_pelunasan.html', variables)


####COBA

def jurnal_bank_jkt_plns_kelebihan_transfer(ks,kelebihan,kelebihan_transfer, user):
    D = decimal.Decimal
    bank = KasirPelunasanMapper.objects.get(item ='10',cabang = user.profile.gerai)
    a_titipan_pelunasan = bank.coa_1
    a_bank = bank.coa_2
    #a_pend_lainnya= bank.coa_3
    a_kelebihan_pend= bank.coa_5

    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang =  user.profile.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_bank,
        kredit = 0,debet = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

    #jurnal.tbl_transaksi_set.create(
        #jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_pend_lainnya,
        #debet = 0,kredit = (kelebihan),id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        #id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_kelebihan_pend,
        debet = 0,kredit = (kelebihan_transfer),id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = ks.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_jkt_plns_kelebihan_transfer_pendapatan(ks,kelebihan,kelebihan_transfer, user):
    D = decimal.Decimal
    bank = KasirPelunasanMapper.objects.get(item ='11',cabang = user.profile.gerai)
    a_titipan_pelunasan = bank.coa_1
    a_bank = bank.coa_2
    a_pend_lainnya= bank.coa_3
    a_kelebihan_pend= bank.coa_5

    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang =  user.profile.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_bank,
        kredit = 0,debet = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_pend_lainnya,
        debet = 0,kredit = (kelebihan),id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_kelebihan_pend,
        debet = 0,kredit = (kelebihan_transfer),id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = ks.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_jkt_plns_pendapatan(ks,kelebihan,kelebihan_transfer, user):
    D = decimal.Decimal
    bank = KasirPelunasanMapper.objects.get(item ='9',cabang = user.profile.gerai)
    a_titipan_pelunasan = bank.coa_1
    a_bank = bank.coa_2
    a_pend_lainnya= bank.coa_3
    #a_kelebihan_pend= bank.coa_5

    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang =  user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_bank,
        kredit = 0,debet = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_pend_lainnya,
        debet = 0,kredit = (kelebihan),id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

    #jurnal.tbl_transaksi_set.create(
        #jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_kelebihan_pend,
        #debet = 0,kredit = (kelebihan),id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        #id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
 
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = ks.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
####AKHIRCOBA


#####jurnal pelunasan bank jakarta    
def jurnal_bank_jkt_plns_lebih(ks, user):
    D = decimal.Decimal
    bank = KasirPelunasanMapper.objects.get(item ='1',cabang = user.profile.gerai)
    a_titipan_pelunasan = bank.coa_1
    a_bank = bank.coa_2
    a_pend_lainnya= bank.coa_3

    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang =  user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_bank,
        kredit = 0,debet = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_pend_lainnya,
        debet = 0,kredit = (ks.selisih_lunas),id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = ks.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_jkt_plns_sama(ks, user):
    D = decimal.Decimal
    bank = KasirPelunasanMapper.objects.get(item ='2',cabang = user.profile.gerai)
    a_titipan_pelunasan = bank.coa_1
    a_bank = bank.coa_2
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang = user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_bank,
        kredit = 0,debet = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
       
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = ks.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)


##### RAK LEBIH
def jurnal_bank_jkt_plns_lebih_rak(ks, user):
    D = decimal.Decimal
    bank = KasirPelunasanRakMapper.objects.get(item ='1',jenis=u'1',cabang = user.profile.gerai, ke_cabang =ks.kasir_lunas.gerai )
    a_bank = bank.coa_2
    a_pendapatan_lain = bank.coa_3
    a_rak_cabang = bank.debet_rak_cabang
    a_rak_kecabang = bank.kredit_rak_pusat
    a_titipan = bank.coa_1
    a_rak_debet_pusat = bank.rak_debet_pusat1
    a_rak_kredit_pusat = bank.rak_kredit_pusat2

    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns RAK: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang = user.profile.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank_rak"), id_coa = a_bank,
        kredit = 0,debet = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

       
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank_rak"), id_coa = a_rak_cabang,
        debet = 0,kredit = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
    
    #####CABANG TJ
    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns RAK: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang = ks.kasir_lunas.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank_rak1"), id_coa = a_rak_kecabang,
        kredit = 0,debet = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = ks.kasir_lunas.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank_rak1"), id_coa = a_rak_cabang,
        debet = 0,kredit = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = ks.kasir_lunas.gerai.kode_cabang,id_unit= 300)

    ####RAK PUSAT
    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns RAK: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang = user.profile.gerai.parent.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank_pusat_rak"), id_coa = a_rak_debet_pusat,
        kredit = 0,debet = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.parent.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank_pusat_rak"), id_coa = a_rak_kredit_pusat,
        debet = 0,kredit = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.parent.kode_cabang,id_unit= 300)
    
def jurnal_bank_jkt_plns_kurang(ks, user):
    D = decimal.Decimal
    bank = KasirPelunasanMapper.objects.get(item ='3',cabang = user.profile.gerai)
    a_titipan_pelunasan = bank.coa_1
    a_bank = bank.coa_2
    a_beban_lainnya= bank.coa_4
    a_rak_cabang = bank.debet_rak_cabang
    a_rak_kecabang = bank.kredit_rak_pusat
    a_titipan = bank.coa_1

    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns RAK: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang = ks.kasir_lunas.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank_rak"), id_coa = a_bank,
        kredit = 0,debet = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank_bol_rak"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * ks.selisih_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
        
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank_rak"), id_coa = a_rak_cabang,
        debet = 0,kredit = (ks.nilai_pembulatan_lunas) +(-1 * ks.selisih_lunas),id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

###01 oktober 2016
def jurnal_kas_jkt_plns_kurang_eror(ks, user):
    D = decimal.Decimal
    kas = KasirPelunasanMapper.objects.get(item ='3',cabang = user.profile.gerai)
    a_titipan_pelunasan = kas.coa_1
    a_kas = kas.coa_2
    a_beban_lainnya= kas.coa_4

    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang = user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir"), id_coa = a_kas,
        kredit = 0,debet = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_kurang"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * ks.selisih_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
        
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = (ks.nilai_pembulatan_lunas)+(-1 * ks.selisih_lunas),id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)


def jurnal_bank_jkt_plns_titipan_sama(ks, user):
    D = decimal.Decimal
    bank = KasirPelunasanMapper.objects.get(item ='2',cabang = user.profile.gerai)
    a_titipan_pelunasan = bank.coa_1
    a_bank = bank.coa_2

    jurnal = Jurnal.objects.create(
        diskripsi= 'Setoran Titipan Plns: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang = user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_bank,
        kredit = 0,debet = ks.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
      
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = ks.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)


def jurnal_bank_jkt_plns_titipan_lebih(ks, user):
    D = decimal.Decimal
    bank = KasirPelunasanMapper.objects.get(item ='1',cabang = user.profile.gerai)
    a_titipan_pelunasan = bank.coa_1
    a_bank = bank.coa_2
    a_pend_lainnya= bank.coa_3
 
    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans = ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang = user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_bank,
        kredit = 0,debet = (ks.selisih_lunas + ks.sisa_bayar_lunas)  ,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_pend_lainnya,
        debet = 0,kredit = (ks.selisih_lunas),id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = ks.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_jkt_plns_titipan_kurang(ks, user):
    D = decimal.Decimal
    bank = KasirPelunasanMapper.objects.get(item ='3',cabang = user.profile.gerai)
    a_titipan_pelunasan = bank.coa_1
    a_bank = bank.coa_2
    a_beban_lainnya= bank.coa_4

    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang = user.profile.gerai.kode_cabang )
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_bank,
        kredit = 0,debet = ks.sisa_bayar_lunas -( -1 * ks.selisih_lunas),id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank_bol"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * ks.selisih_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
        
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = ks.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_jkt_plns_rpp(ks, user):
    D = decimal.Decimal
    bank = KasirPelunasanMapper.objects.get(item ='8',cabang = user.profile.gerai)
    a_titipan_pelunasan = bank.coa_1
    a_bank = bank.coa_2
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Setoran Titipan Plns: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang = user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_bank,
        kredit = 0,debet = ks.nilai_titipan,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
        
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_bank"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = ks.nilai_titipan,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300) 

#####jurnal pencairan bank
### Jurnal pelunasan Kas RAK
def jurnal_kas_jkt_plns_lebih_rak(ks, user):
    D = decimal.Decimal
    kas = KasirPelunasanRakMapper.objects.get(item ='1', jenis = u'2',cabang = user.profile.gerai,ke_cabang = ks.kasir_lunas.gerai)
    a_kas = kas.coa_2
    a_pend_lainnya= kas.coa_3
    a_debet_rak_cabang = kas.debet_rak_cabang
    a_kredit_rak_pusat = kas.kredit_rak_pusat
    a_titipan_pelunasan = kas.coa_1
    a_rak_debet_pusat = kas.rak_debet_pusat1
    a_rak_kredit_pusat = kas.rak_kredit_pusat2
 
    ### Cabang 
    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns RAK : NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang =  user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_rak"), id_coa = a_kas,
        kredit = 0,debet = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
    
        
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_rak"), id_coa = a_pend_lainnya,
        debet = 0,kredit = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)

    ### Cabang Tuju
    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns RAK : NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang =  ks.kasir_lunas.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_rak1"), id_coa = a_debet_rak_cabang,
        debet = ks.nilai_pembulatan_lunas,kredit = 0,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = ks.kasir_lunas.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_rak1"), id_coa = a_kredit_rak_pusat,
        debet = 0,kredit = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = ks.kasir_lunas.gerai.kode_cabang,id_unit= 300)

    ####RAK PUSAT
    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns RAK: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang = user.profile.gerai.parent.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_kas_rak"), id_coa = a_rak_debet_pusat,
        kredit = 0,debet = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.parent.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_kas_rak"), id_coa = a_rak_kredit_pusat,
        debet = 0,kredit = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.parent.kode_cabang,id_unit= 300)


## Akhir Jurnal Kas RAK
#####jurnal pelunasan kas jakarta
def jurnal_kas_jkt_plns_titipan_sama(ks, user):
    D = decimal.Decimal
    kas = KasirPelunasanMapper.objects.get(item ='5',cabang = user.profile.gerai)
    a_titipan_pelunasan = kas.coa_1
    a_kas = kas.coa_2
    a_pend_lainnya= kas.coa_3

    jurnal = Jurnal.objects.create(
        diskripsi= 'Setoran Titipan Plns: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang = user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir"), id_coa = a_kas,
        kredit = 0,debet = ks.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
      
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = ks.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

def jurnal_kas_jkt_plns_titipan_lebih(ks, user):
    D = decimal.Decimal
    kas = KasirPelunasanMapper.objects.get(item ='4',cabang = user.profile.gerai)
    a_titipan_pelunasan = kas.coa_1
    a_kas = kas.coa_2
    a_pend_lainnya= kas.coa_3
 
    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang = user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir"), id_coa = a_kas,
        kredit = 0,debet = (ks.selisih_lunas + ks.sisa_bayar_lunas)  ,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir"), id_coa = a_pend_lainnya,
        debet = 0,kredit = (ks.selisih_lunas),id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = ks.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)


def jurnal_kas_jkt_plns_titipan_kurang(ks, user):
    D = decimal.Decimal
    kas = KasirPelunasanMapper.objects.get(item ='6',cabang = user.profile.gerai)
    a_titipan_pelunasan = kas.coa_1
    a_kas = kas.coa_2
    a_beban_lainnya= kas.coa_4

    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang = user.profile.gerai.kode_cabang )
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir"), id_coa = a_kas,
        kredit = 0,debet = ks.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_kurang"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * ks.selisih_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
        
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = ks.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300) 


def jurnal_kas_jkt_plns_lebih(ks, user):
    D = decimal.Decimal
    kas = KasirPelunasanMapper.objects.get(item ='4',cabang = user.profile.gerai)
    a_titipan_pelunasan = kas.coa_1
    a_kas = kas.coa_2
    a_pend_lainnya= kas.coa_3
 
    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang =  user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir"), id_coa = a_kas,
        kredit = 0,debet = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir"), id_coa = a_pend_lainnya,
        debet = 0,kredit = (ks.selisih_lunas),id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = ks.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
    
def jurnal_kas_jkt_plns_sama(ks, user):
    D = decimal.Decimal
    kas = KasirPelunasanMapper.objects.get(item ='5',cabang = user.profile.gerai)
    a_titipan_pelunasan = kas.coa_1
    a_kas = kas.coa_2
    a_pend_lainnya= kas.coa_3

    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang =  user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir"), id_coa = a_kas,
        kredit = 0,debet = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
      
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = ks.sisa_bayar_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
    
def jurnal_kas_jkt_plns_kurang(ks, user):
    D = decimal.Decimal
    kas = KasirPelunasanMapper.objects.get(item ='6',cabang = user.profile.gerai)
    a_titipan_pelunasan = kas.coa_1
    a_kas = kas.coa_2
    a_beban_lainnya= kas.coa_4

    jurnal = Jurnal.objects.create(
        diskripsi= 'Plns: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang = user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir"), id_coa = a_kas,
        kredit = 0,debet = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir_kurang"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * ks.selisih_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
        
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = (ks.nilai_pembulatan_lunas)+(-1 * ks.selisih_lunas),id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)      

def jurnal_kas_jkt_plns_rpp(ks, user):
    D = decimal.Decimal
    kas = KasirPelunasanMapper.objects.get(item ='7',cabang = user.profile.gerai)
    a_titipan_pelunasan = kas.coa_1
    a_kas = kas.coa_2
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Setoran Titipan Plns: NoRek: %s an: %s  ' % (ks.kasir_lunas.norek(), ks.kasir_lunas.agnasabah.nama),
        tgl_trans =ks.tanggal,nobukti=ks.kasir_lunas.norek(),cu = user,mu =user,object_id = ks.id,
        kode_cabang =  user.profile.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir"), id_coa = a_kas,
        kredit = 0,debet = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)
        
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_kasir"), id_coa = a_titipan_pelunasan,
        debet = 0,kredit = ks.nilai_pembulatan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ks.tanggal,
        id_cabang = user.profile.gerai.kode_cabang,id_unit= 300)


##################batas akhir jurnal kas kasir pelunasan

@login_required
@user_passes_test(lambda u: u.groups.filter(name='ADM_GERAI'))
def data_approve(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    view = AkadGadai.objects.filter(gerai__kode_cabang=cab,status_transaksi = 3)
    return render(request,'kasir/view/data_approve.html',{'view':view})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='ADM_GERAI'))
def lunas(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    sekarang = datetime.date.today()
    akad = Pelunasan.objects.filter(gerai__kode_cabang=cab).exclude(pelunasan__sts_tdr='1')
    paginator = Paginator(akad, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        akad = paginator.page(page)
    except (EmptyPage, InvalidPage):
        akad_list = paginator.page(paginator.num_pages)
    return render(request,'kasir/view/data_lunas.html',{'akad':akad})   

 
@login_required
@user_passes_test(lambda u: u.groups.filter(name='ADM_GERAI'))
def kwitansi_gu_adm(request):
    sekarang = datetime.date.today()
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    akad = AkadGadai.objects.filter(gerai__kode_cabang=cab,tanggal = sekarang,kepalagerai__status ='1',kasirgerai__status = '1')
    return render(request,'kasir/view/data_lunas_gu.html',{'akad':akad})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def data_lunas_kasir(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    sekarang = datetime.date.today()
    akad1 = KasirGeraiPelunasan.objects.filter(kasir_lunas__gerai__kode_cabang = cab,kasir_lunas__status_kwlunas = '0',tanggal = sekarang).order_by('-tanggal')
    return render(request,'kasir/view/data_lunas_kasir.html',{'akad1':akad1})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def mastertiket_gl_gl(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    sekarang = datetime.date.today()
    cabang = Tbl_Cabang.objects.get(kode_cabang=cab)
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=cab).filter(status_jurnal=u'2').\
        filter(jenis__in=('GL_GL_PUSAT','GL_GL_NON_KAS','GL_GL_CABANG'))
    template = 'kasir/tiket/mastertiketgl_gl.html'
    variables = RequestContext(request, {'cabang':cabang,'user':User,'g':gr,'total_debet': sum([p.debet for p in gr]),\
        'total_kredit': sum([p.kredit for p in gr])})
    return render_to_response(template, variables)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def mastertiket_pencairan_kasir(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    sekarang = datetime.date.today()
    cabang = Tbl_Cabang.objects.get(kode_cabang=cab)
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=cab).filter(status_jurnal=u'2').filter(jenis=u'Pencairan_kasir')
    template = 'kasir/tiket/mastertiket_pencairan_uji_coba.html'
    variables = RequestContext(request, {'cabang':cabang,'user':User,'g':gr,'total_debet': sum([p.debet for p in gr]),'total_kredit': sum([p.kredit for p in gr])})
    return render_to_response(template, variables)

def mastertiket_uji_coba_kasir(request,object_id):
    if 'dari' in request.GET and request.GET['hingga']:
        dari = request.GET['dari']
        hingga = request.GET['hingga']
        gr = Tbl_Transaksi.objects.filter(tgl_trans__range=(dari,hingga)).filter(id_cabang=object_id).filter(status_jurnal= '2').\
            filter(jenis__in=('Pencairan_kasir','Pencairan_kasir_sisa','Pencairan_kasir_kurang','Pencairan_kasir_bank',\
            'Pencairan_kasir_lebih_bank','Pencairan_kasir_kurang_bank_kecil','Pencairan_kasir_kurang_bank'))  
    else:
        gr = Tbl_Transaksi.objects.all()
    variables = RequestContext(request, {'g': gr,'cabang':Tbl_Cabang.objects.get(kode_cabang=object_id),'g':gr,'total_debet': sum([p.debet for p in gr]),'total_kredit': sum([p.kredit for p in gr])})
    return render_to_response('kasir/tiket/mastertiket_pencairan.html', variables)

def kasir(request, object_id):
    sekarang = datetime.date.today
    kasir = AkadGadai.objects.get(id=object_id)
    form = KasirGeraiForm(initial={'status': 1,'kasir': kasir.id,'no_pinjaman':kasir.norek,'tanggal':sekarang,'nilai':int(kasir.nilai),
        'nilai_terima_bersih':int(kasir.terima_bersih_all())})
    form.fields['kasir'].widget = forms.HiddenInput()
    form.fields['kasir_lunas'].widget = forms.HiddenInput()
    form.fields['status'].widget = forms.HiddenInput()
    
    template = 'kasir/kasir.html'
    variable = RequestContext(request, {'kasir': kasir,'form': form})
    return render_to_response(template,variable) 
    
@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def inputkasir(request, object_id):
    kasir = AkadGadai.objects.get(id=object_id)
    if request.method == 'POST':
        f =  KasirGeraiCairForm(request.POST)
        if f.is_valid():
            tanggal = f.cleaned_data['tanggal']
            status = f.cleaned_data['status']
            jenis_transaksi = f.cleaned_data['jenis_transaksi']
            nilai = f.cleaned_data['nilai']
            nilai_pembulatan = f.cleaned_data['nilai_pembulatan']
            selisih = f.cleaned_data['selisih']
            sisa_bayar = f.cleaned_data['sisa_bayar']
            rek_tab = f.cleaned_data['rek_tab']
            messages.add_message(request, messages.INFO,'### DATA KASIR TERPOSTING ###.')
            ks = KasirGerai(tanggal=tanggal,kasir=kasir,jenis_transaksi=jenis_transaksi,status=status,nilai_pembulatan=nilai_pembulatan,\
                 selisih=selisih,coa_sisa ='41.04.99', val = 0 ,sisa_bayar =0 ,rek_tab = rek_tab)
            ks.save()

            #params = '{"to":"%s", "msg":"%s"}' % (ks.kasir.agnasabah.hp_ktp,ks.kasir.sms())
            #headers = {"Content-Type": "application/json"}
            #conn = httplib.HTTPConnection("103.10.171.125")
            #conn.request("POST", "/api/sms/", params, headers)
            ###bank pencairan
            if ks.jenis_transaksi == u'2' and ks.selisih == 0:
                jurnal_bank_jkt_sama(ks, request.user)
                messages.add_message(request, messages.INFO,'### MAPPER BANK KASIR SAMA TERPOSTING ###.')
            elif ks.jenis_transaksi == u'2' and ks.selisih < 0:
                jurnal_bank_jkt_kecil(ks, request.user)    
                messages.add_message(request, messages.INFO,'### MAPPER BANK KASIR KECIL TERPOSTING ###.')
            elif ks.jenis_transaksi == u'2' and ks.selisih > 0:
                jurnal_bank_jkt_besar(ks, request.user)
                messages.add_message(request, messages.INFO,'### MAPPER BANK KASIR BESAR TERPOSTING ###.')               
          
            ###kas pencairan
            if ks.jenis_transaksi == u'1' and ks.selisih == 0:
                jurnal_kas_jkt_sama(ks, request.user)
                messages.add_message(request, messages.INFO,'### MAPPER KASS KASIR SAMA TERPOSTING ###.')
            elif ks.jenis_transaksi == u'1' and ks.selisih < 0:
                jurnal_kas_jkt_kecil(ks, request.user)
                messages.add_message(request, messages.INFO,'### MAPPER KASS KASIR KECIL TERPOSTING ###.')
            elif ks.jenis_transaksi == u'1' and ks.selisih > 0:
                jurnal_kas_jkt_besar(ks, request.user)
                messages.add_message(request, messages.INFO, '### MAPPER KASS KASIR BESAR TERPOSTING ###.')
            return HttpResponseRedirect('/')
        else:
            variables = RequestContext(request, {'object': kasir, 'form': f})
            return render_to_response('kasir/kasir.html', variables)

def jurnal_kas_jkt_sama(ks, user):
    D = decimal.Decimal
    bm = KasirPencairanMapper.objects.get(item='pencairan_kas_sama', cabang=user.profile.gerai)
    a_titipan_pencairan = bm.coa_debet #get_object_or_404(Tbl_Akun, id=298L)
    a_kas = bm.coa_kredit #get_object_or_404(Tbl_Akun, id=7L)
    #a_pdp_ops_lain = bm.coa_kredit_satu #get_object_or_404(Tbl_Akun, id =448L)

    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek(),kode_cabang = ks.kasir.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_kas,
        kredit = ks.nilai_pembulatan,debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
 
def jurnal_kas_jkt_besar(ks, user):
    D = decimal.Decimal
    bm = KasirPencairanMapper.objects.get(item='pencairan_kas_nilai_besar', cabang=user.profile.gerai)
    a_titipan_pencairan = bm.coa_debet #get_object_or_404(Tbl_Akun, id=298L)
    a_kas = bm.coa_kredit #get_object_or_404(Tbl_Akun, id=7L)
    a_pdp_ops_lain = bm.coa_kredit_satu #get_object_or_404(Tbl_Akun, id =448L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek(),kode_cabang = ks.kasir.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_pdp_ops_lain,
        kredit = (ks.selisih),debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_kas,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
def jurnal_kas_jkt_kecil(ks, user):###teddy
    D = decimal.Decimal
    bm = KasirPencairanMapper.objects.get(item='pencairan_kas_nilai_kecil', cabang=user.profile.gerai)
    a_titipan_pencairan = bm.coa_debet #get_object_or_404(Tbl_Akun, id=298L)
    a_kas = bm.coa_kredit #get_object_or_404(Tbl_Akun, id=7L)
    a_beban_lainnya = bm.coa_debet_satu#get_object_or_404(Tbl_Akun, id=539L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek(),kode_cabang = ks.kasir.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir_kurang"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * (ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_kas,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
####refisi tanggal 8.12.2014
def jurnal_bank_jkt_sama(ks, user):
    D = decimal.Decimal
    bm = KasirPencairanBankMapper.objects.get(item='pencairan_bank_sama', cabang=user.profile.gerai)
    a_titipan_pencairan = bm.coa_debet #get_object_or_404(Tbl_Akun, id=298L)
    a_bank = bm.coa_kredit #get_object_or_404(Tbl_Akun, id=7L)
    #a_pdp_ops_lain = bm.coa_kredit_satu #get_object_or_404(Tbl_Akun, id =448L)

    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek(),kode_cabang = ks.kasir.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir_bank"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir_bank"), id_coa = a_bank,
        kredit = ks.nilai_pembulatan,debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_jkt_kecil(ks, user):###teddy
    D = decimal.Decimal
    bm = KasirPencairanBankMapper.objects.get(item='pencairan_bank_nilai_kecil', cabang=user.profile.gerai)
    a_titipan_pencairan = bm.coa_debet #get_object_or_404(Tbl_Akun, id=298L)
    a_bank = bm.coa_kredit #get_object_or_404(Tbl_Akun, id=7L)
    a_beban_lainnya = bm.coa_debet_satu#get_object_or_404(Tbl_Akun, id=539L)

    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek(),kode_cabang = ks.kasir.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir_kurang_bank"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir_kurang_bank_kecil"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * (ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir_kurang_bank"), id_coa = a_bank,
        debet = 0, kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
def jurnal_bank_jkt_besar(ks, user):
    D = decimal.Decimal
    bm = KasirPencairanBankMapper.objects.get(item='pencairan_bank_nilai_besar', cabang=user.profile.gerai)
    a_titipan_pencairan = bm.coa_debet #get_object_or_404(Tbl_Akun, id=298L)
    a_bank = bm.coa_kredit #get_object_or_404(Tbl_Akun, id=7L)
    a_pdp_ops_lain = bm.coa_kredit_satu #get_object_or_404(Tbl_Akun, id =448L)

    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek(),kode_cabang = ks.kasir.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir_lebih_bank"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir_lebih_bank"), id_coa = a_pdp_ops_lain,
        kredit = (ks.selisih),debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir_lebih_bank"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_suci(ks, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=134L)
    a_pdp_ops_lain = get_object_or_404(Tbl_Akun, id =448L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek(),kode_cabang = ks.kasir.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_pdp_ops_lain,
        kredit = (ks.selisih),debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_suci_kecil(ks, user):###teddy
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=134L)
    a_beban_lainnya = get_object_or_404(Tbl_Akun, id=539L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek(),kode_cabang = ks.kasir.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * (ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_du(ks, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=136L)
    a_pdp_ops_lain = get_object_or_404(Tbl_Akun, id =448L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_pdp_ops_lain,
        kredit = (ks.selisih),debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
def jurnal_bank_du_kecil(ks, user):###teddy
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=136L)
    a_beban_lainnya = get_object_or_404(Tbl_Akun, id=539L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * (ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
def jurnal_bank_balubur(ks, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=141L)
    a_pdp_ops_lain = get_object_or_404(Tbl_Akun, id =448L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_pdp_ops_lain,
        kredit = (ks.selisih),debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_balubur_kecil(ks, user):###teddy
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=141L)
    a_beban_lainnya = get_object_or_404(Tbl_Akun, id=539L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * (ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
def jurnal_bank_gh(ks, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=137L)
    a_pdp_ops_lain = get_object_or_404(Tbl_Akun, id =448L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_pdp_ops_lain,
        kredit = (ks.selisih),debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
def jurnal_bank_gh_kecil(ks, user):###teddy
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=137L)
    a_beban_lainnya = get_object_or_404(Tbl_Akun, id=539L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * (ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
def jurnal_bank_kopo(ks, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=138L)
    a_pdp_ops_lain = get_object_or_404(Tbl_Akun, id =448L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_pdp_ops_lain,
        kredit = (ks.selisih),debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_kopo_kecil(ks, user):###teddy
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=138L)
    a_beban_lainnya = get_object_or_404(Tbl_Akun, id=539L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * (ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
def jurnal_bank_cbr(ks, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=135L)
    a_pdp_ops_lain = get_object_or_404(Tbl_Akun, id =448L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_pdp_ops_lain,
        kredit = (ks.selisih),debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_cbr_kecil(ks, user):###teddy
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=135L)
    a_beban_lainnya = get_object_or_404(Tbl_Akun, id=539L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * (ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
def jurnal_bank_cipacing(ks, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=139L)
    a_pdp_ops_lain = get_object_or_404(Tbl_Akun, id =448L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_pdp_ops_lain,
        kredit = (ks.selisih),debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
def jurnal_bank_cipacing_kecil(ks, user):###teddy
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=139L)
    a_beban_lainnya = get_object_or_404(Tbl_Akun, id=539L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * (ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
def jurnal_bank_jatinangor(ks, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=140L)
    a_pdp_ops_lain = get_object_or_404(Tbl_Akun, id =448L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_pdp_ops_lain,
        kredit = (ks.selisih),debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_jatinangor_kecil(ks, user):###teddy
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=140L)
    a_beban_lainnya = get_object_or_404(Tbl_Akun, id=539L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * (ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_cimahi(ks, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=142L)
    a_pdp_ops_lain = get_object_or_404(Tbl_Akun, id =448L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_pdp_ops_lain,
        kredit = (ks.selisih),debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_cimahi_kecil(ks, user):###teddy
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=142L)
    a_beban_lainnya = get_object_or_404(Tbl_Akun, id=539L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * (ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_bubat(ks, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=148L)
    a_pdp_ops_lain = get_object_or_404(Tbl_Akun, id =448L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_pdp_ops_lain,
        kredit = (ks.selisih),debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_bubat_kecil(ks, user):###teddy
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=148L)
    a_beban_lainnya = get_object_or_404(Tbl_Akun, id=539L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * (ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
        
def jurnal_bank_cihanjuang(ks, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=143L)
    a_pdp_ops_lain = get_object_or_404(Tbl_Akun, id =448L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_pdp_ops_lain,
        kredit = (ks.selisih),debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_cihanjuang_kecil(ks, user):###teddy
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=143L)
    a_beban_lainnya = get_object_or_404(Tbl_Akun, id=539L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * (ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
def jurnal_bank_maranata(ks, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=144L)
    a_pdp_ops_lain = get_object_or_404(Tbl_Akun, id =448L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_pdp_ops_lain,
        kredit = (ks.selisih),debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_maranata_kecil(ks, user):###teddy
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=144L)
    a_beban_lainnya = get_object_or_404(Tbl_Akun, id=539L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * (ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

    
def jurnal_bank_crbp(ks, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=147L)
    a_pdp_ops_lain = get_object_or_404(Tbl_Akun, id =448L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_pdp_ops_lain,
        kredit = (ks.selisih),debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
def jurnal_bank_crbp_kecil(ks, user):###teddy
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=147L)
    a_beban_lainnya = get_object_or_404(Tbl_Akun, id=539L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * (ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
def jurnal_bank_cimuleuit(ks, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=150L)
    a_pdp_ops_lain = get_object_or_404(Tbl_Akun, id =448L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_pdp_ops_lain,
        kredit = (ks.selisih),debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_cimuleuit_kecil(ks, user):###teddy
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=150L)
    a_beban_lainnya = get_object_or_404(Tbl_Akun, id=539L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * (ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
def jurnal_bank_uber(ks, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=151L)
    a_pdp_ops_lain = get_object_or_404(Tbl_Akun, id =448L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_pdp_ops_lain,
        kredit = (ks.selisih),debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_uber_kecil(ks, user):###teddy
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=151L)
    a_beban_lainnya = get_object_or_404(Tbl_Akun, id=539L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * (ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
def jurnal_bank_ciwastra(ks, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=629L)
    a_pdp_ops_lain = get_object_or_404(Tbl_Akun, id =448L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_pdp_ops_lain,
        kredit = (ks.selisih),debet = 0,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

def jurnal_bank_ciwastra_kecil(ks, user):###teddy
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_bank = get_object_or_404(Tbl_Akun, id=629L)
    a_beban_lainnya = get_object_or_404(Tbl_Akun, id=539L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ks.kasir.norek(), ks.kasir.agnasabah.nama),
        tgl_trans =ks.tanggal,cu = user, mu = user,nobukti=ks.kasir.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_titipan_pencairan,
        kredit = 0,debet = D(ks.nilai_pembulatan) + D(ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_beban_lainnya,
        kredit = 0,debet = -1 * (ks.selisih),
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan_kasir"), id_coa = a_bank,
        debet = 0,kredit = ks.nilai_pembulatan,
        id_product = '4',status_jurnal ='2',tgl_trans =ks.tanggal,
        id_cabang =ks.kasir.gerai.kode_cabang,id_unit= 300)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def all_transaksi_bank(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    kocab = Tbl_Cabang.objects.get(kode_cabang=cab)
    sekarang = datetime.date.today()
    tgl = timedelta(days=1)
    tanggal = sekarang - tgl
    a = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang,id_coa__coa__startswith ='11.05',jenis='SALDOKASGERAI').latest('id')
    c = a.tgl_trans
    d = sekarang - c
    s_awal = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang,id_coa__coa__startswith ='11.05',tgl_trans=sekarang).\
        filter(jenis='SALDOKASGERAI')
    s_awal_lates = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang,id_coa__coa__startswith ='11.05',jenis='SALDOKASGERAI').\
        filter(tgl_trans=c)
    sekarang = datetime.date.today()
    tampil =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(status_posting__isnull = True).\
        filter(jurnal__kode_cabang=kocab.kode_cabang)
    setoran_bank_gerai = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis__in = (u'GL_GL_PENGELUARAN_BANK','GL_GL_PENAMBAHAN_BANK_RAK',u'Pelunasan_kasir_bank_rak')).\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_uk_bank = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGELUARAN_BANK').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_bank_pusat = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('GL_GL_PENGEMBALIAN_PUSAT_BANK','GL_GL_PENGEMBALIAN_PUSAT_BANK_RAK','GL_GL_PENGEMBALIAN_BANK_CABANG_RAK')).\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_kas_pusat = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today(),jenis = 'GL_GL_PENGELUARAN_KAS_PUSAT').\
        filter(id_cabang=cab,status_jurnal=2)
    pengembalian_bank = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today(),jenis__in =('GL_GL_PENAMBAHAN_BANK',\
        'GL_GL_PENGELUARAN_BANK_RAK'),id_cabang=cab,status_jurnal=2)
    pengembalian_kas = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today(),jenis = 'GL_GL_PENGELUARAN_KAS_PUSAT').\
        filter(id_cabang=cab,status_jurnal=2)
    uang_muka_gerai = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PUSAT_UK').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pencairan_kasir = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pencairan_kasir_bank',\
        'Pencairan_kasir_lebih_bank','Pencairan_kasir_kurang_bank')).\
        filter(id_cabang=cab).filter(status_jurnal=2).filter(id_coa = 298L)
    pencairan_kasir_sisa = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pencairan_kasir_bank',\
        'Pencairan_kasir_lebih_bank','Pencairan_kasir_kurang_bank','Pelunasan_kasir_bank','Pelunasan_gu_kasir_nilai_sblm_kurang_bank',\
        'Pelunasan_gu_kasir_nilai_sblm_lebih_bank','Pelunasan_Gadai_Ulang_kasir_bank','Pelunasan_Gadai_Ulang_kasir_bank',\
        'Pelunasan_gu_kasir_nilai_sblm_kurang_bank_bol','Pelunasan_kasir_bank_rak',\
        'Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer',\
        'Pelunasan_Gadai_ulang_kasir_bank_kelebihan_pendapatan_lbh','Pencairan_kasir_sisa','Pelunasan_gu_bank_nilai_sblm_lebih_pol',\
        'Pendapatan_Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan','Pendapatan_Pelunasan_Gadai_ulang_kasir_bank_kelebihan_pendapatan')).filter(id_cabang=cab).filter(status_jurnal=2).filter(id_coa__in= (448L,546L))    
    pengembalian_uk = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGEMBALIAN_UK').\
        filter(id_cabang=cab).filter(status_jurnal=2)    
    saldo_yang_dikirim = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').\
        filter(id_cabang=cab,status_jurnal=2)
    transaksi_jurnal = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pencairan_kasir_kurang_bank_kecil','Pelunasan_gu_kasir_nilai_sblm_kurang_bol_bank','Pelunasan_gu_kasir_nilai_sblm_lebih_bank_10_bol',\
        'Pelunasan_kasir_bank_bol','GL_GL_CABANG_ADM_BANK')).filter(id_cabang=cab).filter(status_jurnal=2)
    saldo_awal_hari = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_BIAYA_GERAI').\
        filter(id_cabang=cab,status_jurnal=2)#.filter(jurnal__status_jurnal = u'2')
    saldo_uang_muka_hari = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT_UK').\
        filter(id_cabang=cab,status_jurnal=2)
    jurnal_list = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'Pencairan_kasir_bank').\
        filter(id_cabang=cab,status_jurnal=2,id_coa= 7L)
    pndptn_lainnya = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis__in =('Pencairan_kasir_bank','Pelunasan_kasir','Pelunasan_kasir_bank')).\
        filter(id_cabang=cab,status_jurnal=2,id_coa= 448L)
    tbl = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = (u'Pelunasan_kasir_bank',u'Pelunasan_kasir_bank_rak')).\
        filter(id_cabang=cab,status_jurnal=2,id_coa__in= (287L,651L,635L))
    tbl_beban =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').\
        filter(id_cabang=cab,status_jurnal=2,id_coa= 516L)
    rakp =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').\
        filter(id_cabang=cab,status_jurnal=2,id_coa= 378L)
    ak_ulang = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pelunasan_gu_kasir_nilai_sblm_lebih_bank',\
        'Pelunasan_Gadai_Ulang_kasir_bank','Pelunasan_gu_kasir_nilai_sblm_kurang_bank','Pelunasan_gu_bank_nilai_sblm_lebih',\
        'Penerimaan Gadai Ulang','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan',\
        'Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_pendapatan')).\
        filter(id_cabang=cab,status_jurnal=2,id_coa__in= (448L,287L,298L))
    akad_ulang_pengeluaran = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
         filter(jenis = ('Pelunasan_Gadai_Ulang_kasir_pinjaman_besar')).filter(id_cabang=cab,status_jurnal=2,id_coa= 298L)
    pengeluaran_gadai_ulang = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis__in=( u'Pelunasan_Gadai_Ulang_Kasir_nilai_pinjaman_lebih','Pelunasan_gu_kasir_nilai_sblm_kurang_bank',\
        'Pelunasan_Gadai_Ulang_kasir_bank','Pelunasan_gu_kasir_nilai_sblm_lebih_bank_10'),id_cabang=cab,status_jurnal=2,id_coa =298L)
    pelunasan_kelebihan_kasir = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis = 'Pelunasan_kasir_bank',id_cabang=cab,status_jurnal=2,id_coa= 771)
    gadai_ulang_kelebihan_kasir = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis__in = ('Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan',\
        'Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_pendapatan',\
        'Pendapatan1_Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan',\
        'Pendapatan1_Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer'),id_cabang=cab,status_jurnal=2,id_coa= 771)
    hitung_a = sum ([a.kredit for a in ak_ulang]) + sum ([a.kredit for a in setoran_bank_gerai]) \
        + sum ([a.kredit for a in pencairan_kasir_sisa]) + sum ([a.kredit for a in tbl]) + sum([a.kredit for a in pelunasan_kelebihan_kasir])\
        + sum ([a.kredit for a in gadai_ulang_kelebihan_kasir])
    hitung_b = sum ([a.debet for a in pengembalian_bank])\
        + sum ([a.debet for a in pencairan_kasir])\
        + sum([a.debet for a in pengeluaran_gadai_ulang])\
        + sum([a.debet for a in transaksi_jurnal])
    saldo_awal = sum([p.saldo for p  in s_awal])
    saldo_awal_lates =  sum([p.saldo for p in s_awal_lates])

    if d > datetime.timedelta(1) :
        variables = RequestContext(request,{'pelunasan_kelebihan_kasir':pelunasan_kelebihan_kasir,'kocab':kocab,'transaksi_jurnal':transaksi_jurnal,'a':jurnal_list,\
            'gadai_ulang_kelebihan_kasir':gadai_ulang_kelebihan_kasir,
            'total_pencairan':sum ([a.kredit for a in jurnal_list]),\
            'setoran_bank_gerai' : sum ([a.kredit for a in setoran_bank_gerai]),\
            'pengembalian_bank_pusat_pjb' :sum ([a.debet for a in pengembalian_bank_pusat]) ,
            'pengembalian_bank' :sum ([a.debet for a in pengembalian_bank]) + sum ([a.kredit for a in pengembalian_kas]),\
            'uang_muka':sum ([a.kredit for a in uang_muka_gerai]),'saldo_awal':saldo_awal,
            'total_penerimaan':hitung_a,
            'total_pengeluaran': hitung_b ,
            'saldo_akhir': saldo_awal + int(hitung_a) - int(hitung_b),
            'saldo_keseluruhan': (saldo_awal + hitung_a - hitung_b) - sum ([a.kredit for a in pengembalian_bank_pusat]),             
            'pencairan':sum ([a.debet for a in pencairan_kasir]),\
            'pencairan_kasir_sisa':pencairan_kasir_sisa,\
            'saldo_awal_hari':sum ([a.debet for a in saldo_awal_hari]),\
            'saldo_uangmuka_hari':sum ([a.debet for a in saldo_uang_muka_hari]),\
            'total_pelunasan':tbl,\
            'total_pendapatan_lainnya':sum ([a.kredit for a in pndptn_lainnya]),'sekarang':datetime.date.today(),\
            'beban_listrik':(sum ([a.debet for a in tbl_beban])),\
            'total_rakp':sum ([a.kredit for a in rakp]), \
            'total_transaksi_jurnal': sum ([a.debet for a in transaksi_jurnal]),\
            'total_saldo' :  saldo_awal ,'ak_ulang':ak_ulang,
            #'penjualan': penjualan,
            'pengeluaran_gadai_ulang': pengeluaran_gadai_ulang,'pengembalian_kas_pusat':pengembalian_kas_pusat,\
            'pengembalian_bank_pusat':pengembalian_kas_pusat,\
            'saldo_yang_di_kirim':sum ([a.debet for a in saldo_yang_dikirim]), 'pengembalian_kas':pengembalian_kas,\
            't_kasir':pencairan_kasir,'tampil':tampil,
            'pengembalian_bank':pengembalian_bank,'setoran_bank_gerai':setoran_bank_gerai,'cabang':kocab,
            'pengembalian_uk_bank':pengembalian_uk_bank})

    if d <= datetime.timedelta(1) :
        variables = RequestContext(request,{'pelunasan_kelebihan_kasir':pelunasan_kelebihan_kasir,'kocab':kocab,'transaksi_jurnal':transaksi_jurnal,'a':jurnal_list,\
            'gadai_ulang_kelebihan_kasir':gadai_ulang_kelebihan_kasir,
            'total_pencairan':sum ([a.kredit for a in jurnal_list]),\
            'setoran_bank_gerai' : sum ([a.kredit for a in setoran_bank_gerai]),\
            'pengembalian_bank_pusat_pjb' :sum ([a.debet for a in pengembalian_bank_pusat]) ,
            'pengembalian_bank' :sum ([a.debet for a in pengembalian_bank]) + sum ([a.kredit for a in pengembalian_kas]),\
            'uang_muka':sum ([a.kredit for a in uang_muka_gerai]),'saldo_awal':saldo_awal,
            #'saldo_awal': sum([a.saldo for a in s_awal]),
            'total_penerimaan':hitung_a,
            'total_pengeluaran': hitung_b ,
            'saldo_akhir': saldo_awal_lates + int(hitung_a) - int(hitung_b),
            'saldo_keseluruhan': (saldo_awal_lates + hitung_a - hitung_b) - sum ([a.kredit for a in pengembalian_bank_pusat]),
            'pencairan':sum ([a.debet for a in pencairan_kasir]),\
            'pencairan_kasir_sisa':pencairan_kasir_sisa,\
            'saldo_awal_hari':sum ([a.debet for a in saldo_awal_hari]),\
            'saldo_uangmuka_hari':sum ([a.debet for a in saldo_uang_muka_hari]),\
            'total_pelunasan':tbl,\
            'total_pendapatan_lainnya':sum ([a.kredit for a in pndptn_lainnya]),'sekarang':datetime.date.today(),\
            'beban_listrik':(sum ([a.debet for a in tbl_beban])),\
            'total_rakp':sum ([a.kredit for a in rakp]), \
            'total_transaksi_jurnal': sum ([a.debet for a in transaksi_jurnal]),\
            'total_saldo' :  saldo_awal ,'ak_ulang':ak_ulang,
            #'penjualan': penjualan,
            'pengeluaran_gadai_ulang': pengeluaran_gadai_ulang,'pengembalian_kas_pusat':pengembalian_kas_pusat,\
            'pengembalian_bank_pusat':pengembalian_kas_pusat,\
            'saldo_yang_di_kirim':sum ([a.debet for a in saldo_yang_dikirim]), 'pengembalian_kas':pengembalian_kas,\
            't_kasir':pencairan_kasir,'tampil':tampil,
            'pengembalian_bank':pengembalian_bank,'setoran_bank_gerai':setoran_bank_gerai,'cabang':kocab,
            'pengembalian_uk_bank':pengembalian_uk_bank})
    template='kasir/view/all_transaksi_bank.html'
    return render_to_response(template,variables)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def cetak_all_transaksi_bank(request,object_id):
    kocab = Tbl_Cabang.objects.get(kode_cabang=object_id)
    sekarang = datetime.date.today()
    tgl = timedelta(days=1)
    tanggal = sekarang - tgl
    a = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang).filter(id_coa__coa__startswith ='11.05').filter(jenis='SALDOKASGERAI').latest('id')
    #b = a[0]
    c = a.tgl_trans
    d = sekarang - c
    print'c', c, 'd',d,'tanggal',tanggal
    s_awal = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang).filter(id_coa__coa__startswith ='11.05').filter(tgl_trans=sekarang).\
        filter(jenis='SALDOKASGERAI')
    s_awal_lates = Tbl_TransaksiKeu.objects.filter(id_cabang=kocab.kode_cabang).filter(id_coa__coa__startswith ='11.05').filter(jenis='SALDOKASGERAI').filter(tgl_trans=c)

    kocab = Tbl_Cabang.objects.get(kode_cabang=object_id)
    cab = object_id
    sekarang = datetime.date.today()
    #s_awal =Tbl_Transaksi.objects.filter(id_cabang=kocab.kode_cabang).filter(tgl_trans=sekarang).filter(id_coa__coa__contains ='11.05').\
        #filter(jenis='SALDOKASGERAI')
    #s_awal =Tbl_Transaksi.objects.filter(jurnal__kode_cabang=kocab.kode_cabang).filter(id_coa__coa__contains ='11.05').\
        #filter(jenis='SALDOKASGERAI').latest('id')
    tampil =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(status_posting__isnull = True).\
        filter(jurnal__kode_cabang=kocab.kode_cabang)
    setoran_bank_gerai = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis__in = (u'GL_GL_PENGELUARAN_BANK','GL_GL_PENAMBAHAN_BANK_RAK',u'Pelunasan_kasir_bank_rak')).\
        filter(id_cabang=cab).filter(status_jurnal=2)
    #setoran_kas_gerai = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENAMBAHAN_KAS').\
        #filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_uk_bank = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGELUARAN_BANK').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_bank_pusat = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('GL_GL_PENGEMBALIAN_PUSAT_BANK','GL_GL_PENGEMBALIAN_PUSAT_BANK_RAK','GL_GL_PENGEMBALIAN_BANK_CABANG_RAK')).\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_kas_pusat = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGELUARAN_KAS_PUSAT').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_bank = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in =('GL_GL_PENAMBAHAN_BANK','GL_GL_PENGELUARAN_BANK_RAK')).\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pengembalian_kas = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGELUARAN_KAS_PUSAT').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    uang_muka_gerai = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PUSAT_UK').\
        filter(id_cabang=cab).filter(status_jurnal=2)
    pencairan_kasir = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pencairan_kasir_bank',\
        'Pencairan_kasir_lebih_bank','Pencairan_kasir_kurang_bank')).\
        filter(id_cabang=cab).filter(status_jurnal=2).filter(id_coa = 298L)
    pencairan_kasir_sisa = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pencairan_kasir_bank',\
        'Pencairan_kasir_lebih_bank','Pencairan_kasir_kurang_bank','Pelunasan_kasir_bank','Pelunasan_gu_kasir_nilai_sblm_kurang_bank',\
        'Pelunasan_gu_kasir_nilai_sblm_lebih_bank','Pelunasan_Gadai_Ulang_kasir_bank','Pelunasan_Gadai_Ulang_kasir_bank',\
        'Pelunasan_gu_kasir_nilai_sblm_kurang_bank_bol','Pelunasan_kasir_bank_rak','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_pendapatan_lbh',\
        'Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer',\
        'Pelunasan_Gadai_ulang_kasir_bank_kelebihan_pendapatan','Pencairan_kasir_sisa','Pelunasan_gu_bank_nilai_sblm_lebih_pol',\
        'Pendapatan_Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan','Pendapatan_Pelunasan_Gadai_ulang_kasir_bank_kelebihan_pendapatan')).filter(id_cabang=cab).filter(status_jurnal=2).filter(id_coa__in= (448L,546L))    
    pengembalian_uk = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'GL_GL_PENGEMBALIAN_UK').\
        filter(id_cabang=cab).filter(status_jurnal=2)    
    saldo_yang_dikirim = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').\
        filter(id_cabang=cab).filter(status_jurnal=2)#.filter(jurnal__status_jurnal = u'3')
    transaksi_jurnal = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pencairan_kasir_kurang_bank_kecil','Pelunasan_gu_kasir_nilai_sblm_kurang_bol_bank','Pelunasan_gu_kasir_nilai_sblm_lebih_bank_10_bol',\
        'Pelunasan_kasir_bank_bol','GL_GL_CABANG_ADM_BANK')).filter(id_cabang=cab).filter(status_jurnal=2)
    saldo_awal_hari = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_BIAYA_GERAI').\
        filter(id_cabang=cab).filter(status_jurnal=2)#.filter(jurnal__status_jurnal = u'2')
    saldo_uang_muka_hari = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT_UK').\
        filter(id_cabang=cab).filter(status_jurnal=2)#.filter(jurnal__status_jurnal = u'2')
    jurnal_list = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'Pencairan_kasir_bank').\
        filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa= 7L)
    pndptn_lainnya = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis__in =('Pencairan_kasir_bank','Pelunasan_kasir','Pelunasan_kasir_bank')).filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa= 448L)
    tbl = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = (u'Pelunasan_kasir_bank',u'Pelunasan_kasir_bank_rak')).\
        filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa__in= (287L,651L,635L))
    tbl_beban =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').\
        filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa= 516L)
    rakp =Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = u'GL_GL_PUSAT').\
        filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa= 378L)    
    #penjualan = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = ('Penjualan_lelang_kasir')).\
        #filter(id_cabang=object_id).filter(status_jurnal=2)
    ak_ulang = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pelunasan_gu_kasir_nilai_sblm_lebih_bank',\
        'Pelunasan_Gadai_Ulang_kasir_bank','Pelunasan_gu_kasir_nilai_sblm_kurang_bank','Pelunasan_gu_bank_nilai_sblm_lebih',\
        'Penerimaan Gadai Ulang','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_pendapatan')).filter(id_cabang=object_id).filter(status_jurnal=2)\
        .filter(id_coa__in= (448L,287L,298L))

    akad_ulang_pengeluaran = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
         filter(jenis = ('Pelunasan_Gadai_Ulang_kasir_pinjaman_besar')).filter(id_cabang=object_id).filter(status_jurnal=2).filter(id_coa= 298L)

    pengeluaran_gadai_ulang = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).\
        filter(jenis__in=( u'Pelunasan_Gadai_Ulang_Kasir_nilai_pinjaman_lebih','Pelunasan_gu_kasir_nilai_sblm_kurang_bank',\
        'Pelunasan_Gadai_Ulang_kasir_bank','Pelunasan_gu_kasir_nilai_sblm_lebih_bank_10')).filter(id_cabang=object_id).\
        filter(status_jurnal=2).filter(id_coa =298L)

    pelunasan_kelebihan_kasir = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis = 'Pelunasan_kasir_bank').filter(id_cabang=cab).filter(status_jurnal=2).filter(id_coa= 771)

    #gadai_ulang_kelebihan_kasir = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_pendapatan','Pendapatan1_Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan')).filter(id_cabang=cab).filter(status_jurnal=2).filter(id_coa= 771)
    gadai_ulang_kelebihan_kasir = Tbl_Transaksi.objects.filter(tgl_trans = datetime.date.today()).filter(jenis__in = ('Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_pendapatan','Pendapatan1_Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan','Pendapatan1_Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer')).filter(id_cabang=cab).filter(status_jurnal=2).filter(id_coa= 771)

    hitung_a = sum ([a.kredit for a in ak_ulang]) + sum ([a.kredit for a in setoran_bank_gerai]) \
        + sum ([a.kredit for a in pencairan_kasir_sisa]) + sum ([a.kredit for a in tbl]) + sum([a.kredit for a in pelunasan_kelebihan_kasir])\
        + sum ([a.kredit for a in gadai_ulang_kelebihan_kasir])
    hitung_b = sum ([a.debet for a in pengembalian_bank])\
        + sum ([a.debet for a in pencairan_kasir])\
        + sum([a.debet for a in pengeluaran_gadai_ulang])\
        + sum([a.debet for a in transaksi_jurnal])
    saldo_awal = sum([p.saldo for p  in s_awal])   
    saldo_awal_lates =  sum([p.saldo for p in s_awal_lates])

    if d > datetime.timedelta(1) :
        variables = RequestContext(request,{'pelunasan_kelebihan_kasir':pelunasan_kelebihan_kasir,'kocab':kocab,'transaksi_jurnal':transaksi_jurnal,'a':jurnal_list,\
            'gadai_ulang_kelebihan_kasir':gadai_ulang_kelebihan_kasir,
            'total_pencairan':sum ([a.kredit for a in jurnal_list]),\
            'setoran_bank_gerai' : sum ([a.kredit for a in setoran_bank_gerai]),\
            'pengembalian_bank_pusat_pjb' :sum ([a.debet for a in pengembalian_bank_pusat]) ,
            'pengembalian_bank' :sum ([a.debet for a in pengembalian_bank]) + sum ([a.kredit for a in pengembalian_kas]),\
            'uang_muka':sum ([a.kredit for a in uang_muka_gerai]),'saldo_awal':saldo_awal,
            #'saldo_awal': sum([a.saldo for a in s_awal]),
            'total_penerimaan':hitung_a,
            'total_pengeluaran': hitung_b ,
            'saldo_akhir': saldo_awal + int(hitung_a) - int(hitung_b),
            'saldo_keseluruhan': (saldo_awal + hitung_a - hitung_b) - sum ([a.kredit for a in pengembalian_bank_pusat]),             
            'pencairan':sum ([a.debet for a in pencairan_kasir]),\
            'pencairan_kasir_sisa':pencairan_kasir_sisa,\
            'saldo_awal_hari':sum ([a.debet for a in saldo_awal_hari]),\
            'saldo_uangmuka_hari':sum ([a.debet for a in saldo_uang_muka_hari]),\
            'total_pelunasan':tbl,\
            'total_pendapatan_lainnya':sum ([a.kredit for a in pndptn_lainnya]),'sekarang':datetime.date.today(),\
            'beban_listrik':(sum ([a.debet for a in tbl_beban])),\
            'total_rakp':sum ([a.kredit for a in rakp]), \
            'total_transaksi_jurnal': sum ([a.debet for a in transaksi_jurnal]),\
            'total_saldo' :  saldo_awal ,'ak_ulang':ak_ulang,
            #'penjualan': penjualan,
            'pengeluaran_gadai_ulang': pengeluaran_gadai_ulang,'pengembalian_kas_pusat':pengembalian_kas_pusat,\
            'pengembalian_bank_pusat':pengembalian_kas_pusat,\
            'saldo_yang_di_kirim':sum ([a.debet for a in saldo_yang_dikirim]), 'pengembalian_kas':pengembalian_kas,\
            't_kasir':pencairan_kasir,'tampil':tampil,
            'pengembalian_bank':pengembalian_bank,'setoran_bank_gerai':setoran_bank_gerai,'cabang':kocab,
            'pengembalian_uk_bank':pengembalian_uk_bank})

    if d <= datetime.timedelta(1) :
        variables = RequestContext(request,{'pelunasan_kelebihan_kasir':pelunasan_kelebihan_kasir,'kocab':kocab,'transaksi_jurnal':transaksi_jurnal,'a':jurnal_list,\
            'gadai_ulang_kelebihan_kasir':gadai_ulang_kelebihan_kasir,
            'total_pencairan':sum ([a.kredit for a in jurnal_list]),\
            'setoran_bank_gerai' : sum ([a.kredit for a in setoran_bank_gerai]),\
            'pengembalian_bank_pusat_pjb' :sum ([a.debet for a in pengembalian_bank_pusat]) ,
            'pengembalian_bank' :sum ([a.debet for a in pengembalian_bank]) + sum ([a.kredit for a in pengembalian_kas]),\
            'uang_muka':sum ([a.kredit for a in uang_muka_gerai]),'saldo_awal':saldo_awal,
            #'saldo_awal': sum([a.saldo for a in s_awal]),
            'total_penerimaan':hitung_a,
            'total_pengeluaran': hitung_b ,
            'saldo_akhir': saldo_awal_lates + int(hitung_a) - int(hitung_b),
            'saldo_keseluruhan': (saldo_awal_lates + hitung_a - hitung_b) - sum ([a.kredit for a in pengembalian_bank_pusat]),             
            'pencairan':sum ([a.debet for a in pencairan_kasir]),\
            'pencairan_kasir_sisa':pencairan_kasir_sisa,\
            'saldo_awal_hari':sum ([a.debet for a in saldo_awal_hari]),\
            'saldo_uangmuka_hari':sum ([a.debet for a in saldo_uang_muka_hari]),\
            'total_pelunasan':tbl,\
            'total_pendapatan_lainnya':sum ([a.kredit for a in pndptn_lainnya]),'sekarang':datetime.date.today(),\
            'beban_listrik':(sum ([a.debet for a in tbl_beban])),\
            'total_rakp':sum ([a.kredit for a in rakp]), \
            'total_transaksi_jurnal': sum ([a.debet for a in transaksi_jurnal]),\
            'total_saldo' :  saldo_awal ,'ak_ulang':ak_ulang,
            #'penjualan': penjualan,
            'pengeluaran_gadai_ulang': pengeluaran_gadai_ulang,'pengembalian_kas_pusat':pengembalian_kas_pusat,\
            'pengembalian_bank_pusat':pengembalian_kas_pusat,\
            'saldo_yang_di_kirim':sum ([a.debet for a in saldo_yang_dikirim]), 'pengembalian_kas':pengembalian_kas,\
            't_kasir':pencairan_kasir,'tampil':tampil,
            'pengembalian_bank':pengembalian_bank,'setoran_bank_gerai':setoran_bank_gerai,'cabang':kocab,
            'pengembalian_uk_bank':pengembalian_uk_bank})
    template='kasir/view/cetak_all_transaksi_bank.html'
    return render_to_response(template,variables)    

