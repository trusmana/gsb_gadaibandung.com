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
from gadai.appgadai.models import *
from gadai.appgadai.perpanjang.forms import *

def rekapbulan(request, object_id):    
    tanggal = forms.DateField().clean(request.GET.get('tgl',''))
    prpj = Perpanjang.objects.filter(gerai= str(object_id)).filter(tanggal__month = tanggal.month).filter(tanggal__year=tanggal.year).order_by('gerai')
    t_denda = 0
    t_jasa = 0
    for k in prpj :
        t_denda += k.denda()
        t_jasa += k.bea_jasa()
    template = 'perpanjang/bulan.html'
    variables = RequestContext(request, {
        'prpj': prpj,
        'tanggal' : tanggal,
        'nilai': sum([b.nilai for b in prpj ]),
        'td': t_denda,'tj':t_jasa
    })
    return render_to_response(template, variables)

def list(request):
    tanggal =  Perpanjang.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    return HttpResponseRedirect("/perpanjang/arsip/?tgl=%s" % tanggal.strftime('%Y-%m-%d') )

def list_day(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  Perpanjang.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  Perpanjang.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    gerai = []   
    
    for (b,k) in GERAI:
        
        bn = Perpanjang.objects.filter(gerai = b ).filter(tanggal = tanggal).filter(status__isnull=False).order_by('status')
    
        for perpanjang in bn :
            gerai.append(perpanjang) 
    template = 'perpanjang/list_day.html'
    variables = RequestContext(request, {
        'tanggal' : tanggal,
        'day_list' : Perpanjang.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month),
        'month_list': Perpanjang.objects.dates('tanggal', 'month', order="DESC").filter(tanggal__year=tanggal.year),
        'year_list' : Perpanjang.objects.dates('tanggal', 'year', order="DESC"),
        'gerai' : gerai,
    })    
    return render_to_response(template, variables)

def list_month(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  Perpanjang.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month).filter(tanggal__year=tanggal.year)[0] 
        except:
            tanggal =  Perpanjang.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    gerai = []   
    
    for (b,k) in GERAI:
        
        bn = Perpanjang.objects.filter(gerai = b ).filter(tanggal__month=tanggal.month).filter(tanggal__year=tanggal.year).filter(status__isnull=False).order_by('tanggal')
    
        for perpanjang in bn :
            gerai.append(perpanjang) 
    template = 'perpanjang/list_month.html'
    variables = RequestContext(request, {
        'tanggal' : tanggal,
        'day_list' : Perpanjang.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month),
        'month_list': Perpanjang.objects.dates('tanggal', 'month', order="DESC").filter(tanggal__year=tanggal.year),
        'year_list' : Perpanjang.objects.dates('tanggal', 'year', order="DESC"),
        'gerai' : gerai,
    })    
    return render_to_response(template, variables)

def list_year(request):
    try :
        f = forms.DateField()
        tanggal = f.clean(request.GET.get('tgl',''))
    except :
        try:
            tanggal =  Perpanjang.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month)[0] 
        except:
            tanggal =  Perpanjang.objects.dates('tanggal', 'day', order="DESC")[0] 
    
    gerai = []   
    
    for (b,k) in GERAI:
        
        bn = Perpanjang.objects.filter(gerai = b ).filter(tanggal__year=tanggal.year).filter(status__isnull=False).order_by('tanggal')
    
        for perpanjang in bn :
            gerai.append(perpanjang) 
    template = 'perpanjang/list_year.html'
    variables = RequestContext(request, {
        'tanggal' : tanggal,
        'day_list' : Perpanjang.objects.dates('tanggal', 'day', order="DESC").filter(tanggal__month=tanggal.month),
        'month_list': Perpanjang.objects.dates('tanggal', 'month', order="DESC").filter(tanggal__year=tanggal.year),
        'year_list' : Perpanjang.objects.dates('tanggal', 'year', order="DESC"),
        'gerai' : gerai,
    })    
    return render_to_response(template, variables)

