from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django import forms
import datetime, os
import csv
from django.db.models import Sum, Count
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import *
from gadai.appgadai.templatetags.number_format import number_format
from gadai.appgadai.templatetags.terbilang import terbilang
from gadai.appgadai.pelunasan.forms import *
from gadai.appgadai.models import *
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm

def kw_sbg_plns(request, object_id):
    pk = KasirGeraiPelunasan.objects.get(kasir_lunas__id=object_id)
    pk.kasir_lunas.status_kwlunas = '1'
    pk.save()

    #tiga_play = [p,p,p]
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s.pdf' % pk.kasir_lunas.norek()
    c = canvas.Canvas(response, pagesize=(9.5*inch, 13*inch))
    c.setTitle("kwitansi %s" % pk.kasir_lunas.norek())
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
    tb=terbilang(pk.nilai_pembulatan_lunas)
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
    c.drawString(270, 910, "%s"% (pk.kasir_lunas.gerai.nama_cabang))
    c.setFont("Courier-Bold", 9)
    c.drawString(270, 900, "%s/Telp: 0%s "% (pk.kasir_lunas.gerai.alamat, pk.kasir_lunas.gerai.no_telp))

    c.setFont("Courier", 7)
    barcode = code128.Code128("%s" % (pk.kasir_lunas.norek()))
    barcode.drawOn(c, 185*mm, 304.5*mm)
    c.setFont("Courier-Bold", 9) 
    c.drawString(540, 848, "Tanggal Jatuh Tempo") 
    c.drawString(540, 825, "%s" % (pk.kasir_lunas.jatuhtempo.strftime('%d %b %Y')))
    c.drawString(540, 810, "Tanggal Pelunasan") 
    c.drawString(540, 790, "%s" % (pk.tanggal.strftime('%d %b %Y')))
   
    c.setFont("Courier-Bold", 12)  
    c.drawString(19, 868, "SURAT BUKTI GADAI PELUNASAN")
    c.setFont("Courier-Bold", 14)  
    c.drawString(220, 868, "NO NASABAH: %s"% (pk.kasir_lunas.nonas()))
    c.setFont("Courier", 9)
    c.drawString(20, 848, "Nomor Rek")
    c.drawString(100, 848, ": %s" % (pk.kasir_lunas.norek()))
    c.drawString(20, 838, "Nama")
    c.drawString(100, 838, ": %s" % (pk.kasir_lunas.agnasabah.nama))
    c.drawString(20, 828, "No Identitas")
    c.drawString(100, 828, ": %s" % (pk.kasir_lunas.agnasabah.no_ktp))
    c.drawString(20, 818, "No Telepon")
    c.drawString(100, 818, ": %s" % (pk.kasir_lunas.agnasabah.telepon_domisili,))
    c.drawString(20, 808, "Alamat")
    c.drawString(100, 808, ": %s No %s" %(pk.kasir_lunas.agnasabah.alamat_domisili,pk.kasir_lunas.agnasabah.no_rumah_domisili))
    c.drawString(100.5, 798, "  RT/RW %s/%s %s" %(pk.kasir_lunas.agnasabah.rt_domisili,pk.kasir_lunas.agnasabah.rw_domisili,pk.kasir_lunas.agnasabah.kelurahan_domisili,))
    c.drawString(20, 788, "Tempat,Tgl Lhr")
    c.drawString(100, 788, ": %s, %s" %(pk.kasir_lunas.agnasabah.tempat,pk.kasir_lunas.agnasabah.tgl_lahir.strftime('%d %B %Y')))
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
    c.drawString(285, 525, "%s" %(pk.kasir_lunas.agnasabah.nama))
    c.drawString(535, 620, "Kuasa Pemutus Jaminan")
    c.drawString(535, 525, "%s" %(pk.kasir_lunas.gerai.nama_kg))
    c.setFont("Courier", 9)
    c.drawString(20, 775, "KETERANGAN NILAI PELUNASAN:")
    ###ISI PELUNSAN 
    c.drawString(20, 755, "Nilai Yang Diterima")
    c.drawString(130,755, ": Rp. %s" % (number_format(pk.nilai_pembulatan_lunas)))     
    tb=terbilang(pk.nilai_pembulatan_lunas)
    c.drawString(20, 745, "Terbilang") 
    c.drawString(90, 745, ":" ) 
    c.drawString(30, 735, "%s Rupiah" % (tb.title()))
    c.setFont("Courier", 9)
    c.drawString(280, 775, "KETERANGAN BARANG JAMINAN:")
    c.drawString(280, 765, "1. %s"% (pk.kasir_lunas.taksiran_kwitansi()[0:43] ))
    c.drawString(280, 755, "%s"% (pk.kasir_lunas.taksiran_kwitansi()[43:89] ))
    c.drawString(280, 745, "%s "% (pk.kasir_lunas.taksiran_kwitansi()[89:134] ))
    c.drawString(280, 735, "%s "% (pk.kasir_lunas.taksiran_kwitansi()[134:] ))

    if pk.kasir_lunas.barang.jenis_barang == u'1': ###('1','HP')
        c.drawString(280, 725, "Kelengkapan :") 
        c.drawString(280, 715, "1.Charger")
        c.drawString(335, 715, "%s "% (pk.kasir_lunas.barang.get_kondisi_charger_display()))  #CHARGER
        c.drawString(280, 705, "2.Baterai")
        c.drawString(335, 705, "%s "% (pk.kasir_lunas.barang.get_kondisi_batre_display()))  #BATRE
        c.drawString(280, 695, "3.Keypad")
        c.drawString(335, 695, "%s "% (pk.kasir_lunas.barang.get_kondisi_keybord_display()))   #KEYPAD
        c.drawString(280, 685, "4.Cassing")
        c.drawString(335, 685, "%s "% (pk.kasir_lunas.barang.get_kondisi_cassing_display())) #CASSING

        c.drawString(400, 715, "5.Layar")
        c.drawString(460, 715, "%s "% (pk.kasir_lunas.barang.get_kondisi_layar_display())) #LAYAR
        c.drawString(400, 705, "6.Password")
        c.drawString(460, 705, "%s "% (pk.kasir_lunas.barang.password_barang ))  #PASSWORD
        c.drawString(400, 695, "7.Dus")
        c.drawString(460, 695, "%s "% (pk.kasir_lunas.barang.get_dus_display())) #DUS
        c.drawString(400, 685, "8.Tas")
        c.drawString(460, 685, "%s "% (pk.kasir_lunas.barang.get_tas_display()))#TAS

    elif pk.kasir_lunas.barang.jenis_barang == u'2':###('2','LAPTOP/NB'),
        c.drawString(280, 725, "Kelengkapan :") 
        c.drawString(280, 715, "1.Charger")
        c.drawString(335, 715, "%s "% (pk.kasir_lunas.barang.get_kondisi_charger_display()))  #CHARGER
        c.drawString(280, 705, "2.Baterai")
        c.drawString(335, 705, "%s "% (pk.kasir_lunas.barang.get_kondisi_batre_display()))  #BATRE
        c.drawString(280, 695, "3.Keypad")
        c.drawString(335, 695, "%s "% (pk.kasir_lunas.barang.get_kondisi_keybord_display()))   #KEYPAD
        c.drawString(280, 685, "4.Cassing")
        c.drawString(335, 685, "%s "% (pk.kasir_lunas.barang.get_kondisi_cassing_display())) #CASSING

        c.drawString(400, 715, "5.Layar")
        c.drawString(460, 715, "%s "% (pk.kasir_lunas.barang.get_kondisi_layar_display())) #LAYAR
        c.drawString(400, 705, "6.Password")
        c.drawString(460, 705, "%s "% (pk.kasir_lunas.barang.password_barang ))  #PASSWORD
        c.drawString(400, 695, "7.Dus")
        c.drawString(460, 695, "%s "% (pk.kasir_lunas.barang.get_dus_display())) #DUS
        c.drawString(400, 685, "8.Tas")
        c.drawString(460, 685, "%s "% (pk.kasir_lunas.barang.get_tas_display()))#TAS

    elif pk.kasir_lunas.barang.jenis_barang == u'3':###('3','KAMERA'),
        c.drawString(280, 725, "Kelengkapan :")
        c.drawString(280, 715, "1.Lensa")
        c.drawString(335, 715, "%s "% (pk.kasir_lunas.barang.get_lensa_display()))
        c.drawString(280, 705, "2.Baterai")
        c.drawString(335, 705, "%s "% (pk.kasir_lunas.barang.get_batre_kamera_display()))
        c.drawString(280, 695, "3.Cassing")
        c.drawString(335, 695, "%s "% (pk.kasir_lunas.barang.get_cassing_kamera_display()))
        c.drawString(280, 685, "4.Dus")
        c.drawString(335, 685, "%s "% (pk.kasir_lunas.barang.get_dus_display()))

        c.drawString(420, 715, "5.Tas")
        c.drawString(460, 715, "%s "% (pk.kasir_lunas.barang.get_tas_display()))

    elif pk.kasir_lunas.barang.jenis_barang == u'4':###('4','PS'),
        c.drawString(280, 725, "Kelengkapan :")
        c.drawString(280, 715, "1.Optik")
        c.drawString(335, 715, "%s "% (pk.kasir_lunas.barang.get_kondisi_optik_ps_display()))
        c.drawString(280, 705, "2.Stick")
        c.drawString(335, 705, "%s "% (pk.kasir_lunas.barang.get_kondisi_stick_display()))
        c.drawString(280, 695, "3.HDMI")
        c.drawString(335, 695, "%s "% (pk.kasir_lunas.barang.get_kondisi_hdmi_display())) 
        c.drawString(280, 685, "4.Harddisk")
        c.drawString(335, 685, "%s "% (pk.kasir_lunas.barang.get_kondisi_harddisk_display()))

        c.drawString(420, 715, "5.Dus")
        c.drawString(460, 715, "%s "% (pk.kasir_lunas.barang.get_dus_display()))
        c.drawString(420, 705, "6.Tas")
        c.drawString(460, 705, "%s "% (pk.kasir_lunas.barang.get_tas_display()))

    elif pk.kasir_lunas.barang.jenis_barang == u'5':###('5','TV LCD'),
        c.drawString(280, 725, "Kelengkapan :")
        c.drawString(280, 715, "1.Layar")
        c.drawString(335, 715, "%s "% (pk.kasir_lunas.barang.get_kondisi_layar_tv_display()))
        c.drawString(280, 705, "2.Remote")
        c.drawString(335, 705, "%s "% (pk.kasir_lunas.barang.get_kondisi_remote_display()))
        c.drawString(280, 695, "3.Dus")
        c.drawString(335, 695, "%s "% (pk.kasir_lunas.barang.get_dus_display()))
        c.drawString(280, 685, "4.Tas")
        c.drawString(335, 685, "%s "% (pk.kasir_lunas.barang.get_tas_display()))

    elif pk.kasir_lunas.barang.jenis_kendaraan == u'1':###('6','MOTOR'),
        c.drawString(280, 725, "Kelengkapan :")
        c.drawString(280, 715, "1.Bpkb")
        c.drawString(390, 715, "%s "% (pk.kasir_lunas.barang.get_bpkb_display()))
        c.drawString(280, 705, "2.Stnk")
        c.drawString(390, 705, "%s "% (pk.kasir_lunas.barang.get_stnk_display()))
        c.drawString(280, 695, "3.Faktur")
        c.drawString(390, 695, "%s "% (pk.kasir_lunas.barang.get_faktur_display()))
        c.drawString(280, 685, "4.Gesek No Mesin")
        c.drawString(390, 685, "%s "% (pk.kasir_lunas.barang.get_gesek_nomesin_display()))
        c.drawString(280, 675, "5.Gesek No Rangka")
        c.drawString(390, 675, "%s "% (pk.kasir_lunas.barang.get_gesek_norangka_display()))

    elif pk.kasir_lunas.barang.jenis_kendaraan == u'2':###('7','Mobil'),
        c.drawString(280, 725, "Kelengkapan :")
        c.drawString(280, 715, "1.Bpkb")
        c.drawString(390, 715, "%s "% (pk.kasir_lunas.barang.get_bpkb_display()))
        c.drawString(280, 705, "2.Stnk")
        c.drawString(390, 705, "%s "% (pk.kasir_lunas.barang.get_stnk_display()))
        c.drawString(280, 695, "3.Faktur")
        c.drawString(390, 695, "%s "% (pk.kasir_lunas.barang.get_faktur_display()))
        c.drawString(280, 685, "4.Gesek No Mesin")
        c.drawString(390, 685, "%s "% (pk.kasir_lunas.barang.get_gesek_nomesin_display()))
        c.drawString(280, 675, "5.Gesek No Rangka")
        c.drawString(390, 675, "%s "% (pk.kasir_lunas.barang.get_gesek_norangka_display()))
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
    c.drawString(270, 442, "%s"% (pk.kasir_lunas.gerai.nama_cabang))
    c.setFont("Courier-Bold", 9)
    c.drawString(270, 432, "%s/Telp: 0%s "% (pk.kasir_lunas.gerai.alamat, pk.kasir_lunas.gerai.no_telp))

    c.setFont("Courier", 7)
    barcode = code128.Code128("%s" % (pk.kasir_lunas.norek()))
    barcode.drawOn(c, 185*mm, 139.5*mm)
    c.setFont("Courier-Bold", 9) 
    c.drawString(540, 380, "Tanggal Jatuh Tempo") 
    c.drawString(540, 349, "%s" % (pk.kasir_lunas.jatuhtempo.strftime('%d %b %Y')))
    c.drawString(540, 337, "Tanggal Pelunasan") 
    c.drawString(540, 320, "%s" % (pk.tanggal.strftime('%d %b %Y')))

    c.setFont("Courier-Bold", 12)  
    c.drawString(19, 400, "SURAT BUKTI GADAI PELUNASAN")
    c.setFont("Courier-Bold", 14)  
    c.drawString(220, 400, "NO NASABAH: %s"% (pk.kasir_lunas.nonas()))
    c.setFont("Courier", 9)
    c.drawString(20, 379, "Nomor Rek")
    c.drawString(100, 379, ": %s" % (pk.kasir_lunas.norek()))
    c.drawString(20, 369, "Nama")
    c.drawString(100, 369, ": %s" % (pk.kasir_lunas.agnasabah.nama))
    c.drawString(20, 359, "No Identitas")
    c.drawString(100, 359, ": %s" % (pk.kasir_lunas.agnasabah.no_ktp))
    c.drawString(20, 349, "No Telepon")
    c.drawString(100, 349, ": %s" % (pk.kasir_lunas.agnasabah.telepon_domisili,))
    c.drawString(20, 339, "Alamat")
    c.drawString(100, 339, ": %s No %s" %(pk.kasir_lunas.agnasabah.alamat_domisili,pk.kasir_lunas.agnasabah.no_rumah_domisili))
    c.drawString(100.5, 329, "  RT/RW %s/%s %s" %(pk.kasir_lunas.agnasabah.rt_domisili,pk.kasir_lunas.agnasabah.rw_domisili,pk.kasir_lunas.agnasabah.kelurahan_domisili,))
    c.drawString(20, 319, "Tempat,Tgl Lhr")
    c.drawString(100, 319, ": %s, %s" %(pk.kasir_lunas.agnasabah.tempat,pk.kasir_lunas.agnasabah.tgl_lahir.strftime('%d %B %Y')))
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
    c.drawString(285, 56, "%s" %(pk.kasir_lunas.agnasabah.nama))
    c.drawString(535, 151, "Kuasa Pemutus Jaminan")
    c.drawString(535, 56, "%s" %(pk.kasir_lunas.gerai.nama_kg))
    c.setFont("Courier", 9)
    c.drawString(20, 306, "KETERANGAN NILAI PINJAMAN:")
    ##ISI PELUNASAN
    c.drawString(20, 286, "Nilai Yang Diterima")
    c.drawString(130,286, ": Rp. %s" % (number_format(pk.nilai_pembulatan_lunas)))     
    tb=terbilang(pk.nilai_pembulatan_lunas)
    c.drawString(20, 276, "Terbilang") 
    c.drawString(90, 276, ":" ) 
    c.drawString(30, 266, "%s Rupiah" % (tb.title()))
    c.setFont("Courier", 9)
    c.drawString(280, 306, "KETERANGAN BARANG JAMINAN:")
    c.drawString(280, 296, "1. %s"% (pk.kasir_lunas.taksiran_kwitansi()[0:43] ))
    c.drawString(280, 286, "%s"% (pk.kasir_lunas.taksiran_kwitansi()[43:89] ))
    c.drawString(280, 276, "%s "% (pk.kasir_lunas.taksiran_kwitansi()[89:134] ))
    c.drawString(280, 266, "%s "% (pk.kasir_lunas.taksiran_kwitansi()[134:] ))

    if pk.kasir_lunas.barang.jenis_barang == u'1': ###('1','HP')
        c.drawString(280, 256, "Kelengkapan :") 
        c.drawString(280, 246, "1.Charger")
        c.drawString(335, 246, "%s "% (pk.kasir_lunas.barang.get_kondisi_charger_display()))  #CHARGER
        c.drawString(280, 236, "2.Baterai")
        c.drawString(335, 236, "%s "% (pk.kasir_lunas.barang.get_kondisi_batre_display()))  #BATRE
        c.drawString(280, 226, "3.Keypad")
        c.drawString(335, 226, "%s "% (pk.kasir_lunas.barang.get_kondisi_keybord_display()))   #KEYPAD
        c.drawString(280, 216, "4.Cassing")
        c.drawString(335, 216, "%s "% (pk.kasir_lunas.barang.get_kondisi_cassing_display())) #CASSING

        c.drawString(400, 246, "5.Layar")
        c.drawString(460, 246, "%s "% (pk.kasir_lunas.barang.get_kondisi_layar_display())) #LAYAR
        c.drawString(400, 236, "6.Password")
        c.drawString(460, 236, "%s "% (pk.kasir_lunas.barang.password_barang ))  #PASSWORD
        c.drawString(400, 226, "7.Dus")
        c.drawString(460, 226, "%s "% (pk.kasir_lunas.barang.get_dus_display())) #DUS
        c.drawString(400, 216, "8.Tas")
        c.drawString(460, 216, "%s "% (pk.kasir_lunas.barang.get_tas_display()))#TAS

    elif pk.kasir_lunas.barang.jenis_barang == u'2':###('2','LAPTOP/NB'),
        c.drawString(280, 256, "Kelengkapan :") 
        c.drawString(280, 246, "1.Charger")
        c.drawString(335, 246, "%s "% (pk.kasir_lunas.barang.get_kondisi_charger_display()))  #CHARGER
        c.drawString(280, 236, "2.Baterai")
        c.drawString(335, 236, "%s "% (pk.kasir_lunas.barang.get_kondisi_batre_display()))  #BATRE
        c.drawString(280, 226, "3.Keypad")
        c.drawString(335, 226, "%s "% (pk.kasir_lunas.barang.get_kondisi_keybord_display()))   #KEYPAD
        c.drawString(280, 216, "4.Cassing")
        c.drawString(335, 216, "%s "% (pk.kasir_lunas.barang.get_kondisi_cassing_display())) #CASSING

        c.drawString(400, 246, "5.Layar")
        c.drawString(460, 246, "%s "% (pk.kasir_lunas.barang.get_kondisi_layar_display())) #LAYAR
        c.drawString(400, 236, "6.Password")
        c.drawString(460, 236, "%s "% (pk.kasir_lunas.barang.password_barang ))  #PASSWORD
        c.drawString(400, 226, "7.Dus")
        c.drawString(460, 226, "%s "% (pk.kasir_lunas.barang.get_dus_display())) #DUS
        c.drawString(400, 216, "8.Tas")
        c.drawString(460, 216, "%s "% (pk.kasir_lunas.barang.get_tas_display()))#TAS

    elif pk.kasir_lunas.barang.jenis_barang == u'3':###('3','KAMERA'),
        c.drawString(280, 256, "Kelengkapan :")
        c.drawString(280, 246, "1.Lensa")
        c.drawString(335, 246, "%s "% (pk.kasir_lunas.barang.get_kondisi_lensa_display()))
        c.drawString(280, 236, "2.Baterai")
        c.drawString(335, 236, "%s "% (pk.kasir_lunas.barang.get_kondisi_batre_kamera_display()))
        c.drawString(280, 226, "3.Cassing")
        c.drawString(335, 226, "%s "% (pk.kasir_lunas.barang.get_kondisi_cassing_kamera_display()))
        c.drawString(280, 216, "4.Dus")
        c.drawString(335, 216, "%s "% (pk.kasir_lunas.barang.get_dus_display()))

        c.drawString(420, 246, "5.Tas")
        c.drawString(460, 246, "%s "% (pk.kasir_lunas.barang.get_tas_display()))

    elif pk.kasir_lunas.barang.jenis_barang == u'4':###('4','PS'),
        c.drawString(280, 256, "Kelengkapan :")
        c.drawString(280, 246, "1.Optik")
        c.drawString(335, 246, "%s "% (pk.kasir_lunas.barang.get_kondisi_optik_ps_display()))
        c.drawString(280, 236, "2.Stick")
        c.drawString(335, 236, "%s "% (pk.kasir_lunas.barang.get_kondisi_stick_display()))
        c.drawString(280, 226, "3.HDMI")
        c.drawString(335, 226, "%s "% (pk.kasir_lunas.barang.get_kondisi_hdmi_display())) 
        c.drawString(280, 216, "4.Harddisk")
        c.drawString(335, 216, "%s "% (pk.kasir_lunas.barang.get_kondisi_harddisk_display()))

        c.drawString(420, 246, "5.Dus")
        c.drawString(460, 246, "%s "% (pk.kasir_lunas.barang.get_dus_display()))
        c.drawString(420, 236, "6.Tas")
        c.drawString(460, 236, "%s "% (pk.kasir_lunas.barang.get_tas_display()))

    elif pk.kasir_lunas.barang.jenis_barang == u'5':###('5','TV LCD'),
        c.drawString(280, 256, "Kelengkapan :")
        c.drawString(280, 246, "1.Layar")
        c.drawString(335, 246, "%s "% (pk.kasir_lunas.barang.get_kondisi_layar_tv_display()))
        c.drawString(280, 236, "2.Remote")
        c.drawString(335, 236, "%s "% (pk.kasir_lunas.barang.get_kondisi_remote_display()))
        c.drawString(280, 226, "3. Dus")
        c.drawString(335, 226, "%s "% (pk.kasir_lunas.barang.get_dus_display()))
        c.drawString(280, 216, "4.Tas")
        c.drawString(335, 216, "%s "% (pk.kasir_lunas.barang.get_tas_display()))

    elif pk.kasir_lunas.barang.jenis_kendaraan == u'1':###('6','MOTOR'),
        c.drawString(280, 256, "Kelengkapan :")
        c.drawString(280, 246, "1.Bpkb")
        c.drawString(390, 246, "%s "% (pk.kasir_lunas.barang.get_bpkb_display()))
        c.drawString(280, 236, "2.Stnk")
        c.drawString(390, 236, "%s "% (pk.kasir_lunas.barang.get_stnk_display()))
        c.drawString(280, 226, "3.Faktur")
        c.drawString(390, 226, "%s "% (pk.kasir_lunas.barang.get_faktur_display()))
        c.drawString(280, 216, "4.Gesek No Mesin")
        c.drawString(390, 216, "%s "% (pk.kasir_lunas.barang.get_gesek_nomesin_display()))
        c.drawString(280, 206, "5.Gesek No Rangka")
        c.drawString(390, 206, "%s "% (pk.kasir_lunas.barang.get_gesek_norangka_display()))

    elif pk.kasir_lunas.barang.jenis_kendaraan == u'2':###('7','Mobil'),
        c.drawString(280, 256, "Kelengkapan :")
        c.drawString(280, 246, "1.Bpkb")
        c.drawString(390, 246, "%s "% (pk.kasir_lunas.barang.get_bpkb_display()))
        c.drawString(280, 236, "2.Stnk")
        c.drawString(390, 236, "%s "% (pk.kasir_lunas.barang.get_stnk_display()))
        c.drawString(280, 226, "3.Faktur")
        c.drawString(390, 226, "%s "% (pk.kasir_lunas.barang.get_faktur_display()))
        c.drawString(280, 216, "4.Gesek No Mesin")
        c.drawString(390, 216, "%s "% (pk.kasir_lunas.barang.get_gesek_nomesin_display()))
        c.drawString(280, 206, "5.Gesek No Rangka")
        c.drawString(390, 206, "%s "% (pk.kasir_lunas.barang.get_gesek_norangka_display()))
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
    c.drawString(18, 829, "( %s )" %(pk.kasir_lunas.agnasabah.nama)); y -=2*y1
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
    c.drawString(50, 535, "( %s )" %(pk.kasir_lunas.agnasabah.nama)); y -=y1
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
    c.drawString(18, 360, "( %s )" %(pk.kasir_lunas.agnasabah.nama)); y -=2*y1
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
    c.drawString(50, 66, "( %s )" %(pk.kasir_lunas.agnasabah.nama)); y -=y1
    c.drawString(50, 56, "Nasabah Penerima Kuasa"); y -=y1

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


