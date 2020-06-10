from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gadai.appgadai.lelang.views import*
from gadai.appgadai.models import *
import xlwt
import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
import io
import xlsxwriter
from gadai.xlsxwriter.workbook import Workbook
from gadai.appgadai.templatetags.number_format import number_format
from gadai.appgadai.models import *
from gadai.appgadai.lelang.forms import BarangLelangForm
from django import forms
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os, string
from django.conf import settings
from gadai.appgadai.templatetags.terbilang import terbilang
from gadai.appkeuangan.report.forms import SearchForm

def lapur(request, object_id):
    sekarang = datetime.datetime.now()
    pl = AkadGadai.objects.get(id=object_id)
    if request.method == 'POST':
        f = BarangLelangForm(request.POST)
        if f.is_valid():
            aglelang = f.cleaned_data['aglelang']
            tgl_lelang =f.cleaned_data['tgl_lelang']
            harga_jual =f.cleaned_data['harga_jual']
            nama_pembeli = f.cleaned_data['nama_pembeli']

            f.save()
            messages.add_message(request, messages.INFO, 'Barang Lelang Telah ditambahkan')
        return HttpResponseRedirect('/lelang/jual/')
    else:
        f = BarangLelangForm(initial = {'tgl_lelang': sekarang.date, 'aglelang':pl.id})
        template = 'lelang/add.html'
        variables = RequestContext(request,{'form':f})
        return render_to_response(template,variables)

@login_required
def list(request):
    lapur = AkadGadai.objects.filter(status_transaksi= 'LELANG').filter(baranglelang__isnull=True)    
    template = 'lelang/lelang.html'
    variables = RequestContext(request, {
        'lapur': lapur,
        'tot_nilai': sum([b.nilai for b in lapur ]),
        'jml' : len(lapur),
        })    
    return render_to_response(template, variables)

'''
def jual(request):
    lapur = AkadGadai.objects.filter(status_transaksi__in=('2','6','7')).filter(baranglelang__isnull=False)
    template = 'lelang/datajual.html'
    variables = RequestContext(request, {
        'lapur': lapur,
        'tot_nilai': sum([b.nilai for b in lapur ]),
        'tot_lelang': sum([b.hargalelang() for b in lapur ]),
        'tot_nilai_lelang': sum([b.nilai_lelang() for b in lapur ]),
        'tot_rugi': sum([b.rugi_lelang() for b in lapur ]),
        'jml' : len(lapur),
        })                        
    return render_to_response(template, variables)
'''