def rekaphari(request, object_id):
    tanggal = forms.DateField().clean(request.GET.get('tgl',''))
            
    prpj = Perpanjang.objects.filter(gerai= str(object_id)).filter(tanggal = tanggal).order_by('gerai')
    
    template = 'perpanjang/harian.html'
    variables = RequestContext(request, {
        'prpj': prpj,
        'tanggal' : tanggal,
        'nilai': sum([b.nilai for b in prpj ]),
        
    })    
    return render_to_response(template, variables)
  
def cetak(request, object_id):
    prpj = Perpanjang.objects.get(id=object_id)
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


        trk=prpj.agkredit.tanggal
        dd=patokan.month-trk.month
        yy=patokan.year-trk.year

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= kuitansi_%s.pdf' % prpj.agkredit.norek()
    
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
    c.drawString(x+0.02*inch, y+0.2*inch, "%s" % sekarang.strftime('[%-b][%Y]') ); y -= y1

    x,y = header1
    y1 = 0.10* inch
    c.setFont("Courier-Bold", 16)
    c.drawString(x-0.5*inch, y, "KWITANSI" ); y -=1.5*y1
    c.setFont("Courier-Bold", 12)
    c.drawString(x-3.1*inch, y,"Badan Hukum No.518/BH.88-Diskop/THN.2007 Tgl 27 Desember 2007 "); y -=1.5*y1
    c.setFont("Courier-Bold", 12)
    c.drawString(x-1.1*inch, y, "GERAI [%s]"% (prpj.agkredit.gerai.nama)); y -=1.5*y1
    c.drawString(x-1.9*inch, y, "[%s/Telp: %s]"% (prpj.agkredit.gerai.alamat, prpj.agkredit.gerai.telepon)); y -=y1
    
    x,y = colom1
    y1 = 0.100 * inch



    tb=terbilang(prpj.agkredit.terima_bersih)

    c.setFont("Courier-Bold", 9)
    c.drawString(x, y, "Sudah terima dari   : %s" % (prpj.agkredit.agnasabah.nama)); y -= 1.2*y1
    c.setFont("Courier", 9)
    c.drawString(x, y, "Alamat              : %s" % (prpj.agkredit.agnasabah.alamat_ktp)); y -=1.5*y1
    c.drawString(x, y, "No.KTP              : %s" % (prpj.agkredit.agnasabah.no_ktp)); y -=1.5*y1
    c.drawString(x, y, "Telp/Hp             : %s" % (prpj.agkredit.agnasabah.telepon_ktp)); y -=2*y1
    c.drawString(0.3*inch, y-0.1*inch, "Untuk Pembayaran    : %s %s"% (prpj.agkredit.barang.merk,prpj.agkredit.barang.type, )); y -=1.5* y1	
    c.drawString(0.3*inch, y-0.1*inch, "Status              : %s" % (prpj.status)  ); y -=1.5* y1
    c.setFont("Courier", 9)
    c.drawString(x+2.2*inch, y-0.6*inch, "Petugas Admin %s" % (prpj.gerai.adm_gadai) ); y -=2* y1
    c.drawString(x+0.3*inch, y-0.4*inch,   "Nasabah "  ); y -= y1
    c.setFont("Courier", 9)
    c.drawString(x-0.0*inch, y-1.2*inch,    "[%s]"% (prpj.agkredit.agnasabah.nama)  ); y -=1.2*y1
    c.drawString(x+2.6*inch, y-1.08*inch,   "[%s]"% sekarang.strftime('%d %B %Y') ); y -=1.2*y1
    c.setFont("Courier", 9)
    c.drawString(x+2.2*inch, y+0.09*inch, "Bandung,%s" % sekarang.strftime('%d %B %Y') ); y -= 4*y1     
    
    
    y -= +11.5 * y1
    y2 = y + 2.8 * inch
    c.setFont("Courier-Bold", 10)
    c.drawString(x, y, "PERHATIAN :"); y -=1.2*y1
    c.setFont("Courier", 9)
    c.drawString(x, y, "1. Pelunasan pinjaman harus dilakukan tepat waktu sesuai tanggal jatuh tempo"); y -=1.2*y1
    c.drawString(x, y, "2. Bilamana akan melakukan perpanjangan,harap mendatangi gerai 1(satu) hari sebelum jatuh tempo.");y -=1.2*y1
    c.drawString(x, y, "3. Apabila sampai dengan tanggal jatuh tempo tidak melakukan pelunasan atau tidak diperpanjang,");y -=1.2*y1
    c.drawString(x, y, "   maka Koperasi berhak menjual barang jaminan yang bersangkutan.");y -=1.2*y1
    c.drawString(x, y, "4. Setiap melakukan pelunasan atau perpanjangan pinjaman, Kwitansi ini harus diperlihatkan kepada petugas.");y -=1.2*y1
    c.drawString(x, y, "5. Kwitansi sah bilamana telah divalidasi ditandatangani dan distampel.");y -=y1
    
    y -=  2 * y1
    y2 = y + 0.1 * inch
   
    x,y = colom2
    y1 = 0.100 * inch
    tb=terbilang(prpj.jumlahperpanjang)
    c.setFont("Courier", 9)
    c.drawString(x-0.15*inch, y, "Nomor Nasabah      : %s" % prpj.agkredit.nonas()); y -=3.5*y1
    c.drawString(x-0.15*inch, y, "Nomor Kwitansi     : %s" % (prpj.norek())); y -=1.5*y1
    c.drawString(x-0.15*inch, y, "Tanggal Transaksi  : %s" % prpj.tanggal.strftime('%d %b %Y')); y -= 1.5*y1
    c.drawString(x-0.15*inch, y, "Tanggal Jt tempo   : %s" % prpj.jatuhtempo_perpanjang().strftime('%d %b %Y')); y -=2.5* y1
    c.drawString(x-0.15*inch, y, "Hari Terlambat     : %s (Hari)" % prpj.terlambat) ; y -=3.5*y1
    c.drawString(x-0.15*inch, y, "Jangka waktu       : %s" % prpj.jw) ; y -=5*y1
    c.drawString(x-0.15*inch, y, "Nilai Pinjaman        : Rp.%s"% (number_format(prpj.agkredit.nilai))); y -=1.5* y1
    c.drawString(x-0.15*inch, y, "Bea Simpan/Survey  : Rp %s"% (number_format(prpj.bea_simpan))); y -=1.5* y1
    c.drawString(x-0.15*inch, y, "Denda              : Rp %s"% (number_format(prpj.denda()))); y -= 1.5*y1
    c.drawString(x-0.15*inch, y, "Jasa               : Rp.%s"%(number_format(prpj.jumlahjasa))); y -=1.5* y1
    c.line( 7.6 * inch , y , 9.02 * inch , y ) ; y -=1.5*y1
    c.setFont("Courier-Bold", 9)
    c.drawString(x-0.15*inch, y, "Nilai Yang dibayar : Rp.%s"%(number_format(prpj.jumlahperpanjang))); y -=1.2* y1
    c.setFont("Courier", 12)
    
    y -=  1 * y1
    y2 = y + 0.1 * inch
    c.setFont("Courier-Bold", 10)
    c.line( 0.4 * inch , y2 , 8.2 * inch , y2 );
    c.line( 0.4* inch , y2 , 0.4 * inch , y -2* y1 );
    c.line( 8.2 * inch , y2 , 8.2  * inch , y - 2 * y1 );
    y -= y1
    c.drawString(x-5.8*inch, y,  "Terbilang: ##%sRupiah ##"  % tb.title() ); y -= y1
    c.line( 0.4* inch , y , 8.2 * inch , y );
    
    c.showPage()
    c.save()
    
    return response  

