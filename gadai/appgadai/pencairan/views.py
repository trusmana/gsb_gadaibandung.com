from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext    
from django.shortcuts import render_to_response, get_object_or_404
from gadai.appgadai.models import *
from django import forms
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os, string
from django.conf import settings
from gadai.appgadai.templatetags.terbilang import terbilang
from gadai.appgadai.templatetags.number_format import number_format
from gadai.appgadai.pencairan.forms import *
import datetime
import decimal
import csv
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from io import BytesIO
from django.contrib.auth.decorators import login_required, user_passes_test
from dateutil.relativedelta import *

import httplib, urllib
import json
from django.core.serializers.json import DjangoJSONEncoder

from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm
D = decimal.Decimal
#import locale
#locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

def parameter_produk(request):
    user = request.user
    if request.is_ajax():
        jenis = request.GET.get('jenis')
        jenis_barang = request.GET.get('jenis_barang')
        pm = ParameterProduk.objects.filter(jenis =jenis,jenis_barang =jenis_barang,jenis_kredit=user.profile.gerai.kode_unit).filter(aktif='1')
        run = HttpResponse(json.dumps({'jenis': jenis, 'biayasimpan': float(pm[0].biayasimpan),'denda': float(pm[0].denda), \
            'jw': float(pm[0].jw),'adm': float(pm[0].adm),'materai': float(pm[0].materai),'pembagi': float(pm[0].pembagi),'jenis_barang':jenis_barang,\
            'jasa': float(pm[0].jasa)}), content_type="application/json")
        return run

def parameter_laptop(request):
    user = request.user
    if request.is_ajax():
        jenis_transaksi = request.GET.get('jenis_transaksi')
        jenis_barang = request.GET.get('jenis_barang')
        pm = ParameterProduk.objects.filter(jenis_transaksi =jenis_transaksi,jenis_barang = jenis_barang,jenis_kredit=user.profile.gerai.kode_unit).filter(aktif='1')
        run = HttpResponse(json.dumps({'jenis_transaksi': jenis_transaksi, 'biayasimpan': float(pm[0].biayasimpan),'denda': float(pm[0].denda), \
            'jw': float(pm[0].jw),'adm': float(pm[0].adm),'materai': float(pm[0].materai),'pembagi': float(pm[0].pembagi),'jenis_barang':jenis_barang,\
            'jasa': float(pm[0].jasa)}), content_type="application/json")
        return run

def produk(request):
    forms = ParameterForm()
    if 'submit' in request.GET:
        jenis=request.GET['jenis']
        jenis_barang=request.GET['jenis_barang']
        try:
            if jenis == '5' and  jenis_barang == '1':
                return HttpResponseRedirect("/pencairan/add_hp_1bulan/%s/%s/" % (jenis,jenis_barang ))
            elif jenis == '5' and  jenis_barang == '2':
                return HttpResponseRedirect("/pencairan/add_laptop_1bulan/%s/%s/" % (jenis,jenis_barang ))
            elif jenis == '5' and  jenis_barang == '3':
                return HttpResponseRedirect("/pencairan/add_kamera_1bulan/%s/%s/" % (jenis,jenis_barang ))
            elif jenis == '7' and  jenis_barang == '6':
                return HttpResponseRedirect("/pencairan/add_motor_3bulan/%s/%s/" % (jenis,jenis_barang ))
            else:
                 return HttpResponseRedirect("/pencairan/produk/" % akad.id)   
        except:
            messages.add_message(request, messages.INFO,'PARAMETER YANG ANDA PILIH TIDAK ADA')
            return HttpResponseRedirect("/pencairan/produk/")
    else:
        template = 'pencairan/produk.html'
        variable = RequestContext(request, {'produk':produk,'forms':forms})
        return render_to_response(template,variable) 