def kwlunas_val(request, object_id):
    #gr = Pelunasan.objects.get(id = object_id)
    gr = KasirGerai.objects.get(kasir_lunas_id = object_id)
    gr.val = 1
    gr.save()
    template = 'kasir/view/kwlunas_val.html'
    variable = RequestContext(request, {'gr':gr,})
    return render_to_response(template,variable)

def list(request):    
    tanggal =  Pelunasan.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    return HttpResponseRedirect("/pelunasan/arsip/?tgl=%s" % tanggal.strftime('%Y-%m-%d') )

def list_day(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  Pelunasan.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  Pelunasan.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    gerai = []   
    
    for (b,k) in GERAI:
        
        bn = Pelunasan.objects.filter(gerai = b ).filter(tanggal = tanggal).order_by('tanggal')
    
        for pelunasan in bn :
            gerai.append(pelunasan) 
    template = 'pelunasan/list_day.html'
    variables = RequestContext(request, {
        'tanggal' : tanggal,
        'day_list' : Pelunasan.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month),
        'month_list': Pelunasan.objects.dates('tanggal', 'month', order="DESC").filter(tanggal__year=tanggal.year),
        'year_list' : Pelunasan.objects.dates('tanggal', 'year', order="DESC"),
        'gerai' : gerai,
    })    
    return render_to_response(template, variables)