def cetak_kendaraan(request, object_id):
    prpj = Perpanjang.objects.get(id=object_id)
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


        trk=prpj.agkredit.tanggal
        dd=patokan.month-trk.month
        yy=patokan.year-trk.year

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename= kuitansi_%s.pdf' % prpj.agkredit.norek()
    
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
    c.drawString(x+0.02*inch, y+0.2*inch, "%s" % sekarang.strftime('[%-b][%Y]') ); y -= y1

    x,y = header1
    y1 = 0.10* inch
    c.setFont("Courier-Bold", 16)
    c.drawString(x-0.5*inch, y, "KWITANSI" ); y -=1.5*y1
    c.setFont("Courier-Bold", 12)
    c.drawString(x-3.1*inch, y,"Badan Hukum No.518/BH.88-Diskop/THN.2007 Tgl 27 Desember 2007 "); y -=1.5*y1
    c.setFont("Courier-Bold", 12)
    c.drawString(x-1.1*inch, y, "GERAI [%s]"% (prpj.agkredit.gerai.nama)); y -=1.5*y1
    c.drawString(x-1.9*inch, y, "[%s/Telp: %s]"% (prpj.agkredit.gerai.alamat, prpj.agkredit.gerai.telepon)); y -=y1
    
    x,y = colom1
    y1 = 0.100 * inch



    tb=terbilang(prpj.agkredit.terima_bersih)

    c.setFont("Courier-Bold", 9)
    c.drawString(x, y, "Sudah terima dari   : %s" % (prpj.agkredit.agnasabah.nama)); y -= 1.2*y1
    c.setFont("Courier", 9)
    c.drawString(x, y, "Alamat              : %s" % (prpj.agkredit.agnasabah.alamat_ktp)); y -=1.5*y1
    c.drawString(x, y, "No.KTP              : %s" % (prpj.agkredit.agnasabah.no_ktp)); y -=1.5*y1
    c.drawString(x, y, "Telp/Hp             : %s" % (prpj.agkredit.agnasabah.telepon_ktp)); y -=2*y1
    c.drawString(0.3*inch, y-0.1*inch, "Untuk Pembayaran    : %s %s"% (prpj.agkredit.barang.type_kendaraan,prpj.agkredit.barang.no_polisi, )); y -=1.5* y1	
    c.drawString(0.3*inch, y-0.1*inch, "Status              : %s" % (prpj.status)  ); y -=1.5* y1
    c.setFont("Courier", 9)
    c.drawString(x+2.2*inch, y-0.6*inch, "Petugas Admin %s" % (prpj.gerai.adm_gadai) ); y -=2* y1
    c.drawString(x+0.3*inch, y-0.4*inch,   "Nasabah "  ); y -= y1
    c.setFont("Courier", 9)
    c.drawString(x-0.0*inch, y-1.2*inch,    "[%s]"% (prpj.agkredit.agnasabah.nama)  ); y -=1.2*y1
    c.drawString(x+2.6*inch, y-1.08*inch,   "[%s]"% sekarang.strftime('%d %B %Y') ); y -=1.2*y1
    c.setFont("Courier", 9)
    c.drawString(x+2.2*inch, y+0.09*inch, "Bandung,%s" % sekarang.strftime('%d %B %Y') ); y -= 4*y1     
    
    
    y -= +11.5 * y1
    y2 = y + 2.8 * inch
    c.setFont("Courier-Bold", 10)
    c.drawString(x, y, "PERHATIAN :"); y -=1.2*y1
    c.setFont("Courier", 9)
    c.drawString(x, y, "1. Pelunasan pinjaman harus dilakukan tepat waktu sesuai tanggal jatuh tempo"); y -=1.2*y1
    c.drawString(x, y, "2. Bilamana akan melakukan perpanjangan,harap mendatangi gerai 1(satu) hari sebelum jatuh tempo.");y -=1.2*y1
    c.drawString(x, y, "3. Apabila sampai dengan tanggal jatuh tempo tidak melakukan pelunasan atau tidak diperpanjang,");y -=1.2*y1
    c.drawString(x, y, "   maka Koperasi berhak menjual barang jaminan yang bersangkutan.");y -=1.2*y1
    c.drawString(x, y, "4. Setiap melakukan pelunasan atau perpanjangan pinjaman, Kwitansi ini harus diperlihatkan kepada petugas.");y -=1.2*y1
    c.drawString(x, y, "5. Kwitansi sah bilamana telah divalidasi ditandatangani dan distampel.");y -=y1
    
    y -=  2 * y1
    y2 = y + 0.1 * inch
   
    x,y = colom2
    y1 = 0.100 * inch
    tb=terbilang(prpj.jmlprpj_kendaraan)
    c.setFont("Courier", 9)
    c.drawString(x-0.15*inch, y, "Nomor Nasabah      : %s" % prpj.agkredit.nonas()); y -=2.5*y1
    c.drawString(x-0.15*inch, y, "Nomor Kwitansi     : %s" % (prpj.norek())); y -=1.5*y1
    c.drawString(x-0.15*inch, y, "Tanggal Transaksi  : %s" % prpj.tanggal.strftime('%d %b %Y')); y -= 1.5*y1
    c.drawString(x-0.15*inch, y, "Tanggal Jt tempo   : %s" % prpj.jt_kendaraan().strftime('%d %b %Y')); y -=1.5* y1
    c.drawString(x-0.15*inch, y, "Hari Terlambat     : %s (Hari)" % prpj.terlambat_kendaraan) ; y -=2.5*y1
    c.drawString(x-0.15*inch, y, "Jangka waktu       : %s (Bln)" % prpj.jw_kendaraan) ; y -=5*y1
    c.drawString(x-0.15*inch, y, "Nilai Pinjaman        : Rp.%s"% (number_format(prpj.agkredit.nilai))); y -=1.5* y1
    c.drawString(x-0.15*inch, y, "Bea Simpan/Survey  : Rp %s"% (number_format(prpj.beasimpan_kendaraan))); y -=1.5* y1
    c.drawString(x-0.15*inch, y, "Denda              : Rp %s"% (number_format(prpj.denda_kendaraan()))); y -= 1.5*y1
    c.drawString(x-0.15*inch, y, "Jasa Terlambat     : Rp %s"% (number_format(prpj.bea_jasa_terlambat_kendaraan()))); y -= 1.5*y1
    c.drawString(x-0.15*inch, y, "Jasa               : Rp.%s"%(number_format(prpj.bea_jasa_kendaraan()))); y -=1.5* y1
    c.line( 7.6 * inch , y , 9.02 * inch , y ) ; y -=1.5*y1
    c.setFont("Courier-Bold", 9)
    c.drawString(x-0.15*inch, y, "Nilai Yang dibayar : Rp.%s"%(number_format(prpj.jmlprpj_kendaraan))); y -=3.5* y1
    c.setFont("Courier", 9)
    
    y -=  1 * y1
    y2 = y + 0.1 * inch
    c.setFont("Courier-Bold", 10)
    c.line( 0.4 * inch , y2 , 8.2 * inch , y2 );
    c.line( 0.4* inch , y2 , 0.4 * inch , y -2* y1 );
    c.line( 8.2 * inch , y2 , 8.2  * inch , y - 2 * y1 );
    y -= y1
    c.drawString(x-5.8*inch, y,  "Terbilang: ##%sRupiah ##"  % tb.title() ); y -= y1
    c.line( 0.4* inch , y , 8.2 * inch , y );
    
    c.showPage()
    c.save()
    
    return response   
    