def add_motor_3bulan(request,jenis,jenis_barang):
    user = request.user
    D = decimal.Decimal
    j = jenis
    b = jenis_barang
    jenis_transaksi = '1'
    if request.method == "POST":
        form = AGForm(request.POST,request.FILES)
        if form.is_valid():
            jenis_keanggotaan = form.cleaned_data['jenis_keanggotaan']
            jenis = form.cleaned_data['jenis']
            nama = form.cleaned_data['nama']
            tgl_lahir = form.cleaned_data['tgl_lahir']
            tempat = form.cleaned_data['tempat']
            no_ktp = form.cleaned_data['no_ktp']
            alamat_ktp = form.cleaned_data['alamat_ktp']
            rt_ktp= form.cleaned_data['rt_ktp']
            rw_ktp= form.cleaned_data['rw_ktp']
            telepon_ktp = form.cleaned_data['telepon_ktp']
            hp_ktp =form.cleaned_data['hp_ktp']
            kelurahan_ktp = form.cleaned_data['kelurahan_ktp']
            kecamatan_ktp = form.cleaned_data['kecamatan_ktp']
            kotamadya_ktp = form.cleaned_data['kotamadya_ktp']
            kabupaten_ktp = form.cleaned_data['kabupaten_ktp']
            no_rumah_ktp = form.cleaned_data['no_rumah_ktp']
            
            alamat_domisili = form.cleaned_data['alamat_domisili']
            rt_domisili= form.cleaned_data['rt_domisili']
            rw_domisili= form.cleaned_data['rw_domisili']
            telepon_domisili = form.cleaned_data['telepon_domisili']
            hp_domisili =form.cleaned_data['hp_domisili']
            kelurahan_domisili = form.cleaned_data['kelurahan_domisili']
            kecamatan_domisili = form.cleaned_data['kecamatan_domisili']
            kotamadya_domisili = form.cleaned_data['kotamadya_domisili']
            kabupaten_domisili = form.cleaned_data['kabupaten_domisili']
            no_rumah_domisili = form.cleaned_data['no_rumah_domisili']
            
            jenis_pekerjaan = form.cleaned_data['jenis_pekerjaan']
            alamat_kantor = form.cleaned_data['alamat_kantor']
            kode_pos = form.cleaned_data['kode_pos']
            telepon_kantor =form.cleaned_data['telepon_kantor']
            email= form.cleaned_data['email']
            jenis_kelamin= form.cleaned_data['jenis_kelamin']

            jenis_barang = form.cleaned_data['jenis_barang']            
            #merk = form.cleaned_data['merk']
            #type = form.cleaned_data['type']
            sn= form.cleaned_data['sn']
            warna = form.cleaned_data['warna']
            tahun_pembuatan =form.cleaned_data['tahun_pembuatan']
            bulan_produksi = form.cleaned_data['bulan_produksi']
            lampiran_dokumen = form.cleaned_data['lampiran_dokumen']            
            accesoris_barang1 = form.cleaned_data['accesoris_barang1']

            jangka_waktu_kendaraan = form.cleaned_data['jangka_waktu_kendaraan'] 
            jenis_kendaraan = form.cleaned_data['jenis_kendaraan']
            merk_kendaraan = form.cleaned_data['merk_kendaraan']
            type_kendaraan = form.cleaned_data['type_kendaraan']
            no_polisi = form.cleaned_data['no_polisi']
            no_rangka = form.cleaned_data['no_rangka']
            no_mesin = form.cleaned_data['no_mesin']
            warna_kendaraan = form.cleaned_data['warna_kendaraan']
            no_bpkb = form.cleaned_data['no_bpkb']
            stnk_atas_nama = form.cleaned_data['stnk_atas_nama']
            no_faktur = form.cleaned_data['no_faktur']
            
            tanggal = form.cleaned_data['tanggal']
            #gerai = form.cleaned_data['gerai']
            jangka_waktu = form.cleaned_data['jangka_waktu']
            nilai = form.cleaned_data['nilai']
            taksir = form.cleaned_data['taksir']
            bea_materai = form.cleaned_data['bea_materai']
            #jenis_transaksi = form.cleaned_data['jenis_transaksi']
            foto_nasabah = form.cleaned_data['foto_nasabah']
            tanda_tangan = form.cleaned_data['tanda_tangan']
            berkas_barang = form.cleaned_data['berkas_barang']
            #Data Pasangan
            nama_pasangan = form.cleaned_data['nama_pasangan']
            alamat_pasangan = form.cleaned_data['alamat_pasangan']
            jekel_pasangan = form.cleaned_data['jekel_pasangan']
            tlp_pasangan = form.cleaned_data['tlp_pasangan'] 
            no_rumah_pas = form.cleaned_data['no_rumah_pas']
            no_rt_pas = form.cleaned_data['no_rt_pas']
            no_rw_pas = form.cleaned_data['no_rw_pas']
            
            fungsi_sistem = form.cleaned_data['fungsi_sistem']
            charger = form.cleaned_data['charger']
            kondisi_charger = form.cleaned_data['kondisi_charger']   
            batre = form.cleaned_data['batre']
            kondisi_batre = form.cleaned_data['kondisi_batre']
            keybord = form.cleaned_data['keybord']
            kondisi_keybord = form.cleaned_data['kondisi_keybord']   
            cassing = form.cleaned_data['cassing']
            kondisi_cassing = form.cleaned_data['kondisi_cassing']   
            layar = form.cleaned_data['layar']
            kondisi_layar = form.cleaned_data['kondisi_layar']  
            lensa = form.cleaned_data['lensa']
            kondisi_lensa = form.cleaned_data['kondisi_lensa']
            batre_kamera = form.cleaned_data['batre_kamera']
            kondisi_batre_kamera = form.cleaned_data['kondisi_batre_kamera']
            cassing_kamera = form.cleaned_data['cassing_kamera']
            kondisi_cassing_kamera = form.cleaned_data['kondisi_cassing_kamera']
            password = form.cleaned_data['password']
            password_barang = form.cleaned_data['password_barang']

            optik_ps = form.cleaned_data['optik_ps']
            kondisi_optik_ps = form.cleaned_data['kondisi_optik_ps']
            layar_tv = form.cleaned_data['layar_tv']
            kondisi_layar_tv = form.cleaned_data['kondisi_layar_tv']
            
            harddisk  = form.cleaned_data['harddisk']
            kondisi_harddisk = form.cleaned_data['kondisi_harddisk']
            stick  = form.cleaned_data['stick']
            kondisi_stick = form.cleaned_data['kondisi_stick']
            hdmi  = form.cleaned_data['hdmi']
            kondisi_hdmi = form.cleaned_data['kondisi_hdmi']
            remote = form.cleaned_data['remote']
            kondisi_remote = form.cleaned_data['kondisi_remote']
            dus = form.cleaned_data['dus']
            tas = form.cleaned_data['tas']
            jasa_baru = form.cleaned_data['jasa_baru']
            beasimpan_baru = form.cleaned_data['beasimpan_baru']
            adm_baru = form.cleaned_data['adm_baru']
            total_all = form.cleaned_data['total_all']

            nilai_jasa = form.cleaned_data['nilai_jasa']
            nilai_biayasimpan = form.cleaned_data['nilai_biayasimpan']
            nilai_adm = form.cleaned_data['nilai_adm']
            nilai_materai = form.cleaned_data['nilai_materai']
            nilai_pembagi = form.cleaned_data['nilai_materai']
                
            agnasabah = Nasabah(nama=nama,tgl_lahir=tgl_lahir,tempat=tempat,no_ktp=no_ktp,alamat_ktp=alamat_ktp,jenis_keanggotaan = jenis_keanggotaan,
                rt_ktp=rt_ktp,rw_ktp=rw_ktp,telepon_ktp=telepon_ktp,hp_ktp=hp_ktp,kelurahan_ktp=kelurahan_ktp,\
                jenis_pekerjaan=jenis_pekerjaan,alamat_kantor=alamat_kantor,
                kode_pos=kode_pos,telepon_kantor=telepon_kantor,email=email,jenis_kelamin=jenis_kelamin,\
                kotamadya_ktp=kotamadya_ktp,no_rumah_ktp=no_rumah_ktp,
                kabupaten_ktp=kabupaten_ktp,kecamatan_ktp=kecamatan_ktp,alamat_domisili = alamat_ktp,rt_domisili= rt_domisili,\
                rw_domisili= rw_domisili,telepon_domisili = telepon_domisili,kelurahan_domisili = kelurahan_domisili,\
                kecamatan_domisili = kecamatan_domisili,
                kotamadya_domisili = kotamadya_domisili,kabupaten_domisili = kabupaten_domisili,no_rumah_domisili=no_rumah_domisili,
                nama_pasangan = nama_pasangan,alamat_pasangan = alamat_pasangan,jekel_pasangan = jekel_pasangan,tlp_pasangan = tlp_pasangan,
                no_rumah_pas = no_rumah_pas, no_rt_pas = no_rt_pas, no_rw_pas = no_rw_pas)
            agnasabah.save()
            barang = Barang(sn=sn,warna=warna,tahun_pembuatan=tahun_pembuatan,bulan_produksi=bulan_produksi,fungsi_sistem=fungsi_sistem,
                lampiran_dokumen=lampiran_dokumen,accesoris_barang1=accesoris_barang1,jenis_barang='1',
                merk_kendaraan=merk_kendaraan,no_polisi=no_polisi,no_rangka=no_rangka,no_mesin=no_mesin,warna_kendaraan=warna_kendaraan,
                no_bpkb=no_bpkb,stnk_atas_nama=stnk_atas_nama,no_faktur=no_faktur,jenis_kendaraan=0,
                type_kendaraan=type_kendaraan,\
                charger=charger,kondisi_charger=kondisi_charger,batre=batre,kondisi_batre=kondisi_batre,keybord=keybord,
                kondisi_keybord=kondisi_keybord,cassing=cassing,kondisi_cassing = kondisi_cassing,layar=layar,
                kondisi_layar=kondisi_layar,lensa=lensa,kondisi_lensa=kondisi_lensa,optik_ps=optik_ps,kondisi_optik_ps=kondisi_optik_ps,
                
                layar_tv=layar_tv,kondisi_layar_tv = kondisi_layar_tv,
                harddisk = harddisk,kondisi_harddisk = kondisi_harddisk,stick  = stick,kondisi_stick = kondisi_stick,hdmi  = hdmi,kondisi_hdmi = kondisi_hdmi,
                remote = remote,kondisi_remote = kondisi_remote,dus = dus,tas = tas,
                batre_kamera = batre_kamera,kondisi_batre_kamera = kondisi_batre_kamera,cassing_kamera = cassing_kamera,
                kondisi_cassing_kamera = kondisi_cassing_kamera,password = password,password_barang =password_barang)
            barang.save()
            
            ag = AkadGadai (tanggal = tanggal,agnasabah=agnasabah,gerai=user.profile.gerai,jangka_waktu=0,bea_materai=bea_materai,status_kw = '0',
                nilai=nilai,cu=request.user, mu=request.user,taksir=taksir,barang=barang,jangka_waktu_kendaraan=jangka_waktu,
                jenis_transaksi='2',status_transaksi=3,selisih_pelunasan = 0,jasa_lunas=0,denda_lunas=0,jenis=jenis,
                jasa_kendaraan_lunas=0,denda_kendaraan_lunas=0,terlambat=0,terlambat_kendaraan=0,nilai_lunas=0)
            print ag.jenis_transaksi
            


            if  ag.jenis_transaksi == u'1' and ag.nilai > ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'1':
                D = decimal.Decimal
                non = ParameterProduk.objects.get(jenis_kredit = user.profile.gerai.kode_unit, jenis= produk, jenis_transaksi =ag.jenis_transaksi)
                a_jasa = non.jasa
                a_denda = non.denda
                a_pdp_denda_terlambat = non.denda_terlambat
                a_pdp_adm = non.adm
                a_pdp_provisi = non.provisi
                a_pdp_asuransi = non.asuransi
                a_pdp_biayasimpan =non.biayasimpan
                a_pdp_materai =non.materai

                ag.p_jasa = a_jasa
                ag.p_denda = a_denda
                ag.p_denda_terlambat = a_pdp_denda_terlambat
                ag.p_adm = a_pdp_adm
                ag.p_provisi = a_pdp_provisi 
                ag.p.asuransi = a_pdp_asuransi
                ag.p_biayasimpan = a_pdp_biayasimpan 

                ag.status_taksir = 2
                ag.asumsi_jasa = round(ag.asumsi_pendapatan_jasa())
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm =  ag.p_adm#D(ag.adm)
                ag.nilai_jasa = D(round(ag.jasa))
                ag.nilai_biayasimpan = D(ag.biayasimpan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan(ag, request.user)
                
            elif ag.jenis_transaksi == u'2' and ag.nilai > ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'1':
                ag.status_taksir = 2
                ag.asumsi_jasa = round(ag.asumsi_pendapatan_jasa())
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm_kendaraan = D(ag.adm_kendaraan)
                ag.nilai_jasa_kendaraan = D(round(ag.jasa_kendaraan))
                ag.nilai_beasimpan_kendaraan = D(ag.beasimpan_kendaraan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan(ag, request.user)
                
            elif ag.jenis_transaksi == u'1' and ag.nilai <=  ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'1':
                ag.status_taksir = 1
                ag.asumsi_jasa = ag.asumsi_pendapatan_jasa()
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm = D(ag.adm)
                ag.nilai_jasa = D(round(ag.jasa))
                ag.nilai_biayasimpan = D(ag.biayasimpan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir 1')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan(ag, request.user)
                
            elif ag.jenis_transaksi == u'2' and ag.nilai <= ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'1':
                ag.status_taksir = 1
                ag.asumsi_jasa = round(ag.asumsi_pendapatan_jasa())
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm_kendaraan = D(ag.adm_kendaraan)
                ag.nilai_jasa_kendaraan = D(round(ag.jasa_kendaraan))
                ag.nilai_beasimpan_kendaraan = D(ag.beasimpan_kendaraan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan(ag, request.user)

            elif  ag.jenis_transaksi == u'1' and ag.nilai > ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'2':
                ag.status_taksir = 2
                ag.asumsi_jasa = round(ag.asumsi_pendapatan_jasa())
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm = D(ag.adm)
                ag.nilai_jasa = D(round(ag.jasa))
                ag.nilai_biayasimpan = D(ag.biayasimpan)
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan_nonanggota(ag, request.user)
                
            elif ag.jenis_transaksi == u'2' and ag.nilai > ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'2':
                ag.status_taksir = 2
                ag.asumsi_jasa = round(ag.asumsi_pendapatan_jasa())
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm_kendaraan = D(ag.adm_kendaraan)
                ag.nilai_jasa_kendaraan = D(round(ag.jasa_kendaraan))
                ag.nilai_beasimpan_kendaraan = D(ag.beasimpan_kendaraan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan_nonanggota(ag, request.user)
                
            elif ag.jenis_transaksi == u'1' and ag.nilai <=  ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'2':
                ag.status_taksir = 1
                ag.asumsi_jasa = round(ag.asumsi_pendapatan_jasa())
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm = D(ag.adm)
                ag.nilai_jasa = D(round(ag.jasa))
                ag.nilai_biayasimpan = D(ag.biayasimpan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir 2')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan_nonanggota(ag, request.user)
                
            #elif ag.jenis_transaksi == u'2' and ag.nilai <= ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'2':
            else:
                ag.status_taksir = 1
                ag.asumsi_jasa = ag.asumsi_pendapatan_jasa()
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm_kendaraan = D(ag.adm_kendaraan)
                ag.nilai_jasa_kendaraan = D(round(ag.jasa_kendaraan))
                ag.nilai_beasimpan_kendaraan = D(ag.beasimpan_kendaraan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan_nonanggota(ag, request.user)
                form  = AGForm()
                #form.fields['gerai'].queryset = Tbl_Cabang.objects.for_user(user)
            barang = Barang.objects.all()
            banding = barang.filter(id = ag.barang_id)
            banding.update(merk = ag.taksir.type,type = ag.taksir.type )       

            #params = '{"to":"%s", "msg":"%s"}' % (ag.agnasabah.hp_ktp,ag.sms())
            #headers = {"Content-Type": "application/json"}
            #conn = httplib.HTTPConnection("103.10.171.125")
            #conn.request("POST", "/api/sms/", params, headers)
            #response = conn.getresponse()
            #print "tes push sms dari pusat", response.status
            #print "tes push sms dari pusat", response.read()
            #print params
            messages.add_message(request, messages.INFO, 'Akadgadai Telah tersimpan')
            return HttpResponseRedirect('/')

    else:
        form  = AGForm()
        #form.fields['gerai'].queryset = Tbl_Cabang.objects.for_user(user) 
        form.fields['jenis'].initial = jenis
        form.fields['jenis_barang'].initial = jenis_barang 
        form.fields['jenis_transaksi'].initial = jenis_transaksi
    variables = RequestContext(request, {'form': form})
    return render_to_response('pencairan/parameter/motor_3minggu.html', variables)


def add_laptop_1bulan(request,jenis,jenis_barang):
    user = request.user
    D = decimal.Decimal
    j = jenis
    b = jenis_barang
    jenis_transaksi = '1'
    if request.method == "POST":
        form = AGForm(request.POST,request.FILES)
        if form.is_valid():
            jenis_keanggotaan = form.cleaned_data['jenis_keanggotaan']
            jenis = form.cleaned_data['jenis']
            nama = form.cleaned_data['nama']
            tgl_lahir = form.cleaned_data['tgl_lahir']
            tempat = form.cleaned_data['tempat']
            no_ktp = form.cleaned_data['no_ktp']
            alamat_ktp = form.cleaned_data['alamat_ktp']
            rt_ktp= form.cleaned_data['rt_ktp']
            rw_ktp= form.cleaned_data['rw_ktp']
            telepon_ktp = form.cleaned_data['telepon_ktp']
            hp_ktp =form.cleaned_data['hp_ktp']
            kelurahan_ktp = form.cleaned_data['kelurahan_ktp']
            kecamatan_ktp = form.cleaned_data['kecamatan_ktp']
            kotamadya_ktp = form.cleaned_data['kotamadya_ktp']
            kabupaten_ktp = form.cleaned_data['kabupaten_ktp']
            no_rumah_ktp = form.cleaned_data['no_rumah_ktp']
            
            alamat_domisili = form.cleaned_data['alamat_domisili']
            rt_domisili= form.cleaned_data['rt_domisili']
            rw_domisili= form.cleaned_data['rw_domisili']
            telepon_domisili = form.cleaned_data['telepon_domisili']
            hp_domisili =form.cleaned_data['hp_domisili']
            kelurahan_domisili = form.cleaned_data['kelurahan_domisili']
            kecamatan_domisili = form.cleaned_data['kecamatan_domisili']
            kotamadya_domisili = form.cleaned_data['kotamadya_domisili']
            kabupaten_domisili = form.cleaned_data['kabupaten_domisili']
            no_rumah_domisili = form.cleaned_data['no_rumah_domisili']
            
            jenis_pekerjaan = form.cleaned_data['jenis_pekerjaan']
            alamat_kantor = form.cleaned_data['alamat_kantor']
            kode_pos = form.cleaned_data['kode_pos']
            telepon_kantor =form.cleaned_data['telepon_kantor']
            email= form.cleaned_data['email']
            jenis_kelamin= form.cleaned_data['jenis_kelamin']

            jenis_barang = form.cleaned_data['jenis_barang']            
            #merk = form.cleaned_data['merk']
            #type = form.cleaned_data['type']
            sn= form.cleaned_data['sn']
            warna = form.cleaned_data['warna']
            tahun_pembuatan =form.cleaned_data['tahun_pembuatan']
            bulan_produksi = form.cleaned_data['bulan_produksi']
            lampiran_dokumen = form.cleaned_data['lampiran_dokumen']            
            accesoris_barang1 = form.cleaned_data['accesoris_barang1']

            jangka_waktu_kendaraan = form.cleaned_data['jangka_waktu_kendaraan'] 
            jenis_kendaraan = form.cleaned_data['jenis_kendaraan']
            merk_kendaraan = form.cleaned_data['merk_kendaraan']
            type_kendaraan = form.cleaned_data['type_kendaraan']
            no_polisi = form.cleaned_data['no_polisi']
            no_rangka = form.cleaned_data['no_rangka']
            no_mesin = form.cleaned_data['no_mesin']
            warna_kendaraan = form.cleaned_data['warna_kendaraan']
            no_bpkb = form.cleaned_data['no_bpkb']
            stnk_atas_nama = form.cleaned_data['stnk_atas_nama']
            no_faktur = form.cleaned_data['no_faktur']
            
            tanggal = form.cleaned_data['tanggal']
            #gerai = form.cleaned_data['gerai']
            jangka_waktu = form.cleaned_data['jangka_waktu']
            nilai = form.cleaned_data['nilai']
            taksir = form.cleaned_data['taksir']
            bea_materai = form.cleaned_data['bea_materai']
            #jenis_transaksi = form.cleaned_data['jenis_transaksi']
            foto_nasabah = form.cleaned_data['foto_nasabah']
            tanda_tangan = form.cleaned_data['tanda_tangan']
            berkas_barang = form.cleaned_data['berkas_barang']
            #Data Pasangan
            nama_pasangan = form.cleaned_data['nama_pasangan']
            alamat_pasangan = form.cleaned_data['alamat_pasangan']
            jekel_pasangan = form.cleaned_data['jekel_pasangan']
            tlp_pasangan = form.cleaned_data['tlp_pasangan'] 
            no_rumah_pas = form.cleaned_data['no_rumah_pas']
            no_rt_pas = form.cleaned_data['no_rt_pas']
            no_rw_pas = form.cleaned_data['no_rw_pas']
            
            fungsi_sistem = form.cleaned_data['fungsi_sistem']
            charger = form.cleaned_data['charger']
            kondisi_charger = form.cleaned_data['kondisi_charger']   
            batre = form.cleaned_data['batre']
            kondisi_batre = form.cleaned_data['kondisi_batre']
            keybord = form.cleaned_data['keybord']
            kondisi_keybord = form.cleaned_data['kondisi_keybord']   
            cassing = form.cleaned_data['cassing']
            kondisi_cassing = form.cleaned_data['kondisi_cassing']   
            layar = form.cleaned_data['layar']
            kondisi_layar = form.cleaned_data['kondisi_layar']  
            lensa = form.cleaned_data['lensa']
            kondisi_lensa = form.cleaned_data['kondisi_lensa']
            batre_kamera = form.cleaned_data['batre_kamera']
            kondisi_batre_kamera = form.cleaned_data['kondisi_batre_kamera']
            cassing_kamera = form.cleaned_data['cassing_kamera']
            kondisi_cassing_kamera = form.cleaned_data['kondisi_cassing_kamera']
            password = form.cleaned_data['password']
            password_barang = form.cleaned_data['password_barang']

            optik_ps = form.cleaned_data['optik_ps']
            kondisi_optik_ps = form.cleaned_data['kondisi_optik_ps']
            layar_tv = form.cleaned_data['layar_tv']
            kondisi_layar_tv = form.cleaned_data['kondisi_layar_tv']
            
            harddisk  = form.cleaned_data['harddisk']
            kondisi_harddisk = form.cleaned_data['kondisi_harddisk']
            stick  = form.cleaned_data['stick']
            kondisi_stick = form.cleaned_data['kondisi_stick']
            hdmi  = form.cleaned_data['hdmi']
            kondisi_hdmi = form.cleaned_data['kondisi_hdmi']
            remote = form.cleaned_data['remote']
            kondisi_remote = form.cleaned_data['kondisi_remote']
            dus = form.cleaned_data['dus']
            tas = form.cleaned_data['tas']
            jasa_baru = form.cleaned_data['jasa_baru']
            beasimpan_baru = form.cleaned_data['beasimpan_baru']
            adm_baru = form.cleaned_data['adm_baru']
            total_all = form.cleaned_data['total_all']

            nilai_jasa = form.cleaned_data['nilai_jasa']
            nilai_biayasimpan = form.cleaned_data['nilai_biayasimpan']
            nilai_adm = form.cleaned_data['nilai_adm']
            nilai_materai = form.cleaned_data['nilai_materai']
            nilai_pembagi = form.cleaned_data['nilai_materai']
                
            agnasabah = Nasabah(nama=nama,tgl_lahir=tgl_lahir,tempat=tempat,no_ktp=no_ktp,alamat_ktp=alamat_ktp,jenis_keanggotaan = jenis_keanggotaan,
                rt_ktp=rt_ktp,rw_ktp=rw_ktp,telepon_ktp=telepon_ktp,hp_ktp=hp_ktp,kelurahan_ktp=kelurahan_ktp,\
                jenis_pekerjaan=jenis_pekerjaan,alamat_kantor=alamat_kantor,
                kode_pos=kode_pos,telepon_kantor=telepon_kantor,email=email,jenis_kelamin=jenis_kelamin,\
                kotamadya_ktp=kotamadya_ktp,no_rumah_ktp=no_rumah_ktp,
                kabupaten_ktp=kabupaten_ktp,kecamatan_ktp=kecamatan_ktp,alamat_domisili = alamat_ktp,rt_domisili= rt_domisili,\
                rw_domisili= rw_domisili,telepon_domisili = telepon_domisili,kelurahan_domisili = kelurahan_domisili,\
                kecamatan_domisili = kecamatan_domisili,
                kotamadya_domisili = kotamadya_domisili,kabupaten_domisili = kabupaten_domisili,no_rumah_domisili=no_rumah_domisili,
                nama_pasangan = nama_pasangan,alamat_pasangan = alamat_pasangan,jekel_pasangan = jekel_pasangan,tlp_pasangan = tlp_pasangan,
                no_rumah_pas = no_rumah_pas, no_rt_pas = no_rt_pas, no_rw_pas = no_rw_pas)
            agnasabah.save()
            barang = Barang(sn=sn,warna=warna,tahun_pembuatan=tahun_pembuatan,bulan_produksi=bulan_produksi,fungsi_sistem=fungsi_sistem,
                lampiran_dokumen=lampiran_dokumen,accesoris_barang1=accesoris_barang1,jenis_barang='1',
                merk_kendaraan=merk_kendaraan,no_polisi=no_polisi,no_rangka=no_rangka,no_mesin=no_mesin,warna_kendaraan=warna_kendaraan,
                no_bpkb=no_bpkb,stnk_atas_nama=stnk_atas_nama,no_faktur=no_faktur,jenis_kendaraan=0,
                type_kendaraan=type_kendaraan,\
                charger=charger,kondisi_charger=kondisi_charger,batre=batre,kondisi_batre=kondisi_batre,keybord=keybord,
                kondisi_keybord=kondisi_keybord,cassing=cassing,kondisi_cassing = kondisi_cassing,layar=layar,
                kondisi_layar=kondisi_layar,lensa=lensa,kondisi_lensa=kondisi_lensa,optik_ps=optik_ps,kondisi_optik_ps=kondisi_optik_ps,
                
                layar_tv=layar_tv,kondisi_layar_tv = kondisi_layar_tv,
                harddisk = harddisk,kondisi_harddisk = kondisi_harddisk,stick  = stick,kondisi_stick = kondisi_stick,hdmi  = hdmi,kondisi_hdmi = kondisi_hdmi,
                remote = remote,kondisi_remote = kondisi_remote,dus = dus,tas = tas,
                batre_kamera = batre_kamera,kondisi_batre_kamera = kondisi_batre_kamera,cassing_kamera = cassing_kamera,
                kondisi_cassing_kamera = kondisi_cassing_kamera,password = password,password_barang =password_barang)
            barang.save()
            
            ag = AkadGadai (tanggal = tanggal,agnasabah=agnasabah, gerai=user.profile.gerai, jangka_waktu=jangka_waktu,bea_materai=bea_materai,status_kw = '0',
                nilai=nilai,cu=request.user, mu=request.user,taksir=taksir,barang=barang,jangka_waktu_kendaraan=jangka_waktu_kendaraan,
                jenis_transaksi='1',status_transaksi=3,selisih_pelunasan = 0,jasa_lunas=0,denda_lunas=0,jenis=jenis,
                jasa_kendaraan_lunas=0,denda_kendaraan_lunas=0,terlambat=0,terlambat_kendaraan=0,nilai_lunas=0)
            print ag.jenis_transaksi
            


            if  ag.jenis_transaksi == u'1' and ag.nilai > ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'1':
                D = decimal.Decimal
                non = ParameterProduk.objects.get(jenis_kredit = user.profile.gerai.kode_unit, jenis= produk, jenis_transaksi =ag.jenis_transaksi)
                a_jasa = non.jasa
                a_denda = non.denda
                a_pdp_denda_terlambat = non.denda_terlambat
                a_pdp_adm = non.adm
                a_pdp_provisi = non.provisi
                a_pdp_asuransi = non.asuransi
                a_pdp_biayasimpan =non.biayasimpan
                a_pdp_materai =non.materai

                ag.p_jasa = a_jasa
                ag.p_denda = a_denda
                ag.p_denda_terlambat = a_pdp_denda_terlambat
                ag.p_adm = a_pdp_adm
                ag.p_provisi = a_pdp_provisi 
                ag.p.asuransi = a_pdp_asuransi
                ag.p_biayasimpan = a_pdp_biayasimpan 

                ag.status_taksir = 2
                ag.asumsi_jasa = round(ag.asumsi_pendapatan_jasa())
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm =  ag.p_adm#D(ag.adm)
                ag.nilai_jasa = D(round(ag.jasa))
                ag.nilai_biayasimpan = D(ag.biayasimpan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan(ag, request.user)
                
            elif ag.jenis_transaksi == u'2' and ag.nilai > ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'1':
                ag.status_taksir = 2
                ag.asumsi_jasa = round(ag.asumsi_pendapatan_jasa())
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm_kendaraan = D(ag.adm_kendaraan)
                ag.nilai_jasa_kendaraan = D(round(ag.jasa_kendaraan))
                ag.nilai_beasimpan_kendaraan = D(ag.beasimpan_kendaraan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan(ag, request.user)
                
            elif ag.jenis_transaksi == u'1' and ag.nilai <=  ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'1':
                ag.status_taksir = 1
                ag.asumsi_jasa = ag.asumsi_pendapatan_jasa()
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm = D(ag.adm)
                ag.nilai_jasa = D(round(ag.jasa))
                ag.nilai_biayasimpan = D(ag.biayasimpan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir 1')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan(ag, request.user)
                
            elif ag.jenis_transaksi == u'2' and ag.nilai <= ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'1':
                ag.status_taksir = 1
                ag.asumsi_jasa = round(ag.asumsi_pendapatan_jasa())
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm_kendaraan = D(ag.adm_kendaraan)
                ag.nilai_jasa_kendaraan = D(round(ag.jasa_kendaraan))
                ag.nilai_beasimpan_kendaraan = D(ag.beasimpan_kendaraan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan(ag, request.user)

            elif  ag.jenis_transaksi == u'1' and ag.nilai > ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'2':
                ag.status_taksir = 2
                ag.asumsi_jasa = round(ag.asumsi_pendapatan_jasa())
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm = D(ag.adm)
                ag.nilai_jasa = D(round(ag.jasa))
                ag.nilai_biayasimpan = D(ag.biayasimpan)
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan_nonanggota(ag, request.user)
                
            elif ag.jenis_transaksi == u'2' and ag.nilai > ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'2':
                ag.status_taksir = 2
                ag.asumsi_jasa = round(ag.asumsi_pendapatan_jasa())
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm_kendaraan = D(ag.adm_kendaraan)
                ag.nilai_jasa_kendaraan = D(round(ag.jasa_kendaraan))
                ag.nilai_beasimpan_kendaraan = D(ag.beasimpan_kendaraan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan_nonanggota(ag, request.user)
                
            elif ag.jenis_transaksi == u'1' and ag.nilai <=  ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'2':
                ag.status_taksir = 1
                ag.asumsi_jasa = round(ag.asumsi_pendapatan_jasa())
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm = D(ag.adm)
                ag.nilai_jasa = D(round(ag.jasa))
                ag.nilai_biayasimpan = D(ag.biayasimpan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir 2')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan_nonanggota(ag, request.user)
                
            #elif ag.jenis_transaksi == u'2' and ag.nilai <= ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'2':
            else:
                ag.status_taksir = 1
                ag.asumsi_jasa = ag.asumsi_pendapatan_jasa()
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm_kendaraan = D(ag.adm_kendaraan)
                ag.nilai_jasa_kendaraan = D(round(ag.jasa_kendaraan))
                ag.nilai_beasimpan_kendaraan = D(ag.beasimpan_kendaraan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan_nonanggota(ag, request.user)
                form  = AGForm()
                #form.fields['gerai'].queryset = Tbl_Cabang.objects.for_user(user)
            barang = Barang.objects.all()
            banding = barang.filter(id = ag.barang_id)
            banding.update(merk = ag.taksir.type,type = ag.taksir.type )       

            #params = '{"to":"%s", "msg":"%s"}' % (ag.agnasabah.hp_ktp,ag.sms())
            #headers = {"Content-Type": "application/json"}
            #conn = httplib.HTTPConnection("103.10.171.125")
            #conn.request("POST", "/api/sms/", params, headers)
            #response = conn.getresponse()
            #print "tes push sms dari pusat", response.status
            #print "tes push sms dari pusat", response.read()
            #print params
            messages.add_message(request, messages.INFO, 'Akadgadai Telah tersimpan')
            return HttpResponseRedirect('/')

    else:
        form  = AGForm()
        #form.fields['gerai'].queryset = Tbl_Cabang.objects.for_user(user) 
        form.fields['jenis'].initial = jenis
        form.fields['jenis_barang'].initial = jenis_barang 
        form.fields['jenis_transaksi'].initial = jenis_transaksi
    variables = RequestContext(request, {'form': form})
    return render_to_response('pencairan/parameter/laptop_4minggu.html', variables)

def add_hp_1bulan(request,jenis,jenis_barang):
    user = request.user
    D = decimal.Decimal
    j = jenis
    b = jenis_barang
    jenis_transaksi = '1'
    forms = AGForm(initial={'jenis_barang': b,'jenis_transaksi':j})
    if request.method == "POST":
        form = AGForm(request.POST,request.FILES)
        if form.is_valid():
            jenis = form.cleaned_data['jenis']
            jenis_keanggotaan = form.cleaned_data['jenis_keanggotaan']
            nama = form.cleaned_data['nama']
            tgl_lahir = form.cleaned_data['tgl_lahir']
            tempat = form.cleaned_data['tempat']
            no_ktp = form.cleaned_data['no_ktp']
            alamat_ktp = form.cleaned_data['alamat_ktp']
            rt_ktp= form.cleaned_data['rt_ktp']
            rw_ktp= form.cleaned_data['rw_ktp']
            telepon_ktp = form.cleaned_data['telepon_ktp']
            hp_ktp =form.cleaned_data['hp_ktp']
            kelurahan_ktp = form.cleaned_data['kelurahan_ktp']
            kecamatan_ktp = form.cleaned_data['kecamatan_ktp']
            kotamadya_ktp = form.cleaned_data['kotamadya_ktp']
            kabupaten_ktp = form.cleaned_data['kabupaten_ktp']
            no_rumah_ktp = form.cleaned_data['no_rumah_ktp']
            
            alamat_domisili = form.cleaned_data['alamat_domisili']
            rt_domisili= form.cleaned_data['rt_domisili']
            rw_domisili= form.cleaned_data['rw_domisili']
            telepon_domisili = form.cleaned_data['telepon_domisili']
            hp_domisili =form.cleaned_data['hp_domisili']
            kelurahan_domisili = form.cleaned_data['kelurahan_domisili']
            kecamatan_domisili = form.cleaned_data['kecamatan_domisili']
            kotamadya_domisili = form.cleaned_data['kotamadya_domisili']
            kabupaten_domisili = form.cleaned_data['kabupaten_domisili']
            no_rumah_domisili = form.cleaned_data['no_rumah_domisili']
            
            jenis_pekerjaan = form.cleaned_data['jenis_pekerjaan']
            alamat_kantor = form.cleaned_data['alamat_kantor']
            kode_pos = form.cleaned_data['kode_pos']
            telepon_kantor =form.cleaned_data['telepon_kantor']
            email= form.cleaned_data['email']
            jenis_kelamin= form.cleaned_data['jenis_kelamin']

            jenis_barang = form.cleaned_data['jenis_barang']            
            #merk = form.cleaned_data['merk']
            #type = form.cleaned_data['type']
            sn= form.cleaned_data['sn']
            warna = form.cleaned_data['warna']
            tahun_pembuatan =form.cleaned_data['tahun_pembuatan']
            bulan_produksi = form.cleaned_data['bulan_produksi']
            lampiran_dokumen = form.cleaned_data['lampiran_dokumen']            
            accesoris_barang1 = form.cleaned_data['accesoris_barang1']

            jangka_waktu_kendaraan = form.cleaned_data['jangka_waktu_kendaraan'] 
            jenis_kendaraan = form.cleaned_data['jenis_kendaraan']
            merk_kendaraan = form.cleaned_data['merk_kendaraan']
            type_kendaraan = form.cleaned_data['type_kendaraan']
            no_polisi = form.cleaned_data['no_polisi']
            no_rangka = form.cleaned_data['no_rangka']
            no_mesin = form.cleaned_data['no_mesin']
            warna_kendaraan = form.cleaned_data['warna_kendaraan']
            no_bpkb = form.cleaned_data['no_bpkb']
            stnk_atas_nama = form.cleaned_data['stnk_atas_nama']
            no_faktur = form.cleaned_data['no_faktur']
            
            tanggal = form.cleaned_data['tanggal']
            #gerai = form.cleaned_data['gerai']
            jangka_waktu = form.cleaned_data['jangka_waktu']
            nilai = form.cleaned_data['nilai']
            taksir = form.cleaned_data['taksir']
            bea_materai = form.cleaned_data['bea_materai']
            jenis_transaksi = form.cleaned_data['jenis_transaksi']
            foto_nasabah = form.cleaned_data['foto_nasabah']
            tanda_tangan = form.cleaned_data['tanda_tangan']
            berkas_barang = form.cleaned_data['berkas_barang']
            #Data Pasangan
            nama_pasangan = form.cleaned_data['nama_pasangan']
            alamat_pasangan = form.cleaned_data['alamat_pasangan']
            jekel_pasangan = form.cleaned_data['jekel_pasangan']
            tlp_pasangan = form.cleaned_data['tlp_pasangan'] 
            no_rumah_pas = form.cleaned_data['no_rumah_pas']
            no_rt_pas = form.cleaned_data['no_rt_pas']
            no_rw_pas = form.cleaned_data['no_rw_pas']
            
            fungsi_sistem = form.cleaned_data['fungsi_sistem']
            charger = form.cleaned_data['charger']
            kondisi_charger = form.cleaned_data['kondisi_charger']   
            batre = form.cleaned_data['batre']
            kondisi_batre = form.cleaned_data['kondisi_batre']
            keybord = form.cleaned_data['keybord']
            kondisi_keybord = form.cleaned_data['kondisi_keybord']   
            cassing = form.cleaned_data['cassing']
            kondisi_cassing = form.cleaned_data['kondisi_cassing']   
            layar = form.cleaned_data['layar']
            kondisi_layar = form.cleaned_data['kondisi_layar']  
            lensa = form.cleaned_data['lensa']
            kondisi_lensa = form.cleaned_data['kondisi_lensa']
            batre_kamera = form.cleaned_data['batre_kamera']
            kondisi_batre_kamera = form.cleaned_data['kondisi_batre_kamera']
            cassing_kamera = form.cleaned_data['cassing_kamera']
            kondisi_cassing_kamera = form.cleaned_data['kondisi_cassing_kamera']
            password = form.cleaned_data['password']
            password_barang = form.cleaned_data['password_barang']

            optik_ps = form.cleaned_data['optik_ps']
            kondisi_optik_ps = form.cleaned_data['kondisi_optik_ps']
            layar_tv = form.cleaned_data['layar_tv']
            kondisi_layar_tv = form.cleaned_data['kondisi_layar_tv']
            
            harddisk  = form.cleaned_data['harddisk']
            kondisi_harddisk = form.cleaned_data['kondisi_harddisk']
            stick  = form.cleaned_data['stick']
            kondisi_stick = form.cleaned_data['kondisi_stick']
            hdmi  = form.cleaned_data['hdmi']
            kondisi_hdmi = form.cleaned_data['kondisi_hdmi']
            remote = form.cleaned_data['remote']
            kondisi_remote = form.cleaned_data['kondisi_remote']
            dus = form.cleaned_data['dus']
            tas = form.cleaned_data['tas']
            jasa_baru = form.cleaned_data['jasa_baru']
            beasimpan_baru = form.cleaned_data['beasimpan_baru']
            adm_baru = form.cleaned_data['adm_baru']
            total_all = form.cleaned_data['total_all']

            nilai_jasa = form.cleaned_data['nilai_jasa']
            nilai_biayasimpan = form.cleaned_data['nilai_biayasimpan']
            nilai_adm = form.cleaned_data['nilai_adm']
            nilai_materai = form.cleaned_data['nilai_materai']
            nilai_pembagi = form.cleaned_data['nilai_materai']
                
            agnasabah = Nasabah(nama=nama,tgl_lahir=tgl_lahir,tempat=tempat,no_ktp=no_ktp,alamat_ktp=alamat_ktp,jenis_keanggotaan = jenis_keanggotaan,
                rt_ktp=rt_ktp,rw_ktp=rw_ktp,telepon_ktp=telepon_ktp,hp_ktp=hp_ktp,kelurahan_ktp=kelurahan_ktp,\
                jenis_pekerjaan=jenis_pekerjaan,alamat_kantor=alamat_kantor,
                kode_pos=kode_pos,telepon_kantor=telepon_kantor,email=email,jenis_kelamin=jenis_kelamin,\
                kotamadya_ktp=kotamadya_ktp,no_rumah_ktp=no_rumah_ktp,
                kabupaten_ktp=kabupaten_ktp,kecamatan_ktp=kecamatan_ktp,alamat_domisili = alamat_ktp,rt_domisili= rt_domisili,\
                rw_domisili= rw_domisili,telepon_domisili = telepon_domisili,kelurahan_domisili = kelurahan_domisili,\
                kecamatan_domisili = kecamatan_domisili,
                kotamadya_domisili = kotamadya_domisili,kabupaten_domisili = kabupaten_domisili,no_rumah_domisili=no_rumah_domisili,
                nama_pasangan = nama_pasangan,alamat_pasangan = alamat_pasangan,jekel_pasangan = jekel_pasangan,tlp_pasangan = tlp_pasangan,
                no_rumah_pas = no_rumah_pas, no_rt_pas = no_rt_pas, no_rw_pas = no_rw_pas)
            agnasabah.save()
            barang = Barang(sn=sn,warna=warna,tahun_pembuatan=tahun_pembuatan,bulan_produksi=bulan_produksi,fungsi_sistem=fungsi_sistem,
                lampiran_dokumen=lampiran_dokumen,accesoris_barang1=accesoris_barang1,jenis_barang='1',
                merk_kendaraan=merk_kendaraan,no_polisi=no_polisi,no_rangka=no_rangka,no_mesin=no_mesin,warna_kendaraan=warna_kendaraan,
                no_bpkb=no_bpkb,stnk_atas_nama=stnk_atas_nama,no_faktur=no_faktur,jenis_kendaraan=0,
                type_kendaraan=type_kendaraan,\
                charger=charger,kondisi_charger=kondisi_charger,batre=batre,kondisi_batre=kondisi_batre,keybord=keybord,
                kondisi_keybord=kondisi_keybord,cassing=cassing,kondisi_cassing = kondisi_cassing,layar=layar,
                kondisi_layar=kondisi_layar,lensa=lensa,kondisi_lensa=kondisi_lensa,optik_ps=optik_ps,kondisi_optik_ps=kondisi_optik_ps,
                
                layar_tv=layar_tv,kondisi_layar_tv = kondisi_layar_tv,
                harddisk = harddisk,kondisi_harddisk = kondisi_harddisk,stick  = stick,kondisi_stick = kondisi_stick,hdmi  = hdmi,kondisi_hdmi = kondisi_hdmi,
                remote = remote,kondisi_remote = kondisi_remote,dus = dus,tas = tas,
                batre_kamera = batre_kamera,kondisi_batre_kamera = kondisi_batre_kamera,cassing_kamera = cassing_kamera,
                kondisi_cassing_kamera = kondisi_cassing_kamera,password = password,password_barang =password_barang)
            barang.save()
            
            ag = AkadGadai (tanggal = tanggal,agnasabah=agnasabah, gerai=user.profile.gerai, jangka_waktu=jangka_waktu,bea_materai=bea_materai,status_kw = '0',
                nilai=nilai,cu=request.user, mu=request.user,taksir=taksir,barang=barang,jangka_waktu_kendaraan=jangka_waktu_kendaraan,
                jenis_transaksi='1',status_transaksi=3,selisih_pelunasan = 0,jasa_lunas=0,denda_lunas=0,jenis =jenis,
                jasa_kendaraan_lunas=0,denda_kendaraan_lunas=0,terlambat=0,terlambat_kendaraan=0,nilai_lunas=0)
            print ag.jenis_transaksi
            


            if  ag.jenis_transaksi == u'1' and ag.nilai > ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'1':
                D = decimal.Decimal
                non = ParameterProduk.objects.get(jenis_kredit = user.profile.gerai.kode_unit, jenis= produk, jenis_transaksi =ag.jenis_transaksi)
                a_jasa = non.jasa
                a_denda = non.denda
                a_pdp_denda_terlambat = non.denda_terlambat
                a_pdp_adm = non.adm
                a_pdp_provisi = non.provisi
                a_pdp_asuransi = non.asuransi
                a_pdp_biayasimpan =non.biayasimpan
                a_pdp_materai =non.materai

                ag.p_jasa = a_jasa
                ag.p_denda = a_denda
                ag.p_denda_terlambat = a_pdp_denda_terlambat
                ag.p_adm = a_pdp_adm
                ag.p_provisi = a_pdp_provisi 
                ag.p.asuransi = a_pdp_asuransi
                ag.p_biayasimpan = a_pdp_biayasimpan 

                ag.status_taksir = 2
                ag.asumsi_jasa = round(ag.asumsi_pendapatan_jasa())
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm =  ag.p_adm#D(ag.adm)
                ag.nilai_jasa = D(round(ag.jasa))
                ag.nilai_biayasimpan = D(ag.biayasimpan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan(ag, request.user)
                
            elif ag.jenis_transaksi == u'2' and ag.nilai > ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'1':
                ag.status_taksir = 2
                ag.asumsi_jasa = round(ag.asumsi_pendapatan_jasa())
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm_kendaraan = D(ag.adm_kendaraan)
                ag.nilai_jasa_kendaraan = D(round(ag.jasa_kendaraan))
                ag.nilai_beasimpan_kendaraan = D(ag.beasimpan_kendaraan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan(ag, request.user)
                
            elif ag.jenis_transaksi == u'1' and ag.nilai <=  ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'1':
                ag.status_taksir = 1
                ag.asumsi_jasa = ag.asumsi_pendapatan_jasa()
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm = D(ag.adm)
                ag.nilai_jasa = D(round(ag.jasa))
                ag.nilai_biayasimpan = D(ag.biayasimpan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir 1')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan(ag, request.user)
                
            elif ag.jenis_transaksi == u'2' and ag.nilai <= ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'1':
                ag.status_taksir = 1
                ag.asumsi_jasa = round(ag.asumsi_pendapatan_jasa())
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm_kendaraan = D(ag.adm_kendaraan)
                ag.nilai_jasa_kendaraan = D(round(ag.jasa_kendaraan))
                ag.nilai_beasimpan_kendaraan = D(ag.beasimpan_kendaraan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan(ag, request.user)

            elif  ag.jenis_transaksi == u'1' and ag.nilai > ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'2':
                ag.status_taksir = 2
                ag.asumsi_jasa = round(ag.asumsi_pendapatan_jasa())
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm = D(ag.adm)
                ag.nilai_jasa = D(round(ag.jasa))
                ag.nilai_biayasimpan = D(ag.biayasimpan)
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan_nonanggota(ag, request.user)
                
            elif ag.jenis_transaksi == u'2' and ag.nilai > ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'2':
                ag.status_taksir = 2
                ag.asumsi_jasa = round(ag.asumsi_pendapatan_jasa())
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm_kendaraan = D(ag.adm_kendaraan)
                ag.nilai_jasa_kendaraan = D(round(ag.jasa_kendaraan))
                ag.nilai_beasimpan_kendaraan = D(ag.beasimpan_kendaraan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan_nonanggota(ag, request.user)
                
            elif ag.jenis_transaksi == u'1' and ag.nilai <=  ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'2':
                ag.status_taksir = 1
                ag.asumsi_jasa = round(ag.asumsi_pendapatan_jasa())
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm = D(ag.adm)
                ag.nilai_jasa = D(round(ag.jasa))
                ag.nilai_biayasimpan = D(ag.biayasimpan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir 2')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan_nonanggota(ag, request.user)
                
            #elif ag.jenis_transaksi == u'2' and ag.nilai <= ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'2':
            else:
                ag.status_taksir = 1
                ag.asumsi_jasa = ag.asumsi_pendapatan_jasa()
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm_kendaraan = D(ag.adm_kendaraan)
                ag.nilai_jasa_kendaraan = D(round(ag.jasa_kendaraan))
                ag.nilai_beasimpan_kendaraan = D(ag.beasimpan_kendaraan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                ag.save()
                request.FILES['tanda_tangan'].name = nama + '_' +  ag.norek() + '_' + request.FILES['tanda_tangan'].name
                request.FILES['foto_nasabah'].name = nama + '_' +  ag.norek() + '_' + request.FILES['foto_nasabah'].name
                request.FILES['berkas_barang'].name = nama + '_' +  ag.norek() + '_' + request.FILES['berkas_barang'].name
                berkas = BerkasGadai(upload=ag, tanda_tangan=request.FILES['tanda_tangan'], foto_nasabah=request.FILES['foto_nasabah'] ,\
                    berkas_barang=request.FILES['berkas_barang'])
                berkas.save()
                #jurnal_pencairan_nonanggota(ag, request.user)
                form  = AGForm()
                #form.fields['gerai'].queryset = Tbl_Cabang.objects.for_user(user)
            barang = Barang.objects.all()
            banding = barang.filter(id = ag.barang_id)
            banding.update(merk = ag.taksir.type,type = ag.taksir.type )       

            #params = '{"to":"%s", "msg":"%s"}' % (ag.agnasabah.hp_ktp,ag.sms())
            #headers = {"Content-Type": "application/json"}
            #conn = httplib.HTTPConnection("103.10.171.125")
            #conn.request("POST", "/api/sms/", params, headers)
            #response = conn.getresponse()
            #print "tes push sms dari pusat", response.status
            #print "tes push sms dari pusat", response.read()
            #print params
            messages.add_message(request, messages.INFO, 'Akadgadai Telah tersimpan')
            return HttpResponseRedirect('/')

    else:
        form  = AGForm()
        #form.fields['gerai'].queryset = Tbl_Cabang.objects.for_user(user) 
        form.fields['jenis'].initial = jenis 
        form.fields['jenis_barang'].initial = jenis_barang
        form.fields['jenis_transaksi'].initial = jenis_transaksi 
    variables = RequestContext(request, {'form': form,'j':j,'b':b,'forms':forms})
    return render_to_response('pencairan/parameter/elektronik_4minggu.html', variables)

