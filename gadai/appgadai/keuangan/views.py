from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from gadai.appgadai.models import *
from django import forms
import os, string
from django.conf import settings
from gadai.appgadai.templatetags.terbilang import terbilang
from gadai.appgadai.templatetags.number_format import number_format
from gadai.appgadai.keuangan.forms import BiayasForm,BiayaPusatForm,BiayaPusatGeraiForm
import datetime
import decimal
from gadai.appgadai.templatetags.number_format import number_format
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

def add_gerai(request,object_id):
    sekarang = datetime.date.today()
    c = object_id
    bea = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(status_jurnal = 1L).\
        filter(jenis = u'Transaksi_Gerai_oleh_Pusat').exclude(jurnal__diskripsi ='GL_GL_PUSAT_BANK')
		
    user = request.user
    if request.method == "POST":
        form = BiayaPusatGeraiForm(request.POST)
        tanggal = datetime.date.today()
        if form.is_valid():

            telpon = form.cleaned_data['telpon']
            ket_telpon= form.cleaned_data['ket_telpon']
            jenis_transaksi_telepon = form.cleaned_data['jenis_transaksi_telepon']            
            telpon_gerai =form.cleaned_data['telpon_gerai']

            bbm = form.cleaned_data['bbm']
            ket_bbm = form.cleaned_data['ket_bbm']
            jenis_transaksi_bbm = form.cleaned_data['jenis_transaksi_bbm']
            bbm_gerai =form.cleaned_data['bbm_gerai']

            sumbangan = form.cleaned_data['sumbangan']
            ket_sumbangan = form.cleaned_data['ket_sumbangan']
            jenis_transaksi_sumbangan = form.cleaned_data['jenis_transaksi_sumbangan']
            sumbangan_gerai =form.cleaned_data['sumbangan_gerai']
            ##ACAN
            jenis_transaksi_listrik	= form.cleaned_data['jenis_transaksi_listrik']
            ket_listrik = form.cleaned_data['ket_listrik']
            listrik_gerai = form.cleaned_data['listrik_gerai']
            listrik = form.cleaned_data['listrik']

            jenis_transaksi_pdam = form.cleaned_data['jenis_transaksi_pdam']
            ket_pdam = form.cleaned_data['ket_pdam']
            pdam_gerai = form.cleaned_data['pdam_gerai']
            pdam = form.cleaned_data['pdam']

            jenis_transaksi_transport = form.cleaned_data['jenis_transaksi_transport']
            ket_transport = form.cleaned_data['ket_transport']
            transport_gerai = form.cleaned_data['transport_gerai']
            transport = form.cleaned_data['transport']

            #jenis_transaksi_palkir = form.cleaned_data['jenis_transaksi_palkir']
            #ket_palkir = form.cleaned_data['ket_palkir']
            #palkir_gerai = form.cleaned_data['palkir_gerai']
            #palkir = form.cleaned_data['palkir']

            biaya = BiayaPusat(gerai = user.profile.gerai,tanggal = tanggal,
                    telpon_gerai=telpon_gerai,telpon = telpon,ket_telpon= ket_telpon,jenis_transaksi_telepon = jenis_transaksi_telepon,
                  bbm = bbm, ket_bbm = ket_bbm, jenis_transaksi_bbm = jenis_transaksi_bbm, bbm_gerai = bbm_gerai,
                  sumbangan = sumbangan, ket_sumbangan = ket_sumbangan, jenis_transaksi_sumbangan = jenis_transaksi_sumbangan, sumbangan_gerai = sumbangan_gerai,
                  jenis_transaksi_listrik = jenis_transaksi_listrik, ket_listrik = ket_listrik, listrik_gerai = listrik_gerai,listrik = listrik,
                  jenis_transaksi_pdam = jenis_transaksi_pdam,ket_pdam = ket_pdam,pdam_gerai = pdam_gerai,pdam = pdam,
                  jenis_transaksi_transport = jenis_transaksi_transport,ket_transport = ket_transport,transport_gerai = transport_gerai,transport = transport,)
                  #jenis_transaksi_palkir = jenis_transaksi_palkir, ket_palkir = ket_palkir, palkir_gerai = palkir_gerai, palkir = palkir)
            biaya.save()

            ##BIAYA TELPON
            if biaya.telpon > 0 and biaya.jenis_transaksi_telepon == 'KAS':
                jurnal_kas_biaya_telpon_gerai(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Telpon Berhasil 57 ###')
            if biaya.telpon > 0 and biaya.jenis_transaksi_telepon == 'BANK':
                jurnal_bank_biaya_telpon_gerai(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Telpon Berhasil 60 ###')
            if biaya.telpon > 0 and biaya.jenis_transaksi_telepon == '':
                jurnal_biaya_telpon_gerai_tuju_gerai(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Telpon Berhasil 63 ###')

            ##BIAYA BBM
            if biaya.bbm > 0 and biaya.jenis_transaksi_bbm == 'KAS':
                jurnal_kas_biaya_bbm_gerai(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya bbm Berhasil 68 ###')
            if biaya.bbm > 0 and biaya.jenis_transaksi_bbm == 'BANK':
                jurnal_bank_biaya_bbm_gerai(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya bbm Berhasil 71 ###')
            if biaya.bbm > 0 and biaya.jenis_transaksi_bbm == '':
                jurnal_biaya_bbm_gerai_tuju_gerai(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya bbm Berhasil 74 ###')

            ##BIAYA SUMBANGAN
            if biaya.sumbangan > 0 and biaya.jenis_transaksi_sumbangan == 'KAS':
                jurnal_kas_biaya_sumbangan_gerai(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya sumbangan Berhasil 68 ###')
            if biaya.sumbangan > 0 and biaya.jenis_transaksi_sumbangan == 'BANK':
                jurnal_bank_biaya_sumbangan_gerai(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya sumbangan Berhasil 71 ###')
            if biaya.sumbangan > 0 and biaya.jenis_transaksi_sumbangan == '':
                jurnal_biaya_sumbangan_gerai_tuju_gerai(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya sumbangan Berhasil 74 ###')

            ##BIAYA LISTRIK
            if biaya.listrik > 0 and biaya.jenis_transaksi_listrik == 'KAS':
                jurnal_kas_biaya_listrik_gerai(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya listrik Berhasil 68 ###')
            if biaya.listrik > 0 and biaya.jenis_transaksi_listrik == 'BANK':
                jurnal_bank_biaya_listrik_gerai(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya listrik Berhasil 71 ###')
            if biaya.listrik > 0 and biaya.jenis_transaksi_listrik == '':
                jurnal_biaya_listrik_gerai_tuju_gerai(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya listrik Berhasil 74 ###')

            ##BIAYA PDAM
            if biaya.pdam > 0 and biaya.jenis_transaksi_pdam == 'KAS':
                jurnal_kas_biaya_pdam_gerai(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya PDAM Berhasil 68 ###')
            if biaya.pdam > 0 and biaya.jenis_transaksi_pdam == 'BANK':
                jurnal_bank_biaya_pdam_gerai(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya PDAM Berhasil 71 ###')
            if biaya.pdam > 0 and biaya.jenis_transaksi_pdam == '':
                jurnal_biaya_pdam_gerai_tuju_gerai(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya PDAM Berhasil 74 ###')
            return HttpResponseRedirect('/keuangan/%s/add_gerai/' % (object_id))
    else:
        form  = BiayaPusatGeraiForm()
    variables = RequestContext(request, {'form': form,'bea':bea,'c':object_id,'total_kredit': sum([p.kredit for p in bea]),\
        'total_debet': sum([p.kredit for p in bea])})
    return render_to_response('biaya/add_biaya_gerai.html', variables)

def jurnal_kas_biaya_telpon_gerai(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapperdiBayarPusat.objects.get(item='telepon',cabang = biaya.telpon_gerai)
    telpon_debet = bm.coa_debet_pusat
    telpon_kredit = bm.coa_kredit_pusat
    telpon_debet_gerai = bm.coa_debet_gerai
    telpon_kredit_gerai = bm.coa_kredit_gerai
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Telpon Gerai Oleh Pusat',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_telpon)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = telpon_debet,
        kredit = 0,debet = D((biaya.telpon)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_telpon,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.telpon_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = telpon_kredit,
        debet = 0,kredit = D((biaya.telpon)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_telpon,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.telpon_gerai.kode_cabang)

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Telpon Gerai Oleh Pusat',kode_cabang = biaya.telpon_gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_telpon)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = telpon_debet_gerai,
        kredit = 0,debet = D((biaya.telpon)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_telpon,
        id_cabang =biaya.telpon_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.telpon_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = telpon_kredit_gerai,
        debet = 0,kredit = D((biaya.telpon)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_telpon,
        id_cabang =biaya.telpon_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.telpon_gerai.kode_cabang)


def jurnal_bank_biaya_telpon_gerai(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapperdiBayarPusat.objects.get(item='telepon_bank',cabang = biaya.telpon_gerai)
    telpon_debet = bm.coa_debet_pusat
    telpon_kredit = bm.coa_kredit_pusat
    telpon_debet_gerai = bm.coa_debet_gerai
    telpon_kredit_gerai = bm.coa_kredit_gerai
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Telpon Gerai Oleh Pusat',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_telpon)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = telpon_debet,
        kredit = 0,debet = D((biaya.telpon)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_telpon,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.telpon_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = telpon_kredit,
        debet = 0,kredit = D((biaya.telpon)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_telpon,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.telpon_gerai.kode_cabang)

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Telpon Gerai Oleh Pusat',kode_cabang = biaya.telpon_gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_telpon)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = telpon_debet_gerai,
        kredit = 0,debet = D((biaya.telpon)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_telpon,
        id_cabang =biaya.telpon_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.telpon_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = telpon_kredit_gerai,
        debet = 0,kredit = D((biaya.telpon)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_telpon,
        id_cabang =biaya.telpon_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.telpon_gerai.kode_cabang)

def jurnal_kas_biaya_bbm_gerai(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapperdiBayarPusat.objects.get(item='bbm',cabang = biaya.bbm_gerai)
    bbm_debet = bm.coa_debet_pusat
    bbm_kredit = bm.coa_kredit_pusat
    bbm_debet_gerai = bm.coa_debet_gerai
    bbm_kredit_gerai = bm.coa_kredit_gerai
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Bbm Gerai Oleh Pusat',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_bbm)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = bbm_debet,
        kredit = 0,debet = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_bbm,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.bbm_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = bbm_kredit,
        debet = 0,kredit = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_bbm,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.bbm_gerai.kode_cabang)

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Bbm Gerai Oleh Pusat',kode_cabang = biaya.bbm_gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_bbm)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = bbm_debet_gerai,
        kredit = 0,debet = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_bbm,
        id_cabang =biaya.bbm_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.bbm_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = bbm_kredit_gerai,
        debet = 0,kredit = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_bbm,
        id_cabang =biaya.bbm_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.bbm_gerai.kode_cabang)


def jurnal_bank_biaya_bbm_gerai(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapperdiBayarPusat.objects.get(item='bbm_bank',cabang = biaya.bbm_gerai)
    bbm_debet = bm.coa_debet_pusat
    bbm_kredit = bm.coa_kredit_pusat
    bbm_debet_gerai = bm.coa_debet_gerai
    bbm_kredit_gerai = bm.coa_kredit_gerai
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Bbm Gerai Oleh Pusat',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_bbm)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = bbm_debet,
        kredit = 0,debet = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_bbm,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.bbm_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = bbm_kredit,
        debet = 0,kredit = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_bbm,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.bbm_gerai.kode_cabang)

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Bbm Gerai Oleh Pusat',kode_cabang = biaya.bbm_gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_bbm)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = bbm_debet_gerai,
        kredit = 0,debet = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_bbm,
        id_cabang =biaya.bbm_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.bbm_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = bbm_kredit_gerai,
        debet = 0,kredit = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_bbm,
        id_cabang =biaya.bbm_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.bbm_gerai.kode_cabang)

def jurnal_kas_biaya_sumbangan_gerai(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapperdiBayarPusat.objects.get(item='sumbangan',cabang = biaya.sumbangan_gerai)
    sumbangan_debet = bm.coa_debet_pusat
    sumbangan_kredit = bm.coa_kredit_pusat
    sumbangan_debet_gerai = bm.coa_debet_gerai
    sumbangan_kredit_gerai = bm.coa_kredit_gerai
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Sumbangan Gerai Oleh Pusat',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_sumbangan)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = sumbangan_debet,
        kredit = 0,debet = D((biaya.sumbangan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_sumbangan,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.sumbangan_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = sumbangan_kredit,
        debet = 0,kredit = D((biaya.sumbangan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_sumbangan,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.sumbangan_gerai.kode_cabang)

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Sumbangan Gerai Oleh Pusat',kode_cabang = biaya.sumbangan_gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_sumbangan)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = sumbangan_debet_gerai,
        kredit = 0,debet = D((biaya.sumbangan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_sumbangan,
        id_cabang =biaya.sumbangan_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.sumbangan_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = sumbangan_kredit_gerai,
        debet = 0,kredit = D((biaya.sumbangan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_sumbangan,
        id_cabang =biaya.sumbangan_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.sumbangan_gerai.kode_cabang)


def jurnal_bank_biaya_sumbangan_gerai(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapperdiBayarPusat.objects.get(item='sumbangan_bank',cabang = biaya.sumbangan_gerai)
    sumbangan_debet = bm.coa_debet_pusat
    sumbangan_kredit = bm.coa_kredit_pusat
    sumbangan_debet_gerai = bm.coa_debet_gerai
    sumbangan_kredit_gerai = bm.coa_kredit_gerai
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Sumbangan Gerai Oleh Pusat',kode_cabang = biaya.sumbangan_gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_sumbangan)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = sumbangan_debet,
        kredit = 0,debet = D((biaya.sumbangan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_sumbangan,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.sumbangan_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = sumbangan_kredit,
        debet = 0,kredit = D((biaya.sumbangan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_sumbangan,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.sumbangan_gerai.kode_cabang)

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Sumbangan Gerai Oleh Pusat',kode_cabang = biaya.sumbangan_gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_sumbangan)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = sumbangan_debet_gerai,
        kredit = 0,debet = D((biaya.sumbangan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_sumbangan,
        id_cabang =biaya.sumbangan_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.sumbangan_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = sumbangan_kredit_gerai,
        debet = 0,kredit = D((biaya.sumbangan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_sumbangan,
        id_cabang =biaya.sumbangan_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.sumbangan_gerai.kode_cabang)


def jurnal_kas_biaya_listrik_gerai(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapperdiBayarPusat.objects.get(item='listrik',cabang = biaya.listrik_gerai)
    listrik_debet = bm.coa_debet_pusat
    listrik_kredit = bm.coa_kredit_pusat
    listrik_debet_gerai = bm.coa_debet_gerai
    listrik_kredit_gerai = bm.coa_kredit_gerai
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Listrik Gerai Oleh Pusat',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_listrik)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = listrik_debet,
        kredit = 0,debet = D((biaya.listrik)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_listrik,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.listrik_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = listrik_kredit,
        debet = 0,kredit = D((biaya.listrik)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_listrik,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.listrik_gerai.kode_cabang)

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Listrik Gerai Oleh Pusat',kode_cabang = biaya.listrik_gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_listrik)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = listrik_debet_gerai,
        kredit = 0,debet = D((biaya.listrik)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_listrik,
        id_cabang =biaya.listrik_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.listrik_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = listrik_kredit_gerai,
        debet = 0,kredit = D((biaya.listrik)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_listrik,
        id_cabang =biaya.listrik_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.listrik_gerai.kode_cabang)


def jurnal_bank_biaya_listrik_gerai(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapperdiBayarPusat.objects.get(item='listrik_bank',cabang = biaya.listrik_gerai)
    listrik_debet = bm.coa_debet_pusat
    listrik_kredit = bm.coa_kredit_pusat
    listrik_debet_gerai = bm.coa_debet_gerai
    listrik_kredit_gerai = bm.coa_kredit_gerai
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Listrik Gerai Oleh Pusat',kode_cabang = biaya.listrik_gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_listrik)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = listrik_debet,
        kredit = 0,debet = D((biaya.listrik)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_listrik,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.listrik_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = listrik_kredit,
        debet = 0,kredit = D((biaya.listrik)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_listrik,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.listrik_gerai.kode_cabang)

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Listrik Gerai Oleh Pusat',kode_cabang = biaya.listrik_gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_listrik)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = listrik_debet_gerai,
        kredit = 0,debet = D((biaya.listrik)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_listrik,
        id_cabang =biaya.listrik_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.listrik_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = listrik_kredit_gerai,
        debet = 0,kredit = D((biaya.listrik)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_listrik,
        id_cabang =biaya.listrik_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.listrik_gerai.kode_cabang)


def jurnal_kas_biaya_pdam_gerai(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapperdiBayarPusat.objects.get(item='pdam',cabang = biaya.pdam_gerai)
    pdam_debet = bm.coa_debet_pusat
    pdam_kredit = bm.coa_kredit_pusat
    pdam_debet_gerai = bm.coa_debet_gerai
    pdam_kredit_gerai = bm.coa_kredit_gerai
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran PDAM Gerai Oleh Pusat',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pdam)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = pdam_debet,
        kredit = 0,debet = D((biaya.pdam)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_pdam,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.pdam_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = pdam_kredit,
        debet = 0,kredit = D((biaya.pdam)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_pdam,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.pdam_gerai.kode_cabang)

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran PDAM Gerai Oleh Pusat',kode_cabang = biaya.pdam_gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pdam)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = pdam_debet_gerai,
        kredit = 0,debet = D((biaya.pdam)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_pdam,
        id_cabang =biaya.pdam_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.pdam_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = pdam_kredit_gerai,
        debet = 0,kredit = D((biaya.pdam)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_pdam,
        id_cabang =biaya.pdam_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.pdam_gerai.kode_cabang)


def jurnal_bank_biaya_pdam_gerai(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapperdiBayarPusat.objects.get(item='pdam_bank',cabang = biaya.pdam_gerai)
    pdam_debet = bm.coa_debet_pusat
    pdam_kredit = bm.coa_kredit_pusat
    pdam_debet_gerai = bm.coa_debet_gerai
    pdam_kredit_gerai = bm.coa_kredit_gerai
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran PDAM Gerai Oleh Pusat',kode_cabang = biaya.pdam_gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pdam)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = pdam_debet,
        kredit = 0,debet = D((biaya.pdam)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_pdam,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.pdam_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = pdam_kredit,
        debet = 0,kredit = D((biaya.pdam)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_pdam,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.pdam_gerai.kode_cabang)

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran PDAM Gerai Oleh Pusat',kode_cabang = biaya.pdam_gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pdam)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = pdam_debet_gerai,
        kredit = 0,debet = D((biaya.pdam)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_pdam,
        id_cabang =biaya.pdam_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.pdam_gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("Transaksi_Gerai_oleh_Pusat"), id_coa = pdam_kredit_gerai,
        debet = 0,kredit = D((biaya.pdam)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_pdam,
        id_cabang =biaya.pdam_gerai.kode_cabang,id_unit= 300,id_cabang_tuju=biaya.pdam_gerai.kode_cabang)
###---akhir tes

def hapus_jurnal_penyetoran(request,object_id):#### Menu hapus di menu pengeluaran dan penyetoran PUSAT
    user = request.user
    tbl = Jurnal.objects.get(id=object_id)
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Penghapusan Jurnal Berhasil')
    return HttpResponseRedirect("/keuangan/300/add/" )

def hapus_jurnal_add(request,object_id):
    tbl = Tbl_Transaksi.objects.get(id=object_id)
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Penghapusan Jurnal Berhasil')
    return HttpResponseRedirect(tbl.keuangan_hapus() )

def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['KEUANGAN1','KEUANGAN2'])
@login_required
@user_passes_test(is_in_multiple_groups)
def mastertiket_gl_gl_pusat(request,user,object_id):
    user = request.user
    sekarang = datetime.date.today()
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=object_id,jurnal__cu__id=user.id).filter(status_jurnal__in=(u'2','2')).\
        filter(jenis__in=(u'GL_GL_CABANG',u'GL_GL_PUSAT_UK',u'GL_GL_PUSAT',u'GL_GL_BIAYA_GERAI','GL_GL_CABANG_PENGEMBALIAN',\
        'GL_GL_PENAMBAHAN_GERAI','GL_GL_PENAMBAHAN_BANK','GL_GL_PENAMBAHAN_KAS','GL_GL_PENGELUARAN_KAS_PUSAT',\
        'GL_GL_PENGEMBALIAN_GERAI','GL_GL_PENGEMBALIAN_PUSAT','GL_GL_PENAMBAHAN_SALDO','GL_GL_PENGELUARAN_BANK',\
        'GL_GL_PENGELUARAN_BANK_PUSAT','GL_GL_PENGELUARAN_KAS',\
        'GL_GL_PENGEMBALIAN_UK','GL_GL_CABANG_UK')) #'GL_GL_RAK_PUSAT',\
    template = 'biaya/mastertiketgl_gl_pusat.html'
    variables = RequestContext(request, {'user':user,'g':gr,'total_debet': sum([p.debet for p in gr]),'total_kredit': sum([p.kredit for p in gr])})
    return render_to_response(template, variables)

def hapus_jurnal_pusat(request,object_id):
    tbl = Tbl_Transaksi.objects.get(id=object_id)
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Penghapusan Jurnal Berhasil')
    return HttpResponseRedirect(tbl.get_absolute_url_biaya_pusat() )


def add_pusat(request,object_id):
    sekarang = datetime.date.today()
    c = object_id
    bea = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=object_id).filter(status_jurnal = 1L).\
        filter(jenis__in=( u'GL_GL_CABANG',u'GL_GL_PUSAT_UK',u'GL_GL_PUSAT',u'GL_GL_BIAYA_GERAI','GL_GL_CABANG_PENGEMBALIAN',\
        'GL_GL_PENAMBAHAN_GERAI','GL_GL_PENAMBAHAN_BANK','GL_GL_PENAMBAHAN_KAS','GL_GL_PENGELUARAN_KAS_PUSAT','Penerimaan Materai',\
	'GL_GL_PENGEMBALIAN_GERAI','GL_GL_PENGEMBALIAN_PUSAT','GL_GL_PENAMBAHAN_SALDO','GL_GL_PENGELUARAN_BANK',\
        'GL_GL_PENGELUARAN_BANK_PUSAT','GL_GL_PENGELUARAN_KAS','Pemakaian Materai Pusat',\
	'GL_GL_PENGEMBALIAN_UK','GL_GL_CABANG_UK','GL_GL_PENGEMBALIAN_UK','GL_GL_PUSAT_UK','PEMBELIAN MATERAI PUSAT','PENJUALAN MATERAI PUSAT')).\
        exclude(jurnal__diskripsi ='GL_GL_PUSAT_BANK')
		
    user = request.user
    if request.method == "POST":
        form = BiayaPusatForm(request.POST)
        if form.is_valid():
            tanggal = form.cleaned_data['tanggal']
            saldo_awal = form.cleaned_data['saldo_awal']
            saldo_akhir =  form.cleaned_data['saldo_akhir']
            antar_gerai_kembali= form.cleaned_data['antar_gerai_kembali']
            antar_gerai= form.cleaned_data['antar_gerai']
            ## TAMBAHAN SEPUR
            bbm = form.cleaned_data['bbm']
            ket_bbm= form.cleaned_data['ket_bbm']
            jenis_transaksi_bbm = form.cleaned_data['jenis_transaksi_bbm']
            bbm_gerai =form.cleaned_data['bbm_gerai']            

            tol = form.cleaned_data['tol']
            ket_tol= form.cleaned_data['ket_tol']
            jenis_transaksi_tol = form.cleaned_data['jenis_transaksi_tol']
            tol_gerai =form.cleaned_data['tol_gerai'] 

            transport = form.cleaned_data['transport']
            ket_transport= form.cleaned_data['ket_transport']
            jenis_transaksi_transport = form.cleaned_data['jenis_transaksi_transport']
            transport_gerai =form.cleaned_data['transport_gerai'] 

            peralkantor = form.cleaned_data['peralkantor']
            ket_peralkantor= form.cleaned_data['ket_peralkantor']
            jenis_transaksi_peralkantor = form.cleaned_data['jenis_transaksi_peralkantor']
            peralkantor_gerai =form.cleaned_data['peralkantor_gerai']

            ## AKHIR TAMBAHAN SEPUR
            gaji = form.cleaned_data['gaji']
            ket_gaji= form.cleaned_data['ket_gaji']
            jenis_transaksi_gaji = form.cleaned_data['jenis_transaksi_gaji']
            gaji_gerai =form.cleaned_data['gaji_gerai']

            sewa = form.cleaned_data['sewa']
            ket_sewa= form.cleaned_data['ket_sewa']
            jenis_transaksi_sewa = form.cleaned_data['jenis_transaksi_sewa']
            sewa_gerai =form.cleaned_data['sewa_gerai']
     
            penerimaan_saldo = form.cleaned_data['penerimaan_saldo']
            pendapatan_lain =  form.cleaned_data['pendapatan_lain']
            ket_pendapatan_lain= form.cleaned_data['ket_pendapatan_lain']
        
            listrik = form.cleaned_data['listrik']
            ket_listrik= form.cleaned_data['ket_listrik']
            jenis_transaksi_listrik = form.cleaned_data['jenis_transaksi_listrik']
            listrik_gerai =form.cleaned_data['listrik_gerai']
        
            pdam = form.cleaned_data['pdam']
            ket_pdam= form.cleaned_data['ket_pdam']
            jenis_transaksi_pdam = form.cleaned_data['jenis_transaksi_pdam']
            pdam_gerai =form.cleaned_data['pdam_gerai']            

            telpon = form.cleaned_data['telpon']
            ket_telpon= form.cleaned_data['ket_telpon']
            jenis_transaksi_telepon = form.cleaned_data['jenis_transaksi_telepon']            
            telpon_gerai =form.cleaned_data['telpon_gerai']

            foto_copy = form.cleaned_data['foto_copy']
            ket_foto_copy= form.cleaned_data['ket_foto_copy']
            jenis_transaksi_foto_copy = form.cleaned_data['jenis_transaksi_foto_copy']
            fotocopy_gerai =form.cleaned_data['fotocopy_gerai']
        
            majalah = form.cleaned_data['majalah']
            ket_majalah= form.cleaned_data['ket_majalah']
            jenis_transaksi_majalah = form.cleaned_data['jenis_transaksi_majalah']
            majalah_gerai =form.cleaned_data['majalah_gerai']
        
            ##untuk transaksi pusat
            nilai_materai = form.cleaned_data['nilai_materai']
            keterangan_materai = form.cleaned_data['keterangan_materai']
        
            ## AKhir untuk transaksi pusat
        
            pemb_lingkungan = form.cleaned_data['pemb_lingkungan']
            ket_pemb_lingkungan = form.cleaned_data['ket_pemb_lingkungan']
            jenis_transaksi_pemb_lingkungan = form.cleaned_data['jenis_transaksi_pemb_lingkungan']
            lingkungan_gerai =form.cleaned_data['lingkungan_gerai']
        
            sumbangan= form.cleaned_data['sumbangan']
            ket_sumbangan = form.cleaned_data['ket_sumbangan']
            jenis_transaksi_sumbangan = form.cleaned_data['jenis_transaksi_sumbangan']
            sumbangan_gerai =form.cleaned_data['sumbangan_gerai']
            
            perlengkapan = form.cleaned_data['perlengkapan']
            ket_perlengkapan = form.cleaned_data['ket_perlengkapan']
            jenis_transaksi_perlengkapan = form.cleaned_data['jenis_transaksi_perlengkapan']
            perlengkapan_gerai =form.cleaned_data['perlengkapan_gerai']
        
            konsumsi = form.cleaned_data['konsumsi']
            ket_konsumsi = form.cleaned_data['ket_konsumsi']
            jenis_transaksi_konsumsi = form.cleaned_data['jenis_transaksi_konsumsi']
            konsumsi_gerai =form.cleaned_data['konsumsi_gerai']
            js_trans = form.cleaned_data['js_trans']
            js_trans_kembali = form.cleaned_data['js_trans_kembali']
            ## Penambahan Uang Muka            
            penambahan_uk =  form.cleaned_data['penambahan_uk']
            ket_penambahan_uk = form.cleaned_data['ket_penambahan_uk']
            pengembalian_uk = form.cleaned_data['pengembalian_uk']
            ket_pengembalian_uk = form.cleaned_data['ket_pengembalian_uk']

            pembelian_materai = form.cleaned_data['pembelian_materai']
            ket_pmb_materai= form.cleaned_data['ket_pmb_materai']
            jenis_pmb_materai = form.cleaned_data['jenis_pmb_materai']

            jual_materai = form.cleaned_data['jual_materai']
            ket_jual_materai= form.cleaned_data['ket_jual_materai']
            jenis_jual_materai = form.cleaned_data['jenis_jual_materai']

            biaya = BiayaPusat(gerai = user.profile.gerai,tanggal = tanggal,saldo_awal = saldo_awal,saldo_akhir =saldo_akhir,\
                antar_gerai_kembali= antar_gerai_kembali,antar_gerai= antar_gerai,listrik_gerai=listrik_gerai,pdam_gerai=pdam_gerai,\
                penerimaan_saldo = penerimaan_saldo,pendapatan_lain =pendapatan_lain,telpon_gerai=telpon_gerai,fotocopy_gerai=fotocopy_gerai,\
                ket_pendapatan_lain= ket_pendapatan_lain,listrik = listrik,ket_listrik= ket_listrik,perlengkapan_gerai=perlengkapan_gerai,\
                jenis_transaksi_listrik = jenis_transaksi_listrik,majalah_gerai=majalah_gerai,lingkungan_gerai=lingkungan_gerai,\
                sumbangan_gerai=sumbangan_gerai,\
                pdam = pdam,ket_pdam= ket_pdam,jenis_transaksi_pdam = jenis_transaksi_pdam,konsumsi_gerai=konsumsi_gerai,\
                telpon = telpon,ket_telpon= ket_telpon,jenis_transaksi_telepon = jenis_transaksi_telepon,\
                foto_copy = foto_copy,ket_foto_copy= ket_foto_copy,jenis_transaksi_foto_copy = jenis_transaksi_foto_copy,\
                majalah = majalah,ket_majalah= ket_majalah,jenis_transaksi_majalah = jenis_transaksi_majalah,\
                nilai_materai = nilai_materai,keterangan_materai = keterangan_materai,
                pemb_lingkungan = pemb_lingkungan,ket_pemb_lingkungan = ket_pemb_lingkungan,\
                jenis_transaksi_pemb_lingkungan = jenis_transaksi_pemb_lingkungan,
                sumbangan= sumbangan,ket_sumbangan = ket_sumbangan,jenis_transaksi_sumbangan = jenis_transaksi_sumbangan,\
                perlengkapan = perlengkapan,ket_perlengkapan = ket_perlengkapan,\
                jenis_transaksi_perlengkapan = jenis_transaksi_perlengkapan,konsumsi = konsumsi,ket_konsumsi = ket_konsumsi,\
                jenis_transaksi_konsumsi = jenis_transaksi_konsumsi,\
                js_trans = js_trans,js_trans_kembali = js_trans_kembali,
                gaji = gaji,ket_gaji=ket_gaji,jenis_transaksi_gaji =jenis_transaksi_gaji,gaji_gerai =gaji_gerai,\
                sewa = sewa, ket_sewa= ket_sewa,jenis_transaksi_sewa =jenis_transaksi_sewa,sewa_gerai =sewa_gerai,\
                bbm = bbm, ket_bbm = ket_bbm, jenis_transaksi_bbm = jenis_transaksi_bbm, bbm_gerai = bbm_gerai,\
                tol = tol, ket_tol = ket_tol, jenis_transaksi_tol = jenis_transaksi_tol, tol_gerai = tol_gerai,\
                transport = transport, ket_transport = ket_transport, jenis_transaksi_transport = jenis_transaksi_transport,\
                transport_gerai = transport_gerai,\
                peralkantor = peralkantor, ket_peralkantor = ket_peralkantor, jenis_transaksi_peralkantor = jenis_transaksi_peralkantor,\
                peralkantor_gerai = peralkantor_gerai,penambahan_uk = penambahan_uk,ket_penambahan_uk = ket_penambahan_uk,
                pengembalian_uk = pengembalian_uk,ket_pengembalian_uk = ket_pengembalian_uk,\
                pembelian_materai=pembelian_materai,ket_pmb_materai=ket_pmb_materai,jenis_pmb_materai=jenis_pmb_materai,
                jual_materai=jual_materai,ket_jual_materai=ket_jual_materai,jenis_jual_materai=jenis_jual_materai)
            biaya.save()
            if biaya.jual_materai > 0 and biaya.jenis_jual_materai== '1':
                jurnal_jual_materai_kas(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Penjualan Materai kas ###')

            if biaya.jual_materai > 0 and biaya.jenis_jual_materai== '2':
                jurnal_jual_materai_panjar(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Penjualan Materai panjar ###')

            if biaya.pembelian_materai > 0 and biaya.jenis_pmb_materai== '':
                jurnal_pmb_materai_kas(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Pembelian Materai kas ###')

            if biaya.konsumsi> 0 and biaya.jenis_transaksi_konsumsi== '2':
                jurnal_biaya_konsumsi_panjar(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 191 ###')
            if biaya.konsumsi > 0 and biaya.jenis_transaksi_konsumsi== '1':
                jurnal_biaya_konsumsi(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 194 ###')
            if biaya.konsumsi > 0 and biaya.jenis_transaksi_konsumsi== '':
                jurnal_biaya_konsumsi_gerai_tuju_kas(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 197 ###')
            if biaya.telpon > 0 and biaya.jenis_transaksi_telepon == u'2':
                jurnal_biaya_telpon_panjar(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 200 ###')
            if biaya.telpon > 0 and biaya.jenis_transaksi_telepon == u'1':
                jurnal_biaya_telpon(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 203 ###')
            if biaya.telpon > 0 and biaya.jenis_transaksi_telepon == '':
                jurnal_biaya_telpon_gerai_tuju(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 206 ###')
            ''' Biaya Majalah Di hapus Tgl 17 Feb 2016 pa Dirman ### SEPUR           
            if biaya.majalah > 0 and biaya.jenis_transaksi_majalah == '2':#
                jurnal_biaya_majalah_panjar(biaya, request.user)
            if biaya.majalah > 0 and biaya.jenis_transaksi_majalah == '1':
                jurnal_biaya_majalah(biaya, request.user)
            if biaya.majalah > 0 and biaya.jenis_transaksi_majalah == '':
                jurnal_biaya_majalah_gerai_tuju(biaya, request.user)
            '''
            if biaya.pemb_lingkungan> 0 and biaya.jenis_transaksi_pemb_lingkungan== '2':#
                jurnal_biaya_pemb_lingkungan_panjar(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 217 ###')
            if biaya.pemb_lingkungan > 0 and biaya.jenis_transaksi_pemb_lingkungan == '1':
                jurnal_biaya_pemb_lingkungan(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 220 ###')
            if biaya.pemb_lingkungan > 0 and biaya.jenis_transaksi_pemb_lingkungan == '':
                jurnal_biaya_lingkungan_gerai_tuju(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 223 ###')
            if biaya.sumbangan> 0 and biaya.jenis_transaksi_sumbangan== '2':
                jurnal_biaya_sumbangan_panjar(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 226 ###')
            if biaya.sumbangan > 0 and biaya.jenis_transaksi_sumbangan== '1':
                jurnal_biaya_sumbangan(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 229 ###')
            if biaya.sumbangan > 0 and biaya.jenis_transaksi_sumbangan== '':
                jurnal_biaya_sumbangan_gerai_tuju(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 232 ###')
            if biaya.perlengkapan> 0 and biaya.jenis_transaksi_perlengkapan== '2':#
                jurnal_biaya_perlengkapan_panjar(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 235 ###')
            if biaya.perlengkapan > 0 and biaya.jenis_transaksi_perlengkapan== '1' :
                jurnal_biaya_perlengkapan(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 238 ###')
            if biaya.perlengkapan > 0 and biaya.jenis_transaksi_perlengkapan== '' :
                jurnal_biaya_perlengkapan_gerai_tuju(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 241 ###')
            if biaya.foto_copy > 0 and biaya.jenis_transaksi_foto_copy == '2':#
                jurnal_biaya_foto_copy_panjar(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 244 ###')
            if biaya.foto_copy > 0 and biaya.jenis_transaksi_foto_copy == '1':
                jurnal_biaya_foto_copy(biaya, request.user)
            if biaya.foto_copy > 0 and biaya.jenis_transaksi_foto_copy == '':
                jurnal_biaya_fotocopy_gerai_tuju(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 249 ###')
            if biaya.pdam > 0 and biaya.jenis_transaksi_pdam == '2':#
                jurnal_biaya_pdam_panjar(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 252 ###')
            if biaya.pdam > 0 and biaya.jenis_transaksi_pdam == '1':
                jurnal_biaya_pdam(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 255 ###')
            if biaya.pdam > 0 and biaya.jenis_transaksi_pdam == '':
                jurnal_biaya_pdam_gerai_tuju(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 258 ###')
            if biaya.listrik > 0 and biaya.jenis_transaksi_listrik == u'2':
                jurnal_biaya_listrik_panjar(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 261 ###')
            if biaya.listrik > 0 and biaya.jenis_transaksi_listrik == u'1':
                jurnal_biaya_listrik(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 264 ###')
            if biaya.listrik > 0 and biaya.jenis_transaksi_listrik == '':
                jurnal_biaya_listrik_gerai_tuju(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 267 ###')
            ### Tambahan Sepur
            if biaya.bbm > 0 and biaya.jenis_transaksi_bbm == u'2':
                jurnal_biaya_bbm_panjar(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 271 ###')
            if biaya.bbm > 0 and biaya.jenis_transaksi_bbm == u'1':
                jurnal_biaya_bbm(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 274 ###')
            if biaya.bbm > 0 and biaya.jenis_transaksi_bbm == '':
                jurnal_biaya_bbm_gerai_tuju_kas(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 277 ###')
            if biaya.tol > 0 and biaya.jenis_transaksi_tol == u'2':
                jurnal_biaya_tol_panjar(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 280 ###')
            if biaya.tol > 0 and biaya.jenis_transaksi_tol == u'1':
                jurnal_biaya_tol(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 283 ###')
            if biaya.tol > 0 and biaya.jenis_transaksi_tol == '':
                jurnal_biaya_tol_gerai_tuju_kas(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 286 ###')
            if biaya.transport > 0 and biaya.jenis_transaksi_transport == u'2':
                jurnal_biaya_transport_panjar(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 289 ###')
            if biaya.transport > 0 and biaya.jenis_transaksi_transport == u'1':
                jurnal_biaya_transport(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 292 ###')
            if biaya.transport > 0 and biaya.jenis_transaksi_transport == '':
                jurnal_biaya_transport_gerai_tuju_kas(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 295 ###')
            if biaya.peralkantor > 0 and biaya.jenis_transaksi_peralkantor == u'2':
                jurnal_biaya_peralkantor_panjar(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 298 ###')
            if biaya.peralkantor > 0 and biaya.jenis_transaksi_peralkantor == u'1':
                jurnal_biaya_peralkantor(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 301 ###')
            if biaya.peralkantor > 0 and biaya.jenis_transaksi_peralkantor == '':
                jurnal_biaya_peralkantor_gerai_tuju_kas(biaya, request.user)
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 304 ###')
            ### Akhir Tambahan Sepur
            ### Tambahan Uang Muka
            if biaya.penambahan_uk > 0 :#
                jurnal_biaya_penambahan_uk(biaya, request.user)
                messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (316)")

            if biaya.pengembalian_uk > 0 :#
                jurnal_biaya_pengembalian_uk(biaya, request.user)
                messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (320)")

            ### Akhir Tambahan Uang Muka
            if biaya.nilai_materai > 0 and biaya.antar_gerai.id != 1: # and biaya.jenis_transaksi_materai== '1':
                materai_cab = Biaya_Materai_Cab(gerai_id = biaya.antar_gerai.id, nilai = nilai_materai, tanggal = sekarang,\
                keterangan = 'Penerimaan Materai')
                materai_cab.save()
                jurnal_biaya_materai(biaya, request.user) 
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 311 ###')

            if biaya.nilai_materai > 0 and biaya.antar_gerai.id ==1: # and biaya.jenis_transaksi_materai== '1':
                materai_cab = Biaya_Materai_Cab(gerai_id = biaya.antar_gerai.id, nilai = nilai_materai, tanggal = sekarang,\
                keterangan = 'Penerimaan Materai')
                materai_cab.save()
                jurnal_biaya_materai_pusat(biaya, request.user) 
                messages.add_message(request, messages.INFO,'### Jurnal Biaya Berhasil 361 ###')            
            return HttpResponseRedirect('/keuangan/%s/add_pusat/' % (object_id))
    else:
        form  = BiayaPusatForm()
    variables = RequestContext(request, {'form': form,'bea':bea,'c':object_id,'total_kredit': sum([p.kredit for p in bea]),\
        'total_debet': sum([p.kredit for p in bea])})
    return render_to_response('biaya/addbiayapusat.html', variables)

def jurnal_biaya_materai_pusat(biaya, user):######panjar atau u" muka 30 april
    D = decimal.Decimal
    bm = MateraiPusatMapper.objects.get(item='1', cabang=biaya.antar_gerai)
    a_meterai_debet = bm.coa1
    a_materai_kredit = bm.coa2
    a_materai_debet_cabang = bm.coa_cabang_debet 
    a_materai_kredit_cabang = bm.coa_cabang_kredit
    jurnal = Jurnal.objects.create(
        diskripsi= 'Persediaan Materai Untuk %s dari Pusat' % (biaya.antar_gerai),kode_cabang = user.profile.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.keterangan_materai)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pemakaian Materai Pusat"), id_coa = a_meterai_debet,
        kredit = 0,debet = D((biaya.nilai_materai)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang_tuju =biaya.antar_gerai.kode_cabang,id_unit= 300,id_cabang=user.profile.gerai.kode_cabang,
        deskripsi = biaya.keterangan_materai)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pemakaian Materai Pusat"), id_coa = a_materai_kredit,
        debet = 0,kredit = D((biaya.nilai_materai)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang_tuju =biaya.antar_gerai.kode_cabang,id_unit= 300,id_cabang=user.profile.gerai.kode_cabang,
        deskripsi = biaya.keterangan_materai)


def jurnal_jual_materai_kas(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='penjualan_materai', cabang=user.profile.gerai)
    pembelian_debet = bm.coa_debet
    pembelian_kredit = bm.coa
    jurnal = Jurnal.objects.create(diskripsi= 'Penjualan Materai Pusat',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pmb_materai)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("PENJUALAN MATERAI PUSAT"), id_coa = pembelian_debet,deskripsi = biaya.ket_jual_materai,
        kredit = 0,debet = D((biaya.jual_materai)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("PENJUALAN MATERAI PUSAT"), id_coa = pembelian_kredit,deskripsi = biaya.ket_jual_materai,
        debet = 0,kredit = D((biaya.jual_materai)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_pmb_materai_kas(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='pembelian_materai', cabang=user.profile.gerai)
    pembelian_debet = bm.coa_debet
    pembelian_kredit = bm.coa
    jurnal = Jurnal.objects.create(diskripsi= 'Pembelian Materai Pusat',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pmb_materai)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("PEMBELIAN MATERAI PUSAT"), id_coa = pembelian_debet,deskripsi = biaya.ket_pmb_materai,
        kredit = 0,debet = D((biaya.pembelian_materai)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("PEMBELIAN MATERAI PUSAT"), id_coa = pembelian_kredit,deskripsi = biaya.ket_pmb_materai,
        debet = 0,kredit = D((biaya.pembelian_materai)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_uk(biaya, user):
    D = decimal.Decimal
    bm =UangMukaGeraiMapper.objects.get(item='1', cabang=user.profile.gerai)
    a_penambahan_uk_kredit = bm.kredit_pengambilan_uk
    a_penambahan_uk_debet = bm.debet_pengambilan_uk

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengambilan Uang Muka',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_uk)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = a_penambahan_uk_debet,deskripsi= biaya.ket_penambahan_uk,
        kredit = 0,debet = D((biaya.penambahan_uk)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = a_penambahan_uk_kredit,deskripsi= biaya.ket_penambahan_uk,
        debet = 0,kredit = D((biaya.penambahan_uk)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_pengembalian_uk(biaya, user):
    D = decimal.Decimal
    bm = UangMukaGeraiMapper.objects.get(item='2', cabang=user.profile.gerai)
    a_pengembalian_uk_debet = bm.debet_pengembalian_uk
    a_pengembalian_uk_kredit = bm.kredit_pengembalian_uk
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengembalian Uang Muka',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pengembalian_uk)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_UK"), id_coa = a_pengembalian_uk_debet,deskripsi = biaya.ket_pengembalian_uk,
        kredit = 0,debet = D((biaya.pengembalian_uk)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_UK"), id_coa = a_pengembalian_uk_kredit,deskripsi = biaya.ket_pengembalian_uk,
        debet = 0,kredit = D((biaya.pengembalian_uk)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
### Akhir Tambahan Uang Muka
###TAMBAHAN SEPUR
def jurnal_biaya_bbm_panjar(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='bbm', cabang=user.profile.gerai)
    bbm_debet = bm.coa_debet
    bbm_kredit = bm.coa_uk
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Uang Muka Bbm',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_bbm)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = konsumsi_debet,deskripsi = biaya.ket_bbm,
        kredit = 0,debet = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = bbm_kredit,deskripsi = biaya.ket_bbm,
        debet = 0,kredit = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_bbm(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='bbm', cabang=user.profile.gerai)
    bbm_debet = bm.coa_debet
    bbm_kredit = bm.coa
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Bbm',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_bbm)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = bbm_debet,deskripsi = biaya.ket_bbm,
        kredit = 0,debet = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT"), id_coa = bbm_kredit,deskripsi = biaya.ket_bbm,
        debet = 0,kredit = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_bbm_gerai_tuju_kas(biaya, user):
    D = decimal.Decimal
    bm = BiayaPusatMapper.objects.get(item='bbm',jenis = None)
    bbm_debet = bm.coa_debet
    bbm_kredit = bm.coa
    debet_tuju = bm.coa_debet_tuju
    kredit_tuju = bm.coa_kredit_tuju
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Bbm Untuk %s' % (biaya.bbm_gerai),kode_cabang = biaya.gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_bbm)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = bbm_debet,deskripsi = biaya.ket_bbm,
        kredit = 0,debet = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT"), id_coa = bbm_kredit,deskripsi = biaya.ket_bbm,
        debet = 0,kredit = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    #####Gerai 
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Bbm Untuk %s' % (biaya.bbm_gerai),kode_cabang = biaya.bbm_gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_bbm)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_CABANG"), id_coa = debet_tuju,deskripsi = biaya.ket_bbm,
        kredit = 0,debet = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.bbm_gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_CABANG"), id_coa = kredit_tuju,deskripsi = biaya.ket_bbm,
        debet = 0,kredit = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.bbm_gerai.kode_cabang,id_unit= 300)
####BATAS BBM

def jurnal_biaya_tol_panjar(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='parkir', cabang=user.profile.gerai)
    #bm = BiayaPusatMapper.objects.get(item='tol', cabang=user.profile.gerai)
    tol_debet = bm.coa_debet
    tol_kredit = bm.coa_uk
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Uang Muka Tol Dan Parkir',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_tol)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = tol_debet,deskripsi = biaya.ket_tol,
        kredit = 0,debet = D((biaya.tol)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = tol_kredit,deskripsi = biaya.ket_tol,
        debet = 0,kredit = D((biaya.tol)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_tol(biaya, user):
    D = decimal.Decimal
    #bm = BiayaMapper.objects.get(item='tol', cabang=user.profile.gerai)
    bm = BiayaMapper.objects.get(item='parkir', cabang=user.profile.gerai)
    tol_debet = bm.coa_debet
    tol_kredit = bm.coa
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Tol Dan Parkir',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_tol)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = tol_debet,deskripsi = biaya.ket_tol,
        kredit = 0,debet = D((biaya.tol)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT"), id_coa = tol_kredit,deskripsi = biaya.ket_tol,
        debet = 0,kredit = D((biaya.tol)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_tol_gerai_tuju_kas(biaya, user):
    D = decimal.Decimal
    bm = BiayaPusatMapper.objects.get(item='tol',jenis = None)
    tol_debet = bm.coa_debet
    tol_kredit = bm.coa
    debet_tuju = bm.coa_debet_tuju
    kredit_tuju = bm.coa_kredit_tuju
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Tol Dan Parkir Untuk %s' % (biaya.tol_gerai),kode_cabang = biaya.gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_tol)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = tol_debet,deskripsi = biaya.ket_tol,
        kredit = 0,debet = D((biaya.tol)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT"), id_coa = tol_kredit,deskripsi = biaya.ket_tol,
        debet = 0,kredit = D((biaya.tol)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    #####Gerai 
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Konsumsi Untuk %s' % (biaya.tol_gerai),kode_cabang = biaya.tol_gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_tol)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_CABANG"), id_coa = debet_tuju,deskripsi = biaya.ket_tol,
        kredit = 0,debet = D((biaya.tol)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.tol_gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_CABANG"), id_coa = kredit_tuju,deskripsi = biaya.ket_tol,
        debet = 0,kredit = D((biaya.tol)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.tol_gerai.kode_cabang,id_unit= 300)
####BATAS TOL

def jurnal_biaya_transport_panjar(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='transport', cabang=user.profile.gerai)
    transport_debet = bm.coa_debet
    transport_kredit = bm.coa_uk
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Uang Muka Transport',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_transport)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = transport_debet,deskripsi = biaya.ket_transport,
        kredit = 0,debet = D((biaya.transport)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = transport_kredit,deskripsi = biaya.ket_transport,
        debet = 0,kredit = D((biaya.transport)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_transport(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='transport', cabang=user.profile.gerai)
    transport_debet = bm.coa_debet
    transport_kredit = bm.coa
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Transport',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_transport)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = transport_debet,deskripsi = biaya.ket_transport,
        kredit = 0,debet = D((biaya.transport)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT"), id_coa = transport_kredit,deskripsi = biaya.ket_transport,
        debet = 0,kredit = D((biaya.transport)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_transport_gerai_tuju_kas(biaya, user):
    D = decimal.Decimal
    bm = BiayaPusatMapper.objects.get(item='transport',jenis = None)
    transport_debet = bm.coa_debet
    transport_kredit = bm.coa
    debet_tuju = bm.coa_debet_tuju
    kredit_tuju = bm.coa_kredit_tuju
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Transport Untuk %s' % (biaya.transport_gerai),kode_cabang = biaya.gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_transport)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = transport_debet,deskripsi = biaya.ket_transport,
        kredit = 0,debet = D((biaya.transport)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT"), id_coa = transport_kredit,deskripsi = biaya.ket_transport,
        debet = 0,kredit = D((biaya.transport)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    #####Gerai 
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Transport Untuk %s' % (biaya.transport_gerai),\
        kode_cabang = biaya.transport_gerai.kode_cabang,object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,\
        nobukti=biaya.ket_transport)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_CABANG"), id_coa = debet_tuju,deskripsi = biaya.ket_transport,
        kredit = 0,debet = D((biaya.transport)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.transport_gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_CABANG"), id_coa = kredit_tuju,deskripsi = biaya.ket_transport,
        debet = 0,kredit = D((biaya.transport)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.transport_gerai.kode_cabang,id_unit= 300)
####BATAS TRANSPORT

def jurnal_biaya_peralkantor_panjar(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='peralkantor', cabang=user.profile.gerai)
    peralkantor_debet = bm.coa_debet
    peralkantor_kredit = bm.coa_uk
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Uang Muka Peral. Kantor',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_peralkantor)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = peralkantor_debet,deskripsi = biaya.ket_peralkantor,
        kredit = 0,debet = D((biaya.peralkantor)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = peralkantor_kredit,deskripsi = biaya.ket_peralkantor,
        debet = 0,kredit = D((biaya.peralkantor)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_peralkantor(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='peralkantor', cabang=user.profile.gerai)
    peralkantor_debet = bm.coa_debet
    peralkantor_kredit = bm.coa
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Peral. Kantor',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_peralkantor)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = peralkantor_debet,deskripsi = biaya.ket_peralkantor,
        kredit = 0,debet = D((biaya.peralkantor)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT"), id_coa = peralkantor_kredit,deskripsi = biaya.ket_peralkantor,
        debet = 0,kredit = D((biaya.peralkantor)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_peralkantor_gerai_tuju_kas(biaya, user):
    D = decimal.Decimal
    bm = BiayaPusatMapper.objects.get(item='peralkantor',jenis = None)
    peralkantor_debet = bm.coa_debet
    peralkantor_kredit = bm.coa
    debet_tuju = bm.coa_debet_tuju
    kredit_tuju = bm.coa_kredit_tuju
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Peral. Kantor Untuk %s' % (biaya.peralkantor_gerai),kode_cabang = biaya.gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_peralkantor)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = peralkantor_debet,deskripsi = biaya.ket_peralkantor,
        kredit = 0,debet = D((biaya.peralkantor)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT"), id_coa = peralkantor_kredit,deskripsi = biaya.ket_peralkantor,
        debet = 0,kredit = D((biaya.peralkantor)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    #####Gerai 
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Peral Kantor Untuk %s' % (biaya.peralkantor_gerai),\
        kode_cabang = biaya.peralkantor_gerai.kode_cabang,object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,\
        nobukti=biaya.ket_peralkantor)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_CABANG"), id_coa = debet_tuju,deskripsi = biaya.ket_peralkantor,
        kredit = 0,debet = D((biaya.peralkantor)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.peralkantor_gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_CABANG"), id_coa = kredit_tuju,deskripsi = biaya.ket_peralkantor,
        debet = 0,kredit = D((biaya.peralkantor)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.peralkantor_gerai.kode_cabang,id_unit= 300)
####BATAS PERALATAN KANTOR

###AKHIR TAMBAHAN SEPUR


def jurnal_biaya_konsumsi_panjar(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='konsumsi', cabang=user.profile.gerai)
    konsumsi_debet = bm.coa_debet
    konsumsi_kredit = bm.coa_uk
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Uang Muka Konsumsi',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = konsumsi_debet,deskripsi = biaya.ket_konsumsi,
        kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = konsumsi_kredit,deskripsi = biaya.ket_konsumsi,
        debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_konsumsi(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='konsumsi', cabang=user.profile.gerai)
    konsumsi_debet = bm.coa_debet
    konsumsi_kredit = bm.coa
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran  Konsumsi',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = konsumsi_debet,deskripsi = biaya.ket_konsumsi,
        kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT"), id_coa = konsumsi_kredit,deskripsi = biaya.ket_konsumsi,
        debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_konsumsi_gerai_tuju_kas(biaya, user):
    D = decimal.Decimal
    bm = BiayaPusatMapper.objects.get(item='konsumsi',jenis = None)
    konsumsi_debet = bm.coa_debet
    konsumsi_kredit = bm.coa
    debet_tuju = bm.coa_debet_tuju
    kredit_tuju = bm.coa_kredit_tuju
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Konsumsi Untuk %s' % (biaya.konsumsi_gerai),kode_cabang = biaya.gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = konsumsi_debet,deskripsi = biaya.ket_konsumsi,
        kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT"), id_coa = konsumsi_kredit,deskripsi = biaya.ket_konsumsi,
        debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    #####Gerai 
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Konsumsi Untuk %s' % (biaya.konsumsi_gerai),kode_cabang = biaya.konsumsi_gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_CABANG"), id_coa = debet_tuju,deskripsi = biaya.ket_konsumsi,
        kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.konsumsi_gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_CABANG"), id_coa = kredit_tuju,deskripsi = biaya.ket_konsumsi,
        debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.konsumsi_gerai.kode_cabang,id_unit= 300)
####BATAS KONSUMSI
####TELEPON
def jurnal_biaya_telpon_panjar(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='telepon', cabang=user.profile.gerai)
    majalah_debet = bm.coa_debet
    majalah_kredit = bm.coa_uk
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Uang Muka Telepon',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_majalah)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = majalah_debet,
        kredit = 0,debet = D((biaya.telpon)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_telpon,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = majalah_kredit,
        debet = 0,kredit = D((biaya.telpon)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_telpon,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_telpon(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='telepon', cabang=user.profile.gerai)
    majalah_debet = bm.coa_debet
    majalah_kredit = bm.coa
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Telpon',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_majalah)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = majalah_debet,deskripsi = biaya.ket_telpon,
        kredit = 0,debet = D((biaya.telpon)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = majalah_kredit,deskripsi = biaya.ket_telpon,
        debet = 0,kredit = D((biaya.telpon)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_telpon_gerai_tuju(biaya, user):
    D = decimal.Decimal
    bm = BiayaPusatMapper.objects.get(item='telepon',jenis = None)
    konsumsi_debet = bm.coa_debet
    konsumsi_kredit = bm.coa
    debet_tuju = bm.coa_debet_tuju
    kredit_tuju = bm.coa_kredit_tuju
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Telepon Untuk %s' % (biaya.konsumsi_gerai),kode_cabang = biaya.gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = konsumsi_debet,deskripsi = biaya.ket_konsumsi,
        kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT"), id_coa = konsumsi_kredit,deskripsi = biaya.ket_konsumsi,
        debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    #####Gerai 
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Telepon Untuk %s' % (biaya.konsumsi_gerai),kode_cabang = biaya.konsumsi_gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_CABANG"), id_coa = debet_tuju,deskripsi = biaya.ket_konsumsi,
        kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.konsumsi_gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_CABANG"), id_coa = kredit_tuju,deskripsi = biaya.ket_konsumsi,
        debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.konsumsi_gerai.kode_cabang,id_unit= 300)
#####BATAS TELEPON
#####MAJALAH
def jurnal_biaya_majalah_panjar(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='majalah', cabang=user.profile.gerai)
    majalah_debet = bm.coa_debet
    majalah_kredit = bm.coa_uk
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Uang Muka Majalah',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_majalah)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = majalah_debet,
        kredit = 0,debet = D((biaya.majalah)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = majalah_kredit,
        debet = 0,kredit = D((biaya.majalah)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_majalah(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='majalah', cabang=user.profile.gerai)
    majalah_debet = bm.coa_debet
    majalah_kredit = bm.coa
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran  Majalah',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_majalah)
    
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = majalah_debet,
        kredit = 0,debet = D((biaya.majalah)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = majalah_kredit,
        debet = 0,kredit = D((biaya.majalah)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_majalah_gerai_tuju(biaya, user):
    D = decimal.Decimal
    bm = BiayaPusatMapper.objects.get(item='majalah',jenis = None)
    konsumsi_debet = bm.coa_debet
    konsumsi_kredit = bm.coa
    debet_tuju = bm.coa_debet_tuju
    kredit_tuju = bm.coa_kredit_tuju
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran majalah  Untuk %s' % (biaya.konsumsi_gerai),kode_cabang = biaya.gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = konsumsi_debet,deskripsi = biaya.ket_konsumsi,
        kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT"), id_coa = konsumsi_kredit,deskripsi = biaya.ket_konsumsi,
        debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    #####Gerai 
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Majalah Untuk %s' % (biaya.konsumsi_gerai),kode_cabang = biaya.konsumsi_gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_CABANG"), id_coa = debet_tuju,deskripsi = biaya.ket_konsumsi,
        kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.konsumsi_gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_CABANG"), id_coa = kredit_tuju,deskripsi = biaya.ket_konsumsi,
        debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.konsumsi_gerai.kode_cabang,id_unit= 300)
##### BATAS MAJALAH
##### LINGKUNGAN
def jurnal_biaya_pemb_lingkungan_panjar(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='lingkungan', cabang=user.profile.gerai)
    lingkungan_debet = bm.coa_debet
    lingkungan_kredit = bm.coa_uk
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Uang Muka Lingkungan',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.pemb_lingkungan)
    
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = lingkungan_debet,deskripsi=biaya.ket_pemb_lingkungan,
        kredit = 0,debet = D((biaya.pemb_lingkungan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = lingkungan_kredit,deskripsi=biaya.ket_pemb_lingkungan,
        debet = 0,kredit = D((biaya.pemb_lingkungan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_pemb_lingkungan(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='lingkungan', cabang=user.profile.gerai)
    lingkungan_debet = bm.coa_debet
    lingkungan_kredit = bm.coa
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran  Lingkungan',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.pemb_lingkungan)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = lingkungan_debet,deskripsi=biaya.ket_pemb_lingkungan,
        kredit = 0,debet = D((biaya.pemb_lingkungan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT"), id_coa = lingkungan_kredit,deskripsi = biaya.ket_konsumsi,
        debet = 0,kredit = D((biaya.pemb_lingkungan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_lingkungan_gerai_tuju(biaya, user):
    D = decimal.Decimal
    bm = BiayaPusatMapper.objects.get(item='lingkungan',jenis = None)
    konsumsi_debet = bm.coa_debet
    konsumsi_kredit = bm.coa
    debet_tuju = bm.coa_debet_tuju
    kredit_tuju = bm.coa_kredit_tuju
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran iuran Lingkungan Untuk %s' % (biaya.konsumsi_gerai),kode_cabang = biaya.gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = konsumsi_debet,deskripsi = biaya.ket_konsumsi,
        kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT"), id_coa = konsumsi_kredit,deskripsi = biaya.ket_konsumsi,
        debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    #####Gerai 
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Lingkungan Untuk %s' % (biaya.konsumsi_gerai),\
        kode_cabang = biaya.konsumsi_gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_CABANG"), id_coa = debet_tuju,deskripsi = biaya.ket_konsumsi,
        kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.konsumsi_gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_CABANG"), id_coa = kredit_tuju,deskripsi = biaya.ket_konsumsi,
        debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.konsumsi_gerai.kode_cabang,id_unit= 300)
####BATAS LINGKUNGAN

#### PERLENGKAPAN
def jurnal_biaya_perlengkapan_panjar(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='perlengkapan', cabang=user.profile.gerai)
    perlengkapan_debet = bm.coa_debet
    perlengkapan_kredit = bm.coa_uk
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Uang Muka Perlengkapan',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_perlengkapan)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = perlengkapan_debet,deskripsi =biaya.ket_perlengkapan,
        kredit = 0,debet = D((biaya.perlengkapan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = perlengkapan_kredit,deskripsi =biaya.ket_perlengkapan,
        debet = 0,kredit = D((biaya.perlengkapan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_perlengkapan(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='perlengkapan', cabang=user.profile.gerai)
    perlengkapan_debet = bm.coa_debet
    perlengkapan_kredit = bm.coa
    jurnal = Jurnal.objects.create(
            diskripsi= 'Pembayaran  Perlengkapan',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
            tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_perlengkapan)

    jurnal.tbl_transaksi_set.create(
            jenis = '%s' % ("GL_GL_PUSAT"), id_coa = perlengkapan_debet,deskripsi =biaya.ket_perlengkapan,
            kredit = 0,debet = D((biaya.perlengkapan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
            id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
            jenis = '%s' % ("GL_GL_PUSAT"), id_coa = perlengkapan_kredit,deskripsi =biaya.ket_perlengkapan,
            debet = 0,kredit = D((biaya.perlengkapan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
            id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
##### BATAS PERLENGKAPAN

##### SUMBANGAN 
def jurnal_biaya_sumbangan_panjar(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='sumbangan', cabang=user.profile.gerai)
    sumbangan_debet = bm.coa_debet
    sumbangan_kredit = bm.coa_uk
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Uang Muka SUMBANGAN',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_sumbangan)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = sumbangan_debet,deskripsi = biaya.ket_sumbangan,
        kredit = 0,debet = D((biaya.sumbangan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = sumbangan_kredit,deskripsi = biaya.ket_sumbangan,
        debet = 0,kredit = D((biaya.sumbangan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_sumbangan(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='sumbangan', cabang=user.profile.gerai)
    sumbangan_debet = bm.coa_debet
    sumbangan_kredit = bm.coa
    jurnal = Jurnal.objects.create(
            diskripsi= 'Pembayaran  sumbangan',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
            tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_sumbangan)

    jurnal.tbl_transaksi_set.create(
            jenis = '%s' % ("GL_GL_PUSAT"), id_coa = sumbangan_debet,deskripsi = biaya.ket_sumbangan,
            kredit = 0,debet = D((biaya.sumbangan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
            id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
            jenis = '%s' % ("GL_GL_PUSAT"), id_coa = sumbangan_kredit,deskripsi = biaya.ket_sumbangan,
            debet = 0,kredit = D((biaya.sumbangan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
            id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_sumbangan_gerai_tuju(biaya, user):
    D = decimal.Decimal
    bm = BiayaPusatMapper.objects.get(item='sumbangan',jenis = None)
    konsumsi_debet = bm.coa_debet
    konsumsi_kredit = bm.coa
    debet_tuju = bm.coa_debet_tuju
    kredit_tuju = bm.coa_kredit_tuju
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran sumbangan Untuk %s' % (biaya.konsumsi_gerai),kode_cabang = biaya.gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = konsumsi_debet,
        kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_sumbangan,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT"), id_coa = konsumsi_kredit,deskripsi = biaya.ket_sumbangan,
        debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    #####Gerai 
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Sumbangan Untuk %s' % (biaya.konsumsi_gerai),\
        kode_cabang = biaya.konsumsi_gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_CABANG"), id_coa = debet_tuju,
        kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_sumbangan,
        id_cabang =biaya.konsumsi_gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_CABANG"), id_coa = kredit_tuju,deskripsi = biaya.ket_sumbangan,
        debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.konsumsi_gerai.kode_cabang,id_unit= 300)
####BATAS SUMBANGAN
####FOTOCOPY
def jurnal_biaya_foto_copy_panjar(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='fotocopy', cabang=user.profile.gerai)
    fotocopy_debet = bm.coa_debet
    fotocopy_kredit = bm.coa_uk
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Uang Muka FOTOCOPY',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_foto_copy)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = fotocopy_debet,deskripsi = biaya.ket_foto_copy,
        kredit = 0,debet = D((biaya.foto_copy)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = fotocopy_kredit,deskripsi = biaya.ket_foto_copy,
        debet = 0,kredit = D((biaya.foto_copy)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_foto_copy(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='fotocopy', cabang=user.profile.gerai)
    fotocopy_debet = bm.coa_debet
    fotocopy_kredit = bm.coa
    jurnal = Jurnal.objects.create(
            diskripsi= 'Pembayaran  Fotocopy',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
            tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_foto_copy)

    jurnal.tbl_transaksi_set.create(
            jenis = '%s' % ("GL_GL_PUSAT"), id_coa = fotocopy_debet,
            kredit = 0,debet = D((biaya.foto_copy)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_foto_copy,
            id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
            jenis = '%s' % ("GL_GL_PUSAT"), id_coa = fotocopy_kredit,
            debet = 0,kredit = D((biaya.foto_copy)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,deskripsi = biaya.ket_foto_copy,
            id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_fotocopy_gerai_tuju(biaya, user):
    D = decimal.Decimal
    bm = BiayaPusatMapper.objects.get(item='fotocopy',jenis = None)
    konsumsi_debet = bm.coa_debet
    konsumsi_kredit = bm.coa
    debet_tuju = bm.coa_debet_tuju
    kredit_tuju = bm.coa_kredit_tuju
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran fotocopy Untuk %s' % (biaya.konsumsi_gerai),kode_cabang = biaya.gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = konsumsi_debet,deskripsi = biaya.ket_konsumsi,
        kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT"), id_coa = konsumsi_kredit,deskripsi = biaya.ket_konsumsi,
        debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    #####Gerai 
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Fotocopy Untuk %s' % (biaya.konsumsi_gerai),\
        kode_cabang = biaya.konsumsi_gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_CABANG"), id_coa = debet_tuju,deskripsi = biaya.ket_konsumsi,
        kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.konsumsi_gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_CABANG"), id_coa = kredit_tuju,deskripsi = biaya.ket_konsumsi,
        debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.konsumsi_gerai.kode_cabang,id_unit= 300)
######BATAS FOTOCOPY
######PDAM
def jurnal_biaya_pdam_panjar(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='pdam', cabang=user.profile.gerai)
    pdam_debet = bm.coa_debet
    pdam_kredit = bm.coa_uk
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Uang Muka PDAM',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pdam)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = pdam_debet,deskripsi =biaya.ket_pdam,
        kredit = 0,debet = D((biaya.listrik)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = pdam_kredit,deskripsi =biaya.ket_pdam,
        debet = 0,kredit = D((biaya.listrik)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_pdam(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='pdam', cabang=user.profile.gerai)
    pdam_debet = bm.coa_debet
    pdam_kredit = bm.coa
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran  PDAM',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pdam)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = pdam_debet,deskripsi =biaya.ket_pdam,
        kredit = 0,debet = D((biaya.pdam)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = pdam_kredit,deskripsi =biaya.ket_pdam,
        debet = 0,kredit = D((biaya.pdam)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_fotocopy_gerai_tuju(biaya, user):
    D = decimal.Decimal
    bm = BiayaPusatMapper.objects.get(item='pdam',jenis = None)
    konsumsi_debet = bm.coa_debet
    konsumsi_kredit = bm.coa
    debet_tuju = bm.coa_debet_tuju
    kredit_tuju = bm.coa_kredit_tuju
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran PDAM Untuk %s' % (biaya.konsumsi_gerai),kode_cabang = biaya.gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = konsumsi_debet,deskripsi = biaya.ket_konsumsi,
        kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT"), id_coa = konsumsi_kredit,deskripsi = biaya.ket_konsumsi,
        debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    #####Gerai 
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran PDAM Untuk %s' % (biaya.konsumsi_gerai),\
        kode_cabang = biaya.konsumsi_gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_CABANG"), id_coa = debet_tuju,deskripsi = biaya.ket_konsumsi,
        kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.konsumsi_gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_CABANG"), id_coa = kredit_tuju,deskripsi = biaya.ket_konsumsi,
        debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.konsumsi_gerai.kode_cabang,id_unit= 300)
#####BATAS PDAM
#####BBM
#def jurnal_biaya_bbm_panjar(biaya, user):
	#D = decimal.Decimal
        #bm = BiayaMapper.objects.get(item='bbm', cabang=user.profile.gerai)
        #a_listrik_debet = bm.coa_debet
        #a_listrik_kredit = bm.coa_uk
	#jurnal = Jurnal.objects.create(
		#diskripsi= 'Pembayaran Uang Muka BBM',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		#tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_listrik)

	#jurnal.tbl_transaksi_set.create(
		#jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = a_listrik_debet,
		#kredit = 0,debet = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		#id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	#jurnal.tbl_transaksi_set.create(
		#jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = a_listrik_kredit,
		#debet = 0,kredit = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		#id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

#def jurnal_biaya_bbm(biaya, user):
    #D = decimal.Decimal
    #bm = BiayaMapper.objects.get(item='bbm', cabang=user.profile.gerai)
    #bbm_debet = bm.coa_debet
    #bbm_kredit = bm.coa
    #jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran  bbm',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        #tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_bbm)

    #jurnal.tbl_transaksi_set.create(
        #jenis = '%s' % ("GL_GL_PUSAT"), id_coa = bbm_debet,
        #kredit = 0,debet = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        #id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    #jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = bbm_kredit,
        #debet = 0,kredit = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        #id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
#####BATAS BBM
#####LISTRIK
def jurnal_biaya_listrik_panjar(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='listrik', cabang=user.profile.gerai)
    a_listrik_debet = bm.coa_debet
    a_listrik_kredit = bm.coa_uk
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Uang Muka Listrik',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_listrik)
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = a_listrik_debet,deskripsi = biaya.ket_listrik,
        kredit = 0,debet = D((biaya.listrik)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = a_listrik_kredit,deskripsi = biaya.ket_listrik,
        debet = 0,kredit = D((biaya.listrik)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_listrik(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='listrik', cabang=user.profile.gerai)
    a_listrik_debet = bm.coa_debet
    a_listrik_kredit = bm.coa
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran  Listrik',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_listrik)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT"), id_coa = a_listrik_debet,deskripsi = biaya.ket_listrik,
        kredit = 0,debet = D((biaya.listrik)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = a_listrik_kredit,deskripsi = biaya.ket_listrik,
        debet = 0,kredit = D((biaya.listrik)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_listrik_gerai_tuju(biaya, user):
    D = decimal.Decimal
    bm = BiayaPusatMapper.objects.get(item='listrik',jenis = None)
    konsumsi_debet = bm.coa_debet
    konsumsi_kredit = bm.coa
    debet_tuju = bm.coa_debet_tuju
    kredit_tuju = bm.coa_kredit_tuju
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Listrik Untuk %s' % (biaya.konsumsi_gerai),kode_cabang = biaya.gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PUSAT"), id_coa = konsumsi_debet,deskripsi = biaya.ket_listrik,
        kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PUSAT"), id_coa = konsumsi_kredit,deskripsi = biaya.ket_listrik,
        debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    #####Gerai 
    jurnal = Jurnal.objects.create(diskripsi= 'Pembayaran Listrik Untuk %s' % (biaya.konsumsi_gerai),\
        kode_cabang = biaya.konsumsi_gerai.kode_cabang,\
        object_id=biaya.id,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_CABANG"), id_coa = debet_tuju,deskripsi = biaya.ket_listrik,
        kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.konsumsi_gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_CABANG"), id_coa = kredit_tuju,deskripsi = biaya.ket_listrik,
        debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.konsumsi_gerai.kode_cabang,id_unit= 300)

######BATAS LISTRIK
def jurnal_biaya_materai(biaya, user):######panjar atau u" muka 30 april
    D = decimal.Decimal
    bm = MateraiPusatMapper.objects.get(item='1', cabang=biaya.antar_gerai)
    a_meterai_debet = bm.coa1
    a_materai_kredit = bm.coa2
    a_materai_debet_cabang = bm.coa_cabang_debet 
    a_materai_kredit_cabang = bm.coa_cabang_kredit
    jurnal = Jurnal.objects.create(
        diskripsi= 'Persediaan Materai Untuk %s dari Pusat' % (biaya.antar_gerai),kode_cabang = user.profile.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.keterangan_materai)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penerimaan Materai"), id_coa = a_meterai_debet,
        kredit = 0,debet = D((biaya.nilai_materai)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang_tuju =biaya.antar_gerai.kode_cabang,id_unit= 300,id_cabang=user.profile.gerai.kode_cabang,
        deskripsi = biaya.keterangan_materai)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penerimaan Materai"), id_coa = a_materai_kredit,
        debet = 0,kredit = D((biaya.nilai_materai)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang_tuju =biaya.antar_gerai.kode_cabang,id_unit= 300,id_cabang=user.profile.gerai.kode_cabang,
        deskripsi = biaya.keterangan_materai)

    jurnal = Jurnal.objects.create(
        diskripsi= 'Persediaan Materai Untuk %s dari Pusat' % (biaya.antar_gerai),kode_cabang = biaya.antar_gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_listrik)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penerimaan Materai"), id_coa = a_materai_debet_cabang,
        kredit = 0,debet = D((biaya.nilai_materai)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang_tuju =biaya.antar_gerai.kode_cabang,id_unit= 300,id_cabang=biaya.antar_gerai.kode_cabang,
        deskripsi = biaya.keterangan_materai)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penerimaan Materai"), id_coa = a_materai_kredit_cabang,
        debet = 0,kredit = D((biaya.nilai_materai)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang_tuju =biaya.antar_gerai.kode_cabang,id_unit= 300,id_cabang=biaya.antar_gerai.kode_cabang,
        deskripsi = biaya.keterangan_materai)
####### BATAS JURNAL YANG HARUS DI PERBAIKI
	
def cari(request):
	rekening=request.GET['rekening']

	try:
		ag=AkadGadai.objects.get(id=int(rekening))
		return HttpResponseRedirect("/biaya/%s/show/" % ag.id)
	except:
		request.user.message_set.create(message="No rekening tidak ditemukan.")
		return HttpResponseRedirect("/biaya/")

def edit(request,object_id):
	biy=Biaya.objects.get(id=object_id)

	template='biaya/edit.html'
	variable = RequestContext(request,{'biy': biy})
	return render_to_response(template,variable)

def hapus_jurnal(request,object_id):
	tbl = Tbl_Transaksi.objects.get(id=object_id)
	tbl.delete()
	messages.add_message(request, messages.INFO, 'Penghapusan Jurnal Berhasil')
	return HttpResponseRedirect(tbl.get_absolute_url_biaya_keuangan() )

def biaya_post(request):
    user = request.user
    for i in request.POST.getlist('id_pilih'):        
        gl = Jurnal.objects.get(id=(i))
        jurnal = gl.tbl_transaksi_set.filter(tgl_trans= datetime.date.today()).filter(jurnal__id =gl.id) 
        for mutasi in jurnal:
            mutasi.status_jurnal = 2  
            mutasi.save()          
    return HttpResponseRedirect("/keuangan/%s/add/" % user.profile.gerai.kode_cabang)

def show(request,object_id):
	ag = Biaya.objects.get(id=object_id)
	sekarang = datetime.datetime.now()
	template = 'biaya/show.html'
	variable = RequestContext(request, {
		'ag': ag})
	return render_to_response(template,variable)

def list(request):
	bea = Biaya.objects.all()
	paginator = Paginator(bea, 50)

	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		bea = paginator.page(page)
	except (EmptyPage, InvalidPage):
		bea = paginator.page(paginator.num_pages)

	template='biaya/index.html'
	variable = RequestContext(request,{'bea': bea})
	return render_to_response(template,variable)

def add(request,object_id):
    sekarang = datetime.date.today()
    c = object_id
    bea = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=object_id).filter(status_jurnal = 1L).\
        filter(jenis__in= (u'GL_GL_PENAMBAHAN_PUSAT_BANK',u'GL_GL_PENAMBAHAN_PUSAT_KAS',u'GL_GL_PENGELUARAN_PUSAT_BANK',\
        u'GL_GL_PENGELUARAN_PUSAT_KAS',u'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI','GL_GL_PENGELUARAN_PUSAT_KAS_GERAI','GL_GL_PENGEMBALIAN_PUSAT_BANK',\
        'GL_GL_PENGEMBALIAN_PUSAT_BANK_RAK','GL_GL_RAK_PUSAT'))
	
    user = request.user
    if request.method == "POST":
        form = BiayasForm(request.POST)
        if form.is_valid():
            penambahan_saldo = form.cleaned_data['penambahan_saldo']
            ket_penambahan_saldo = form.cleaned_data['ket_penambahan_saldo']
            pengembalian_saldo = form.cleaned_data['pengembalian_saldo']
            ket_pengembalian_saldo = form.cleaned_data['ket_pengembalian_saldo']
            js_trans = form.cleaned_data['js_trans']
            antar_gerai = form.cleaned_data['antar_gerai']
            js_trans_kembali = form.cleaned_data['js_trans_kembali']
            antar_gerai_kembali = form.cleaned_data['antar_gerai_kembali']
            tanggal = form.cleaned_data['tanggal']
            #gerai = form.cleaned_data['gerai']
	
	    biaya = Biaya(gerai=user.profile.gerai,tanggal=tanggal,penambahan_saldo = penambahan_saldo,ket_penambahan_saldo =ket_penambahan_saldo,\
                pengembalian_saldo = pengembalian_saldo,ket_pengembalian_saldo=ket_pengembalian_saldo,js_trans = js_trans,\
                antar_gerai = antar_gerai,antar_gerai_kembali=antar_gerai_kembali,js_trans_kembali=js_trans_kembali)
	    biaya.save()
            if biaya.penambahan_saldo > 0 and biaya.js_trans == 'BANK': #
                jurnal_biaya_penambahan_saldo_pusat_bank(biaya, request.user)
                messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN 1275")
            #####penerimaan Pusat Kas
            if biaya.penambahan_saldo > 0  and biaya.js_trans == 'KAS'  :
                jurnal_biaya_penambahan_saldo_pusat_kas(biaya, request.user)
                messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN 1279")            
            #####pengeluaran Pusat Bank
            if biaya.pengembalian_saldo > 0 and biaya.js_trans_kembali == 'BANK' :
                jurnal_biaya_pengembalian_saldo_pusat_bank_kecabang(biaya, request.user)
                messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN 1283")
            if biaya.pengembalian_saldo > 0 and biaya.js_trans_kembali == 'KAS' :#
                jurnal_biaya_pengembalian_saldo_pusat_kas_kecabang(biaya, request.user)
                messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN 1286")
	    return HttpResponseRedirect('/keuangan/%s/add/' % (object_id))
        else:
  	    form  = BiayasForm()
	    #form.fields['gerai'].queryset = Tbl_Cabang.objects.filter(kode_cabang=object_id)
  	variables = RequestContext(request, {'form': form,'bea':bea,'c':object_id,'total_kredit': sum([p.kredit for p in bea]),\
            'total_debet': sum([p.kredit for p in bea])})
	return HttpResponseRedirect('/keuangan/%s/add/' % (object_id))
    else:
        form  = BiayasForm()
	#form.fields['gerai'].queryset = Tbl_Cabang.objects.filter(kode_cabang=object_id)
    variables = RequestContext(request, {'form': form,'bea':bea,'c':object_id,'total_kredit': sum([p.kredit for p in bea]),'total_debet': sum([p.kredit for p in bea])})
    return render_to_response('keuangan/tambah_biaya.html', variables)

#####penerimaan Pusat Bank
def jurnal_biaya_penambahan_saldo_pusat_bank(biaya, user):
	D = decimal.Decimal
        bm = PusatKasBankMapper.objects.get(item='1',ke_cabang = biaya.antar_gerai, cabang=user.profile.gerai)
        a_penambahan_saldo_debet = bm.coa
        a_penambahan_saldo_kredit = bm.coa_kredit
	jurnal = Jurnal.objects.create(
		diskripsi= 'Penerimaan Setoran dari %s melalui %s ' % (biaya.antar_gerai,biaya.js_trans),kode_cabang=biaya.gerai.kode_cabang,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_PENAMBAHAN_PUSAT_BANK"), id_coa = a_penambahan_saldo_debet,
		kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_cabang_tuju =biaya.antar_gerai.kode_cabang, id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_PENAMBAHAN_PUSAT_BANK"), id_coa = a_penambahan_saldo_kredit,
		debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju =biaya.antar_gerai.kode_cabang)

###Penambahan pusat Kas
#def jurnal_biaya_penambahan_saldo_pusat_jkt_kas(biaya, user):
def jurnal_biaya_penambahan_saldo_pusat_kas(biaya, user):
	D = decimal.Decimal
        bm = PusatKasBankMapper.objects.get(item='2', cabang=user.profile.gerai, ke_cabang = biaya.antar_gerai)
        a_penambahan_saldo_debet = bm.coa
        a_penambahan_saldo_kredit = bm.coa_kredit
	jurnal = Jurnal.objects.create(
		diskripsi= 'Penerimaan Setoran dari %s melalui %s ' % (biaya.antar_gerai,biaya.js_trans),kode_cabang=biaya.gerai.kode_cabang,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI"), id_coa = a_penambahan_saldo_debet,
		kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju =biaya.antar_gerai.kode_cabang )

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI"), id_coa = a_penambahan_saldo_kredit,
		debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju =biaya.antar_gerai.kode_cabang )
		
#####Pengeluaran Pusat Bank
def jurnal_biaya_pengembalian_saldo_pusat_bank_kecabang(biaya, user):
    D = decimal.Decimal
    a = PusatKasBankMapper.objects.filter(item='3',ke_cabang__kode_cabang=biaya.antar_gerai_kembali.kode_cabang)
    bm = a.get(ke_cabang__kode_cabang = biaya.antar_gerai_kembali.kode_cabang)
    a_rak_cabang =bm.debet_rak_cabang
    a_rak_pusat = bm.kredit_rak_pusat
    a_pengembalian_saldo_debet = bm.coa
    a_pengembalian_saldo_kredit = bm.coa_kredit

    a_pengembalian_saldo_debet_jakarta = bm.coa_lawan_debet
    a_pengembalian_saldo_kredit_jakarta = bm.coa_lawan_kredit
    jurnal = Jurnal.objects.create(diskripsi= 'Pengeluaran ke %s melalui %s ' % (biaya.antar_gerai_kembali,biaya.js_trans_kembali ),\
        kode_cabang=biaya.gerai.kode_cabang,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pengembalian_saldo)
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PENGELUARAN_PUSAT_BANK"), id_coa = a_pengembalian_saldo_debet,\
        kredit = 0,debet = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,\
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju =biaya.antar_gerai_kembali.kode_cabang)
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PENGELUARAN_PUSAT_BANK"), id_coa = a_pengembalian_saldo_kredit,
        debet = 0,kredit = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,\
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju =biaya.antar_gerai_kembali.kode_cabang )
    #####RAK
    jurnal = Jurnal.objects.create(diskripsi= 'Penerimaan Dari %s melalui %s ' % (biaya.gerai.nama_cabang,biaya.js_trans_kembali),
        kode_cabang=biaya.antar_gerai_kembali.kode_cabang,tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pengembalian_saldo)
    
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PENGELUARAN_BANK"), id_coa = a_pengembalian_saldo_debet_jakarta,
        kredit = 0,debet = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.antar_gerai_kembali.kode_cabang,id_unit= 300)#status_jurnal ='2',

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PENGELUARAN_BANK"), id_coa = a_pengembalian_saldo_kredit_jakarta,
        debet = 0,kredit = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.antar_gerai_kembali.kode_cabang,id_unit= 300)#status_jurnal ='2',

    ########RAK KONSOLIDASI
    #jurnal = Jurnal.objects.create(
        #diskripsi= 'Pengeluaran ke %s melalui %s ' % (biaya.antar_gerai_kembali ,biaya.js_trans_kembali ),kode_cabang =biaya.gerai.kode_cabang,
        #tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pengembalian_saldo)

    #jurnal.tbl_transaksi_set.create(
        #jenis = '%s' % ("GL_GL_RAK_PUSAT"), id_coa = a_rak_cabang,
        #kredit = 0,debet = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='2',tgl_trans =biaya.tanggal,
        #id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju =biaya.antar_gerai_kembali.kode_cabang )###untuk transaksi pusat

    #jurnal.tbl_transaksi_set.create(
        #jenis = '%s' % ("GL_GL_RAK_PUSAT"), id_coa = a_rak_pusat,
        #debet = 0,kredit = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='2',tgl_trans =biaya.tanggal,
        #id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju =biaya.antar_gerai_kembali.kode_cabang )###untuk transaksi pusat 
		
		
###Penambahan pusat Kas
def jurnal_biaya_pengembalian_saldo_pusat_kas_kecabang(biaya, user):
    D = decimal.Decimal
    bm = PusatKasBankMapper.objects.get(item='4',ke_cabang__kode_cabang=biaya.antar_gerai_kembali.kode_cabang)
    a_pengembalian_saldo_debet = bm.coa
    a_pengembalian_saldo_kredit = bm.coa_kredit
    a_rak_cabang =bm.debet_rak_cabang
    a_rak_pusat = bm.kredit_rak_pusat
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengeluaran ke %s melalui %s ' % (biaya.antar_gerai_kembali ,biaya.js_trans_kembali ),kode_cabang =biaya.gerai.kode_cabang,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pengembalian_saldo)

    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("GL_GL_PENGELUARAN_PUSAT_KAS_GERAI"), id_coa = a_pengembalian_saldo_debet,
        kredit = 0,debet = D(biaya.pengembalian_saldo),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju =biaya.antar_gerai_kembali.kode_cabang )
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGELUARAN_PUSAT_KAS_GERAI"), id_coa = a_pengembalian_saldo_kredit,
        debet = 0,kredit = D(biaya.pengembalian_saldo),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju =biaya.antar_gerai_kembali.kode_cabang )

    ########RAK PUSAT
    #jurnal = Jurnal.objects.create(
        #diskripsi= 'Pengeluaran ke %s melalui %s ' % (biaya.antar_gerai_kembali ,biaya.js_trans_kembali ),kode_cabang =biaya.gerai.kode_cabang,
        #tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pengembalian_saldo)

    #jurnal.tbl_transaksi_set.create(
        #jenis = '%s' % ("GL_GL_RAK_PUSAT"), id_coa = a_rak_cabang,
        #kredit = 0,debet = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='2',tgl_trans =biaya.tanggal,
        #id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju =biaya.antar_gerai_kembali.kode_cabang )###untuk transaksi pusat

    #jurnal.tbl_transaksi_set.create(
        #jenis = '%s' % ("GL_GL_RAK_PUSAT"), id_coa = a_rak_pusat,
        #debet = 0,kredit = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='2',tgl_trans =biaya.tanggal,
        #id_cabang =biaya.gerai.kode_cabang,id_unit= 300,id_cabang_tuju =biaya.antar_gerai_kembali.kode_cabang )###untuk transaksi pusat 