def terbit_bulan_csv(request, year, month):
    '''Tampilkan PK pada bulan/tahun terpilih dalam format CSV'''
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=pk_%s_%s.csv' % (year, month)
    writer = csv.writer(response)
    writer.writerow(['No Rek','Transaksi','Tagihan','Anggota','JW','Nilai','Provisi','ADM','Tabungan','Asuransi','Wajib','Terima Bersih','Angsuran','Baki Debet','Status','Retur','Pokok Perbln','Jasa PerBln','Pokok jasa PBB','Penyaluran','Terbit'])
    for p in Kwitansi.objects.filter(tagihan__year=year).filter(tagihan__month=month):
        writer.writerow([p.pkredit.no(),p.pkredit.tanggal,p.tagihan,p.pkredit.anggota,p.pkredit.jangka_waktu,p.pkredit.nilai,p.pkredit.provisi,p.pkredit.administrasi,p.pkredit.tabungan,p.pkredit.jaminan_kredit,p.pkredit.wajib,p.pkredit.terima_bersih,p.pkredit.besar_angsuran,p.pkredit.debet(),p.pkredit.catatan_lunas,p.pkredit.retur,p.pkredit.ppb(),p.pkredit.jasaperbln(),p.pkredit.pokokjasaperbln(),p.pkredit.penyaluran(),p.terbit])
    return response