def prpj_bulan(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  Pelunasan.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  Pelunasan.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    gerai = []
    
    
    for (b,k) in GERAI:
        
        bn = Pelunasan.objects.filter(gerai = b ).filter(tanggal__month=tanggal.month).order_by('no').order_by('cu')
    
        for akadgadai in bn :
            gerai.append(akadgadai)    
           
    template = 'pelunasan/list_month.html'
    variables = RequestContext(request, {
        'tanggal' : tanggal,
        'day_list' : Pelunasan.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month),
        'month_list': Pelunasan.objects.dates('tanggal', 'month', order="DESC").filter(tanggal__year=tanggal.year),
        'year_list' : Pelunasan.objects.dates('tanggal', 'year', order="DESC"),
        'gerai' : gerai,
    })    
    return render_to_response(template, variables)

def list_year(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  Pelunasan.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  Pelunasan.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    gerai = []
    
    for (b,k) in GERAI:
        
        bn = Pelunasan.objects.filter(gerai = b ).filter(tanggal__year=tanggal.year).order_by('no').order_by('cu')
    
        for pelunasan in bn :
            gerai.append(perlunasan)  
        
    
    template = 'perpanjang/list_year.html'

    variables = RequestContext(request, {
        'tanggal' : tanggal,
        'day_list' : Pelunasan.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month),
        'month_list': Pelunasan.objects.dates('tanggal', 'month', order="DESC").filter(tanggal__year=tanggal.year),
        'year_list' : Pelunasan.objects.dates('tanggal', 'year', order="DESC"),
        'gerai' : gerai ,
        })    
    return render_to_response(template, variables)

