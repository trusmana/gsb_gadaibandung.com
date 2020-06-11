from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404,render
from gadai.appgadai.models import *
from django import forms
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os, string
from django.conf import settings
from gadai.appgadai.templatetags.terbilang import terbilang
from gadai.appgadai.templatetags.number_format import number_format
from gadai.appgadai.akadgadai.forms import *
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
## Untuk QR Code
#from reportlab.graphics.shapes import Drawing 
#from reportlab.graphics.barcode.qr import QrCodeWidget 
#from reportlab.graphics import renderPDF


#import locale
#locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
def kw_sbg_gu(request, object_id):
    pk = AkadGadai.objects.get(id=object_id)
    pk.status_kw = '1'
    pk.save()
    #tiga_play = [p,p,p]
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % pk.norek()
    c = canvas.Canvas(response, pagesize=(9.5*inch, 13*inch))
    c.setTitle("kwitansi %s" % pk.norek())
    atas = 1
    sekarang=datetime.datetime.now()
    h=sekarang.day
    m=sekarang.month
    y=sekarang.year
    jumlah = pk.nilai_gu + pk.denda_gu + pk.jasa_gu
    if m+1 <= 12:
        b=m+1
        t=y
    else  :
        b=1
        t=y+1
        patokan=datetime.date(int(t),int(b),int(h))
        trk=pk.tanggal
        dd=patokan.month-trk.month
        yy=patokan.year-trk.year


    header1=(4.25 *inch, (5.3 + 5.5) * inch)
    colom1 = (0.5*inch, (4.3 + 5.5) *inch)
            #ke kiri  ke atas ke bawah
    colom2 = (6.7*inch, (4.5 + 5.5) *inch)
    colom3 = (6.0*inch, (4.8 + 4.5) *inch)
    colom4 = (0.5*inch, (3.7 + 4.5) *inch)

    header2=(8.25 *inch, (2.75 + 2.5) * inch)    
    header3=(4.25 *inch, (2.8 + 2.65) * inch)        
    #header2=(4.25 *inch, (5.3 + 5.5) * inch)
    colom5 = (0.5*inch, (2.15 + 2.3) *inch)
            #ke kiri  ke atas ke bawah
    colom6 = (6.7*inch, (2.15 + 2.3) *inch)
    colom7 = (6.0*inch, (2.25 + 1.5) *inch)
    colom8 = (0.5*inch, (1.5 + 1.1) *inch)
    tb=terbilang(pk.terima_bersih_all())
    ###KOTAK LOGO
    c.setFillColorRGB(255,255,255)
    c.rect(0.2*inch,12.3*inch,9*inch,0.6*inch, fill=1)
    ###Tanggal Transaksi
    c.rect(7.4*inch,11.3*inch,1.8*inch,0.6*inch, fill=1)
    ###KOTAK SURAT BUKTI GADAI
    c.setFillColorRGB(245, 229, 27,1)
    c.rect(0.2*inch,11.9*inch,3*inch,0.4*inch, fill=1)
    ###KOTAK NO BUKTI
    c.rect(3*inch,11.9*inch,6.2*inch,0.4*inch, fill=1)
    ###KOTAK Tanggal JATUH TEMPO
    c.rect(7.4*inch,11.9*inch,1.8*inch,0.4*inch, fill=1)

    ###KOTAK INFO PERHATIAN
    c.rect(7.4*inch,10.18*inch,1.8*inch,1.22*inch, fill=1)
    ##Kotak TTD NASABAH
    c.rect(7.4*inch,8.9*inch,1.8*inch,2.0*inch, fill=1)

    ##KOTAK KETERANGAN BARANG JAMINAN
    c.rect(0.2*inch,7.2*inch,7.2*inch,4.5*inch, fill=1)
    c.rect(3.8*inch,7.7*inch,3.6*inch,4.1*inch, fill=1)
    ###KOTAK ISIAN NAMA 
    c.rect(0.2*inch,10.9*inch,7.2*inch,1.0*inch, fill=1)
    ##Kotak TTD Petugas
    c.rect(3.8*inch,7.2*inch,5.4*inch,1.7*inch, fill=1)
    ##Kotak Setuju2
    c.rect(3.8*inch,8.7*inch,5.4*inch,0.2*inch, fill=1)
    c.setFillColorRGB(0,0,0)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/gaban_gsb.png'), 0.3*inch, (6.9 + 5.5) * inch, width=78/17.5*0.51*inch,height=15/17.5*0.51*inch,mask=None)
    x,y = colom1
    y1 = 0.10 * inch
    y -=1*y1
    c.setFont("Courier",9)
    c.drawString(190, 905, "OUTLET/GERAI :")
    c.setFont("Courier-Bold", 12)
    c.drawString(270, 910, "%s"% (pk.gerai.nama_cabang))
    c.setFont("Courier-Bold", 9)
    c.drawString(270, 900, "%s/Telp: 0%s "% (pk.gerai.alamat, pk.gerai.no_telp))

    c.setFont("Courier", 7)
    barcode = code128.Code128("%s" % (pk.norek()))
    barcode.drawOn(c, 185*mm, 304.5*mm)
    c.setFont("Courier-Bold", 9) 
    c.drawString(540, 848, "Tanggal Transaksi") 
    c.drawString(540, 825, "%s" % (pk.tanggal.strftime('%d %b %Y')))
    c.drawString(540, 810, "Tanggal Jatuh Tempo") 
    c.drawString(540, 790, "%s" % (pk.jatuhtempo.strftime('%d %b %Y')))
   
    c.setFont("Courier-Bold", 12)  
    c.drawString(19, 868, "SURAT BUKTI GADAI ULANG")
    c.setFont("Courier-Bold", 14)  
    c.drawString(220, 868, "NO NASABAH: %s"% (pk.nonas()))
    c.setFont("Courier", 9)
    c.drawString(20, 848, "Nomor Rek")
    c.drawString(100, 848, ": %s" % (pk.norek()))
    c.drawString(20, 838, "Nama")
    c.drawString(100, 838, ": %s" % (pk.agnasabah.nama))
    c.drawString(20, 828, "No Identitas")
    c.drawString(100, 828, ": %s" % (pk.agnasabah.no_ktp))
    c.drawString(20, 818, "No Telepon")
    c.drawString(100, 818, ": %s" % (pk.agnasabah.telepon_domisili,))
    c.drawString(20, 808, "Alamat")
    c.drawString(100, 808, ": %s No %s" %(pk.agnasabah.alamat_domisili,pk.agnasabah.no_rumah_domisili))
    c.drawString(100.5, 798, "  RT/RW %s/%s %s" %(pk.agnasabah.rt_domisili,pk.agnasabah.rw_domisili,pk.agnasabah.kelurahan_domisili,))
    c.drawString(20, 788, "Tempat,Tgl Lhr")
    c.drawString(100, 788, ": %s, %s" %(pk.agnasabah.tempat,pk.agnasabah.tgl_lahir.strftime('%d %B %Y')))
    c.setFont("Courier-Bold", 9)
    c.drawString(570, 775, "Perhatian")
    c.setFont("Courier", 6)
    c.drawString(540, 753, "1. Apabila sampai dengan tanggal")
    c.drawString(540, 747, "   jatuh  tempo  tidak melakukan")
    c.drawString(540, 741, "   Pelunasan  atau  tidak  gadai")
    c.drawString(540, 735, "   ulang maka PT. GSB berhak men")
    c.drawString(540, 729, "   jual barang jaminan  yang ter")
    c.drawString(540, 723, "   tera di Surat Bukti Gadai ini.") 
    c.drawString(540, 717, "2. Apabila akan melakukan  gadai") 
    c.drawString(540, 711, "   ulang  harap menginformasikan") 
    c.drawString(540, 705, "   1  hari sebelum  jatuh  tempo")
    c.drawString(540, 699, "3. Setiap melakukan pelunasan at") 
    c.drawString(540, 693, "   au gadai  ulang, kwitansi ini") 
    c.drawString(540, 687, "   harus   diperlihatkan  kepada") 
    c.drawString(540, 681, "   petugas gerai.")
    c.drawString(540, 675, "4. Pelunasan atau gadai ulang ha")
    c.drawString(540, 669, "   rus dilakukan tepat waktu ses")
    c.drawString(540, 663, "   uai tanggal jatuh tempo.")
    c.drawString(540, 657, "5. Kwitansi ini sah apabila telah ")
    c.drawString(540, 651, "   divalidasi ditanda tangan dan ")
    c.drawString(540, 645, "   di stempel.")
    c.setFont("Courier", 8)
    c.drawString(278, 632, "Setuju atas isi perjanjian Gadai yang tertera di belakang Surat Bukti Gadai ini")
    c.drawString(285, 620, "Nasabah")
    c.drawString(285, 525, "%s" %(pk.agnasabah.nama))
    c.drawString(535, 620, "Kuasa Pemutus Jaminan")
    c.drawString(535, 525, "%s" %(pk.gerai.nama_kg))
    c.setFont("Courier", 9)

    c.drawString(20, 775, "KETERANGAN NILAI PINJAMAN:")
    c.setFont("Courier-Bold", 9)
    c.drawString(20, 755,"Pinjaman lama")
    c.drawString(120,755,":Rp.")
    c.drawRightString(235,755,"%s"% (number_format(pk.nilai_gu)))
    c.setFont("Courier", 9)
    c.drawString(20, 745, "Denda")
    c.drawString(120,745, ":Rp.")
    c.drawRightString(235,745, "%s"% (number_format(pk.denda_gu)))
    c.drawString(20, 735, "Jasa Terlambat")
    c.drawString(120, 735,":Rp.")
    c.drawRightString(235, 735, "%s"% (number_format(pk.jasa_gu)))
    c.setLineWidth(.3)
    c.line(120, 733, 235, 733)
    c.drawString(20, 723, "T. Biaya Plns")
    c.drawString(120, 723, ":Rp.")
    c.drawRightString(235, 723, "%s"%(number_format(jumlah)))
    c.setLineWidth(.3)
    c.line(120, 721, 235, 721)
    c.line(120, 719, 235, 719)
    c.setFont("Courier-Bold", 9)
    c.drawString(20, 696,"Pinjaman Baru")
    c.drawString(120, 696,":Rp.")
    c.drawRightString(235, 696,"%s"% (number_format(pk.nilai)))
    c.setFont("Courier", 9)
    c.drawString(20, 686, "Bea Simpan/Survey")
    c.drawString(120, 686,":Rp.")
    c.drawRightString(235, 686, "%s"% (number_format(pk.beasimpan_all())))
    c.drawString(20, 676, "Bea Administrasi")
    c.drawString(120, 676,":Rp.")
    c.drawRightString(235, 676, "%s"% (number_format(pk.adm_all())))
    c.drawString(20, 666, "Jasa")
    c.drawString(120, 666,":Rp.")
    c.drawRightString(235, 666, "%s"% (number_format(pk.jasa_kwitansi())))
    c.drawString(20, 656, "Bea Materai")
    c.drawString(120, 656,":Rp.")
    c.drawRightString(235, 656, "%s"% (number_format(pk.bea_materai)))
    c.setLineWidth(.3)
    c.line(120, 654, 235, 654)
    c.drawString(20, 644, "Total Biaya 1")
    c.drawString(120, 644, ":Rp.")
    c.drawRightString(235, 644, "%s"%(number_format(pk.jumlah_biaya_pk())))
    c.setLineWidth(.3)
    c.line(120, 642, 235, 642)
    c.drawString(20, 632, "Nilai diterima")
    c.drawString(120, 632, ":Rp.")
    c.drawRightString(235, 632, "%s"%(number_format(pk.terima_bersih_all())))
    c.setLineWidth(.3)
    c.line(120, 630, 235, 630)
    c.line(120, 628, 235, 628)
    c.setFont("Courier-Bold", 9)
    c.drawString(20, 618, "Plns Pinj Lama")
    c.drawString(120, 618, ":Rp.")
    c.drawRightString(235, 618, "%s"%(number_format(pk.total_plns_gu)))
    c.setLineWidth(.3)
    c.setFont("Courier", 9)
    c.line(120, 616, 235, 616)
    c.line(120, 614, 235, 614)
    c.line(120, 612, 235, 612)
    tbk=terbilang(pk.total_plns_gu)
    c.drawString(20, 602, "Terbilang") 
    c.drawString(90, 602, ":" ) 
    c.drawString(30, 592, "%s" % (tbk.title()[0:37]))
    c.drawString(30, 582, "%s Rupiah" % (tbk.title()[37:90]))


    c.setFont("Courier", 9)
    c.drawString(280, 775, "KETERANGAN BARANG JAMINAN:")
    c.drawString(280, 765, "1. %s"% (pk.taksiran_kwitansi()[0:43] ))
    c.drawString(280, 755, "%s"% (pk.taksiran_kwitansi()[43:89] ))
    c.drawString(280, 745, "%s "% (pk.taksiran_kwitansi()[89:134] ))
    c.drawString(280, 735, "%s "% (pk.taksiran_kwitansi()[134:] ))

    if pk.barang.jenis_barang == u'1': ###('1','HP')
        c.drawString(280, 725, "Kelengkapan :") 
        c.drawString(280, 715, "1.Charger")
        c.drawString(335, 715, "%s "% (pk.barang.get_kondisi_charger_display()))  #CHARGER
        c.drawString(280, 705, "2.Baterai")
        c.drawString(335, 705, "%s "% (pk.barang.get_kondisi_batre_display()))  #BATRE
        c.drawString(280, 695, "3.Keypad")
        c.drawString(335, 695, "%s "% (pk.barang.get_kondisi_keybord_display()))   #KEYPAD
        c.drawString(280, 685, "4.Cassing")
        c.drawString(335, 685, "%s "% (pk.barang.get_kondisi_cassing_display())) #CASSING

        c.drawString(400, 715, "5.Layar")
        c.drawString(460, 715, "%s "% (pk.barang.get_kondisi_layar_display())) #LAYAR
        c.drawString(400, 705, "6.Password")
        c.drawString(460, 705, "%s "% (pk.barang.password_barang ))  #PASSWORD
        c.drawString(400, 695, "7.Dus")
        c.drawString(460, 695, "%s "% (pk.barang.get_dus_display())) #DUS
        c.drawString(400, 685, "8.Tas")
        c.drawString(460, 685, "%s "% (pk.barang.get_tas_display()))#TAS

    elif pk.barang.jenis_barang == u'2':###('2','LAPTOP/NB'),
        c.drawString(280, 725, "Kelengkapan :") 
        c.drawString(280, 715, "1.Charger")
        c.drawString(335, 715, "%s "% (pk.barang.get_kondisi_charger_display()))  #CHARGER
        c.drawString(280, 705, "2.Baterai")
        c.drawString(335, 705, "%s "% (pk.barang.get_kondisi_batre_display()))  #BATRE
        c.drawString(280, 695, "3.Keypad")
        c.drawString(335, 695, "%s "% (pk.barang.get_kondisi_keybord_display()))   #KEYPAD
        c.drawString(280, 685, "4.Cassing")
        c.drawString(335, 685, "%s "% (pk.barang.get_kondisi_cassing_display())) #CASSING

        c.drawString(400, 715, "5.Layar")
        c.drawString(460, 715, "%s "% (pk.barang.get_kondisi_layar_display())) #LAYAR
        c.drawString(400, 705, "6.Password")
        c.drawString(460, 705, "%s "% (pk.barang.password_barang ))  #PASSWORD
        c.drawString(400, 695, "7.Dus")
        c.drawString(460, 695, "%s "% (pk.barang.get_dus_display())) #DUS
        c.drawString(400, 685, "8.Tas")
        c.drawString(460, 685, "%s "% (pk.barang.get_tas_display()))#TAS

    elif pk.barang.jenis_barang == u'3':###('3','KAMERA'),
        c.drawString(280, 725, "Kelengkapan :")
        c.drawString(280, 715, "1.Lensa")
        c.drawString(335, 715, "%s "% (pk.barang.get_lensa_display()))
        c.drawString(280, 705, "2.Baterai")
        c.drawString(335, 705, "%s "% (pk.barang.get_batre_kamera_display()))
        c.drawString(280, 695, "3.Cassing")
        c.drawString(335, 695, "%s "% (pk.barang.get_cassing_kamera_display()))
        c.drawString(280, 685, "4.Dus")
        c.drawString(335, 685, "%s "% (pk.barang.get_dus_display()))

        c.drawString(420, 715, "5.Tas")
        c.drawString(460, 715, "%s "% (pk.barang.get_tas_display()))

    elif pk.barang.jenis_barang == u'4':###('4','PS'),
        c.drawString(280, 725, "Kelengkapan :")
        c.drawString(280, 715, "1.Optik")
        c.drawString(335, 715, "%s "% (pk.barang.get_kondisi_optik_ps_display()))
        c.drawString(280, 705, "2.Stick")
        c.drawString(335, 705, "%s "% (pk.barang.get_kondisi_stick_display()))
        c.drawString(280, 695, "3.HDMI")
        c.drawString(335, 695, "%s "% (pk.barang.get_kondisi_hdmi_display())) 
        c.drawString(280, 685, "4.Harddisk")
        c.drawString(335, 685, "%s "% (pk.barang.get_kondisi_harddisk_display()))

        c.drawString(420, 715, "5.Dus")
        c.drawString(460, 715, "%s "% (pk.barang.get_dus_display()))
        c.drawString(420, 705, "6.Tas")
        c.drawString(460, 705, "%s "% (pk.barang.get_tas_display()))

    elif pk.barang.jenis_barang == u'5':###('5','TV LCD'),
        c.drawString(280, 725, "Kelengkapan :")
        c.drawString(280, 715, "1.Layar")
        c.drawString(335, 715, "%s "% (pk.barang.get_kondisi_layar_tv_display()))
        c.drawString(280, 705, "2.Remote")
        c.drawString(335, 705, "%s "% (pk.barang.get_kondisi_remote_display()))
        c.drawString(280, 695, "3.Dus")
        c.drawString(335, 695, "%s "% (pk.barang.get_dus_display()))
        c.drawString(280, 685, "4.Tas")
        c.drawString(335, 685, "%s "% (pk.barang.get_tas_display()))

    elif pk.barang.jenis_kendaraan == u'1':###('6','MOTOR'),
        c.drawString(280, 725, "Kelengkapan :")
        c.drawString(280, 715, "1.Bpkb")
        c.drawString(390, 715, "%s "% (pk.barang.get_bpkb_display()))
        c.drawString(280, 705, "2.Stnk")
        c.drawString(390, 705, "%s "% (pk.barang.get_stnk_display()))
        c.drawString(280, 695, "3.Faktur")
        c.drawString(390, 695, "%s "% (pk.barang.get_faktur_display()))
        c.drawString(280, 685, "4.Gesek No Mesin")
        c.drawString(390, 685, "%s "% (pk.barang.get_gesek_nomesin_display()))
        c.drawString(280, 675, "5.Gesek No Rangka")
        c.drawString(390, 675, "%s "% (pk.barang.get_gesek_norangka_display()))

    elif pk.barang.jenis_kendaraan == u'2':###('7','Mobil'),
        c.drawString(280, 725, "Kelengkapan :")
        c.drawString(280, 715, "1.Bpkb")
        c.drawString(390, 715, "%s "% (pk.barang.get_bpkb_display()))
        c.drawString(280, 705, "2.Stnk")
        c.drawString(390, 705, "%s "% (pk.barang.get_stnk_display()))
        c.drawString(280, 695, "3.Faktur")
        c.drawString(390, 695, "%s "% (pk.barang.get_faktur_display()))
        c.drawString(280, 685, "4.Gesek No Mesin")
        c.drawString(390, 685, "%s "% (pk.barang.get_gesek_nomesin_display()))
        c.drawString(280, 675, "5.Gesek No Rangka")
        c.drawString(390, 675, "%s "% (pk.barang.get_gesek_norangka_display()))
    c.setFont("Courier", 6)
    c.drawString(20, 530, "SBG Sah dan mengikat setelah ditandatangani oleh Para Pihak" ) 
    c.drawString(0, 490, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" )

    ###KE DUA
    ###KOTAK LOGO
    c.setFillColorRGB(255,255,255)
    c.rect(0.2*inch,5.8*inch,9*inch,0.6*inch, fill=1)
    ###Tanggal Transaksi
    c.rect(7.4*inch,4.8*inch,1.8*inch,0.6*inch, fill=1)
    ###KOTAK SURAT BUKTI GADAI
    c.setFillColorRGB(245, 229, 27,1)
    c.rect(0.2*inch,5.4*inch,3*inch,0.4*inch, fill=1)

    ###KOTAK NO BUKTI
    c.rect(3*inch,5.4*inch,6.2*inch,0.4*inch, fill=1)
    ###KOTAK Barcode
    c.rect(7.4*inch,5.4*inch,1.8*inch,0.4*inch, fill=1)
    ###KOTAK Tanggal JATUH TEMPO
    c.rect(7.4*inch,4.4*inch,1.8*inch,0.4*inch, fill=1)
    ##Kotak INFO PERHATIAN
    c.rect(7.4*inch,2.4*inch,1.8*inch,2.0*inch, fill=1)

    ##KOTAK KETERANGAN BARANG JAMINAN
    c.rect(0.2*inch,0.7*inch,7.2*inch,4.2*inch, fill=1)
    c.rect(3.8*inch,1.2*inch,3.6*inch,4.1*inch, fill=1)
    ###KOTAK ISIAN NAMA 
    c.rect(0.2*inch,4.4*inch,7.2*inch,1.0*inch, fill=1)
    ##Kotak TTD Petugas

    c.rect(3.8*inch,0.7*inch,5.4*inch,1.5*inch, fill=1)
    ##Kotak Setuju2
    c.rect(3.8*inch,2.2*inch,5.4*inch,0.2*inch, fill=1)
    c.setFillColorRGB(0,0,0)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/gaban_gsb.png'), 0.3*inch, (0.40 + 5.5) * inch, width=78/17.5*0.51*inch,height=15/17.5*0.51*inch,mask=None)
    x,y = colom1	
    y1 = 0.10 * inch
    y -=1*y1
    c.setFont("Courier",9)
    c.drawString(190, 437, "OUTLET/GERAI :")
    c.setFont("Courier-Bold", 12)
    c.drawString(270, 442, "%s"% (pk.gerai.nama_cabang))
    c.setFont("Courier-Bold", 9)
    c.drawString(270, 432, "%s/Telp: 0%s "% (pk.gerai.alamat, pk.gerai.no_telp))

    c.setFont("Courier", 7)
    barcode = code128.Code128("%s" % (pk.norek()))
    barcode.drawOn(c, 185*mm, 139.5*mm)
    c.setFont("Courier-Bold", 9) 
    c.drawString(540, 380, "Tanggal Transaksi") 
    c.drawString(540, 349, "%s" % (pk.tanggal.strftime('%d %b %Y')))
    c.drawString(540, 337, "Tanggal Jatuh Tempo") 
    c.drawString(540, 320, "%s" % (pk.jatuhtempo.strftime('%d %b %Y')))

    c.setFont("Courier-Bold", 12)  
    c.drawString(19, 400, "SURAT BUKTI GADAI ULANG")
    c.setFont("Courier-Bold", 14)  
    c.drawString(220, 400, "NO NASABAH: %s"% (pk.nonas()))
    c.setFont("Courier", 9)
    c.drawString(20, 379, "Nomor Rek")
    c.drawString(100, 379, ": %s" % (pk.norek()))
    c.drawString(20, 369, "Nama")
    c.drawString(100, 369, ": %s" % (pk.agnasabah.nama))
    c.drawString(20, 359, "No Identitas")
    c.drawString(100, 359, ": %s" % (pk.agnasabah.no_ktp))
    c.drawString(20, 349, "No Telepon")
    c.drawString(100, 349, ": %s" % (pk.agnasabah.telepon_domisili,))
    c.drawString(20, 339, "Alamat")
    c.drawString(100, 339, ": %s No %s" %(pk.agnasabah.alamat_domisili,pk.agnasabah.no_rumah_domisili))
    c.drawString(100.5, 329, "  RT/RW %s/%s %s" %(pk.agnasabah.rt_domisili,pk.agnasabah.rw_domisili,pk.agnasabah.kelurahan_domisili,))
    c.drawString(20, 319, "Tempat,Tgl Lhr")
    c.drawString(100, 319, ": %s, %s" %(pk.agnasabah.tempat,pk.agnasabah.tgl_lahir.strftime('%d %B %Y')))
    c.setFont("Courier-Bold", 9)

    c.drawString(570, 306, "Perhatian")
    c.setFont("Courier", 6)
    c.drawString(540, 284, "1. Apabila sampai dengan tanggal")
    c.drawString(540, 278, "   jatuh  tempo  tidak melakukan")
    c.drawString(540, 272, "   Pelunasan  atau  tidak  gadai")
    c.drawString(540, 266, "   ulang maka PT. GSB berhak men")
    c.drawString(540, 260, "   jual barang jaminan  yang ter")
    c.drawString(540, 254, "   tera di Surat Bukti Gadai ini.") 
    c.drawString(540, 248, "2. Apabila akan melakukan  gadai") 
    c.drawString(540, 242, "   ulang  harap menginformasikan") 
    c.drawString(540, 236, "   1  hari sebelum  jatuh  tempo")
    c.drawString(540, 230, "3. Setiap melakukan pelunasan at") 
    c.drawString(540, 224, "   au gadai  ulang, kwitansi ini") 
    c.drawString(540, 218, "   harus   diperlihatkan  kepada") 
    c.drawString(540, 212, "   petugas gerai.")
    c.drawString(540, 206, "4. Pelunasan atau gadai ulang ha")
    c.drawString(540, 200, "   rus dilakukan tepat waktu ses")
    c.drawString(540, 194, "   uai tanggal jatuh tempo.")
    c.drawString(540, 188, "5. Kwitansi ini sah apabila telah ")
    c.drawString(540, 182, "   divalidasi ditanda tangan dan ")
    c.drawString(540, 176, "   di stempel.")
    c.setFont("Courier", 8)
    c.drawString(278, 163, "Setuju atas isi perjanjian Gadai yang tertera di belakang Surat Bukti Gadai ini")
    c.drawString(285, 151, "Nasabah")
    c.drawString(285, 56, "%s" %(pk.agnasabah.nama))
    c.drawString(535, 151, "Kuasa Pemutus Jaminan")
    c.drawString(535, 56, "%s" %(pk.gerai.nama_kg))
    c.setFont("Courier", 9)

    c.drawString(20, 306, "KETERANGAN NILAI PINJAMAN:")
    c.setFont("Courier-Bold", 9)
    c.drawString(20, 286,"Pinjaman lama")
    c.drawString(120,286,":Rp.")
    c.drawRightString(235,286,"%s"% (number_format(pk.nilai_gu)))
    c.setFont("Courier", 9)
    c.drawString(20, 276, "Denda")
    c.drawString(120,276, ":Rp.")
    c.drawRightString(235,276, "%s"% (number_format(pk.denda_gu)))
    c.drawString(20, 266, "Jasa Terlambat")
    c.drawString(120, 266,":Rp.")
    c.drawRightString(235, 266, "%s"% (number_format(pk.jasa_gu)))
    c.setLineWidth(.3)
    c.line(120, 264, 235, 264)
    c.drawString(20, 256, "T. Biaya Plns")
    c.drawString(120, 256, ":Rp.")
    c.drawRightString(235, 256, "%s"%(number_format(jumlah)))
    c.setLineWidth(.3)
    c.line(120, 254, 235, 254)
    c.line(120, 252, 235, 252)
    c.setFont("Courier-Bold", 9)
    c.drawString(20, 232,"Pinjaman Baru")
    c.drawString(120, 232,":Rp.")
    c.drawRightString(235, 232,"%s"% (number_format(pk.nilai)))
    c.setFont("Courier", 9)
    c.drawString(20, 222, "Bea Simpan/Survey")
    c.drawString(120, 222,":Rp.")
    c.drawRightString(235, 222, "%s"% (number_format(pk.beasimpan_all())))
    c.drawString(20, 212, "Bea Administrasi")
    c.drawString(120, 212,":Rp.")
    c.drawRightString(235, 212, "%s"% (number_format(pk.adm_all())))
    c.drawString(20, 202, "Jasa")
    c.drawString(120, 202,":Rp.")
    c.drawRightString(235, 202, "%s"% (number_format(pk.jasa_kwitansi())))
    c.drawString(20, 192, "Bea Materai")
    c.drawString(120, 192,":Rp.")
    c.drawRightString(235, 192, "%s"% (number_format(pk.bea_materai)))
    c.setLineWidth(.3)
    c.line(120, 190, 235, 190)
    c.drawString(20, 180, "Total Biaya 1")
    c.drawString(120, 180, ":Rp.")
    c.drawRightString(235, 180, "%s"%(number_format(pk.jumlah_biaya_pk())))
    c.setLineWidth(.3)
    c.line(120, 178, 235, 178)
    c.drawString(20, 168, "Nilai diterima")
    c.drawString(120, 168, ":Rp.")
    c.drawRightString(235, 168, "%s"%(number_format(pk.terima_bersih_all())))
    c.setLineWidth(.3)
    c.line(120, 166, 235, 166)
    c.line(120, 164, 235, 164)
    c.setFont("Courier-Bold", 9)
    c.drawString(20, 154, "Plns Pinj Lama")
    c.drawString(120, 154, ":Rp.")
    c.drawRightString(235, 154, "%s"%(number_format(pk.total_plns_gu)))
    c.setLineWidth(.3)
    c.setFont("Courier", 9)
    c.line(120, 152, 235, 152)
    c.line(120, 150, 235, 150)
    c.line(120, 148, 235, 148)
    tbk=terbilang(pk.total_plns_gu)
    c.drawString(20, 138, "Terbilang") 
    c.drawString(90, 138, ":" ) 
    c.drawString(30, 128, "%s" % (tbk.title()[0:37]))
    c.drawString(30, 118, "%s Rupiah" % (tbk.title()[37:90]))

    c.setFont("Courier", 9)
    c.drawString(280, 306, "KETERANGAN BARANG JAMINAN:")
    c.drawString(280, 296, "1. %s"% (pk.taksiran_kwitansi()[0:43] ))
    c.drawString(280, 286, "%s"% (pk.taksiran_kwitansi()[43:89] ))
    c.drawString(280, 276, "%s "% (pk.taksiran_kwitansi()[89:134] ))
    c.drawString(280, 266, "%s "% (pk.taksiran_kwitansi()[134:] ))

    if pk.barang.jenis_barang == u'1': ###('1','HP')
        c.drawString(280, 256, "Kelengkapan :") 
        c.drawString(280, 246, "1.Charger")
        c.drawString(335, 246, "%s "% (pk.barang.get_kondisi_charger_display()))  #CHARGER
        c.drawString(280, 236, "2.Baterai")
        c.drawString(335, 236, "%s "% (pk.barang.get_kondisi_batre_display()))  #BATRE
        c.drawString(280, 226, "3.Keypad")
        c.drawString(335, 226, "%s "% (pk.barang.get_kondisi_keybord_display()))   #KEYPAD
        c.drawString(280, 216, "4.Cassing")
        c.drawString(335, 216, "%s "% (pk.barang.get_kondisi_cassing_display())) #CASSING

        c.drawString(400, 246, "5.Layar")
        c.drawString(460, 246, "%s "% (pk.barang.get_kondisi_layar_display())) #LAYAR
        c.drawString(400, 236, "6.Password")
        c.drawString(460, 236, "%s "% (pk.barang.password_barang ))  #PASSWORD
        c.drawString(400, 226, "7.Dus")
        c.drawString(460, 226, "%s "% (pk.barang.get_dus_display())) #DUS
        c.drawString(400, 216, "8.Tas")
        c.drawString(460, 216, "%s "% (pk.barang.get_tas_display()))#TAS

    elif pk.barang.jenis_barang == u'2':###('2','LAPTOP/NB'),
        c.drawString(280, 256, "Kelengkapan :") 
        c.drawString(280, 246, "1.Charger")
        c.drawString(335, 246, "%s "% (pk.barang.get_kondisi_charger_display()))  #CHARGER
        c.drawString(280, 236, "2.Baterai")
        c.drawString(335, 236, "%s "% (pk.barang.get_kondisi_batre_display()))  #BATRE
        c.drawString(280, 226, "3.Keypad")
        c.drawString(335, 226, "%s "% (pk.barang.get_kondisi_keybord_display()))   #KEYPAD
        c.drawString(280, 216, "4.Cassing")
        c.drawString(335, 216, "%s "% (pk.barang.get_kondisi_cassing_display())) #CASSING

        c.drawString(400, 246, "5.Layar")
        c.drawString(460, 246, "%s "% (pk.barang.get_kondisi_layar_display())) #LAYAR
        c.drawString(400, 236, "6.Password")
        c.drawString(460, 236, "%s "% (pk.barang.password_barang ))  #PASSWORD
        c.drawString(400, 226, "7.Dus")
        c.drawString(460, 226, "%s "% (pk.barang.get_dus_display())) #DUS
        c.drawString(400, 216, "8.Tas")
        c.drawString(460, 216, "%s "% (pk.barang.get_tas_display()))#TAS

    elif pk.barang.jenis_barang == u'3':###('3','KAMERA'),
        c.drawString(280, 256, "Kelengkapan :")
        c.drawString(280, 246, "1.Lensa")
        c.drawString(335, 246, "%s "% (pk.barang.get_kondisi_lensa_display()))
        c.drawString(280, 236, "2.Baterai")
        c.drawString(335, 236, "%s "% (pk.barang.get_kondisi_batre_kamera_display()))
        c.drawString(280, 226, "3.Cassing")
        c.drawString(335, 226, "%s "% (pk.barang.get_kondisi_cassing_kamera_display()))
        c.drawString(280, 216, "4.Dus")
        c.drawString(335, 216, "%s "% (pk.barang.get_dus_display()))

        c.drawString(420, 246, "5.Tas")
        c.drawString(460, 246, "%s "% (pk.barang.get_tas_display()))

    elif pk.barang.jenis_barang == u'4':###('4','PS'),
        c.drawString(280, 256, "Kelengkapan :")
        c.drawString(280, 246, "1.Optik")
        c.drawString(335, 246, "%s "% (pk.barang.get_kondisi_optik_ps_display()))
        c.drawString(280, 236, "2.Stick")
        c.drawString(335, 236, "%s "% (pk.barang.get_kondisi_stick_display()))
        c.drawString(280, 226, "3.HDMI")
        c.drawString(335, 226, "%s "% (pk.barang.get_kondisi_hdmi_display())) 
        c.drawString(280, 216, "4.Harddisk")
        c.drawString(335, 216, "%s "% (pk.barang.get_kondisi_harddisk_display()))

        c.drawString(420, 246, "5.Dus")
        c.drawString(460, 246, "%s "% (pk.barang.get_dus_display()))
        c.drawString(420, 236, "6.Tas")
        c.drawString(460, 236, "%s "% (pk.barang.get_tas_display()))

    elif pk.barang.jenis_barang == u'5':###('5','TV LCD'),
        c.drawString(280, 256, "Kelengkapan :")
        c.drawString(280, 246, "1.Layar")
        c.drawString(335, 246, "%s "% (pk.barang.get_kondisi_layar_tv_display()))
        c.drawString(280, 236, "2.Remote")
        c.drawString(335, 236, "%s "% (pk.barang.get_kondisi_remote_display()))
        c.drawString(280, 226, "3. Dus")
        c.drawString(335, 226, "%s "% (pk.barang.get_dus_display()))
        c.drawString(280, 216, "4.Tas")
        c.drawString(335, 216, "%s "% (pk.barang.get_tas_display()))

    elif pk.barang.jenis_kendaraan == u'1':###('6','MOTOR'),
        c.drawString(280, 256, "Kelengkapan :")
        c.drawString(280, 246, "1.Bpkb")
        c.drawString(390, 246, "%s "% (pk.barang.get_bpkb_display()))
        c.drawString(280, 236, "2.Stnk")
        c.drawString(390, 236, "%s "% (pk.barang.get_stnk_display()))
        c.drawString(280, 226, "3.Faktur")
        c.drawString(390, 226, "%s "% (pk.barang.get_faktur_display()))
        c.drawString(280, 216, "4.Gesek No Mesin")
        c.drawString(390, 216, "%s "% (pk.barang.get_gesek_nomesin_display()))
        c.drawString(280, 206, "5.Gesek No Rangka")
        c.drawString(390, 206, "%s "% (pk.barang.get_gesek_norangka_display()))

    elif pk.barang.jenis_kendaraan == u'2':###('7','Mobil'),
        c.drawString(280, 256, "Kelengkapan :")
        c.drawString(280, 246, "1.Bpkb")
        c.drawString(390, 246, "%s "% (pk.barang.get_bpkb_display()))
        c.drawString(280, 236, "2.Stnk")
        c.drawString(390, 236, "%s "% (pk.barang.get_stnk_display()))
        c.drawString(280, 226, "3.Faktur")
        c.drawString(390, 226, "%s "% (pk.barang.get_faktur_display()))
        c.drawString(280, 216, "4.Gesek No Mesin")
        c.drawString(390, 216, "%s "% (pk.barang.get_gesek_nomesin_display()))
        c.drawString(280, 206, "5.Gesek No Rangka")
        c.drawString(390, 206, "%s "% (pk.barang.get_gesek_norangka_display()))
    c.setFont("Courier", 6)
    c.drawString(20, 56, "SBG Sah dan mengikat setelah ditandatangani oleh Para Pihak" ) 
    c.showPage()


    ###KOTAK Perjanjian Utang Piutang Dengan Jaminan Gadai
    c.setFillColorRGB(255,255,255)
    c.rect(0.2*inch,7.2*inch,9*inch,5.7*inch, fill=1)
    ###KOTAK KUASA MENJUAL
    #c.rect(0.2*inch,10.9*inch,2*inch,2.0*inch, fill=1)
    c.rect(0.2*inch,11.4*inch,2*inch,1.5*inch, fill=1)
    ###KOTAK PEMBERIAN KUASA
    c.rect(0.2*inch,7.9*inch,2*inch,3.5*inch, fill=1)
    ###KOTAK BUKTI Penyerahan
    c.rect(0.2*inch,7.2*inch,2*inch,1*inch, fill=1)
    c.setFillColorRGB(0,0,0)

    c.setFont("Courier-Bold", 8)
    c.drawString(55, 920, "KUASA MENJUAL")
    c.setFont("Courier", 6)
    c.drawString(18, 913, "Hak untuk menjual barang jaminan  yang")
    c.drawString(18, 906, "telah lewat jatuh tempo. Saya serahkan")
    c.drawString(18, 899, "kepada PT. Gadai Solusi Bersama.")
    c.drawString(18, 892, "Pemberi Kuasa Menjual :")
    c.drawString(18, 878, "Nama"); 
    c.drawString(50, 878, ": ............")
    c.drawString(18, 864, "No Telp"); 
    c.drawString(50, 864, ": ............")
    c.drawString(18, 850, "Alamat"); 
    c.drawString(50, 850, ": ............")
    c.drawString(18, 829, "( %s )" %(pk.agnasabah.nama)); y -=2*y1
    c.setFont("Courier-Bold", 8)
    c.drawString(55, 813, "PEMBERIAN KUASA"); y -=y1
    c.setFont("Courier", 6)
    c.drawString(18, 799, "Pada Tanggal :"); y -=2*y1
    c.drawString(18, 785, ".................................."); y -=2*y1
    c.drawString(18, 771, "Dengan ini saya memberikan kuasa untuk"); y -=y1
    c.drawString(18, 757, "Gadai  Ulang / Top Up Pinjaman / Cicil"); y -=y1
    c.drawString(18, 743, "Pokok Pinjaman/ Pelunasan dan Menerima"); y -=y1
    c.drawString(18, 729, "Barang  Jaminan*)  /  pengambilan uang"); y -=y1
    c.drawString(18, 715, "kelebihan *) kepada :"); y -=2.5*y1
    c.drawString(18, 701, "Nama"); 
    c.drawString(50, 701, ": ............"); y -=2*y1
    c.drawString(18, 687, "Alamat");
    c.drawString(50, 687, ": ............"); y -=2*y1
    c.drawString(18, 673, "No KTP"); 
    c.drawString(50, 673, ": ............"); y -=2*y1

    c.drawString(18, 659, "Pemberi Kuasa"); 
    c.drawString(75, 659, "Penerima Kuasa"); y -=3*y1

    c.drawString(18, 615, "..............."); 
    c.drawString(75, 615, "..............."); y -=2*y1
    c.drawString(18, 605, "*) konfirmasi kepada nasabah dan coret"); y -=y1	
    c.drawString(18, 595, "yang tidak perlu"); y -=1.5*y1	

    c.drawString(50, 580, "BUKTI PENYERAHAN BARANG"); y -=y1
    c.drawString(50, 572, "JAMINAN/ UANG KELEBIHAN"); y -=6*y1
    c.drawString(50, 535, "( %s )" %(pk.agnasabah.nama)); y -=y1
    c.drawString(50, 525, "Nasabah Penerima Kuasa"); y -=y1

    c.setFont("Courier-Bold", 10)
    c.drawString(305, 920, "Perjanjian Utang Piutang Dengan Jaminan Gadai"); y -=y1
    c.setFont("Courier", 7)
    c.drawString(160, 906, "Kami yang bertandatangan dibawah Surat Bukti Gadai (SBG) ini, yakni PT.GADAI SOLUSI BERSAMA dan Nasabah (pemilik barang"); y -=y1
    c.drawString(160, 899, "jaminan atau kuasa dari pemilik barang jaminan) sepakat membuat perjanjian sebagai berikut :"); y -=y1
    c.drawString(160, 885, "1. Barang yang diserahkan sebagai jaminan adalah milik Nasabah dan/atau kepemilikan  sebagaimana pasal 1977 KUH Per dan"); y -=y1
    c.drawString(160, 878, "   menjamin  bukan berasal dari  hasil kejahatan, tidak dalam  obyek sengketa  dan/atau sita jaminan. Barang asli bukan"); y -=y1
    c.drawString(160, 871, "   replika, tiruan dan/atau palsu."); y -=y1

    c.drawString(160, 862, "2. Nasabah  menyatakan telah berutang kepada PT. GADAI SOLUSI BERSAMA  dan  berkewajiban untuk membayar Pelunasan Uang"); y -=y1
    c.drawString(160, 848, "   Pinjaman ditambah jasa sebesar  tarif yang  berlaku di PT. GADAI SOLUSI BERSAMA, dan biaya proses lelang (jika ada),"); y -=y1
    c.drawString(160, 841, "   biaya keterlambatan pembayaran."); y -=y1

    c.drawString(160, 832, "3. Nasabah menerima  dan  setuju  terhadap  uraian  barang  jaminan, penetapan  besarnya taksiran  barang jaminan, uang"); y -=y1
    c.drawString(160, 825, "   pinjaman, tarif jasa, biaya  administrasi  dan  biaya  simpan sebagaimana yang dimaksud pada Surat Bukti Gadai (SBG)"); y -=y1
    c.drawString(160, 818, "   dan sebagai tanda bukti yang sah penerimaan uang pinjaman."); y -=y1

    c.drawString(160, 809, "4. Nasabah dapat melakukan Gadai Ulang, selama nilai taksiran masih  memenuhi syarat dengan memperhitungkan jasa, biaya"); y -=y1
    c.drawString(160, 802, "   administrasi dan biaya simpan yang masih akan dibayar.Jika terjadi penurunan nilai Taksiran Barang Jaminan pada saat"); y -=y1
    c.drawString(160, 795, "   Gadai Ulang, maka nasabah wajib mengangsur uang pinjaman."); y -=y1

    c.drawString(160, 786, "5. Apabila terjadi keterlambatan pada  saat dilakukan pelunasan oleh nasabah,maka nasabah harus membayar biaya keterlam"); y -=y1
    c.drawString(160, 779, "   batan yang ditetapkan oleh PT. GADAI SOLUSI BERSAMA."); y -=y1

    c.drawString(160, 770, "6. Nasabah dapat  datang sendiri untuk  melakukan gadai ulang, mengangsur  uang pinjaman, pelunasan dan menerima barang"); y -=y1
    c.drawString(160, 763, "   jaminan dan menerima uang kelebihan lelang atau  dengan memberikan kuasa kepada  orang lain dengan mengisi dan membu"); y -=y1
    c.drawString(160, 756, "   buhkan tanda tangan pada  kolom yang tersedia, dengan  melampirkan foto  copy KTP  Nasabah dan  penerima kuasa serta"); y -=y1
    c.drawString(160, 749, "   menunjukkan asli KTP Penerima kuasa."); y -=y1

    c.drawString(160, 740, "7. Pengembalian  barang jaminan  nasabah wajib  menyampaikan pemberitahuan  kepada petugas  gerai tempat dimana nasabah "); y -=y1
    c.drawString(160, 733, "   melakukan transaksi pinjaman, paling lambat 1 (satu) hari sebelum pelunasan dilakukan."); y -=y1

    c.drawString(160, 724, "8. Pinjaman yang telah jatuh tempo, PT. Gadai Solusi Bersama akan menyampaikan pemberitahuan secara layak, baik melalui"); y -=y1
    c.drawString(160, 717, "   surat atau  media lainnya  ke alamat / nomor kontak  yang  dicantumkan  nasabah sesuai Surat Bukti Gadai ini untuk"); y -=y1
    c.drawString(160, 710, "   segera melunasi pokok pinjaman beserta denda/ biaya lain yang ditetapkan oleh pihak PT. Gadai Solusi Bersama."); y -=y1

    c.drawString(160, 701, "9. Apabila sampai dengan tanggal Jatuh Tempo tidak  dilakukan Pelunasan atau Gadai Ulang, maka PT. GADAI SOLUSI BERSAMA"); y -=y1
    c.drawString(160, 694, "   berhak melakukan penjualan Barang Jaminan melalui Lelang.Barang Jaminan dapat dijual dengan cara nasabah menjual sen "); y -=y1
    c.drawString(160, 687, "   diri Barang Jaminannya,atau nasabah memberikan kuasa kepada perusahaan pergadaian untuk menjualkan Barang Jaminannya."); y -=y1

    c.drawString(160, 678, "10.Hasil  penjualan lelang barang jaminan setelah dikurangi uang pinjaman,jasa, biaya administrasi, biaya simpan, denda"); y -=y1
    c.drawString(160, 671, "   keterlambatan, biaya proses lelang  (bila ada) dan bea  lelang, merupakan kelebihan yang menjadi hak nasabah. Jangka"); y -=y1
    c.drawString(160, 664, "   waktu  pengambilan uang  kelebihan lelang selama  satu tahun sejak  tanggal lelang, dan jika lewat waktu dari jangka"); y -=y1
    c.drawString(160, 657, "   waktu pengambilan uang kelebihan, nasabah menyatakan setuju untuk menyalurkan uang  kelebihan tersebut  sebagai dana"); y -=y1
    c.drawString(160, 651, "   kepedulian sosial yang pelaksanannya diserahkan kepada PT.  GADAI SOLUSI BERSAMA. "); y -=y1#Jika hasil penjualan barang lelang"); y -=y1
  
    c.drawString(160, 642, "11.Bilamana  nasabah  meninggal  dunia dan  terdapat hak  dan kewajiban  terhadap PT. GADAI SOLUSI BERSAMA ataupun seba"); y -=y1
    c.drawString(160, 635, "   liknya, maka hak  dan kewajiban  dibebankan  kepada  ahli waris nasabah  sesuai  dengan ketentuan waris dalam  hukum");y -=y1
    c.drawString(160, 628, "   Republik Indonesia."); y -=y1

    c.drawString(160, 619, "12.PT. GADAI SOLUSI BERSAMA  akan  memberikan  ganti  kerugian  apabila  barang  jaminan  yang  berada dalam penguasaan "); y -=y1
    c.drawString(160, 612, "   PT. GADAI SOLUSI BERSAMA  mengalami  kerusakan atau  hilang yang tidak  disebabkan oleh  suatu  bencana  alam (Force  "); y -=y1
    c.drawString(160, 605, "   Majeure) yang ditetapkan pemerintah.Ganti rugi diberikan setelah diperhitungkan dengan Uang Pinjaman dan penggantian"); y -=y1
    c.drawString(160, 598, "   berupa uang atau barang yang nilainya maksimal sama atau setara dengan barang jaminan saat terjadinya kerusakan atau "); y -=y1
    c.drawString(160, 591, "   kehilangan atau pada saat barang tersebut dijaminkan."); y -=y1

    c.drawString(160, 582, "13.Nasabah menyatakan  telah  membaca  dan memahami  isi perjanjian ini serta tunduk dan mengikuti terhadap aturan yang "); y -=y1
    c.drawString(160, 575, "   tertuang dalam Surat Bukti Gadai  ini.  "); y -=y1

    c.drawString(160, 566, "14.PT. GADAI SOLUSI BERSAMA bersedia  menerima dan menyelesaikan setiap  bentuk pengaduan dan sengketa, apabila terjadi"); y -=y1
    c.drawString(160, 559, "   perselisihan dikemudian  hari  akan  diselesaikan secara musyawarah  untuk mufakat dan apabila tidak tercapai kesepa "); y -=y1
    c.drawString(160, 552, "   katan akan diselesaikan melalui pengadilan negeri setempat."); y -=y1

    c.drawString(160, 538, "Demikian perjanjian ini berlaku dan mengikat PT. GADAI SOLUSI BERSAMA  dengan Nasabah sejak Surat Bukti Gadai ini ditan"); y -=y1
    c.drawString(160, 531, "datangani oleh kedua belah pihak pada kolom yang tersedia di bagian depan."); y -=y1

    ##--------##
    ###KOTAK Perjanjian Utang Piutang Dengan Jaminan Gadai
    c.setFillColorRGB(255,255,255)
    c.rect(0.2*inch,0.64*inch,9*inch,5.74*inch, fill=1)
    #c.rect(0.2*inch,-0.2*inch,9*inch,7.2*inch, fill=1)

    ###KOTAK KUASA MENJUAL
    c.rect(0.2*inch,4.88*inch,2*inch,1.5*inch, fill=1)
    ###KOTAK PEMBERIAN KUASA
    c.rect(0.2*inch,1.4*inch,2*inch,3.5*inch, fill=1)
    ###KOTAK BUKTI Penyerahan
    c.rect(0.2*inch,0.64*inch,2*inch,1.2*inch, fill=1)
    c.setFillColorRGB(0,0,0)

    c.setFont("Courier-Bold", 8)
    c.drawString(55, 451, "KUASA MENJUAL")
    c.setFont("Courier", 6)
    c.drawString(18, 444, "Hak untuk menjual barang jaminan  yang")
    c.drawString(18, 437, "telah lewat jatuh tempo. Saya serahkan")
    c.drawString(18, 430, "kepada PT. Gadai Solusi Bersama.")
    c.drawString(18, 423, "Pemberi Kuasa Menjual :")
    c.drawString(18, 409, "Nama"); 
    c.drawString(50, 409, ": ............")
    c.drawString(18, 395, "No Telp"); 
    c.drawString(50, 395, ": ............")
    c.drawString(18, 381, "Alamat"); 
    c.drawString(50, 381, ": ............")
    c.drawString(18, 360, "( %s )" %(pk.agnasabah.nama)); y -=2*y1
    c.setFont("Courier-Bold", 8)
    c.drawString(55, 344, "PEMBERIAN KUASA"); y -=y1
    c.setFont("Courier", 6)
    c.drawString(18, 330, "Pada Tanggal :"); y -=2*y1
    c.drawString(18, 316, ".................................."); y -=2*y1
    c.drawString(18, 302, "Dengan ini saya memberikan kuasa untuk"); y -=y1
    c.drawString(18, 288, "Gadai  Ulang / Top Up Pinjaman / Cicil"); y -=y1
    c.drawString(18, 274, "Pokok Pinjaman/ Pelunasan dan Menerima"); y -=y1
    c.drawString(18, 260, "Barang  Jaminan*)  /  pengambilan uang"); y -=y1
    c.drawString(18, 246, "kelebihan *) kepada :"); y -=2.5*y1
    c.drawString(18, 232, "Nama"); 
    c.drawString(50, 232, ": ............"); y -=2*y1
    c.drawString(18, 218, "Alamat");
    c.drawString(50, 218, ": ............"); y -=2*y1
    c.drawString(18, 204, "No KTP"); 
    c.drawString(50, 204, ": ............"); y -=2*y1

    c.drawString(18, 190, "Pemberi Kuasa"); 
    c.drawString(75, 190, "Penerima Kuasa"); y -=3*y1

    c.drawString(18, 156, "..............."); 
    c.drawString(75, 156, "..............."); y -=2*y1
    c.drawString(18, 146, "*) konfirmasi kepada nasabah dan coret"); y -=y1	
    c.drawString(18, 136, "yang tidak perlu"); y -=1.5*y1	

    c.drawString(50, 121, "BUKTI PENYERAHAN BARANG"); y -=y1
    c.drawString(50, 113, "JAMINAN/ UANG KELEBIHAN"); y -=6*y1
    c.drawString(50, 76, "( %s )" %(pk.agnasabah.nama)); y -=y1
    c.drawString(50, 66, "Nasabah Penerima Kuasa"); y -=y1

    c.setFont("Courier-Bold", 10)
    c.drawString(305, 451, "Perjanjian Utang Piutang Dengan Jaminan Gadai"); y -=y1
    c.setFont("Courier", 7)
    c.drawString(160, 437, "Kami yang bertandatangan dibawah Surat Bukti Gadai (SBG) ini, yakni PT.GADAI SOLUSI BERSAMA dan Nasabah (pemilik barang"); y -=y1
    c.drawString(160, 430, "jaminan atau kuasa dari pemilik barang jaminan) sepakat membuat perjanjian sebagai berikut :"); y -=y1
    c.drawString(160, 416, "1. Barang yang diserahkan sebagai jaminan adalah milik Nasabah dan/atau kepemilikan  sebagaimana pasal 1977 KUH Per dan"); y -=y1
    c.drawString(160, 409, "   menjamin  bukan berasal dari  hasil kejahatan, tidak dalam  obyek sengketa  dan/atau sita jaminan. Barang asli bukan"); y -=y1
    c.drawString(160, 402, "   replika, tiruan dan/atau palsu."); y -=y1

    c.drawString(160, 393, "2. Nasabah  menyatakan telah berutang kepada PT. GADAI SOLUSI BERSAMA  dan  berkewajiban untuk membayar Pelunasan Uang"); y -=y1
    c.drawString(160, 386, "   Pinjaman ditambah jasa sebesar  tarif yang  berlaku di PT. GADAI SOLUSI BERSAMA, dan biaya proses lelang (jika ada),"); y -=y1
    c.drawString(160, 379, "   biaya keterlambatan pembayaran."); y -=y1

    c.drawString(160, 370, "3. Nasabah menerima  dan  setuju  terhadap  uraian  barang  jaminan, penetapan  besarnya taksiran  barang jaminan, uang"); y -=y1
    c.drawString(160, 363, "   pinjaman, tarif jasa, biaya  administrasi  dan  biaya  simpan sebagaimana yang dimaksud pada Surat Bukti Gadai (SBG)"); y -=y1
    c.drawString(160, 356, "   dan sebagai tanda bukti yang sah penerimaan uang pinjaman."); y -=y1

    c.drawString(160, 347, "4. Nasabah dapat melakukan Gadai Ulang, selama nilai taksiran masih  memenuhi syarat dengan memperhitungkan jasa, biaya"); y -=y1
    c.drawString(160, 340, "   administrasi dan biaya simpan yang masih akan dibayar.Jika terjadi penurunan nilai Taksiran Barang Jaminan pada saat"); y -=y1
    c.drawString(160, 333, "   Gadai Ulang, maka nasabah wajib mengangsur uang pinjaman."); y -=y1

    c.drawString(160, 324, "5. Apabila terjadi keterlambatan pada  saat dilakukan pelunasan oleh nasabah,maka nasabah harus membayar biaya keterlam"); y -=y1
    c.drawString(160, 317, "   batan yang ditetapkan oleh PT. GADAI SOLUSI BERSAMA."); y -=y1

    c.drawString(160, 308, "6. Nasabah dapat  datang sendiri untuk  melakukan gadai ulang, mengangsur  uang pinjaman, pelunasan dan menerima barang"); y -=y1
    c.drawString(160, 301, "   jaminan dan menerima uang kelebihan lelang atau  dengan memberikan kuasa kepada  orang lain dengan mengisi dan membu"); y -=y1
    c.drawString(160, 294, "   buhkan tanda tangan pada  kolom yang tersedia, dengan  melampirkan foto  copy KTP  Nasabah dan  penerima kuasa serta"); y -=y1
    c.drawString(160, 287, "   menunjukkan asli KTP Penerima kuasa."); y -=y1

    c.drawString(160, 278, "7. Pengembalian  barang jaminan  nasabah wajib  menyampaikan pemberitahuan  kepada petugas  gerai tempat dimana nasabah "); y -=y1
    c.drawString(160, 271, "   melakukan transaksi pinjaman, paling lambat 1 (satu) hari sebelum pelunasan dilakukan."); y -=y1

    c.drawString(160, 262, "8. Pinjaman yang telah jatuh tempo, PT. Gadai Solusi Bersama akan menyampaikan pemberitahuan secara layak, baik melalui"); y -=y1
    c.drawString(160, 255, "   surat atau  media lainnya  ke alamat / nomor kontak  yang  dicantumkan  nasabah sesuai Surat Bukti Gadai ini untuk"); y -=y1
    c.drawString(160, 248, "   segera melunasi pokok pinjaman beserta denda/ biaya lain yang ditetapkan oleh pihak PT. Gadai Solusi Bersama."); y -=y1

    c.drawString(160, 239, "9. Apabila sampai dengan tanggal Jatuh Tempo tidak  dilakukan Pelunasan atau Gadai Ulang, maka PT. GADAI SOLUSI BERSAMA"); y -=y1
    c.drawString(160, 232, "   berhak melakukan penjualan Barang Jaminan melalui Lelang.Barang Jaminan dapat dijual dengan cara nasabah menjual sen "); y -=y1
    c.drawString(160, 225, "   diri Barang Jaminannya,atau nasabah memberikan kuasa kepada perusahaan pergadaian untuk menjualkan Barang Jaminannya."); y -=y1

    c.drawString(160, 216, "10.Hasil  penjualan lelang barang jaminan setelah dikurangi uang pinjaman,jasa, biaya administrasi, biaya simpan, denda"); y -=y1
    c.drawString(160, 209, "   keterlambatan, biaya proses lelang  (bila ada) dan bea  lelang, merupakan kelebihan yang menjadi hak nasabah. Jangka"); y -=y1
    c.drawString(160, 202, "   waktu  pengambilan uang  kelebihan lelang selama  satu tahun sejak  tanggal lelang, dan jika lewat waktu dari jangka"); y -=y1
    c.drawString(160, 195, "   waktu pengambilan uang kelebihan, nasabah menyatakan setuju untuk menyalurkan uang  kelebihan tersebut  sebagai dana"); y -=y1
    c.drawString(160, 186, "   kepedulian sosial yang pelaksanannya diserahkan kepada PT.  GADAI SOLUSI BERSAMA. "); y -=y1#Jika hasil penjualan barang lelang"); y -=y1
  
    c.drawString(160, 177, "11.Bilamana  nasabah  meninggal  dunia dan  terdapat hak  dan kewajiban  terhadap PT. GADAI SOLUSI BERSAMA ataupun seba"); y -=y1
    c.drawString(160, 170, "   liknya, maka hak  dan kewajiban  dibebankan  kepada  ahli waris nasabah  sesuai  dengan ketentuan waris dalam  hukum");y -=y1
    c.drawString(160, 163, "   Republik Indonesia."); y -=y1

    c.drawString(160, 154, "12.PT. GADAI SOLUSI BERSAMA  akan  memberikan  ganti  kerugian  apabila  barang  jaminan  yang  berada dalam penguasaan "); y -=y1
    c.drawString(160, 147, "   PT. GADAI SOLUSI BERSAMA  mengalami  kerusakan atau  hilang yang tidak  disebabkan oleh  suatu  bencana  alam (Force  "); y -=y1
    c.drawString(160, 140, "   Majeure) yang ditetapkan pemerintah.Ganti rugi diberikan setelah diperhitungkan dengan Uang Pinjaman dan penggantian"); y -=y1
    c.drawString(160, 133, "   berupa uang atau barang yang nilainya maksimal sama atau setara dengan barang jaminan saat terjadinya kerusakan atau "); y -=y1
    c.drawString(160, 126, "   kehilangan atau pada saat barang tersebut dijaminkan."); y -=y1

    c.drawString(160, 117, "13.Nasabah menyatakan  telah  membaca  dan memahami  isi perjanjian ini serta tunduk dan mengikuti terhadap aturan yang "); y -=y1
    c.drawString(160, 110, "   tertuang dalam Surat Bukti Gadai  ini.  "); y -=y1

    c.drawString(160, 101, "14.PT. GADAI SOLUSI BERSAMA bersedia  menerima dan menyelesaikan setiap  bentuk pengaduan dan sengketa, apabila terjadi"); y -=y1
    c.drawString(160, 92, "   perselisihan dikemudian  hari  akan  diselesaikan secara musyawarah  untuk mufakat dan apabila tidak tercapai kesepa "); y -=y1
    c.drawString(160, 85, "   katan akan diselesaikan melalui pengadilan negeri setempat."); y -=y1

    c.drawString(160, 71, "Demikian perjanjian ini berlaku dan mengikat PT. GADAI SOLUSI BERSAMA  dengan Nasabah sejak Surat Bukti Gadai ini ditan"); y -=y1
    c.drawString(160, 64, "datangani oleh kedua belah pihak pada kolom yang tersedia di bagian depan."); y -=y1

    c.showPage()
    c.save()
    return response


def kw_sbg(request, object_id):
    pk = AkadGadai.objects.get(id=object_id)
    pk.status_kw = '1'
    pk.save()
    #tiga_play = [p,p,p]
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % pk.norek()
    c = canvas.Canvas(response, pagesize=(9.5*inch, 13*inch))
    c.setTitle("kwitansi %s" % pk.norek())
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
        trk=pk.tanggal
        dd=patokan.month-trk.month
        yy=patokan.year-trk.year


    header1=(4.25 *inch, (5.3 + 5.5) * inch)
    colom1 = (0.5*inch, (4.3 + 5.5) *inch)
            #ke kiri  ke atas ke bawah
    colom2 = (6.7*inch, (4.5 + 5.5) *inch)
    colom3 = (6.0*inch, (4.8 + 4.5) *inch)
    colom4 = (0.5*inch, (3.7 + 4.5) *inch)

    header2=(8.25 *inch, (2.75 + 2.5) * inch)    
    header3=(4.25 *inch, (2.8 + 2.65) * inch)        
    #header2=(4.25 *inch, (5.3 + 5.5) * inch)
    colom5 = (0.5*inch, (2.15 + 2.3) *inch)
            #ke kiri  ke atas ke bawah
    colom6 = (6.7*inch, (2.15 + 2.3) *inch)
    colom7 = (6.0*inch, (2.25 + 1.5) *inch)
    colom8 = (0.5*inch, (1.5 + 1.1) *inch)
    tb=terbilang(pk.terima_bersih_all())
    ###KOTAK LOGO
    c.setFillColorRGB(255,255,255)
    c.rect(0.2*inch,12.3*inch,9*inch,0.6*inch, fill=1)
    ###Tanggal Transaksi
    c.rect(7.4*inch,11.3*inch,1.8*inch,0.6*inch, fill=1)
    ###KOTAK SURAT BUKTI GADAI
    c.setFillColorRGB(245, 229, 27,1)
    c.rect(0.2*inch,11.9*inch,3*inch,0.4*inch, fill=1)
    ###KOTAK NO BUKTI
    c.rect(3*inch,11.9*inch,6.2*inch,0.4*inch, fill=1)
    ###KOTAK Tanggal JATUH TEMPO
    c.rect(7.4*inch,11.9*inch,1.8*inch,0.4*inch, fill=1)

    ###KOTAK INFO PERHATIAN
    c.rect(7.4*inch,10.18*inch,1.8*inch,1.22*inch, fill=1)
    ##Kotak TTD NASABAH
    c.rect(7.4*inch,8.9*inch,1.8*inch,2.0*inch, fill=1)

    ##KOTAK KETERANGAN BARANG JAMINAN
    c.rect(0.2*inch,7.2*inch,7.2*inch,4.5*inch, fill=1)
    c.rect(3.8*inch,7.7*inch,3.6*inch,4.1*inch, fill=1)
    ###KOTAK ISIAN NAMA 
    c.rect(0.2*inch,10.9*inch,7.2*inch,1.0*inch, fill=1)
    ##Kotak TTD Petugas
    c.rect(3.8*inch,7.2*inch,5.4*inch,1.7*inch, fill=1)
    ##Kotak Setuju2
    c.rect(3.8*inch,8.7*inch,5.4*inch,0.2*inch, fill=1)
    c.setFillColorRGB(0,0,0)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/gaban_gsb.png'), 0.3*inch, (6.9 + 5.5) * inch, width=78/17.5*0.51*inch,height=15/17.5*0.51*inch,mask=None)
    x,y = colom1
    y1 = 0.10 * inch
    y -=1*y1
    c.setFont("Courier",9)
    c.drawString(190, 905, "OUTLET/GERAI :")
    c.setFont("Courier-Bold", 12)
    c.drawString(270, 910, "%s"% (pk.gerai.nama_cabang))
    c.setFont("Courier-Bold", 9)
    c.drawString(270, 900, "%s/Telp: 0%s "% (pk.gerai.alamat, pk.gerai.no_telp))

    c.setFont("Courier", 7)
    barcode = code128.Code128("%s" % (pk.norek()))
    barcode.drawOn(c, 185*mm, 304.5*mm)
    c.setFont("Courier-Bold", 9) 
    c.drawString(540, 848, "Tanggal Transaksi") 
    c.drawString(540, 825, "%s" % (pk.tanggal.strftime('%d %b %Y')))
    c.drawString(540, 810, "Tanggal Jatuh Tempo") 
    c.drawString(540, 790, "%s" % (pk.jatuhtempo.strftime('%d %b %Y')))
   
    c.setFont("Courier-Bold", 12)  
    c.drawString(19, 868, "SURAT BUKTI GADAI PENCAIRAN")
    c.setFont("Courier-Bold", 14)  
    c.drawString(220, 868, "NO NASABAH: %s"% (pk.nonas()))
    c.setFont("Courier", 9)
    c.drawString(20, 848, "Nomor Rek")
    c.drawString(100, 848, ": %s" % (pk.norek()))
    c.drawString(20, 838, "Nama")
    c.drawString(100, 838, ": %s" % (pk.agnasabah.nama))
    c.drawString(20, 828, "No Identitas")
    c.drawString(100, 828, ": %s" % (pk.agnasabah.no_ktp))
    c.drawString(20, 818, "No Telepon")
    c.drawString(100, 818, ": %s" % (pk.agnasabah.telepon_domisili,))
    c.drawString(20, 808, "Alamat")
    c.drawString(100, 808, ": %s No %s" %(pk.agnasabah.alamat_domisili,pk.agnasabah.no_rumah_domisili))
    c.drawString(100.5, 798, "  RT/RW %s/%s %s" %(pk.agnasabah.rt_domisili,pk.agnasabah.rw_domisili,pk.agnasabah.kelurahan_domisili,))
    c.drawString(20, 788, "Tempat,Tgl Lhr")
    c.drawString(100, 788, ": %s, %s" %(pk.agnasabah.tempat,pk.agnasabah.tgl_lahir.strftime('%d %B %Y')))
    c.setFont("Courier-Bold", 9)
    c.drawString(570, 775, "Perhatian")
    c.setFont("Courier", 6)
    c.drawString(540, 753, "1. Apabila sampai dengan tanggal")
    c.drawString(540, 747, "   jatuh  tempo  tidak melakukan")
    c.drawString(540, 741, "   Pelunasan  atau  tidak  gadai")
    c.drawString(540, 735, "   ulang maka PT. GSB berhak men")
    c.drawString(540, 729, "   jual barang jaminan  yang ter")
    c.drawString(540, 723, "   tera di Surat Bukti Gadai ini.") 
    c.drawString(540, 717, "2. Apabila akan melakukan  gadai") 
    c.drawString(540, 711, "   ulang  harap menginformasikan") 
    c.drawString(540, 705, "   1  hari sebelum  jatuh  tempo")
    c.drawString(540, 699, "3. Setiap melakukan pelunasan at") 
    c.drawString(540, 693, "   au gadai  ulang, kwitansi ini") 
    c.drawString(540, 687, "   harus   diperlihatkan  kepada") 
    c.drawString(540, 681, "   petugas gerai.")
    c.drawString(540, 675, "4. Pelunasan atau gadai ulang ha")
    c.drawString(540, 669, "   rus dilakukan tepat waktu ses")
    c.drawString(540, 663, "   uai tanggal jatuh tempo.")
    c.drawString(540, 657, "5. Kwitansi ini sah apabila telah ")
    c.drawString(540, 651, "   divalidasi ditanda tangan dan ")
    c.drawString(540, 645, "   di stempel.")
    c.setFont("Courier", 8)
    c.drawString(278, 632, "Setuju atas isi perjanjian Gadai yang tertera di belakang Surat Bukti Gadai ini")
    c.drawString(285, 620, "Nasabah")
    c.drawString(285, 525, "%s" %(pk.agnasabah.nama))
    c.drawString(535, 620, "Kuasa Pemutus Jaminan")
    c.drawString(535, 525, "%s" %(pk.gerai.nama_kg))
    c.setFont("Courier", 9)
    c.drawString(20, 775, "KETERANGAN NILAI PINJAMAN:")
    c.drawString(20, 755, "Taksiran")
    c.drawString(90,755, ": Rp. %s" % (number_format(pk.taksir.maxpinjaman))) 
    c.drawString(20, 745, "Uang Pinjaman")
    c.drawString(90,745, ": Rp. %s" % (number_format(pk.nilai))) 

    tb=terbilang(pk.nilai)
    c.drawString(20, 735, "Terbilang") 
    c.drawString(90, 735, ":" ) 
    c.drawString(30, 725, "%s Rupiah" % (tb.title()))
    c.drawString(20, 705, "Bea Simpan/Survey")
    c.drawString(120, 705,":Rp.")
    if pk.jenis_transaksi  == '1':
        c.drawRightString(220, 705,"%s"% (number_format(pk.biayasimpan)))
    else:
        c.drawRightString(220, 705,"%s"% (number_format(pk.beasimpan_kendaraan)))
    c.drawString(20, 695, "Bea Administrasi")
    c.drawString(120, 695,":Rp.")
    if pk.jenis_transaksi  == '1':
        c.drawRightString(220, 695,"%s"%(number_format(pk.adm)))
    else:
        c.drawRightString(220, 695,"%s"%(number_format(pk.adm_kendaraan)))
    c.drawString(20, 685, "Jasa") 
    c.drawString(120, 685,":Rp.")
    c.drawRightString(220, 685,"%s"%(number_format(pk.jasa_kwitansi())))
    c.drawString(20, 675, "Bea Materai")
    c.drawString(120, 675,":Rp.")
    c.drawRightString(220, 675,"%s"% (number_format(pk.bea_materai)))
    c.line( 120 , 673 , 220 , 673 ) ; y -=y1
    c.drawString(20, 660, "Total Biaya") 
    c.drawString(120, 660,":Rp.")
    if pk.jenis_transaksi  == '1':
        c.drawRightString(220, 660,"%s"%(number_format(pk.jumlahbiaya_kwitansi)))
    else:
        c.drawRightString(220, 660,"%s"%(number_format(pk.jumlahbiaya_kendaraan)))
    c.line( 120 , 658 , 220 , 658 )
    c.setFont("Courier-Bold", 9)
    c.drawString(20, 640, "Nilai Diterima")
    c.drawString(120, 640,":Rp.")
    if pk.jenis_transaksi  == '1':    
        c.drawRightString(220, 640," %s"% (number_format(pk.terima_bersih_all())))        
    else:
        c.drawRightString(220, 640," %s"% (number_format(pk.terima_bersih_kendaraan)))
    if pk.jenis_transaksi  == '1':    
        tbk = terbilang(pk.terima_bersih_kwitansi)
    else:
        tbk = terbilang(pk.terima_bersih_kendaraan)
    c.drawString(20, 620, "Terbilang") 
    c.drawString(90, 620, ":" ) 
    c.drawString(30, 610, "%s" % (tbk.title()[0:37]))
    c.drawString(30, 600, "%s Rupiah" % (tbk.title()[37:90]))

    c.setFont("Courier", 9)
    c.drawString(280, 775, "KETERANGAN BARANG JAMINAN:")
    c.drawString(280, 765, "1. %s"% (pk.taksiran_kwitansi()[0:43] ))
    c.drawString(280, 755, "%s"% (pk.taksiran_kwitansi()[43:89] ))
    c.drawString(280, 745, "%s "% (pk.taksiran_kwitansi()[89:134] ))
    c.drawString(280, 735, "%s "% (pk.taksiran_kwitansi()[134:] ))

    if pk.barang.jenis_barang == u'1': ###('1','HP')
        c.drawString(280, 725, "Kelengkapan :") 
        c.drawString(280, 715, "1.Charger")
        c.drawString(335, 715, "%s "% (pk.barang.get_kondisi_charger_display()))  #CHARGER
        c.drawString(280, 705, "2.Baterai")
        c.drawString(335, 705, "%s "% (pk.barang.get_kondisi_batre_display()))  #BATRE
        c.drawString(280, 695, "3.Keypad")
        c.drawString(335, 695, "%s "% (pk.barang.get_kondisi_keybord_display()))   #KEYPAD
        c.drawString(280, 685, "4.Cassing")
        c.drawString(335, 685, "%s "% (pk.barang.get_kondisi_cassing_display())) #CASSING

        c.drawString(400, 715, "5.Layar")
        c.drawString(460, 715, "%s "% (pk.barang.get_kondisi_layar_display())) #LAYAR
        c.drawString(400, 705, "6.Password")
        c.drawString(460, 705, "%s "% (pk.barang.password_barang ))  #PASSWORD
        c.drawString(400, 695, "7.Dus")
        c.drawString(460, 695, "%s "% (pk.barang.get_dus_display())) #DUS
        c.drawString(400, 685, "8.Tas")
        c.drawString(460, 685, "%s "% (pk.barang.get_tas_display()))#TAS

    elif pk.barang.jenis_barang == u'2':###('2','LAPTOP/NB'),
        c.drawString(280, 725, "Kelengkapan :") 
        c.drawString(280, 715, "1.Charger")
        c.drawString(335, 715, "%s "% (pk.barang.get_kondisi_charger_display()))  #CHARGER
        c.drawString(280, 705, "2.Baterai")
        c.drawString(335, 705, "%s "% (pk.barang.get_kondisi_batre_display()))  #BATRE
        c.drawString(280, 695, "3.Keypad")
        c.drawString(335, 695, "%s "% (pk.barang.get_kondisi_keybord_display()))   #KEYPAD
        c.drawString(280, 685, "4.Cassing")
        c.drawString(335, 685, "%s "% (pk.barang.get_kondisi_cassing_display())) #CASSING

        c.drawString(400, 715, "5.Layar")
        c.drawString(460, 715, "%s "% (pk.barang.get_kondisi_layar_display())) #LAYAR
        c.drawString(400, 705, "6.Password")
        c.drawString(460, 705, "%s "% (pk.barang.password_barang ))  #PASSWORD
        c.drawString(400, 695, "7.Dus")
        c.drawString(460, 695, "%s "% (pk.barang.get_dus_display())) #DUS
        c.drawString(400, 685, "8.Tas")
        c.drawString(460, 685, "%s "% (pk.barang.get_tas_display()))#TAS

    elif pk.barang.jenis_barang == u'3':###('3','KAMERA'),
        c.drawString(280, 725, "Kelengkapan :")
        c.drawString(280, 715, "1.Lensa")
        c.drawString(335, 715, "%s "% (pk.barang.get_lensa_display()))
        c.drawString(280, 705, "2.Baterai")
        c.drawString(335, 705, "%s "% (pk.barang.get_batre_kamera_display()))
        c.drawString(280, 695, "3.Cassing")
        c.drawString(335, 695, "%s "% (pk.barang.get_cassing_kamera_display()))
        c.drawString(280, 685, "4.Dus")
        c.drawString(335, 685, "%s "% (pk.barang.get_dus_display()))

        c.drawString(420, 715, "5.Tas")
        c.drawString(460, 715, "%s "% (pk.barang.get_tas_display()))

    elif pk.barang.jenis_barang == u'4':###('4','PS'),
        c.drawString(280, 725, "Kelengkapan :")
        c.drawString(280, 715, "1.Optik")
        c.drawString(335, 715, "%s "% (pk.barang.get_kondisi_optik_ps_display()))
        c.drawString(280, 705, "2.Stick")
        c.drawString(335, 705, "%s "% (pk.barang.get_kondisi_stick_display()))
        c.drawString(280, 695, "3.HDMI")
        c.drawString(335, 695, "%s "% (pk.barang.get_kondisi_hdmi_display())) 
        c.drawString(280, 685, "4.Harddisk")
        c.drawString(335, 685, "%s "% (pk.barang.get_kondisi_harddisk_display()))

        c.drawString(420, 715, "5.Dus")
        c.drawString(460, 715, "%s "% (pk.barang.get_dus_display()))
        c.drawString(420, 705, "6.Tas")
        c.drawString(460, 705, "%s "% (pk.barang.get_tas_display()))

    elif pk.barang.jenis_barang == u'5':###('5','TV LCD'),
        c.drawString(280, 725, "Kelengkapan :")
        c.drawString(280, 715, "1.Layar")
        c.drawString(335, 715, "%s "% (pk.barang.get_kondisi_layar_tv_display()))
        c.drawString(280, 705, "2.Remote")
        c.drawString(335, 705, "%s "% (pk.barang.get_kondisi_remote_display()))
        c.drawString(280, 695, "3.Dus")
        c.drawString(335, 695, "%s "% (pk.barang.get_dus_display()))
        c.drawString(280, 685, "4.Tas")
        c.drawString(335, 685, "%s "% (pk.barang.get_tas_display()))

    elif pk.barang.jenis_kendaraan == u'1':###('6','MOTOR'),
        c.drawString(280, 725, "Kelengkapan :")
        c.drawString(280, 715, "1.Bpkb")
        c.drawString(390, 715, "%s "% (pk.barang.get_bpkb_display()))
        c.drawString(280, 705, "2.Stnk")
        c.drawString(390, 705, "%s "% (pk.barang.get_stnk_display()))
        c.drawString(280, 695, "3.Faktur")
        c.drawString(390, 695, "%s "% (pk.barang.get_faktur_display()))
        c.drawString(280, 685, "4.Gesek No Mesin")
        c.drawString(390, 685, "%s "% (pk.barang.get_gesek_nomesin_display()))
        c.drawString(280, 675, "5.Gesek No Rangka")
        c.drawString(390, 675, "%s "% (pk.barang.get_gesek_norangka_display()))

    elif pk.barang.jenis_kendaraan == u'2':###('7','Mobil'),
        c.drawString(280, 725, "Kelengkapan :")
        c.drawString(280, 715, "1.Bpkb")
        c.drawString(390, 715, "%s "% (pk.barang.get_bpkb_display()))
        c.drawString(280, 705, "2.Stnk")
        c.drawString(390, 705, "%s "% (pk.barang.get_stnk_display()))
        c.drawString(280, 695, "3.Faktur")
        c.drawString(390, 695, "%s "% (pk.barang.get_faktur_display()))
        c.drawString(280, 685, "4.Gesek No Mesin")
        c.drawString(390, 685, "%s "% (pk.barang.get_gesek_nomesin_display()))
        c.drawString(280, 675, "5.Gesek No Rangka")
        c.drawString(390, 675, "%s "% (pk.barang.get_gesek_norangka_display()))
    c.setFont("Courier", 6)
    c.drawString(20, 530, "SBG Sah dan mengikat setelah ditandatangani oleh Para Pihak" ) 
    c.drawString(0, 490, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" )

    ###KE DUA
    ###KOTAK LOGO
    c.setFillColorRGB(255,255,255)
    c.rect(0.2*inch,5.8*inch,9*inch,0.6*inch, fill=1)
    ###Tanggal Transaksi
    c.rect(7.4*inch,4.8*inch,1.8*inch,0.6*inch, fill=1)
    ###KOTAK SURAT BUKTI GADAI
    c.setFillColorRGB(245, 229, 27,1)
    c.rect(0.2*inch,5.4*inch,3*inch,0.4*inch, fill=1)

    ###KOTAK NO BUKTI
    c.rect(3*inch,5.4*inch,6.2*inch,0.4*inch, fill=1)
    ###KOTAK Barcode
    c.rect(7.4*inch,5.4*inch,1.8*inch,0.4*inch, fill=1)
    ###KOTAK Tanggal JATUH TEMPO
    c.rect(7.4*inch,4.4*inch,1.8*inch,0.4*inch, fill=1)
    ##Kotak INFO PERHATIAN
    c.rect(7.4*inch,2.4*inch,1.8*inch,2.0*inch, fill=1)

    ##KOTAK KETERANGAN BARANG JAMINAN
    c.rect(0.2*inch,0.7*inch,7.2*inch,4.2*inch, fill=1)
    c.rect(3.8*inch,1.2*inch,3.6*inch,4.1*inch, fill=1)
    ###KOTAK ISIAN NAMA 
    c.rect(0.2*inch,4.4*inch,7.2*inch,1.0*inch, fill=1)
    ##Kotak TTD Petugas

    c.rect(3.8*inch,0.7*inch,5.4*inch,1.5*inch, fill=1)
    ##Kotak Setuju2
    c.rect(3.8*inch,2.2*inch,5.4*inch,0.2*inch, fill=1)
    c.setFillColorRGB(0,0,0)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/gaban_gsb.png'), 0.3*inch, (0.40 + 5.5) * inch, width=78/17.5*0.51*inch,height=15/17.5*0.51*inch,mask=None)
    x,y = colom1	
    y1 = 0.10 * inch
    y -=1*y1
    c.setFont("Courier",9)
    c.drawString(190, 437, "OUTLET/GERAI :")
    c.setFont("Courier-Bold", 12)
    c.drawString(270, 442, "%s"% (pk.gerai.nama_cabang))
    c.setFont("Courier-Bold", 9)
    c.drawString(270, 432, "%s/Telp: 0%s "% (pk.gerai.alamat, pk.gerai.no_telp))

    c.setFont("Courier", 7)
    barcode = code128.Code128("%s" % (pk.norek()))
    barcode.drawOn(c, 185*mm, 139.5*mm)
    c.setFont("Courier-Bold", 9) 
    c.drawString(540, 380, "Tanggal Transaksi") 
    c.drawString(540, 349, "%s" % (pk.tanggal.strftime('%d %b %Y')))
    c.drawString(540, 337, "Tanggal Jatuh Tempo") 
    c.drawString(540, 320, "%s" % (pk.jatuhtempo.strftime('%d %b %Y')))

    c.setFont("Courier-Bold", 12)  
    c.drawString(19, 400, "SURAT BUKTI GADAI PENCAIRAN")
    c.setFont("Courier-Bold", 14)  
    c.drawString(220, 400, "NO NASABAH: %s"% (pk.nonas()))
    c.setFont("Courier", 9)
    c.drawString(20, 379, "Nomor Rek")
    c.drawString(100, 379, ": %s" % (pk.norek()))
    c.drawString(20, 369, "Nama")
    c.drawString(100, 369, ": %s" % (pk.agnasabah.nama))
    c.drawString(20, 359, "No Identitas")
    c.drawString(100, 359, ": %s" % (pk.agnasabah.no_ktp))
    c.drawString(20, 349, "No Telepon")
    c.drawString(100, 349, ": %s" % (pk.agnasabah.telepon_domisili,))
    c.drawString(20, 339, "Alamat")
    c.drawString(100, 339, ": %s No %s" %(pk.agnasabah.alamat_domisili,pk.agnasabah.no_rumah_domisili))
    c.drawString(100.5, 329, "  RT/RW %s/%s %s" %(pk.agnasabah.rt_domisili,pk.agnasabah.rw_domisili,pk.agnasabah.kelurahan_domisili,))
    c.drawString(20, 319, "Tempat,Tgl Lhr")
    c.drawString(100, 319, ": %s, %s" %(pk.agnasabah.tempat,pk.agnasabah.tgl_lahir.strftime('%d %B %Y')))
    c.setFont("Courier-Bold", 9)

    c.drawString(570, 306, "Perhatian")
    c.setFont("Courier", 6)
    c.drawString(540, 284, "1. Apabila sampai dengan tanggal")
    c.drawString(540, 278, "   jatuh  tempo  tidak melakukan")
    c.drawString(540, 272, "   Pelunasan  atau  tidak  gadai")
    c.drawString(540, 266, "   ulang maka PT. GSB berhak men")
    c.drawString(540, 260, "   jual barang jaminan  yang ter")
    c.drawString(540, 254, "   tera di Surat Bukti Gadai ini.") 
    c.drawString(540, 248, "2. Apabila akan melakukan  gadai") 
    c.drawString(540, 242, "   ulang  harap menginformasikan") 
    c.drawString(540, 236, "   1  hari sebelum  jatuh  tempo")
    c.drawString(540, 230, "3. Setiap melakukan pelunasan at") 
    c.drawString(540, 224, "   au gadai  ulang, kwitansi ini") 
    c.drawString(540, 218, "   harus   diperlihatkan  kepada") 
    c.drawString(540, 212, "   petugas gerai.")
    c.drawString(540, 206, "4. Pelunasan atau gadai ulang ha")
    c.drawString(540, 200, "   rus dilakukan tepat waktu ses")
    c.drawString(540, 194, "   uai tanggal jatuh tempo.")
    c.drawString(540, 188, "5. Kwitansi ini sah apabila telah ")
    c.drawString(540, 182, "   divalidasi ditanda tangan dan ")
    c.drawString(540, 176, "   di stempel.")
    c.setFont("Courier", 8)
    c.drawString(278, 163, "Setuju atas isi perjanjian Gadai yang tertera di belakang Surat Bukti Gadai ini")
    c.drawString(285, 151, "Nasabah")
    c.drawString(285, 56, "%s" %(pk.agnasabah.nama))
    c.drawString(535, 151, "Kuasa Pemutus Jaminan")
    c.drawString(535, 56, "%s" %(pk.gerai.nama_kg))
    c.setFont("Courier", 9)
    c.drawString(20, 306, "KETERANGAN NILAI PINJAMAN:")
    c.drawString(20, 286, "Taksiran")
    c.drawString(90, 286, ": Rp. %s" % (number_format(pk.taksir.maxpinjaman))) 
    c.drawString(20, 276, "Uang Pinjaman")
    c.drawString(90, 276, ": Rp. %s" % (number_format(pk.nilai))) 

    
    tb=terbilang(pk.nilai)
    c.drawString(20, 266, "Terbilang") 
    c.drawString(90, 266, ":" ) 
    c.drawString(30, 256, "%s Rupiah" % (tb.title()))
    c.drawString(20, 236, "Bea Simpan/Survey")
    c.drawString(120, 236,":Rp.")
    if pk.jenis_transaksi  == '1':
        c.drawRightString(220, 236,"%s"% (number_format(pk.biayasimpan)))
    else:
        c.drawRightString(220, 236,"%s"% (number_format(pk.beasimpan_kendaraan)))
    c.drawString(20, 226, "Bea Administrasi")
    c.drawString(120, 226,":Rp.")
    if pk.jenis_transaksi  == '1':
        c.drawRightString(220, 226,"%s"%(number_format(pk.adm)))
    else:
        c.drawRightString(220, 226,"%s"%(number_format(pk.adm_kendaraan)))
    c.drawString(20, 216, "Jasa") 
    c.drawString(120, 216,":Rp.")
    c.drawRightString(220, 216,"%s"%(number_format(pk.jasa_kwitansi())))
    c.drawString(20, 206, "Bea Materai")
    c.drawString(120, 206,":Rp.")
    c.drawRightString(220, 206,"%s"% (number_format(pk.bea_materai)))
    c.line( 120 , 204 , 220 , 204 ) ; y -=y1
    c.drawString(20, 191, "Total Biaya") 
    c.drawString(120, 191,":Rp.")
    if pk.jenis_transaksi  == '1':
        c.drawRightString(220, 191,"%s"%(number_format(pk.jumlahbiaya_kwitansi)))
    else:
        c.drawRightString(220, 191,"%s"%(number_format(pk.jumlahbiaya_kendaraan)))
    c.line( 120 , 189 , 220 , 189 )
    c.setFont("Courier-Bold", 9)
    c.drawString(20, 171, "Nilai Diterima")
    c.drawString(120, 171,":Rp.")
    if pk.jenis_transaksi  == '1':    
        c.drawRightString(220, 171," %s"% (number_format(pk.terima_bersih_kwitansi)))        
    else:
        c.drawRightString(220, 171," %s"% (number_format(pk.terima_bersih_kendaraan)))
    if pk.jenis_transaksi  == '1':    
        tbk = terbilang(pk.terima_bersih_kwitansi)
    else:
        tbk = terbilang(pk.terima_bersih_kendaraan)
    c.drawString(20, 151, "Terbilang") 
    c.drawString(90, 151, ":" ) 
    c.drawString(30, 141, "%s" % (tbk.title()[0:37]))
    c.drawString(30, 131, "%s Rupiah" % (tbk.title()[37:90]))

    c.setFont("Courier", 9)
    c.drawString(280, 306, "KETERANGAN BARANG JAMINAN:")
    c.drawString(280, 296, "1. %s"% (pk.taksiran_kwitansi()[0:43] ))
    c.drawString(280, 286, "%s"% (pk.taksiran_kwitansi()[43:89] ))
    c.drawString(280, 276, "%s "% (pk.taksiran_kwitansi()[89:134] ))
    c.drawString(280, 266, "%s "% (pk.taksiran_kwitansi()[134:] ))

    if pk.barang.jenis_barang == u'1': ###('1','HP')
        c.drawString(280, 256, "Kelengkapan :") 
        c.drawString(280, 246, "1.Charger")
        c.drawString(335, 246, "%s "% (pk.barang.get_kondisi_charger_display()))  #CHARGER
        c.drawString(280, 236, "2.Baterai")
        c.drawString(335, 236, "%s "% (pk.barang.get_kondisi_batre_display()))  #BATRE
        c.drawString(280, 226, "3.Keypad")
        c.drawString(335, 226, "%s "% (pk.barang.get_kondisi_keybord_display()))   #KEYPAD
        c.drawString(280, 216, "4.Cassing")
        c.drawString(335, 216, "%s "% (pk.barang.get_kondisi_cassing_display())) #CASSING

        c.drawString(400, 246, "5.Layar")
        c.drawString(460, 246, "%s "% (pk.barang.get_kondisi_layar_display())) #LAYAR
        c.drawString(400, 236, "6.Password")
        c.drawString(460, 236, "%s "% (pk.barang.password_barang ))  #PASSWORD
        c.drawString(400, 226, "7.Dus")
        c.drawString(460, 226, "%s "% (pk.barang.get_dus_display())) #DUS
        c.drawString(400, 216, "8.Tas")
        c.drawString(460, 216, "%s "% (pk.barang.get_tas_display()))#TAS

    elif pk.barang.jenis_barang == u'2':###('2','LAPTOP/NB'),
        c.drawString(280, 256, "Kelengkapan :") 
        c.drawString(280, 246, "1.Charger")
        c.drawString(335, 246, "%s "% (pk.barang.get_kondisi_charger_display()))  #CHARGER
        c.drawString(280, 236, "2.Baterai")
        c.drawString(335, 236, "%s "% (pk.barang.get_kondisi_batre_display()))  #BATRE
        c.drawString(280, 226, "3.Keypad")
        c.drawString(335, 226, "%s "% (pk.barang.get_kondisi_keybord_display()))   #KEYPAD
        c.drawString(280, 216, "4.Cassing")
        c.drawString(335, 216, "%s "% (pk.barang.get_kondisi_cassing_display())) #CASSING

        c.drawString(400, 246, "5.Layar")
        c.drawString(460, 246, "%s "% (pk.barang.get_kondisi_layar_display())) #LAYAR
        c.drawString(400, 236, "6.Password")
        c.drawString(460, 236, "%s "% (pk.barang.password_barang ))  #PASSWORD
        c.drawString(400, 226, "7.Dus")
        c.drawString(460, 226, "%s "% (pk.barang.get_dus_display())) #DUS
        c.drawString(400, 216, "8.Tas")
        c.drawString(460, 216, "%s "% (pk.barang.get_tas_display()))#TAS

    elif pk.barang.jenis_barang == u'3':###('3','KAMERA'),
        c.drawString(280, 256, "Kelengkapan :")
        c.drawString(280, 246, "1.Lensa")
        c.drawString(335, 246, "%s "% (pk.barang.get_kondisi_lensa_display()))
        c.drawString(280, 236, "2.Baterai")
        c.drawString(335, 236, "%s "% (pk.barang.get_kondisi_batre_kamera_display()))
        c.drawString(280, 226, "3.Cassing")
        c.drawString(335, 226, "%s "% (pk.barang.get_kondisi_cassing_kamera_display()))
        c.drawString(280, 216, "4.Dus")
        c.drawString(335, 216, "%s "% (pk.barang.get_dus_display()))

        c.drawString(420, 246, "5.Tas")
        c.drawString(460, 246, "%s "% (pk.barang.get_tas_display()))

    elif pk.barang.jenis_barang == u'4':###('4','PS'),
        c.drawString(280, 256, "Kelengkapan :")
        c.drawString(280, 246, "1.Optik")
        c.drawString(335, 246, "%s "% (pk.barang.get_kondisi_optik_ps_display()))
        c.drawString(280, 236, "2.Stick")
        c.drawString(335, 236, "%s "% (pk.barang.get_kondisi_stick_display()))
        c.drawString(280, 226, "3.HDMI")
        c.drawString(335, 226, "%s "% (pk.barang.get_kondisi_hdmi_display())) 
        c.drawString(280, 216, "4.Harddisk")
        c.drawString(335, 216, "%s "% (pk.barang.get_kondisi_harddisk_display()))

        c.drawString(420, 246, "5.Dus")
        c.drawString(460, 246, "%s "% (pk.barang.get_dus_display()))
        c.drawString(420, 236, "6.Tas")
        c.drawString(460, 236, "%s "% (pk.barang.get_tas_display()))

    elif pk.barang.jenis_barang == u'5':###('5','TV LCD'),
        c.drawString(280, 256, "Kelengkapan :")
        c.drawString(280, 246, "1.Layar")
        c.drawString(335, 246, "%s "% (pk.barang.get_kondisi_layar_tv_display()))
        c.drawString(280, 236, "2.Remote")
        c.drawString(335, 236, "%s "% (pk.barang.get_kondisi_remote_display()))
        c.drawString(280, 226, "3. Dus")
        c.drawString(335, 226, "%s "% (pk.barang.get_dus_display()))
        c.drawString(280, 216, "4.Tas")
        c.drawString(335, 216, "%s "% (pk.barang.get_tas_display()))

    elif pk.barang.jenis_kendaraan == u'1':###('6','MOTOR'),
        c.drawString(280, 256, "Kelengkapan :")
        c.drawString(280, 246, "1.Bpkb")
        c.drawString(390, 246, "%s "% (pk.barang.get_bpkb_display()))
        c.drawString(280, 236, "2.Stnk")
        c.drawString(390, 236, "%s "% (pk.barang.get_stnk_display()))
        c.drawString(280, 226, "3.Faktur")
        c.drawString(390, 226, "%s "% (pk.barang.get_faktur_display()))
        c.drawString(280, 216, "4.Gesek No Mesin")
        c.drawString(390, 216, "%s "% (pk.barang.get_gesek_nomesin_display()))
        c.drawString(280, 206, "5.Gesek No Rangka")
        c.drawString(390, 206, "%s "% (pk.barang.get_gesek_norangka_display()))

    elif pk.barang.jenis_kendaraan == u'2':###('7','Mobil'),
        c.drawString(280, 256, "Kelengkapan :")
        c.drawString(280, 246, "1.Bpkb")
        c.drawString(390, 246, "%s "% (pk.barang.get_bpkb_display()))
        c.drawString(280, 236, "2.Stnk")
        c.drawString(390, 236, "%s "% (pk.barang.get_stnk_display()))
        c.drawString(280, 226, "3.Faktur")
        c.drawString(390, 226, "%s "% (pk.barang.get_faktur_display()))
        c.drawString(280, 216, "4.Gesek No Mesin")
        c.drawString(390, 216, "%s "% (pk.barang.get_gesek_nomesin_display()))
        c.drawString(280, 206, "5.Gesek No Rangka")
        c.drawString(390, 206, "%s "% (pk.barang.get_gesek_norangka_display()))
    c.setFont("Courier", 6)
    c.drawString(20, 56, "SBG Sah dan mengikat setelah ditandatangani oleh Para Pihak" ) 
    c.showPage()


    ###KOTAK Perjanjian Utang Piutang Dengan Jaminan Gadai
    c.setFillColorRGB(255,255,255)
    c.rect(0.2*inch,7.2*inch,9*inch,5.7*inch, fill=1)
    ###KOTAK KUASA MENJUAL
    #c.rect(0.2*inch,10.9*inch,2*inch,2.0*inch, fill=1)
    c.rect(0.2*inch,11.4*inch,2*inch,1.5*inch, fill=1)
    ###KOTAK PEMBERIAN KUASA
    c.rect(0.2*inch,7.9*inch,2*inch,3.5*inch, fill=1)
    ###KOTAK BUKTI Penyerahan
    c.rect(0.2*inch,7.2*inch,2*inch,1*inch, fill=1)
    c.setFillColorRGB(0,0,0)

    c.setFont("Courier-Bold", 8)
    c.drawString(55, 920, "KUASA MENJUAL")
    c.setFont("Courier", 6)
    c.drawString(18, 913, "Hak untuk menjual barang jaminan  yang")
    c.drawString(18, 906, "telah lewat jatuh tempo. Saya serahkan")
    c.drawString(18, 899, "kepada PT. Gadai Solusi Bersama.")
    c.drawString(18, 892, "Pemberi Kuasa Menjual :")
    c.drawString(18, 878, "Nama"); 
    c.drawString(50, 878, ": ............")
    c.drawString(18, 864, "No Telp"); 
    c.drawString(50, 864, ": ............")
    c.drawString(18, 850, "Alamat"); 
    c.drawString(50, 850, ": ............")
    c.drawString(18, 829, "( %s )" %(pk.agnasabah.nama)); y -=2*y1
    c.setFont("Courier-Bold", 8)
    c.drawString(55, 813, "PEMBERIAN KUASA"); y -=y1
    c.setFont("Courier", 6)
    c.drawString(18, 799, "Pada Tanggal :"); y -=2*y1
    c.drawString(18, 785, ".................................."); y -=2*y1
    c.drawString(18, 771, "Dengan ini saya memberikan kuasa untuk"); y -=y1
    c.drawString(18, 757, "Gadai  Ulang / Top Up Pinjaman / Cicil"); y -=y1
    c.drawString(18, 743, "Pokok Pinjaman/ Pelunasan dan Menerima"); y -=y1
    c.drawString(18, 729, "Barang  Jaminan*)  /  pengambilan uang"); y -=y1
    c.drawString(18, 715, "kelebihan *) kepada :"); y -=2.5*y1
    c.drawString(18, 701, "Nama"); 
    c.drawString(50, 701, ": ............"); y -=2*y1
    c.drawString(18, 687, "Alamat");
    c.drawString(50, 687, ": ............"); y -=2*y1
    c.drawString(18, 673, "No KTP"); 
    c.drawString(50, 673, ": ............"); y -=2*y1

    c.drawString(18, 659, "Pemberi Kuasa"); 
    c.drawString(75, 659, "Penerima Kuasa"); y -=3*y1

    c.drawString(18, 615, "..............."); 
    c.drawString(75, 615, "..............."); y -=2*y1
    c.drawString(18, 605, "*) konfirmasi kepada nasabah dan coret"); y -=y1	
    c.drawString(18, 595, "yang tidak perlu"); y -=1.5*y1	

    c.drawString(50, 580, "BUKTI PENYERAHAN BARANG"); y -=y1
    c.drawString(50, 572, "JAMINAN/ UANG KELEBIHAN"); y -=6*y1
    c.drawString(50, 535, "( %s )" %(pk.agnasabah.nama)); y -=y1
    c.drawString(50, 525, "Nasabah Penerima Kuasa"); y -=y1

    c.setFont("Courier-Bold", 10)
    c.drawString(305, 920, "Perjanjian Utang Piutang Dengan Jaminan Gadai"); y -=y1
    c.setFont("Courier", 7)
    c.drawString(160, 906, "Kami yang bertandatangan dibawah Surat Bukti Gadai (SBG) ini, yakni PT.GADAI SOLUSI BERSAMA dan Nasabah (pemilik barang"); y -=y1
    c.drawString(160, 899, "jaminan atau kuasa dari pemilik barang jaminan) sepakat membuat perjanjian sebagai berikut :"); y -=y1
    c.drawString(160, 885, "1. Barang yang diserahkan sebagai jaminan adalah milik Nasabah dan/atau kepemilikan  sebagaimana pasal 1977 KUH Per dan"); y -=y1
    c.drawString(160, 878, "   menjamin  bukan berasal dari  hasil kejahatan, tidak dalam  obyek sengketa  dan/atau sita jaminan. Barang asli bukan"); y -=y1
    c.drawString(160, 871, "   replika, tiruan dan/atau palsu."); y -=y1

    c.drawString(160, 862, "2. Nasabah  menyatakan telah berutang kepada PT. GADAI SOLUSI BERSAMA  dan  berkewajiban untuk membayar Pelunasan Uang"); y -=y1
    c.drawString(160, 848, "   Pinjaman ditambah jasa sebesar  tarif yang  berlaku di PT. GADAI SOLUSI BERSAMA, dan biaya proses lelang (jika ada),"); y -=y1
    c.drawString(160, 841, "   biaya keterlambatan pembayaran."); y -=y1

    c.drawString(160, 832, "3. Nasabah menerima  dan  setuju  terhadap  uraian  barang  jaminan, penetapan  besarnya taksiran  barang jaminan, uang"); y -=y1
    c.drawString(160, 825, "   pinjaman, tarif jasa, biaya  administrasi  dan  biaya  simpan sebagaimana yang dimaksud pada Surat Bukti Gadai (SBG)"); y -=y1
    c.drawString(160, 818, "   dan sebagai tanda bukti yang sah penerimaan uang pinjaman."); y -=y1

    c.drawString(160, 809, "4. Nasabah dapat melakukan Gadai Ulang, selama nilai taksiran masih  memenuhi syarat dengan memperhitungkan jasa, biaya"); y -=y1
    c.drawString(160, 802, "   administrasi dan biaya simpan yang masih akan dibayar.Jika terjadi penurunan nilai Taksiran Barang Jaminan pada saat"); y -=y1
    c.drawString(160, 795, "   Gadai Ulang, maka nasabah wajib mengangsur uang pinjaman."); y -=y1

    c.drawString(160, 786, "5. Apabila terjadi keterlambatan pada  saat dilakukan pelunasan oleh nasabah,maka nasabah harus membayar biaya keterlam"); y -=y1
    c.drawString(160, 779, "   batan yang ditetapkan oleh PT. GADAI SOLUSI BERSAMA."); y -=y1

    c.drawString(160, 770, "6. Nasabah dapat  datang sendiri untuk  melakukan gadai ulang, mengangsur  uang pinjaman, pelunasan dan menerima barang"); y -=y1
    c.drawString(160, 763, "   jaminan dan menerima uang kelebihan lelang atau  dengan memberikan kuasa kepada  orang lain dengan mengisi dan membu"); y -=y1
    c.drawString(160, 756, "   buhkan tanda tangan pada  kolom yang tersedia, dengan  melampirkan foto  copy KTP  Nasabah dan  penerima kuasa serta"); y -=y1
    c.drawString(160, 749, "   menunjukkan asli KTP Penerima kuasa."); y -=y1

    c.drawString(160, 740, "7. Pengembalian  barang jaminan  nasabah wajib  menyampaikan pemberitahuan  kepada petugas  gerai tempat dimana nasabah "); y -=y1
    c.drawString(160, 733, "   melakukan transaksi pinjaman, paling lambat 1 (satu) hari sebelum pelunasan dilakukan."); y -=y1

    c.drawString(160, 724, "8. Pinjaman yang telah jatuh tempo, PT. Gadai Solusi Bersama akan menyampaikan pemberitahuan secara layak, baik melalui"); y -=y1
    c.drawString(160, 717, "   surat atau  media lainnya  ke alamat / nomor kontak  yang  dicantumkan  nasabah sesuai Surat Bukti Gadai ini untuk"); y -=y1
    c.drawString(160, 710, "   segera melunasi pokok pinjaman beserta denda/ biaya lain yang ditetapkan oleh pihak PT. Gadai Solusi Bersama."); y -=y1

    c.drawString(160, 701, "9. Apabila sampai dengan tanggal Jatuh Tempo tidak  dilakukan Pelunasan atau Gadai Ulang, maka PT. GADAI SOLUSI BERSAMA"); y -=y1
    c.drawString(160, 694, "   berhak melakukan penjualan Barang Jaminan melalui Lelang.Barang Jaminan dapat dijual dengan cara nasabah menjual sen "); y -=y1
    c.drawString(160, 687, "   diri Barang Jaminannya,atau nasabah memberikan kuasa kepada perusahaan pergadaian untuk menjualkan Barang Jaminannya."); y -=y1

    c.drawString(160, 678, "10.Hasil  penjualan lelang barang jaminan setelah dikurangi uang pinjaman,jasa, biaya administrasi, biaya simpan, denda"); y -=y1
    c.drawString(160, 671, "   keterlambatan, biaya proses lelang  (bila ada) dan bea  lelang, merupakan kelebihan yang menjadi hak nasabah. Jangka"); y -=y1
    c.drawString(160, 664, "   waktu  pengambilan uang  kelebihan lelang selama  satu tahun sejak  tanggal lelang, dan jika lewat waktu dari jangka"); y -=y1
    c.drawString(160, 657, "   waktu pengambilan uang kelebihan, nasabah menyatakan setuju untuk menyalurkan uang  kelebihan tersebut  sebagai dana"); y -=y1
    c.drawString(160, 651, "   kepedulian sosial yang pelaksanannya diserahkan kepada PT.  GADAI SOLUSI BERSAMA. "); y -=y1#Jika hasil penjualan barang lelang"); y -=y1
  
    c.drawString(160, 642, "11.Bilamana  nasabah  meninggal  dunia dan  terdapat hak  dan kewajiban  terhadap PT. GADAI SOLUSI BERSAMA ataupun seba"); y -=y1
    c.drawString(160, 635, "   liknya, maka hak  dan kewajiban  dibebankan  kepada  ahli waris nasabah  sesuai  dengan ketentuan waris dalam  hukum");y -=y1
    c.drawString(160, 628, "   Republik Indonesia."); y -=y1

    c.drawString(160, 619, "12.PT. GADAI SOLUSI BERSAMA  akan  memberikan  ganti  kerugian  apabila  barang  jaminan  yang  berada dalam penguasaan "); y -=y1
    c.drawString(160, 612, "   PT. GADAI SOLUSI BERSAMA  mengalami  kerusakan atau  hilang yang tidak  disebabkan oleh  suatu  bencana  alam (Force  "); y -=y1
    c.drawString(160, 605, "   Majeure) yang ditetapkan pemerintah.Ganti rugi diberikan setelah diperhitungkan dengan Uang Pinjaman dan penggantian"); y -=y1
    c.drawString(160, 598, "   berupa uang atau barang yang nilainya maksimal sama atau setara dengan barang jaminan saat terjadinya kerusakan atau "); y -=y1
    c.drawString(160, 591, "   kehilangan atau pada saat barang tersebut dijaminkan."); y -=y1

    c.drawString(160, 582, "13.Nasabah menyatakan  telah  membaca  dan memahami  isi perjanjian ini serta tunduk dan mengikuti terhadap aturan yang "); y -=y1
    c.drawString(160, 575, "   tertuang dalam Surat Bukti Gadai  ini.  "); y -=y1

    c.drawString(160, 566, "14.PT. GADAI SOLUSI BERSAMA bersedia  menerima dan menyelesaikan setiap  bentuk pengaduan dan sengketa, apabila terjadi"); y -=y1
    c.drawString(160, 559, "   perselisihan dikemudian  hari  akan  diselesaikan secara musyawarah  untuk mufakat dan apabila tidak tercapai kesepa "); y -=y1
    c.drawString(160, 552, "   katan akan diselesaikan melalui pengadilan negeri setempat."); y -=y1

    c.drawString(160, 538, "Demikian perjanjian ini berlaku dan mengikat PT. GADAI SOLUSI BERSAMA  dengan Nasabah sejak Surat Bukti Gadai ini ditan"); y -=y1
    c.drawString(160, 531, "datangani oleh kedua belah pihak pada kolom yang tersedia di bagian depan."); y -=y1

    ##--------##
    ###KOTAK Perjanjian Utang Piutang Dengan Jaminan Gadai
    c.setFillColorRGB(255,255,255)
    c.rect(0.2*inch,0.64*inch,9*inch,5.74*inch, fill=1)
    #c.rect(0.2*inch,-0.2*inch,9*inch,7.2*inch, fill=1)

    ###KOTAK KUASA MENJUAL
    c.rect(0.2*inch,4.88*inch,2*inch,1.5*inch, fill=1)
    ###KOTAK PEMBERIAN KUASA
    c.rect(0.2*inch,1.4*inch,2*inch,3.5*inch, fill=1)
    ###KOTAK BUKTI Penyerahan
    c.rect(0.2*inch,0.64*inch,2*inch,1.2*inch, fill=1)
    c.setFillColorRGB(0,0,0)

    c.setFont("Courier-Bold", 8)
    c.drawString(55, 451, "KUASA MENJUAL")
    c.setFont("Courier", 6)
    c.drawString(18, 444, "Hak untuk menjual barang jaminan  yang")
    c.drawString(18, 437, "telah lewat jatuh tempo. Saya serahkan")
    c.drawString(18, 430, "kepada PT. Gadai Solusi Bersama.")
    c.drawString(18, 423, "Pemberi Kuasa Menjual :")
    c.drawString(18, 409, "Nama"); 
    c.drawString(50, 409, ": ............")
    c.drawString(18, 395, "No Telp"); 
    c.drawString(50, 395, ": ............")
    c.drawString(18, 381, "Alamat"); 
    c.drawString(50, 381, ": ............")
    c.drawString(18, 360, "( %s )" %(pk.agnasabah.nama)); y -=2*y1
    c.setFont("Courier-Bold", 8)
    c.drawString(55, 344, "PEMBERIAN KUASA"); y -=y1
    c.setFont("Courier", 6)
    c.drawString(18, 330, "Pada Tanggal :"); y -=2*y1
    c.drawString(18, 316, ".................................."); y -=2*y1
    c.drawString(18, 302, "Dengan ini saya memberikan kuasa untuk"); y -=y1
    c.drawString(18, 288, "Gadai  Ulang / Top Up Pinjaman / Cicil"); y -=y1
    c.drawString(18, 274, "Pokok Pinjaman/ Pelunasan dan Menerima"); y -=y1
    c.drawString(18, 260, "Barang  Jaminan*)  /  pengambilan uang"); y -=y1
    c.drawString(18, 246, "kelebihan *) kepada :"); y -=2.5*y1
    c.drawString(18, 232, "Nama"); 
    c.drawString(50, 232, ": ............"); y -=2*y1
    c.drawString(18, 218, "Alamat");
    c.drawString(50, 218, ": ............"); y -=2*y1
    c.drawString(18, 204, "No KTP"); 
    c.drawString(50, 204, ": ............"); y -=2*y1

    c.drawString(18, 190, "Pemberi Kuasa"); 
    c.drawString(75, 190, "Penerima Kuasa"); y -=3*y1

    c.drawString(18, 156, "..............."); 
    c.drawString(75, 156, "..............."); y -=2*y1
    c.drawString(18, 146, "*) konfirmasi kepada nasabah dan coret"); y -=y1	
    c.drawString(18, 136, "yang tidak perlu"); y -=1.5*y1	

    c.drawString(50, 121, "BUKTI PENYERAHAN BARANG"); y -=y1
    c.drawString(50, 113, "JAMINAN/ UANG KELEBIHAN"); y -=6*y1
    c.drawString(50, 76, "( %s )" %(pk.agnasabah.nama)); y -=y1
    c.drawString(50, 66, "Nasabah Penerima Kuasa"); y -=y1

    c.setFont("Courier-Bold", 10)
    c.drawString(305, 451, "Perjanjian Utang Piutang Dengan Jaminan Gadai"); y -=y1
    c.setFont("Courier", 7)
    c.drawString(160, 437, "Kami yang bertandatangan dibawah Surat Bukti Gadai (SBG) ini, yakni PT.GADAI SOLUSI BERSAMA dan Nasabah (pemilik barang"); y -=y1
    c.drawString(160, 430, "jaminan atau kuasa dari pemilik barang jaminan) sepakat membuat perjanjian sebagai berikut :"); y -=y1
    c.drawString(160, 416, "1. Barang yang diserahkan sebagai jaminan adalah milik Nasabah dan/atau kepemilikan  sebagaimana pasal 1977 KUH Per dan"); y -=y1
    c.drawString(160, 409, "   menjamin  bukan berasal dari  hasil kejahatan, tidak dalam  obyek sengketa  dan/atau sita jaminan. Barang asli bukan"); y -=y1
    c.drawString(160, 402, "   replika, tiruan dan/atau palsu."); y -=y1

    c.drawString(160, 393, "2. Nasabah  menyatakan telah berutang kepada PT. GADAI SOLUSI BERSAMA  dan  berkewajiban untuk membayar Pelunasan Uang"); y -=y1
    c.drawString(160, 386, "   Pinjaman ditambah jasa sebesar  tarif yang  berlaku di PT. GADAI SOLUSI BERSAMA, dan biaya proses lelang (jika ada),"); y -=y1
    c.drawString(160, 379, "   biaya keterlambatan pembayaran."); y -=y1

    c.drawString(160, 370, "3. Nasabah menerima  dan  setuju  terhadap  uraian  barang  jaminan, penetapan  besarnya taksiran  barang jaminan, uang"); y -=y1
    c.drawString(160, 363, "   pinjaman, tarif jasa, biaya  administrasi  dan  biaya  simpan sebagaimana yang dimaksud pada Surat Bukti Gadai (SBG)"); y -=y1
    c.drawString(160, 356, "   dan sebagai tanda bukti yang sah penerimaan uang pinjaman."); y -=y1

    c.drawString(160, 347, "4. Nasabah dapat melakukan Gadai Ulang, selama nilai taksiran masih  memenuhi syarat dengan memperhitungkan jasa, biaya"); y -=y1
    c.drawString(160, 340, "   administrasi dan biaya simpan yang masih akan dibayar.Jika terjadi penurunan nilai Taksiran Barang Jaminan pada saat"); y -=y1
    c.drawString(160, 333, "   Gadai Ulang, maka nasabah wajib mengangsur uang pinjaman."); y -=y1

    c.drawString(160, 324, "5. Apabila terjadi keterlambatan pada  saat dilakukan pelunasan oleh nasabah,maka nasabah harus membayar biaya keterlam"); y -=y1
    c.drawString(160, 317, "   batan yang ditetapkan oleh PT. GADAI SOLUSI BERSAMA."); y -=y1

    c.drawString(160, 308, "6. Nasabah dapat  datang sendiri untuk  melakukan gadai ulang, mengangsur  uang pinjaman, pelunasan dan menerima barang"); y -=y1
    c.drawString(160, 301, "   jaminan dan menerima uang kelebihan lelang atau  dengan memberikan kuasa kepada  orang lain dengan mengisi dan membu"); y -=y1
    c.drawString(160, 294, "   buhkan tanda tangan pada  kolom yang tersedia, dengan  melampirkan foto  copy KTP  Nasabah dan  penerima kuasa serta"); y -=y1
    c.drawString(160, 287, "   menunjukkan asli KTP Penerima kuasa."); y -=y1

    c.drawString(160, 278, "7. Pengembalian  barang jaminan  nasabah wajib  menyampaikan pemberitahuan  kepada petugas  gerai tempat dimana nasabah "); y -=y1
    c.drawString(160, 271, "   melakukan transaksi pinjaman, paling lambat 1 (satu) hari sebelum pelunasan dilakukan."); y -=y1

    c.drawString(160, 262, "8. Pinjaman yang telah jatuh tempo, PT. Gadai Solusi Bersama akan menyampaikan pemberitahuan secara layak, baik melalui"); y -=y1
    c.drawString(160, 255, "   surat atau  media lainnya  ke alamat / nomor kontak  yang  dicantumkan  nasabah sesuai Surat Bukti Gadai ini untuk"); y -=y1
    c.drawString(160, 248, "   segera melunasi pokok pinjaman beserta denda/ biaya lain yang ditetapkan oleh pihak PT. Gadai Solusi Bersama."); y -=y1

    c.drawString(160, 239, "9. Apabila sampai dengan tanggal Jatuh Tempo tidak  dilakukan Pelunasan atau Gadai Ulang, maka PT. GADAI SOLUSI BERSAMA"); y -=y1
    c.drawString(160, 232, "   berhak melakukan penjualan Barang Jaminan melalui Lelang.Barang Jaminan dapat dijual dengan cara nasabah menjual sen "); y -=y1
    c.drawString(160, 225, "   diri Barang Jaminannya,atau nasabah memberikan kuasa kepada perusahaan pergadaian untuk menjualkan Barang Jaminannya."); y -=y1

    c.drawString(160, 216, "10.Hasil  penjualan lelang barang jaminan setelah dikurangi uang pinjaman,jasa, biaya administrasi, biaya simpan, denda"); y -=y1
    c.drawString(160, 209, "   keterlambatan, biaya proses lelang  (bila ada) dan bea  lelang, merupakan kelebihan yang menjadi hak nasabah. Jangka"); y -=y1
    c.drawString(160, 202, "   waktu  pengambilan uang  kelebihan lelang selama  satu tahun sejak  tanggal lelang, dan jika lewat waktu dari jangka"); y -=y1
    c.drawString(160, 195, "   waktu pengambilan uang kelebihan, nasabah menyatakan setuju untuk menyalurkan uang  kelebihan tersebut  sebagai dana"); y -=y1
    c.drawString(160, 186, "   kepedulian sosial yang pelaksanannya diserahkan kepada PT.  GADAI SOLUSI BERSAMA. "); y -=y1#Jika hasil penjualan barang lelang"); y -=y1
  
    c.drawString(160, 177, "11.Bilamana  nasabah  meninggal  dunia dan  terdapat hak  dan kewajiban  terhadap PT. GADAI SOLUSI BERSAMA ataupun seba"); y -=y1
    c.drawString(160, 170, "   liknya, maka hak  dan kewajiban  dibebankan  kepada  ahli waris nasabah  sesuai  dengan ketentuan waris dalam  hukum");y -=y1
    c.drawString(160, 163, "   Republik Indonesia."); y -=y1

    c.drawString(160, 154, "12.PT. GADAI SOLUSI BERSAMA  akan  memberikan  ganti  kerugian  apabila  barang  jaminan  yang  berada dalam penguasaan "); y -=y1
    c.drawString(160, 147, "   PT. GADAI SOLUSI BERSAMA  mengalami  kerusakan atau  hilang yang tidak  disebabkan oleh  suatu  bencana  alam (Force  "); y -=y1
    c.drawString(160, 140, "   Majeure) yang ditetapkan pemerintah.Ganti rugi diberikan setelah diperhitungkan dengan Uang Pinjaman dan penggantian"); y -=y1
    c.drawString(160, 133, "   berupa uang atau barang yang nilainya maksimal sama atau setara dengan barang jaminan saat terjadinya kerusakan atau "); y -=y1
    c.drawString(160, 126, "   kehilangan atau pada saat barang tersebut dijaminkan."); y -=y1

    c.drawString(160, 117, "13.Nasabah menyatakan  telah  membaca  dan memahami  isi perjanjian ini serta tunduk dan mengikuti terhadap aturan yang "); y -=y1
    c.drawString(160, 110, "   tertuang dalam Surat Bukti Gadai  ini.  "); y -=y1

    c.drawString(160, 101, "14.PT. GADAI SOLUSI BERSAMA bersedia  menerima dan menyelesaikan setiap  bentuk pengaduan dan sengketa, apabila terjadi"); y -=y1
    c.drawString(160, 92, "   perselisihan dikemudian  hari  akan  diselesaikan secara musyawarah  untuk mufakat dan apabila tidak tercapai kesepa "); y -=y1
    c.drawString(160, 85, "   katan akan diselesaikan melalui pengadilan negeri setempat."); y -=y1

    c.drawString(160, 71, "Demikian perjanjian ini berlaku dan mengikat PT. GADAI SOLUSI BERSAMA  dengan Nasabah sejak Surat Bukti Gadai ini ditan"); y -=y1
    c.drawString(160, 64, "datangani oleh kedua belah pihak pada kolom yang tersedia di bagian depan."); y -=y1

    c.showPage()
    c.save()
    return response


@login_required
@user_passes_test(lambda u: u.groups.filter(name='ADM_GERAI'))
def upload_pk(request,object_id):
    n = AkadGadai.objects.get(pk = object_id)
    user = request.user
    D = decimal.Decimal
    if request.method == "POST":
        form = UploadPKForm(request.POST,request.FILES)
        if form.is_valid():
            berkas_pk = form.cleaned_data['berkas_pk']
            request.FILES['berkas_pk'].name = n.norek() + '_' + n.agnasabah.nama + '_' +  request.FILES['berkas_pk'].name
            berkas = UploadPk(upload=n, berkas_pk=request.FILES['berkas_pk'])
            berkas.save()
            messages.add_message(request, messages.INFO, 'PK Telah Di Upload')
            return HttpResponseRedirect('/')
    else:
        form = UploadPKForm(initial={'upload':n})
    variables = RequestContext(request, {'form': form,'n':n})
    return render_to_response('akadgadai/upload_pk.html', variables)

@login_required
def cari_sop(request):
    form = PencarianSopForm()
    if 'cari' in request.GET and 'submit_satu' in request.GET :
        cari = request.GET['cari']

        ledger_search = BerkasSop.objects.filter(agsop__pk = cari).order_by('no_urut')
        #tb = ([ o for o in tb1 if o.date_date_cuy()==True])
        cari = cari
        template='akadgadai/sop_show.html'
        variable = RequestContext(request,{'ledger_search':ledger_search,})
        return render_to_response(template,variable)
    else:
        variables = RequestContext(request, {'form': form})
        return render_to_response('akadgadai/pencarian_sop.html', variables)

@login_required
def tambah_sop(request):
    user = request.user
    D = decimal.Decimal
    if request.method == "POST":
        form = TambahSopForm(request.POST,request.FILES)
        if form.is_valid():
            judul_sop = form.cleaned_data['judul_sop']
            tanggal_sop = form.cleaned_data['tanggal_sop']
            status_sop = form.cleaned_data['status_sop']

            gambar = form.cleaned_data['gambar']
            judul = form.cleaned_data['judul']
            deskripsi = form.cleaned_data['deskripsi']
            no_urut = form.cleaned_data['no_urut']
            tanggal = form.cleaned_data['tanggal']
            status = form.cleaned_data['status']
                
            sop = Master_Sop(judul_sop = judul_sop, tanggal_sop = tanggal_sop, status_sop = status_sop)
            sop.save()
            request.FILES['gambar'].name = judul + request.FILES['gambar'].name
            berkas = BerkasSop(agsop=sop, judul = judul,deskripsi = deskripsi, no_urut = no_urut, tanggal = tanggal, status = status, gambar=request.FILES['gambar'])
            berkas.save()

            messages.add_message(request, messages.INFO, 'Sop Telah tersimpan')
            return HttpResponseRedirect('/')

    else:
        form  = TambahSopForm()
        #form.fields['gerai'].queryset = Tbl_Cabang.objects.for_user(user) 
    variables = RequestContext(request, {'form': form})
    return render_to_response('akadgadai/tambah_sop_baru.html', variables)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='manop'))
def hapus_dobel(request,object_id):
    a = AkadGadai.objects.get(id=object_id)
    n = KasirGeraiPelunasan.objects.get(kasir_lunas=a)
    template= 'akadgadai/hapus_dobel.html'
    variable = RequestContext(request,{'n': n})
    return render_to_response(template,variable)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='manop'))
def eksekusi_hapus_dobel(request,object_id):
    a = AkadGadai.objects.get(id=object_id)
    n = KasirGeraiPelunasan.objects.get(kasir_lunas = a)
    n.delete()
    messages.add_message(request, messages.INFO, 'Kasir Pelunasan Telah Terhapus')
    return HttpResponseRedirect("/akadgadai/%s/show/" % a.id)

@login_required
def export_saldo(request):
    ''' Tampilkan Akad pada bulan/tahun terpilih dalam format CSV '''
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=SALDO.csv'
    writer = csv.writer(response)
    kemarin = datetime.date(2016,10,01)
    #sekarang = datetime.date(2015,01,31)
    writer.writerow(['id','Coa','Saldo'])
    for p in Tbl_TransaksiKeu.objects.all().filter(tgl_trans= kemarin):
        writer.writerow([p.id,p.id_coa,p.saldo])

    return response

@login_required
def delete_akad(request, object_id):
    ag = AkadGadai.objects.get(id=object_id)
    jurnal = Jurnal.objects.filter(nobukti = ag.norek)
    jurnal.delete()
    materai = Biaya_Materai_Cab.objects.filter(norek = ag.norek)
    materai.delete()
    ag.delete() 
    messages.add_message(request, messages.INFO, 'AKAD GADAI TELAH TERHAPUS')
    return HttpResponseRedirect(ag.get_absolute_url_delete())

@login_required
def tampil_kondisi_barang(request, object_id):
    barang = AkadGadai.objects.get(id=object_id)
    barang.status_kondisi_barang = 1
    barang.save()
    variables = RequestContext(request, {'barang': barang})
    return render_to_response('akadgadai/kondisi_barang.html', variables)

##### IMPORT AKADGADAI ALL JURNALL #####
@login_required
class UploadAkadForm(forms.Form):
    ag_file = forms.FileField()

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('manop','asmanpjb')))
def view_verifikasi_manop(request, object_id):
    ag = AkadGadai.objects.get(id=object_id)
    a = datetime.date.today()
    form = Verifikasi_ManOpForm(initial={'manop': ag.id,'tanggal': a})
    form.fields['manop'].widget = forms.HiddenInput()

    template = 'manop/verifikasi_manop.html'
    variable = RequestContext(request, {
        'ag': ag,
        'form': form})
    return render_to_response(template,variable) 
    
@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('manop','asmanpjb')))
def verifikasi_manop(request, object_id):
    ag = AkadGadai.objects.get(id=object_id)
    if request.method == 'POST':
        f = Verifikasi_ManOpForm(request.POST)
        if f.is_valid():
            manop = f.cleaned_data['manop']   
            tanggal = f.cleaned_data['tanggal']
            status = f.cleaned_data['status']
            note = f.cleaned_data['note']
            f = ManopGadai(manop=ag, tanggal=tanggal, status=status, note = note)
            f.save()
            if f.status == '1':
                ag.status_taksir = 1
                ag.save()
                messages.add_message(request, messages.INFO,'### PENGAJUAN DITERIMA ###')    
            else: 
                ag.status_taksir = 2
                ag.save()    
                messages.add_message(request, messages.INFO,'### PENGAJUAN DITOLAK ###')                
        return HttpResponseRedirect('/manop/')
    else:
        variables = RequestContext(request, {'object': ag, 'form': f})
        return render_to_response('manop/verifikasi_manop.html', variables)

@login_required
def import_ag(request):
    if request.method != 'POST':
        messages.add_message(request, messages.INFO,"Bukan POST.")
        return HttpResponseRedirect('/')
    else:
        form = UploadAkadForm(request.POST, request.FILES)
        if 1:
            reader = csv.reader(request.FILES['ag_file'])
            out = 0
            for row in reader:
                (nama, tgl_lahir,tempat, no_ktp, alamat_ktp,  rt_ktp,rw_ktp, telepon_ktp,hp_ktp,kelurahan_ktp,kecamatan_ktp,\
                    jenis_pekerjaan,alamat_kantor,kode_pos,telepon_kantor,\
                    email,jenis_kelamin,cdate,mdate, \
                    jenis_barang,merk,type,sn,warna, tahun_pembuatan,bulan_produksi,accesoris_barang1,lampiran_dokumen,\
                    jenis_kendaraan,merk_kendaraan,type_kendaraan,no_polisi,no_rangka,no_mesin,tahun_pembuatan_kendaraan,warna_kendaraan,\
                    no_bpkb,stnk_atas_nama,no_faktur,\
                    tanggal,gerai,nilai,jangka_waktu,jangka_waktu_kendaraan,bea_materai,jenis_transaksi,status_taksir,jatuhtempo,taksir) = row
                
                (tg, bl, th) = tgl_lahir.split('-')
                tlahir = datetime.date(int(tg), int(bl), int(th))
                try:
                    (nasabah, created) = Nasabah.objects.get_or_create(no_ktp=no_ktp, defaults={'nama':nama, 'tgl_lahir':tlahir,'tempat':tempat, 'no_ktp':no_ktp, 'alamat_ktp':alamat_ktp,\
                    'no_rumah_ktp':0,'rt_ktp':rt_ktp,'rw_ktp':rw_ktp,'telepon_ktp':telepon_ktp,'hp_ktp':hp_ktp, 'kelurahan_ktp':kelurahan_ktp,\
                    'kecamatan_ktp':kecamatan_ktp, 'kotamadya_ktp':0, 'kabupaten_ktp':0,\
                    'no_sim':0,'alamat_sim':0,\
                    'rt_sim':0,'rw_sim':0,'kelurahan_sim':0, 'kecamatan_sim':0, 'alamat_domisili':0,\
                    'no_rumah_domisili':0,'rt_domisili':0, 'rw_domisili':0,'telepon_domisili':0,\
                    'hp_domisili':0,'kelurahan_domisili':0,'kecamatan_domisili':0,'kotamadya_domisili':0, \
                    'kabupaten_domisili':0,
                    'jenis_pekerjaan':jenis_pekerjaan,'alamat_kantor':alamat_kantor,'kode_pos':kode_pos, \
                    'telepon_kantor':telepon_kantor,'email':email,'jenis_kelamin':jenis_kelamin,'cdate':cdate,'mdate':mdate})
                    
                except Nasabah.MultipleObjectsReturned:
                    nasabah = Nasabah.objects.filter(no_ktp=no_ktp)[0]
                (barang, created) = Barang.objects.get_or_create(jenis_barang=jenis_barang, merk = merk, type= type,sn= sn, tahun_pembuatan= tahun_pembuatan, \
                bulan_produksi=bulan_produksi, accesoris_barang1=accesoris_barang1, lampiran_dokumen =lampiran_dokumen,jenis_kendaraan =jenis_kendaraan, \
                merk_kendaraan = merk_kendaraan,type_kendaraan = type_kendaraan,no_polisi = no_polisi,no_rangka = no_rangka,no_mesin = no_mesin, \
                tahun_pembuatan_kendaraan = tahun_pembuatan_kendaraan,warna_kendaraan = warna_kendaraan,no_bpkb = no_bpkb,stnk_atas_nama = stnk_atas_nama, \
                no_faktur = no_faktur)                    
                (th,bl,tg) = tanggal.split('-')
                trx = datetime.date(int(th), int(bl), int(tg))
                (ts, created) = Taksir.objects.get_or_create(id=int(taksir))#, type = type, spesifikasi = spesifikasi,harga_baru = harga_baru, harga_pasar = harga_pasar, maxpinjaman = maxpinjaman, tglupdate = tglupdate)
                (kb, created) = Tbl_Cabang.objects.get_or_create(id=int(gerai), defaults={'nama': ''})
                nilai = float(nilai)
                (im, created) = AkadGadai.objects.get_or_create(agnasabah = nasabah ,barang =barang ,tanggal = trx,gerai = kb, nilai = nilai,jatuhtempo =jatuhtempo ,\
                    jangka_waktu =jangka_waktu , jangka_waktu_kendaraan = jangka_waktu_kendaraan,jenis_transaksi=jenis_transaksi,status_taksir=status_taksir,\
                    taksir = ts,nocoa_titipan ='21.05.01',nocoa_kas = '11.01.04')
                im.asumsi_jasa = im.asumsi_pendapatan_jasa()
                im.nilai_jasa = im.jasa
                im.nilai_jasa_kendaraan = im.jasa_kendaraan
                im.nilai_biayasimpan = im.biayasimpan
                im.nilai_beasimpan_kendaraan = im.beasimpan_kendaraan
                im.nilai_adm = im.adm
                im.nilai_adm_kendaraan = im.adm_kendaraan
                im.save()
                out += 1                
                jurnal_pencairan_import(im, request.user)
            messages.add_message(request, messages.INFO,"Sukses import data akad sebanyak %s" % out)
        else:
            messages.add_message(request, messages.INFO,"Form tidak valid.")
        return HttpResponseRedirect('/')

def jurnal_pencairan_import(im, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_pinjaman = get_object_or_404(Tbl_Akun, id=163L)
    a_pdp_adm = get_object_or_404(Tbl_Akun, id='430')
    a_pdp_jasa = get_object_or_404(Tbl_Akun, id='189')
    a_pdp_bea_simpan = get_object_or_404(Tbl_Akun, id='429')
   
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (im.norek_import(), im.agnasabah.nama),tgl_trans = im.tanggal,nobukti = im.norek_import())
    
    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pinjaman,
        debet = im.nilai,kredit = 0,
        deskripsi= 'Penc: NoRek: %s an: %s  ' % (im.norek_import(), im.agnasabah.nama),
        id_product = '4',status_jurnal ='1',id_cabang = im.gerai.kode_cabang,tgl_trans =im.tanggal,
        id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pdp_adm,
        debet = 0,kredit = im.adm_all(),
        deskripsi= 'Penc: NoRek: %s an: %s  ' % (im.norek_import(), im.agnasabah.nama),
        id_product = '4',status_jurnal ='1',id_cabang = im.gerai.kode_cabang,tgl_trans = im.tanggal,
        id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_jasa,tgl_trans =im.tanggal,
        debet = 0,kredit =  round(im.asumsi_pendapatan_jasa()),
        deskripsi= 'Penc: NoRek: %s an: %s  ' % (im.norek_import(), im.agnasabah.nama),
        id_product = '4',status_jurnal ='1',
        id_cabang =im.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_bea_simpan,
        debet = 0,kredit =  im.beasimpan_all(),
        deskripsi= 'Penc: NoRek: %s an: %s  ' % (im.norek_import(), im.agnasabah.nama),
        id_product = '4',status_jurnal ='1',id_cabang = im.gerai.kode_cabang,tgl_trans = im.tanggal,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_titipan_pencairan,
        deskripsi= 'Penc: NoRek: %s an: %s  ' % (im.norek_import(), im.agnasabah.nama),
        debet = 0 , kredit = im.nilai - im.adm_all() - round(im.asumsi_pendapatan_jasa()) - im.beasimpan_all(),
        id_product = '4',status_jurnal ='1',id_cabang = im.gerai.kode_cabang,tgl_trans = im.tanggal,
        id_unit= 300)
##### IMPORT AKADGADAI ALL JURNALL #####

### fungsi pelunasan gadai ###
'''
def batal_lunas(request, object_id):
    ag = AkadGadai.objects.get(id=object_id)     
    ag.lunas = None
    ag.status_transaksi = None
    ag.status_kwlunas = None
    ag.status_oto_plns = None
    ag.jasa_lunas = 0
    ag.denda_lunas = 0
    ag.terlambat = 0
    ag.jasa_kendaraan_lunas = 0
    ag.denda_kendaraan_lunas = 0
    ag.terlambat_kendaraan = 0
    ag.nilai_lunas = 0
    ag.save()
    tbl_pelunasan = ag.pelunasan_set.all()
    tbl_pelunasan.delete()       
    a = ag.kasirgeraipelunasan
    a.delete()
    #id_akad = ag.id
    #jurnal = Jurnal.objects.filter(object_id=id_akad).order_by('-id')
    #jrl = jurnal[0]
    jurnal = Jurnal.objects.filter(nobukti=ag.norek()).filter(diskripsi__icontains = 'Plns')
    jurnal.delete()
    jurnal1 = Jurnal.objects.filter(nobukti=ag.norek()).filter(diskripsi__icontains = 'Pelunasan')
    jurnal1.delete()
    if ag.manoppelunasan == None or ag.manoppelunasan == u'':
        b = ag.manoppelunasan 
        b.delete()
    messages.add_message(request, messages.INFO, 'Akadgadai no rek : %s BATAL lunas" % ag.norek()')
    return HttpResponseRedirect(ag.get_absolute_url())
'''
#####Batal Lunas Dan pembatalan Jurnal
@login_required
def batal_lunas(request, object_id):
    ag = AkadGadai.objects.get(id=object_id)
    sekarang = datetime.date.today()
    ag.lunas = None
    ag.status_transaksi = None
    ag.status_kwlunas = None
    ag.status_oto_plns = None
    ag.jasa_lunas = 0
    ag.denda_lunas = 0
    ag.terlambat = 0
    ag.jasa_kendaraan_lunas = 0
    ag.denda_kendaraan_lunas = 0
    ag.terlambat_kendaraan = 0
    ag.nilai_lunas = 0
    ag.barang.akad_ulang = 0
    ag.norek_lunas_sblm = None
    ag.save()
    tbl_pelunasan = ag.pelunasan_set.all()
    tbl_pelunasan.delete()       
    jurnal = Jurnal.objects.filter(nobukti=ag.norek()).filter(tgl_trans = sekarang).filter(diskripsi__icontains = 'Plns')
    jurnal.delete()
    jurnal1 = Jurnal.objects.filter(nobukti=ag.norek()).filter(tgl_trans = sekarang).filter(diskripsi__icontains = 'Pelunasan')
    jurnal1.delete()
    materai = Biaya_Materai_Cab.objects.filter(norek = ag.norek)
    materai.delete() 
    #if ag.manoppelunasan == None or ag.manoppelunasan == u'':
        #b = ag.manoppelunasan 
        #b.delete()
    messages.add_message(request, messages.INFO, 'Akadgadai no rek : %s BATAL lunas" % ag.norek()')
    return HttpResponseRedirect(ag.get_absolute_url())

### fungsi pelunasan gadai non GU ###
@login_required
def batal_lunas_saja(request, object_id):
    ag = AkadGadai.objects.get(id=object_id)
    ag.lunas = None
    ag.status_transaksi = None
    ag.status_kwlunas = None
    ag.status_oto_plns = None
    ag.jasa_lunas = 0
    ag.denda_lunas = 0
    ag.terlambat = 0
    ag.jasa_kendaraan_lunas = 0
    ag.denda_kendaraan_lunas = 0
    ag.terlambat_kendaraan = 0
    ag.nilai_lunas = 0
    ag.barang.akad_ulang = 0
    ag.norek_lunas_sblm = None
    ag.save()
    tbl_pelunasan = ag.pelunasan_set.all()
    tbl_pelunasan.delete()       
    jurnal = Jurnal.objects.filter(nobukti=ag.norek()).filter(diskripsi__icontains = 'Plns')
    jurnal.delete()
    jurnal1 = Jurnal.objects.filter(nobukti=ag.norek()).filter(diskripsi__icontains = 'Pelunasan')
    jurnal1.delete()
    jurnal = KasirGeraiPelunasan.objects.filter(kasir_lunas__id=ag.id)
    jurnal.delete()
    messages.add_message(request, messages.INFO, 'Akadgadai no rek : %s BATAL lunas" % ag.norek()')
    return HttpResponseRedirect(ag.get_absolute_url())

@login_required
def batal_cair_manop(request, object_id):
    ag = AkadGadai.objects.get(id=object_id)     
    ag.lunas = None
    ag.status_transaksi = '4'
    ag.status_kwlunas = None
    ag.save()
    jurnal = Jurnal.objects.filter(nobukti=ag.norek())
    jurnal.delete()
    ksr = KasirGerai.objects.get(kasir=object_id)
    ksr.delete()
    kg = KepalaGerai.objects.get(kepala_gerai=object_id)
    kg.delete()
    mat = Biaya_Materai_Cab.objects.filter(norek=ag.norek())
    mat.delete()
    #id_akad = ag.id
    #jurnal = Jurnal.objects.filter(object_id=id_akad).order_by('-id')
    #jrl = jurnal[0]
    #jurnal.delete() 
    messages.add_message(request, messages.INFO, 'Akadgadai no rek : %s BATAL CAIR % ag.norek()')
    return HttpResponseRedirect(ag.get_absolute_url())

@login_required
@user_passes_test(lambda u: u.groups.filter(name='ADM_GERAI'))
def data_tolak(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    akad = AkadGadai.objects.filter(status_transaksi__in=('4','5')).filter(gerai__kode_cabang=cab)
    variables = RequestContext(request, {'akad': akad})
    return render(request,'akadgadai/data_tolak.html', {'akad':akad})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='ADM_GERAI'))
def lunas(request):
    akad = AkadGadai.objects.all()
    template='pelunasan/plns.html'
    variable = RequestContext(request,{'akad': akad})
    return render_to_response(template,variable)

@login_required
def cariplns(request):
    rekening=request.GET['rekening']
    barcode = rekening[11:]
    try:
        akad=AkadGadai.objects.get(id=int(barcode))
        return HttpResponseRedirect("/akadgadai/%s/plns/" % akad.id)
    except:
        messages.add_message(request, messages.INFO,'No rekening tidak ditemukan.')
        return HttpResponseRedirect("/akadgadai/lunas/")
   
@login_required
def plns(request, object_id):
    sekarang = datetime.date.today()
    akad = AkadGadai.objects.get(id=object_id)
    titip = TitipanPelunasan.objects.filter(norek = object_id)
    if akad.jenis_transaksi == u'1' and akad.status_oto_plns == u'' :
        form = PelunasanForm(initial={'pelunasan': akad.id,'tanggal': sekarang,'nilai': int(akad.nilai),
            'jenis_barang':akad.jenis_transaksi,'terlambat':akad.hari_terlambat,'lunas':sekarang,'terlambat_kendaraan':0,
            'gerai':akad.gerai,'jatuhtempo':akad.jatuhtempo,'lunas':sekarang,'status_transaksi':1,'tgl_akad':akad.tanggal,'norek':akad.norek(),
            'denda': int(akad.hitung_denda_pelunasan()),'bea_jasa':int(akad.hitung_jasa_pelunasan()),#0,
            'total': (int(akad.nilai) + int(akad.hitung_denda_pelunasan())) + int(akad.hitung_jasa_pelunasan())})
        form.fields['pelunasan'].widget = forms.HiddenInput()
        form.fields['lunas'].widget = forms.HiddenInput()
        form.fields['status_transaksi'].widget = forms.HiddenInput()
        template = 'akadgadai/pelunasan.html'
        variable = RequestContext(request, {'akad': akad,'form':form,'titip':titip})
        return render_to_response(template,variable)
    elif akad.jenis_transaksi == u'1' and akad.status_oto_plns == None:
        form = PelunasanForm(initial={'pelunasan': akad.id,'tanggal': sekarang,'nilai': int(akad.nilai),
            'jenis_barang':akad.jenis_transaksi,'terlambat':akad.hari_terlambat,'lunas':sekarang,'terlambat_kendaraan':0,
            'gerai':akad.gerai,'jatuhtempo':akad.jatuhtempo,'lunas':sekarang,'status_transaksi':1,'tgl_akad':akad.tanggal,'norek':akad.norek(),
            'denda': int(akad.denda_plns_baru()),'bea_jasa':int(akad.hitung_jasa_pelunasan()),#0,
            'total': (int(akad.nilai) + int(akad.hitung_denda_pelunasan())) + int(akad.hitung_jasa_pelunasan())})
        form.fields['pelunasan'].widget = forms.HiddenInput()
        form.fields['lunas'].widget = forms.HiddenInput()
        form.fields['status_transaksi'].widget = forms.HiddenInput()
        template = 'akadgadai/pelunasan.html'
        variable = RequestContext(request, {'akad': akad,'form':form,'titip':titip})
        return render_to_response(template,variable)
    elif akad.jenis_transaksi == u'2'  and akad.status_oto_plns == u'':
        form = PelunasanForm(initial={'pelunasan': akad.id,'tanggal': sekarang,'nilai': int(akad.nilai),
            'jenis_barang':akad.jenis_transaksi,'terlambat':akad.hari_terlambat,'lunas':sekarang,'terlambat_kendaraan':akad.hari_terlambat,
            'gerai':akad.gerai,'jatuhtempo':akad.jatuhtempo,'lunas':sekarang,'status_transaksi':1,'tgl_akad':akad.tanggal,'norek':akad.norek(),
            'denda': int(akad.denda_plns_baru()),'bea_jasa':int(akad.hitung_jasa_pelunasan()),#0,
            'total':0,
            'total_kendaraan': (int(akad.nilai) + int(akad.hitung_denda_pelunasan())) + int(akad.hitung_jasa_pelunasan())})
        form.fields['pelunasan'].widget = forms.HiddenInput()
        form.fields['lunas'].widget = forms.HiddenInput()
        form.fields['status_transaksi'].widget = forms.HiddenInput()
        template = 'akadgadai/pelunasan.html'
        variable = RequestContext(request, {'akad': akad,'form':form,'titip':titip})
        return render_to_response(template,variable)
    elif akad.jenis_transaksi == u'2'  and akad.status_oto_plns == None:
        form = PelunasanForm(initial={'pelunasan': akad.id,'tanggal': sekarang,'nilai': int(akad.nilai),
            'jenis_barang':akad.jenis_transaksi,'terlambat':akad.hari_terlambat,'lunas':sekarang,'terlambat_kendaraan':akad.hari_terlambat,
            'gerai':akad.gerai,'jatuhtempo':akad.jatuhtempo,'lunas':sekarang,'status_transaksi':1,'tgl_akad':akad.tanggal,'norek':akad.norek(),
            'denda': int(akad.denda_plns_baru()),'bea_jasa':int(akad.hitung_jasa_pelunasan()),#0
            'total_kendaraan': (int(akad.nilai) + int(akad.hitung_denda_pelunasan())) + int(akad.hitung_jasa_pelunasan()),
            'total': 0})
        form.fields['pelunasan'].widget = forms.HiddenInput()
        form.fields['lunas'].widget = forms.HiddenInput()
        form.fields['status_transaksi'].widget = forms.HiddenInput()
        template = 'akadgadai/pelunasan.html'
        variable = RequestContext(request, {'akad':  akad,'form':form,'titip':titip})
        return render_to_response(template,variable)
    elif akad.jenis_transaksi == u'3' and akad.status_oto_plns == u'':
        form = PelunasanForm(initial={'pelunasan': akad.id,'tanggal': sekarang,'nilai': int(akad.nilai),
            'jenis_barang':akad.jenis_transaksi,'terlambat':akad.hari_terlambat,'lunas':sekarang,'terlambat_kendaraan':akad.hari_terlambat,
            'gerai':akad.gerai,'jatuhtempo':akad.jatuhtempo,'lunas':sekarang,'status_transaksi':1,'tgl_akad':akad.tanggal,'norek':akad.norek(),
            'denda': 0,'bea_jasa':0,
            'denda_kendaraan': int(akad.denda_plns_baru()),'bea_jasa_kendaraan':(akad.hitung_jasa_pelunasan()),#0
            'total': 0,
            'total_kendaraan': (int(akad.nilai) + int(akad.hitung_denda_pelunasan()))+ int(akad.hitung_jasa_pelunasan())}) 
        form.fields['pelunasan'].widget = forms.HiddenInput()
        form.fields['lunas'].widget = forms.HiddenInput()
        form.fields['status_transaksi'].widget = forms.HiddenInput()
        template = 'akadgadai/pelunasan.html'
        variable = RequestContext(request, {'akad': akad,'form':form,'titip':titip})
        return render_to_response(template,variable)
    elif akad.jenis_transaksi == u'3' and akad.status_oto_plns == None:
        form = PelunasanForm(initial={'pelunasan': akad.id,'tanggal': sekarang,'nilai': int(akad.nilai),
            'jenis_barang':akad.jenis_transaksi,'terlambat':akad.hari_terlambat,'lunas':sekarang,'terlambat_kendaraan':akad.hari_terlambat,
            'gerai':akad.gerai,'jatuhtempo':akad.jatuhtempo,'lunas':sekarang,'status_transaksi':1,'tgl_akad':akad.tanggal,'norek':akad.norek(),
            'denda': 0,'bea_jasa':0,
            'denda_kendaraan': int(akad.denda_plns_baru()),'bea_jasa_kendaraan':(akad.hitung_jasa_pelunasan()),#0
            'total': 0,
            'total_kendaraan': (int(akad.nilai) + int(akad.hitung_denda_pelunasan())) + int(akad.hitung_jasa_pelunasan())}) 
        form.fields['pelunasan'].widget = forms.HiddenInput()
        form.fields['lunas'].widget = forms.HiddenInput()
        form.fields['status_transaksi'].widget = forms.HiddenInput()
        template = 'akadgadai/pelunasan.html'
        variable = RequestContext(request, {'akad': akad,'form':form,'titip':titip})
        return render_to_response(template,variable)
    elif akad.jenis_transaksi =='1' and akad.status_oto_plns == '3':
        form_diskon = PelunasanDiskonForm(initial={'pelunasan': akad.id,'tanggal': sekarang,'nilai': int(akad.nilai_lunas),
            'jenis_barang':akad.jenis_transaksi,'terlambat':akad.hari_terlambat,'lunas':sekarang,'terlambat_kendaraan':0,
            'gerai':akad.gerai,'jatuhtempo':akad.jatuhtempo,'lunas':sekarang,'status_transaksi':1,'tgl_akad':akad.tanggal,'norek':akad.norek(),
            #'denda': int(akad.denda_kendaraan_lunas),'denda_kendaraan':0,
            'denda': int(akad.denda_lunas),'denda_kendaraan':0,
            #'bea_jasa':int(akad.jasa_kendaraan_lunas) ,'bea_jasa_kendaraan':0,
            'bea_jasa':int(akad.jasa_lunas) ,'bea_jasa_kendaraan':0,
            'total': (int(akad.nilai_lunas) + int(akad.jasa_lunas) + int(akad.denda_lunas)),
            #'total': (int(akad.nilai_lunas) + int(akad.jasa_kendaraan_lunas) + int(akad.jasa_lunas) +int(akad.jasa_kendaraan_lunas)),
            'total_kendaraan': 0})
        form_diskon.fields['pelunasan'].widget = forms.HiddenInput()
        form_diskon.fields['lunas'].widget = forms.HiddenInput()
        form_diskon.fields['status_transaksi'].widget = forms.HiddenInput() 
        template = 'akadgadai/pelunasan.html'
        variable = RequestContext(request, {'akad': akad,'form_diskon':form_diskon,'titip':titip})
        return render_to_response(template,variable) 
    elif akad.jenis_transaksi =='2' and akad.status_oto_plns == '3':
        form_diskon = PelunasanDiskonForm(initial={'pelunasan': akad.id,'tanggal': sekarang,'nilai': int(akad.nilai_lunas),
            'jenis_barang':akad.jenis_transaksi,'terlambat':0,'lunas':sekarang,'terlambat_kendaraan':akad.hari_terlambat,
            'gerai':akad.gerai,'jatuhtempo':akad.jatuhtempo,'lunas':sekarang,'status_transaksi':1,'tgl_akad':akad.tanggal,'norek':akad.norek(),
            'denda': 0,'denda_kendaraan': int(akad.denda_kendaraan_lunas),
            'bea_jasa':0 ,'bea_jasa_kendaraan':int(akad.jasa_kendaraan_lunas) ,
            'total': 0,
            'total_kendaraan': (int(akad.nilai_lunas) + int(akad.denda_kendaraan_lunas) + int(akad.jasa_kendaraan_lunas))})
        form_diskon.fields['pelunasan'].widget = forms.HiddenInput()
        form_diskon.fields['lunas'].widget = forms.HiddenInput()
        form_diskon.fields['status_transaksi'].widget = forms.HiddenInput() 
        template = 'akadgadai/pelunasan.html'
        variable = RequestContext(request, {'akad': akad,'form_diskon':form_diskon,'titip':titip})
        return render_to_response(template,variable) 
    elif akad.jenis_transaksi =='3' and akad.status_oto_plns == '3':
        form_diskon = PelunasanDiskonForm(initial={'pelunasan': akad.id,'tanggal': sekarang,'nilai': int(akad.nilai_lunas),
            'jenis_barang':akad.jenis_transaksi,'terlambat':0,'lunas':sekarang,'terlambat_kendaraan':akad.hari_terlambat,
            'gerai':akad.gerai,'jatuhtempo':akad.jatuhtempo,'lunas':sekarang,'status_transaksi':1,'tgl_akad':akad.tanggal,'norek':akad.norek(),
            'denda': 0,'denda_kendaraan': int(akad.denda_kendaraan_lunas),
            'bea_jasa':0 ,'bea_jasa_kendaraan':int(akad.jasa_kendaraan_lunas) ,
            'total': 0,
            'total_kendaraan': (int(akad.nilai_lunas) + int(akad.denda_kendaraan_lunas) + int(akad.jasa_kendaraan_lunas))})
        form_diskon.fields['pelunasan'].widget = forms.HiddenInput()
        form_diskon.fields['lunas'].widget = forms.HiddenInput()
        form_diskon.fields['status_transaksi'].widget = forms.HiddenInput()
        template = 'akadgadai/pelunasan.html'
        variable = RequestContext(request, {'akad': akad,'form_diskon':form_diskon,'titip':titip})
        return render_to_response(template,variable) 
    else:
        form =PelunasanForm()
        form_diskon =PelunasanDiskonForm()
        template = 'akadgadai/pelunasan.html'
        variable = RequestContext(request, {'akad': akad,'form':form,'form_diskon':form_diskon,'titip':titip})
        return render_to_response(template,variable) 

@login_required
def pelunasan(request, object_id):
    user = request.user
    d = decimal.Decimal
    ag = AkadGadai.objects.get(id=object_id)
    if request.method == 'POST':
        form= PelunasanForm(request.POST)
        if form.is_valid():
            lunas = form.cleaned_data['lunas']
            status_transaksi = form.cleaned_data['status_transaksi']
            tanggal = form.cleaned_data['tanggal']
            nilai = form.cleaned_data['nilai']
            pelunasan = form.cleaned_data['pelunasan']
            terlambat = form.cleaned_data['terlambat']
            denda = form.cleaned_data['denda']
            bea_jasa = form.cleaned_data['bea_jasa']
            jenis_barang = form.cleaned_data['jenis_barang']
            terlambat_kendaraan = form.cleaned_data['terlambat_kendaraan']
            denda_kendaraan = form.cleaned_data['denda_kendaraan']
            bea_jasa_kendaraan = form.cleaned_data['bea_jasa_kendaraan']
            gerai = form.cleaned_data['gerai']
            status = form.cleaned_data['status']
            comment = form.cleaned_data['comment']

            ag.denda_lunas = denda
            ag.denda_kendaraan_lunas = denda_kendaraan
            ag.jasa_lunas = bea_jasa
            ag.jasa_kendaraan_lunas = bea_jasa_kendaraan
            ag.terlambat = terlambat
            ag.terlambat_kendaraan = terlambat_kendaraan
            ag.status_oto_plns = status
            ag.nilai_lunas = nilai
            ag.save()
            if ag.status_oto_plns == '2':
                manop = ManopPelunasan(pelunasan_id = ag.id,tanggal = datetime.date.today(),status = 1,note =comment)
                manop.save()
                messages.add_message(request, messages.INFO, 'Otorisasi Pelunasan Manop')
            ##### elektronik             
            elif ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == u'1' and ag.denda_lunas > 0 \
                and ag.jasa_lunas > 0 and ag.nilai_lunas == ag.nilai and ag.kasirgeraipelunasan.cu.profile.gerai == user.profile.gerai :
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi 1 (467)')
                jurnal_pelunasan(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=terlambat,denda = denda,bea_jasa=bea_jasa,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=0,denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment,sts_plns = 1)
                plns.save()
            elif ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == u'1' and ag.denda_lunas > 0 \
                and ag.jasa_lunas > 0 and ag.nilai_lunas == ag.nilai and ag.kasirgeraipelunasan.cu.profile.gerai != user.profile.gerai and ag.selisih_pelunasan > 0:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi 1 (480)')
                jurnal_pelunasan_rak_pol(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=terlambat,denda = denda,bea_jasa=bea_jasa,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=0,denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment,sts_plns = 1)
                plns.save()
            elif ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == u'1' and ag.denda_lunas > 0 \
                and ag.jasa_lunas > 0 and ag.nilai_lunas == ag.nilai and ag.kasirgeraipelunasan.cu.profile.gerai != user.profile.gerai and ag.selisih_pelunasan < 0:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi 1 (450)')
                jurnal_pelunasan_rak_bol(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=terlambat,denda = denda,bea_jasa=bea_jasa,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=0,denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment,sts_plns = 1)
                plns.save()
            elif ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == u'1' and ag.denda_lunas > 0 \
                and ag.jasa_lunas > 0 and ag.nilai_lunas == ag.nilai and ag.kasirgeraipelunasan.cu.profile.gerai != user.profile.gerai and ag.selisih_pelunasan == 0:
                ag.lunas = tanggal
                ag.os_pokok = 0 
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi 1 (450)')
                jurnal_pelunasan_rak_sama(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=terlambat,denda = denda,bea_jasa=bea_jasa,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=0,denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment, sts_plns = 1)
                plns.save()
            #####NON RAK KASIR
            elif ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == u'1' and ag.denda_lunas > 0 and \
                ag.jasa_lunas > 0 and ag.nilai_lunas == ag.nilai and ag.kasirgeraipelunasan.cu.profile.gerai == user.profile.gerai :
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.denda_lunas = ag.hitung_denda_pelunasan()
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi 2 (463)')
                jurnal_pelunasan_none(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=terlambat,denda = ag.hitung_denda_pelunasan(),bea_jasa=bea_jasa,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=0,denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment, sts_plns = 1)
                plns.save()
            elif ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == u'1' and ag.denda_lunas > 0 and \
                ag.jasa_lunas > 0 and ag.nilai_lunas == ag.nilai and ag.kasirgeraipelunasan.cu.profile.gerai != user.profile.gerai and\
                ag.selisih_pelunasan > 0 :
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.denda_lunas = ag.hitung_denda_pelunasan()
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi RAK (493)')
                jurnal_pelunasan_none_rak_pol(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=terlambat,denda = ag.hitung_denda_pelunasan(),bea_jasa=bea_jasa,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=0,denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment, sts_plns = 1)
                plns.save()
            elif ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == u'1' and ag.denda_lunas > 0 and \
                ag.jasa_lunas > 0 and ag.nilai_lunas == ag.nilai and ag.kasirgeraipelunasan.cu.profile.gerai != user.profile.gerai and ag.selisih_pelunasan < 0 :
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi RAK (508)')
                jurnal_pelunasan_none_rak_bol(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=terlambat,denda = denda,bea_jasa=bea_jasa,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=0,denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment, sts_plns = 1)
                plns.save()
            elif ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == u'1' and ag.denda_lunas > 0 and \
                ag.jasa_lunas > 0 and ag.nilai_lunas == ag.nilai and ag.kasirgeraipelunasan.cu.profile.gerai != user.profile.gerai and ag.selisih_pelunasan == 0 :
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi RAK (560)')
                jurnal_pelunasan_none_rak_sama(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=terlambat,denda = denda,bea_jasa=bea_jasa,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=0,denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment, sts_plns = 1)
                plns.save()

            ##### Kendaraan Anggota Rak & non
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == u'1' and ag.denda_kendaraan_lunas > 0 \
                and ag.jasa_kendaraan_lunas > 0 and ag.nilai_lunas == ag.nilai and ag.nilai_lunas == ag.nilai and ag.kasirgeraipelunasan.cu.profile.gerai == user.profile.gerai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi 1 (575)')
                jurnal_pelunasan_nonoto_kendaraan(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=0,denda =0,bea_jasa=0,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=terlambat_kendaraan,denda_kendaraan=denda_kendaraan,val= 0,
                    bea_jasa_kendaraan=bea_jasa_kendaraan,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment, sts_plns = 1)
                plns.save()
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == u'1' and ag.denda_kendaraan_lunas > 0 \
                and ag.jasa_kendaraan_lunas > 0 and ag.nilai_lunas == ag.nilai and ag.nilai_lunas == ag.nilai and ag.kasirgeraipelunasan.cu.profile.gerai != user.profile.gerai \
                and ag.selisih_pelunasan > 0:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi 1 (589)')
                jurnal_pelunasan_nonoto_kendaraan_rak_pol(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=0,denda =0,bea_jasa=0,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=terlambat_kendaraan,denda_kendaraan=denda_kendaraan,val= 0,
                    bea_jasa_kendaraan=bea_jasa_kendaraan,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment, sts_plns = 1)
                plns.save()
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == u'1' and ag.denda_kendaraan_lunas > 0 \
                and ag.jasa_kendaraan_lunas > 0 and ag.nilai_lunas == ag.nilai and ag.nilai_lunas == ag.nilai and ag.kasirgeraipelunasan.cu.profile.gerai != user.profile.gerai \
                and ag.selisih_pelunasan < 0:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi 1 (603)')
                jurnal_pelunasan_nonoto_kendaraan_rak_bol(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=0,denda =0,bea_jasa=0,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=terlambat_kendaraan,denda_kendaraan=denda_kendaraan,val= 0,
                    bea_jasa_kendaraan=bea_jasa_kendaraan,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment, sts_plns = 1)
                plns.save()
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == u'1' and ag.denda_kendaraan_lunas > 0 \
                and ag.jasa_kendaraan_lunas > 0 and ag.nilai_lunas == ag.nilai and ag.nilai_lunas == ag.nilai and ag.kasirgeraipelunasan.cu.profile.gerai != user.profile.gerai \
                and ag.selisih_pelunasan == 0:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi 1 (617)')
                jurnal_pelunasan_nonoto_kendaraan_rak_sama(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=0,denda =0,bea_jasa=0,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=terlambat_kendaraan,denda_kendaraan=denda_kendaraan,val= 0,
                    bea_jasa_kendaraan=bea_jasa_kendaraan,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment, sts_plns = 1)
                plns.save()
            ###### Kendaraan Anggota RAK And NOn AKHIR

            ##### KENDARAAN NON ANGGOTA RAK & NON
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == u'1' and \
                ag.denda_kendaraan_lunas > 0 and ag.jasa_kendaraan_lunas > 0 and ag.nilai_lunas == ag.nilai and ag.kasirgeraipelunasan.cu.profile.gerai == user.profile.gerai:
                ag.lunas = tanggal 
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi 2 (633)')
                jurnal_pelunasan_noneoto_kendaraan(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=0,denda = 0,bea_jasa=0,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=terlambat_kendaraan,denda_kendaraan=denda_kendaraan,val= 0,
                    bea_jasa_kendaraan=bea_jasa_kendaraan,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment, sts_plns = 1)
                plns.save()
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == u'1' and \
                ag.denda_kendaraan_lunas > 0 and ag.jasa_kendaraan_lunas > 0 and ag.nilai_lunas == ag.nilai and \
                ag.kasirgeraipelunasan.cu.profile.gerai != user.profile.gerai and ag.selisih_pelunasan > 0:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi 2 (647)')
                jurnal_pelunasan_noneoto_kendaraan_rak_pol(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=0,denda = 0,bea_jasa=0,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=terlambat_kendaraan,denda_kendaraan=denda_kendaraan,val= 0,
                    bea_jasa_kendaraan=bea_jasa_kendaraan,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment, sts_plns = 1)
                plns.save()
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == u'1' and \
                ag.denda_kendaraan_lunas > 0 and ag.jasa_kendaraan_lunas > 0 and ag.nilai_lunas == ag.nilai and \
                ag.kasirgeraipelunasan.cu.profile.gerai != user.profile.gerai and ag.selisih_pelunasan < 0:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi 2 (661)')
                jurnal_pelunasan_noneoto_kendaraan_rak_bol(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=0,denda = 0,bea_jasa=0,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=terlambat_kendaraan,denda_kendaraan=denda_kendaraan,val= 0,
                    bea_jasa_kendaraan=bea_jasa_kendaraan,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment, sts_plns = 1)
                plns.save() 
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == u'1' and \
                ag.denda_kendaraan_lunas > 0 and ag.jasa_kendaraan_lunas > 0 and ag.nilai_lunas == ag.nilai and \
                ag.kasirgeraipelunasan.cu.profile.gerai != user.profile.gerai and ag.selisih_pelunasan == 0:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi RAK (675)')
                jurnal_pelunasan_noneoto_kendaraan_rak_sama(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=0,denda = 0,bea_jasa=0,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=terlambat_kendaraan,denda_kendaraan=denda_kendaraan,val= 0,
                    bea_jasa_kendaraan=bea_jasa_kendaraan,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment, sts_plns = 1)
                plns.save()
            #####jasa atau denda kosong elektronik
            elif ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == u'1' and \
                ag.denda_lunas == 0 and ag.jasa_lunas == 0 and ag.nilai_lunas == ag.nilai and ag.kasirgeraipelunasan.cu.profile.gerai == user.profile.gerai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi (689)')
                jurnal_pelunasan_denda_jasa_kosong(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=terlambat,denda = denda,bea_jasa=bea_jasa,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=0,denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment, sts_plns = 1)
                plns.save()
            elif ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == u'1' and \
                ag.denda_lunas == 0 and ag.jasa_lunas == 0 and ag.nilai_lunas == ag.nilai  and ag.kasirgeraipelunasan.cu.profile.gerai == user.profile.gerai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi 2 (702)')
                jurnal_pelunasan_none_denda_jasa_kosong(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=terlambat,denda = denda,bea_jasa=bea_jasa,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=0,denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment, sts_plns = 1)
                plns.save()
            #####jasa atau denda kosong Kendaraan
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == u'1' and \
                ag.denda_kendaraan_lunas == 0 and ag.jasa_kendaraan_lunas == 0 and ag.nilai_lunas == ag.nilai and ag.kasirgeraipelunasan.cu.profile.gerai == user.profile.gerai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi 1(716)')
                jurnal_pelunasan_denda_jasa_kosong(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=0,denda =0,bea_jasa=0,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=terlambat_kendaraan,denda_kendaraan=denda_kendaraan,val= 0,
                    bea_jasa_kendaraan=bea_jasa_kendaraan,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment, sts_plns = 1)
                plns.save()
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == u'1' and \
                ag.denda_lunas == 0 and ag.jasa_lunas == 0 and ag.nilai_lunas == ag.nilai  and ag.kasirgeraipelunasan.cu.profile.gerai == user.profile.gerai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi 2 (729)')
                jurnal_pelunasan_none_denda_jasa_kosong(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=0,denda = 0,bea_jasa=0,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=terlambat_kendaraan,denda_kendaraan=denda_kendaraan,val= 0,
                    bea_jasa_kendaraan=bea_jasa_kendaraan,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment, sts_plns = 1)
                plns.save()

            #params = '{"to":"%s", "msg":"%s"}' % (ag.agnasabah.hp_ktp,ag.smslunas())
            #headers = {"Content-Type": "application/json"}
            #conn = httplib.HTTPConnection("103.10.171.125")
            #conn.request("POST", "/api/sms/", params, headers)
            #response = conn.getresponse()
            messages.add_message(request, messages.INFO, 'Nilai Pelunasan OK')
            return HttpResponseRedirect('/')
        else:
            variables = RequestContext(request, {'form': form,'ag':ag})
            return render_to_response('akadgadai/pelunasan.html', variables) 

def jurnal_pelunasan_nonoto_kendaraan(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='1')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4

   
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang = ag.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(),ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai)) + D(ag.jasa_kendaraan_lunas) + D(ag.denda_kendaraan_lunas),id_product = '4',status_jurnal ='2',
        tgl_trans = ag.lunas ,id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(),ag.agnasabah.nama),
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(),ag.agnasabah.nama),
        debet = 0,kredit = ag.denda_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_jasa,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(),ag.agnasabah.nama),
        debet = 0,kredit = ag.jasa_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_nonoto_kendaraan_rak_pol(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='1')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4
    a_pdp_lainnya = lunas.coa_6

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang = ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(),ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai)) + D(ag.jasa_kendaraan_lunas) + D(ag.denda_kendaraan_lunas) + D(ag.selisih_pelunasan),id_product = '4',status_jurnal ='2',
        tgl_trans = ag.lunas ,id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(),ag.agnasabah.nama),
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(),ag.agnasabah.nama),
        debet = 0,kredit = ag.denda_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_jasa,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(),ag.agnasabah.nama),
        debet = 0,kredit = ag.jasa_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_lainnya,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(),ag.agnasabah.nama),
        debet = 0,kredit = ag.selisih_pelunasan,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_nonoto_kendaraan_rak_bol(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='1')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4
    a_pdp_lainnya = lunas.coa_7

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang = ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai)) + D(ag.jasa_kendaraan_lunas) + D(ag.denda_kendaraan_lunas) - D(-1 * ag.selisih_pelunasan),id_product = '4',status_jurnal ='2',
        tgl_trans = ag.lunas ,id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.denda_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_jasa,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.jasa_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_lainnya,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = -1 * ag.selisih_pelunasan,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_nonoto_kendaraan_rak_sama(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='1')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang = ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai)) + D(ag.jasa_kendaraan_lunas) + D(ag.denda_kendaraan_lunas) - D(-1 * ag.selisih_pelunasan),id_product = '4',status_jurnal ='2',
        tgl_trans = ag.lunas ,id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.denda_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_jasa,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.jasa_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)


def jurnal_pelunasan_noneoto_kendaraan(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='2')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang = ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(),ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai)) + D(ag.jasa_kendaraan_lunas) + D(ag.denda_kendaraan_lunas),id_product = '4',status_jurnal ='2',\
        tgl_trans = ag.lunas ,id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(),ag.agnasabah.nama),
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(),ag.agnasabah.nama),
        debet = 0,kredit = ag.denda_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_jasa,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(),ag.agnasabah.nama),
        debet = 0,kredit = ag.jasa_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_noneoto_kendaraan_rak_pol(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='2')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4
    a_pdp_lainnya = lunas.coa_6

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang = ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(),ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai)) + D(ag.jasa_kendaraan_lunas) + D(ag.denda_kendaraan_lunas) + D(ag.selisih_pelunasan),id_product = '4',status_jurnal ='2',\
        tgl_trans = ag.lunas ,id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(),ag.agnasabah.nama),
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(),ag.agnasabah.nama),
        debet = 0,kredit = ag.denda_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_jasa,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(),ag.agnasabah.nama),
        debet = 0,kredit = ag.jasa_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_lainnya,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(),ag.agnasabah.nama),
        debet = 0,kredit = ag.selisih_pelunasan,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_noneoto_kendaraan_rak_bol(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='2')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4
    a_pdp_lainnya = lunas.coa_7

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang = ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai)) + D(ag.jasa_kendaraan_lunas) + D(ag.denda_kendaraan_lunas) + D(-1 *ag.selisih_pelunasan),id_product = '4',status_jurnal ='2',\
        tgl_trans = ag.lunas ,id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.denda_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_jasa,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.jasa_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_lainnya,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = (-1 * ag.selisih_pelunasan),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_noneoto_kendaraan_rak_sama(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='2')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang = ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai)) + D(ag.jasa_kendaraan_lunas) + D(ag.denda_kendaraan_lunas),id_product = '4',status_jurnal ='2',\
        tgl_trans = ag.lunas ,id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.denda_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_jasa,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.jasa_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_diskon_denda_anggota(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='9')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_jasa =lunas.coa_4

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang = ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai)) + ag.jasa_lunas + ag.jasa_kendaraan_lunas ,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,#debet D(str(ag.nilai_lunas))
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = D(str(ag.nilai_lunas)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,#debet = D(str(ag.nilai)) -(ag.nilai_lunas)
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_jasa,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.jasa_lunas + ag.jasa_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_diskon_denda_nonanggota(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='10')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_jasa =lunas.coa_4

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang = ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai)) + ag.jasa_lunas + ag.jasa_kendaraan_lunas ,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = D(str(ag.nilai)),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_jasa,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.jasa_lunas + ag.jasa_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)




def jurnal_diskon_jasa_nonanggota(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='8')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda =lunas.coa_3

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang = ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai_lunas))+ ag.denda_lunas + ag.denda_kendaraan_lunas,\
        id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = D(str(ag.nilai)),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.denda_lunas + ag.denda_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)


def jurnal_diskon_jasa(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='7')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda =lunas.coa_3

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang = ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai_lunas)) + ag.denda_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,# D(str(ag.nilai_lunas))
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = D(str(ag.nilai_lunas)),debet =  0,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas , # debet = D(str(ag.nilai)) - (ag.nilai_lunas)
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit =  ag.denda_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_diskon_jasa_kendaraan(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='7')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda =lunas.coa_3

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang = ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai_lunas)),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai)) - (ag.nilai_lunas),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.denda_kendaraan_lunas ,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)



def jurnal_ppap(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='5')
    a_titipan_pelunasan = lunas.coa_1
    a_ppap = lunas.coa_5
    a_pinjaman_anggota = lunas.coa_2

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang=ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai_lunas)),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_ppap,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai)) - ag.nilai_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_ppap_nonanggota(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='6')
    a_titipan_pelunasan = lunas.coa_1
    a_ppap = lunas.coa_5
    a_pinjaman_anggota = lunas.coa_2

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang=ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai_lunas)),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_ppap,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai)) - ag.nilai_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

        
def jurnal_pelunasan(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='1')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4

   
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang=ag.gerai.kode_cabang)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai  + ag.jasa_lunas + (ag.denda_lunas))),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.denda_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_jasa,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.jasa_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_rak_pol(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='1')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4
    a_pdp_lainnya = lunas.coa_6

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang=ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai  + ag.jasa_lunas + (ag.denda_lunas))) + D(ag.selisih_pelunasan),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.denda_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_jasa,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.jasa_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_lainnya,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.selisih_pelunasan,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_rak_bol(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='1')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4
    a_pdp_lainnya = lunas.coa_7

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang=ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai  + ag.jasa_lunas + (ag.denda_lunas))) - D(-1 * ag.selisih_pelunasan),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.denda_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_jasa,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.jasa_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_lainnya,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = (-1 *ag.selisih_pelunasan),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_rak_sama(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='1')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang=ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        kredit = 0,debet = D(str(ag.nilai  + ag.jasa_lunas + (ag.denda_lunas))) ,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.denda_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_jasa,
        deskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = ag.jasa_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)


def jurnal_pelunasan_kendaraan(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='1')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4


    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang=ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        kredit = 0,debet = D(str(ag.nilai  + ag.jasa_kendaraan_lunas + (ag.denda_kendaraan_lunas))),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        debet = 0,kredit = ag.denda_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_jasa,
        debet = 0,kredit = ag.jasa_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    
    
def jurnal_pelunasan_none(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='2')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang=ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        #kredit = 0,debet = D(str(ag.nilai  + ag.jasa_lunas + (ag.denda_lunas))),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        kredit = 0,debet = (int(ag.nilai) + int(ag.hitung_denda_pelunasan())) + int(ag.hitung_jasa_pelunasan()),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        debet = 0,kredit = int(ag.hitung_denda_pelunasan()) ,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_jasa,
        debet = 0,kredit = ag.jasa_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_none_rak_pol(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='2')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4
    a_pdp_lainnya =lunas.coa_6

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang=ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        kredit = 0,debet = D(str(ag.nilai  + ag.jasa_lunas + (ag.denda_lunas))) + D(ag.selisih_pelunasan),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        debet = 0,kredit = ag.denda_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_jasa,
        debet = 0,kredit = ag.jasa_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_lainnya,
        debet = 0,kredit = ag.selisih_pelunasan,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_none_rak_bol(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='2')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4
    a_pdp_beban =lunas.coa_7

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang=ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        kredit = 0,debet = D(str(ag.nilai  + ag.jasa_lunas + (ag.denda_lunas))) - D(-1 * ag.selisih_pelunasan),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_beban,
        kredit = 0,debet = (-1 * ag.selisih_pelunasan),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        debet = 0,kredit = ag.denda_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_jasa,
        debet = 0,kredit = ag.jasa_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_none_rak_sama(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='2')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang=ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        kredit = 0,debet = D(str(ag.nilai  + ag.jasa_lunas + (ag.denda_lunas))),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        debet = 0,kredit = ag.denda_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_jasa,
        debet = 0,kredit = ag.jasa_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_none_kendaraan(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='2')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang=ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        kredit = 0,debet = D(ag.nilai)  + ag.jasa_kendaraan_lunas + ag.denda_kendaraan_lunas,
        id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        debet = 0,kredit = ag.denda_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_jasa,
        debet = 0,kredit = ag.jasa_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)


###Jurnal Non Denda None Jasa

def jurnal_pelunasan_none_denda_jasa_kosong(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='2')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang=ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        kredit = 0,debet = D(str(ag.nilai)),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_denda_jasa_kosong(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='1')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda = lunas.coa_3
    a_pdp_jasa = lunas.coa_4

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id(),kode_cabang=ag.gerai.kode_cabang)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        kredit = 0,debet = D(str(ag.nilai)),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

####Akhir Jurnal Non Denda None Jasa
@login_required
def diskon_pelunasan(request, object_id):
    d = decimal.Decimal
    ag = AkadGadai.objects.get(id=object_id)
    #plns = Pelunasan.objects.filter(pelunasan = ag.id)
    if request.method == 'POST':
        form = PelunasanDiskonForm(request.POST)
        if form.is_valid():
            lunas = form.cleaned_data['lunas']
            status_transaksi = form.cleaned_data['status_transaksi']
            tanggal = form.cleaned_data['tanggal']
            nilai = form.cleaned_data['nilai']
            pelunasan = form.cleaned_data['pelunasan']
            terlambat = form.cleaned_data['terlambat']
            denda = form.cleaned_data['denda']
            bea_jasa = form.cleaned_data['bea_jasa']
            jenis_barang = form.cleaned_data['jenis_barang']
            terlambat_kendaraan = form.cleaned_data['terlambat_kendaraan']
            denda_kendaraan = form.cleaned_data['denda_kendaraan']
            bea_jasa_kendaraan = form.cleaned_data['bea_jasa_kendaraan']
            gerai = form.cleaned_data['gerai']
            status = form.cleaned_data['status']
            comment = form.cleaned_data['comment']
            #form.save()
            #plns.update(status =1)
            ag.denda_lunas = denda
            ag.denda_kendaraan_lunas = denda_kendaraan
            ag.jasa_lunas = bea_jasa
            ag.jasa_kendaraan_lunas = bea_jasa_kendaraan
            ag.terlambat = terlambat
            ag.terlambat_kendaraan = terlambat_kendaraan
            ag.status_oto_plns = 2
            ag.nilai_lunas = nilai
            ag.save()
            ###diskon non ppap Elektronik
            if ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == 2 and ag.denda_lunas > 0 and ag.jasa_lunas > 0 \
                and ag.nilai_lunas == ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi (918)')
                jurnal_pelunasan(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=terlambat,denda = denda,bea_jasa=bea_jasa,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=0,denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=2,comment=comment,status_pelunasan = 1,sts_plns =1)
                plns.save()
            elif ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == 2 and ag.denda_lunas > 0 and ag.jasa_lunas > 0\
                and ag.nilai_lunas == ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi (931)')
                jurnal_pelunasan_none(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=terlambat,denda = denda,bea_jasa=bea_jasa,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=0,denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=2,comment=comment,status_pelunasan = 1,sts_plns =1)
                plns.save()

            ###diskon non ppap Kendaraan
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == 2 and ag.denda_kendaraan_lunas > 0 and ag.jasa_kendaraan_lunas > 0 \
                and ag.nilai_lunas == ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi (946)')
                jurnal_pelunasan_kendaraan(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=0,denda = 0,bea_jasa=0,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=terlambat_kendaraan,denda_kendaraan=denda_kendaraan,val= 0,
                    bea_jasa_kendaraan=bea_jasa_kendaraan,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=2,comment=comment,status_pelunasan = 1,sts_plns =1)
                plns.save()
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == 2 and ag.denda_kendaraan_lunas > 0 and ag.jasa_kendaraan_lunas > 0\
                and ag.nilai_lunas == ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi (959)')
                jurnal_pelunasan_none_kendaraan(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=0,denda = 0,bea_jasa=0,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=terlambat_kendaraan,denda_kendaraan=denda_kendaraan,val= 0,
                    bea_jasa_kendaraan=bea_jasa_kendaraan,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=2,comment=comment,status_pelunasan = 1,sts_plns =1)
                plns.save()

            ####denda kosong dan jasa Elektronik
            elif ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == 2 and ag.denda_lunas == 0 and ag.jasa_lunas == 0 \
                and ag.nilai_lunas == ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah lunas denda jasa diskon 1 (974)')
                jurnal_pelunasan_denda_jasa_kosong(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=terlambat,denda = denda,bea_jasa=bea_jasa,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=0,denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=2,comment=comment,status_pelunasan = 1,sts_plns =1)
                plns.save()
            elif ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == 2 and ag.denda_lunas == 0 and ag.jasa_lunas == 0\
                and ag.nilai_lunas == ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah lunas denda jasa diskon 2 (987)')
                jurnal_pelunasan_none_denda_jasa_kosong(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=terlambat,denda = denda,bea_jasa=bea_jasa,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=0,denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=2,comment=comment,status_pelunasan = 1,sts_plns =1)
                plns.save()            

            ### Denda Kosong dan Jasa Kosong Kendaraan
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == 2 and ag.denda_kendaraan_lunas == 0 and ag.jasa_kendaraan_lunas == 0 \
                and ag.nilai_lunas == ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah lunas denda jasa diskon 1 (1002)')
                jurnal_pelunasan_denda_jasa_kosong(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=0,denda =0,bea_jasa=0,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=terlambat_kendaraan,denda_kendaraan=denda_kendaraan,val= 0,
                    bea_jasa_kendaraan=bea_jasa_kendaraan,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=2,comment=comment,status_pelunasan = 1,sts_plns =1)
                plns.save()
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == 2 and ag.denda_kendaraan_lunas == 0\
                and ag.jasa_kendaraan_lunas == 0 and ag.nilai_lunas == ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah lunas denda jasa diskon 2 (1015)')
                jurnal_pelunasan_none_denda_jasa_kosong(ag, request.user)
                plns=Pelunasan(nilai=nilai,tanggal=tanggal,terlambat=0,denda =0,bea_jasa=0,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=terlambat_kendaraan,denda_kendaraan=denda_kendaraan,val= 0,
                    bea_jasa_kendaraan=bea_jasa_kendaraan,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=2,comment=comment,status_pelunasan = 1,sts_plns =1)
                plns.save()

            ###JURNAL PPAP Elektronik
            elif ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == 2 and ag.denda_lunas == 0 and ag.jasa_lunas == 0 \
                and ag.nilai_lunas < ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                plns=Pelunasan(nilai=ag.nilai_lunas,tanggal=tanggal,terlambat=terlambat,denda = 0,bea_jasa=0,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=terlambat_kendaraan,denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=2,comment=comment,status_pelunasan = 1,sts_plns =1)
                plns.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi PPAP 1 (1035)')
                jurnal_ppap(ag, request.user)
            elif ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == 2 and ag.denda_lunas == 0 and ag.jasa_lunas == 0\
                and ag.nilai_lunas < ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                plns=Pelunasan(nilai=ag.nilai_lunas,tanggal=tanggal,terlambat=terlambat,denda = 0,bea_jasa=0,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=terlambat_kendaraan,denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=2,comment=comment,status_pelunasan = 1,sts_plns =1)
                plns.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi PPAP 2 (1048)')
                jurnal_ppap_nonanggota(ag, request.user)
            ### JURNAL PPAP Kendaraan
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == 2 and ag.denda_kendaraan_lunas == 0 and ag.jasa_kendaraan_lunas == 0 \
                and ag.nilai_lunas < ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                plns=Pelunasan(nilai=ag.nilai_lunas,tanggal=tanggal,terlambat=0,denda = 0,bea_jasa=0,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=terlambat_kendaraan,denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=2,comment=comment,status_pelunasan = 1,sts_plns =1)
                plns.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi PPAP 1 (1062)')
                jurnal_ppap(ag, request.user)
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == 2 and ag.denda_kendaraan_lunas == 0 and ag.jasa_kendaraan_lunas == 0\
                and ag.nilai_lunas < ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                plns=Pelunasan(nilai=ag.nilai_lunas,tanggal=tanggal,terlambat=0,denda = 0,bea_jasa=0,pelunasan_id=ag.id,
                    jenis_barang=jenis_barang,terlambat_kendaraan=terlambat_kendaraan,denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=2,comment=comment,status_pelunasan = 1,sts_plns =1)
                plns.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi PPAP 2 (1075)')
                jurnal_ppap_nonanggota(ag, request.user)

            ###JURNAL OTORISASI JASA ELEKTRONIK 
            elif ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == 2 and ag.denda_lunas > 0 and ag.jasa_lunas == 0 \
                and ag.nilai_lunas == ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                plns=Pelunasan(nilai=ag.nilai_lunas,tanggal=tanggal,terlambat=ag.terlambat,denda = ag.denda_lunas,bea_jasa=ag.jasa_lunas,\
                    pelunasan_id=ag.id, jenis_barang=ag.barang.jenis_barang,terlambat_kendaraan=0,\
                    denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=ag.gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=2,comment=comment,status_pelunasan = 1,sts_plns =1)
                plns.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi OTO JAS (1091)')
                jurnal_diskon_jasa(ag, request.user)
            elif ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == 2 and ag.denda_lunas > 0 and ag.jasa_lunas == 0 \
                and ag.nilai_lunas == ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                plns=Pelunasan(nilai=ag.nilai_lunas,tanggal=tanggal,terlambat=ag.terlambat,denda = ag.denda_lunas,bea_jasa=ag.jasa_lunas,\
                    pelunasan_id=ag.id, jenis_barang=ag.barang.jenis_barang,terlambat_kendaraan=0,\
                    denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=ag.gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=2,comment=comment,status_pelunasan = 1,sts_plns =1)
                plns.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi Non Anggota OTO JAS 1 (1105)')
                jurnal_diskon_jasa_nonanggota(ag, request.user)
            ###JURNAL OTORISASI JASA KENDARAAN
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == 2 and ag.denda_kendaraan_lunas > 0 and ag.jasa_kendaraan_lunas == 0 \
                and ag.nilai_lunas == ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                plns=Pelunasan(nilai=ag.nilai_lunas,tanggal=tanggal,terlambat=0,denda =0,bea_jasa=0,\
                    pelunasan_id=ag.id, jenis_barang=ag.barang.jenis_barang,terlambat_kendaraan=ag.terlambat_kendaraan,\
                    denda_kendaraan=ag.denda_kendaraan_lunas,val= 0,
                    bea_jasa_kendaraan=ag.jasa_kendaraan_lunas,gerai=ag.gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=2,comment=comment,status_pelunasan = 1,sts_plns =1)
                plns.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi OTO JAS 1 (1120)')
                jurnal_diskon_jasa_kendaraan(ag, request.user)
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == 2 and ag.denda_kendaraan_lunas > 0 and ag.jasa_kendaraan_lunas == 0 \
                and ag.nilai_lunas == ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                plns=Pelunasan(nilai=ag.nilai_lunas,tanggal=tanggal,terlambat=0,denda =0,bea_jasa=0,\
                    pelunasan_id=ag.id, jenis_barang=ag.barang.jenis_barang,terlambat_kendaraan=ag.terlambat_kendaraan,\
                    denda_kendaraan=ag.denda_kendaraan_lunas,val= 0,
                    bea_jasa_kendaraan=ag.jasa_kendaraan_lunas,gerai=ag.gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=2,comment=comment,status_pelunasan = 1,sts_plns =1)
                plns.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi Non Anggota OTO JAS 1 (1134)')
                jurnal_diskon_jasa_nonanggota_kendaraan(ag, request.user)

            ###JURNAL OTORISASI DENDA Elektronik
            elif ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == 2 and ag.denda_lunas == 0 and ag.jasa_lunas > 0 \
                and ag.nilai_lunas == ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                plns=Pelunasan(nilai=ag.nilai_lunas,tanggal=tanggal,terlambat=ag.terlambat,denda =ag.denda_lunas,bea_jasa=ag.jasa_lunas,\
                    pelunasan_id=ag.id,jenis_barang=ag.barang.jenis_barang,terlambat_kendaraan=0,
                    denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=ag.gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=2,comment=comment,status_pelunasan = 1,sts_plns =1)
                plns.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi OTO DENDA 1 (1150)')
                jurnal_diskon_denda_anggota(ag, request.user)
            elif ag.jenis_transaksi == u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == 2 and ag.denda_lunas == 0 and ag.jasa_lunas > 0 \
                and ag.nilai_lunas == ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                plns=Pelunasan(nilai=ag.nilai_lunas,tanggal=tanggal,terlambat=ag.terlambat,denda =ag.denda_lunas,bea_jasa=ag.jasa_lunas,\
                    pelunasan_id=ag.id,jenis_barang=ag.barang.jenis_barang,terlambat_kendaraan=0,
                    denda_kendaraan=0,val= 0,
                    bea_jasa_kendaraan=0,gerai=ag.gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=2,comment=comment,status_pelunasan = 1,sts_plns =1)
                plns.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi Non Anggota OTO DENDA 1 (1164)')
                jurnal_diskon_denda_nonanggota(ag, request.user)
            ###JURNAL OTORISASI DENDA Kendaraan
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'1' and ag.status_oto_plns == 2 and ag.denda_kendaraan_lunas == 0 and ag.jasa_kendaraan_lunas > 0 \
                and ag.nilai_lunas == ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                plns=Pelunasan(nilai=ag.nilai_lunas,tanggal=tanggal,terlambat=0,denda =0,bea_jasa=0,\
                    pelunasan_id=ag.id,jenis_barang=ag.barang.jenis_barang,terlambat_kendaraan=ag.terlambat_kendaraan,
                    denda_kendaraan=ag.denda_kendaraan_lunas,val= 0,
                    bea_jasa_kendaraan=ag.jasa_kendaraan_lunas,gerai=ag.gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=status,comment=comment,status_pelunasan = 1)
                plns.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi OTO DENDA 1 (1179)')
                jurnal_diskon_denda_anggota_kendaraan(ag, request.user)
            elif ag.jenis_transaksi != u'1' and ag.agnasabah.jenis_keanggotaan == u'2' and ag.status_oto_plns == 2 and ag.denda_kendaraan_lunas == 0 and ag.jasa_kendaraan_lunas > 0 \
                and ag.nilai_lunas == ag.nilai:
                ag.lunas = tanggal
                ag.os_pokok = 0
                ag.status_transaksi = 1
                ag.save()
                plns=Pelunasan(nilai=ag.nilai_lunas,tanggal=tanggal,terlambat=0,denda =0,bea_jasa=0,\
                    pelunasan_id=ag.id,jenis_barang=ag.barang.jenis_barang,terlambat_kendaraan=ag.terlambat_kendaraan,
                    denda_kendaraan=ag.denda_kendaraan_lunas,val= 0,
                    bea_jasa_kendaraan=ag.jasa_kendaraan_lunas,gerai=ag.gerai,nocoa_titipan='21.03.01',nocoa_kas='11.01.04',status_kwlunas = 0,\
                    status=2,comment=comment,status_pelunasan = 1,sts_plns =1)
                plns.save()
                messages.add_message(request, messages.INFO, 'Akadgadai telah dilunasi Non Anggota OTO DENDA 1 (1193)')
                jurnal_diskon_denda_nonanggota_kendaraan(ag, request.user)

            return HttpResponseRedirect('/')
        else:
            variables = RequestContext(request, {'form_diskon': form,'ag':ag})
            return render_to_response('akadgadai/pelunasan.html', variables)

def jurnal_diskon_denda_anggota_kendaraan(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='9')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_jasa =lunas.coa_4

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id())

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        kredit = 0,debet = D(str(ag.nilai)) + ag.jasa_kendaraan_lunas ,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        debet = 0,kredit = D(str(ag.nilai)),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_jasa,
        debet = 0,kredit = ag.jasa_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_diskon_denda_nonanggota_kendaraan(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='10')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_jasa =lunas.coa_4

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id())

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        kredit = 0,debet = D(str(ag.nilai)) +  ag.jasa_kendaraan_lunas ,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        debet = 0,kredit = D(str(ag.nilai)),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_jasa,
        debet = 0,kredit =  ag.jasa_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

def jurnal_diskon_jasa_nonanggota_kendaraan(ag, user):
    D = decimal.Decimal
    lunas = AdmPelunasanMapper.objects.get(item='8')
    a_titipan_pelunasan = lunas.coa_1
    a_pinjaman_anggota = lunas.coa_2
    a_denda =lunas.coa_3

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),cu=user,mu=user,
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id())

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        kredit = 0,debet = D(str(ag.nilai_lunas)) + ag.denda_kendaraan_lunas,\
        id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        debet = 0,kredit = D(str(ag.nilai)),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        debet = 0,kredit = ag.denda_kendaraan_lunas,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)

       
def jurnal_pelunasan_diskon_denda(ag, user):
    D = decimal.Decimal
    a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
    a_pinjaman_anggota = get_object_or_404(Tbl_Akun, id=166L)
    a_denda = get_object_or_404(Tbl_Akun, id=442L)
    a_pdp_jasa = get_object_or_404(Tbl_Akun, id='416')
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm_diskon"), id_coa = a_titipan_pelunasan,
        kredit = 0,debet = ((D(ag.nilai))  + ag.lunas_jasa() + ag.lunas_denda() + ag.lunas_denda_kendaraan() + ag.lunas_bea_jasa_kendaraan()),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm_diskon"), id_coa = a_denda,
        debet = 0,kredit = ag.lunas_denda(),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm_diskon"), id_coa = a_pdp_jasa,
        debet = 0,kredit = ag.lunas_jasa(),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm_diskon"), id_coa = a_pinjaman_anggota,
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)
    
def jurnal_pelunasan_diskon_pokok(ag, user):
    D = decimal.Decimal
    a_ppap = get_object_or_404(Tbl_Akun, id=172L)
    a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
    a_pinjaman_anggota = get_object_or_404(Tbl_Akun, id=166L)
    a_denda = get_object_or_404(Tbl_Akun, id=442L)
    a_pdp_jasa = get_object_or_404(Tbl_Akun, id='416')
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        tgl_trans = ag.lunas,nobukti=ag.norek(),object_id = ag.norek_id())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm_diskon"), id_coa = a_ppap,
        kredit = 0,debet = D(ag.nilai) - D(ag.nilai_pelunasan())  ,id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm_diskon"), id_coa = a_titipan_pelunasan,
        kredit = 0,debet = D(ag.nilai_pelunasan()),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas ,
        id_cabang =ag.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm_diskon"), id_coa = a_denda,
        debet = 0,kredit = ag.lunas_denda(),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm_diskon"), id_coa = a_pdp_jasa,
        debet = 0,kredit = ag.lunas_jasa(),id_product = '4',status_jurnal ='2',tgl_trans = ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm_diskon"), id_coa = a_pinjaman_anggota,
        debet = 0,kredit = ag.nilai,id_product = '4',status_jurnal ='2',tgl_trans =ag.lunas,
        id_cabang = ag.gerai.kode_cabang,id_unit= 300)


### fungsi pelunasan gadai ###
@login_required
def kw_val(request, object_id):
    gr = AkadGadai.objects.get(id = object_id)
    template = 'akadgadai/kw_val.html'
    variable = RequestContext(request, {'gr':gr,})
    return render_to_response(template,variable)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='manop'))
def view_verifikasi_manop(request, object_id):
    ag = AkadGadai.objects.get(id=object_id)
    a = datetime.date.today()
    form = Verifikasi_ManOpForm(initial={'manop': ag.id,'tanggal': a})
    form.fields['manop'].widget = forms.HiddenInput()

    template = 'manop/verifikasi_manop.html'
    variable = RequestContext(request, {
        'ag': ag,
        'form': form})
    return render_to_response(template,variable) 
    
@login_required
@user_passes_test(lambda u: u.groups.filter(name='manop'))
def verifikasi_manop(request, object_id):
    ag = AkadGadai.objects.get(id=object_id)
    if request.method == 'POST':
        f = Verifikasi_ManOpForm(request.POST)
        if f.is_valid():
            manop = f.cleaned_data['manop']   
            tanggal = f.cleaned_data['tanggal']
            status = f.cleaned_data['status']
            note = f.cleaned_data['note']
            f = ManopGadai(manop=ag, tanggal=tanggal, status=status, note = note)
            f.save()
            if f.status == '1':
                ag.status_taksir = 1
                ag.save()
                messages.add_message(request, messages.INFO,'### PENGAJUAN DITERIMA ###')    
            else: 
                ag.status_taksir = 2
                ag.save()    
                messages.add_message(request, messages.INFO,'### PENGAJUAN DITOLAK ###')                
        return HttpResponseRedirect('/manop/')
    else:
        variables = RequestContext(request, {'object': ag, 'form': f})
        return render_to_response('manop/verifikasi_manop.html', variables)
'''
def teguran(request, object_id):
    akadgadai = AkadGadai.objects.get(id=object_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="suratteguran.pdf"'
    sekarang=datetime.datetime.now()
    h=sekarang.day
    m=sekarang.month
    y=sekarang.year
    buffer = BytesIO()
    tb=terbilang(akadgadai.terima_bersih)
    p = canvas.Canvas(buffer)
    p.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ra2.png'), 0.4*inch, (5.2 + 5.35) * inch, width=35.5/17.5*0.51*inch,height=24/17.5*0.51*inch)

    p.drawRightString(550, 800, "KSU RIZKY ABADI DIVISI PJB")
    p.drawRightString(550 , 788,"%s" % akadgadai.gerai.alamat)
    p.drawRightString(550 , 776,"%s" % akadgadai.gerai.telepon)
    p.drawRightString(550 , 765,"pjb.contactcenter@ksura.co.id")

    p.line(  30 , 760, 580 ,760  ) 
    p.setLineWidth(.3)
    p.line(  30 , 758, 580 ,758  ) 
    p.setFont('Helvetica', 10)
    p.drawRightString(550,748,"Bandung,%s" % sekarang.strftime('%d %B %Y'))
    p.drawString(30,748,"Nomor ")
    p.drawString(75,748,":         /PJB-RA/%s"% sekarang.strftime('%Y'))
    p.drawString(30,736,"Lampiran")
    p.drawString(75,736,":")    
    p.drawString(30,724,"Perihal")
    p.drawString(75,724,": SURAT TAGIHAN")    
    p.drawString(350,712,"Kepada Yth:")
    p.drawString(350,700,"Bpk/ Ibu/ Sdr/ I %s" % akadgadai.agnasabah.nama)
    p.drawString(350,688,"Di %s RT %s RW%s" % (akadgadai.agnasabah.alamat_domisili,akadgadai.agnasabah.rt_domisili,akadgadai.agnasabah.rw_domisili))
    p.drawString(30,676,"Dengan Hormat,")
    p.drawString(45,664,"Diberitahukan kepada Bpk/ Ibu/ Sdr/ i bahwa sesuai dengan  kwitansi  pencairan / perpanjangan  pinjaman sebesar")   
    p.drawString(30,652,"Rp. %s , berupa satu buah %s %s bahwa pinjaman atas nama Bpk/ Ibu/ Sdr/ i"% (number_format(akadgadai.nilai),akadgadai.barang.get_jenis_barang_display(),akadgadai.barang.merk, ))
    p.drawString(30,640,"telah jatuh tempo pada tanggal %s dan telah mengalami keterlambatan selama %s hari." %(akadgadai.jatuhtempo.strftime('%d %B %Y'),akadgadai.terlambat_tajuhtempo()))
    p.drawString(45,628,"Sesuai dengan Surat Perjanjian Pinjaman tanggal %s No %s yang telah Bpk/ Ibu/ Sdr/ i " % (akadgadai.tanggal.strftime('%d %B %Y'),akadgadai.norek()))   
    p.drawString(30,616,"tandatangani, maka koperasi akan melakukan penjualan apabila sampai dengan tanggal %s Bpk/ Ibu/ Sdr/ i" % akadgadai.tgl_jatuhtempo().strftime('%d %B %Y'))
    p.drawString(30,604,"belum juga melunasi pinjamannya.")
    p.drawString(45,592,"Demikian surat tagihan dan pemberitahuan ini kami sampaikan untuk mendapat perhatian dari Bpk/Ibu/Sdr/i.")
    p.drawString(30,580,"Atas perhatian dan kerjasamanya kami ucapkan  terimakasih.")    
    p.drawRightString(550,568,"KSU RIZKY ABADI DIVISI PJB")
    p.drawString(412,556,"Manajer Operasi")
    p.drawString(412,490,"( BANI ARVIN )")
    p.drawString(30,556,"Tanda terima surat :")
    p.drawString(30,544,"Diterima oleh .................. Tanggal .................." )
    p.drawString(30,490,"( Tanda Tangan Dan Nama Jelas)" )
 
    p.drawString(0,480,"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - " )
    p.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ra2.png'), 0.4*inch, (5.2 + 0.75) * inch, width=35.5/17.5*0.51*inch,height=24/17.5*0.51*inch)

    p.drawRightString(550, 470, "KSU RIZKY ABADI DIVISI PJB")
    p.drawRightString(550 , 458,"%s" % akadgadai.gerai.alamat)
    p.drawRightString(550 , 446,"%s" % akadgadai.gerai.telepon)
    p.drawRightString(550 , 434,"pjb.contactcenter@ksura.co.id")

    p.line(  30 ,430 , 580 ,430  ) 
    p.setLineWidth(.3)
    p.line(  30 , 427, 580 ,427  ) 
    p.setFont('Helvetica', 10)
    p.drawRightString(550,417,"Bandung,%s" % sekarang.strftime('%d %B %Y'))
    p.drawString(30,417,"Nomor ")
    p.drawString(75,417,":         /PJB-RA/%s"% sekarang.strftime('%Y'))
    p.drawString(30,402,"Lampiran")
    p.drawString(75,402,":")    
    p.drawString(30,390,"Perihal")
    p.drawString(75,390,": SURAT TAGIHAN")    
    p.drawString(350,378,"Kepada Yth:")
    p.drawString(350,366,"Bpk/ Ibu/ Sdr/ I %s" % akadgadai.agnasabah.nama)
    p.drawString(350,354,"Di %s RT %s RW %s" % (akadgadai.agnasabah.alamat_domisili,akadgadai.agnasabah.rt_domisili,akadgadai.agnasabah.rw_domisili))
    p.drawString(30,342,"Dengan Hormat,")
    p.drawString(45,330,"Diberitahukan kepada Bpk/ Ibu/ Sdr/ i bahwa sesuai dengan  kwitansi  pencairan / perpanjangan  pinjaman sebesar")   
    p.drawString(30,318,"Rp. %s , berupa satu buah %s %s bahwa pinjaman atas nama Bpk/ Ibu/ Sdr/ i"% (number_format(akadgadai.nilai),akadgadai.barang.get_jenis_barang_display(),akadgadai.barang.merk, ))
    p.drawString(30,306,"telah jatuh tempo pada tanggal %s dan telah mengalami keterlambatan selama %s hari." %(akadgadai.jatuhtempo.strftime('%d %B %Y'),akadgadai.terlambat_tajuhtempo()))
    p.drawString(45,294,"Sesuai dengan Surat Perjanjian Pinjaman tanggal %s No %s yang telah Bpk/ Ibu/ Sdr/ i " % (akadgadai.tanggal.strftime('%d %B %Y'),akadgadai.norek()))   
    p.drawString(30,282,"tandatangani, maka koperasi akan melakukan penjualan apabila sampai dengan tanggal %s Bpk/ Ibu/ Sdr/ i" % akadgadai.tgl_jatuhtempo().strftime('%d %B %Y'))
    p.drawString(30,270,"belum juga melunasi pinjamannya.")
    p.drawString(45,258,"Demikian surat tagihan dan pemberitahuan ini kami sampaikan untuk mendapat perhatian dari Bpk/Ibu/Sdr/i.")
    p.drawString(30,246,"Atas perhatian dan kerjasamanya kami ucapkan  terimakasih.")    
    p.drawRightString(550,234,"KSU RIZKY ABADI DIVISI PJB")
    p.drawString(412,222,"Manajer Operasi")
    p.drawString(412,156,"( BANI ARVIN )")
    p.drawString(30,222,"Tanda terima surat :")
    p.drawString(30,210,"Diterima oleh .................. Tanggal .................." )
    p.drawString(30,156,"( Tanda Tangan Dan Nama Jelas)" )
           
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
'''
@login_required
def teguran(request, object_id):
    usr = User.objects.get(username='manop_pjb')
    nama_manop =  usr.first_name
    usr1 = User.objects.get(username='kadiv_pjb')
    nama_kadiv =  usr1.first_name
    
    sekarang = datetime.date.today()
    akadgadai = AkadGadai.objects.get(id=object_id)
    akadgadai.status_teguran = 1
    akadgadai.no_teguran = akadgadai.nomor_teguran()
    akadgadai.save()
    tanggal_cetak = akadgadai.jatuhtempo - datetime.timedelta(1)
    
    tegur =  Teguran(agteguran = akadgadai,tanggal = sekarang, no_teg = akadgadai.no_teguran,nilai=akadgadai.nilai)
    tegur.save()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= "suratteguran_%s_%s.pdf"' % (akadgadai.agnasabah.nama,akadgadai.norek())
    sekarang=datetime.datetime.now()
    sekarang=datetime.datetime.now()
    h=sekarang.day
    m=sekarang.month
    y=sekarang.year
    buffer = BytesIO()
    tb=terbilang(akadgadai.nilai)
    p = canvas.Canvas(buffer)
    p.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ra2.png'), 0.4*inch, (5.2 + 5.35) * inch, width=35.5/17.5*0.51*inch,height=24/17.5*0.51*inch)

    p.drawRightString(550, 800, "KSU RIZKY ABADI DIVISI PJB")
    p.drawRightString(550 , 788,"%s" % akadgadai.gerai.alamat)
    p.drawRightString(550 , 776,"%s" % akadgadai.gerai.no_telp)
    p.drawRightString(550 , 765,"pjb.contactcenter@ksura.co.id")

    p.line(  30 , 760, 580 ,760  ) 
    p.setLineWidth(.3)
    p.line(  30 , 758, 580 ,758  ) 
    p.setFont('Helvetica', 10)
    p.drawRightString(550,748,"Bandung,%s" % tanggal_cetak.strftime('%d %B %Y'))
    p.drawString(30,748,"Nomor ")
    p.drawString(75,748,": %s/PJB-RA/%s"% (akadgadai.no_teguran,sekarang.strftime('%Y')))
    p.drawString(30,736,"Perihal")
    p.drawString(75,736,": SURAT PEMBERITAHUAN")
    p.drawString(30,718,"Kepada Yth:")
    p.drawString(30,706,"Bpk/ Ibu/ Sdr/ I %s" % akadgadai.agnasabah.nama)
    p.drawString(30,694,"Di %s No %s RT %s RW %s Kel %s"% (akadgadai.agnasabah.alamat_domisili,akadgadai.agnasabah.no_rumah_domisili,akadgadai.agnasabah.rt_domisili,akadgadai.agnasabah.rw_domisili,akadgadai.agnasabah.kelurahan_domisili))
    p.drawString(30,682,"Kec %s Kota Madya %s Kab %s " % (akadgadai.agnasabah.kecamatan_domisili,akadgadai.agnasabah.kotamadya_domisili,akadgadai.agnasabah.kabupaten_domisili))
    p.drawString(30,666,"Dengan Hormat,")
    p.drawString(30,650,"Dengan ini diberitahukan kepada Bpk/Ibu/Sdr/i bahwa sesuai dengan kwitansi pinjaman/perpanjangan pinjaman sebesar,")   
    p.drawString(30,638,"Rp. %s , (%s Rupiah) dengan jaminan berupa barang: "  % ((number_format(akadgadai.nilai)),tb.title()))
    p.drawString(30,626,"%s %s akan segera jatuh tempo pada tanggal %s." % ((akadgadai.jenis_barang_all(),akadgadai.merk_all(),akadgadai.jatuhtempo.strftime('%d %B %Y'))))
    #p.drawString(30,630,"akan segera jatuh tempo pada tanggal %s." %(akadgadai.jatuhtempo.strftime('%d %B %Y')))
    #p.drawString(45,618,"akan segera jatuh tempo pada tanggal %s." %(akadgadai.jatuhtempo.strftime('%d %B %Y')))
    p.drawString(30,610,"Sesuai dengan Surat Perjanjian Pinjaman tanggal %s No %s" % (akadgadai.tanggal.strftime('%d %B %Y'),akadgadai.norek()))
    p.drawString(440,610,"   yang telah Bpk/Ibu/Sdr/i" )      
    p.drawString(30,598,"tandatangani, berikut kami sampaikan kembali bahwa apabila sampai dengan tanggal")      
    p.drawString(415,598,"%s" % akadgadai.tgl_jatuhtempo().strftime('%d %B %Y'))
    p.drawString(30,586,"Bpk/ Ibu/ Sdr/ i belum melunasi pinjamannya, maka secara otomatis  Bpk/Ibu/Sdr/i telah  setuju untuk mengalihkan status" )
    p.drawString(30,574,"kepemilikan barang atas nama Bpk/Ibu/Sdr/i menjadi milik Koperasi Rizky Abadi.")

    p.drawString(30,558,"Demikian  surat  pemberitahuan  ini  kami  sampaikan  untuk  mendapat  perhatian  dari Bpk/Ibu/Sdr/i. Atas perhatian dan")
    p.drawString(30,546,"kerjasamanya kami ucapkan  terima kasih.")    
    p.drawString(412,530,"KSU RIZKY ABADI UNIT PJB")
    p.drawString(412,518,"Assisten Manajer Operasi")
    # BUAT YANG NANA NYA PANJANG p.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ttd_manop.png'), 5.7*inch, (1.7 + 4.75) * inch, width=60.5/17.5*0.51*inch,height=24/17.5*0.51*inch)      
    p.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ttd_manop.png'), 5.5*inch, (1.7 + 4.75) * inch, width=60.5/17.5*0.51*inch,height=24/17.5*0.51*inch) 
    p.drawString(412,458,"( %s )" % nama_manop)
    p.drawString(30,518,"Tanda terima surat :")
    p.drawString(30,506,"Diterima oleh .................. Tanggal .................." )
    p.setFont('Helvetica', 8)
    p.drawString(30,494,"( Sesuai lembar bukti pengiriman surat)" )
    p.setFont('Helvetica', 10)
    p.drawString(30,458,"( Tanda Tangan Dan Nama Jelas)" )
    p.setFont('Helvetica', 8)
    p.drawString(30,449,"- Asli -" )
    
    p.drawString(0,442,"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - " )
    p.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ra2.png'), 0.4*inch, (5.2 + 0.20) * inch, width=35.5/17.5*0.51*inch,height=24/17.5*0.51*inch)
    p.drawRightString(550, 426, "KSU RIZKY ABADI DIVISI PJB")
    p.drawRightString(550 , 414,"%s" % akadgadai.gerai.alamat)
    p.drawRightString(550 , 402,"%s" % akadgadai.gerai.no_telp)
    p.drawRightString(550 , 390,"pjb.contactcenter@ksura.co.id")

    p.line(  30 ,385 , 580 ,385  ) 
    p.setLineWidth(.3)
    p.line(  30 , 383, 580 ,383  ) 
    p.setFont('Helvetica', 10)
    p.drawRightString(550,373,"Bandung,%s" % tanggal_cetak.strftime('%d %B %Y'))
    p.drawString(30,373,"Nomor ")
    p.drawString(75,373,": %s/PJB-RA/%s"% (akadgadai.no_teguran,sekarang.strftime('%Y')))
    p.drawString(30,361,"Perihal")
    p.drawString(75,361,": SURAT PEMBERITAHUAN")

    p.drawString(30,343,"Kepada Yth:")
    p.drawString(30,331,"Bpk/ Ibu/ Sdr/ I %s" % akadgadai.agnasabah.nama)
    p.drawString(30,319,"Di %s No %s RT %s RW %s Kel %s"% (akadgadai.agnasabah.alamat_domisili,akadgadai.agnasabah.no_rumah_domisili,akadgadai.agnasabah.rt_domisili,akadgadai.agnasabah.rw_domisili,akadgadai.agnasabah.kelurahan_domisili))
    p.drawString(30,307,"Kec %s Kota Madya %s Kab %s " % (akadgadai.agnasabah.kecamatan_domisili,akadgadai.agnasabah.kotamadya_domisili,akadgadai.agnasabah.kabupaten_domisili))
    p.drawString(30,291,"Dengan Hormat,")
    p.drawString(30,275,"Dengan ini diberitahukan kepada Bpk/Ibu/Sdr/i bahwa sesuai dengan kwitansi pinjaman/perpanjangan pinjaman sebesar,")   
    p.drawString(30,263,"Rp. %s , (%s Rupiah) dengan jaminan berupa barang: "  % ((number_format(akadgadai.nilai)),tb.title()))
    p.drawString(30,251,"%s %s akan segera jatuh tempo pada tanggal %s." % ((akadgadai.jenis_barang_all(),akadgadai.merk_all(),akadgadai.jatuhtempo.strftime('%d %B %Y'))))
    p.drawString(30,235,"Sesuai dengan Surat Perjanjian Pinjaman tanggal %s No %s" % (akadgadai.tanggal.strftime('%d %B %Y'),akadgadai.norek()))
    p.drawString(440,235,"      yang telah Bpk/Ibu/Sdr/i" )      
    p.drawString(30,223,"tandatangani, berikut kami sampaikan kembali bahwa apabila sampai dengan tanggal")      
    p.drawString(415,223,"%s" % akadgadai.tgl_jatuhtempo().strftime('%d %B %Y'))
    p.drawString(30,211,"Bpk/ Ibu/ Sdr/ i belum melunasi pinjamannya, maka secara otomatis  Bpk/Ibu/Sdr/i telah  setuju untuk mengalihkan status" )
    p.drawString(30,199,"kepemilikan barang atas nama Bpk/Ibu/Sdr/i menjadi milik Koperasi Rizky Abadi.")

    p.drawString(30,183,"Demikian  surat  pemberitahuan  ini  kami  sampaikan  untuk  mendapat  perhatian  dari Bpk/Ibu/Sdr/i. Atas perhatian dan")
    p.drawString(30,171,"kerjasamanya kami ucapkan  terima kasih.")    
    p.drawString(412,155,"KSU RIZKY ABADI UNIT PJB")
    p.drawString(412,143,"Assisten Manajer Operasi")
    #BUAT YANG NAMANYA PANJANG p.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ttd_manop.png'), 5.7*inch, (-4.1 + 5.35) * inch, width=60.5/17.5*0.51*inch,height=24/17.5*0.51*inch)         
    p.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ttd_manop.png'), 5.5*inch, (-4.1 + 5.35) * inch, width=60.5/17.5*0.51*inch,height=24/17.5*0.51*inch)

    p.drawString(412,83,"( %s )" % nama_manop)
    p.drawString(30,143,"Tanda terima surat :")
    p.drawString(30,131,"Diterima oleh .................. Tanggal .................." )
    p.setFont('Helvetica', 8)
    p.drawString(30,119,"( Sesuai lembar bukti pengiriman surat)" )
    p.setFont('Helvetica', 10)
    p.drawString(30,83,"( Tanda Tangan Dan Nama Jelas)" )
    p.setFont('Helvetica', 8)
    p.drawString(30,71,"- Salinan -" )
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

'''##jatuh Tempo Akad Gadai Elektronik All
def hitung_jatuhtempo_elektronik_all(request):
    akad = AkadGadai.objects.filter(jenis_transaksi=1)
    for hitung in akad:
        hitung.jatuhtempo = hitung.jatuhtempo_hitung()
        hitung.save()
    variable = RequestContext(request,{'akad': akad})
    return render_to_response(variable)

##jatuh Tempo Akad Gadai Kendaraan All
def hitung_jatuhtempo_kendaraan_all(request):
    akad = AkadGadai.objects.filter(jenis_transaksi=2)
    for hitung in akad:
        hitung.jatuhtempo = hitung.jatuh_tempo_kendaraan_hitung()
        hitung.save()
    variable = RequestContext(request,{'akad': akad})
    return render_to_response(variable)

##jatuh Tempo Perpanjang 1 Elektronik 
def hitung_jatuhtempo_perpanjang_1_elektronik(request):
    akad = AkadGadai.objects.filter(perpanjang__status=u'P1').filter(jenis_transaksi=1)
    for hitung in akad:
        hitung.jatuhtempo = hitung.prpj_jatuhtempo()
        hitung.save()
    variable = RequestContext(request,{'akad': akad})
    return render_to_response(variable)
'''
##jatuh Tempo Perpanjang 2 Kendaraan
@login_required
def hitung_jatuhtempo_perpanjang_2_kendaraan(request):
    akad = AkadGadai.objects.filter(perpanjang__status=u'P2').filter(jenis_transaksi=2)
    for hitung in akad:
        hitung.jatuhtempo = hitung.prpj_jatuhtempo_kendaraan()
        hitung.save()
    variable = RequestContext(request,{'akad': akad})
    return render_to_response(variable)

@login_required
def akad_terbit_bulan_csv(request, year, month):
    ''' Tampilkan Akad pada bulan/tahun terpilih dalam format CSV '''
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=akadgadai_%s_%s.csv' % (year, month)
    writer = csv.writer(response)
    writer.writerow(['No Rek','Tgl Akad','Nama','JW','JW Kendaraan','No KTP','Telepon','HP','Alamat','Barang','Jenis Barang','Nilai Pinjaman','Bea Jasa', 'Bea Simpan','Adm','Gerai','Adm Gerai'])
    for p in AkadGadai.objects.filter(tanggal__year=year).filter(tanggal__month=month):
        writer.writerow([p.norek(), p.tanggal, p.agnasabah.nama,p.jangka_waktu,p.jangka_waktu_kendaraan, p.agnasabah.no_ktp, p.agnasabah.telepon_ktp, p.agnasabah.hp_ktp, p.agnasabah.alamat_ktp, p.barang, p.barang.jenis_barang, p.nilai, p._get_jasa(), p._get_biayasimpan(), p._get_adm(), p.gerai, p.cu])
    return response
@login_required    
def prpj_terbit_bulan_csv(request, year, month):
    ''' Tampilkan Perpanjangan pada bulan/tahun terpilih dalam format CSV '''
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=perpanjangan_%s_%s.csv' % (year, month)
    writer = csv.writer(response)
    writer.writerow(['No Rek','Tgl Perpanjangan','Nama','No KTP','Telepon','HP','Alamat','Barang','Jenis Barang','jw','jw_kendaraan','Nilai Pinjaman','Terlambat Hari','Bea Jasa', 'Bea Simpan','Gerai','Adm Gerai','Terlambat'])
    for p in Perpanjang.objects.filter(tanggal__year=year).filter(tanggal__month=month):
        writer.writerow([p.agkredit.norek(), p.tanggal,p.agkredit.agnasabah.nama, p.agkredit.agnasabah.no_ktp, p.agkredit.agnasabah.telepon_ktp, p.agkredit.agnasabah.hp_ktp, p.agkredit.agnasabah.alamat_ktp, p.agkredit.barang, p.agkredit.barang.jenis_barang,p.agkredit.jangka_waktu, p.agkredit.jangka_waktu_kendaraan, p.agkredit.nilai, p.terlambat, p.bea_jasa(), p.bea_simpan, p.agkredit.gerai, p.agkredit.cu,p.terlambat])
    return response

@login_required
def pelunasan_terbit_bulan_csv(request, year, month):
    ''' Tampilkan Pelunasan pada bulan/tahun terpilih dalam format CSV '''
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=pelunasan_%s_%s.csv' % (year, month)
    writer = csv.writer(response)
    writer.writerow(['No Rek','Tgl Pelunasan','Nama','No KTP','Telepon','HP','Alamat','Barang','Jenis Barang','Nilai Pinjaman','Terlambat Hari','Bea Jasa', 'Denda','Gerai','Adm Gerai'])
    #ag = AkadGadai.objects.all()
    for p in Pelunasan.objects.filter(tanggal__year=year).filter(tanggal__month=month):
        writer.writerow([p.pelunasan.norek(), p.tanggal, p.pelunasan.agnasabah.nama, p.pelunasan.agnasabah.no_ktp, p.pelunasan.agnasabah.telepon_ktp, p.pelunasan.agnasabah.hp_ktp, p.pelunasan.agnasabah.alamat_ktp, p.pelunasan.barang, p.pelunasan.barang.jenis_barang, p.nilai, p.terlambat, p.bea_jasa, p.denda, p.pelunasan.gerai, p.pelunasan.cu])
    return response


@login_required
def list(request):
    akad = AkadGadai.objects.all()
    paginator = Paginator(akad, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        akad = paginator.page(page)
    except (EmptyPage, InvalidPage):
        akad = paginator.page(paginator.num_pages)

    template='akadgadai/index.html'
    variable = RequestContext(request,{'akad': akad})
    return render_to_response(template,variable)

@login_required
def perpanjang(request, object_id):
    ag = AkadGadai.objects.get(id=object_id)
    if request.method == 'POST':
        f = PerpanjangForm(request.POST)
        if f.is_valid():
            agkredit = f.cleaned_data['agkredit']
            tanggal= f.cleaned_data['tanggal']
            jenis_barang = f.cleaned_data['jenis_barang']
            status = f.cleaned_data['status']
            gerai =f.cleaned_data['gerai']
            ###ELEKTRONIK
            terlambat=f.cleaned_data['terlambat']
            #denda = f.cleaned_data['denda']
            bea_simpan = f.cleaned_data['bea_simpan']
            #bea_jasa = f.cleaned_data['bea_jasa']
            #bea_jasa_terlambat = f.cleaned_data['bea_jasa_terlambat']
            jw = f.cleaned_data['jw']
            hitung_hari = f.cleaned_data['hitung_hari']            
            ###kendaraan
            jw_kendaraan = f.cleaned_data['jw_kendaraan']
            terlambat_kendaraan = f.cleaned_data['terlambat_kendaraan']
            #denda_kendaraan = f.cleaned_data['denda_kendaraan']
            beasimpan_kendaraan = f.cleaned_data['beasimpan_kendaraan']
            nilai = f.cleaned_data['nilai']          
            hitung_hari_kendaraan = f.cleaned_data['hitung_hari_kendaraan'] 
            bunga_denda = f.cleaned_data['bunga_denda']
            bunga_jasa = f.cleaned_data['bunga_jasa']
            prj =Perpanjang(agkredit = agkredit,tanggal= tanggal, jenis_barang =jenis_barang, status = status, gerai =gerai,terlambat=terlambat,
                bea_simpan = bea_simpan, jw = jw, hitung_hari = hitung_hari, jw_kendaraan = jw_kendaraan,
                terlambat_kendaraan = terlambat_kendaraan, beasimpan_kendaraan = beasimpan_kendaraan,nilai=nilai,bunga_denda=bunga_denda,bunga_jasa =bunga_jasa,
                hitung_hari_kendaraan = hitung_hari_kendaraan)
            prj.save()
            ag.jatuhtempo = prj.coba_jt_prpj()           
            ag.save()         
            messages.add_message(request, messages.INFO, 'Data Perpanjangan Telah berhasil simpan.')
        return HttpResponseRedirect(ag.get_absolute_url())
    else:
        sekarang = datetime.datetime.now()
        f = PerpanjangForm(initial={'agkredit': ag.id,'jenis_barang': ag.jenis_transaksi,
            'gerai': ag.gerai.id,
            'tanggal': sekarang.date,
            'nilai': ag.nilai,'bea_simpan':ag.biayasimpan,'beasimpan_kendaraan':ag.beasimpan_kendaraan})
        f.fields['agkredit'].widget = forms.HiddenInput()
        variables = RequestContext(request,{'object': ag,'form':f})
        return render_to_response('akadgadai/perpanjang.html',variables)

@login_required
def show(request,object_id):
    ag = AkadGadai.objects.get(id=object_id)
    sekarang = datetime.datetime.now()
    skr = datetime.date.today()
    titip = TitipanPelunasan.objects.filter(norek = object_id)
    total_titip = sum([a.nilai for a in titip])
    form = PelunasanForm(initial={'pelunasan': ag.id, 
        'gerai': ag.gerai.id,
        'tanggal': sekarang.date,
        'nilai': ag.nilai,
        'skr':skr})

    template = 'akadgadai/show.html'
    variable = RequestContext(request, {
        'ag': ag,'form': form,'skr':skr,'total_titip':total_titip,'titip':titip})
    return render_to_response(template,variable)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='ADM_GERAI'))
def add(request):
    skr = datetime.date.today()
    user = request.user
    D = decimal.Decimal
    if request.method == "POST":
        form = AGForm(request.POST,request.FILES)
        if form.is_valid():
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
                
            agnasabah = Nasabah(nama=nama,tgl_lahir=tgl_lahir,tempat=tempat,no_ktp=no_ktp,alamat_ktp=alamat_ktp,jenis_keanggotaan = jenis_keanggotaan,
                rt_ktp=rt_ktp,rw_ktp=rw_ktp,telepon_ktp=telepon_ktp,hp_ktp=hp_ktp,kelurahan_ktp=kelurahan_ktp,\
                jenis_pekerjaan=jenis_pekerjaan,alamat_kantor=alamat_kantor,
                kode_pos=kode_pos,telepon_kantor=telepon_kantor,email=email,jenis_kelamin=jenis_kelamin,\
                kotamadya_ktp=kotamadya_ktp,no_rumah_ktp=no_rumah_ktp,
                kabupaten_ktp=kabupaten_ktp,kecamatan_ktp=kecamatan_ktp,alamat_domisili = alamat_domisili,rt_domisili= rt_domisili,\
                rw_domisili= rw_domisili,telepon_domisili = telepon_domisili,kelurahan_domisili = kelurahan_domisili,\
                kecamatan_domisili = kecamatan_domisili,
                kotamadya_domisili = kotamadya_domisili,kabupaten_domisili = kabupaten_domisili,no_rumah_domisili=no_rumah_domisili,
                nama_pasangan = nama_pasangan,alamat_pasangan = alamat_pasangan,jekel_pasangan = jekel_pasangan,tlp_pasangan = tlp_pasangan,
                no_rumah_pas = no_rumah_pas, no_rt_pas = no_rt_pas, no_rw_pas = no_rw_pas)
            agnasabah.save()
            barang = Barang(sn=sn,warna=warna,tahun_pembuatan=tahun_pembuatan,bulan_produksi=bulan_produksi,fungsi_sistem=fungsi_sistem,
                lampiran_dokumen=lampiran_dokumen,accesoris_barang1=accesoris_barang1,jenis_barang=jenis_barang,
                merk_kendaraan=merk_kendaraan,no_polisi=no_polisi,no_rangka=no_rangka,no_mesin=no_mesin,warna_kendaraan=warna_kendaraan,
                no_bpkb=no_bpkb,stnk_atas_nama=stnk_atas_nama,no_faktur=no_faktur,jenis_kendaraan=jenis_kendaraan,
                type_kendaraan=type_kendaraan,\
                charger=charger,kondisi_charger=kondisi_charger,batre=batre,kondisi_batre=kondisi_batre,keybord=keybord,
                kondisi_keybord=kondisi_keybord,cassing=cassing,kondisi_cassing = kondisi_cassing,layar=layar,
                kondisi_layar=kondisi_layar,lensa=lensa,kondisi_lensa=kondisi_lensa,optik_ps=optik_ps,kondisi_optik_ps=kondisi_optik_ps,
                
                layar_tv=layar_tv,kondisi_layar_tv = kondisi_layar_tv,
                harddisk = harddisk,kondisi_harddisk = kondisi_harddisk,stick  = stick,kondisi_stick = kondisi_stick,hdmi  = hdmi,kondisi_hdmi = kondisi_hdmi,
                remote = remote,kondisi_remote = kondisi_remote,dus = dus,tas = tas,
                batre_kamera = batre_kamera,kondisi_batre_kamera = kondisi_batre_kamera,cassing_kamera = cassing_kamera,
                kondisi_cassing_kamera = kondisi_cassing_kamera,password = password,password_barang =password_barang,akad_ulang=0,buka_tutup_gu =99)
            barang.save()
            
            ag = AkadGadai (tanggal = skr,agnasabah=agnasabah, gerai=user.profile.gerai, jangka_waktu=jangka_waktu,bea_materai=bea_materai,status_kw = '0',
                nilai=nilai,cu=request.user, mu=request.user,taksir=taksir,barang=barang,jangka_waktu_kendaraan=jangka_waktu_kendaraan,
                jenis_transaksi=jenis_transaksi,status_transaksi=3,selisih_pelunasan = 0,jasa_lunas=0,denda_lunas=0,jns_gu=0,
                jasa_kendaraan_lunas=0,denda_kendaraan_lunas=0,terlambat=0,terlambat_kendaraan=0,nilai_lunas=0)
            if ag.jenis_transaksi != u'1':
                    ag.pilih_jasa = 1
                    ag.save()

            if  ag.jenis_transaksi == u'1' and ag.nilai > ag.taksir.maxpinjaman and ag.agnasabah.jenis_keanggotaan == u'1':
                ag.status_taksir = 2
                ag.asumsi_jasa = round(ag.asumsi_pendapatan_jasa())
                ag.os_pokok = ag.nilai
                ag.jatuhtempo = ag.menu_hitung_jt()
                ag.nilai_adm = D(ag.adm)
                ag.nilai_jasa = D(round(ag.jasa))
                ag.nilai_biayasimpan = D(ag.biayasimpan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                ag.jns_gu = 0
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
                ag.jns_gu = 0
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
                ag.jns_gu = 0
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
                ag.jns_gu = 0
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
                ag.jns_gu = 0
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
                ag.jns_gu = 0
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
                ag.nilai_biayasimpan = (ag.biayasimpan)
                ag.nilai_asuransi = 0
                ag.nilai_provisi = 0
                ag.jns_gu = 0
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
                ag.jns_gu = 0
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
        form.fields['pilih_jasa'].widget = forms.HiddenInput()
        #form.fields['gerai'].queryset = Tbl_Cabang.objects.for_user(user) 
    variables = RequestContext(request, {'form': form,'pilih_jasa':2})
    return render_to_response('akadgadai/akadnasabah.html', variables)

def jurnal_pencairan(ag, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_pinjaman = get_object_or_404(Tbl_Akun, id=163L)
    a_pdp_adm = get_object_or_404(Tbl_Akun, id='430')
    a_pdp_jasa = get_object_or_404(Tbl_Akun, id='383')
    a_pdp_bea_simpan = get_object_or_404(Tbl_Akun, id='429')
    a_pdp_bea_materai = get_object_or_404(Tbl_Akun, id='608')
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),tgl_trans =ag.tanggal,nobukti=ag.norek(),
        object_id=ag.norek_id())
    
    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pinjaman,
        debet = ag.nilai,kredit = 0,
        deskripsi ='Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        id_product = '4',status_jurnal ='1',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)
    
    
    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pdp_adm,
        deskripsi='Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = D(float(ag.adm_all())),
        id_product = '4',status_jurnal ='1',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pdp_bea_materai,
        deskripsi='Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit = D(float(ag.bea_materai)),
        id_product = '4',status_jurnal ='1',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)

    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_jasa,no_trans = no_trans,
        debet = 0,kredit =  D(float(ag.jasa_all())),
        deskripsi='Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        id_product = '4',status_jurnal ='1',
        id_cabang = ag.gerai.kode_cabang,tgl_trans =ag.tanggal,id_unit= 300)

    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_bea_simpan,
        deskripsi='Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0,kredit =  D(float(ag.beasimpan_all())),
        id_product = '4',status_jurnal ='1',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_titipan_pencairan,
        deskripsi='Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0 ,  kredit = round(D(ag.nilai) - D(ag.adm_all()) - ag.jasa_all() - ag.beasimpan_all()),
        id_product = '4',status_jurnal ='1',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)

def jurnal_pencairan_nonanggota(ag, user):
    D = decimal.Decimal
    a_titipan_pencairan = get_object_or_404(Tbl_Akun, id=298L)
    a_pinjaman = get_object_or_404(Tbl_Akun, id=166L)
    a_pdp_adm = get_object_or_404(Tbl_Akun, id='432')
    a_pdp_jasa = get_object_or_404(Tbl_Akun, id='383')
    a_pdp_bea_simpan = get_object_or_404(Tbl_Akun, id='429')
    a_pdp_bea_materai = get_object_or_404(Tbl_Akun, id='608')
   
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),tgl_trans =ag.tanggal,nobukti=ag.norek(),
        object_id=ag.norek_id())
    
    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pinjaman,
        debet = ag.nilai,kredit = 0,
        deskripsi= 'Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        id_product = '4',status_jurnal ='1',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pdp_adm,
        debet = 0,kredit = D(float(ag.adm_all())),deskripsi= 'Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        id_product = '4',status_jurnal ='1',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_jasa,
        debet = 0,kredit =  D(float(ag.jasa_all())),
        deskripsi= 'Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        id_product = '4',status_jurnal ='1',
        id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = 'Pencairan', id_coa = a_pdp_bea_materai,
        debet = 0,kredit = D(float(ag.bea_materai)),
        deskripsi= 'Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        id_product = '4',status_jurnal ='1',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_pdp_bea_simpan,
        debet = 0,kredit =  D(float(ag.beasimpan_all())),
        deskripsi= 'Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        id_product = '4',status_jurnal ='1',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pencairan"), id_coa = a_titipan_pencairan,
        deskripsi= 'Penc: NoRek: %s an: %s  ' % (ag.norek(), ag.agnasabah.nama),
        debet = 0 , kredit = round(D(ag.nilai) - D(ag.adm_all()) - ag.jasa_all() - ag.beasimpan_all()),#D(ag.jasa_all()) 
        id_product = '4',status_jurnal ='1',id_cabang =ag.gerai.kode_cabang,tgl_trans =ag.tanggal,
        id_unit= 300)

@login_required
def baru(request):
    if request.method == "POST":
        D = decimal.Decimal
        form = AkadForm(request.POST)
        if form.is_valid():
            agnasabah = form.cleaned_data['agnasabah']
            tanggal = form.cleaned_data['tanggal']
            gerai = form.cleaned_data['gerai']
            jenis_transaksi = form.cleaned_data['jenis_transaksi']
            taksir = form.cleaned_data['taksir'] 
            jangka_waktu = form.cleaned_data['jangka_waktu']
            nilai = form.cleaned_data['nilai']
            jenis_kendaraan = form.cleaned_data['jenis_kendaraan']
            barang = form.cleaned_data['barang']
            jangka_waktu_kendaraan = form.cleaned_data['jangka_waktu_kendaraan']
            bea_materai = form.cleaned_data['bea_materai']
            
            akad = AkadGadai (tanggal = tanggal,agnasabah=agnasabah, gerai=gerai, jangka_waktu=jangka_waktu,
                nilai=nilai,cu=request.user, mu=request.user,taksir=taksir,barang=barang,
                bea_materai=bea_materai, jangka_waktu_kendaraan=jangka_waktu_kendaraan,
                jenis_transaksi=jenis_transaksi)
  
            if  akad.jenis_transaksi == u'1' and akad.nilai > akad.taksir.maxpinjaman:
                akad.status_taksir = 2
                akad.jatuhtempo = ag.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(akad.jasa)
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nocoa_titipan = '21.05.01'
                akad.nocoa_kas = '11.01.04'
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                akad.save()
            elif akad.jenis_transaksi == u'2' and akad.nilai > akad.taksir.maxpinjaman:
                akad.status_taksir = 2
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(akad.jasa_kendaraan)
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nocoa_titipan = '21.05.01'
                akad.nocoa_kas = '11.01.04'
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Melebihi Nilai Taksir')
                akad.save()
            elif akad.jenis_transaksi == u'1' and akad.nilai <=  akad.taksir.maxpinjaman:
                akad.status_taksir = 1
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm = D(akad.adm)
                akad.nilai_jasa = D(akad.jasa)
                akad.nilai_biayasimpan = D(akad.biayasimpan)
                akad.nocoa_titipan = '21.05.01'
                akad.nocoa_kas = '11.01.04'
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
                
            elif akad.jenis_transaksi == u'2' and akad.nilai <= akad.taksir.maxpinjaman:
                akad.status_taksir = 1
                akad.jatuhtempo = akad.menu_hitung_jt()
                akad.nilai_adm_kendaraan = D(akad.adm_kendaraan)
                akad.nilai_jasa_kendaraan = D(akad.jasa_kendaraan)
                akad.nilai_beasimpan_kendaraan = D(akad.beasimpan_kendaraan)
                akad.nocoa_titipan = '21.05.01'
                akad.nocoa_kas = '11.01.04'
                messages.add_message(request, messages.INFO, 'Nilai Pinjaman Sesuai Nilai Taksir')
                akad.save()
            jurnal_pencairan(akad, request.user)            
            return HttpResponseRedirect('/')
    else:
        form = Akadform()
    template='nasabah/addnasabah.html'
    variable = RequestContext(request, {'form':form})
    return render_to_response(template,variable)


def tterima(request,object_id):
    akadgadai = AkadGadai.objects.get(id=object_id)
    #barang = Barang.objects.get(id=object_id)
    #gerai = GeraiGadai.objects.get(id=object_id)
    akadgadai.sts_tdr = '1'
    akadgadai.save()
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


        trk=akadgadai.tanggal
        dd=patokan.month-trk.month
        yy=patokan.year-trk.year

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= "kuitansi_%s.pdf"' % akadgadai.norek()
    
    c = canvas.Canvas(response, pagesize=(9.5*inch, 11*inch))

    header0=(8.25 *inch, (5.2 + 5.5) * inch)
    header1=(4.60 *inch, (5.35 + 5.5) * inch)
    colom1 = (0.3*inch, (4.35 + 5.5) *inch)
    colom2 = (6.3*inch, (4.35 + 5.5) *inch)
    colom3 = (6.3*inch, (4.3 + 4.5) *inch)
    
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ra2.png'), 0.5*inch, (4.8 + 5.5) * inch, width=24.5/17.5*0.51*inch,height=24/17.5*0.51*inch)

    x,y = header0
    y1 = 0.126* inch
    c.setFont("Courier", 7)
    #c.drawString(x-0.02*inch, y+0.2, "[kowil][koger][%b] [akadgadai.mu]"); y -=2*y1
    #c.drawString(x-0.02*inch, y+0.2*inch,    "( %s )"% (akadgadai.agnasabah.nama)  ); y -=y1
    c.drawString(x+0.02*inch, y+0.2*inch, "%s" % sekarang.strftime('[%-b][%Y]') ); y -= y1

    x,y = header1
    y1 = 0.10* inch
    c.setFont("Courier-Bold", 14)
    c.drawString(x-1.9*inch, y, "TANDA TERIMA BARANG JAMINAN" ); y -=1.5*y1
    c.setFont("Courier-Bold", 10)
    c.drawString(x-3.1*inch, y,"Badan Hukum No.518/BH.88-Diskop/THN.2007 Tgl 27 Desember 2007 "); y -=1.5*y1
    c.setFont("Courier-Bold", 10)
    c.drawString(x-1.1*inch, y, "GERAI [%s]"% (akadgadai.gerai.nama)); y -=1.5*y1
    c.drawString(x-1.9*inch, y, "%s/Telp: %s"% (akadgadai.gerai.alamat, akadgadai.gerai.telepon)); y -=y1
    #c.line( 0.53 * inch , y , 7.75 * inch , y ) ; y -=2*y1
    #c.setFont("Courier-Bold", 14)

    x,y = colom1
    y1 = 0.100 * inch

    tb=terbilang(akadgadai.terima_bersih)

    c.setFont("Courier-Bold", 10)
    c.drawString(x, y, "Telah terima dari   : %s" % (akadgadai.agnasabah.nama)); y -= 1.2*y1
    c.drawString(x, y, "Nomor Kwitansi      : %s" % (akadgadai.norek())); y -=1.5*y1
    c.drawString(x, y, "No.KTP              : %s" % (akadgadai.agnasabah.no_ktp)); y -=1.5*y1
    c.drawString(x, y, "Barang jaminan, sebagai berikut :  " ); y -= 1.5*y1
    c.drawString(x, y, "1.  %s %s"% (akadgadai.barang.merk,akadgadai.barang.type, )); y -=1.5* y1
    c.drawString(0.2*inch, y-0.4*inch, "Diserahkan pada tanggal: %s" % sekarang.strftime('%d-%-b-%Y') ); y -= y1
    c.drawString(4.0*inch, y-0.3*inch, "Dikembalikan pada tanggal:" ); y -= 1.5*y1
   
    y -=  3 * y1
    y2 = y + 0.1 * inch
    c.setFont("Courier-Bold", 11)
    c.line( 0.2 * inch , y2 , 7.7 * inch , y2 );
   
    
    y -= y1
    c.setFont("Courier-Bold", 9)
    c.drawString(0.3*inch, y-0.1*inch,  "DEBITUR"); y -= y1
    c.line( 2.3* inch , y , 5.7 * inch , y );
    c.drawString(x+2.1*inch, y+0.1*inch,  "YANG MENERIMA"); y -= y1
    c.drawString(x+2.1*inch, y-0.0*inch,  "GERAI %s"% (akadgadai.gerai.nama)); y -= y1
    c.line( 0.2* inch , y , 7.7 * inch , y );y -= y1
    c.drawString(x+3.8*inch, y+0.4*inch,  "YANG MENYERAHKAN"); y -= y1
    c.drawString(x+3.8*inch, y+0.3*inch,  "GERAI %s"% (akadgadai.gerai.nama)); y -= y1
    c.drawString(x+5.5*inch, y+0.5*inch,  "DEBITUR"); y -= y1
    
    c.setFont("Courier-Bold", 8)
    c.drawString(x+3.8*inch, y-0.4*inch,  "%s"%(akadgadai.cu)); y -= y1
    c.drawString(x+5.5*inch, y-0.3*inch,  "%s"% (akadgadai.agnasabah.nama)); y -= y1
    c.line( 0.2* inch , y , 7.7 * inch , y ); y -= y1
    c.setFont("Courier-Bold", 8)
    c.drawString(x+2.1*inch, y-0.1*inch,  "%s"%(akadgadai.cu)); y -= y1
    c.drawString(0.3*inch, y-0.0*inch,  "%s"% (akadgadai.agnasabah.nama)); y -= y1
    
    c.line( 0.2* inch , y2 , 0.2 * inch , y );
    c.line( 4.0 * inch , y2 , 4.0  * inch , y );
    c.line( 2.3 * inch , y2 , 2.3  * inch , y  );
    c.line( 0.2* inch , y , 7.7 * inch , y );
    c.line( 5.7 * inch , y2 , 5.7  * inch , y  );
    c.line( 7.7 * inch , y2 , 7.7  * inch , y );
    c.drawString(0.2*inch, y-0.2*inch,  "KETENTUAN :"); y -= y1
    c.drawString(0.2*inch, y-0.2*inch,  "Syarat Pengambilan Barang Jaminan harus menunjukan bukti ini, Kwitansi & KTP Debitur / Ahli Waris"); y -= y1
    
    c.showPage()
    c.save()
    
    return response


@login_required
def cari(request):
    rekening=request.GET['rekening']
    barcode = rekening[11:]
    try:
        ag=AkadGadai.objects.get(id=int(barcode))
        return HttpResponseRedirect("/akadgadai/%s/show/" % ag.id)
    except:
        messages.add_message(request, messages.INFO,'No rekening tidak ditemukan.')
        return HttpResponseRedirect("/akadgadai/")

def pengundurandiri(request, object_id):
    sekarang=datetime.datetime.now()
    akad = AkadGadai.objects.get(id=object_id)
    tb=terbilang(akad.nilai)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= "Formulir Pendaftaran %s.pdf"' % akad.norek()
    h=sekarang.day
    m=sekarang.month
    y=sekarang.year

    buffer = BytesIO()

    p = canvas.Canvas(buffer)
    p.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/kopri.png'), 0.4*inch, (5.2 + 5.7) * inch, width=33.5/17.5*0.51*inch,height=26/17.5*0.51*inch)
    p.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ra2.png'), 7.0*inch, (5.2 + 5.7) * inch, width=35.5/17.5*0.51*inch,height=24/17.5*0.51*inch)
    
    

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(300, 800, "FORMULIR PENGUNDURAN DIRI")
    p.drawCentredString(300, 780, "ANGGOTA KOPERASI RIZKY ABADI")
    p.line(  30 , 775, 580 ,775  ) 
    p.setLineWidth(.3)
    p.line(  30 , 773, 580 ,773  ) 
    p.setFont('Helvetica', 10)
    #p.drawAlignedString(30,763,'Yang bertanda tangan dibawah ini :')
    p.drawString(30,750,'Yang bertanda tangan dibawah ini :')
    p.drawString(30,735,"Nama Lengkap")
    p.drawString(145,735,": %s" % akad.agnasabah.nama)
    p.drawString(30,720,"Tempat & Tanggal Lahir")
    p.drawString(145,720,": %s, %s " % (akad.agnasabah.tempat,akad.agnasabah.tgl_lahir))
    p.drawString(30,705,"Alamat Lengkap")
    p.drawString(145,705,": %s RT %s RW %s Kel %s Kec %s" % (akad.agnasabah.alamat_ktp,akad.agnasabah.rt_ktp,akad.agnasabah.rw_ktp,akad.agnasabah.kelurahan_ktp,akad.agnasabah.kecamatan_ktp))
    p.drawString(30,690,"Nomor KTP / SIM")
    p.drawString(145,690,": %s " % akad.agnasabah.no_ktp)
    p.drawString(30,675,"Pekerjaan")
    p.drawString(145,675,": %s " % akad.agnasabah.get_jenis_pekerjaan_display())
    p.drawString(30,660,"Pendidikan Terakhir")
    p.drawString(145,660,": .................................")
    p.drawString(30,645,"Status Pernikahan")
    p.drawString(145,645,": .................................")
    p.drawString(30,630,"No. Telepon")
    p.drawString(145,630,": %s " % akad.agnasabah.telepon_ktp)
    p.setFont('Helvetica', 10)
    p.drawString(30,610,'Melalui formulir ini saya selaku Anggota mengajukan pengunduran diri dari Koperasi "Rizky Abadi" dengan alasan .........')
    p.drawString(30,600,'....................................................................................................................................')
    p.drawString(395,600,'............................................................')
    p.drawString(30,590,'....................................................................................................................................')
    p.drawString(395,590,'............................................................')
    p.drawAlignedString(353,580,'formulir ini saya buat sesuai peraturan yang berrlaku di KSU Rizky Abadi. Saya berharap KSU Rizky Abadi dapat mema-')
    p.drawString(30,570,'hami kondisi saya dan memberikan hak - hak saya sesuai ketentuan yang berlaku')
    p.drawAlignedString(565,560,'Demikian surat pengunduran diri ini saya buat dengan sesungguhnya,  atas bantuan  dan dukungan yang telah diberikan')
    p.drawString(30,550,'selama ini, saya ucapkan terima kasih.')
    p.drawCentredString(300,530,"Bandung, %s" % sekarang.strftime('%d %B %Y'))
    p.drawCentredString(300, 520, "Yang membuat pernyataan,")    
    p.drawCentredString(300,470,"( %s )" % akad.agnasabah.nama)
    p.drawCentredString(300, 280, "Disetujui oleh,")
    p.drawCentredString(300, 230, "..................................................................")
    p.setLineWidth(.3)
    p.line(209, 229,391, 229)
    p.setFont('Helvetica-Bold', 10)
    p.drawCentredString(300, 220, "Ketua / Kepala Kantor / Manager")
    p.drawCentredString(300, 200, "Kantor Pusat :")
    p.drawCentredString(300, 190, "Badan Hukum Nomor : 518/BH.88-DISKOP/THN.2007 Tgl. 27 Desember 2007")
    p.drawCentredString(300, 175, "Jl. Cisaranten Kulon IV No 55 Rt.06/Rw.05 Kel. Cisaranten Kulon")
    p.drawCentredString(300, 165, "Kec. Arcamanik Bandung 40293 Telp./Fax. 022 87882769")

    
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
 

def keanggotaan(request, object_id):
    sekarang=datetime.datetime.now()
    akad = Nasabah.objects.get(id=object_id)
    akad.klik_keanggotaan = '1'
    akad.save()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= "Formulir Pendaftaran %s.pdf"' % akad.id
    h=sekarang.day
    m=sekarang.month
    y=sekarang.year

    buffer = BytesIO()

    p = canvas.Canvas(buffer)
    p.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/kopri2.png'), 0.4*inch, (5.2 + 5.7) * inch, width=33.5/17.5*0.51*inch,height=26/17.5*0.51*inch)
    p.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ra2.png'), 7.0*inch, (5.2 + 5.7) * inch, width=35.5/17.5*0.51*inch,height=24/17.5*0.51*inch)

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(300, 800, "FORMULIR PENDAFTARAN")
    p.drawCentredString(300, 780, "ANGGOTA KOPERASI RIZKY ABADI")
    p.line(  30 , 775, 580 ,775  ) 
    p.setLineWidth(.3)
    p.line(  30 , 773, 580 ,773  ) 
    p.setFont('Helvetica', 10)
    #p.drawAlignedString(30,763,'Yang bertanda tangan dibawah ini :')
    p.drawString(30,750,'Yang bertanda tangan dibawah ini :')
    p.drawString(30,735,"Nama Lengkap")
    p.drawString(145,735,": %s" % akad.nama)
    p.drawString(30,720,"Tempat & Tanggal Lahir")
    p.drawString(145,720,": %s, %s " % (akad.tempat,akad.tgl_lahir))
    p.drawString(30,705,"Alamat Lengkap")
    p.drawString(145,705,": %s RT %s RW %s Kel %s Kec %s" % (akad.alamat_ktp,akad.rt_ktp,akad.rw_ktp,akad.kelurahan_ktp,akad.kecamatan_ktp))
    p.drawString(30,690,"Nomor KTP / SIM")
    p.drawString(145,690,": %s " % akad.no_ktp)
    p.drawString(30,675,"Pekerjaan")
    p.drawString(145,675,": %s " % akad.get_jenis_pekerjaan_display())
    p.drawString(30,660,"Pendidikan Terakhir")
    p.drawString(145,660,": .................................")
    p.drawString(30,645,"Status Pernikahan")
    p.drawString(145,645,": .................................")
    p.drawString(30,630,"No. Telepon")
    p.drawString(145,630,": %s " % akad.telepon_ktp)
    p.setFont('Helvetica-Bold', 10)
    p.drawString(30,610,"*")
    p.setFont('Helvetica', 10)
    p.drawAlignedString(565,610,'Saya dengan ini mengajukan permohonan menjadi Anggota Koperasi "Rizky Abadi",  dan bersedia mentaati Anggaran')
    p.drawAlignedString(565,600,'Dasar, Anggaran Rumah Tangga, Keputusan kebijakan pengurus serta peraturan lain yang berlaku di Koperasi "Rizky')
    p.drawString(40,590,'Abadi" dengan jujur, disiplin, dan penuh tanggung jawab.')
    p.drawString(45,580,'')
    p.setFont('Helvetica-Bold', 10)
    p.drawString(30,570,"*")
    p.setFont('Helvetica', 10)
    p.drawAlignedString(565,570,'Saya bersedia membayar  simpanan koperasi berupa Simpanan Pokok dan Simpanan Wajib di  Koperasi Rizky  Abadi')
    p.drawAlignedString(565,560,'yang pembayarannya  disesuaikan dengan aturan yang  ada dan sebagaimana yang telah tercantum dalam Anggaran')
    p.drawString(37,550,' dalam Anggaran Dasar/Anggaran Rumah dengan jujur, disiplin, dan penuh tanggung jawab.')
    p.setFont('Helvetica-Bold', 10)
    p.drawString(30,530,"*")
    p.setFont('Helvetica', 10)
    p.drawString(37,530,'Bersama Formulir Permohonan ini, saya sertakan :')
    p.drawString(37,520,'1. Satu lembar Fotocopy KTP/SIM (yang masih berlaku)')
    p.drawString(37,510,'2. Satu lembar Foto Ukuran 2x3 (uk. KTP jika ada)')
    p.drawString(37,490,'Demikian permohonan ini saya buat dengan sebenar-benarnya, atas perhatiannya diucapkan terimakasih.')
    p.drawString(37,470,"Bandung,%s" % sekarang.strftime('%d %b %Y'))
    p.drawString(37,400,"( %s )" % akad.nama)
    
    p.drawCentredString(300, 379, "Diisi/Dicatat oleh Petugas Administrasi")
    p.drawString(35, 365, "Unit Usaha :")
    p.drawString(135, 365, "No anggota :")
    p.drawString(235, 365, "Tanggal menjadi anggota :")
    #p.drawString(200, 355, "")
    p.drawString(395, 365, "Paraf / tanda tangan petugas :")
    #p.drawString(480, 355, "")
    p.setFont('Helvetica', 10)
    # garis Paling atas
    p.line(30, 390, 550, 390)
    #garis kedua dari atas
    p.line(30, 375, 550, 375)
    #garis paling bawah
    p.line(30, 300, 550, 300)
    #garis paling kiri
    p.line(30, 390, 30, 300)
    #garis kedua dari kiri
    p.line(130, 375, 130, 300)
    #garis ketiga dari kiri
    p.line(230, 375, 230, 300)
    #garis ketiga dari kiri
    p.line(390, 375, 390, 300)
    #garis paling kanan
    p.line(550, 390, 550, 300)


    p.drawCentredString(300, 280, "Disetujui oleh,")
    p.drawCentredString(300, 230, "..................................................................")
    p.setLineWidth(.3)
    p.line(209, 229,391, 229)
    p.setFont('Helvetica-Bold', 10)
    p.drawCentredString(300, 220, "Ketua / Kepala Kantor / Manager")
    p.drawCentredString(300, 200, "Kantor Pusat :")
    p.drawCentredString(300, 190, "Badan Hukum Nomor : 518/BH.88-DISKOP/THN.2007 Tgl. 27 Desember 2007")
    p.drawCentredString(300, 175, "Jl. Cisaranten Kulaon IV No 55 Rt.06/Rw.05 Kel. Cisaranten Kulon")
    p.drawCentredString(300, 165, "Kec. Arcamanik Bandung 40293 Telp./Fax. 022 87882769")

    
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def label(request,object_id):
    p = AkadGadai.objects.get(id=object_id)
    p.status_label = '1'
    p.save()
    merk_barang = p.barang.merk[:47]
    merk_barang2 = p.barang.merk[47:100]
    nama_awal = p.agnasabah.nama[:30]
    nama_akhir = p.agnasabah.nama[30:62]    
    
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % p.norek()
    c = canvas.Canvas(response, pagesize=(8.8*inch,11.7*inch))
    c.setTitle("Label %s" % p.norek())
    atas = 0
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
    colom1 = (0.5*inch, (3.4 + 4.9) *inch)
            #ke kiri  ke atas ke bawah
    colom2 = (4.8*inch, (3.4 + 4.9) *inch)
    tb=terbilang(p.terima_bersih)
    #c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/logoksu_hitamputih.png'), 1.0*inch, (5.5 + 1.5) * inch, width=200.5/17.5*0.51*inch,height=120/17.5*0.51*inch)
    #c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 0.5*inch, (4.75 + 5.5) * inch, width=30/17.5*0.51*inch,height=25/17.5*0.51*inch,mask=None)
    
    x,y = header1
    y1 = 0.10 * inch

    y -=1*y1
    ####KOLOM 1 hiji Coy
    x,y = colom1
    y1 = 0.120 * inch
    c.drawString(x-0.3*inch, y, ""); y -=y1
    #c.line( x + 1.9 * inch , y-502 * inch, x + 1.9 * inch, y+102 * inch ) ; y -=y1
    ###Kotak LABEL 1 Garis kiri 
    c.line( x - 0.4*inch , y+3.4*  inch, x - 0.4*inch,  y+1.0*  inch )  
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ra2.png'), 0.15*inch, (5.4 + 5.5) * inch, width=24.5/17.5*0.51*inch, height=22/17.5*0.51*inch)
    ###Kotak LABEL 1 Garis Logo
    c.line( x + 0.4*inch , y+3.4*  inch, x + 0.4*inch,  y+2.6*  inch )
    c.line( x - 0.4*inch , y+2.6*  inch, x + 3.4*inch,  y+2.6*  inch )    
    ###Kotak LABEL 1 Garis kanan 
    c.line( x + 3.4*inch ,y+3.4* inch, x + 3.4*inch, y+1.0*  inch  ) 
    ###Kotak LABEL 1 Garis Atas
    c.line( x - 0.4*inch, y+3.4* inch, x + 3.4*inch, y+3.4 * inch )
    ###Kotak LABEL 1 Garis Bawah
    c.line( x - 0.4*inch,  y+1.0* inch, x + 3.4*inch,  y+1.0* inch )
    c.setFont("Courier-Bold", 11)
    #c.drawString(0.5 * inch , y -8.5* y1 , "Norek"); y -= 1.2*y1
    c.drawString(x + 0.5 * inch , y +3.0* inch , "Gerai"); 
    c.drawString(x + 0.5 * inch , y +2.7*inch, "%s" % (p.gerai.nama_cabang)); y
    barcode = code128.Code128("%s" % (p.norek()))
    barcode.drawOn(c, 49*mm, 285*mm)
    c.drawString(x + 1.8*inch , y +2.9*  inch  , "Norek");
    c.drawString(x + 2.5*inch , y +2.9*  inch  , "%s" % (p.id)); y 
    c.drawString(x - 0.3 *inch, y +2.45*  inch , "Nasabah : %s" % (nama_awal)); y
    c.drawString(x + 0.6 *inch, y +2.3*  inch , "%s" % (nama_akhir)); y
    c.line( x - 0.4*inch , y+2.2*  inch, x + 3.4*inch,  y+2.2*  inch )    
    if p.jenis_transaksi == u'1':
        c.drawString(x - 0.3 *inch, y +2.0*  inch , "Barang : %s" % (p.barang.get_jenis_barang_display())); y
        c.setFont("Courier-Bold", 9)
        c.drawString(x - 0.3 *inch, y +1.8*  inch , "%s" % (merk_barang)); y #,p.barang.type)); y
        c.drawString(x - 0.3 *inch, y +1.6*  inch , "%s" % (merk_barang2)); y #,p.barang.type)); y
    else:
        c.drawString(x - 0.3 *inch, y +2.0*  inch , "Barang : %s" % (p.barang.get_jenis_kendaraan_display())); y
        c.drawString(x - 0.3 *inch, y +1.8*  inch , "%s" % (p.barang.get_merk_kendaraan_display())); y #,p.barang.type)); y
        c.drawString(x - 0.3 *inch, y +1.6*  inch , "%s" % (p.barang.type_kendaraan)); y #,p.barang.type)); y
    c.line( x - 0.4*inch , y+1.5*  inch, x + 3.4*inch,  y+1.5*  inch )  
    c.setFont("Courier-Bold", 10)
    c.drawString(x - 0.3 *inch, y +1.3*  inch , "Tgl Kontrak"); y
    c.drawString(x - 0.3 *inch, y +1.1*  inch, "%s" % p.tanggal.strftime('%d %B %Y')); y
    c.line( x + 1.1*inch , y+1.5*  inch, x + 1.1*inch,  y+1.0*  inch )
    c.drawString(x + 1.15*inch  , y +1.3* inch , "Jth Tempo"); y
    c.drawString(x + 1.15*inch  , y +1.1* inch , "%s"  % p.jatuhtempo.strftime('%d %B %Y')); y
    c.line( x + 2.5*inch , y+1.5*  inch, x + 2.5*inch,  y+1.0*  inch )
    c.drawString(x + 2.55*inch , y +1.3*  inch, "Status "); y
    c.drawString(x + 2.55*inch , y +1.1* inch , "%s" % (p.get_status_transaksi_display())); y

    ####Akhir KOLOM 1 hiji Coy

    ####KOLOM 2 Dua Coy
    x,y = colom2
    y1 = 0.120 * inch
    c.drawString(x-0.3*inch, y, ""); y -=y1
    #c.line( x + 1.9 * inch , y-502 * inch, x + 1.9 * inch, y+102 * inch ) ; y -=y1
    ###Kotak LABEL 1 Garis kiri 
    c.line( x - 0.4*inch , y+3.4*  inch, x - 0.4*inch,  y+1.0*  inch )  
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ra2.png'), 4.45*inch, (5.4 + 5.5) * inch, width=24.5/17.5*0.51*inch, height=22/17.5*0.51*inch)
    ###Kotak LABEL 1 Garis Logo
    c.line( x + 0.4*inch , y+3.4*  inch, x + 0.4*inch,  y+2.6*  inch )
    c.line( x - 0.4*inch , y+2.6*  inch, x + 3.4*inch,  y+2.6*  inch )    
    ###Kotak LABEL 1 Garis kanan 
    c.line( x + 3.4*inch ,y+3.4* inch, x + 3.4*inch, y+1.0*  inch  ) 
    ###Kotak LABEL 1 Garis Atas
    c.line( x - 0.4*inch, y+3.4* inch, x + 3.4*inch, y+3.4 * inch )
    ###Kotak LABEL 1 Garis Bawah
    c.line( x - 0.4*inch,  y+1.0* inch, x + 3.4*inch,  y+1.0* inch )
    c.setFont("Courier-Bold", 11)
    #c.drawString(0.5 * inch , y -8.5* y1 , "Norek"); y -= 1.2*y1
    c.drawString(x + 0.5 * inch , y +3.0* inch , "Gerai"); 
    c.drawString(x + 0.5 * inch , y +2.7*inch, "%s" % (p.gerai.nama_cabang)); y
    barcode = code128.Code128("%s" % (p.norek()))
    barcode.drawOn(c, 158*mm, 285*mm)
    c.drawString(x + 1.8*inch , y +2.9*  inch  , "Norek");
    c.drawString(x + 2.5*inch , y +2.9*  inch  , "%s" % (p.id)); y 
    c.drawString(x - 0.3 *inch, y +2.45*  inch , "Nasabah : %s" % (nama_awal)); y
    c.drawString(x + 0.6 *inch, y +2.3*  inch , "%s" % (nama_akhir)); y

    c.line( x - 0.4*inch , y+2.2*  inch, x + 3.4*inch,  y+2.2*  inch )    
    if p.jenis_transaksi == u'1':
        c.drawString(x - 0.3 *inch, y +2.0*  inch , "Barang : %s" % (p.barang.get_jenis_barang_display())); y
        c.setFont("Courier-Bold", 9)
        c.drawString(x - 0.3 *inch, y +1.8*  inch , "%s" % (merk_barang)); y #,p.barang.type)); y
        c.drawString(x - 0.3 *inch, y +1.6*  inch , "%s" % (merk_barang2)); y #,p.barang.type)); y
    else:
        c.drawString(x - 0.3 *inch, y +2.0*  inch , "Barang : %s" % (p.barang.get_jenis_kendaraan_display())); y
        c.drawString(x - 0.3 *inch, y +1.8*  inch , "%s" % (p.barang.get_merk_kendaraan_display())); y #,p.barang.type)); y
        c.drawString(x - 0.3 *inch, y +1.6*  inch , "%s" % (p.barang.type_kendaraan)); y #,p.barang.type)); y
    c.line( x - 0.4*inch , y+1.5*  inch, x + 3.4*inch,  y+1.5*  inch )  
    c.setFont("Courier-Bold", 10)
    c.drawString(x - 0.3 *inch, y +1.3*  inch , "Tgl Kontrak"); y
    c.drawString(x - 0.3 *inch, y +1.1*  inch, "%s" % p.tanggal.strftime('%d %B %Y')); y
    c.line( x + 1.1*inch , y+1.5*  inch, x + 1.1*inch,  y+1.0*  inch )
    c.drawString(x + 1.15*inch  , y +1.3* inch , "Jth Tempo"); y
    c.drawString(x + 1.15*inch  , y +1.1* inch , "%s"  % p.jatuhtempo.strftime('%d %B %Y')); y
    c.line( x + 2.5*inch , y+1.5*  inch, x + 2.5*inch,  y+1.0*  inch )
    c.drawString(x + 2.55*inch , y +1.3*  inch, "Status "); y
    c.drawString(x + 2.55*inch , y +1.1* inch , "%s" % (p.get_status_transaksi_display())); y
    ####AKHiR KOLOM 2 Dua Coy
    c.showPage()
            ####AKHIR KOLOM 4 Opat Coy
    c.save()
    return response
'''
def label(request,object_id):
    akadgadai = AkadGadai.objects.get(id=object_id)
    akadgadai.status_label = 1
    akadgadai.save()
    merk_barang = akadgadai.barang.merk[:31]
    merk_barang2 = akadgadai.barang.merk[31:50]
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= Label_%s.pdf' % akadgadai.norek()
    
    c = canvas.Canvas(response, pagesize=(9.5*inch, 11*inch))
    barcode = code128.Code128("%s" % (akadgadai.norek()))
    barcode.drawOn(c, 36*mm, 230*mm)

    header0=(8.25 *inch, (5.2 + 5.5) * inch)
    header1=(4.60 *inch, (5.35 + 5.5) * inch)
    colom1 = (0.3*inch, (4.35 + 5.5) *inch)
    colom2 = (6.3*inch, (4.35 + 5.5) *inch)
    colom3 = (6.3*inch, (4.3 + 4.5) *inch)
    
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ra2.png'), 0.7*inch, (3.4 + 5.5) * inch, width=24.5/17.5*0.51*inch, height=24/17.5*0.51*inch)

    x,y = colom1
    y1 = 0.100 * inch
    y2 = y + 0.1 * inch

    y -=  3 * y1
    y2 = y + 0.1 * inch
    c.setFont("Courier-Bold", 11)
    c.drawString(0.5 * inch , y -8.5* y1 , "Norek"); y -= 1.2*y1
    c.drawString(0.5 * inch , y -11* y1 , "%s" % (akadgadai.id)); y 
    c.drawString(1.9 * inch , y -7.5* y1 , "Gerai :"); y -= 1.2*y1
    c.drawString(1.9 * inch , y -9.5* y1 , "%s" % (akadgadai.gerai.nama_cabang)); y
    c.drawString(0.5 * inch , y -11.5* y1 , "Nasabah :"); y
    c.drawString(0.5 * inch , y -14* y1 , "%s" % (akadgadai.agnasabah.nama)); y
    c.drawString(0.5 * inch , y -16.5* y1 , "Barang :" ); y
    c.drawString(1.5 * inch , y -16.5* y1 , "%s" % (akadgadai.barang.get_jenis_barang_display())); y
    c.setFont("Courier-Bold", 10)
    c.drawString(0.5 * inch , y -18* y1 , "%s" % (merk_barang)); y #,akadgadai.barang.type)); y
    c.drawString(0.5 * inch , y -19.5* y1 , "%s" % (merk_barang2)); y #,akadgadai.barang.type)); y
    c.setFont("Courier-Bold", 11)
    c.drawString(0.5 * inch , y -21.5* y1 , "Tgl Kontrak"); y
    c.drawString(0.5 * inch , y -24.5* y1 , " %s" % akadgadai.tanggal.strftime('%d %B %Y')); y
    c.drawString(0.5 * inch , y -27* y1 , "Jth Tempo "); y
    c.drawString(0.5 * inch , y -29.5* y1 , " %s"  % akadgadai.jatuhtempo.strftime('%d %B %Y')); y
    c.drawString(0.5 * inch , y -32* y1 , "Status : %s" % (akadgadai.get_status_transaksi_display())); y
    
    #garis paling atas
    c.line( 0.4 * inch , y2 , 3.2 * inch , y2 );
    #garis paling kiri
    c.line( 0.4* inch , y2 , 0.4 * inch , y -35* y1 );
    #garis tengah
    c.line( 1.8* inch ,  y -5* y1 , 1.8 * inch , y -10* y1 );
    #garis paling kanan
    c.line( 3.2 * inch , y2 , 3.2  * inch , y - 35 * y1 );
    #garis kedua dari atas
    c.line( 0.4* inch , y - 5 * y1 , 3.2 * inch , y - 5 * y1 );
    #garis ketiga dari atas
    c.line( 0.4* inch , y - 10 * y1 , 3.2 * inch , y - 10 * y1 );
    #garis keempat dari atas
    c.line( 0.4* inch , y - 15 * y1 , 3.2 * inch , y - 15 * y1 );
    #garis kelima dari atas
    c.line( 0.4* inch , y - 20 * y1 , 3.2 * inch , y - 20 * y1 );
    #garis keenam dari atas
    c.line( 0.4* inch , y - 25 * y1 , 3.2 * inch , y - 25 * y1 );
    #garis ketujuh dari atas
    c.line( 0.4* inch , y - 30 * y1 , 3.2 * inch , y - 30 * y1 );
    #garis paling bawah
    c.line( 0.4* inch , y - 35 * y1 , 3.2 * inch , y - 35 * y1 );
    c.showPage()
    c.save()
    return response
'''
''' INI YAG TERAKHIR Sbl REViSI PA RW
def pk(request, object_id):
    p = AkadGadai.objects.get(id=object_id)
    tiga_play = [p,p,p]
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s.pdf' % p.norek()
    c = canvas.Canvas(response, pagesize=(11.7*inch, 8.8*inch))
    c.setTitle("kwitansi %s" % p.norek())
    atas = 0
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
    colom1 = (0.5*inch, (-1.12 + 5.5) *inch)
            #ke kiri  ke atas ke bawah
    colom2 = (0.3*inch, (-0.9 + 5) *inch)
    colom3 = (5.35*inch, (-0.6 + 4.5) *inch)
    colom4 = (0.5*inch, (-1 + 5.1) *inch)

    tb=terbilang(p.terima_bersih)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/diskop.png'), 0.6*inch, (1.45 + 5.7) * inch, width=55.5/17.5*0.51*inch,height=40/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 9.5*inch, (1.45 + 5.7) * inch, width=55.5/17.5*0.51*inch,height=40/17.5*0.51*inch,mask=None)
    tb=terbilang(p.nilai)
    barcode = code128.Code128("%s" % (p.norek()))
    barcode.drawOn(c, 195*mm, 268*mm)
    x,y = colom1
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Helvetica-Bold", 16)
    #c.drawString(x-2.78*inch, y-5.45*inch, "KSU RIZKY ABADI 111111111111111"); y -=y1
    ###Kotak kiri Luar
    c.line( x - 0.3*inch , y-4 * inch, x - 0.3*inch, y+4.31 * inch )  
    ###Kotak Kanan Luar
    c.line( x + 11*inch ,y-4 * inch, x + 11*inch, y+4.31 * inch  ) 
    ###Kotak Atas Luar
    c.line( x - 0.3*inch, y+4.3 * inch, x + 11*inch, y+4.3 * inch )
    ###Kotak Bawah Luar
    c.line( x - 0.3*inch, y-4 * inch, x + 11*inch, y-4 * inch )

    ###Kotak kiri Dalam
    c.line( x-0.1*inch , y-3.8 * inch, x-0.1*inch, y+4.1 * inch ) 
    ###Kotak Kanan Dalam
    c.line( x+10.8*inch , y-3.8 * inch, x+10.8*inch, y+4.1 * inch ) 
    ###Kotak Atas Dalam
    c.line( x - 0.1*inch, y+4.1 * inch, x + 10.8*inch, y+4.1 * inch )
    ###Kotak Bawah Dalam
    c.line( x - 0.1*inch, y-3.8 * inch, x + 10.8*inch, y-3.8 * inch )

    ###Kotak Isi kiri 
    c.line( x+0.2*inch , y-2.8 * inch, x+0.2*inch, y+2.8 * inch ) 
    ###Kotak Isi Kanan
    c.line( x+10.5*inch , y-2.8 * inch, x+10.5*inch, y+2.8 * inch ) 
    ###Kotak Isi Atas
    c.line( x + 0.2*inch, y+2.8 * inch, x + 10.5*inch, y+2.8 * inch )
    ###Kotak Isi Bawah
    c.line( x + 0.2*inch, y-2.8 * inch, x + 10.5*inch, y-2.8 * inch )
    ###Kotak Isi Tengah Ke bawah
    c.line( x + 5.35*inch, y-2.8 * inch, x + 5.35*inch, y+2.8 * inch )
    c.line( x + 0.2*inch, y+0.1 * inch, x + 10.5*inch, y+0.1 * inch )
    c.line( x + 5.35*inch, y-1 * inch, x + 10.5*inch, y-1 * inch )
    c.line( x + 5.35*inch, y-1.3 * inch, x + 10.5*inch, y-1.3 * inch )
    c.line( x + 7.9*inch, y-2.8 * inch, x + 7.9*inch, y-1.3 * inch )
    
    c.setFont("Helvetica-Bold", 13)
    c.drawString(x+3.2*inch, y+3.8 * inch, "BUKTI PINJAMAN DENGAN JAMINAN BARANG"); y -=2*y1
    c.drawString(x+3.5*inch, y+3.8 * inch, "No. PK : %s/ PJB/ %s/ %s"  % (p.id,p.gerai.init_cabang,p.tanggal.strftime('%b/ %Y'))); y -=y1


    x,y = colom2
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x+0.65*inch , y+2.89 * inch, "Pihak I"); y -=2*y1
    c.setFont("Helvetica", 10)
    c.drawString(x+0.65*inch , y+2.89 * inch, "Nama : %s"%(p.gerai.nama_kg)); y -=2*y1
    c.drawString(x+0.65*inch , y+2.89 * inch, "Jabatan : Kepala Gerai PJB %s"%(p.gerai.nama_cabang)); y -=2*y1

    c.drawString(x+0.65*inch , y+2.89 * inch, "dalam kedudukannya tersebut di atas mewakili secara sah untuk dan atas"); y -=2*y1
    c.drawString(x+0.65*inch , y+2.89 * inch, "nama  Koperasi Rizky Abadi,  berkedudukan   dan   berkantor    pusat   di"); y -=2*y1
    c.drawString(x+0.65*inch , y+2.89 * inch, "Jl. Cisaranten  Kulon  IV  No  55  Bandung, selanjutnya   disebut")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x+4.65*inch , y+2.89 * inch, "Kreditur."); y -=6*y1
    c.setFont("Helvetica", 10)
    c.drawString(x+0.7*inch , y+ 1.7* inch, "Barang Jaminan :"); y -=1*y1
    c.setFont("Helvetica", 9)
    c.drawString(x+0.9*inch , y+ 1.5* inch, "1. %s|%s|"% (p.barang.merk,p.barang.sn )); y -=3*y1
    c.setFont("Helvetica", 10)
    if p.barang.jenis_barang == u'1': ###('1','HP')
        c.drawString(x+0.7*inch , y+ 1.5* inch, "Kelengkapan :"); y -=3*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "1. Charger")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_charger_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "2. Baterai")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_batre_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "3. Keypad")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_keybord_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "4. Cassing")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_cassing_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "5. Layar")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_layar_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "6. Password")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_password_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "7. Dus")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_dus_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "8. Tas")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_tas_display())); y -=2*y1
    elif p.barang.jenis_barang == u'2':###('2','LAPTOP/NB'),
        c.drawString(x+0.7*inch , y+ 1.5* inch, "Kelengkapan :"); y -=3*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "1. Charger")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_charger_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "2. Baterai")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_batre_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "3. Keypad")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_keybord_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "4. Cassing")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_cassing_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "5. Layar")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_layar_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "6. Password")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.password_barang )); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "7. Dus")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_dus_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "8. Tas")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_tas_display())); y -=2*y1
    elif p.barang.jenis_barang == u'3':###('3','KAMERA'),
        c.drawString(x+0.7*inch , y+ 1.5* inch, "Kelengkapan :"); y -=3*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "1. Lensa")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_lensa_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "2. Baterai")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_batre_kamera_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "3. Cassing")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_cassing_kamera_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "4. Dus")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_dus_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "5. Tas")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_tas_display())); y -=2*y1
    elif p.barang.jenis_barang == u'4':###('4','PS'),
        c.drawString(x+0.7*inch , y+ 1.5* inch, "Kelengkapan :"); y -=3*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "1. Optik")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_optik_ps_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "2. Stick")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_stick_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "3. HDMI")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_hdmi_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "4. Harddisk")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_harddisk_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "5. Dus")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_dus_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "6. Tas")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_tas_display())); y -=2*y1
    elif p.barang.jenis_barang == u'5':###('5','TV LCD'),
        c.drawString(x+0.7*inch , y+ 1.5* inch, "Kelengkapan :"); y -=3*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "1. Layar")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_layar_tv_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "2. Remote")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_remote_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "3. Dus")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_dus_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "4. Tas")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_tas_display())); y -=2*y1
        

    

    x,y = colom3
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x+0.7*inch , y+3.1 * inch, "Pihak II"); y -=2*y1
    c.setFont("Helvetica", 10)
    c.drawString(x+0.7*inch  , y+3.1 * inch, "Nama")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x+1.9*inch  , y+3.1 * inch, ": %s"%(p.agnasabah.nama)); y -=2*y1
    c.setFont("Helvetica", 10)
    c.drawString(x+0.7*inch  , y+3.1 * inch, "No Identitas")
    c.drawString(x+1.9*inch  , y+3.1 * inch, ": %s"%(p.agnasabah.no_ktp)); y -=2*y1
    c.drawString(x+0.7*inch  , y+3.1 * inch, "pekerjaan")
    c.drawString(x+1.9*inch  , y+3.1 * inch, ": %s"%(p.agnasabah.get_jenis_pekerjaan_display())); y -=2*y1
    c.drawString(x+0.7*inch  , y+3.1 * inch, "No Telepon")
    c.drawString(x+1.9*inch  , y+3.1 * inch, ": %s / %s "%(p.agnasabah.telepon_ktp,p.agnasabah.hp_ktp)); y -=2*y1
    c.drawString(x+0.7*inch  , y+3.1 * inch, "Tempat Tinggal")
    c.drawString(x+1.9*inch  , y+3.1 * inch, ": %s No %s RT/RW %s/%s "% (p.agnasabah.alamat_ktp,p.agnasabah.no_rumah_ktp,p.agnasabah.rt_ktp,p.agnasabah.rw_ktp)); y -=2*y1
    c.drawString(x+2*inch  , y+3.1 * inch, "Kel. %s Kec. %s"% (p.agnasabah.kelurahan_ktp,p.agnasabah.kecamatan_ktp)); y -=2*y1
    c.drawString(x+2*inch  , y+3.1 * inch, "Kota Madya %s Kab %s "% (p.agnasabah.kotamadya_ktp,p.agnasabah.kabupaten_ktp)); y -=2*y1
    c.drawString(x+0.7*inch  , y+3.1 * inch, "Almt S. Menyurat")
    c.drawString(x+1.9*inch  , y+3.1 * inch, ": %s No %s RT/RW %s/%s "% (p.agnasabah.alamat_domisili,p.agnasabah.no_rumah_domisili,p.agnasabah.rt_domisili,p.agnasabah.rw_domisili)); y -=2*y1
    c.drawString(x+2*inch  , y+3.1 * inch, "Kel. %s Kec. %s"% (p.agnasabah.kelurahan_domisili,p.agnasabah.kecamatan_domisili)); y -=2*y1
    c.drawString(x+2*inch  , y+3.1 * inch, "Kota Madya %s Kab %s "% (p.agnasabah.kotamadya_domisili,p.agnasabah.kabupaten_domisili)); y -=2*y1
    c.drawString(x+0.7*inch  , y+3.1 * inch, "Dalam hal ini bertindak untuk dan atas nama sendiri,"); y -=2*y1
    c.drawString(x+0.7*inch  , y+3.1 * inch, "selanjutnya disebut")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x+1.95*inch  , y+3.1 * inch, "Debitur"); y -=3*y1
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x+0.7*inch  , y+3.1 * inch, "Nilai Pinjaman  : Rp.     %s"% (number_format(p.nilai))); y -=2*y1
    c.drawString(x+0.7*inch  , y+3.1 * inch,  " ## %s Rupiah ##"  % tb.title()); y -=2*y1
    c.setFont("Helvetica", 10)
    if p.jenis_transaksi == u'1': ###Elektronik
        c.drawString(x+0.7*inch  , y+3.1 * inch, "Jangka Waktu  : %s [ Hari ]"% (p.jangka_waktu)); y -=2*y1
    else:
        c.drawString(x+0.7*inch  , y+3.1 * inch, "Jangka Waktu  : %s [ Bulan ]"% (p.jangka_waktu_kendaraan)); y -=2*y1
    c.drawString(x+0.7*inch  , y+3.1 * inch, "Jatuh Tempo   : %s "% (p.jatuhtempo.strftime('%d %b %Y'))); y -=5*y1

    if p.gerai.kode_cabang == u'318' or p.gerai.kode_cabang == u'317': ###Elektronik
        c.drawString(x+2*inch  , y+3.1 * inch, "Cirebon, %s" % sekarang.strftime('%d %b %Y') ); y -=3*y1
    else:
        c.drawString(x+2*inch  , y+3.1 * inch, "Bandung, %s" % sekarang.strftime('%d %b %Y') ); y -=3*y1
    c.drawString(x+0.7*inch  , y+3.1 * inch, "Kreditur,")   
    c.drawString(x+3.2*inch  , y+3.1 * inch, "Debitur,"); y -=12*y1
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x+0.7*inch ,y+3.1 * inch, "( %s )"%(p.gerai.nama_kg))
    c.drawString(x+3.2*inch  , y+3.1 * inch, "( %s )"%(p.agnasabah.nama))

    
    
    x,y = colom4
    y1 = 0.10 * inch

    y -=1*y1
    c.drawString(x+0.6*inch, y-2.8 * inch, "Keterangan :")
    c.setFont("Courier-Bold", 8)
    #c.drawString(x+7.6*inch, y-2.9 * inch, "Lembar Asli               : Debitur"); y -=y1
    #c.drawString(x+7.6*inch, y-2.9 * inch, "Lembar Copy (Bermaterai)  : Kreditur")
    c.setFont("Courier", 8)
    c.drawString(x+0.7*inch, y-2.9 * inch, "1. Pada saat pelunasan pinjaman Bukti ini harus dibawa"); y -=y1
    c.drawString(x+0.7*inch, y-2.9 * inch, "2. Apabila Bukti hilang agar segera melaporkan kepada pihak Koperasi"); y -=y1
    c.drawString(x+0.7*inch, y-2.9 * inch, "3. Ketentuan perjanjian tercantum di balik Bukti ini"); y -=y1

   


    c.showPage()

    header1=(4.25 *inch, (5.3 + 5.5) * inch)
    colom1 = (0.5*inch, (3.4 + 4.9) *inch)
            #ke kiri  ke atas ke bawah
    colom2 = (3.4*inch, (3.4 + 4.9) *inch)
    colom3 = (6.3*inch, (3.4 + 4.9) *inch)
    colom4 = (9.2*inch, (3.4 + 4.9) *inch)
    tb=terbilang(p.terima_bersih)
    #c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/logoksu_hitamputih.png'), 1.0*inch, (5.5 + 1.5) * inch, width=200.5/17.5*0.51*inch,height=120/17.5*0.51*inch)
    #c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 0.5*inch, (4.75 + 5.5) * inch, width=30/17.5*0.51*inch,height=25/17.5*0.51*inch,mask=None)
    
    x,y = header1
    y1 = 0.10 * inch

    y -=1*y1
    ####KOLOM 1 hiji Coy
    x,y = colom1
    y1 = 0.120 * inch
    c.drawString(x-0.3*inch, y, ""); y -=y1
    #c.line( x + 1.9 * inch , y-502 * inch, x + 1.9 * inch, y+102 * inch ) ; y -=y1
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.5*inch, y, "PERJANJIAN"); y -=y1
    c.drawString(x-0.3*inch, y, "PINJAMAN DENGAN JAMINAN BARANG"); y -=2*y1
    c.drawString(x+0.65*inch, y, "PASAL 1"); y -=y1
    c.drawString(x+0.65*inch, y, "DEFINISI"); y -=y1
    c.setFont("Helvetica",8)
    c.drawString(x-0.4*inch, y,"(1)")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  Unit  Usaha   Pinjaman  Jaminan  Barang"); y -=y1
    c.drawString(x-0.3*inch, y,"  (PJB)  adalah")
    c.setFont("Helvetica",8)
    c.drawString(x+0.55*inch, y,"merupakan unit usaha yang"); y -=y1
    
    c.drawString(x-0.3*inch, y,"  dimiliki  dan  dikelola  oleh  Koperasi   Rizky"); y -=y1
    c.drawString(x-0.3*inch, y,"  Abadi."); y -=2*y1
    c.setFont("Helvetica",8)
    c.drawString(x-0.4*inch, y,"(2)")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  PIHAK I            Kreditur")
    c.setFont("Helvetica",8)
    c.drawString(x+0.25*inch, y,"atau                  adalah    Koperasi"); y -=y1
    c.drawString(x-0.3*inch, y,"  Rizky     Abadi,    sebuah     badan     usaha    "); y -=y1
    c.drawString(x-0.3*inch, y,"  berbadan       hukum       koperasi        yang"); y -=y1
    c.drawString(x-0.3*inch, y,"  salah satu bidang usahanya adalah membe"); y -=y1
    c.drawString(x-0.3*inch, y,"  rikan  pinjaman   dengan   jaminan   barang"); y -=y1
    c.drawString(x-0.3*inch, y,"  kepada anggota/calon anggotanya."); y -=2*y1
    c.setFont("Helvetica",8)
    c.drawString(x-0.4*inch, y, "(3)")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  PIHAK II         Debitur")
    c.setFont("Helvetica",8)
    c.drawString(x+0.23*inch, y,"atau              adalah subjek hukum"); y -=y1
    c.drawString(x-0.3*inch, y,"  perorangan  maupun  badan   usaha    yang"); y -=y1
    c.drawString(x-0.3*inch, y,"  merupakan    anggota   /   calon      anggota"); y -=y1
    c.drawString(x-0.3*inch, y,"  Koperasi   yang    bermaksud   memperoleh"); y -=y1
    c.drawString(x-0.3*inch, y,"  fasilitas pinjaman dari PJB."); y -=2*y1
    c.setFont("Helvetica",8)
    c.drawString(x-0.4*inch, y,"(4)")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  Lembar ini")
    c.setFont("Helvetica",8)
    c.drawString(x+0.3*inch, y," adalah bukti yang sah atas pinja"); y -=y1
    c.drawString(x-0.3*inch, y,"  man uang yang telah diterima Debitur sekal" ); y -=y1
    c.drawString(x-0.3*inch, y,"  igus merupakan  bukti  penyerahan  barang"); y -=y1
    c.drawString(x-0.3*inch, y,"  jaminan dari  Debitur kepada Kreditur."); y -=2*y1
    c.setFont("Helvetica",8)
    c.drawString(x-0.4*inch, y,"(5)")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  Pinjaman")
    c.setFont("Helvetica",8)
    c.drawString(x+0.35*inch, y,"adalah  fasilitas  yang   disetujui "); y -=y1
    c.drawString(x-0.3*inch, y,"  Kreditur  atas  permohonan  yang   diajukan"); y -=y1
    c.drawString(x-0.3*inch, y,"  Debitur  berdasarkan  nilai  jaminan  barang"); y -=y1
    c.drawString(x-0.3*inch, y,"  yang dijaminkan Debitur."); y -=2*y1
    c.setFont("Helvetica",8)
    c.drawString(x-0.4*inch, y,"(6)")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  Jangka Waktu Pinjaman")
    c.setFont("Helvetica",8)
    c.drawString(x+1.1*inch, y,"adalah   periode "); y -=y1
    c.drawString(x-0.3*inch, y,"  masa pinjaman kepada Kreditur  atas  uang"); y -=y1
    c.drawString(x-0.3*inch, y,"  pinjaman yang diterima Debitur."); y -=2*y1
    c.setFont("Helvetica",8)
    c.drawString(x-0.4*inch, y,"(7)")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  Daluwarsa")
    c.setFont("Helvetica",8)
    c.drawString(x+0.4*inch, y,"adalah status pinjaman berikut"); y -=y1
    c.drawString(x-0.3*inch, y,"  barang jaminan yang  periode pinjamannya "); y -=y1
    c.drawString(x-0.3*inch, y,"  telah melampaui masa jatuh tempo."); y -=2*y1
    c.setFont("Helvetica",8)
    c.drawString(x-0.4*inch, y, "(8)")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  Pemberitahuan")
    c.setFont("Helvetica",8)
    c.drawString(x+0.6*inch, y,"adalah   berita  /  informasi "); y -=y1
    c.drawString(x-0.3*inch, y,"  yang   disampaikan  kepada   Debitur,  baik"); y -=y1
    c.drawString(x-0.3*inch, y,"  melalui  surat  maupun  media   komunikasi "); y -=y1
    c.drawString(x-0.3*inch, y,"  tertulis  lainnya  (SMS, e-mail, BBM)  terkait"); y -=y1            
    c.drawString(x-0.3*inch, y,"  masa pinjaman yang akan/telah jatuh tempo."); y -=2*y1            
    
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.65*inch, y, "PASAL 2"); y -=y1
    c.drawString(x+0.25*inch, y, "MAKSUD DAN TUJUAN"); y -=2*y1
    c.setFont("Helvetica",8)
    c.drawString(x-0.3*inch, y,"Perjanjian ini dibuat oleh Kreditur atas permo"); y -=y1
    c.drawString(x-0.3*inch, y,"honan pinjaman yang diajukan  Debitur  atas"); y -=y1
    c.drawString(x-0.3*inch, y,"sejumlah uang dengan menyerahkan barang"); y -=y1
    c.drawString(x-0.3*inch, y,"jaminan selama jangka waktu tertentu sesuai"); y -=y1
    c.drawString(x-0.3*inch, y,"persetujuan  dan  kesepakatan  kedua  belah "); y -=y1
    c.drawString(x-0.3*inch, y,"pihak."); y -=2*y1
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.65*inch, y,"PASAL 3"); y -=y1
    c.drawString(x+0.25*inch, y,"HAK DAN KEWAJIBAN"); y -=y1
    c.setFont("Helvetica",8) 
    c.drawString(x-0.4*inch, y,"(1)")
    c.drawString(x-0.3*inch, y,"  Kreditur wajib memeriksa permohonan pinja"); y -=y1
    c.drawString(x-0.3*inch, y,"  man yang diajukan Debitur,  dan melakukan"); y -=y1
    c.drawString(x-0.3*inch, y,"  pengecekan kalaikan barang jaminan  yang"); y -=y1  
    c.drawString(x-0.3*inch, y,"  akan dijaminkan oleh Debitur."); y -=y1          
    #c.line( x + 0.3*inch, y+0.1*inch , x + 11.1*inch, y+0.1*inch )
    ####Akhir KOLOM 1 hiji Coy

    ####KOLOM 2 Dua Coy
    x,y = colom2
    y1 = 0.120 * inch
    #c.line( x + 2.45 * inch , y-502 * inch, x + 2.45 * inch, y+102 * inch ) ; y -=y1
    #c.line( x + 1.9 * inch , y-502 * inch, x + 1.9 * inch, y+102 * inch ) ; y -=y1
    c.drawString(x-0.3*inch, y, ""); y -=y1
    c.setFont("Helvetica", 8)
    c.drawString(x-0.4*inch, y,"(2)")
    c.drawString(x-0.3*inch, y,"  Kreditur  wajib  menjaga   keamanan   serta"); y -=y1
    c.drawString(x-0.3*inch, y,"  keutuhan barang  jaminan yang  diserahkan"); y -=y1
    c.drawString(x-0.3*inch, y,"  Debitur  kepadanya  sampai  dengan  masa"); y -=y1
    c.drawString(x-0.3*inch, y,"  perjanjian ini berakhir."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(3)")
    c.drawString(x-0.3*inch, y,"  Debitur wajib  mengembalikan  pinjaman se"); y -=y1
    c.drawString(x-0.3*inch, y,"  suai   dengan    periode     pinjaman    yang"); y -=y1
    c.drawString(x-0.3*inch, y,"  disepakati."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(4)")
    c.drawString(x-0.3*inch, y,"  Debitur    wajib     menyampaikan     barang"); y -=y1
    c.drawString(x-0.3*inch, y,"  jaminan   dalam   kondisi   yang   baik   dan"); y -=y1
    c.drawString(x-0.3*inch, y,"  menyertakan    tanda     bukti    kepemilikan"); y -=y1
    c.drawString(x-0.3*inch, y,"  barang  (kuitansi  pembelian)."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(5)")
    c.drawString(x-0.3*inch, y,"  Kreditur berhak untuk menolak permohonan"); y -=y1
    c.drawString(x-0.3*inch, y,"  pinjaman    yang   diajukan   Debitur   berda"); y -=y1
    c.drawString(x-0.3*inch, y,"  sarkan hak  penilaian yang dimiliki Kreditur."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(6)")
    c.drawString(x-0.3*inch, y,"  Kreditur  berhak  untuk  menguasai  barang"); y -=y1
    c.drawString(x-0.3*inch, y,"  jaminan sampai dengan  pinjaman  yang  di"); y -=y1
    c.drawString(x-0.3*inch, y,"  terima    Debitur     dinyatakan   lunas   oleh"); y -=y1
    c.drawString(x-0.3*inch, y,"  Kreditur."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(7)")
    c.drawString(x-0.3*inch, y,"  Kreditur   berhak   untuk   menjual    barang"); y -=y1
    c.drawString(x-0.3*inch, y,"  jaminan  yang  diserahkan  Debitur  apabila"); y -=y1
    c.drawString(x-0.3*inch, y,"  sampai dengan masa  pinjaman yang  telah"); y -=y1
    c.drawString(x-0.3*inch, y,"  disepakati     Debitur      tidak      melakukan "); y -=y1            
    c.drawString(x-0.3*inch, y,"  pelunasan pinjaman kepada pihak Kreditur."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(8)")
    c.drawString(x-0.3*inch, y,"  Debitur  berhak   untuk  memperoleh   dana"); y -=y1
    c.drawString(x-0.3*inch, y,"  pinjaman  apabila  Debitur  telah  menyerah"); y -=y1
    c.drawString(x-0.3*inch, y,"  kan   barang  jaminan  sesuai  kriteria  yang"); y -=y1
    c.drawString(x-0.3*inch, y,"  ditentukan  oleh  pihak  Kreditur. "); y -=2*y1            
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.55*inch, y,"PASAL 4"); y -=y1
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.1*inch, y,"PELUNASAN PINJAMAN "); y -=y1
    c.drawString(x-0.3*inch, y,"DAN PENGAMBILAN BARANG JAMINAN"); y -=2*y1
    c.setFont("Helvetica", 8) 
    c.drawString(x-0.4*inch, y,"(1)")
    c.drawString(x-0.3*inch, y,"  Untuk    melakukan    pelunasan    pinjaman"); y -=y1
    c.drawString(x-0.3*inch, y,"  serta  mengambil  barang  jaminan,  Debitur"); y -=y1
    c.drawString(x-0.3*inch, y,"  harus    melakukannya    sendiri    ke   gerai"); y -=y1
    c.drawString(x-0.3*inch, y,"  tempat dimana  Debitur  melakukan  pemin-"); y -=y1
    c.drawString(x-0.3*inch, y,"  jaman, dengan membawa  Bukti   asli   dan"); y -=y1
    c.drawString(x-0.3*inch, y,"  identitas diri."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(2)")
    c.drawString(x-0.3*inch, y,"  Dalam  hal   Debitur    berhalangan    untuk"); y -=y1
    c.drawString(x-0.3*inch, y,"  melakukan   pelunasan    pinjaman   secara"); y -=y1
    c.drawString(x-0.3*inch, y,"  langsung pada waktu yang telah ditentukan,"); y -=y1
    c.drawString(x-0.3*inch, y,"  Debitur   dapat   diwakili   oleh   kuasa   ahli"); y -=y1
    c.drawString(x-0.3*inch, y,"  warisnya  untuk  melakukan  pelunasan dan"); y -=y1
    c.drawString(x-0.3*inch, y,"  pengambilan barang jaminan  dengan mem"); y -=y1
    c.drawString(x-0.3*inch, y,"  bawa   Bukti   asli,  Surat Kuasa bermaterai,"); y -=y1            
    c.drawString(x-0.3*inch, y,"  KTP  Pemberi  dan  Penerima  Kuasa, serta"); y -=y1            
    c.drawString(x-0.3*inch, y,"  Surat Kematian dan Keterangan Ahli  Waris"); y -=y1
    c.drawString(x-0.3*inch, y,"  dari  kelurahan  apabila  Debitur  meninggal"); y -=y1  
    c.drawString(x-0.3*inch, y,"  dunia."); y -=2*y1  
    c.drawString(x-0.4*inch, y, "(3)")
    c.drawString(x-0.3*inch, y,"  Untuk   kelancaran   pengembalian   barang"); y -=y1
    c.drawString(x-0.3*inch, y,"  jaminan  Debitur  wajib menyampaikan pem"); y -=y1
    c.drawString(x-0.3*inch, y,"  beritahuan ke petugas gerai tempat dimana"); y -=y1
    c.drawString(x-0.3*inch, y,"  Debitur   melakukan    transaksi    pinjaman, "); y -=y1
    c.drawString(x-0.3*inch, y,"  paling    lambat   1   ( satu )   hari    sebelum "); y -=y1
    c.drawString(x-0.3*inch, y,"  pelunasan dilakukan."); y -=y1
    ####AKHiR KOLOM 2 Dua Coy



    ####KOLOM 3 Tilu Coy
    #y -=  2 * y1
    #y2 = y + 0.1 * inch
    #c.setFont("Courier-Bold", 14)
               
            
    x,y = colom3
    y1 = 0.120 * inch
    #c.line( x + 2.45 * inch , y-502 * inch, x + 2.45 * inch, y+102 * inch ) ; y -=y1
    #c.line( x + 1.9 * inch , y-502 * inch, x + 1.9 * inch, y+102 * inch ) ; y -=y1
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.55*inch, y, ""); y -=y1
    c.drawString(x+0.55*inch, y, "PASAL 5"); y -=y1
    c.drawString(x+0.40*inch, y, "JATUH TEMPO"); y -=2*y1
    c.setFont("Helvetica", 8)
    c.drawString(x-0.4*inch, y,"(1)")
    c.drawString(x-0.3*inch, y,"  Pinjaman  dikategorikan  telah  jatuh tempo"); y -=y1
    c.drawString(x-0.3*inch, y,"  apabila  sampai  dengan batas  waktu yang"); y -=y1
    c.drawString(x-0.3*inch, y,"  ditentukan      Debitur     tidak     melakukan"); y -=y1
    c.drawString(x-0.3*inch, y,"  pelunasan   pinjaman   kepada   Kreditur."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(2)")
    c.drawString(x-0.3*inch, y,"  Terhadap  pinjaman yang telah jatuh tempo,"); y -=y1
    c.drawString(x-0.3*inch, y,"  Kreditur    akan    menyampaikan   Pemberi"); y -=y1
    c.drawString(x-0.3*inch, y,"  tahuan   secara   layak,  baik   melalui  surat"); y -=y1
    c.drawString(x-0.3*inch, y,"  maupun media  lainnya ke alamat  /  nomor"); y -=y1
    c.drawString(x-0.3*inch, y,"  kontak  yang   dicantumkan  Debitur  sesuai"); y -=y1
    c.drawString(x-0.3*inch, y,"  Bukti  ini   untuk   segera   melunasi   pokok"); y -=y1
    c.drawString(x-0.3*inch, y,"  pinjaman  beserta  denda / biaya  lain  yang"); y -=y1
    c.drawString(x-0.3*inch, y,"  ditetapkan oleh pihak Kreditur."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(3)")
    c.drawString(x-0.3*inch, y,"  Apabila    Kreditur    telah     menyampaikan"); y -=y1
    c.drawString(x-0.3*inch, y,"  Pemberitahuan     secara     layak     namun"); y -=y1
    c.drawString(x-0.3*inch, y,"  Debitur  tetap   tidak  melakukan pelunasan"); y -=y1
    c.drawString(x-0.3*inch, y,"  pinjaman sesuai  batas waktu  yang ditentu"); y -=y1
    c.drawString(x-0.3*inch, y,"  kan dalam pemperitahuan tersebut, maka 7"); y -=y1
    c.drawString(x-0.3*inch, y,"  (Tujuh) hari terhitung sejak tanggal pemberi"); y -=y1
    c.drawString(x-0.3*inch, y,"  tahuan    disampaikan,   Debitur    dianggap"); y -=y1
    c.drawString(x-0.3*inch, y,"  setuju  untuk  melepaskan hak  kepemilikan"); y -=y1
    c.drawString(x-0.3*inch, y,"  atas barang jaminan   dan Barang   jaminan"); y -=y1
    c.drawString(x-0.3*inch, y,"  tersebut dianggap Daluwarsa."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(4)")
    c.drawString(x-0.3*inch, y,"  Untuk kepentingan pelunasan pinjaman Deb"); y -=y1
    c.drawString(x-0.3*inch, y,"  itur serta mengacu  pada   ketentuan  dalam "); y -=y1
    c.drawString(x-0.3*inch, y,"  Pasal 3  ayat  (7)  tersebut  di  atas, Kreditur  "); y -=y1
    c.drawString(x-0.3*inch, y,"  berhak  menjual  barang  jaminan kepada  pi"); y -=y1
    c.drawString(x-0.3*inch, y,"  hak ketiga,  guna  keperluan  pelunasan  pin"); y -=y1
    c.drawString(x-0.3*inch, y,"  jaman  Debitur terhadap Kreditur,   sehingga"); y -=y1
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  Debitur tidak dapat mengajukan keberatan"); y -=y1
    c.drawString(x-0.3*inch, y,"  /upaya apapun atas  pengalihan  hak kepe"); y -=y1
    c.drawString(x-0.3*inch, y,"  milikan atas barang jaminan tersebut."); y -=2*y1
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.60*inch, y,"PASAL 6"); y -=y1
    c.drawString(x+0.20*inch, y,"BIAYA KETERLAMBATAN"); y -=2*y1
    c.setFont("Helvetica", 8)
    c.drawString(x-0.3*inch, y,"  Apabila terjadi   keterlambatan   pada   saat"); y -=y1
    c.drawString(x-0.3*inch, y,"  dilakukan   pelunasan  oleh   debitur,  maka"); y -=y1
    c.drawString(x-0.3*inch, y,"  debitur  harus  membayar   biaya   keterlam"); y -=y1
    c.drawString(x-0.3*inch, y,"  batan yang ditetapkan oleh Kreditur."); y -=2*y1
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.60*inch, y,"PASAL 7"); y -=y1
    c.drawString(x+0.5*inch, y,"GANTI RUGI"); y -=2*y1
    c.setFont("Helvetica", 8)
    c.drawString(x-0.4*inch, y,"(1)")
    c.drawString(x-0.3*inch, y,"  KOPERASI RIZKY ABADI   akan     membe"); y -=y1
    c.drawString(x-0.3*inch, y,"  rikan ganti kerugian apabila barang jaminan"); y -=y1
    c.drawString(x-0.3*inch, y,"  yang   berada   dalam   penguasaan  KOPE"); y -=y1
    c.drawString(x-0.3*inch, y,"  RASI    RIZKY    ABADI     sampai   dengan"); y -=y1
    c.drawString(x-0.3*inch, y,"  berakhirnya         perjanjian         mengalami"); y -=y1
    c.drawString(x-0.3*inch, y,"  kerusakan  (bukan   merupakan  kerusakan   "); y -=y1
    c.drawString(x-0.3*inch, y,"  software) atau hilang yang tidak disebabkan"); y -=y1
    c.drawString(x-0.3*inch, y,"  oleh   suatu  bencana  alam  (forcemajeure) "); y -=y1
    c.drawString(x-0.3*inch, y,"  yang ditetapkan pemerintah."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(2)")
    c.drawString(x-0.3*inch, y,"  Ganti  rugi  diberikan  sebesar  nilai  barang "); y -=y1
    c.drawString(x-0.3*inch, y, "  padasaat barang jaminan  diterima Kreditur"); y -=y1
    c.drawString(x-0.3*inch, y, "  dengan  mempertimbangkan  nilai pinjaman"); y -=y1
    c.drawString(x-0.3*inch, y, "  debitur sebelum pelunasan dilakukan."); y -=2*y1

    ####AKHiR KOLOM 3 Tilu Coy

    ####KOLOM 4 Opat Coy
    x,y = colom4
    y1 = 0.120 * inch
    #c.line( x + 2.45 * inch , y-502 * inch, x + 2.45 * inch, y+102 * inch ) ; y -=y1
    #c.line( x + 1.9 * inch , y-502 * inch, x + 1.9 * inch, y+102 * inch ) ; y -=y1
    c.drawString(x-0.3*inch, y, ""); y -=y1
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.55*inch, y, "PASAL 8"); y -=y1
    c.drawString(x+0*inch, y, "PERNYATAAN DAN JAMINAN"); y -=2*y1
    c.setFont("Helvetica", 8)
    c.drawString(x-0.4*inch, y, "(1)")
    c.drawString(x-0.3*inch, y,"  Debitur  dengan    ini    menyatakan  bahwa"); y -=y1
    c.drawString(x-0.3*inch, y,"  barang  jaminan yang  diserahkan   kepada"); y -=y1
    c.drawString(x-0.3*inch, y,"  Kreditur adalah benar barang milik  Debitur,"); y -=y1
    c.drawString(x-0.3*inch, y,"  dan  tidak  diperoleh  dari  hasil   kejahatan/"); y -=y1
    c.drawString(x-0.3*inch, y,"  tindak   pidana.   Oleh   karenanya   Debitur"); y -=y1
    c.drawString(x-0.3*inch, y,"  melepaskan pihak Kreditur segala tanggung"); y -=y1
    c.drawString(x-0.3*inch, y,"  jawab dari  segala tuntutan pihak ketiga."); y -=2*y1
    c.drawString(x-0.4*inch, y, "(2)")
    c.drawString(x-0.3*inch, y,"  Debitur menyatakan bahwa barang jaminan"); y -=y1
    c.drawString(x-0.3*inch, y,"  asli,   yang    diserahkan    kepada  Kreditur"); y -=y1
    c.drawString(x-0.3*inch, y,"  adalah bukan replika, tiruan, palsu.  Apabila"); y -=y1
    c.drawString(x-0.3*inch, y,"  dikemudian  hari   ditemukan   fakta  bahwa"); y -=y1
    c.drawString(x-0.3*inch, y,"  barang jaminan tersebut replika, tiruan dan/"); y -=y1
    c.drawString(x-0.3*inch, y,"  atau    palsu    maka   Debitur   menyatakan"); y -=y1
    c.drawString(x-0.3*inch, y,"  sanggup  untuk mengganti barang  jaminan"); y -=y1
    c.drawString(x-0.3*inch, y,"  dan / atau membayar   ganti  kerugian yang"); y -=y1
    c.drawString(x-0.3*inch, y,"  diderita Kreditur  akibat penyerahan barang"); y -=y1
    c.drawString(x-0.3*inch, y,"  jaminan yang tidak sesuai."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(3)")
    c.drawString(x-0.3*inch, y,"  Debitur  menyatakan tunduk  dan mengikuti"); y -=y1
    c.drawString(x-0.3*inch, y,"  segala    peraturan  yang    tertuang  dalam"); y -=y1
    c.drawString(x-0.3*inch, y,"  perjanjian ini."); y -=2*y1
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.60*inch, y, "PASAL 9"); y -=y1
    c.drawString(x+0.55*inch, y, "PENUTUP"); y -=2*y1
    c.setFont("Helvetica", 8)
    c.drawString(x-0.3*inch, y, "Apabila terjadi  perselisihan dikemudian hari,"); y -=y1
    c.drawString(x-0.3*inch, y, "maka akan diselesaikan secara musyawarah"); y -=y1
    c.drawString(x-0.3*inch, y, "untuk   mufakat dan   apabila  tidak   tercapai "); y -=y1
    c.drawString(x-0.3*inch, y, "kesepakatan    akan     diselesaikan    sesuai"); y -=y1
    c.drawString(x-0.3*inch, y, "hukum yang berlaku. Demikian perjanjian  ini"); y -=y1
    c.drawString(x-0.3*inch, y, "dibuat    dengan    sebenar  -  benarnya   dan "); y -=y1
    c.drawString(x-0.3*inch, y, "mengikat      kedua      belah    pihak,   serta "); y -=y1
    c.drawString(x-0.3*inch, y, "ditandatangani  oleh  masing - masing  pihak"); y -=y1
    c.drawString(x-0.3*inch, y, "dan mempunyai kekuatan hukum yang sama."); y -=2*y1
    if p.gerai.kode_cabang == u'318' or p.gerai.kode_cabang == u'317': ###Elektronik
        c.drawString(x+0.3*inch, y, "Cirebon, %s" % sekarang.strftime('%d %b %Y') ); y -=2*y1
    else:
        c.drawString(x+0.3*inch, y, "Bandung, %s" % sekarang.strftime('%d %b %Y') ); y -=2*y1
    #c.drawString(x-0.3*inch, y, ""); y -=2*y1
    c.drawString(x+0.65*inch, y, "Debitur,"); y -=5*y1
    c.drawString(x+0.46*inch, y, "Materai Rp.6.000"); y -=8*y1
    c.drawString(x+0.18*inch, y, "(..............................................)"); y -=3*y1
    c.drawString(x+0.65*inch, y, "Kreditur,"); y -=7*y1
    c.drawString(x+0.18*inch, y, "(..............................................)"); y -=2*y1
    c.drawString(x+0.6*inch, y, "Kepala Gerai")

    c.showPage()
            ####AKHIR KOLOM 4 Opat Coy
    c.save()
    return response
'''
def pk(request, object_id):
    p = AkadGadai.objects.get(id=object_id)
    tiga_play = [p,p,p]
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % p.norek()
    c = canvas.Canvas(response, pagesize=(11.7*inch, 8.8*inch))
    c.setTitle("kwitansi %s" % p.norek())
    atas = 0
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
    colom1 = (0.5*inch, (-1.12 + 5.5) *inch)
            #ke kiri  ke atas ke bawah
    colom2 = (0.3*inch, (-0.9 + 5) *inch)
    colom3 = (5.35*inch, (-0.6 + 4.5) *inch)
    colom4 = (0.5*inch, (-1 + 5.1) *inch)

    tb=terbilang(p.terima_bersih)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/diskop.png'), 0.6*inch, (1.45 + 5.7) * inch, width=55.5/17.5*0.51*inch,height=40/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 9.5*inch, (1.45 + 5.7) * inch, width=55.5/17.5*0.51*inch,height=40/17.5*0.51*inch,mask=None)
    tb=terbilang(p.nilai)
    barcode = code128.Code128("%s" % (p.norek()))
    barcode.drawOn(c, 195*mm, 268*mm)
    x,y = colom1
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Helvetica-Bold", 16)
    #c.drawString(x-2.78*inch, y-5.45*inch, "KSU RIZKY ABADI 111111111111111"); y -=y1
    ###Kotak kiri Luar
    c.line( x - 0.3*inch , y-4 * inch, x - 0.3*inch, y+4.31 * inch )  
    ###Kotak Kanan Luar
    c.line( x + 11*inch ,y-4 * inch, x + 11*inch, y+4.31 * inch  ) 
    ###Kotak Atas Luar
    c.line( x - 0.3*inch, y+4.3 * inch, x + 11*inch, y+4.3 * inch )
    ###Kotak Bawah Luar
    c.line( x - 0.3*inch, y-4 * inch, x + 11*inch, y-4 * inch )

    ###Kotak kiri Dalam
    c.line( x-0.1*inch , y-3.8 * inch, x-0.1*inch, y+4.1 * inch ) 
    ###Kotak Kanan Dalam
    c.line( x+10.8*inch , y-3.8 * inch, x+10.8*inch, y+4.1 * inch ) 
    ###Kotak Atas Dalam
    c.line( x - 0.1*inch, y+4.1 * inch, x + 10.8*inch, y+4.1 * inch )
    ###Kotak Bawah Dalam
    c.line( x - 0.1*inch, y-3.8 * inch, x + 10.8*inch, y-3.8 * inch )

    ###Kotak Isi kiri 
    c.line( x+0.2*inch , y-2.8 * inch, x+0.2*inch, y+2.8 * inch ) 
    ###Kotak Isi Kanan
    c.line( x+10.5*inch , y-2.8 * inch, x+10.5*inch, y+2.8 * inch ) 
    ###Kotak Isi Atas
    c.line( x + 0.2*inch, y+2.8 * inch, x + 10.5*inch, y+2.8 * inch )
    ###Kotak Isi Bawah
    c.line( x + 0.2*inch, y-2.8 * inch, x + 10.5*inch, y-2.8 * inch )
    ###Kotak Isi Tengah Ke bawah
        ###GARIS TENGAH KE ATAS
    c.line( x + 5.35*inch, y-2.8 * inch, x + 5.35*inch, y+2.8 * inch )
        ###GARIS TENGAH KE PINGGIR
    c.line( x + 0.2*inch, y+0.1 * inch, x + 10.5*inch, y+0.1 * inch )
        ###GARIS DI ATAS TANGGAL
    c.line( x + 5.35*inch, y-1 * inch, x + 10.5*inch, y-1 * inch )
        ###GARIS DI ATAS TTD KREDITUR DAN  DEBITUR
    c.line( x + 5.35*inch, y-1.3 * inch, x + 10.5*inch, y-1.3 * inch )
        ###GARIS DI PINGGIR TTD DEBITUR
    c.line( x + 7.9*inch, y-2.8 * inch, x + 7.9*inch, y-1.3 * inch )
    
    c.setFont("Helvetica-Bold", 13)
    c.drawString(x+3.2*inch, y+3.8 * inch, "BUKTI PINJAMAN DENGAN JAMINAN BARANG"); y -=2*y1
    c.drawString(x+3.5*inch, y+3.8 * inch, "No. PK : %s/ PJB/ %s/ %s"  % (p.id,p.gerai.init_cabang,p.tanggal.strftime('%b/ %Y'))); y -=y1


    x,y = colom2
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x+0.65*inch , y+2.89 * inch, "Pihak I"); y -=2*y1
    c.setFont("Helvetica", 10)
    c.drawString(x+0.65*inch , y+2.89 * inch, "Nama : %s"%(p.gerai.nama_kg)); y -=2*y1
    c.drawString(x+0.65*inch , y+2.89 * inch, "Jabatan : Kepala Gerai PJB %s"%(p.gerai.nama_cabang)); y -=2*y1

    c.drawString(x+0.65*inch , y+2.89 * inch, "dalam kedudukannya tersebut di atas mewakili secara sah untuk dan atas"); y -=2*y1
    c.drawString(x+0.65*inch , y+2.89 * inch, "nama  Koperasi Rizky Abadi,  berkedudukan   dan   berkantor    pusat   di"); y -=2*y1
    c.drawString(x+0.65*inch , y+2.89 * inch, "Jl. Cisaranten  Kulon  IV  No  55  Bandung, selanjutnya   disebut")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x+4.65*inch , y+2.89 * inch, "Kreditur."); y -=6*y1
    c.setFont("Helvetica", 10)
    c.drawString(x+0.7*inch , y+ 1.7* inch, "Barang Jaminan :"); y -=1*y1
    c.setFont("Helvetica", 9)
    if p.jenis_transaksi == u'1': ###('1','Elektronik')
        c.drawString(x+0.9*inch , y+ 1.5* inch, "1. %s|%s|"% (p.barang.merk,p.barang.sn )); y -=3*y1
    elif p.jenis_transaksi != u'1': ###('1','MObil')
        c.drawString(x+0.9*inch , y+ 1.5* inch, "1. %s | %s | %s |"% (p.barang.get_merk_kendaraan_display(),p.barang.type,p.barang.no_polisi )); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "    %s|%s|"% (p.barang.no_rangka,p.barang.no_mesin )); y -=3*y1
    c.setFont("Helvetica", 10)
    if p.barang.jenis_barang == u'1': ###('1','HP')
        c.drawString(x+0.7*inch , y+ 1.5* inch, "Kelengkapan :"); y -=3*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "1. Charger")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_charger_display())); y #CARGER
        c.drawString(x+2.9*inch , y+ 1.5* inch, "2. Baterai")
        c.drawString(x+3.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_batre_display())); y -=2*y1 #BATRE
        c.drawString(x+0.9*inch , y+ 1.5* inch, "3. Keypad")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_keybord_display())); y #KEYPAD
        c.drawString(x+2.9*inch , y+ 1.5* inch, "4. Cassing")
        c.drawString(x+3.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_cassing_display())); y -=2*y1 #CASSING
        c.drawString(x+0.9*inch , y+ 1.5* inch, "5. Layar")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_layar_display())); y  #LAYAR
        c.drawString(x+2.9*inch , y+ 1.5* inch, "6. Password")
        c.drawString(x+3.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_password_display())); y -=2*y1 #PASSWORD
        c.drawString(x+0.9*inch , y+ 1.5* inch, "7. Dus")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_dus_display())); y #DUS
        c.drawString(x+2.9*inch , y+ 1.5* inch, "8. Tas")
        c.drawString(x+3.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_tas_display())); y -=4*y1 # TAS
        c.setFont("Helvetica", 10)
        c.drawString(x+0.7*inch  , y+1.5 * inch, "* Gadai Ulang pinjaman hanya dapat dilakukan sebanyak 1 (satu) kali."); y -=2*y1
    elif p.barang.jenis_barang == u'2':###('2','LAPTOP/NB'),
        c.drawString(x+0.7*inch , y+ 1.5* inch, "Kelengkapan :"); y -=3*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "1. Charger")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_charger_display())); y #CHARGER
        c.drawString(x+2.9*inch , y+ 1.5* inch, "2. Baterai")
        c.drawString(x+3.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_batre_display())); y -=2*y1 #BATRE
        c.drawString(x+0.9*inch , y+ 1.5* inch, "3. Keypad")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_keybord_display())); y  #KEYPAD
        c.drawString(x+2.9*inch , y+ 1.5* inch, "4. Cassing")
        c.drawString(x+3.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_cassing_display())); y -=2*y1#CASSING
        c.drawString(x+0.9*inch , y+ 1.5* inch, "5. Layar")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_layar_display())); y #LAYAR
        c.drawString(x+2.9*inch , y+ 1.5* inch, "6. Password")
        c.drawString(x+3.9*inch , y+ 1.5* inch, "%s "% (p.barang.password_barang )); y -=2*y1 #PASSWORD
        c.drawString(x+0.9*inch , y+ 1.5* inch, "7. Dus")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_dus_display())); y #DUS
        c.drawString(x+2.9*inch , y+ 1.5* inch, "8. Tas")
        c.drawString(x+3.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_tas_display())); y -=4*y1#TAS
        c.setFont("Helvetica", 10)
        c.drawString(x+0.7*inch  , y+1.5 * inch, "* Gadai Ulang pinjaman hanya dapat dilakukan sebanyak 1 (satu) kali."); y -=2*y1
    elif p.barang.jenis_barang == u'3':###('3','KAMERA'),
        c.drawString(x+0.7*inch , y+ 1.5* inch, "Kelengkapan :"); y -=3*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "1. Lensa")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_lensa_display())); y
        c.drawString(x+2.9*inch , y+ 1.5* inch, "2. Baterai")
        c.drawString(x+3.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_batre_kamera_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "3. Cassing")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_cassing_kamera_display()));
        c.drawString(x+2.9*inch , y+ 1.5* inch, "4. Dus")
        c.drawString(x+3.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_dus_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "5. Tas")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_tas_display())); y -=4*y1
        c.setFont("Helvetica", 10)
        c.drawString(x+0.7*inch  , y+1.5 * inch, "* Gadai Ulang pinjaman hanya dapat dilakukan sebanyak 1 (satu) kali."); y -=2*y1
    elif p.barang.jenis_barang == u'4':###('4','PS'),
        c.drawString(x+0.7*inch , y+ 1.5* inch, "Kelengkapan :"); y -=3*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "1. Optik")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_optik_ps_display())); y
        c.drawString(x+2.9*inch , y+ 1.5* inch, "2. Stick")
        c.drawString(x+3.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_stick_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "3. HDMI")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_hdmi_display())); y 
        c.drawString(x+2.9*inch , y+ 1.5* inch, "4. Harddisk")
        c.drawString(x+3.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_harddisk_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "5. Dus")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_dus_display())); y
        c.drawString(x+2.9*inch , y+ 1.5* inch, "6. Tas")
        c.drawString(x+3.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_tas_display())); y -=4*y1
        c.setFont("Helvetica", 10)
        c.drawString(x+0.7*inch  , y+1.5 * inch, "* Gadai Ulang pinjaman hanya dapat dilakukan sebanyak 1 (satu) kali."); y -=2*y1
    elif p.barang.jenis_barang == u'5':###('5','TV LCD'),
        c.drawString(x+0.7*inch , y+ 1.5* inch, "Kelengkapan :"); y -=3*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "1. Layar")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_layar_tv_display())); y
        c.drawString(x+2.9*inch , y+ 1.5* inch, "2. Remote")
        c.drawString(x+3.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_remote_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "3. Dus")
        c.drawString(x+1.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_dus_display())); y
        c.drawString(x+2.9*inch , y+ 1.5* inch, "4. Tas")
        c.drawString(x+3.9*inch , y+ 1.5* inch, "%s "% (p.barang.get_tas_display())); y -=4*y1
        c.setFont("Helvetica", 10)
        c.drawString(x+0.7*inch  , y+1.5 * inch, "* Gadai Ulang pinjaman hanya dapat dilakukan sebanyak 1 (satu) kali."); y -=2*y1
    elif p.barang.jenis_kendaraan == u'1':###('6','MOTOR'),
        c.drawString(x+0.7*inch , y+ 1.5* inch, "Kelengkapan :"); y -=3*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "1. Bpkb")
        c.drawString(x+2.3*inch , y+ 1.5* inch, "%s "% (p.barang.get_bpkb_display())); y
        c.drawString(x+3.3*inch , y+ 1.5* inch, "2. Stnk")
        c.drawString(x+4.7*inch , y+ 1.5* inch, "%s "% (p.barang.get_stnk_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "3. Faktur")
        c.drawString(x+2.3*inch , y+ 1.5* inch, "%s "% (p.barang.get_faktur_display())); y
        c.drawString(x+3.3*inch , y+ 1.5* inch, "4. Gesek No Mesin")
        c.drawString(x+4.7*inch , y+ 1.5* inch, "%s "% (p.barang.get_gesek_nomesin_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "5. Gesek No Rangka")
        c.drawString(x+2.3*inch , y+ 1.5* inch, "%s "% (p.barang.get_gesek_norangka_display())); y -=4*y1
        c.setFont("Helvetica", 10)
        c.drawString(x+0.7*inch  , y+1.5 * inch, "* Gadai Ulang pinjaman hanya dapat dilakukan sebanyak 1 (satu) kali."); y -=2*y1
    elif p.barang.jenis_kendaraan == u'2':###('7','Mobil'),
        c.drawString(x+0.7*inch , y+ 1.5* inch, "Kelengkapan :"); y -=3*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "1. Bpkb")
        c.drawString(x+2.3*inch , y+ 1.5* inch, "%s "% (p.barang.get_bpkb_display())); y
        c.drawString(x+3.3*inch , y+ 1.5* inch, "2. Stnk")
        c.drawString(x+4.7*inch , y+ 1.5* inch, "%s "% (p.barang.get_stnk_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "3. Faktur")
        c.drawString(x+2.3*inch , y+ 1.5* inch, "%s "% (p.barang.get_faktur_display())); y
        c.drawString(x+3.3*inch , y+ 1.5* inch, "4. Gesek No Mesin")
        c.drawString(x+4.7*inch , y+ 1.5* inch, "%s "% (p.barang.get_gesek_nomesin_display())); y -=2*y1
        c.drawString(x+0.9*inch , y+ 1.5* inch, "5. Gesek No Rangka")
        c.drawString(x+2.3*inch , y+ 1.5* inch, "%s "% (p.barang.get_gesek_norangka_display())); y -=4*y1
        c.setFont("Helvetica", 10)
        c.drawString(x+0.7*inch  , y+1.5 * inch, "* Gadai Ulang pinjaman hanya dapat dilakukan sebanyak 1 (satu) kali."); y -=2*y1
    x,y = colom3
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x+0.7*inch , y+3.1 * inch, "Pihak II"); y -=2*y1
    c.setFont("Helvetica", 10)
    c.drawString(x+0.7*inch  , y+3.1 * inch, "Nama")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x+1.9*inch  , y+3.1 * inch, ": %s"%(p.agnasabah.nama)); y -=2*y1
    c.setFont("Helvetica", 10)
    c.drawString(x+0.7*inch  , y+3.1 * inch, "No Identitas")
    c.drawString(x+1.9*inch  , y+3.1 * inch, ": %s"%(p.agnasabah.no_ktp)); y -=2*y1
    c.drawString(x+0.7*inch  , y+3.1 * inch, "pekerjaan")
    c.drawString(x+1.9*inch  , y+3.1 * inch, ": %s"%(p.agnasabah.get_jenis_pekerjaan_display())); y -=2*y1
    c.drawString(x+0.7*inch  , y+3.1 * inch, "No Telepon")
    c.drawString(x+1.9*inch  , y+3.1 * inch, ": %s / %s "%(p.agnasabah.telepon_ktp,p.agnasabah.hp_ktp)); y -=2*y1
    c.drawString(x+0.7*inch  , y+3.1 * inch, "Tempat Tinggal")
    c.drawString(x+1.9*inch  , y+3.1 * inch, ": %s No %s RT/RW %s/%s "% (p.agnasabah.alamat_ktp,p.agnasabah.no_rumah_ktp,p.agnasabah.rt_ktp,p.agnasabah.rw_ktp)); y -=2*y1
    c.drawString(x+2*inch  , y+3.1 * inch, "Kel. %s Kec. %s"% (p.agnasabah.kelurahan_ktp,p.agnasabah.kecamatan_ktp)); y -=2*y1
    c.drawString(x+2*inch  , y+3.1 * inch, "Kota Madya %s Kab %s "% (p.agnasabah.kotamadya_ktp,p.agnasabah.kabupaten_ktp)); y -=2*y1
    c.drawString(x+0.7*inch  , y+3.1 * inch, "Almt S. Menyurat")
    c.drawString(x+1.9*inch  , y+3.1 * inch, ": %s No %s RT/RW %s/%s "% (p.agnasabah.alamat_domisili,p.agnasabah.no_rumah_domisili,p.agnasabah.rt_domisili,p.agnasabah.rw_domisili)); y -=2*y1
    c.drawString(x+2*inch  , y+3.1 * inch, "Kel. %s Kec. %s"% (p.agnasabah.kelurahan_domisili,p.agnasabah.kecamatan_domisili)); y -=2*y1
    c.drawString(x+2*inch  , y+3.1 * inch, "Kota Madya %s Kab %s "% (p.agnasabah.kotamadya_domisili,p.agnasabah.kabupaten_domisili)); y -=2*y1
    c.drawString(x+0.7*inch  , y+3.1 * inch, "Dalam hal ini bertindak untuk dan atas nama sendiri,"); y -=2*y1
    c.drawString(x+0.7*inch  , y+3.1 * inch, "selanjutnya disebut")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x+1.95*inch  , y+3.1 * inch, "Debitur"); y -=3*y1

    c.setFont("Helvetica-Bold", 10)
    c.drawString(x+0.7*inch  , y+3.1 * inch, "Nilai Pinjaman  : Rp.     %s"% (number_format(p.nilai))); y -=2*y1
    c.drawString(x+0.7*inch  , y+3.1 * inch,  " ## %s Rupiah ##"  % tb.title()); y -=2*y1
    c.setFont("Helvetica", 10)
    if p.jenis_transaksi == u'1': ###Elektronik
        c.drawString(x+0.7*inch  , y+3.1 * inch, "Jasa Pinjaman");
        c.drawString(x+1.9*inch  , y+3.1 * inch, ": Rp.");
        c.drawRightString(x+3.1*inch  , y+3.1 * inch, "%s "% (number_format(p.jasa_all())));y -=2*y1## Jasa Pinjaman
        c.drawString(x+0.7*inch  , y+3.1 * inch, "Biaya Administrasi"); 
        c.drawString(x+1.9*inch  , y+3.1 * inch, ": Rp.");
        c.drawRightString(x+3.1*inch  , y+3.1 * inch, "%s "% (number_format(p.adm_all()))); y -=2*y1
        c.drawString(x+0.7*inch  , y+3.1 * inch, "Biaya Simpan");
        c.drawString(x+1.9*inch  , y+3.1 * inch, ": Rp.");
        c.drawRightString(x+3.1*inch  , y+3.1 * inch, "%s "% (number_format(p.nilai_biayasimpan)));  
        c.drawString(x+3.3*inch  , y+3.5 * inch, "Jangka Waktu");
        c.drawString(x+4.4*inch  , y+3.5 * inch, ": %s [ Hari ]"% (p.jangka_waktu)); y -=2*y1

    else:
        c.drawString(x+0.7*inch  , y+3.1 * inch, "Jasa Pinjaman");
        c.drawString(x+1.9*inch  , y+3.1 * inch, ": Rp.");
        c.drawRightString(x+3.1*inch  , y+3.1 * inch, "%s "% (number_format(p.jasa_all())));y -=2*y1## Jasa Pinjaman
        c.drawString(x+0.7*inch  , y+3.1 * inch, "Biaya Administrasi"); 
        c.drawString(x+1.9*inch  , y+3.1 * inch, ": Rp.");
        c.drawRightString(x+3.1*inch  , y+3.1 * inch, "%s "% (number_format(p.adm_all()))); y -=2*y1
        c.drawString(x+0.7*inch  , y+3.1 * inch, "Biaya Simpan");
        c.drawString(x+1.9*inch  , y+3.1 * inch, ": Rp.");
        c.drawRightString(x+3.1*inch  , y+3.1 * inch, "%s "% (number_format(p.nilai_beasimpan_kendaraan)));  
        c.drawString(x+3.3*inch  , y+3.5 * inch, "Jangka Waktu");
        c.drawString(x+4.4*inch  , y+3.5 * inch, ": %s [ Bulan ]"% (p.jangka_waktu_kendaraan)); y -=2*y1            
    c.drawString(x+3.3*inch  , y+3.5 * inch, "Jatuh Tempo");
    c.drawString(x+4.4*inch  , y+3.5 * inch, ": %s "% (p.jatuhtempo.strftime('%d %b %Y'))); y -=2*y1
    if p.jns_gu == u'0':
        c.drawString(x+3.3*inch  , y+3.5 * inch, "Status Pinjaman");
        c.drawString(x+4.4*inch  , y+3.5 * inch, ": Pinjaman Baru"); 
    else:
        c.drawString(x+3.3*inch  , y+3.5 * inch, "Status Pinjaman");
        c.drawString(x+4.4*inch  , y+3.5 * inch, ": Gadai Ulang"); 

    if p.gerai.kode_cabang == u'318' or p.gerai.kode_cabang == u'317': ###Elektronik
        c.drawString(x+2*inch  , y+3.4 * inch, "Cirebon, %s" % sekarang.strftime('%d %b %Y') ); y -=3*y1
    else:
        c.drawString(x+2*inch  , y+3.2 * inch, "Bandung, %s" % sekarang.strftime('%d %b %Y') ); y -=3*y1
    c.drawString(x+0.7*inch  , y+3.2 * inch, "Kreditur,")   
    c.drawString(x+3.2*inch  , y+3.2 * inch, "Debitur,"); y -=12*y1
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x+0.7*inch ,y+3.2 * inch, "( %s )"%(p.gerai.nama_kg))
    c.drawString(x+3.2*inch  , y+3.2 * inch, "( %s )"%(p.agnasabah.nama))

    
    
    x,y = colom4
    y1 = 0.10 * inch

    y -=1*y1
    c.drawString(x+0.6*inch, y-2.8 * inch, "Keterangan :")
    c.setFont("Courier-Bold", 8)
    #c.drawString(x+7.6*inch, y-2.9 * inch, "Lembar Asli               : Debitur"); y -=y1
    #c.drawString(x+7.6*inch, y-2.9 * inch, "Lembar Copy (Bermaterai)  : Kreditur")
    c.setFont("Courier", 8)
    c.drawString(x+0.7*inch, y-2.9 * inch, "1. Pada saat pelunasan pinjaman Bukti ini harus dibawa"); y -=y1
    c.drawString(x+0.7*inch, y-2.9 * inch, "2. Apabila Bukti hilang agar segera melaporkan kepada pihak Koperasi"); y -=y1
    c.drawString(x+0.7*inch, y-2.9 * inch, "3. Ketentuan perjanjian tercantum di balik Bukti ini"); y -=y1

   


    c.showPage()

    header1=(4.25 *inch, (5.3 + 5.5) * inch)
    colom1 = (0.5*inch, (3.4 + 4.9) *inch)
            #ke kiri  ke atas ke bawah
    colom2 = (3.4*inch, (3.4 + 4.9) *inch)
    colom3 = (6.3*inch, (3.4 + 4.9) *inch)
    colom4 = (9.2*inch, (3.4 + 4.9) *inch)
    tb=terbilang(p.terima_bersih)
    #c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/logoksu_hitamputih.png'), 1.0*inch, (5.5 + 1.5) * inch, width=200.5/17.5*0.51*inch,height=120/17.5*0.51*inch)
    #c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 0.5*inch, (4.75 + 5.5) * inch, width=30/17.5*0.51*inch,height=25/17.5*0.51*inch,mask=None)
    
    x,y = header1
    y1 = 0.10 * inch

    y -=1*y1
    ####KOLOM 1 hiji Coy
    x,y = colom1
    y1 = 0.120 * inch
    c.drawString(x-0.3*inch, y, ""); y -=y1
    #c.line( x + 1.9 * inch , y-502 * inch, x + 1.9 * inch, y+102 * inch ) ; y -=y1
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.5*inch, y, "PERJANJIAN"); y -=y1
    c.drawString(x-0.3*inch, y, "PINJAMAN DENGAN JAMINAN BARANG"); y -=2*y1
    c.drawString(x+0.65*inch, y, "PASAL 1"); y -=y1
    c.drawString(x+0.65*inch, y, "DEFINISI"); y -=y1
    c.setFont("Helvetica",8)
    c.drawString(x-0.4*inch, y,"(1)")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  Unit  Usaha   Pinjaman  Jaminan  Barang"); y -=y1
    c.drawString(x-0.3*inch, y,"  (PJB)  adalah")
    c.setFont("Helvetica",8)
    c.drawString(x+0.55*inch, y,"merupakan unit usaha yang"); y -=y1
    
    c.drawString(x-0.3*inch, y,"  dimiliki  dan  dikelola  oleh  Koperasi   Rizky"); y -=y1
    c.drawString(x-0.3*inch, y,"  Abadi."); y -=2*y1
    c.setFont("Helvetica",8)
    c.drawString(x-0.4*inch, y,"(2)")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  PIHAK I            Kreditur")
    c.setFont("Helvetica",8)
    c.drawString(x+0.25*inch, y,"atau                  adalah    Koperasi"); y -=y1
    c.drawString(x-0.3*inch, y,"  Rizky     Abadi,    sebuah     badan     usaha    "); y -=y1
    c.drawString(x-0.3*inch, y,"  berbadan       hukum       koperasi        yang"); y -=y1
    c.drawString(x-0.3*inch, y,"  salah satu bidang usahanya adalah membe"); y -=y1
    c.drawString(x-0.3*inch, y,"  rikan  pinjaman   dengan   jaminan   barang"); y -=y1
    c.drawString(x-0.3*inch, y,"  kepada anggota/calon anggotanya."); y -=2*y1
    c.setFont("Helvetica",8)
    c.drawString(x-0.4*inch, y, "(3)")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  PIHAK II         Debitur")
    c.setFont("Helvetica",8)
    c.drawString(x+0.23*inch, y,"atau              adalah subjek hukum"); y -=y1
    c.drawString(x-0.3*inch, y,"  perorangan  maupun  badan   usaha    yang"); y -=y1
    c.drawString(x-0.3*inch, y,"  merupakan    anggota   /   calon      anggota"); y -=y1
    c.drawString(x-0.3*inch, y,"  Koperasi   yang    bermaksud   memperoleh"); y -=y1
    c.drawString(x-0.3*inch, y,"  fasilitas pinjaman dari PJB."); y -=2*y1
    c.setFont("Helvetica",8)
    c.drawString(x-0.4*inch, y,"(4)")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  Bukti Pinjaman")
    c.setFont("Helvetica",8)
    c.drawString(x+0.6*inch, y," adalah bukti yang sah atas "); y -=y1
    c.drawString(x-0.3*inch, y,"  pinjaman uang  yang telah  diterima  Debitur" ); y -=y1
    c.drawString(x-0.3*inch, y,"  sekaligus   merupakan    bukti   penyerahan  "); y -=y1
    c.drawString(x-0.3*inch, y,"  barang jaminan dari Debitur kepada Kreditur."); y -=2*y1
    c.setFont("Helvetica",8)
    c.drawString(x-0.4*inch, y,"(5)")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  Pinjaman")
    c.setFont("Helvetica",8)
    c.drawString(x+0.35*inch, y,"adalah  fasilitas  yang   disetujui "); y -=y1
    c.drawString(x-0.3*inch, y,"  Kreditur  atas  permohonan  yang   diajukan"); y -=y1
    c.drawString(x-0.3*inch, y,"  Debitur  berdasarkan  nilai  jaminan  barang"); y -=y1
    c.drawString(x-0.3*inch, y,"  yang dijaminkan Debitur."); y -=2*y1
    c.setFont("Helvetica",8)
    c.drawString(x-0.4*inch, y,"(6)")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  Jasa Pinjaman")
    c.setFont("Helvetica",8)
    c.drawString(x+0.55*inch, y,"adalah  nilai  yang  diberikan "); y -=y1
    c.drawString(x-0.3*inch, y,"  Debitur  kepada  Kreditur  terhadap  manfaat "); y -=y1
    c.drawString(x-0.3*inch, y,"  yang  diterima  Debitur  atas  pinjaman  yang"); y -=y1
    c.drawString(x-0.3*inch, y,"  diberikan  Kreditur."); y -=2*y1
    
    c.setFont("Helvetica",8)
    c.drawString(x-0.4*inch, y,"(7)")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  Biaya")
    c.setFont("Helvetica",8)
    c.drawString(x+0.1*inch, y,"adalah nominal tertentu  yang  ditetap"); y -=y1
    c.drawString(x-0.3*inch, y,"  kan  Kreditur  sehubungan  dengan  fasilitas"); y -=y1
    c.drawString(x-0.3*inch, y,"  pinjaman   yang  diterima  Debitur,   meliputi "); y -=y1
    c.drawString(x-0.3*inch, y,"  Biaya Administrasi dan Biaya Simpan "); y -=2*y1

    c.setFont("Helvetica",8)
    c.drawString(x-0.4*inch, y,"(8)") 
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  Jangka Waktu Pinjaman")
    c.setFont("Helvetica",8)
    c.drawString(x+1.15*inch, y,"adalah   periode "); y -=y1
    c.drawString(x-0.3*inch, y,"  masa pinjaman kepada Kreditur  atas  uang"); y -=y1
    c.drawString(x-0.3*inch, y,"  pinjaman yang diterima Debitur."); y -=2*y1
    c.setFont("Helvetica",8)
    c.drawString(x-0.4*inch, y,"(9)") 
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x-0.3*inch, y,"  Gadai Ulang (RO)")
    c.setFont("Helvetica",8)
    c.drawString(x+0.7*inch, y,"adalah penundaan kewa"); y -=y1
    c.drawString(x-0.3*inch, y,"  jiban pelunasan  pinjaman  selama  1 (satu) "); y -=y1
    c.drawString(x-0.3*inch, y,"  bulan atas permintaan Debitur, berdasarkan"); y -=y1
    c.drawString(x-0.3*inch, y,"  biaya    dan    ketentuan    yang   ditetapkan"); y -=y1
    c.drawString(x-0.3*inch, y,"  Kreditur."); y -=2*y1
   

    c.setFont("Helvetica",8)
    c.drawString(x-0.45*inch, y,"(10)") #jadi 10
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  Daluwarsa")
    c.setFont("Helvetica",8)
    c.drawString(x+0.4*inch, y,"adalah status pinjaman berikut"); y -=y1
    c.drawString(x-0.3*inch, y,"  barang jaminan yang  periode pinjamannya "); y -=y1
    c.drawString(x-0.3*inch, y,"  telah melampaui masa jatuh tempo."); y -=2*y1
    c.setFont("Helvetica",8)
    c.drawString(x-0.45*inch, y, "(11)")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  Pemberitahuan")
    c.setFont("Helvetica",8)
    c.drawString(x+0.6*inch, y,"adalah   berita  /  informasi "); y -=y1
    c.drawString(x-0.3*inch, y,"  yang   disampaikan  kepada   Debitur,  baik"); y -=y1
    c.drawString(x-0.3*inch, y,"  melalui  surat  maupun  media   komunikasi "); y -=y1
    c.drawString(x-0.3*inch, y,"  tertulis  lainnya  (SMS, e-mail, BBM)  terkait"); y -=y1            
    c.drawString(x-0.3*inch, y,"  masa pinjaman yang akan/telah jatuh tempo."); y -=2*y1            

    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.65*inch, y, "PASAL 2"); y -=y1
    c.drawString(x+0.25*inch, y, "MAKSUD DAN TUJUAN"); y -=2*y1
    c.setFont("Helvetica",8)
    c.drawString(x-0.3*inch, y,"Perjanjian ini dibuat oleh Kreditur atas permo"); y -=y1
    c.drawString(x-0.3*inch, y,"honan pinjaman yang diajukan  Debitur  atas"); y -=y1
       
    #c.line( x + 0.3*inch, y+0.1*inch , x + 11.1*inch, y+0.1*inch )
    ####Akhir KOLOM 1 hiji Coy

    ####KOLOM 2 Dua Coy
    x,y = colom2
    y1 = 0.120 * inch
    #c.line( x + 2.45 * inch , y-502 * inch, x + 2.45 * inch, y+102 * inch ) ; y -=y1
    #c.line( x + 1.9 * inch , y-502 * inch, x + 1.9 * inch, y+102 * inch ) ; y -=y1
    c.drawString(x-0.3*inch, y,"sejumlah uang dengan menyerahkan barang"); y -=y1
    c.drawString(x-0.3*inch, y,"jaminan selama jangka waktu tertentu sesuai"); y -=y1
    c.drawString(x-0.3*inch, y,"persetujuan  dan  kesepakatan  kedua  belah "); y -=y1
    c.drawString(x-0.3*inch, y,"pihak."); y -=2*y1
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.65*inch, y,"PASAL 3"); y -=y1
    c.drawString(x+0.25*inch, y,"HAK DAN KEWAJIBAN"); y -=y1
    c.setFont("Helvetica",8) 
    c.drawString(x-0.4*inch, y,"(1)")
    c.drawString(x-0.3*inch, y,"  Kreditur wajib memeriksa permohonan pinja"); y -=y1
    c.drawString(x-0.3*inch, y,"  man yang diajukan Debitur,  dan melakukan"); y -=y1
    c.drawString(x-0.3*inch, y,"  pengecekan atas  kalaikan  barang  jaminan "); y -=y1  
    c.drawString(x-0.3*inch, y,"  yang akan dijaminkan oleh Debitur."); y -=y1   

    c.drawString(x-0.3*inch, y, ""); y -=y1
    c.setFont("Helvetica", 8)
    c.drawString(x-0.4*inch, y,"(2)")
    c.drawString(x-0.3*inch, y,"  Kreditur  wajib  menjaga   keamanan   serta"); y -=y1
    c.drawString(x-0.3*inch, y,"  keutuhan barang  jaminan yang  diserahkan"); y -=y1
    c.drawString(x-0.3*inch, y,"  Debitur  kepadanya  sampai  dengan  masa"); y -=y1
    c.drawString(x-0.3*inch, y,"  perjanjian ini berakhir."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(3)")
    c.drawString(x-0.3*inch, y,"  Debitur wajib  mengembalikan  pinjaman se"); y -=y1
    c.drawString(x-0.3*inch, y,"  suai   dengan    periode     pinjaman    yang"); y -=y1
    c.drawString(x-0.3*inch, y,"  disepakati."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(4)")
    c.drawString(x-0.3*inch, y,"  Debitur    wajib     menyampaikan     barang"); y -=y1
    c.drawString(x-0.3*inch, y,"  jaminan   dalam   kondisi   yang   baik   dan"); y -=y1
    c.drawString(x-0.3*inch, y,"  menyertakan    tanda     bukti    kepemilikan"); y -=y1
    c.drawString(x-0.3*inch, y,"  barang  (kuitansi  pembelian)."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(5)")
    c.drawString(x-0.3*inch, y,"  Kreditur berhak untuk menolak permohonan"); y -=y1
    c.drawString(x-0.3*inch, y,"  pinjaman    yang   diajukan   Debitur   berda"); y -=y1
    c.drawString(x-0.3*inch, y,"  sarkan   hak  penilaian  mutlak  yang  dimiliki"); y -=y1
    c.drawString(x-0.3*inch, y,"  Kreditur."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(6)")
    c.drawString(x-0.3*inch, y,"  Kreditur  berhak  untuk  menguasai  barang"); y -=y1
    c.drawString(x-0.3*inch, y,"  jaminan sampai dengan  pinjaman  yang  di"); y -=y1
    c.drawString(x-0.3*inch, y,"  terima    Debitur     dinyatakan   lunas   oleh"); y -=y1
    c.drawString(x-0.3*inch, y,"  Kreditur."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(7)")
    c.drawString(x-0.3*inch, y,"  Kreditur   berhak   untuk   menjual    barang"); y -=y1
    c.drawString(x-0.3*inch, y,"  jaminan  yang  diserahkan  Debitur  apabila"); y -=y1
    c.drawString(x-0.3*inch, y,"  sampai dengan masa  pinjaman yang  telah"); y -=y1
    c.drawString(x-0.3*inch, y,"  disepakati     Debitur      tidak      melakukan "); y -=y1            
    c.drawString(x-0.3*inch, y,"  pelunasan pinjaman kepada pihak Kreditur."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(8)")
    c.drawString(x-0.3*inch, y,"  Debitur  berhak   untuk  memperoleh   dana"); y -=y1
    c.drawString(x-0.3*inch, y,"  pinjaman  apabila  Debitur  telah  menyerah"); y -=y1
    c.drawString(x-0.3*inch, y,"  kan   barang  jaminan  sesuai  kriteria  yang"); y -=y1
    c.drawString(x-0.3*inch, y,"  ditentukan  oleh  pihak  Kreditur. "); y -=2*y1            
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.55*inch, y,"PASAL 4"); y -=y1
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.1*inch, y,"PELUNASAN PINJAMAN "); y -=y1
    c.drawString(x-0.3*inch, y,"DAN PENGAMBILAN BARANG JAMINAN"); y -=2*y1
    c.setFont("Helvetica", 8) 
    c.drawString(x-0.4*inch, y,"(1)")
    c.drawString(x-0.3*inch, y,"  Untuk    melakukan    pelunasan    pinjaman"); y -=y1
    c.drawString(x-0.3*inch, y,"  serta  mengambil  barang  jaminan,  Debitur"); y -=y1
    c.drawString(x-0.3*inch, y,"  harus    melakukannya    sendiri    ke   gerai"); y -=y1
    c.drawString(x-0.3*inch, y,"  tempat dimana  Debitur  melakukan  pemin-"); y -=y1
    c.drawString(x-0.3*inch, y,"  jaman, dengan membawa  Bukti   asli   dan"); y -=y1
    c.drawString(x-0.3*inch, y,"  identitas diri."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(2)")
    c.drawString(x-0.3*inch, y,"  Dalam  hal   Debitur    berhalangan    untuk"); y -=y1
    c.drawString(x-0.3*inch, y,"  melakukan   pelunasan    pinjaman   secara"); y -=y1
    c.drawString(x-0.3*inch, y,"  langsung pada waktu yang telah ditentukan,"); y -=y1
    c.drawString(x-0.3*inch, y,"  Debitur   dapat   diwakili   oleh   kuasa   ahli"); y -=y1
    c.drawString(x-0.3*inch, y,"  warisnya  untuk  melakukan  pelunasan dan"); y -=y1
    c.drawString(x-0.3*inch, y,"  pengambilan barang jaminan  dengan mem"); y -=y1
    c.drawString(x-0.3*inch, y,"  bawa   Bukti   asli,  Surat Kuasa bermaterai,"); y -=y1            
    c.drawString(x-0.3*inch, y,"  Asli  KTP  Pemberi  dan   Penerima  Kuasa,"); y -=y1            
    c.drawString(x-0.3*inch, y,"  serta Surat Kematian  dan  Keterangan  Ahli  "); y -=y1
    c.drawString(x-0.3*inch, y,"  Waris    dari    kelurahan   apabila    Debitur "); y -=y1  
    c.drawString(x-0.3*inch, y,"  meninggal dunia."); y -=2*y1  

    ####AKHiR KOLOM 2 Dua Coy



    ####KOLOM 3 Tilu Coy
    #y -=  2 * y1
    #y2 = y + 0.1 * inch
    #c.setFont("Courier-Bold", 14)
               
            
    x,y = colom3
    y1 = 0.120 * inch
    #c.line( x + 2.45 * inch , y-502 * inch, x + 2.45 * inch, y+102 * inch ) ; y -=y1
    #c.line( x + 1.9 * inch , y-502 * inch, x + 1.9 * inch, y+102 * inch ) ; y -=y1
    c.drawString(x-0.4*inch, y, "(3)")
    c.drawString(x-0.3*inch, y,"  Untuk   kelancaran   pengembalian   barang"); y -=y1
    c.drawString(x-0.3*inch, y,"  jaminan  Debitur  wajib menyampaikan pem"); y -=y1
    c.drawString(x-0.3*inch, y,"  beritahuan ke petugas gerai tempat dimana"); y -=y1
    c.drawString(x-0.3*inch, y,"  Debitur   melakukan    transaksi    pinjaman, "); y -=y1
    c.drawString(x-0.3*inch, y,"  paling    lambat   1   ( satu )   hari    sebelum "); y -=y1
    c.drawString(x-0.3*inch, y,"  pelunasan dilakukan."); y -=y1

    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.55*inch, y, ""); y -=y1
    c.drawString(x+0.55*inch, y, "PASAL 5"); y -=y1
    c.drawString(x+0.40*inch, y, "JATUH TEMPO"); y -=2*y1
    c.setFont("Helvetica", 8)
    c.drawString(x-0.4*inch, y,"(1)")
    c.drawString(x-0.3*inch, y,"  Pinjaman  dikategorikan  telah  jatuh tempo"); y -=y1
    c.drawString(x-0.3*inch, y,"  apabila  sampai  dengan batas  waktu yang"); y -=y1
    c.drawString(x-0.3*inch, y,"  ditentukan      Debitur     tidak     melakukan"); y -=y1
    c.drawString(x-0.3*inch, y,"  pelunasan   pinjaman   kepada   Kreditur."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(2)")
    c.drawString(x-0.3*inch, y,"  Terhadap  pinjaman yang telah jatuh tempo,"); y -=y1
    c.drawString(x-0.3*inch, y,"  Kreditur    akan    menyampaikan   Pemberi"); y -=y1
    c.drawString(x-0.3*inch, y,"  tahuan   secara   layak,  baik   melalui  surat"); y -=y1
    c.drawString(x-0.3*inch, y,"  maupun media  lainnya ke alamat  /  nomor"); y -=y1
    c.drawString(x-0.3*inch, y,"  kontak  yang   dicantumkan  Debitur  sesuai"); y -=y1
    c.drawString(x-0.3*inch, y,"  Bukti  ini   untuk   segera   melunasi   pokok"); y -=y1
    c.drawString(x-0.3*inch, y,"  pinjaman  beserta  denda / biaya  lain  yang"); y -=y1
    c.drawString(x-0.3*inch, y,"  ditetapkan oleh pihak Kreditur."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(3)")
    c.drawString(x-0.3*inch, y,"  Apabila    Kreditur    telah     menyampaikan"); y -=y1
    c.drawString(x-0.3*inch, y,"  Pemberitahuan     secara     layak     namun"); y -=y1
    c.drawString(x-0.3*inch, y,"  Debitur  tetap   tidak  melakukan pelunasan"); y -=y1
    c.drawString(x-0.3*inch, y,"  pinjaman sesuai  batas waktu  yang ditentu"); y -=y1
    c.drawString(x-0.3*inch, y,"  kan dalam pemperitahuan tersebut, maka 7"); y -=y1
    c.drawString(x-0.3*inch, y,"  (Tujuh) hari terhitung sejak tanggal pemberi"); y -=y1
    c.drawString(x-0.3*inch, y,"  tahuan    disampaikan,   Debitur    dianggap"); y -=y1
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x-0.3*inch, y,"  setuju  untuk  melepaskan hak  kepemilikan"); y -=y1
    c.drawString(x-0.3*inch, y,"  atas barang jaminan"); 
    c.setFont("Helvetica", 8)
    c.drawString(x+0.8*inch, y,"  dan Barang   jaminan"); y -=y1
    c.drawString(x-0.3*inch, y,"  tersebut dianggap Daluwarsa."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(4)")
    c.drawString(x-0.3*inch, y,"  Untuk kepentingan pelunasan pinjaman Deb"); y -=y1
    c.drawString(x-0.3*inch, y,"  itur serta mengacu  pada   ketentuan  dalam "); y -=y1
    c.drawString(x-0.3*inch, y,"  Pasal 3  ayat  (7)  tersebut  di  atas, Kreditur  "); y -=y1
    c.drawString(x-0.3*inch, y,"  berhak  menjual  barang  jaminan kepada  pi"); y -=y1
    c.drawString(x-0.3*inch, y,"  hak ketiga,  guna  keperluan  pelunasan  pin"); y -=y1
    c.drawString(x-0.3*inch, y,"  jaman  Debitur terhadap Kreditur,   sehingga"); y -=y1
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x-0.3*inch, y,"  Debitur tidak dapat mengajukan keberatan"); y -=y1
    c.drawString(x-0.3*inch, y,"  /upaya apapun atas  pengalihan  hak kepe"); y -=y1
    c.drawString(x-0.3*inch, y,"  milikan atas barang jaminan tersebut."); y -=2*y1
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.60*inch, y,"PASAL 6"); y -=y1
    c.drawString(x+0.20*inch, y,"BIAYA KETERLAMBATAN"); y -=2*y1
    c.setFont("Helvetica", 8)
    c.drawString(x-0.3*inch, y,"  Apabila terjadi   keterlambatan   pada   saat"); y -=y1
    c.drawString(x-0.3*inch, y,"  dilakukan   pelunasan  oleh   debitur,  maka"); y -=y1
    c.drawString(x-0.3*inch, y,"  debitur  harus  membayar   biaya   keterlam"); y -=y1
    c.drawString(x-0.3*inch, y,"  batan yang ditetapkan oleh Kreditur."); y -=2*y1
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.60*inch, y,"PASAL 7"); y -=y1
    c.drawString(x+0.1*inch, y,"GADAI ULANG PINJAMAN (RO)"); y -=2*y1
    c.setFont("Helvetica", 8)
    c.drawString(x-0.3*inch, y, "Gadai Ulang pinjaman hanya dapat dilakukan"); y -=y1
    c.drawString(x-0.3*inch, y, "sebanyak 1 (satu) kali."); y -=2*y1

    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.60*inch, y,"PASAL 8"); y -=y1
    c.drawString(x+0.5*inch, y,"GANTI RUGI"); y -=2*y1
    c.setFont("Helvetica", 8)

    c.drawString(x-0.3*inch, y,"Kreditur akan memberikan ganti kerugian apabila"); y -=y1
    c.drawString(x-0.3*inch, y,"barang jaminan yang berada dalam penguasaan"); y -=y1
    c.drawString(x-0.3*inch, y,"Kreditur  sampai  dengan  berakhirnya  perjanjian"); y -=y1
    c.drawString(x-0.3*inch, y,"mengalami  kerusakan  (bukan  merupakan  keru"); y -=y1
    c.drawString(x-0.3*inch, y,"sakan  software)   atau  hilang  yang  tidak  diseb"); y -=y1
    c.drawString(x-0.3*inch, y,"abkan  oleh  suatu  bencana alam (force majeure) "); y -=y1
    c.drawString(x-0.3*inch, y,"yang ditetapkan pemerintah."); y -=2*y1

    ####AKHiR KOLOM 3 Tilu Coy

    ####KOLOM 4 Opat Coy
    x,y = colom4
    y1 = 0.120 * inch
    #c.line( x + 2.45 * inch , y-502 * inch, x + 2.45 * inch, y+102 * inch ) ; y -=y1
    #c.line( x + 1.9 * inch , y-502 * inch, x + 1.9 * inch, y+102 * inch ) ; y -=y1
    c.drawString(x-0.3*inch, y, ""); y -=y1
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.55*inch, y, "PASAL 9"); y -=y1
    c.drawString(x+0*inch, y, "PERNYATAAN DAN JAMINAN"); y -=2*y1
    c.setFont("Helvetica", 8)
    c.drawString(x-0.4*inch, y, "(1)")
    c.drawString(x-0.3*inch, y,"  Debitur  dengan    ini    menyatakan  bahwa"); y -=y1
    c.drawString(x-0.3*inch, y,"  barang  jaminan yang  diserahkan   kepada"); y -=y1
    c.drawString(x-0.3*inch, y,"  Kreditur adalah benar barang milik  Debitur,"); y -=y1
    c.drawString(x-0.3*inch, y,"  dan  tidak  diperoleh  dari  hasil   kejahatan/"); y -=y1
    c.drawString(x-0.3*inch, y,"  tindak   pidana.   Oleh   karenanya   Debitur"); y -=y1
    c.drawString(x-0.3*inch, y,"  melepaskan pihak Kreditur segala tanggung"); y -=y1
    c.drawString(x-0.3*inch, y,"  jawab dari  segala tuntutan pihak ketiga."); y -=2*y1
    c.drawString(x-0.4*inch, y, "(2)")
    c.drawString(x-0.3*inch, y,"  Debitur menyatakan bahwa barang jaminan"); y -=y1
    c.drawString(x-0.3*inch, y,"  yang diserahkan kepada Kreditur adalah asli,"); y -=y1
    c.drawString(x-0.3*inch, y,"  bukan replika, tiruan, palsu.  Apabila  dikemu"); y -=y1
    c.drawString(x-0.3*inch, y,"  dian hari ditemukan fakta bahwa barang jami"); y -=y1
    c.drawString(x-0.3*inch, y,"  nan tersebut replika,  tiruan dan / atau  palsu"); y -=y1
    c.drawString(x-0.3*inch, y,"  maka  Debitur   menyatakan  sanggup  untuk "); y -=y1
    c.drawString(x-0.3*inch, y,"  mengganti barang  jaminan dan/atau memba"); y -=y1
    c.drawString(x-0.3*inch, y,"  yar ganti kerugian yang diderita Kreditur akib"); y -=y1
    c.drawString(x-0.3*inch, y,"  at penyerahan  barang   jaminan  yang  tidak "); y -=y1
    c.drawString(x-0.3*inch, y,"  sesuai."); y -=2*y1
    c.drawString(x-0.4*inch, y,"(3)")
   
    c.drawString(x-0.3*inch, y,"  Debitur   menyatakan   telah   membaca  dan "); y -=y1
    c.drawString(x-0.3*inch, y,"  memahami isi Perjanjian ini serta tunduk dan"); y -=y1
    c.drawString(x-0.3*inch, y,"  mengikuti  terhadap   aturan   yang   tertuang "); y -=y1
    c.drawString(x-0.3*inch, y,"  dalam perjanjian ini."); y -=2*y1
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x+0.60*inch, y, "PASAL 10"); y -=y1
    c.drawString(x+0.55*inch, y, "PENUTUP"); y -=2*y1
    c.setFont("Helvetica", 8)
    c.drawString(x-0.3*inch, y, "Apabila terjadi  perselisihan dikemudian hari,"); y -=y1
    c.drawString(x-0.3*inch, y, "maka akan diselesaikan secara musyawarah"); y -=y1
    c.drawString(x-0.3*inch, y, "untuk   mufakat dan   apabila  tidak   tercapai "); y -=y1
    c.drawString(x-0.3*inch, y, "kesepakatan    akan     diselesaikan    sesuai"); y -=y1
    c.drawString(x-0.3*inch, y, "hukum yang berlaku. Demikian perjanjian  ini"); y -=y1
    c.drawString(x-0.3*inch, y, "dibuat    dengan    sebenar  -  benarnya   dan "); y -=y1
    c.drawString(x-0.3*inch, y, "mengikat      kedua      belah    pihak,   serta "); y -=y1
    c.drawString(x-0.3*inch, y, "ditandatangani  oleh  masing - masing  pihak"); y -=y1
    c.drawString(x-0.3*inch, y, "dan mempunyai kekuatan hukum yang sama."); y -=2*y1
    if p.gerai.kode_cabang == u'318' or p.gerai.kode_cabang == u'317': ###Elektronik
        c.drawString(x+0.3*inch, y, "Cirebon, %s" % sekarang.strftime('%d %b %Y') ); y -=2*y1
    else:
        c.drawString(x+0.3*inch, y, "Bandung, %s" % sekarang.strftime('%d %b %Y') ); y -=2*y1
    #c.drawString(x-0.3*inch, y, ""); y -=2*y1
    c.drawString(x+0.65*inch, y, "Debitur,"); y -=5*y1
    c.drawString(x+0.46*inch, y, "Materai Rp.6.000"); y -=8*y1
    c.drawString(x+0.18*inch, y, "(..............................................)"); y -=3*y1
    c.drawString(x+0.65*inch, y, "Kreditur,"); y -=7*y1
    c.drawString(x+0.18*inch, y, "(..............................................)"); y -=2*y1
    c.drawString(x+0.6*inch, y, "Kepala Gerai")

    c.showPage()
            ####AKHIR KOLOM 4 Opat Coy
    c.save()
    return response

def kwitansi(request, object_id):
    pk = AkadGadai.objects.get(id=object_id)
    pk.status_kw = '1'
    pk.save()
    #tiga_play = [p,p,p]
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s.pdf' % pk.norek()
    c = canvas.Canvas(response, pagesize=(9.5*inch, 11*inch))
    c.setTitle("kwitansi %s" % pk.norek())
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
        trk=pk.tanggal
        dd=patokan.month-trk.month
        yy=patokan.year-trk.year


    header1=(4.25 *inch, (5.3 + 5.5) * inch)
    colom1 = (0.5*inch, (4.3 + 5.5) *inch)
            #ke kiri  ke atas ke bawah
    colom2 = (6.7*inch, (4.5 + 5.5) *inch)
    colom3 = (6.0*inch, (4.8 + 4.5) *inch)
    colom4 = (0.5*inch, (3.7 + 4.5) *inch)

    header2=(8.25 *inch, (2.75 + 2.5) * inch)    
    header3=(4.25 *inch, (2.8 + 2.65) * inch)        
    #header2=(4.25 *inch, (5.3 + 5.5) * inch)
    colom5 = (0.5*inch, (2.15 + 2.3) *inch)
            #ke kiri  ke atas ke bawah
    colom6 = (6.7*inch, (2.15 + 2.3) *inch)
    colom7 = (6.0*inch, (2.25 + 1.5) *inch)
    colom8 = (0.5*inch, (1.5 + 1.1) *inch)
    tb=terbilang(pk.terima_bersih_kwitansi)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/logoksu_hitamputih.png'), 1.0*inch, (5.5 + 1.5) * inch, width=200.5/17.5*0.51*inch,height=120/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 0.5*inch, (4.75 + 5.5) * inch, width=30/17.5*0.51*inch,height=25/17.5*0.51*inch,mask=None)
    
    x,y = header1
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Courier-Bold", 16)
    c.drawString(6.2 * inch , y, "KWITANSI"); y -=y1
    c.line( 6.2 * inch , y+0.06* inch , 7.5 * inch ,y+0.06* inch ) ; y -=y1
    c.setFont("Courier-Bold", 16)
    c.drawString(x-2.8*inch, y+0.20*inch, "KSU RIZKY ABADI"); y -=y1
    c.setFont("Courier",8)
    c.drawString(x-2.8*inch, y+0.20*inch, "Badan Hukum No.518/BH.88-DISKOP/THN.2007 Tgl 27 Desember 2007"); y -=y1
    c.drawString(x-2.8*inch, y+0.20*inch, "%s/Telp: 0%s "% (pk.gerai.alamat, pk.gerai.no_telp)); y -=y1
    #c.drawString(x-2.8*inch, y+0.20*inch, "Jln Cisaranten Kulon IV No.55 Bandung Tlp: 022-7808443"); y -=y1
    kb = str.upper(str(pk.gerai.nama_cabang))
    c.setFont("Courier-Bold", 11)
    c.drawString(6.2 * inch , y+0.30*inch,"%s" % (pk.gerai.nama_cabang)); y -=y1      
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
    c.drawString(600, 780, "%s" % sekarang.strftime('[%-b][%Y]') )
    barcode = code128.Code128("%s" % (pk.norek()))
    barcode.drawOn(c, 195*mm, 268*mm)

    ## QR CODE
    #qrw = QrCodeWidget('http://pjb02.ksura.co.id/akadgadai/106262/label/') 
    #b = qrw.getBounds()
    #w=b[2]-b[0] 
    #h=b[3]-b[1] 
    #d = Drawing(100,100,transform=[75./w,0,0,75./h,585,720]) 
    #d.add(qrw)
    #renderPDF.draw(d, c, 1, 1)
    ## AKHIR QR CODE               
            
    c.setFont("Courier", 11)
    x,y = colom2
    y1 = 0.165 * inch
    c.setFont("Courier", 9)
    c.drawString(x, y, "No PK"); 
    c.drawString(x+1.2*inch, y, ": %s" % (pk.norek())); y -=y1
    c.drawString(x, y, "Tgl Transaksi");
    c.drawString(x+1.2*inch, y, ": %s" % (pk.tanggal.strftime('%d %b %Y'))); y -=y1
    
    c.drawString(x, y, "Tgl Jth tempo");
    c.drawString(x+1.2*inch, y, ": %s" %  (pk.jatuhtempo.strftime('%d %b %Y'))); y -=y1
    c.drawString(x, y, "Jangka waktu") ;
    c.drawString(x+1.2*inch, y, ": %s [Hari]" %  (pk.jangka_waktu)) ; y -=y1
    ####AKHiR KOLOM 2 Dua Coy

    ####KOLOM 3 Tilu Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    c.setFont("Courier-Bold", 14)
               
            
    c.setFont("Courier", 11)
    x,y = colom3
    y1 = 0.165 * inch
    c.setFont("Courier", 9)
    c.drawString(x, y, "Nilai Pinjaman")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.9*inch, y,"%s"% (number_format(pk.nilai))); y -=y1
    c.drawString(x, y, "Bea Simpan/Survey")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"% (number_format(pk.biayasimpan))); y -=y1
    c.drawString(x, y, "Bea Administrasi")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"%(number_format(pk.adm))); y -=y1
    c.drawString(x, y, "Jasa") 
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"%(number_format(pk.jasa_kwitansi()))); y -=y1
    c.drawString(x, y, "Bea Materai")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"% (number_format(pk.bea_materai)))
    c.line( x+1.7*inch , y-0.05*inch , 9.0 * inch , y-0.05*inch ) ; y -=y1

    c.drawString(x, y, "Total Biaya") 
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.9*inch, y,"%s"%(number_format(pk.jumlahbiaya_kwitansi)))
    c.line( x+1.7*inch , y-0.05*inch , 9.0 * inch , y-0.05*inch ) ; y -=y1
    c.setFont("Courier-Bold", 9)
    c.drawString(x, y, "Nilai Diterima")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.9*inch, y," %s"% (number_format(pk.terima_bersih_kwitansi)));y -=y1


    ####AKHiR KOLOM 3 Tilu Coy

    ####KOLOM 1 hiji Coy
    x,y = colom1
    y1 = 0.165 * inch
    
    c.setFont("Courier", 11)
    c.drawString(x, y, "Nomor Debitur : %s" % (pk.nonas())); y -=3*y1
    c.drawString(x, y, "Nama          : %s" % (pk.agnasabah.nama)); y -=y1
    c.drawString(x, y, "Alamat        : %s No %s" %(pk.agnasabah.alamat_domisili,pk.agnasabah.no_rumah_domisili)); y -=y1
    c.drawString(x, y, "                RT/RW %s/%s %s" %(pk.agnasabah.rt_domisili,pk.agnasabah.rw_domisili,pk.agnasabah.kelurahan_domisili,)); y -=y1
    c.drawString(x, y, "No KTP        : %s " %(pk.agnasabah.no_ktp)); y -=y1
    c.drawString(x, y, "No Tlp / HP   : %s / %s " %(pk.agnasabah.telepon_domisili,pk.agnasabah.hp_domisili)); y -=y1
    ####AKHIR KOLOM 1 hiji Coy

    ####KOLOM 4 Opat Coy
    x,y = colom4
    y1 = 0.165 * inch

    c.setFont("Courier", 11)
    c.drawString(x, y+0.1*inch, "Sudah menerima dari KSU RIZKY ABADI," ); y -=y1
    #c.drawString(x, y, "Pembayaran Jaminan  : %s|%s|%s|%s"% (pk.barang.merk,pk.barang.sn,pk.barang.type,pk.barang.accesoris_barang1 )); y -=y1
    c.drawString(x, y+0.1*inch, "Pembayaran Jaminan  :" )
    c.setFont("Courier", 10)
    c.drawString(x+1.9*inch, y+0.1*inch, " %s|%s|%s|"% (pk.barang.merk,pk.barang.sn,pk.barang.warna )); y -=y1
    c.drawString(x+1.9*inch, y+0.15*inch, " %s|%s|"% (pk.barang.type,pk.barang.accesoris_barang1 ))
    c.setFont("Courier", 11)
    c.drawString(x, y, "Jenis Pinjaman      : Pinjaman Baru"); y -=1.5*y1
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
    c.drawString(x, y+1.2*inch, "Kepala Gerai,")
    c.drawString(x+6.9*inch, y+1.2*inch, "Debitur,") ; 
    #c.line(410, 488, 500, 488)
    c.drawString(x,y+0.3*inch, "%s"%(pk.gerai.nama_kg))
    c.drawString(x+6.9*inch,y+0.3*inch,"%s"%(pk.agnasabah.nama)) 
    #c.line(550, 488, 650, 488)
    c.setFont("Courier",8)
    c.drawString(x, y, "*Kwitansi ini sah apabila telah di validasi di tanda tangan dan di stample*"); y -=y1
    c.drawString(x, y, " Lembar 1/3 Gerai, Asli "); y -=y1
    c.drawString(x-2.5 * inch, y," - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - " )

    #######BARUUUU 123

    tb=terbilang(pk.terima_bersih_kwitansi)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/logoksu_hitamputih.png'), 1.0*inch, (-0.1 + 1.5) * inch, width=200.5/17.5*0.51*inch,height=120/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 0.5*inch, (2.4 + 2.5) * inch, width=30/17.5*0.51*inch,height=25/17.5*0.51*inch,mask=None)

    y -=  2 * y1
    y2 = y + 0.1 * inch
    ## Barcode
    c.setFont("Courier", 7)
    c.drawString(x+7.73 * inch, y+0.2 * inch, "%s" % sekarang.strftime('[%-b][%Y]') )
    barcode = code128.Code128("%s" % (pk.norek()))
    barcode.drawOn(c, 195*mm, 132*mm)
    x,y = header3
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Courier-Bold", 16)
    c.drawString(6.2 * inch , y, "KWITANSI"); y -=y1
    c.line( 6.2 * inch , y+0.06* inch , 7.5 * inch ,y+0.06* inch ) ; y -=y1
    c.setFont("Courier-Bold", 16)
    c.drawString(x-2.8*inch, y+0.20*inch, "KSU RIZKY ABADI"); y -=y1
    c.setFont("Courier",8)
    c.drawString(x-2.8*inch, y+0.20*inch, "Badan Hukum No.518/BH.88-DISKOP/THN.2007 Tgl 27 Desember 2007"); y -=y1
    c.drawString(x-2.8*inch, y+0.20*inch, "%s/Telp: 0%s"% (pk.gerai.alamat, pk.gerai.no_telp)); y -=y1
    #c.drawString(x-2.8*inch, y+0.20*inch, "Jln Cisaranten Kulon IV No.55 Bandung Tlp: 022-7808443"); y -=y1
    kb = str.upper(str(pk.gerai.nama_cabang))
    c.setFont("Courier-Bold", 11)
    c.drawString(6.2 * inch , y+0.30*inch,"%s" % (pk.gerai.nama_cabang)); y -=y1      
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
    c.drawString(600, 780, "%s" % sekarang.strftime('[%-b][%Y]') )
    barcode = code128.Code128("%s" % (pk.norek()))
    barcode.drawOn(c, 195*mm, 268*mm)
               
            
    c.setFont("Courier", 11)
    x,y = colom6
    y1 = 0.165 * inch
    c.setFont("Courier", 9)
    c.drawString(x, y, "No PK"); 
    c.drawString(x+1.2*inch, y, ": %s" % (pk.norek())); y -=y1
    c.drawString(x, y, "Tgl Transaksi");
    c.drawString(x+1.2*inch, y, ": %s" % (pk.tanggal.strftime('%d %b %Y'))); y -=y1
    
    c.drawString(x, y, "Tgl Jth tempo");
    c.drawString(x+1.2*inch, y, ": %s" %  (pk.jatuhtempo.strftime('%d %b %Y'))); y -=y1
    c.drawString(x, y, "Jangka waktu") ;
    c.drawString(x+1.2*inch, y, ": %s [Hari]" %  (pk.jangka_waktu)) ; y -=y1
    ####AKHiR KOLOM 2 Dua Coy

    ####KOLOM 3 Tilu Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    c.setFont("Courier-Bold", 14)
               
            
    c.setFont("Courier", 11)
    x,y = colom7
    y1 = 0.165 * inch
    c.setFont("Courier", 9)
    c.drawString(x, y, "Nilai Pinjaman")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.9*inch, y,"%s"% (number_format(pk.nilai))); y -=y1
    c.drawString(x, y, "Bea Simpan/Survey")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"% (number_format(pk.biayasimpan))); y -=y1
    c.drawString(x, y, "Bea Administrasi")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"%(number_format(pk.adm))); y -=y1
    c.drawString(x, y, "Jasa") 
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"%(number_format(pk.jasa_kwitansi()))); y -=y1
    c.drawString(x, y, "Bea Materai")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"% (number_format(pk.bea_materai)))
    c.line( x+1.7*inch , y-0.05*inch , 9.0 * inch , y-0.05*inch ) ; y -=y1

    c.drawString(x, y, "Total Biaya") 
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.9*inch, y,"%s"%(number_format(pk.jumlahbiaya_kwitansi)))
    c.line( x+1.7*inch , y-0.05*inch , 9.0 * inch , y-0.05*inch ) ; y -=y1
    c.setFont("Courier-Bold", 9)
    c.drawString(x, y, "Nilai Diterima")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.9*inch, y," %s"% (number_format(pk.terima_bersih_kwitansi)));y -=y1


    ####AKHiR KOLOM 3 Tilu Coy

    ####KOLOM 1 hiji Coy
    x,y = colom5
    y1 = 0.165 * inch
    
    c.setFont("Courier", 11)
    c.drawString(x, y, "Nomor Debitur : %s" % (pk.nonas())); y -=3*y1
    c.drawString(x, y, "Nama          : %s" % (pk.agnasabah.nama)); y -=y1
    c.drawString(x, y, "Alamat        : %s No %s" %(pk.agnasabah.alamat_domisili,pk.agnasabah.no_rumah_domisili)); y -=y1
    c.drawString(x, y, "                RT/RW %s/%s %s" %(pk.agnasabah.rt_domisili,pk.agnasabah.rw_domisili,pk.agnasabah.kelurahan_domisili,)); y -=y1
    c.drawString(x, y, "No KTP        : %s " %(pk.agnasabah.no_ktp)); y -=y1
    c.drawString(x, y, "No Tlp / HP   : %s / %s " %(pk.agnasabah.telepon_domisili,pk.agnasabah.hp_domisili)); y -=y1
    ####AKHIR KOLOM 1 hiji Coy

    ####KOLOM 4 Opat Coy
    x,y = colom8
    y1 = 0.165 * inch

    c.setFont("Courier", 11)
    c.drawString(x, y+0.1*inch, "Sudah menerima dari KSU RIZKY ABADI," ); y -=y1
    #c.drawString(x, y, "Pembayaran Jaminan  : %s|%s|%s|%s"% (pk.barang.merk,pk.barang.sn,pk.barang.type,pk.barang.accesoris_barang1 )); y -=y1
    c.drawString(x, y+0.1*inch, "Pembayaran Jaminan  :" )
    c.setFont("Courier", 10)
    c.drawString(x+1.9*inch, y+0.1*inch, " %s|%s|%s|"% (pk.barang.merk,pk.barang.sn,pk.barang.warna )); y -=y1
    c.drawString(x+1.9*inch, y+0.15*inch, " %s|%s|"% (pk.barang.type,pk.barang.accesoris_barang1 ))
    c.setFont("Courier", 11)
    c.drawString(x, y, "Jenis Pinjaman      : Pinjaman Baru"); y -=1.5*y1
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
    c.drawString(x, y+1.2*inch, "Kepala Gerai,")
    c.drawString(x+6.9*inch, y+1.2*inch, "Debitur,") ; 
    #c.line(410, 488, 500, 488)
    c.drawString(x,y+0.3*inch, "%s"%(pk.gerai.nama_kg))
    c.drawString(x+6.9*inch,y+0.3*inch,"%s"%(pk.agnasabah.nama)) 
    #c.line(550, 488, 650, 488)
    c.setFont("Courier",8)
    c.drawString(x, y, "*Kwitansi ini sah apabila telah di validasi di tanda tangan dan di stample*"); y -=y1
    c.drawString(x, y, " Lembar 2/3 Debitur Copy ")
    #c.drawString(30, 400,"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - " )
    #######Akhir BARU 123
    c.showPage()
    #c.save()


    header1=(4.25 *inch, (5.3 + 5.5) * inch)
    colom1 = (0.5*inch, (4.3 + 5.5) *inch)
            #ke kiri  ke atas ke bawah
    colom2 = (6.7*inch, (4.5 + 5.5) *inch)
    colom3 = (6.0*inch, (4.8 + 4.5) *inch)
    colom4 = (0.5*inch, (3.7 + 4.5) *inch)

    header2=(8.25 *inch, (2.75 + 2.5) * inch)    
    header3=(4.25 *inch, (2.8 + 2.65) * inch)        
    #header2=(4.25 *inch, (5.3 + 5.5) * inch)
    colom5 = (0.5*inch, (2.15 + 2.3) *inch)
            #ke kiri  ke atas ke bawah
    colom6 = (6.7*inch, (2.15 + 2.3) *inch)
    colom7 = (6.0*inch, (2.25 + 1.5) *inch)
    colom8 = (0.5*inch, (1.5 + 1.1) *inch)
    tb=terbilang(pk.terima_bersih_kwitansi)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/logoksu_hitamputih.png'), 1.0*inch, (5.5 + 1.5) * inch, width=200.5/17.5*0.51*inch,height=120/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 0.5*inch, (4.75 + 5.5) * inch, width=30/17.5*0.51*inch,height=25/17.5*0.51*inch,mask=None)
    
    x,y = header1
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Courier-Bold", 16)
    c.drawString(6.2 * inch , y, "KWITANSI"); y -=y1
    c.line( 6.2 * inch , y+0.06* inch , 7.5 * inch ,y+0.06* inch ) ; y -=y1
    c.setFont("Courier-Bold", 16)
    c.drawString(x-2.8*inch, y+0.20*inch, "KSU RIZKY ABADI"); y -=y1
    c.setFont("Courier",8)
    c.drawString(x-2.8*inch, y+0.20*inch, "Badan Hukum No.518/BH.88-DISKOP/THN.2007 Tgl 27 Desember 2007"); y -=y1
    c.drawString(x-2.8*inch, y+0.20*inch, "%s/Telp: 0%s"% (pk.gerai.alamat, pk.gerai.no_telp)); y -=y1
    #c.drawString(x-2.8*inch, y+0.20*inch, "Jln Cisaranten Kulon IV No.55 Bandung Tlp: 022-7808443"); y -=y1
    kb = str.upper(str(pk.gerai.nama_cabang))
    c.setFont("Courier-Bold", 11)
    c.drawString(6.2 * inch , y+0.30*inch,"%s" % (pk.gerai.nama_cabang)); y -=y1      
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
    c.drawString(600, 780, "%s" % sekarang.strftime('[%-b][%Y]') )
    barcode = code128.Code128("%s" % (pk.norek()))
    barcode.drawOn(c, 195*mm, 268*mm)
               
            
    c.setFont("Courier", 11)
    x,y = colom2
    y1 = 0.165 * inch
    c.setFont("Courier", 9)
    c.drawString(x, y, "No PK"); 
    c.drawString(x+1.2*inch, y, ": %s" % (pk.norek())); y -=y1
    c.drawString(x, y, "Tgl Transaksi");
    c.drawString(x+1.2*inch, y, ": %s" % (pk.tanggal.strftime('%d %b %Y'))); y -=y1
    
    c.drawString(x, y, "Tgl Jth tempo");
    c.drawString(x+1.2*inch, y, ": %s" %  (pk.jatuhtempo.strftime('%d %b %Y'))); y -=y1
    c.drawString(x, y, "Jangka waktu") ;
    c.drawString(x+1.2*inch, y, ": %s [Hari]" %  (pk.jangka_waktu)) ; y -=y1
    ####AKHiR KOLOM 2 Dua Coy

    ####KOLOM 3 Tilu Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    c.setFont("Courier-Bold", 14)
               
            
    c.setFont("Courier", 11)
    x,y = colom3
    y1 = 0.165 * inch
    c.setFont("Courier", 9)
    c.drawString(x, y, "Nilai Pinjaman")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.9*inch, y,"%s"% (number_format(pk.nilai))); y -=y1
    c.drawString(x, y, "Bea Simpan/Survey")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"% (number_format(pk.biayasimpan))); y -=y1
    c.drawString(x, y, "Bea Administrasi")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"%(number_format(pk.adm))); y -=y1
    c.drawString(x, y, "Jasa") 
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"%(number_format(pk.jasa_kwitansi()))); y -=y1
    c.drawString(x, y, "Bea Materai")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"% (number_format(pk.bea_materai)))
    c.line( x+1.7*inch , y-0.05*inch , 9.0 * inch , y-0.05*inch ) ; y -=y1

    c.drawString(x, y, "Total Biaya") 
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.9*inch, y,"%s"%(number_format(pk.jumlahbiaya_kwitansi)))
    c.line( x+1.7*inch , y-0.05*inch , 9.0 * inch , y-0.05*inch ) ; y -=y1
    c.setFont("Courier-Bold", 9)
    c.drawString(x, y, "Nilai Diterima")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.9*inch, y," %s"% (number_format(pk.terima_bersih_kwitansi)));y -=y1


    ####AKHiR KOLOM 3 Tilu Coy

    ####KOLOM 1 hiji Coy
    x,y = colom1
    y1 = 0.165 * inch
    
    c.setFont("Courier", 11)
    c.drawString(x, y, "Nomor Debitur : %s" % (pk.nonas())); y -=3*y1
    c.drawString(x, y, "Nama          : %s" % (pk.agnasabah.nama)); y -=y1
    c.drawString(x, y, "Alamat        : %s No %s" %(pk.agnasabah.alamat_domisili,pk.agnasabah.no_rumah_domisili)); y -=y1
    c.drawString(x, y, "                RT/RW %s/%s %s" %(pk.agnasabah.rt_domisili,pk.agnasabah.rw_domisili,pk.agnasabah.kelurahan_domisili,)); y -=y1
    c.drawString(x, y, "No KTP        : %s " %(pk.agnasabah.no_ktp)); y -=y1
    c.drawString(x, y, "No Tlp / HP   : %s / %s " %(pk.agnasabah.telepon_domisili,pk.agnasabah.hp_domisili)); y -=y1
    ####AKHIR KOLOM 1 hiji Coy

    ####KOLOM 4 Opat Coy
    x,y = colom4
    y1 = 0.165 * inch

    c.setFont("Courier", 11)
    c.drawString(x, y+0.1*inch, "Sudah menerima dari KSU RIZKY ABADI," ); y -=y1
    #c.drawString(x, y, "Pembayaran Jaminan  : %s|%s|%s|%s"% (pk.barang.merk,pk.barang.sn,pk.barang.type,pk.barang.accesoris_barang1 )); y -=y1
    c.drawString(x, y+0.1*inch, "Pembayaran Jaminan  :" )
    c.setFont("Courier", 10)
    c.drawString(x+1.9*inch, y+0.1*inch, " %s|%s|%s|"% (pk.barang.merk,pk.barang.sn,pk.barang.warna )); y -=y1
    c.drawString(x+1.9*inch, y+0.15*inch, " %s|%s|"% (pk.barang.type,pk.barang.accesoris_barang1 ))
    c.setFont("Courier", 11)
    c.drawString(x, y, "Jenis Pinjaman      : Pinjaman Baru"); y -=1.5*y1
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
    c.drawString(x, y+1.2*inch, "Kepala Gerai,")
    c.drawString(x+6.9*inch, y+1.2*inch, "Debitur,") ; 
    #c.line(410, 488, 500, 488)
    c.drawString(x,y+0.3*inch, "%s"%(pk.gerai.nama_kg))
    c.drawString(x+6.9*inch,y+0.3*inch,"%s"%(pk.agnasabah.nama)) 
    #c.line(550, 488, 650, 488)
    c.setFont("Courier",8)
    c.drawString(x, y, "*Kwitansi ini sah apabila telah di validasi di tanda tangan dan di stample*"); y -=y1
    c.drawString(x, y, " Lembar 1/3 Pusat, Copy "); y -=y1
    c.drawString(x-2.5 * inch, y," - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - " )

    c.showPage()
    c.save()
    return response

def kwitansi_motor(request, object_id):
    pk = AkadGadai.objects.get(id=object_id)
    pk.status_kw = '1'
    pk.save()
    #tiga_play = [p,p,p]
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % pk.norek()
    c = canvas.Canvas(response, pagesize=(9.5*inch, 11*inch))
    c.setTitle("kwitansi %s" % pk.norek())
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
        trk=pk.tanggal
        dd=patokan.month-trk.month
        yy=patokan.year-trk.year


    header1=(4.25 *inch, (5.3 + 5.5) * inch)
    colom1 = (0.5*inch, (4.3 + 5.5) *inch)
            #ke kiri  ke atas ke bawah
    colom2 = (6.7*inch, (4.5 + 5.5) *inch)
    colom3 = (6.0*inch, (4.8 + 4.5) *inch)
    colom4 = (0.5*inch, (3.7 + 4.5) *inch)

    header2=(8.25 *inch, (2.75 + 2.5) * inch)    
    header3=(4.25 *inch, (2.8 + 2.65) * inch)        
    #header2=(4.25 *inch, (5.3 + 5.5) * inch)
    colom5 = (0.5*inch, (2.15 + 2.3) *inch)
            #ke kiri  ke atas ke bawah
    colom6 = (6.7*inch, (2.15 + 2.3) *inch)
    colom7 = (6.0*inch, (2.25 + 1.5) *inch)
    colom8 = (0.5*inch, (1.5 + 1.1) *inch)
    tb=terbilang(pk.terima_bersih_kendaraan)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/logoksu_hitamputih.png'), 1.0*inch, (5.5 + 1.5) * inch, width=200.5/17.5*0.51*inch,height=120/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 0.5*inch, (4.75 + 5.5) * inch, width=30/17.5*0.51*inch,height=25/17.5*0.51*inch,mask=None)
    
    x,y = header1
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Courier-Bold", 16)
    c.drawString(6.2 * inch , y, "KWITANSI"); y -=y1
    c.line( 6.2 * inch , y+0.06* inch , 7.5 * inch ,y+0.06* inch ) ; y -=y1
    c.setFont("Courier-Bold", 16)
    c.drawString(x-2.8*inch, y+0.20*inch, "KSU RIZKY ABADI"); y -=y1
    c.setFont("Courier",8)
    c.drawString(x-2.8*inch, y+0.20*inch, "Badan Hukum No.518/BH.88-DISKOP/THN.2007 Tgl 27 Desember 2007"); y -=y1
    c.drawString(x-2.8*inch, y+0.20*inch, "%s/Telp: 0%s"% (pk.gerai.alamat, pk.gerai.no_telp)); y -=y1
    #c.drawString(x-2.8*inch, y+0.20*inch, "Jln Cisaranten Kulon IV No.55 Bandung Tlp: 022-7808443"); y -=y1
    kb = str.upper(str(pk.gerai.nama_cabang))
    c.setFont("Courier-Bold", 11)
    c.drawString(6.2 * inch , y+0.30*inch,"%s" % (pk.gerai.nama_cabang)); y -=y1      
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
    c.drawString(600, 780, "%s" % sekarang.strftime('[%-b][%Y]') )
    barcode = code128.Code128("%s" % (pk.norek()))
    barcode.drawOn(c, 195*mm, 268*mm)
               
            
    c.setFont("Courier", 11)
    x,y = colom2
    y1 = 0.165 * inch
    c.setFont("Courier", 9)
    c.drawString(x, y, "No PK"); 
    c.drawString(x+1.2*inch, y, ": %s" % (pk.norek())); y -=y1
    c.drawString(x, y, "Tgl Transaksi");
    c.drawString(x+1.2*inch, y, ": %s" % (pk.tanggal.strftime('%d %b %Y'))); y -=y1
    
    c.drawString(x, y, "Tgl Jth tempo");
    c.drawString(x+1.2*inch, y, ": %s" %  (pk.jatuhtempo.strftime('%d %b %Y'))); y -=y1
    c.drawString(x, y, "Jangka waktu") ;
    c.drawString(x+1.2*inch, y, ": %s [BULAN]" %  (pk.jangka_waktu_kendaraan)) ; y -=y1
    ####AKHiR KOLOM 2 Dua Coy

    ####KOLOM 3 Tilu Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    c.setFont("Courier-Bold", 14)
               
            
    c.setFont("Courier", 11)
    x,y = colom3
    y1 = 0.165 * inch
    c.setFont("Courier", 9)
    c.drawString(x, y, "Nilai Pinjaman")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.9*inch, y,"%s"% (number_format(pk.nilai))); y -=y1
    c.drawString(x, y, "Bea Simpan/Survey")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"% (number_format(pk.beasimpan_kendaraan))); y -=y1
    c.drawString(x, y, "Bea Administrasi")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"%(number_format(pk.adm_kendaraan))); y -=y1
    c.drawString(x, y, "Jasa") 
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"%(number_format(pk.jasa_kwitansi()))); y -=y1
    c.drawString(x, y, "Bea Materai")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"% (number_format(pk.bea_materai)))
    c.line( x+1.7*inch , y-0.05*inch , 9.0 * inch , y-0.05*inch ) ; y -=y1

    c.drawString(x, y, "Total Biaya") 
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.9*inch, y,"%s"%(number_format(pk.jumlahbiaya_kendaraan)))
    c.line( x+1.7*inch , y-0.05*inch , 9.0 * inch , y-0.05*inch ) ; y -=y1
    c.setFont("Courier-Bold", 9)
    c.drawString(x, y, "Nilai Diterima")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.9*inch, y," %s"% (number_format(pk.terima_bersih_kendaraan)));y -=y1


    ####AKHiR KOLOM 3 Tilu Coy

    ####KOLOM 1 hiji Coy
    x,y = colom1
    y1 = 0.165 * inch
    
    c.setFont("Courier", 11)
    c.drawString(x, y, "Nomor Debitur : %s" % (pk.nonas())); y -=3*y1
    c.drawString(x, y, "Nama          : %s" % (pk.agnasabah.nama)); y -=y1
    c.drawString(x, y, "Alamat        : %s No %s" %(pk.agnasabah.alamat_domisili,pk.agnasabah.no_rumah_domisili)); y -=y1
    c.drawString(x, y, "                RT/RW %s/%s %s" %(pk.agnasabah.rt_domisili,pk.agnasabah.rw_domisili,pk.agnasabah.kelurahan_domisili,)); y -=y1
    c.drawString(x, y, "No KTP        : %s " %(pk.agnasabah.no_ktp)); y -=y1
    c.drawString(x, y, "No Tlp / HP   : %s / %s " %(pk.agnasabah.telepon_domisili,pk.agnasabah.hp_domisili)); y -=y1
    ####AKHIR KOLOM 1 hiji Coy

    ####KOLOM 4 Opat Coy
    x,y = colom4
    y1 = 0.165 * inch
    
    c.setFont("Courier", 11)
    c.drawString(x, y, "Sudah menerima dari KSU RIZKY ABADI," ); y -=y1
    c.drawString(x, y, "Pembayaran Jaminan  : %s|%s|%s|"% (pk.barang.get_jenis_kendaraan_display(),pk.barang.get_merk_kendaraan_display() ,pk.barang.type_kendaraan )); y -=y1
    c.drawString(x, y, "Jenis Pinjaman      : Pinjaman Baru"); y -=1.5*y1
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
    c.drawString(x, y+1.2*inch, "Kepala Gerai,")
    c.drawString(x+6.9*inch, y+1.2*inch, "Debitur,") ; 
    #c.line(410, 488, 500, 488)
    c.drawString(x,y+0.3*inch, "%s"%(pk.gerai.nama_kg))
    c.drawString(x+6.9*inch,y+0.3*inch,"%s"%(pk.agnasabah.nama)) 
    #c.line(550, 488, 650, 488)
    c.setFont("Courier",8)
    c.drawString(x, y, "*Kwitansi ini sah apabila telah di validasi di tanda tangan dan di stample*"); y -=y1
    c.drawString(x, y, " Lembar 1/3 Gerai, Asli "); y -=y1
    c.drawString(x-2.5 * inch, y," - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - " )

    #######BARUUUU 123

    tb=terbilang(pk.terima_bersih_kendaraan)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/logoksu_hitamputih.png'), 1.0*inch, (-0.1 + 1.5) * inch, width=200.5/17.5*0.51*inch,height=120/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 0.5*inch, (2.4 + 2.5) * inch, width=30/17.5*0.51*inch,height=25/17.5*0.51*inch,mask=None)

    y -=  2 * y1
    y2 = y + 0.1 * inch
    ## Barcode
    c.setFont("Courier", 7)
    c.drawString(x+7.73 * inch, y+0.2 * inch, "%s" % sekarang.strftime('[%-b][%Y]') )
    barcode = code128.Code128("%s" % (pk.norek()))
    barcode.drawOn(c, 195*mm, 132*mm)
    x,y = header3
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Courier-Bold", 16)
    c.drawString(6.2 * inch , y, "KWITANSI"); y -=y1
    c.line( 6.2 * inch , y+0.06* inch , 7.5 * inch ,y+0.06* inch ) ; y -=y1
    c.setFont("Courier-Bold", 16)
    c.drawString(x-2.8*inch, y+0.20*inch, "KSU RIZKY ABADI"); y -=y1
    c.setFont("Courier",8)
    c.drawString(x-2.8*inch, y+0.20*inch, "Badan Hukum No.518/BH.88-DISKOP/THN.2007 Tgl 27 Desember 2007"); y -=y1
    c.drawString(x-2.8*inch, y+0.20*inch, "%s/Telp: 0%s"% (pk.gerai.alamat, pk.gerai.no_telp)); y -=y1
    #c.drawString(x-2.8*inch, y+0.20*inch, "Jln Cisaranten Kulon IV No.55 Bandung Tlp: 022-7808443"); y -=y1
    kb = str.upper(str(pk.gerai.nama_cabang))
    c.setFont("Courier-Bold", 11)
    c.drawString(6.2 * inch , y+0.30*inch,"%s" % (pk.gerai.nama_cabang)); y -=y1      
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
    c.drawString(600, 780, "%s" % sekarang.strftime('[%-b][%Y]') )
    barcode = code128.Code128("%s" % (pk.norek()))
    barcode.drawOn(c, 195*mm, 268*mm)
               
            
    c.setFont("Courier", 11)
    x,y = colom6
    y1 = 0.165 * inch
    c.setFont("Courier", 9)
    c.drawString(x, y, "No PK"); 
    c.drawString(x+1.2*inch, y, ": %s" % (pk.norek())); y -=y1
    c.drawString(x, y, "Tgl Transaksi");
    c.drawString(x+1.2*inch, y, ": %s" % (pk.tanggal.strftime('%d %b %Y'))); y -=y1
    
    c.drawString(x, y, "Tgl Jth tempo");
    c.drawString(x+1.2*inch, y, ": %s" %  (pk.jatuhtempo.strftime('%d %b %Y'))); y -=y1
    c.drawString(x, y, "Jangka waktu") ;
    c.drawString(x+1.2*inch, y, ": %s [BULAN]" %  (pk.jangka_waktu_kendaraan)) ; y -=y1
    ####AKHiR KOLOM 2 Dua Coy

    ####KOLOM 3 Tilu Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    c.setFont("Courier-Bold", 14)
               
            
    c.setFont("Courier", 11)
    x,y = colom7
    y1 = 0.165 * inch
    c.setFont("Courier", 9)
    c.drawString(x, y, "Nilai Pinjaman")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.9*inch, y,"%s"% (number_format(pk.nilai))); y -=y1
    c.drawString(x, y, "Bea Simpan/Survey")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"% (number_format(pk.beasimpan_kendaraan))); y -=y1
    c.drawString(x, y, "Bea Administrasi")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"%(number_format(pk.adm_kendaraan))); y -=y1
    c.drawString(x, y, "Jasa") 
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"%(number_format(pk.jasa_kwitansi()))); y -=y1
    c.drawString(x, y, "Bea Materai")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"% (number_format(pk.bea_materai)))
    c.line( x+1.7*inch , y-0.05*inch , 9.0 * inch , y-0.05*inch ) ; y -=y1

    c.drawString(x, y, "Total Biaya") 
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.9*inch, y,"%s"%(number_format(pk.jumlahbiaya_kendaraan)))
    c.line( x+1.7*inch , y-0.05*inch , 9.0 * inch , y-0.05*inch ) ; y -=y1
    c.setFont("Courier-Bold", 9)
    c.drawString(x, y, "Nilai Diterima")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.9*inch, y," %s"% (number_format(pk.terima_bersih_kendaraan)));y -=y1


    ####AKHiR KOLOM 3 Tilu Coy

    ####KOLOM 1 hiji Coy
    x,y = colom5
    y1 = 0.165 * inch
    
    c.setFont("Courier", 11)
    c.drawString(x, y, "Nomor Debitur : %s" % (pk.nonas())); y -=3*y1
    c.drawString(x, y, "Nama          : %s" % (pk.agnasabah.nama)); y -=y1
    c.drawString(x, y, "Alamat        : %s No %s" %(pk.agnasabah.alamat_domisili,pk.agnasabah.no_rumah_domisili)); y -=y1
    c.drawString(x, y, "                RT/RW %s/%s %s" %(pk.agnasabah.rt_domisili,pk.agnasabah.rw_domisili,pk.agnasabah.kelurahan_domisili,)); y -=y1
    c.drawString(x, y, "No KTP        : %s " %(pk.agnasabah.no_ktp)); y -=y1
    c.drawString(x, y, "No Tlp / HP   : %s / %s " %(pk.agnasabah.telepon_domisili,pk.agnasabah.hp_domisili)); y -=y1
    ####AKHIR KOLOM 1 hiji Coy

    ####KOLOM 4 Opat Coy
    x,y = colom8
    y1 = 0.165 * inch
    
    c.setFont("Courier", 11)
    c.drawString(x, y, "Sudah menerima dari KSU RIZKY ABADI," ); y -=y1
    c.drawString(x, y, "Pembayaran Jaminan  : %s|%s|%s|"% (pk.barang.get_jenis_kendaraan_display(),pk.barang.get_merk_kendaraan_display() ,pk.barang.type_kendaraan )); y -=y1
    c.drawString(x, y, "Jenis Pinjaman      : Pinjaman Baru"); y -=1.5*y1
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
    c.drawString(x, y+1.2*inch, "Kepala Gerai,")
    c.drawString(x+6.9*inch, y+1.2*inch, "Debitur,") ; 
    #c.line(410, 488, 500, 488)
    c.drawString(x,y+0.3*inch, "%s"%(pk.gerai.nama_kg))
    c.drawString(x+6.9*inch,y+0.3*inch,"%s"%(pk.agnasabah.nama)) 
    #c.line(550, 488, 650, 488)
    c.setFont("Courier",8)
    c.drawString(x, y, "*Kwitansi ini sah apabila telah di validasi di tanda tangan dan di stample*"); y -=y1
    c.drawString(x, y, " Lembar 2/3 Debitur Copy ")
    #c.drawString(30, 400,"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - " )
    #######Akhir BARU 123
    c.showPage()
    #c.save()
    header1=(4.25 *inch, (5.3 + 5.5) * inch)
    colom1 = (0.5*inch, (4.3 + 5.5) *inch)
            #ke kiri  ke atas ke bawah
    colom2 = (6.7*inch, (4.5 + 5.5) *inch)
    colom3 = (6.0*inch, (4.8 + 4.5) *inch)
    colom4 = (0.5*inch, (3.7 + 4.5) *inch)

    header2=(8.25 *inch, (2.75 + 2.5) * inch)    
    header3=(4.25 *inch, (2.8 + 2.65) * inch)        
    #header2=(4.25 *inch, (5.3 + 5.5) * inch)
    colom5 = (0.5*inch, (2.15 + 2.3) *inch)
            #ke kiri  ke atas ke bawah
    colom6 = (6.7*inch, (2.15 + 2.3) *inch)
    colom7 = (6.0*inch, (2.25 + 1.5) *inch)
    colom8 = (0.5*inch, (1.5 + 1.1) *inch)
    tb=terbilang(pk.terima_bersih_kendaraan)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/logoksu_hitamputih.png'), 1.0*inch, (5.5 + 1.5) * inch, width=200.5/17.5*0.51*inch,height=120/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 0.5*inch, (4.75 + 5.5) * inch, width=30/17.5*0.51*inch,height=25/17.5*0.51*inch,mask=None)
    
    x,y = header1
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Courier-Bold", 16)
    c.drawString(6.2 * inch , y, "KWITANSI"); y -=y1
    c.line( 6.2 * inch , y+0.06* inch , 7.5 * inch ,y+0.06* inch ) ; y -=y1
    c.setFont("Courier-Bold", 16)
    c.drawString(x-2.8*inch, y+0.20*inch, "KSU RIZKY ABADI"); y -=y1
    c.setFont("Courier",8)
    c.drawString(x-2.8*inch, y+0.20*inch, "Badan Hukum No.518/BH.88-DISKOP/THN.2007 Tgl 27 Desember 2007"); y -=y1
    c.drawString(x-2.8*inch, y+0.20*inch, "%s/Telp: 0%s"% (pk.gerai.alamat, pk.gerai.no_telp)); y -=y1
    #c.drawString(x-2.8*inch, y+0.20*inch, "Jln Cisaranten Kulon IV No.55 Bandung Tlp: 022-7808443"); y -=y1
    kb = str.upper(str(pk.gerai.nama_cabang))
    c.setFont("Courier-Bold", 11)
    c.drawString(6.2 * inch , y+0.30*inch,"%s" % (pk.gerai.nama_cabang)); y -=y1      
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
    c.drawString(600, 780, "%s" % sekarang.strftime('[%-b][%Y]') )
    barcode = code128.Code128("%s" % (pk.norek()))
    barcode.drawOn(c, 195*mm, 268*mm)
               
            
    c.setFont("Courier", 11)
    x,y = colom2
    y1 = 0.165 * inch
    c.setFont("Courier", 9)
    c.drawString(x, y, "No PK"); 
    c.drawString(x+1.2*inch, y, ": %s" % (pk.norek())); y -=y1
    c.drawString(x, y, "Tgl Transaksi");
    c.drawString(x+1.2*inch, y, ": %s" % (pk.tanggal.strftime('%d %b %Y'))); y -=y1
    
    c.drawString(x, y, "Tgl Jth tempo");
    c.drawString(x+1.2*inch, y, ": %s" %  (pk.jatuhtempo.strftime('%d %b %Y'))); y -=y1
    c.drawString(x, y, "Jangka waktu") ;
    c.drawString(x+1.2*inch, y, ": %s [BULAN]" %  (pk.jangka_waktu_kendaraan)) ; y -=y1
    ####AKHiR KOLOM 2 Dua Coy

    ####KOLOM 3 Tilu Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    c.setFont("Courier-Bold", 14)
               
            
    c.setFont("Courier", 11)
    x,y = colom3
    y1 = 0.165 * inch
    c.setFont("Courier", 9)
    c.drawString(x, y, "Nilai Pinjaman")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.9*inch, y,"%s"% (number_format(pk.nilai))); y -=y1
    c.drawString(x, y, "Bea Simpan/Survey")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"% (number_format(pk.beasimpan_kendaraan))); y -=y1
    c.drawString(x, y, "Bea Administrasi")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"%(number_format(pk.adm_kendaraan))); y -=y1
    c.drawString(x, y, "Jasa") 
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"%(number_format(pk.jasa_kwitansi()))); y -=y1
    c.drawString(x, y, "Bea Materai")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.5*inch, y,"%s"% (number_format(pk.bea_materai)))
    c.line( x+1.7*inch , y-0.05*inch , 9.0 * inch , y-0.05*inch ) ; y -=y1

    c.drawString(x, y, "Total Biaya") 
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.9*inch, y,"%s"%(number_format(pk.jumlahbiaya_kendaraan)))
    c.line( x+1.7*inch , y-0.05*inch , 9.0 * inch , y-0.05*inch ) ; y -=y1
    c.setFont("Courier-Bold", 9)
    c.drawString(x, y, "Nilai Diterima")
    c.drawString(x+1.3*inch, y,":Rp.")
    c.drawRightString(x+2.9*inch, y," %s"% (number_format(pk.terima_bersih_kendaraan)));y -=y1


    ####AKHiR KOLOM 3 Tilu Coy

    ####KOLOM 1 hiji Coy
    x,y = colom1
    y1 = 0.165 * inch
    
    c.setFont("Courier", 11)
    c.drawString(x, y, "Nomor Debitur : %s" % (pk.nonas())); y -=3*y1
    c.drawString(x, y, "Nama          : %s" % (pk.agnasabah.nama)); y -=y1
    c.drawString(x, y, "Alamat        : %s No %s" %(pk.agnasabah.alamat_domisili,pk.agnasabah.no_rumah_domisili)); y -=y1
    c.drawString(x, y, "                RT/RW %s/%s %s" %(pk.agnasabah.rt_domisili,pk.agnasabah.rw_domisili,pk.agnasabah.kelurahan_domisili,)); y -=y1
    c.drawString(x, y, "No KTP        : %s " %(pk.agnasabah.no_ktp)); y -=y1
    c.drawString(x, y, "No Tlp / HP   : %s / %s " %(pk.agnasabah.telepon_domisili,pk.agnasabah.hp_domisili)); y -=y1
    ####AKHIR KOLOM 1 hiji Coy

    ####KOLOM 4 Opat Coy
    x,y = colom4
    y1 = 0.165 * inch
    
    c.setFont("Courier", 11)
    c.drawString(x, y, "Sudah menerima dari KSU RIZKY ABADI," ); y -=y1
    c.drawString(x, y, "Pembayaran Jaminan  : %s|%s|%s|"% (pk.barang.get_jenis_kendaraan_display(),pk.barang.get_merk_kendaraan_display() ,pk.barang.type_kendaraan )); y -=y1
    c.drawString(x, y, "Jenis Pinjaman      : Pinjaman Baru"); y -=1.5*y1
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
    c.drawString(x, y+1.2*inch, "Kepala Gerai,")
    c.drawString(x+6.9*inch, y+1.2*inch, "Debitur,") ; 
    #c.line(410, 488, 500, 488)
    c.drawString(x,y+0.3*inch, "%s"%(pk.gerai.nama_kg))
    c.drawString(x+6.9*inch,y+0.3*inch,"%s"%(pk.agnasabah.nama)) 
    #c.line(550, 488, 650, 488)
    c.setFont("Courier",8)
    c.drawString(x, y, "*Kwitansi ini sah apabila telah di validasi di tanda tangan dan di stample*"); y -=y1
    c.drawString(x, y, " Lembar 1/3 Pusat, Copy "); y -=y1
    c.drawString(x-2.5 * inch, y," - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - " )

    c.showPage()
    c.save()
    return response
'''
def skl(request, object_id):
    sekarang=datetime.datetime.now()
    akad = AkadGadai.objects.get(id=object_id)
    akad.sts_tdr = '1'
    akad.save()
    tb=terbilang(akad.nilai)
    tb_total=terbilang(akad.jumlah_biaya_pk())
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= "SKL %s_%s.pdf"' % (akad.norek(),akad.agnasabah.nama)
    h=sekarang.day
    m=sekarang.month
    y=sekarang.year
    buffer = BytesIO()
    
    p = canvas.Canvas(buffer)
    #p.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/kopri.png'), 0.4*inch, (5.2 + 5.7) * inch, width=33.5/17.5*0.51*inch,height=26/17.5*0.51*inch)
    p.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ra2.png'), 0.4*inch, (5.25 + 5.7) * inch, width=35.5/17.5*0.51*inch,height=24/17.5*0.51*inch)
    p.setFont("Helvetica-Bold",10)
    p.drawCentredString(300, 810, "SURAT KETERANGAN LUNAS")
    p.drawCentredString(300, 795, "No.__/PJB/SKL/%s" % sekarang.strftime('%b/%Y') )
    p.line(  15 , 789, 580 ,789  ) 
    p.setLineWidth(.3)
    p.line(  15 , 787, 580 ,787  )
    #p.line(580, 800, 580, 10)
    #line batas
    p.setFont('Helvetica', 9)
    p.drawString(20,777,"Yang bertandatangan dibawah ini :")
    p.drawString(30,767,"Nama")
    p.setFont("Helvetica-Bold",9)
    p.drawString(145,767,": %s"%(akad.gerai.nama_kg))
    p.setFont("Helvetica",10)    
    p.drawString(30,752,"Jabatan")
    p.drawString(145,752,": Kepala Gerai %s KSU RIZKY ABADI"%(akad.gerai.nama_cabang))
    p.drawString(20,739,"selanjutnya disebut Pihak Pertama / Koperasi")
    p.drawString(20,727,"Sehubungan dengan telah dilunasi pinjaman sbb:")
  
    p.setFont('Helvetica', 9)
    p.drawString(30,716,"No. Rekening")
    p.setFont('Helvetica-Bold', 9)
    p.drawString(145,716,": %s"%(akad.norek()))
    p.setFont('Helvetica', 9)
    p.drawString(30,703,"Nama")
    p.setFont('Helvetica-Bold', 9)
    p.drawString(145,703,": %s "% (akad.agnasabah.nama))
    p.setFont('Helvetica', 9)
    p.drawString(30,690,"Alamat")
    p.setFont('Helvetica-Bold', 9)
    p.drawString(145,690,": %s No %s Rt %s/%s Kelurahan %s Kecamatan %s "%(akad.agnasabah.alamat_ktp,akad.agnasabah.no_rumah_ktp,akad.agnasabah.rt_ktp, akad.agnasabah.rw_ktp,akad.agnasabah.kelurahan_ktp, akad.agnasabah.kelurahan_ktp))
    p.setFont('Helvetica', 9)
    p.drawString(30,677,"Nomor KTP/SIM")
    p.setFont('Helvetica-Bold', 9)
    p.drawString(145,677,": %s"%(akad.agnasabah.no_ktp))
    
    p.setFont('Helvetica', 9)
    p.drawString(20,662,"selanjutnya dalam perjanjian ini disebut Pihak Kedua / Penerima Kredit")
    p.setFont('Helvetica', 9)
    p.drawString(20,652,"Maka bersama ini, pihak pertama menerangkan bahwa pinjaman atas nama pihak kedua di KSU RIZKY ABADI telah")
    p.setFont('Helvetica-Bold', 9)    
    p.drawString(488,652,"lunas")
    p.setFont('Helvetica', 9)
    p.drawString(20,637,"Dan dengan ini pihak kedua menyatakan telah menerima dengan lengkap dai pihak pertama, agunan barang berupa")
    p.setFont('Helvetica-Bold', 9)
    p.drawString(20,620, ":%s|%s|%s|%s"% (akad.barang.merk,akad.barang.sn,akad.barang.type,akad.barang.accesoris_barang1, ))
    
    p.setFont('Helvetica', 9)
    p.drawString(30, 600, "Bandung, %s" % sekarang.strftime('%d %b %Y') )
    p.drawString(30, 588, "Pihak Pertama,")
    p.drawString(30, 540, "( .......................................... )")
    p.drawString(430, 588, "Pihak Kedua,")
    p.drawString(430, 540, "( .......................................... )")
    

 
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
'''
def skl(request, object_id):
    sekarang=datetime.datetime.now()
    akad = AkadGadai.objects.get(id=object_id)
    akad.sts_tdr =1
    akad.save()
    tb=terbilang(akad.nilai)
    tb_total=terbilang(akad.jumlah_biaya_pk())
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= "SKL %s_%s.pdf"' % (akad.norek(),akad.agnasabah.nama)
    h=sekarang.day
    m=sekarang.month
    y=sekarang.year
    buffer = BytesIO()
    
    p = canvas.Canvas(buffer)
    #p.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/kopri.png'), 0.4*inch, (5.2 + 5.7) * inch, width=33.5/17.5*0.51*inch,height=26/17.5*0.51*inch)
    p.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ra2.png'), 0.4*inch, (5.25 + 5.7) * inch, width=35.5/17.5*0.51*inch,height=24/17.5*0.51*inch)
    p.setFont("Helvetica-Bold",10)
    p.drawCentredString(300, 810, "SURAT KETERANGAN LUNAS")
    p.drawCentredString(300, 795, "No.__/PJB/SKL/%s" % sekarang.strftime('%b/%Y') )
    p.line(  15 , 789, 580 ,789  ) 
    p.setLineWidth(.3)
    p.line(  15 , 787, 580 ,787  )
    #p.line(580, 800, 580, 10)
    #line batas
    p.setFont('Helvetica', 9)
    p.drawString(20,777,"Yang bertandatangan dibawah ini :")
    p.drawString(30,767,"Nama")
    p.setFont("Helvetica-Bold",9)
    p.drawString(145,767,": %s"%(akad.gerai.nama_kg))
    p.setFont("Helvetica",10)    
    p.drawString(30,752,"Jabatan")
    p.drawString(145,752,": Kepala Gerai %s KSU RIZKY ABADI"%(akad.gerai.nama_cabang))
    p.drawString(20,739,"selanjutnya disebut Pihak Pertama / Koperasi")
    p.drawString(20,727,"Sehubungan dengan telah dilunasi pinjaman sbb:")
  
    p.setFont('Helvetica', 9)
    p.drawString(30,716,"No. Rekening")
    p.setFont('Helvetica-Bold', 9)
    p.drawString(145,716,": %s"%(akad.norek()))
    p.setFont('Helvetica', 9)
    p.drawString(30,703,"Nama")
    p.setFont('Helvetica-Bold', 9)
    p.drawString(145,703,": %s "% (akad.agnasabah.nama))
    p.setFont('Helvetica', 9)
    p.drawString(30,690,"Alamat")
    p.setFont('Helvetica-Bold', 9)
    p.drawString(145,690,": %s No %s Rt %s/%s"%(akad.agnasabah.alamat_ktp,akad.agnasabah.no_rumah_ktp,akad.agnasabah.rt_ktp, akad.agnasabah.rw_ktp))
    p.drawString(145,678,"  Kelurahan %s Kecamatan %s "%(akad.agnasabah.kelurahan_ktp, akad.agnasabah.kelurahan_ktp))
    p.setFont('Helvetica', 9)
    p.drawString(30,666,"Nomor KTP/SIM")
    p.setFont('Helvetica-Bold', 9)
    p.drawString(145,666,": %s"%(akad.agnasabah.no_ktp))
    
    p.setFont('Helvetica', 9)
    p.drawString(20,654,"selanjutnya dalam perjanjian ini disebut Pihak Kedua / Penerima Kredit")
    p.setFont('Helvetica', 9)
    p.drawString(20,642,"Maka bersama ini, pihak pertama menerangkan bahwa pinjaman atas nama pihak kedua di KSU RIZKY ABADI telah")
    p.setFont('Helvetica-Bold', 9)    
    p.drawString(488,642,"lunas")
    p.setFont('Helvetica', 9)
    p.drawString(20,630,"Dan dengan ini pihak kedua menyatakan telah menerima dengan lengkap dai pihak pertama, agunan barang berupa :")
    p.setFont('Helvetica-Bold', 9)
    p.drawString(20,618, "%s|%s|%s"% (akad.barang.merk,akad.barang.sn,akad.barang.type ))

    
    p.setFont('Helvetica', 9)
    p.drawString(30, 600, "Bandung, %s" % sekarang.strftime('%d %b %Y') )
    p.drawString(30, 588, "Pihak Pertama,")
    p.drawString(30,540, "( %s )"% (akad.gerai.nama_kg))

    p.drawString(430, 588, "Pihak Kedua,")
    p.drawString(430,540, "( %s )"% (akad.agnasabah.nama))
    
    

 
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def kwitansi_gu(request, object_id):
    akadgadai = AkadGadai.objects.get(id=object_id)
    akadgadai.status_kw = '1'
    akadgadai.save()

    sekarang=datetime.datetime.now()
    jumlah = akadgadai.nilai_gu + akadgadai.denda_gu + akadgadai.jasa_gu
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


        trk=akadgadai.tanggal
        dd=patokan.month-trk.month
        yy=patokan.year-trk.year

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= "kuitansi_%s.pdf"' % akadgadai.norek()
    
    c = canvas.Canvas(response, pagesize=(9.5*inch, 11*inch))

    header0=(8.25 *inch, (5.2 + 5.5) * inch)
    header1=(4.60 *inch, (5.35 + 5.5) * inch)
    colom1 = (0.3*inch, (4.35 + 5.5) *inch)
    colom2 = (6.3*inch, (4.35 + 5.5) *inch)
    colom3 = (6.3*inch, (4.35 + 4.5) *inch)
    #c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ra2.png'), 0.5*inch, (4.8 + 5.5) * inch, width=28.5/17.5*0.51*inch,height=24/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/logoksu_hitamputih.png'), 1.0*inch, (5.5 + 1.5) * inch, width=200.5/17.5*0.51*inch,height=120/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ra2.png'), 0.5*inch, (4.8 + 5.5) * inch, width=28.5/17.5*0.51*inch,height=24/17.5*0.51*inch)

    c.setFont("Courier", 7)
    c.drawString(600, 780, "%s" % sekarang.strftime('[%-b][%Y]') )
    barcode = code128.Code128("%s" % (akadgadai.norek()))
    barcode.drawOn(c, 195*mm, 268*mm)

    c.setFont("Courier-Bold", 14)
    c.drawString(100, 780, "KSU RIZKY ABADI" )
    c.setFont("Courier", 8)
    c.drawString(100, 770, "Badan Hukum No.518/BH.88-Diskop/THN.2007 Tgl. 27 Desember 2007")
    c.drawString(100, 760, "%s/Telp: 0%s "% (akadgadai.gerai.alamat, akadgadai.gerai.no_telp))
    c.setFont("Courier-Bold", 12)
    c.drawCentredString(485, 775, "KWITANSI GADAI ULANG")
    c.line( 410 , 773, 560 ,773  ) 
    c.setFont("Courier-Bold", 10)
    c.drawCentredString(485, 763, "GERAI [%s]"% (akadgadai.gerai.nama_cabang))
    #c.setFont("Courier-Bold", 16)
    #c.drawCentredString(340, 775, "KWITANSI GADAI ULANG")
    #c.line( 235 , 773, 450 ,773  ) 
    #c.setFont("Courier-Bold", 12)
    #c.drawCentredString(340, 763, "GERAI [%s]"% (akadgadai.gerai.nama_cabang))
    c.setFont("Courier-Bold", 12)



    tb=terbilang(akadgadai.terima_bersih)
    c.setFont("Courier",8)
    c.drawString(430, 750, "Nomor Kwitansi     : %s" % (akadgadai.nonas()))
    c.drawString(430, 740, "Tanggal Transaksi  : %s" % akadgadai.tanggal.strftime('%d %b %Y'))
    c.drawString(430, 730, "Tanggal Jt tempo   : %s" % akadgadai.jatuhtempo.strftime('%d %b %Y'))
    if akadgadai.jenis_transaksi == u'1': ###('1','Elektronik')
        c.drawString(430, 720, "Jangka waktu       : %s [ Hari ]" % akadgadai.jangka_waktu)
    elif akadgadai.jenis_transaksi != u'1': ###('1','KENDARAAN')
        c.drawString(430, 720, "Jangka waktu       : %s [ Bulan ]" % akadgadai.jangka_waktu_kendaraan)
  
    #c.drawString(100, 742, "Validasi :")
    c.setFont("Courier",7)
    c.drawString(40, 725, "%s" % (akadgadai.kw_validasi()))
    c.setFont("Courier",8)
    # garis Paling atas
    c.line(35, 740, 400, 740)
    #garis Paling Bawah
    c.line(35, 720, 400, 720)
    #garis paling kiri
    c.line(35, 740, 35, 720)
    #garis paling kanan
    c.line(400, 740, 400, 720)
    c.setLineWidth(.3)    
    c.line(500, 715, 500, 620)

    c.drawString(345, 710,"Pinjaman lama")
    c.drawString(414, 710,":Rp.")
    c.drawRightString(495, 710,"%s"% (number_format(akadgadai.nilai_gu)))

    c.drawString(345, 690, "Denda")
    c.drawString(414, 690, ":Rp.")
    c.drawRightString(495, 690, "%s"% (number_format(akadgadai.denda_gu)))
    c.drawString(345, 680, "Jasa Terlambat")
    c.drawString(414, 680,":Rp.")
    c.drawRightString(495, 680, "%s"% (number_format(akadgadai.jasa_gu)))
    c.line(414, 658, 495, 658)
    c.drawString(345, 650, "T. Biaya Plns")
    c.drawString(414, 650, ":Rp.")
    c.drawRightString(495, 650, "%s"%(number_format(jumlah)))
    c.line(414, 640, 495, 640)
    c.drawString(345, 630, "Plns Pinj Lama")
    c.drawString(414, 630, ":Rp.")
    c.drawRightString(495, 630, "%s"%(number_format(akadgadai.total_plns_gu)))
    c.line(414, 627, 495, 627)
    c.line(414, 624, 495, 624)

    c.drawString(502, 710,"Pinjaman Baru")
    c.drawString(575, 710,":Rp.")
    c.drawRightString(660, 710,"%s"% (number_format(akadgadai.nilai)))
    c.drawString(502, 690, "Bea Simpan/Survey:Rp.")
    c.drawRightString(660, 690, "%s"% (number_format(akadgadai.beasimpan_all())))
    c.drawString(502, 680, "Bea Administrasi :Rp.")
    c.drawRightString(660, 680, "%s"% (number_format(akadgadai.adm_all())))
    c.drawString(502, 670, "Jasa             :Rp.")
    c.drawRightString(660, 670, "%s"% (number_format(akadgadai.jasa_kwitansi())))
    c.drawString(502, 660, "Bea Materai      :Rp.")
    #c.drawRightString(610, 660, "0.0")
    c.drawRightString(660, 660, "%s"% (number_format(akadgadai.bea_materai)))
    c.setLineWidth(.3)
    c.line(580, 658, 660, 658)
    c.drawString(502, 650, "Total Biaya 1")
    c.drawString(575, 650, ":Rp.")
    c.drawRightString(660, 650, "%s"%(number_format(akadgadai.jumlah_biaya_pk())))
    c.line(580, 640, 660, 640)
    c.drawString(502, 630, "Nilai diterima")
    c.drawString(575, 630, ":Rp.")
    c.drawRightString(660, 630, "%s"%(number_format(akadgadai.terima_bersih_kwitansi)))
    c.line(580, 627, 660, 627)
    c.line(580, 624, 660, 624)


    c.drawString(35,710, "Nomor Pencairan Debitur")
    c.drawString(150,710, ":%s" % akadgadai.norek())
    c.drawString(35,700, "Nomor Pelunasan Debitur")
    c.drawString(150,700, ":%s" % (akadgadai.norek_lunas_sblm))
    c.line(150, 708, 250, 708)
    c.line(150, 698, 250, 698)
    #c.drawString(35,700, "Nomor Pinjaman")
    #c.drawString(130,700, ":%s" % (akadgadai.nonas()))
    #c.line(135, 698, 240, 698)
    c.drawString(35,680, "Nama")
    c.drawString(130,680, ":%s" %(akadgadai.agnasabah.nama))
    c.line(135, 678, 340, 678)
    c.drawString(35,670, "Alamat")
    c.setFont("Courier",11)
    c.drawString(130,670, ":%s No %s" %(akadgadai.agnasabah.alamat_domisili,akadgadai.agnasabah.no_rumah_domisili))
    c.line(135, 668, 340, 668)
    c.drawString(137,660, "RT/RW %s/%s %s" %(akadgadai.agnasabah.rt_domisili,akadgadai.agnasabah.rw_domisili,akadgadai.agnasabah.kelurahan_domisili,))
    c.line(135, 658, 340, 658)
    c.setFont("Courier",11)
    c.drawString(35,650, "No Ktp")
    c.drawString(130,650, ":%s " %(akadgadai.agnasabah.no_ktp))
    c.line(135, 648, 340, 648)
    c.drawString(35,640, "No Telp /HP")
    c.drawString(130,640,":%s / %s " %(akadgadai.agnasabah.telepon_domisili,akadgadai.agnasabah.hp_domisili))
    c.line(135, 638, 340, 638)
    c.drawString(35,620, "Sudah menerima dari KSU RIZKY ABADI,")
    c.drawString(35,610, "Pembayaran Jaminan")
    c.setFont("Courier", 10)
    c.drawString(160,610, ":%s|%s|%s|%s"% (akadgadai.barang.merk,akadgadai.barang.sn,akadgadai.barang.type,akadgadai.barang.accesoris_barang1, ))
    c.setFont("Courier", 11)
    c.line(165, 608, 525, 608)
    c.drawString(35,600, "Jenis Pinjaman")
    c.drawString(160,600, ": Gadai Ulang")
    c.line(165, 598, 340, 598)
    c.setFont("Courier-Bold", 11)
    c.setLineWidth(.9)
    c.drawString(35,585,  " ##%s Rupiah ##"  % tb.title())
    # garis Paling atas
    c.line(35, 595, 650, 595)
    #garis Paling Bawah
    c.line(35, 580, 650, 580)
    #garis paling kiri
    c.line(35, 595, 35, 580)
    #garis paling kanan
    c.line(650, 595, 650, 580)
   
    c.setFont("Courier-Bold", 10)
    c.drawString(35, 570, "PERHATIAN :")
    c.setFont("Courier", 8)
    c.drawString(35, 560, "1. Apabila sampai dengan tanggal jatuh tempo tidak melakukan pelunasan")
    c.drawString(50, 550,"atau tidak gadai ulang maka Koperasi berhak Menjual barang  jaminan")
    c.drawString(50, 540,"tersebut diatas")
    c.drawString(35, 530, "2. Apabila  akan  melakukan  gadai ulang")
    c.setFont("Courier-Bold", 8)
    c.drawString(230, 530, "harap menginformasikan 1 hari")
    c.drawString(50, 520, "sebelum jatuh tempo")
    c.setFont("Courier", 8)
    c.drawString(35, 510, "3. Setiap melakukan Pelunasan atau gadai ulang, kwitansi ini harus")
    c.drawString(50, 500, "diperlihatkan kepada petugas gerai")
    c.drawString(35, 490, "4. Pelunasan atau gadai ulang")
    c.setFont("Courier-Bold", 8)
    c.drawString(180, 490, "harus dilakukan tepat waktu sesuai tanggal")
    c.drawString(50, 480, "jatuh tempo")
    c.setFont("Courier", 8)
    c.drawString(35, 470, "5. Kwitansi ini sah apabila telah di validasi di tanda tangan dan di stample")
    c.setFont("Courier-Bold", 11)
    c.drawString(35, 450, "Badan Hukum No.518/BH.88-Diskop/THN.2007 Tgl. 27 Desember 2007")

    c.setFont("Courier",11)
    c.drawString(410, 560, "Kepala Gerai,")
    c.drawString(410, 490, "%s"%(akadgadai.gerai.nama_kg))
    c.line(410, 488, 500, 488)
    c.drawRightString(650, 570, "Bandung, %s" % sekarang.strftime('%d %b %Y') )
    c.drawRightString(650, 560, "Debitur,") #568
    c.drawRightString(650, 490, "%s"%(akadgadai.agnasabah.nama)) #570
    c.line(550, 488, 650, 488)
    c.showPage()
    c.save()
    return response