@login_required
def jual(request):
    form =SearchForm
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET :
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']        
        if id_cabang == '500' :
            lapur = BarangLelang.objects.filter(aglelang__status_transaksi__in=('2','6','7')).\
                filter(tgl_lelang__range=(start_date,end_date)).filter(aglelang__baranglelang__isnull=False)
            template='lelang/datajual.html'
            variable = RequestContext(request,{'lapur':lapur,
            'form':form,'id_cabang':id_cabang,'start_date':start_date,'end_date':end_date,
            'start_date':start_date,'end_date':end_date,\
            'tot_nilai': sum([b.aglelang.nilai for b in lapur ]),'tot_lelang': sum([b.aglelang.hargalelang() for b in lapur ]),\
            'tot_nilai_lelang': sum([b.aglelang.nilai_lelang() for b in lapur ]),\
            'tot_rugi': sum([b.aglelang.rugi_lelang() for b in lapur ]),'jml' : len(lapur),})
            return render_to_response(template,variable)
        else:
            lapur= BarangLelang.objects.filter(aglelang__status_transaksi__in=('2','6','7')).\
                filter(aglelang__gerai__kode_cabang = id_cabang).filter(tgl_lelang__range=(start_date,end_date))
            template= 'lelang/datajual.html'
            variable = RequestContext(request,{'lapur':lapur,'form':form,'id_cabang':id_cabang,'start_date':start_date,
            'end_date':end_date,\
            'tot_nilai': sum([b.aglelang.nilai for b in lapur ]),'tot_lelang': sum([b.aglelang.hargalelang() for b in lapur ]),\
            'tot_nilai_lelang': sum([b.aglelang.nilai_lelang() for b in lapur ]),\
            'tot_rugi': sum([b.aglelang.rugi_lelang() for b in lapur ]),'jml' : len(lapur),})
            return render_to_response(template,variable)

    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            lapur= BarangLelang.objects.filter(aglelang__status_transaksi__in=('2','6','7')).filter(aglelang__baranglelang__isnull=False).\
                filter(tgl_lelang__range=(start_date,end_date))
            template1= 'lelang/datajual_pdf.html'
            variable = RequestContext(request,{'tes':lapur,'form':form,'start_date':start_date,'end_date':end_date,
                'id_cabang':id_cabang,'nilai': sum([b.aglelang.nilai for b in lapur ]),
                'tot_nilai': sum([b.aglelang.nilai for b in lapur ]),'tot_lelang': sum([b.aglelang.hargalelang() for b in lapur ]),\
                'tot_nilai_lelang': sum([b.aglelang.nilai_lelang() for b in lapur ]),\
                'tot_rugi': sum([b.aglelang.rugi_lelang() for b in lapur ])})
            return render_to_response(template1,variable)
        else:
            lapur = BarangLelang.objects.filter(aglelang__status_transaksi__in=('2','6','7')).filter(aglelang__baranglelang__isnull=False).\
                filter(tgl_lelang__range=(start_date,end_date)).filter(aglelang__gerai__kode_cabang = id_cabang)
            template1= 'lelang/datajual_pdf.html'
            variable = RequestContext(request,{'tes':lapur,'form':form,'start_date':start_date,'end_date':end_date,
                'id_cabang':id_cabang,'nilai': sum([b.aglelang.nilai for b in lapur ]),
                'tot_nilai': sum([b.aglelang.nilai for b in lapur ]),'tot_lelang': sum([b.aglelang.hargalelang() for b in lapur ]),\
                'tot_nilai_lelang': sum([b.aglelang.nilai_lelang() for b in lapur ]),\
                'tot_rugi': sum([b.aglelang.rugi_lelang() for b in lapur ])})
            return render_to_response(template1,variable)    
 
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']         
        if id_cabang == '500' :
            akad = BarangLelang.objects.filter(aglelang__status_transaksi__in=('2','6','7')).\
                filter(tgl_lelang__range=(start_date,end_date)).filter(aglelang__baranglelang__isnull=False)
            a = sum([b.aglelang.nilai for b in akad ])
            b = sum([b.harga_jual for b in akad])
            c = sum([b.aglelang.nilai_lelang() for b in akad])
            f = start_date
            g = end_date
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': 0})
            bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#C0C0C0'})
            money_format = workbook.add_format({'num_format': '#,##0'})
            date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
            merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#C0C0C0'})
            merge_format1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter',})
        
            worksheet.set_column(0, 0, 10) 
            worksheet.set_column(1, 1, 18)
            worksheet.set_column(2, 2, 11)
            worksheet.set_column(3, 3, 11)
            worksheet.set_column(4, 4, 10)
            worksheet.set_column(5, 5, 10)
            worksheet.set_column(6, 6, 10)
            worksheet.set_column(7, 7, 10)
            worksheet.set_column(8, 8, 10)
            worksheet.set_column(9, 9, 10)

            worksheet.merge_range('A1:I1', 'LAPORAN BARANG TERJUAL GABUNGAN', merge_format1)
            worksheet.merge_range('A2:K2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Nasabah', merge_format)
            worksheet.merge_range('C4:C5', 'Plafon', merge_format)
            worksheet.merge_range('D4:D5', 'Barang', merge_format)
            worksheet.merge_range('E4:E5', 'JT', merge_format)
            worksheet.merge_range('F4:F5', 'Gerai', merge_format)
            worksheet.merge_range('G4:G5', 'T Lelang', merge_format)
            worksheet.merge_range('H4:H5', 'Harga Jual', merge_format)
            worksheet.merge_range('I4:I5', 'Pembeli', merge_format)
            worksheet.merge_range('J4:J5', 'Selisih', merge_format)
            worksheet.merge_range('K4:K5', 'Rugi', merge_format)

            row = 5
            col = 0
            for t in akad:
                worksheet.write_string(row, col , t.aglelang.norek() )
                worksheet.write_string(row, col + 1 , t.aglelang.agnasabah.nama)
                worksheet.write_number(row, col + 2 , t.aglelang.nilai,money_format)                
                worksheet.write_string(row, col + 3 , t.aglelang.barang.type + '' + t.aglelang.barang.merk )
                worksheet.write_datetime(row, col + 4 ,t.aglelang.jatuhtempo,date_format)
                worksheet.write_string(row, col + 5 ,t.aglelang.gerai.nama_cabang )
                worksheet.write_datetime(row, col + 6 ,t.tgl_lelang,date_format)
                worksheet.write_number(row, col + 7 , t.harga_jual,money_format)                 
                worksheet.write_string(row, col + 8 , t.nama_pembeli)
                worksheet.write_number(row, col + 9 , t.aglelang.nilai_lelang(),money_format)
                worksheet.write_number(row, col + 10 , t.aglelang.rugi_lelang(),money_format)
                row += 1

            worksheet.write(row,1, 'Total', bold)    
            worksheet.write(row,2, a, money_format)
            #worksheet.write(row,7, b, money_format)
            worksheet.write(row,9, c, money_format)

            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Laporan_Penjualan_gabungan.xlsx"
            return response
        else:
            akad= BarangLelang.objects.filter(aglelang__status_transaksi__in=('2','6','7')).filter(aglelang__baranglelang__isnull=False).\
                filter(tgl_lelang__range=(start_date,end_date)).filter(aglelang__gerai__kode_cabang = id_cabang)
            a = sum([b.aglelang.nilai for b in akad ])
            f = start_date
            g = end_date
            #h = nacab.nama_cabang
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': 0})
            bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#C0C0C0'})
            money_format = workbook.add_format({'num_format': '#,##0'})
            date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
            merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#C0C0C0'})
            merge_format1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter',})
            
            worksheet.set_column(0, 0, 10) 
            worksheet.set_column(1, 1, 18)
            worksheet.set_column(2, 2, 11)
            worksheet.set_column(3, 3, 11)
            worksheet.set_column(4, 4, 10)
            worksheet.set_column(5, 5, 10)
            worksheet.set_column(6, 6, 10)
            worksheet.set_column(7, 7, 10)
            worksheet.set_column(8, 8, 10)
            worksheet.set_column(9, 9, 10)
        
            worksheet.merge_range('A1:I1', 'LAPORAN BARANG TERJUAL GABUNGAN', merge_format1)
            worksheet.merge_range('A2:K2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Nasabah', merge_format)
            worksheet.merge_range('C4:C5', 'Plafon', merge_format)
            worksheet.merge_range('D4:D5', 'Barang', merge_format)
            worksheet.merge_range('E4:E5', 'JT', merge_format)
            worksheet.merge_range('F4:F5', 'Gerai', merge_format)
            worksheet.merge_range('G4:G5', 'T Lelang', merge_format)
            worksheet.merge_range('H4:H5', 'Harga Jual', merge_format)
            worksheet.merge_range('I4:I5', 'Pembeli', merge_format)
            worksheet.merge_range('J4:J5', 'Selisih', merge_format)
            worksheet.merge_range('K4:K5', 'Rugi', merge_format)

            row = 5
            col = 0
            for t in akad:
                worksheet.write_string(row, col , t.aglelang.norek() )
                worksheet.write_string(row, col + 1 , t.aglelang.agnasabah.nama)
                worksheet.write_number(row, col + 2 , t.aglelang.nilai,money_format)
                worksheet.write_string(row, col + 3 , t.aglelang.barang.type + '' + t.aglelang.barang.merk )
                worksheet.write_datetime(row, col + 4 ,t.aglelang.jatuhtempo,date_format)
                worksheet.write_string(row, col + 5 ,t.aglelang.gerai.nama_cabang )
                worksheet.write_datetime(row, col + 6 ,t.tgl_lelang,date_format)
                worksheet.write_number(row, col + 7 , t.harga_jual,money_format)
                worksheet.write_string(row, col + 8 , t.nama_pembeli)
                worksheet.write_number(row, col + 9 , t.aglelang.nilai_lelang(),money_format)
                worksheet.write_number(row, col + 10 , t.aglelang.rugi_lelang(),money_format)
                row += 1

            worksheet.write(row,1, 'Total', bold)
            worksheet.write(row,2, a, money_format)        
            workbook.close()
            output.seek(0)
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Laporan_Penjualan.xlsx"
            return response

    else:
        variables = RequestContext(request, {'form': form})
        return render_to_response('lelang/datajual.html', variables)