def rekapbulan(request, object_id):    
    tanggal = forms.DateField().clean(request.GET.get('tgl',''))
            
    prpj = Pelunasan.objects.filter(gerai= str(object_id)).filter(tanggal__month = tanggal.month).filter(tanggal__year=tanggal.year).order_by('gerai')
    template = 'pelunasan/bulan.html'
    variables = RequestContext(request, {
        'prpj': prpj,
        'tanggal' : tanggal,
        'nilai': sum([b.nilai for b in prpj ]),
        'jasa': sum([b.bea_jasa for b in prpj ]),
        'denda': sum([b.denda for b in prpj ]),
        #'simpan': sum([b.biayasimpan for b in barang ]),
        #'bersih' : sum([b.terima_bersih for b in barang ]),
    })    
    return render_to_response(template, variables)

def rekaphari(request, object_id):
    tanggal = forms.DateField().clean(request.GET.get('tgl',''))
            
    prpj = Pelunasan.objects.filter(gerai= str(object_id)).filter(tanggal = tanggal).order_by('gerai')
    
    template = 'pelunasan/harian.html'
    variables = RequestContext(request, {
        'prpj': prpj,
        'tanggal' : tanggal,
        'nilai': sum([b.nilai for b in prpj ]),
        'jasa': sum([b.bea_jasa_total for b in prpj ]),
        'denda' : sum([b.denda_total for b in prpj ]),
    })    
    return render_to_response(template, variables)
'''    

'''

def kwlunas(request, object_id):
    akadgadai = KasirGeraiPelunasan.objects.get(kasir_lunas__id=object_id)
    akadgadai.kasir_lunas.status_kwlunas = '1'
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
    response['Content-Disposition'] = 'attachment; filename= tanda_terima_lunas_%s.pdf' % akadgadai.kasir_lunas.norek()
    #for pk in tiga_play:

    c = canvas.Canvas(response, pagesize=(9.5*inch, 11*inch))
    header0=(8.25 *inch, (5.2 + 5.5) * inch)
    header1=(4.25 *inch, (5.3 + 5.5) * inch)
    colom1 = (0.5*inch, (4.3 + 5.5) *inch)
            #ke kiri  ke atas ke bawah
    colom2 = (6.7*inch, (4.5 + 5.5) *inch)
    colom3 = (6.0*inch, (4.8 + 4.5) *inch)
    colom4 = (0.5*inch, (7 + 5.5) *inch)
    header2= (4.25 *inch, (-0.1 + 5.5) * inch)
    colom6 = (0.5*inch, (-1.1 + 5.5) *inch)## == Colom 1
    colom5 = (6.7*inch, (-0.9 + 5.5) *inch) ## == Colom 2
    tb=terbilang(akadgadai.nilai_pembulatan_lunas)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/logoksu_hitamputih.png'), 1.0*inch, (5.5 + 1.5) * inch, width=200.5/17.5*0.51*inch,height=120/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 0.5*inch, (4.75 + 5.5) * inch, width=30/17.5*0.51*inch,height=25/17.5*0.51*inch,mask=None)
    
    x,y = header1
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Courier-Bold", 16)
    c.drawString(6.2 * inch , y-0.5*inch, "BUKTI SETOR PELUNASAN"); y -=2*y1
    #c.line( 6.2 * inch , y+0.06* inch , 7.5 * inch ,y+0.06* inch ) ; y -=y1
    c.setFont("Courier",8)
    # garis Paling atas
    c.line(35, 740, 400, 740)
    #garis Paling Bawah
    c.line(35, 720, 400, 720)
    #garis paling kiri
    c.line(35, 740, 35, 720)
    #garis paling kanan
    c.line(400, 740, 400, 720)
    c.setFont("Courier-Bold", 16)
    c.drawString(x-2.8*inch, y+0.20*inch, "KSU RIZKY ABADI"); y -=y1
    c.setFont("Courier",8)
    c.drawString(x-2.8*inch, y+0.20*inch, "Badan Hukum No.518/BH.88-DISKOP/THN.2007 Tgl 27 Desember 2007"); y -=y1
    c.drawString(x-2.8*inch, y+0.20*inch, "            No.210/PAD/M.KUKM.2/12/2015 Tgl 21 September 2015"); y -=y1
    c.drawString(x-2.8*inch, y+0.20*inch, "[%s/Telp: 0%s]"% (akadgadai.kasir_lunas.gerai.alamat, akadgadai.kasir_lunas.gerai.no_telp)); y -=y1
    #c.drawString(x-2.8*inch, y+0.20*inch, "Jln Cisaranten Kulon IV No.55 Bandung Tlp: 022-7808443"); y -=y1
    kb = str.upper(str(akadgadai.kasir_lunas.gerai.nama_cabang))
    c.setFont("Courier",7)
    c.drawString(x-3.5*inch, y, "%s" % akadgadai.kwlunas_validasi())
    c.setFont("Courier-Bold", 11)
    c.drawString(6.2 * inch , y-0.1*inch,"%s" % (akadgadai.kasir_lunas.gerai.nama_cabang)); y -=y1       
    

    ####KOLOM 2 Dua Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    ## Barcode
    c.setFont("Courier", 7)
    c.drawString(600, 780, "%s" % sekarang.strftime('[%-b][%Y]') )
    barcode = code128.Code128("%s" % (akadgadai.kasir_lunas.norek()))
    barcode.drawOn(c, 195*mm, 268*mm)
               
            
    c.setFont("Courier", 11)
    x,y = colom2
    y1 = 0.165 * inch
    c.setFont("Courier", 10)
    c.drawString(x-0.5*inch, y-0.2*inch, "No Tanda Terima    : %s" % (akadgadai.kasir_lunas.nonas())) ; y -=y1       
    c.drawString(x-0.5*inch, y-0.2*inch, "Tanggal Transaksi  : %s" % akadgadai.kasir_lunas.tanggal.strftime('%d %b %Y')); y -=4*y1       
    c.setFont("Courier-Bold", 11)
    c.drawString(x-1.5*inch, y-0.2*inch, "Nilai yang diterima  :")
    c.drawString(x+1.0*inch, y-0.2*inch, "Rp. %s"%(number_format(akadgadai.nilai_pembulatan_lunas)))
    ####AKHiR KOLOM 2 Dua Coy
    ####KOLOM 3 Tilu Coy
    ####AKHiR KOLOM 3 Tilu Coy

    ####KOLOM 1 hiji Coy
    x,y = colom1
    y1 = 0.165 * inch
    
    c.setFont("Courier", 11)
    c.drawString(x, y, "KSU RIZKY ABADI sudah menerima,"); y -=3*y1
    c.drawString(x, y, "Pelunasan Jaminan")
    c.drawString(x+1.7*inch, y, ": %s|%s|%s|%s"% (akadgadai.kasir_lunas.barang.merk,akadgadai.kasir_lunas.barang.sn,akadgadai.kasir_lunas.barang.type,akadgadai.kasir_lunas.barang.accesoris_barang1, )); y -=1.2*y1
    c.drawString(x, y, "Jenis Pinjaman")
    c.drawString(x+1.7*inch, y, ": PELUNASAN"); y -=1.2*y1
    c.drawString(x, y, "dari :"); y -=1.2*y1
    c.drawString(x, y, "Nomor Debitur")
    c.drawString(x+1.7*inch, y,": %s" % (akadgadai.kasir_lunas.nonas())); y -=1.2*y1
    c.drawString(x, y, "Nama")
    c.drawString(x+1.7*inch, y, ": %s" % (akadgadai.kasir_lunas.agnasabah.nama)); y -=1.2*y1
    c.drawString(x, y, "Alamat")
    c.drawString(x+1.7*inch, y, ": %s No %s" %(akadgadai.kasir_lunas.agnasabah.alamat_domisili,akadgadai.kasir_lunas.agnasabah.no_rumah_domisili)); y -=1.2*y1
    c.drawString(x+1.7*inch, y, "  RT/RW %s/%s %s" %(akadgadai.kasir_lunas.agnasabah.rt_domisili,akadgadai.kasir_lunas.agnasabah.rw_domisili,akadgadai.kasir_lunas.agnasabah.kelurahan_domisili,)); y -=1.2*y1
    c.drawString(x, y, "No KTP")
    c.drawString(x+1.7*inch, y, ": %s " %(akadgadai.kasir_lunas.agnasabah.no_ktp)); y -=1.2*y1
    c.drawString(x, y, "No Tlp / HP")
    c.drawString(x+1.7*inch, y, ": %s / %s " %(akadgadai.kasir_lunas.agnasabah.telepon_domisili,akadgadai.kasir_lunas.agnasabah.hp_domisili)); y -=1.2*y1
    c.setFont("Courier-Bold", 11)
    c.drawString(x,y-0.41* inch,  " ## %s Rupiah ##"  % tb.title())
    c.line( x , y-0.2* inch , x ,y-0.5* inch ) 
    c.line( 9 * inch , y-0.2* inch , 9 * inch ,y-0.5* inch ) 
    c.line( x , y-0.2* inch , 9 * inch ,y-0.2* inch ) 
    c.line( x , y-0.5* inch , 9 * inch ,y-0.5* inch ) ; y -=y1
    if akadgadai.kasir_lunas.gerai.kode_cabang == u'318' or akadgadai.kasir_lunas.gerai.kode_cabang == u'317': ###Elektronik
        c.drawString(x+6.7*inch, y-0.5*inch, "Cirebon, %s" % sekarang.strftime('%d %b %Y') ); y -=3*y1
    else:
        c.drawString(x+6.7*inch, y-0.5*inch, "Bandung, %s" % sekarang.strftime('%d %b %Y') ); y -=y1
    c.drawString(x,y-0.5*inch,  "Debitur,")
    c.drawString(x+6.7*inch, y-0.5*inch,"Kreditur,"); y -=5*y1
    c.drawString(x,y-0.5*inch, "( %s )" % (akadgadai.kasir_lunas.agnasabah.nama));
    c.drawString(x+6.7*inch, y-0.5*inch, "( %s )"%(akadgadai.kasir_lunas.gerai.nama_admin)); y -=y1
    c.setFont("Courier", 9)
    c.drawString(x,y-0.5*inch, "Bukti Setor Pelunasan Sah Setelah divalidasi atau di Tandatangan." )
    c.drawString(x+8.0*inch,y-0.5*inch, "Lembar 1" ); y -=y1