def kuitansi(request,object_id):
    akadgadai = AkadGadai.objects.get(id=object_id)
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
    response['Content-Disposition'] = 'attachment; filename= kuitansi_%s.pdf' % akadgadai.norek()
    
    c = canvas.Canvas(response, pagesize=(9.5*inch, 11*inch))

    header0=(8.25 *inch, (5.2 + 5.5) * inch)
    header1=(4.60 *inch, (5.35 + 5.5) * inch)
    colom1 = (0.3*inch, (4.35 + 5.5) *inch)
    colom2 = (6.3*inch, (4.35 + 5.5) *inch)
    colom3 = (6.3*inch, (4.35 + 4.5) *inch)
    
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
    c.drawString(x-0.75*inch, y, "KSU RIZKY ABADI"); y -=1.5*y1
    c.drawString(x-1.9*inch, y, "[JL.JAKARTA NO 55/Telp: 022-75481003]"); y -=y1
    y -=  1 * y1
    y2 = y + 0.1 * inch
    c.setFont("Courier-Bold", 11)
    c.line( 0.2 * inch , y2 , 9.3 * inch , y2 );
    
    x,y = colom1
    y1 = 0.100 * inch

    tb=terbilang(akadgadai.hargalelang())

    c.setFont("Courier-Bold", 10)
    c.drawString(x, y, "Sudah terima dari: %s" % (akadgadai.namalelang()));  y -=1.5*y1
    c.setFont("Courier",10)
    c.drawString(x, y, "Uang Senilai     : Rp. %s" %(number_format(akadgadai.hargalelang()))); y -=1.5* y1
    c.drawString(x, y, "Terbilang        : #%s rupiah#"%(tb)); y -=1.5*y1
    c.drawString(x, y, "Untuk Pembayaran : Pembelian %s/%s/%s/%s"% (akadgadai.barang.merk,akadgadai.barang.sn,akadgadai.barang.type,akadgadai.barang.accesoris_barang1, )); y -=1.5* y1
    c.setFont("Courier", 10)
    c.drawString(x+2.6*inch, y-0.4*inch, "KSU RIZKY ABADI" ); y -=2* y1
    c.drawString(x-0.0*inch, y-0.2*inch,   "Nasabah "  ); y -= y1
    c.setFont("Courier", 10)
    c.drawString(x-0.0*inch, y-0.9*inch,    "[%s]"% (akadgadai.namalelang())  ); y -=2*y1
    c.drawString(x+2.6*inch, y-0.7*inch,   "[ MUHTAR LATIEP ]"); y -=1.2*y1
    c.setFont("Courier", 12)
    c.drawString(x+2.6*inch, y+0.37*inch, "Bandung,%s" % sekarang.strftime('%d %B %Y') ); y -= 1.5*y1
       
    
    
    y -= +7 * y1
    y2 = y + 2.6 * inch
    c.setFont("Courier-Bold", 12)
    c.drawString(x, y, "PERHATIAN :"); y -=1.2*y1
    c.setFont("Courier", 10)
    c.drawString(x, y, "Barang yang telah dibeli tidak dapat ditukar/dikembalikan,kecuali telah ada perjanjian sebelumnya "); y -=1.2*y1
    
    c.showPage()
    c.save()
    
    return response