####AKHIR KOLOM 1 hiji Coy

    c.drawString(30, 400,"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - " )

    c.setFont("Courier", 7)
    c.drawString(600, 392, "%s" % sekarang.strftime('[%-b][%Y]') )
    barcode = code128.Code128("%s" % (akadgadai.kasir_lunas.norek()))
    barcode.drawOn(c, 195*mm, 131*mm)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/logoksu_hitamputih.png'), 1.0*inch, (0.1 + 1.5) * inch, width=200.5/17.5*0.51*inch,height=120/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 0.5*inch, (-0.65 + 5.5) * inch, width=30/17.5*0.51*inch,height=25/17.5*0.51*inch,mask=None)
    

    ### kedua
    x,y = header2
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Courier-Bold", 16)
    c.drawString(6.2 * inch , y-0.5*inch, "BUKTI SETOR PELUNASAN"); y -=2*y1
    #c.line( 6.2 * inch , y+0.06* inch , 7.5 * inch ,y+0.06* inch ) ; y -=y1
    c.setFont("Courier",8)
    # garis Paling atas
    c.line(35, 350, 400, 350)
    #garis Paling Bawah
    c.line(35, 330, 400, 330)
    #garis paling kiri
    c.line(35, 350, 35, 330)
    #garis paling kanan
    c.line(400, 350, 400, 330)
    c.setFont("Courier-Bold", 16)
    c.drawString(x-2.8*inch, y+0.20*inch, "KSU RIZKY ABADI"); y -=y1
    c.setFont("Courier",8)
    c.drawString(x-2.8*inch, y+0.20*inch, "Badan Hukum No.518/BH.88-DISKOP/THN.2007 Tgl 27 Desember 2007"); y -=y1
    c.drawString(x-2.8*inch, y+0.20*inch, "            No.210/PAD/M.KUKM.2/12/2015 Tgl 21 September 2015"); y -=y1
    c.drawString(x-2.8*inch, y+0.20*inch, "[%s/Telp: 0%s]"% (akadgadai.kasir_lunas.gerai.alamat, akadgadai.kasir_lunas.gerai.no_telp)); y -=y1
    #c.drawString(x-2.8*inch, y+0.20*inch, "Jln Cisaranten Kulon IV No.55 Bandung Tlp: 022-7808443"); y -=y1
    kb = str.upper(str(akadgadai.kasir_lunas.gerai.nama_cabang))
    c.setFont("Courier",7)
    c.drawString(x-3.5*inch, y, "%s" % akadgadai.kwlunas_validasi())
    c.setFont("Courier-Bold", 11)
    c.drawString(6.2 * inch , y-0.1*inch,"%s" % (akadgadai.kasir_lunas.gerai.nama_cabang)); y -=y1       
    

    ####KOLOM 2 Dua Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    ## Barcode
    c.setFont("Courier", 7)
    c.drawString(600, 780, "%s" % sekarang.strftime('[%-b][%Y]') )
    barcode = code128.Code128("%s" % (akadgadai.kasir_lunas.norek()))
    barcode.drawOn(c, 195*mm, 268*mm)
               
            
    c.setFont("Courier", 11)
    x,y = colom5
    y1 = 0.165 * inch
    c.setFont("Courier", 10)
    c.drawString(x-0.5*inch, y-0.2*inch, "No Tanda Terima    : %s" % (akadgadai.kasir_lunas.nonas())) ; y -=y1       
    c.drawString(x-0.5*inch, y-0.2*inch, "Tanggal Transaksi  : %s" % akadgadai.kasir_lunas.tanggal.strftime('%d %b %Y')); y -=4*y1       
    c.setFont("Courier-Bold", 11)
    c.drawString(x-1.5*inch, y-0.2*inch, "Nilai yang diterima  :")
    c.drawString(x+1.0*inch, y-0.2*inch, "Rp. %s"%(number_format(akadgadai.nilai_pembulatan_lunas)))
    ####AKHiR KOLOM 2 Dua Coy
    ####KOLOM 3 Tilu Coy
    ####AKHiR KOLOM 3 Tilu Coy

    ####KOLOM 1 hiji Coy
    x,y = colom6
    y1 = 0.165 * inch
    
    c.setFont("Courier", 11)
    c.drawString(x, y, "KSU RIZKY ABADI sudah menerima,"); y -=3*y1
    c.drawString(x, y, "Pelunasan Jaminan")
    c.drawString(x+1.7*inch, y, ": %s|%s|%s|%s"% (akadgadai.kasir_lunas.barang.merk,akadgadai.kasir_lunas.barang.sn,akadgadai.kasir_lunas.barang.type,akadgadai.kasir_lunas.barang.accesoris_barang1, )); y -=1.2*y1
    c.drawString(x, y, "Jenis Pinjaman")
    c.drawString(x+1.7*inch, y, ": PELUNASAN"); y -=1.2*y1
    c.drawString(x, y, "dari :"); y -=1.2*y1
    c.drawString(x, y, "Nomor Debitur")
    c.drawString(x+1.7*inch, y,": %s" % (akadgadai.kasir_lunas.nonas())); y -=1.2*y1
    c.drawString(x, y, "Nama")
    c.drawString(x+1.7*inch, y, ": %s" % (akadgadai.kasir_lunas.agnasabah.nama)); y -=1.2*y1
    c.drawString(x, y, "Alamat")
    c.drawString(x+1.7*inch, y, ": %s No %s" %(akadgadai.kasir_lunas.agnasabah.alamat_domisili,akadgadai.kasir_lunas.agnasabah.no_rumah_domisili)); y -=1.2*y1
    c.drawString(x+1.7*inch, y, "  RT/RW %s/%s %s" %(akadgadai.kasir_lunas.agnasabah.rt_domisili,akadgadai.kasir_lunas.agnasabah.rw_domisili,akadgadai.kasir_lunas.agnasabah.kelurahan_domisili,)); y -=1.2*y1
    c.drawString(x, y, "No KTP")
    c.drawString(x+1.7*inch, y, ": %s " %(akadgadai.kasir_lunas.agnasabah.no_ktp)); y -=1.2*y1
    c.drawString(x, y, "No Tlp / HP")
    c.drawString(x+1.7*inch, y, ": %s / %s " %(akadgadai.kasir_lunas.agnasabah.telepon_domisili,akadgadai.kasir_lunas.agnasabah.hp_domisili)); y -=1.2*y1
    c.setFont("Courier-Bold", 11)
    c.drawString(x,y-0.41* inch,  " ## %s Rupiah ##"  % tb.title())
    c.line( x , y-0.2* inch , x ,y-0.5* inch ) 
    c.line( 9 * inch , y-0.2* inch , 9 * inch ,y-0.5* inch ) 
    c.line( x , y-0.2* inch , 9 * inch ,y-0.2* inch ) 
    c.line( x , y-0.5* inch , 9 * inch ,y-0.5* inch ) ; y -=y1
    if akadgadai.kasir_lunas.gerai.kode_cabang == u'318' or akadgadai.kasir_lunas.gerai.kode_cabang == u'317': ###Elektronik
        c.drawString(x+6.7*inch, y-0.5*inch, "Cirebon, %s" % sekarang.strftime('%d %b %Y') ); y -=3*y1
    else:
        c.drawString(x+6.7*inch, y-0.5*inch, "Bandung, %s" % sekarang.strftime('%d %b %Y') ); y -=y1
    c.drawString(x,y-0.5*inch,  "Debitur,")
    c.drawString(x+6.7*inch, y-0.5*inch,"Kreditur,"); y -=5*y1
    c.drawString(x,y-0.5*inch, "( %s )" % (akadgadai.kasir_lunas.agnasabah.nama));
    c.drawString(x+6.7*inch, y-0.5*inch, "( %s )"%(akadgadai.kasir_lunas.gerai.nama_admin)); y -=y1
    c.setFont("Courier", 9)
    c.drawString(x,y-0.5*inch, "Bukti Setor Pelunasan Sah Setelah divalidasi atau di Tandatangan." )
    c.drawString(x+8.0*inch,y-0.5*inch, "Lembar 2" ); y -=y1
    c.showPage()



##############-------------------------------------------------------------------------------------

    header0=(8.25 *inch, (5.2 + 5.5) * inch)
    header1=(4.60 *inch, (5.35 + 5.5) * inch)
    colom1 = (0.5*inch, (4.35 + 5.5) *inch)
    colom2 = (6.3*inch, (4.35 + 5.5) *inch)
    colom3 = (6.3*inch, (4.35 + 4.5) *inch)
    
    tb=terbilang(akadgadai.nilai_pembulatan_lunas)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/logoksu_hitamputih.png'), 1.0*inch, (5.5 + 1.5) * inch, width=200.5/17.5*0.51*inch,height=120/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 0.5*inch, (4.75 + 5.5) * inch, width=30/17.5*0.51*inch,height=25/17.5*0.51*inch,mask=None)
    
    x,y = header1
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Courier-Bold", 16)
    c.drawString(6.2 * inch , y-0.5*inch, "BUKTI SETOR PELUNASAN"); y -=2*y1
    #c.line( 6.2 * inch , y+0.06* inch , 7.5 * inch ,y+0.06* inch ) ; y -=y1
    c.setFont("Courier",8)
    # garis Paling atas
    c.line(35, 740, 400, 740)
    #garis Paling Bawah
    c.line(35, 720, 400, 720)
    #garis paling kiri
    c.line(35, 740, 35, 720)
    #garis paling kanan
    c.line(400, 740, 400, 720)
    c.setFont("Courier-Bold", 16)
    c.drawString(x-2.8*inch, y+0.20*inch, "KSU RIZKY ABADI"); y -=y1
    c.setFont("Courier",8)
    c.drawString(x-2.8*inch, y+0.20*inch, "Badan Hukum No.518/BH.88-DISKOP/THN.2007 Tgl 27 Desember 2007"); y -=y1
    c.drawString(x-2.8*inch, y+0.20*inch, "            No.210/PAD/M.KUKM.2/12/2015 Tgl 21 September 2015"); y -=y1
    c.drawString(x-2.8*inch, y+0.20*inch, "[%s/Telp: 0%s]"% (akadgadai.kasir_lunas.gerai.alamat, akadgadai.kasir_lunas.gerai.no_telp)); y -=y1
    #c.drawString(x-2.8*inch, y+0.20*inch, "Jln Cisaranten Kulon IV No.55 Bandung Tlp: 022-7808443"); y -=y1
    kb = str.upper(str(akadgadai.kasir_lunas.gerai.nama_cabang))
    c.setFont("Courier",7)
    c.drawString(x-3.5*inch, y, "%s" % akadgadai.kwlunas_validasi())
    c.setFont("Courier-Bold", 11)
    c.drawString(6.2 * inch , y-0.1*inch,"%s" % (akadgadai.kasir_lunas.gerai.nama_cabang)); y -=y1       
    

    ####KOLOM 2 Dua Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    ## Barcode
    c.setFont("Courier", 7)
    c.drawString(600, 780, "%s" % sekarang.strftime('[%-b][%Y]') )
    barcode = code128.Code128("%s" % (akadgadai.kasir_lunas.norek()))
    barcode.drawOn(c, 195*mm, 268*mm)
               
            
    c.setFont("Courier", 11)
    x,y = colom2
    y1 = 0.165 * inch
    c.setFont("Courier", 10)
    c.drawString(x-0.5*inch, y-0.2*inch, "No Tanda Terima    : %s" % (akadgadai.kasir_lunas.nonas())) ; y -=y1       
    c.drawString(x-0.5*inch, y-0.2*inch, "Tanggal Transaksi  : %s" % akadgadai.kasir_lunas.tanggal.strftime('%d %b %Y')); y -=4*y1       
    c.setFont("Courier-Bold", 11)
    c.drawString(x-1.5*inch, y-0.2*inch, "Nilai yang diterima  :")
    c.drawString(x+1.0*inch, y-0.2*inch, "Rp. %s"%(number_format(akadgadai.nilai_pembulatan_lunas)))
    ####AKHiR KOLOM 2 Dua Coy
    ####KOLOM 3 Tilu Coy
    ####AKHiR KOLOM 3 Tilu Coy

    ####KOLOM 1 hiji Coy
    x,y = colom1
    y1 = 0.165 * inch
    
    c.setFont("Courier", 11)
    c.drawString(x, y, "KSU RIZKY ABADI sudah menerima,"); y -=3*y1
    c.drawString(x, y, "Pelunasan Jaminan")
    c.drawString(x+1.7*inch, y, ": %s|%s|%s|%s"% (akadgadai.kasir_lunas.barang.merk,akadgadai.kasir_lunas.barang.sn,akadgadai.kasir_lunas.barang.type,akadgadai.kasir_lunas.barang.accesoris_barang1, )); y -=1.2*y1
    c.drawString(x, y, "Jenis Pinjaman")
    c.drawString(x+1.7*inch, y, ": PELUNASAN"); y -=1.2*y1
    c.drawString(x, y, "dari :"); y -=1.2*y1
    c.drawString(x, y, "Nomor Debitur")
    c.drawString(x+1.7*inch, y,": %s" % (akadgadai.kasir_lunas.nonas())); y -=1.2*y1
    c.drawString(x, y, "Nama")
    c.drawString(x+1.7*inch, y, ": %s" % (akadgadai.kasir_lunas.agnasabah.nama)); y -=1.2*y1
    c.drawString(x, y, "Alamat")
    c.drawString(x+1.7*inch, y, ": %s No %s" %(akadgadai.kasir_lunas.agnasabah.alamat_domisili,akadgadai.kasir_lunas.agnasabah.no_rumah_domisili)); y -=1.2*y1
    c.drawString(x+1.7*inch, y, "  RT/RW %s/%s %s" %(akadgadai.kasir_lunas.agnasabah.rt_domisili,akadgadai.kasir_lunas.agnasabah.rw_domisili,akadgadai.kasir_lunas.agnasabah.kelurahan_domisili,)); y -=1.2*y1
    c.drawString(x, y, "No KTP")
    c.drawString(x+1.7*inch, y, ": %s " %(akadgadai.kasir_lunas.agnasabah.no_ktp)); y -=1.2*y1
    c.drawString(x, y, "No Tlp / HP")
    c.drawString(x+1.7*inch, y, ": %s / %s " %(akadgadai.kasir_lunas.agnasabah.telepon_domisili,akadgadai.kasir_lunas.agnasabah.hp_domisili)); y -=1.2*y1
    c.setFont("Courier-Bold", 11)
    c.drawString(x,y-0.41* inch,  " ## %s Rupiah ##"  % tb.title())
    c.line( x , y-0.2* inch , x ,y-0.5* inch ) 
    c.line( 9 * inch , y-0.2* inch , 9 * inch ,y-0.5* inch ) 
    c.line( x , y-0.2* inch , 9 * inch ,y-0.2* inch ) 
    c.line( x , y-0.5* inch , 9 * inch ,y-0.5* inch ) ; y -=y1
    if akadgadai.kasir_lunas.gerai.kode_cabang == u'318' or akadgadai.kasir_lunas.gerai.kode_cabang == u'317': ###Elektronik
        c.drawString(x+6.7*inch, y-0.5*inch, "Cirebon, %s" % sekarang.strftime('%d %b %Y') ); y -=3*y1
    else:
        c.drawString(x+6.7*inch, y-0.5*inch, "Bandung, %s" % sekarang.strftime('%d %b %Y') ); y -=y1
    c.drawString(x,y-0.5*inch,  "Debitur,")
    c.drawString(x+6.7*inch, y-0.5*inch,"Kreditur,"); y -=5*y1
    c.drawString(x,y-0.5*inch, "( %s )" % (akadgadai.kasir_lunas.agnasabah.nama));
    c.drawString(x+6.7*inch, y-0.5*inch, "( %s )"%(akadgadai.kasir_lunas.gerai.nama_admin)); y -=y1
    c.setFont("Courier", 9)
    c.drawString(x,y-0.5*inch, "Bukti Setor Pelunasan Sah Setelah divalidasi atau di Tandatangan." )
    c.drawString(x+8.0*inch,y-0.5*inch, "Lembar 3" ); y -=y1
    c.showPage()
    c.save()
    return response

def kwlunas_kendaraan(request, object_id):
    akadgadai = Pelunasan.objects.get(id=object_id)
    akadgadai.pelunasan.status_kwlunas = 1
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
    response['Content-Disposition'] = 'attachment; filename= tanda_terima_lunas_%s.pdf' % akadgadai.norek()
    
    c = canvas.Canvas(response, pagesize=(9.5*inch, 11*inch))

    header0=(8.25 *inch, (5.2 + 5.5) * inch)
    header1=(4.60 *inch, (5.35 + 5.5) * inch)
    colom1 = (0.3*inch, (4.35 + 5.5) *inch)
    colom2 = (6.3*inch, (4.35 + 5.5) *inch)
    colom3 = (6.3*inch, (4.35 + 4.5) *inch)
    
    #c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ra2.png'), 0.5*inch, (4.8 + 5.8) * inch, width=24.5/17.5*0.51*inch,height=24/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/ra2.png'), 0.5*inch, (4.8 + 5.5) * inch, width=28.5/17.5*0.51*inch,height=24/17.5*0.51*inch)

    x,y = header0
    y1 = 0.126* inch
    c.setFont("Courier", 7)
    #c.drawString(x-0.02*inch, y+0.2, "[kowil][koger][%b] [akadgadai.mu]"); y -=2*y1
    #c.drawString(x-0.02*inch, y+0.2*inch,    "( %s )"% (akadgadai.agnasabah.nama)  ); y -=y1
    c.drawString(x+0.02*inch, y+0.2*inch, "%s" % sekarang.strftime('[%-b][%Y]') ); y -= y1

    x,y = header1
    y1 = 0.10* inch
    c.setFont("Courier-Bold", 14)
    #c.setFillColorRGB(255,0,0) #warna pada huruf
    #c.setStrokeColorRGB(0,255,0.3) #warna pada garis
    c.drawString(100, 780, "KSU RIZKY ABADI" )
    c.setFont("Courier-Bold", 16)
    c.drawCentredString(340, 775, "TANDA TERIMA LUNAS")
    c.line( 235 , 773, 450 ,773  ) 
    c.setFont("Courier-Bold", 12)
    c.drawCentredString(340, 763, "GERAI [%s]"% (akadgadai.gerai.nama_cabang))
    c.setFont("Courier-Bold", 12)


    x,y = colom1
    y1 = 0.100 * inch

    tb=terbilang(akadgadai.jumlah_pelunasan_kendaraan)
    c.setFont("Courier",11)
    c.drawString(430, 750, "No Tanda Terima    : %s" % (akadgadai.pelunasan.nonas()))
    c.drawString(430, 740, "Tanggal Transaksi  : %s" % akadgadai.tanggal.strftime('%d %b %Y'))
    c.drawString(430, 730, "Tanggal Jt tempo   : %s" % akadgadai.pelunasan.jatuhtempo.strftime('%d %b %Y'))
    #c.drawString(430, 720, "Jangka waktu       : %s [ Hari ]" % akadgadai.pelunasan.jangka_waktu)
  
    c.drawString(100, 742, "Validasi :")
    #c.drawString(40, 725, "%s" % (akadgadai.kw_validasi()))
    # garis Paling atas
    c.line(35, 740, 400, 740)
    #garis Paling Bawah
    c.line(35, 720, 400, 720)
    #garis paling kiri
    c.line(35, 740, 35, 720)
    #garis paling kanan
    c.line(400, 740, 400, 720)
    
    c.drawString(402, 685,"Nilai Pinjaman")
    c.drawString(520, 685,":Rp.")
    c.drawRightString(650, 685,"%s"% (number_format(akadgadai.nilai)))
    #c.drawString(390, 675, "Biaya Simpan/Survey")
    #c.drawString(520, 675,":Rp.")
    #c.drawRightString(620, 675, "%s"% (number_format(akadgadai.biayasimpan)))
    c.drawString(390, 665, "Biaya Denda ")
    c.drawString(520, 665,":Rp.")
    c.drawRightString(620, 665, "%s"% (number_format(akadgadai.denda_all())))
    
    #c.drawString(390, 660, "%s"% (number_format(akadgadai.bea_materai)))
    c.setLineWidth(.3)
    c.line(510, 663, 650, 663)
    c.drawString(402, 650, "Total Biaya")
    c.drawString(502, 650, ":Rp.")
    c.drawRightString(650, 650, "%s"%(number_format(akadgadai.denda_all())))
    c.line(510, 648, 650, 648)
    c.drawString(380, 630, "Nilai yang diterima")
    c.setFont("Courier-Bold",11)
    c.drawString(525, 630, ":Rp.")
    c.drawRightString(650, 630, "%s"%(number_format(akadgadai.jumlah_pelunasan_kendaraan)))
    c.line(535, 627, 650, 627)
    c.line(535, 624, 650, 624)

    c.setFont("Courier",11)
    c.drawString(35,710, "KSU RIZKY ABADI sudah menerima,")
    c.drawString(35,700, "Pelunasan Jaminan")
    c.setFont("Courier", 10)
    c.drawString(150,700, ":%s|%s"% (akadgadai.pelunasan.barang.type_kendaraan, akadgadai.pelunasan.barang.no_polisi, ))
    c.line(155, 698, 525, 698)
    c.drawString(35,688, "Jenis Pinjaman")
    c.drawString(150,688, ":PELUNASAN")
    c.line(155, 686, 340, 686)
    c.drawString(35,676, "dari :")
    c.drawString(35,664, "Nomor Debitur")
    c.drawString(150,664, ":%s" % akadgadai.pelunasan.norek())
    c.line(155, 662, 340, 662)
    #c.drawString(35,652, "Nomor Pinjaman")
    #c.drawString(150,652, ":%s" % (akadgadai.pelunasan.nonas()))
    #c.line(155, 650, 340, 650)
    c.drawString(35,640, "Nama")
    c.drawString(150,640, ":%s" %(akadgadai.pelunasan.agnasabah.nama))
    c.line(155, 638, 340, 638)
    c.drawString(35,628, "Alamat")
    c.setFont("Courier",11)
    c.drawString(150,628, ":%s" %(akadgadai.pelunasan.agnasabah.alamat_ktp))
    c.line(155, 626, 340, 626)
    c.drawString(157,616, "RT/RW %s/%s %s" %(akadgadai.pelunasan.agnasabah.rt_ktp,akadgadai.pelunasan.agnasabah.rw_ktp,akadgadai.pelunasan.agnasabah.kelurahan_ktp,))
    c.line(155, 614, 340, 614)
    c.setFont("Courier",11)
    c.drawString(35,604, "No Ktp")
    c.drawString(150,604, ":%s " %(akadgadai.pelunasan.agnasabah.no_ktp))
    c.line(155, 602, 340, 602)
    c.drawString(35,582, "No Telp /HP")
    c.drawString(150,582, ":%s / %s " %(akadgadai.pelunasan.agnasabah.telepon_ktp,akadgadai.pelunasan.agnasabah.hp_ktp))
    c.line(155, 580, 340, 580)
    
    
    c.setFont("Courier", 11)
    
    c.setFont("Courier-Bold", 11)
    c.setLineWidth(.9)
    c.drawString(35,565,  " ##%s Rupiah ##"  % tb.title())
    # garis Paling atas
    c.line(35, 575, 650, 575)
	#garis Paling Bawah
    c.line(35, 560, 650, 560)
	#garis paling kiri
    c.line(35, 575, 35, 560)
    #garis paling kanan
    c.line(650, 575, 650, 560)
   
    c.setFont("Courier", 10)
    c.drawString(35, 550, "Demikian tanda terima pelunasan ini dibuat sebagai bukti")
    c.drawString(35, 540,"pelunasan pinjaman saudara.")
    c.drawString(35, 530,"Kami berharap kerja  sama ini dapat  terus terjalin pada")
    c.drawString(35, 520,"masa-masa yang akan datang.")
    c.drawString(35, 510,"Terima kasih")
    c.drawString(35, 500,"Badan Hukum No.518/BH.88-Diskop/THN.2007 Tgl.27 Desember 2007")

    c.setFont("Courier",11)
    c.drawString(410, 540, "Debitur,")
    c.drawString(410, 490, "%s"%(akadgadai.pelunasan.agnasabah.nama))
    c.line(410, 488, 560, 488)
    c.drawRightString(650, 550, "Bandung %s" % sekarang.strftime('%d %b %Y') )
    c.drawString(568, 540, "Kepala Gerai,")
    #c.drawString(570, 490, "%s"%(akadgadai.gerai.adm_gadai))
    c.line(570, 488, 653, 488)
    c.showPage()
    c.save()
    return response
        
