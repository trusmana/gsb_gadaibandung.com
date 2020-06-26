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
from gadai.appgadai.akadgadai.forms import *
from gadai.appgadai.manop.forms import *
from django.shortcuts import render_to_response, get_object_or_404,render,redirect
from gadai.appkeuangan.report.forms import SearchForm


def all_data_cair(request):
    akad= AkadGadai.objects.all()
    start_date = None
    end_date = None
    form = SearchForm()
    all = []
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500':
            tb = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(kepalagerai__status = 1).order_by('gerai')
            a = sum([b.nilai for b in tb ])
            c = sum([b.jasa_all() for b in tb ])
            d = sum([b.adm_all() for b in tb ])
            e = sum([b.beasimpan_all() for b in tb ])
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
            worksheet.set_column(10, 10, 10)
            worksheet.set_column(11, 11, 10)
            worksheet.set_column(12, 12, 10)
            worksheet.set_column(13, 13, 10)
        
            worksheet.merge_range('A1:L1', 'LAPORAN PENCAIRAN GABUNGAN', merge_format1)
            worksheet.merge_range('A2:L2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama', merge_format)
            worksheet.merge_range('D4:D5', 'Tgl Akad', merge_format)
            worksheet.merge_range('E4:E5', 'Jw', merge_format)
            worksheet.merge_range('F4:F5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('G4:G5', 'Jenis', merge_format)
            worksheet.merge_range('H4:H5', 'SK', merge_format)
            worksheet.merge_range('I4:I5', 'Plafon', merge_format)
            worksheet.merge_range('J4:L4', 'Pendapatan', merge_format)
            worksheet.write('J5', 'Jasa',  bold1)
            worksheet.write('K5', 'Adm', bold1)
            worksheet.write('L5', 'Bea Simpan', bold1)
            worksheet.write('M5', 'Status', bold1)
            row = 5
            col = 0
            for t in tb:
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.agnasabah.nama)                
                worksheet.write_datetime(row, col + 3 , t.tanggal,date_format)
                worksheet.write(row, col + 4 , t.jw_all())
                worksheet.write_datetime(row, col + 5, t.jatuhtempo, date_format)
                worksheet.write_string(row, col + 6, t.get_jenis_transaksi_display())
                worksheet.write_string(row, col + 7, t.get_jns_gu_display())
                worksheet.write_number(row, col + 8, t.nilai, money_format)
                worksheet.write_number(row, col + 9, t.jasa_all(), money_format)
                worksheet.write_number(row, col + 10, t.adm_all(), money_format)
                worksheet.write_number(row, col + 11, t.biayasimpan, money_format)
                worksheet.write_string(row, col + 12, t.sts_trans_excel())
                row += 1

            worksheet.write(row,4, 'Total', bold)    
            worksheet.write(row,8, a, money_format)
            worksheet.write(row, 9, c, money_format)
            worksheet.write(row, 10, d, money_format)
            worksheet.write(row, 11, e, money_format)
        
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Laporan_all_cair.xlsx"
            return response
        else:
            tb = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(gerai__kode_cabang = id_cabang).filter(kepalagerai__status = 1)
            a = sum([b.nilai for b in tb ])
            c = sum([b.jasa_all() for b in tb ]) 
            d = sum([b.adm_all() for b in tb ]) 
            e = sum([b.beasimpan_all() for b in tb ]) 
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
            worksheet.set_column(10, 10, 10)
            worksheet.set_column(11, 11, 10)
            worksheet.set_column(12, 12, 10)
            worksheet.set_column(13, 13, 10)
        
            worksheet.merge_range('A1:L1', 'LAPORAN PENCAIRAN ', merge_format1)
            worksheet.merge_range('A2:L2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama', merge_format)
            worksheet.merge_range('D4:D5', 'Tgl Akad', merge_format)
            worksheet.merge_range('E4:E5', 'Jw', merge_format)
            worksheet.merge_range('F4:F5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('G4:G5', 'Jenis', merge_format)
            worksheet.merge_range('H4:H5', 'SK', merge_format)
            worksheet.merge_range('I4:I5', 'Plafon', merge_format)
            worksheet.merge_range('J4:L4', 'Pendapatan', merge_format)
            worksheet.write('J5', 'Jasa',  bold1)
            worksheet.write('K5', 'Adm', bold1)
            worksheet.write('L5', 'Bea Simpan', bold1)
            worksheet.write('M5', 'Status', bold1)
            row = 5
            col = 0
            for t in tb:
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.agnasabah.nama)                
                worksheet.write_datetime(row, col + 3 , t.tanggal,date_format)
                worksheet.write(row, col + 4 , t.jw_all())
                worksheet.write_datetime(row, col + 5, t.jatuhtempo, date_format)
                worksheet.write_string(row, col + 6, t.get_jenis_transaksi_display())
                worksheet.write_string(row, col + 7, t.get_jns_gu_display())
                worksheet.write_number(row, col + 8, t.nilai, money_format)
                worksheet.write_number(row, col + 9, t.jasa_all(), money_format)
                worksheet.write_number(row, col + 10, t.adm_all(), money_format)
                worksheet.write_number(row, col + 11, t.beasimpan_all(), money_format)
                worksheet.write_string(row, col + 12, t.sts_trans_excel())
                row += 1

            worksheet.write(row,4, 'Total', bold)    
            worksheet.write(row,8, a, money_format)
            worksheet.write(row,9, c, money_format)
            worksheet.write(row,10, d, money_format)
            worksheet.write(row,11, e, money_format)
            workbook.close()
            output.seek(0)
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Laporan_all_cair.xlsx"
            return response
    else:
        variables = RequestContext(request, {'form': form})
        return render_to_response('manop/laporan/data_pencairan_all.html', variables)

@login_required
def pencairan_gerai_saja(request):
    akad= AkadGadai.objects.all()
    start_date = None
    end_date = None
    form = SearchForm()
    all = []
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET :
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            tb = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(kepalagerai__status = 1).exclude(jns_gu=('1')).order_by('gerai')
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template='manop/laporan/rekaphari_pencairan.html'
            variable = RequestContext(request,{'tes':tb,
            'form':form,'id_cabang':id_cabang,'start_date':start_date,'end_date':end_date,'start_date':start_date,
            'end_date':end_date,'nilai': sum([b.nilai for b in tb ]),'jasa': sum([b.jasa_all() for b in tb ]),
            'adm': sum([b.adm_all() for b in tb ]),'simpan': sum([b.beasimpan_all() for b in tb ]),
            'bersih' : sum([b.jumlah_biaya for b in tb ]),})
            return render_to_response(template,variable)
        else:
            tb = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(gerai__kode_cabang = id_cabang).exclude(jns_gu=('1')).filter(kepalagerai__status = 1)
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template='manop/laporan/rekaphari_pencairan.html'
            variable = RequestContext(request,{'tes':tb,'form':form,'id_cabang':id_cabang,'start_date':start_date,
            'end_date':end_date,'nilai': sum([b.nilai for b in tb ]),'jasa': sum([b.jasa_all() for b in tb ]),
            'adm': sum([b.adm_all() for b in tb ]),'simpan': sum([b.beasimpan_all() for b in tb ]),
            'bersih' : sum([b.jumlah_biaya for b in tb ]),})
            return render_to_response(template,variable)
    
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            tb = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(kepalagerai__status = 1).exclude(jns_gu=('1')).order_by('gerai')
            template1= 'manop/laporan/cetak_rekaphari_pencairan.html'
            variable = RequestContext(request,{'tes':tb,'form':form,'start_date':start_date,'end_date':end_date,
            'id_cabang':id_cabang,'nilai': sum([b.nilai for b in tb ]),'jasa': sum([b.jasa_all() for b in tb ]),
            'adm': sum([b.adm_all() for b in tb ]),'simpan': sum([b.beasimpan_all() for b in tb ]),
            'bersih' : sum([b.jumlah_biaya for b in tb ]),})
            return render_to_response(template1,variable)
        else:
            tb = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(gerai__kode_cabang = id_cabang).exclude(jns_gu=('1')).filter(kepalagerai__status = 1)
            template1= 'manop/laporan/cetak_rekaphari_pencairan.html'
            variable = RequestContext(request,{'tes':tb,'form':form,'id_cabang':id_cabang,
            'start_date':start_date,'end_date':end_date,'nilai': sum([b.nilai for b in tb ]),
            'jasa': sum([b.jasa_all() for b in tb ]),'adm': sum([b.adm_all() for b in tb ]),
            'simpan': sum([b.beasimpan_all() for b in tb ]),'bersih' : sum([b.jumlah_biaya for b in tb ]),})
            return render_to_response(template1,variable)

    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']         
        if id_cabang == '500':
            tb = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(kepalagerai__status = 1).exclude(jns_gu=('1')).order_by('gerai')
            a = sum([b.nilai for b in tb ])
            c = sum([b.jasa_all() for b in tb ]) 
            d = sum([b.adm_all() for b in tb ]) 
            e = sum([b.beasimpan_all() for b in tb ]) 
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
            worksheet.set_column(10, 10, 10)
            worksheet.set_column(11, 11, 10)
            worksheet.set_column(12, 12, 10)
            worksheet.set_column(13, 13, 10)
        
            worksheet.merge_range('A1:L1', 'LAPORAN PENCAIRAN GABUNGAN', merge_format1)
            worksheet.merge_range('A2:L2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama', merge_format)
            worksheet.merge_range('D4:D5', 'Tgl Akad', merge_format)
            worksheet.merge_range('E4:E5', 'Jw', merge_format)
            worksheet.merge_range('F4:F5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('G4:G5', 'Jenis', merge_format)
            worksheet.merge_range('H4:H5', 'SK', merge_format)
            worksheet.merge_range('I4:I5', 'Plafon', merge_format)
            worksheet.merge_range('J4:L4', 'Pendapatan', merge_format)
            worksheet.write('J5', 'Jasa',  bold1)
            worksheet.write('K5', 'Adm', bold1)
            worksheet.write('L5', 'Bea Simpan', bold1)
            row = 5
            col = 0
            for t in tb:
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.agnasabah.nama)                
                worksheet.write_datetime(row, col + 3 , t.tanggal,date_format)
                worksheet.write(row, col + 4 , t.jw_all())
                worksheet.write_datetime(row, col + 5, t.jatuhtempo, date_format)
                worksheet.write_string(row, col + 6, t.get_jenis_transaksi_display())
                worksheet.write_string(row, col + 7, t.get_jns_gu_display())
                worksheet.write_number(row, col + 8, t.nilai, money_format)
                worksheet.write_number(row, col + 9, t.jasa_all(), money_format)
                worksheet.write_number(row, col + 10, t.adm_all(), money_format)
                worksheet.write_number(row, col + 11, t.biayasimpan, money_format)
                row += 1

            worksheet.write(row,4, 'Total', bold)    
            worksheet.write(row,8, a, money_format)
            worksheet.write(row, 9, c, money_format)
            worksheet.write(row, 10, d, money_format)
            worksheet.write(row, 11, e, money_format)
        
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Laporan_Pencairan.xlsx"
            return response
        else:
            tb = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(gerai__kode_cabang = id_cabang).exclude(jns_gu=('1')).filter(kepalagerai__status = 1)
            a = sum([b.nilai for b in tb ])
            c = sum([b.jasa_all() for b in tb ]) 
            d = sum([b.adm_all() for b in tb ]) 
            e = sum([b.beasimpan_all() for b in tb ]) 
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
            worksheet.set_column(10, 10, 10)
            worksheet.set_column(11, 11, 10)
            worksheet.set_column(12, 12, 10)
            worksheet.set_column(13, 13, 10)
        
            worksheet.merge_range('A1:L1', 'LAPORAN PENCAIRAN ', merge_format1)
            worksheet.merge_range('A2:L2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama', merge_format)
            worksheet.merge_range('D4:D5', 'Tgl Akad', merge_format)
            worksheet.merge_range('E4:E5', 'Jw', merge_format)
            worksheet.merge_range('F4:F5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('G4:G5', 'Jenis', merge_format)
            worksheet.merge_range('H4:H5', 'SK', merge_format)
            worksheet.merge_range('I4:I5', 'Plafon', merge_format)
            worksheet.merge_range('J4:L4', 'Pendapatan', merge_format)
            worksheet.write('J5', 'Jasa',  bold1)
            worksheet.write('K5', 'Adm', bold1)
            worksheet.write('L5', 'Bea Simpan', bold1)
            row = 5
            col = 0
            for t in tb:
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.agnasabah.nama)                
                worksheet.write_datetime(row, col + 3 , t.tanggal,date_format)
                worksheet.write(row, col + 4 , t.jw_all())
                worksheet.write_datetime(row, col + 5, t.jatuhtempo, date_format)
                worksheet.write_string(row, col + 6, t.get_jenis_transaksi_display())
                worksheet.write_string(row, col + 7, t.get_jns_gu_display())
                worksheet.write_number(row, col + 8, t.nilai, money_format)
                worksheet.write_number(row, col + 9, t.jasa_all(), money_format)
                worksheet.write_number(row, col + 10, t.adm_all(), money_format)
                worksheet.write_number(row, col + 11, t.beasimpan_all(), money_format)
                row += 1

            worksheet.write(row,4, 'Total', bold)    
            worksheet.write(row,8, a, money_format)
            worksheet.write(row,9, c, money_format)
            worksheet.write(row,10, d, money_format)
            worksheet.write(row,11, e, money_format)
            workbook.close()
            output.seek(0)
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Laporan_Pencairan.xlsx"
            return response
    else:
        variables = RequestContext(request, {'form': form})
        return render_to_response('manop/laporan/rekaphari_pencairan.html', variables)
'''
@login_required

def rekap_noa_baru(request):
    form = SearchForm()
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET :
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            tb = Nasabah.objects.filter(mdate__range =(start_date,end_date))
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template='manop/baranggerai/rekap_noa_baru.html'
            variable = RequestContext(request,{'tes':tb,'form':form,'nilai':sum([b.nilai_plafon for b in tb ]),
            'form':form,'id_cabang':id_cabang,'start_date':start_date,'end_date':end_date})
            return render_to_response(template,variable)
        else:
            tb = Nasabah.objects.filter(mdate__range =(start_date,end_date)).filter(akadgadai__gerai__kode_cabang = id_cabang)
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template='manop/baranggerai/rekap_noa_baru.html'
            variable = RequestContext(request,{'tes':tb,'nilai':sum([b.nilai_plafon for b in tb ]),
            'form':form,'id_cabang':id_cabang,'start_date':start_date,'end_date':end_date,})            
            return render_to_response(template,variable)
    
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            tb = Nasabah.objects.filter(mdate__range =(start_date,end_date))
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template1= 'manop/baranggerai/cetak_rekap_noa_baru.html'
            variable = RequestContext(request,{'tes':tb,'form':form,
            'form':form,'id_cabang':id_cabang,'start_date':start_date,'end_date':end_date,'nilai': sum([b.nilai_plafon for b in tb ])})
            return render_to_response(template1,variable)
        else:
            tb = Nasabah.objects.filter(mdate__range =(start_date,end_date)).filter(akadgadai__gerai__kode_cabang = id_cabang)
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template1= 'manop/baranggerai/cetak_rekap_noa_baru.html'
            variable = RequestContext(request,{'tes':tb,'form':form,'id_cabang':id_cabang,
            'start_date':start_date,'end_date':end_date,'nilai': sum([b.nilai_plafon for b in tb ]),})
            return render_to_response(template1,variable)

    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']         
        if id_cabang == '500':
            tb = Nasabah.objects.filter(mdate__range =(start_date,end_date))
            a = sum([b.nilai_plafon for b in tb ])
            e = 0 
            f = start_date
            g = end_date
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': 0})
            bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            money_format = workbook.add_format({'num_format': '#,##0'})
            date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
            merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            merge_format1 = workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter',})
        
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
            worksheet.set_column(10, 10, 10)
        
            worksheet.merge_range('A1:H1', 'DAFTAR NASABAH BARU PERGERAI', merge_format1)
            worksheet.merge_range('A2:H2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            
            worksheet.merge_range('A4:A5', 'Nonas ', merge_format)
            worksheet.merge_range('B4:B5', 'Norek', merge_format)
            worksheet.merge_range('C4:C5', 'Gerai', merge_format)
            worksheet.merge_range('D4:D5', 'Nasabah', merge_format)
            worksheet.merge_range('E4:E5', 'Barang', merge_format)
            worksheet.merge_range('F4:F5', 'Tgl Input', merge_format)
            worksheet.merge_range('G4:G5', 'Tgl Akad', merge_format)
            worksheet.merge_range('H4:H5', 'Nilai', merge_format)
            

            row = 5
            col = 0
            for t in tb:
                input = t.mdate
                naive = input.replace(tzinfo=None)
                worksheet.write_string(row, col , t.nomor_nasabah() )
                worksheet.write_string(row, col +1 , t.nomor() )
                worksheet.write_string(row, col + 2 , t.akad_gadai.gerai.nama_cabang)
                worksheet.write_string(row, col + 3 , t.nama)
                worksheet.write_string(row, col + 4 , t.akad_gadai.barang.type)
                worksheet.write_datetime(row, col + 5 , naive, date_format )
                worksheet.write_datetime(row, col + 6, t.akad_gadai.tanggal, date_format)
                worksheet.write_number(row, col + 7, t.akad_gadai.nilai, money_format)                
                row += 1
            
            worksheet.write(row,4, 'Total', bold)
            worksheet.write(row,7, a, money_format)
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=NoaBaru.xlsx"
            return response
        else:
            tb= Nasabah.objects.filter(mdate__range =(start_date,end_date)).filter(akadgadai__gerai__kode_cabang = id_cabang)
            a = sum([b.nilai_plafon for b in tb ])
            f = start_date
            g = end_date
            #h = nacab.nama_cabang
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': 0})
            bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            money_format = workbook.add_format({'num_format': '#,##0'})
            format5 = workbook.add_format({'num_format': 'dd/mm/yy hh:mm'})
            date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
            merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            merge_format1 = workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter',})
            worksheet.set_column(0, 0, 10)
            worksheet.set_column(1, 1, 18)
            worksheet.set_column(2, 2, 11)
            worksheet.set_column(3, 3, 12)
            worksheet.set_column(4, 4, 10)
            worksheet.set_column(5, 5, 10)
            worksheet.set_column(6, 6, 10)
            worksheet.set_column(7, 7, 10)
            worksheet.set_column(8, 8, 10)
            worksheet.set_column(9, 9, 10)
            worksheet.set_column(10, 10, 10)

            worksheet.merge_range('A1:H1', 'DAFTAR NASABAH BARU PERGERAI', merge_format1)
            worksheet.merge_range('A2:H2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            
            worksheet.merge_range('A4:A5', 'Nonas ', merge_format)
            worksheet.merge_range('B4:B5', 'Norek', merge_format)
            worksheet.merge_range('C4:C5', 'Gerai', merge_format)
            worksheet.merge_range('D4:D5', 'Nasabah', merge_format)
            worksheet.merge_range('E4:E5', 'Barang', merge_format)
            worksheet.merge_range('F4:F5', 'Tgl Input', merge_format)
            worksheet.merge_range('G4:G5', 'Tgl Akad', merge_format)
            worksheet.merge_range('H4:H5', 'Nilai', merge_format)


            row = 5
            col = 0
            for t in tb:
                input = t.mdate
                naive = input.replace(tzinfo=None)
                worksheet.write_string(row, col , t.nomor_nasabah() )
                worksheet.write_string(row, col +1 , t.nomor() )
                worksheet.write_string(row, col + 2 , t.akad_gadai.gerai.nama_cabang)
                worksheet.write_string(row, col + 3 , t.nama)
                worksheet.write_string(row, col + 4 , t.akad_gadai.barang.type)
                worksheet.write_datetime(row, col + 5 , naive, date_format )
                worksheet.write_datetime(row, col + 6, t.akad_gadai.tanggal, date_format)
                worksheet.write_number(row, col + 7, t.akad_gadai.nilai, money_format)
                row += 1
            worksheet.write(row,4, 'Total', bold)
            worksheet.write(row,7, a, money_format)
            

            workbook.close()
            output.seek(0)
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Noabaru.xlsx"
            return response

    else:
        variables = RequestContext(request, {'form': form})
        return render_to_response('manop/baranggerai/rekap_noa_baru.html', variables)
'''

@login_required
def rekap_noa_baru(request):
    form = SearchForm()
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET :
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            tb1 = AkadGadai.objects.filter(tanggal__range =(start_date,end_date)).order_by('agnasabah__nama')
            tb = ([ o for o in tb1 if o.date_date_cuy()==True])
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template='manop/baranggerai/rekap_noa_baru.html'
            variable = RequestContext(request,{'tes':tb,'form':form,'nilai':sum([b.nilai for b in tb ]),
            'form':form,'id_cabang':id_cabang,'start_date':start_date,'end_date':end_date})
            return render_to_response(template,variable)
        else:
            #tb = Nasabah.objects.filter(mdate__range =(start_date,end_date)).filter(akadgadai__gerai__kode_cabang = id_cabang)
            tb1 = AkadGadai.objects.filter(tanggal__range =(start_date,end_date)).filter(gerai__kode_cabang = id_cabang).order_by('agnasabah__nama')
            tb = ([ o for o in tb1 if o.date_date_cuy()==True])
 
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template='manop/baranggerai/rekap_noa_baru.html'
            variable = RequestContext(request,{'tes':tb,'nilai':sum([b.nilai for b in tb ]),
            'form':form,'id_cabang':id_cabang,'start_date':start_date,'end_date':end_date,})            
            return render_to_response(template,variable)
    
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            tb1 = AkadGadai.objects.filter(tanggal__range =(start_date,end_date)).order_by('agnasabah__nama')
            tb = ([ o for o in tb1 if o.date_date_cuy()==True])
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template1= 'manop/baranggerai/cetak_rekap_noa_baru.html'
            variable = RequestContext(request,{'tes':tb,'form':form,
            'form':form,'id_cabang':id_cabang,'start_date':start_date,'end_date':end_date,'nilai': sum([b.nilai for b in tb ])})
            return render_to_response(template1,variable)
        else:
            tb1 = AkadGadai.objects.filter(tanggal__range =(start_date,end_date)).filter(gerai__kode_cabang = id_cabang).order_by('agnasabah__nama')
            tb = ([ o for o in tb1 if o.date_date_cuy()==True])
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template1= 'manop/baranggerai/cetak_rekap_noa_baru.html'
            variable = RequestContext(request,{'tes':tb,'form':form,'id_cabang':id_cabang,
            'start_date':start_date,'end_date':end_date,'nilai': sum([b.nilai for b in tb ]),})
            return render_to_response(template1,variable)

    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']         
        if id_cabang == '500':
            tb1 = AkadGadai.objects.filter(tanggal__range =(start_date,end_date)).order_by('agnasabah__nama')
            tb = ([ o for o in tb1 if o.date_date_cuy()==True])
            a = sum([b.nilai for b in tb ])
            e = 0 
            f = start_date
            g = end_date
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': 0})
            bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            money_format = workbook.add_format({'num_format': '#,##0'})
            date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
            merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            merge_format1 = workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter',})
        
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
            worksheet.set_column(10, 10, 10)
        
            worksheet.merge_range('A1:H1', 'DAFTAR NASABAH BARU PERGERAI', merge_format1)
            worksheet.merge_range('A2:H2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            
            worksheet.merge_range('A4:A5', 'Nonas ', merge_format)
            worksheet.merge_range('B4:B5', 'Norek', merge_format)
            worksheet.merge_range('C4:C5', 'Gerai', merge_format)
            worksheet.merge_range('D4:D5', 'Nasabah', merge_format)
            worksheet.merge_range('E4:E5', 'Barang', merge_format)
            worksheet.merge_range('F4:F5', 'Tgl Input', merge_format)
            worksheet.merge_range('G4:G5', 'Tgl Akad', merge_format)
            worksheet.merge_range('H4:H5', 'Nilai', merge_format)
            

            row = 5
            col = 0
            for t in tb:
                input = t.mdate
                naive = input.replace(tzinfo=None)
                worksheet.write_string(row, col , t.nonas() )
                worksheet.write_string(row, col +1 , t.norek() )
                worksheet.write_string(row, col + 2 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 3 , t.agnasabah.nama)
                worksheet.write_string(row, col + 4 , t.barang.type)
                worksheet.write_datetime(row, col + 5 , t.agnasabah.mdate.date(), date_format )
                worksheet.write_datetime(row, col + 6, t.tanggal, date_format)
                worksheet.write_number(row, col + 7, t.nilai, money_format)                
                row += 1
            
            worksheet.write(row,4, 'Total', bold)
            worksheet.write(row,7, a, money_format)
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=NoaBaru.xlsx"
            return response
        else:
            tb1 = AkadGadai.objects.filter(tanggal__range =(start_date,end_date)).filter(gerai__kode_cabang = id_cabang).order_by('agnasabah__nama')
            tb = ([ o for o in tb1 if o.date_date_cuy()==True])
            a = sum([b.nilai for b in tb ])
            f = start_date
            g = end_date
            #h = nacab.nama_cabang
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': 0})
            bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            money_format = workbook.add_format({'num_format': '#,##0'})
            format5 = workbook.add_format({'num_format': 'dd/mm/yy hh:mm'})
            date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
            merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            merge_format1 = workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter',})
            worksheet.set_column(0, 0, 10)
            worksheet.set_column(1, 1, 18)
            worksheet.set_column(2, 2, 11)
            worksheet.set_column(3, 3, 12)
            worksheet.set_column(4, 4, 10)
            worksheet.set_column(5, 5, 10)
            worksheet.set_column(6, 6, 10)
            worksheet.set_column(7, 7, 10)
            worksheet.set_column(8, 8, 10)
            worksheet.set_column(9, 9, 10)
            worksheet.set_column(10, 10, 10)

            worksheet.merge_range('A1:H1', 'DAFTAR NASABAH BARU PERGERAI', merge_format1)
            worksheet.merge_range('A2:H2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            
            worksheet.merge_range('A4:A5', 'Nonas ', merge_format)
            worksheet.merge_range('B4:B5', 'Norek', merge_format)
            worksheet.merge_range('C4:C5', 'Gerai', merge_format)
            worksheet.merge_range('D4:D5', 'Nasabah', merge_format)
            worksheet.merge_range('E4:E5', 'Barang', merge_format)
            worksheet.merge_range('F4:F5', 'Tgl Input', merge_format)
            worksheet.merge_range('G4:G5', 'Tgl Akad', merge_format)
            worksheet.merge_range('H4:H5', 'Nilai', merge_format)


            row = 5
            col = 0
            for t in tb:
                input = t.mdate
                naive = input.replace(tzinfo=None)
                worksheet.write_string(row, col , t.nonas() )
                worksheet.write_string(row, col +1 , t.norek() )
                worksheet.write_string(row, col + 2 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 3 , t.agnasabah.nama)
                worksheet.write_string(row, col + 4 , t.barang.type)
                worksheet.write_datetime(row, col + 5 , t.agnasabah.mdate.date(), date_format )
                worksheet.write_datetime(row, col + 6, t.tanggal, date_format)
                worksheet.write_number(row, col + 7, t.nilai, money_format)
                row += 1
            worksheet.write(row,4, 'Total', bold)
            worksheet.write(row,7, a, money_format)
            

            workbook.close()
            output.seek(0)
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Noabaru.xlsx"
            return response

    else:
        variables = RequestContext(request, {'form': form})
        return render_to_response('manop/baranggerai/rekap_noa_baru.html', variables)
def edit_sts_kw(request,object_id):
    sekarang = datetime.date.today()
    akad = AkadGadai.objects.get(id=object_id)
    form = BukaStatusForm(initial={'buka_sts_tdr': 1,})

    template = 'manop/buka_status.html'
    #template = 'kasir/kasir_pelunasan.html'
    variable = RequestContext(request, {'akad': akad,'form':form,})
    return render_to_response(template,variable)

def input_edit_sts_kw(request, object_id):
    user = request.user
    akad = AkadGadai.objects.get(id=object_id)
    if request.method == 'POST':
        f = BukaStatusForm(request.POST)
        if f.is_valid():
            buka_status_kw = f.cleaned_data['buka_status_kw']
            buka_status_label = f.cleaned_data['buka_status_label']
            buka_kondisi_barang = f.cleaned_data['buka_kondisi_barang']
            buka_sts_tdr = f.cleaned_data['buka_sts_tdr']


            akad.status_kw  = buka_status_kw
            akad.status_label = buka_status_label 
            akad.kondisi_barang = buka_kondisi_barang
            akad.sts_tdr = buka_sts_tdr
            akad.save()
            messages.add_message(request, messages.INFO,'### DATA Telah Dibuka Kembali ###.')
            return HttpResponseRedirect(akad.get_absolute_url())
        else:
            variables = RequestContext(request,{ 'form': form})
            return render_to_response('manop/buka_status.html', variables)
    else:
        form  = BukaStatusForm()
    variables = RequestContext(request, {'form': form,'akad':akad,})
    return render_to_response('manop/buka_status.html', variables)

'''
@login_required
@user_passes_test(lambda u: u.groups.filter(name='KEUANGAN2'))
def menu_penjualan_ayda(request):
    akad = AkadGadai.objects.all()
    sekarang = datetime.date.today()
    rekening = None
    if 'submit' in request.GET:
        rekening=request.GET['rekening']
        print rekening
        try :
            ag=AkadGadai.objects.get(id=int(rekening))            
            #print lapur
            if ag.status_transaksi == u'6' or ag.lunas == u'' :
                lapur = ag.lapur_set.all()
                form = BarangLelangForm(initial={'aglelang': ag.id,'tgl_lelang': sekarang})
                form.fields['aglelang'].widget = forms.HiddenInput()
                template = 'manop/refjurnal/cari_ayda.html'
                variable = RequestContext(request,{'rekening':rekening,'ag':ag,'lapur':lapur,'form':form})
                return render_to_response(template,variable)
            elif ag.status_transaksi != u'6' and ag.lunas != None:
                messages.add_message(request, messages.INFO,'Nasabah sudah lunas Atau Status Barang AYDA')
                return HttpResponseRedirect("/manop/menu_penjualan_ayda/")
        except:
            messages.add_message(request, messages.INFO,'No rekening tidak ditemukan.')
            return HttpResponseRedirect("/manop/menu_penjualan_ayda/")
    else:
        template='manop/refjurnal/cari_ayda.html'
        variable = RequestContext(request,{'akad': akad,'rekening':rekening})
        return render_to_response(template,variable)
'''
@login_required
@user_passes_test(lambda u: u.groups.filter(name='KEUANGAN2'))
def menu_penjualan_ayda_esekusi(request,object_id):
    ag=AkadGadai.objects.get(id=object_id)
    sekarang = datetime.date.today()
    lapur = ag.lapur_set.all()
    form = BarangLelangForm(initial={'aglelang': ag.id,'tgl_lelang': sekarang})
    form.fields['aglelang'].widget = forms.HiddenInput()
    template = 'manop/refjurnal/cari_ayda.html'
    variable = RequestContext(request,{'ag':ag,'lapur':lapur,'form':form})
    return render_to_response(template,variable)
    
@login_required
@user_passes_test(lambda u: u.groups.filter(name='KEUANGAN2'))
def menu_penjualan_ayda(request):
    form =SearchForm()
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET :
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            tb = Lapur.objects.filter(status = u'1').filter(tanggal__range=(start_date,end_date))
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template='manop/refjurnal/cari_ayda_show.html'
            variable = RequestContext(request,{'tes':tb,'nilai':sum([b.nilai for b in tb ]),
            'form':form,'id_cabang':id_cabang,'start_date':start_date,'end_date':end_date})
            return render_to_response(template,variable)
        else:
            tb = Lapur.objects.filter(status = u'1').filter(aglapur__gerai__kode_cabang = id_cabang).filter(tanggal__range=(start_date,end_date))
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template='manop/refjurnal/cari_ayda_show.html'
            variable = RequestContext(request,{'tes':tb,'nilai':sum([b.nilai for b in tb ]),
            'form':form,'id_cabang':id_cabang,'start_date':start_date,'end_date':end_date,})            
            return render_to_response(template,variable)
    else:
        variables = RequestContext(request, {'form': form})
        return render_to_response('manop/refjurnal/cari_ayda_show.html', variables)

def edit_manage_user(request,object_id):
    post = get_object_or_404(User, id=object_id)
    if request.method == "POST":
        form = UserForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            messages.add_message(request, messages.INFO,"Update User Berhasil")
            return HttpResponseRedirect('/manop/manage_user/')
    else:
        form = UserForm(instance=post)
    return render(request, 'manop/manage/edit_manage_user.html', {'form': form,'id':object_id})

def manage_user(request):
    sekarang = datetime.date.today()
    gu = User.objects.all()
    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,"Input User Berhasil")
            return HttpResponseRedirect('/manop/manage_user/')
    else:
        form = UserForm()
        print form
    template = 'manop/manage/manage_user.html'
    variable = RequestContext(request, {'form': form,'gu':gu})
    return render_to_response(template,variable)


def edit_manage_userprofile(request,object_id):
    post = get_object_or_404(UserProfile, id=object_id)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            messages.add_message(request, messages.INFO,"Update UserProfile Berhasil")
            return HttpResponseRedirect('/manop/manage_userprofile/')
    else:
        form = UserProfileForm(instance=post)
    return render(request, 'manop/manage/edit_manage_userprofile.html', {'form': form,'id':object_id})

def manage_userprofile(request):
    sekarang = datetime.date.today()
    gu = UserProfile.objects.all()
    if request.POST:
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,"Input UserProfile Berhasil")
            return HttpResponseRedirect('/manop/manage_userprofile/')
    else:
        form = UserProfileForm()
        print form
    template = 'manop/manage/manage_userprofile.html'
    variable = RequestContext(request, {'form': form,'gu':gu})
    return render_to_response(template,variable)


def edit_manage_gerai(request,object_id):
    post = get_object_or_404(Tbl_Cabang, id=object_id)
    if request.method == "POST":
        form = GeraiForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            messages.add_message(request, messages.INFO,"Update Gerai Berhasil")
            return HttpResponseRedirect('/manop/manage_gerai/')
    else:
        form = GeraiForm(instance=post)
    return render(request, 'manop/manage/edit_manage_gerai.html', {'form': form,'id':object_id})

def manage_gerai(request):
    sekarang = datetime.date.today()
    gu = Tbl_Cabang.objects.all()
    if request.POST:
        form = GeraiForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,"Input Gerai Berhasil")
            return HttpResponseRedirect('/manop/manage_gerai/')
    else:
        form = GeraiForm()
        print form
    template = 'manop/manage/manage_gerai.html'
    variable = RequestContext(request, {'form': form,'gu':gu})
    return render_to_response(template,variable)

def cari(request):
    akad = AkadGadai.objects.all()
    template='manop/refjurnal/cari_norek.html'
    variable = RequestContext(request,{'akad': akad})
    return render_to_response(template,variable)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='manop'))
def cari_jurnal(request):
    rekening=request.GET['rekening']
    try:
        akad=AkadGadai.objects.get(id=int(rekening))
        return HttpResponseRedirect("/manop/%s/jurnal_ref/" % akad.id)
    except:
        messages.add_message(request, messages.INFO,'No rekening tidak ditemukan.')
        return HttpResponseRedirect("/")

def jurnal_ref(request, object_id):
    sekarang = datetime.date.today()
    akad = AkadGadai.objects.get(id=object_id)
    id_akad = akad.id
    jurnal= Jurnal.objects.filter(object_id = id_akad)
    jurnal.delete()
    template = 'manop/refjurnal/manop_show.html'
    variable = RequestContext(request, {'ag': akad})
    return render_to_response(template,variable)

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('manop','asmanpjb')))
def otorisasi_pelunasan(request):
    manop = ManopPelunasan.objects.filter(status='1')
    template = 'manop/otorisasi_pelunasan.html'
    variables = RequestContext(request, {'manop': manop})
    return render_to_response(template, variables)

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('manop','asmanpjb')))
def edit_view(request, object_id):
    user = request.user
    sekarang = datetime.date.today()
    manop = get_object_or_404(ManopPelunasan, id=object_id)
    cc = manop.pelunasan.id
    akad = AkadGadai.objects.get(pk=cc)
    form = MyForm(request.POST or None, instance=manop,
        initial={'tanggal': sekarang,'nilai': int(manop.pelunasan.nilai_lunas),
        'terlambat':int(manop.pelunasan.terlambat) +int(manop.pelunasan.terlambat_kendaraan),
        'denda':int(manop.pelunasan.denda_lunas) + int(manop.pelunasan.denda_kendaraan_lunas),
        'bea_jasa':int(manop.pelunasan.jasa_lunas)+ int(manop.pelunasan.jasa_kendaraan_lunas)})
    if form.is_valid():
        nilai = form.cleaned_data['nilai']
        denda = form.cleaned_data['denda']
        bea_jasa = form.cleaned_data['bea_jasa']
        terlambat = form.cleaned_data['terlambat']
        form.save()
        if manop.pelunasan.jenis_transaksi == '1':
            akad.nilai_lunas = nilai
            akad.jasa_lunas = bea_jasa
            akad.terlambat = terlambat
            akad.denda_lunas = denda
            akad.status_oto_plns = 3
            akad.save()
            messages.add_message(request, messages.INFO,'### Pelunasan Berhasil 1 ###')
        else:
            akad.nilai_lunas = nilai
            akad.jasa_kendaraan_lunas = bea_jasa
            akad.terlambat_kendaraaan = terlambat
            akad.denda_kendaraan_lunas = denda
            akad.status_oto_plns = 3
            akad.save()
            messages.add_message(request, messages.INFO,'### PELUNASAN BERHASIL 2###')
        return HttpResponseRedirect('/manop/otorisasi_pelunasan/')
    variables = RequestContext(request, {'ag': manop, 'form': form})
    return render_to_response('manop/edit_template.html', variables)
###PINDAHAN JURNAL
###1 & 4 & 6 & 7###JURNAL ANGGOTA JENIS ELEKTRONIK NILAI <= NILAI_GU
def jurnal_pelunasan_barang_sama_anggota(akad, user):
    D = decimal.Decimal
    sekarang = datetime.date.today()
    sama = AdmGadaiUlanMapper.objects.get(item='1')
    a_titipan_pencairan = sama.coa_1
    a_titipan_pelunasan =sama.coa_5
    a_anggota = sama.coa
    a_pendapatan_denda = sama.coa_6
    a_pendapatan_jasa = sama.coa_2

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = sekarang, #akad.tanggal
        nobukti=akad.norek(),cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        debet =round(D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) ),kredit =  0,
        id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pelunasan,
        debet =((D(akad.nilai_gu)) + D((akad.denda_gu)) + D((akad.jasa_gu))) - (D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) ),kredit = 0,
        id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu),debet =0  ,id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_denda,
        debet = 0,kredit = D(float(akad.denda_gu)),id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_jasa,
        debet = 0,kredit = D(float(akad.jasa_gu)),id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_barang_sama_anggota_nondenda(akad, user):
    D = decimal.Decimal
    sekarang = datetime.date.today()
    sama = AdmGadaiUlangMapper.objects.get(item='9')
    a_titipan_pencairan = sama.coa_1
    a_titipan_pelunasan = sama.coa_5
    a_anggota = sama.coa
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = sekarang, #akad.tanggal,
        nobukti=akad.norek(),cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        debet =round(D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) ),kredit =  0,
        id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pelunasan,
        debet =((D(akad.nilai_gu)) + D((akad.denda_gu)) + D((akad.jasa_gu))) - (D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) ),kredit = 0,
        id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu),debet =0  ,id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_barang_sama_anggota_lebih(akad, user):
    D = decimal.Decimal
    sekarang = datetime.date.today()
    sama = AdmGadaiUlangMapper.objects.get(item='2')
    a_titipan_pencairan = sama.coa_1
    a_anggota = sama.coa
    a_pendapatan_denda = sama.coa_6
    a_pendapatan_jasa = sama.coa_2

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = sekarang, #akad.tanggal,
        nobukti=akad.norek(),cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        debet = D(akad.nilai_gu) + D(float(akad.denda_gu)) + D(float(akad.jasa_gu)),kredit = 0,
        id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu) ,debet =0  ,id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_denda,
        debet = 0,kredit = D(float(akad.denda_gu)),id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_jasa,
        debet = 0,kredit = D(float(akad.jasa_gu)),id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_barang_sama_anggota_lebih_nondenda(akad, user):
    D = decimal.Decimal 
    sekarang = datetime.date.today()
    sama = AdmGadaiUlangMapper.objects.get(item='10')
    a_titipan_pencairan = sama.coa_1
    a_anggota = sama.coa
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = sekarang, #akad.tanggal,
        nobukti=akad.norek(),cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        debet = D(akad.nilai_gu) + D(float(akad.denda_gu)) + D(float(akad.jasa_gu)),kredit = 0,
        id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu) ,debet =0  ,id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_barang_sama_non_anggota(akad, user):
    D = decimal.Decimal
    sekarang = datetime.date.today()
    sama = AdmGadaiUlangMapper.objects.get(item='3')
    a_titipan_pencairan = sama.coa_1
    a_titipan_pelunasan = sama.coa_5
    a_anggota = sama.coa
    a_pendapatan_denda = sama.coa_6
    a_pendapatan_jasa = sama.coa_2

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = sekarang, #akad.tanggal,
        nobukti=akad.norek(),cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        #debet =round(D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) ),kredit =  0, ASLI
        debet =round(D(akad.nilai) - D(akad.jasa_all())- D(akad.beasimpan_all())- D(akad.adm_all())-D(akad.bea_materai) ),kredit =  0,
        id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pelunasan,
        #debet =((D(akad.nilai_gu)) + D((akad.denda_gu)) + D((akad.jasa_gu))) - (D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())\
        #- D(akad.beasimpan_all()) - D(akad.bea_materai)),kredit = 0, ASLI
        debet =((D(akad.nilai_gu)) + D((akad.denda_gu)) + D((akad.jasa_gu)) + D(akad.adm_all())) - (D(akad.nilai) - D(akad.jasa_all())\
        - D(akad.beasimpan_all()) - D(akad.bea_materai)),
        kredit = 0,id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu),debet = 0 ,id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_denda,
        debet = 0,kredit = D(float(akad.denda_gu)),id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_jasa,
        debet = 0,kredit = D(float(akad.jasa_gu)),id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_barang_sama_non_anggota_nondenda(akad, user):
    D = decimal.Decimal
    sekarang = datetime.date.today()
    sama = AdmGadaiUlangMapper.objects.get(item='11')
    a_titipan_pencairan = sama.coa_1
    a_titipan_pelunasan = sama.coa_5
    a_anggota = sama.coa

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = sekarang, #akad.tanggal,
        nobukti=akad.norek(),cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        #debet =round(D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) ),kredit =  0, ASLI
        debet =round(D(akad.nilai) - D(akad.jasa_all())- D(akad.beasimpan_all())- D(akad.adm_all())-D(akad.bea_materai) ),kredit =  0,
        id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pelunasan,
        #debet =((D(akad.nilai_gu)) + D((akad.denda_gu)) + D((akad.jasa_gu))) - (D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())\
        #- D(akad.beasimpan_all()) - D(akad.bea_materai)),kredit = 0, ASLI
        debet =((D(akad.nilai_gu)) + D((akad.denda_gu)) + D((akad.jasa_gu)) + D(akad.adm_all())) - (D(akad.nilai) - D(akad.jasa_all())\
        - D(akad.beasimpan_all()) - D(akad.bea_materai)),
        kredit = 0,id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu),debet = 0 ,id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_barang_sama_non_anggota_lebih(akad, user):
    D = decimal.Decimal
    sekarang = datetime.date.today()
    sama = AdmGadaiUlangMapper.objects.get(item='4')
    a_titipan_pencairan = sama.coa_1
    a_anggota = sama.coa
    a_pendapatan_denda = sama.coa_6
    a_pendapatan_jasa = sama.coa_2
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = sekarang,nobukti=akad.norek(),cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        debet = D(akad.nilai_gu) + D(float(akad.denda_gu)) + D(float(akad.jasa_gu)),kredit = 0,
        id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu) ,debet =0  ,id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_denda,
        debet = 0,kredit = D(float(akad.denda_gu)),id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_jasa,
        debet = 0,kredit = D(float(akad.jasa_gu)),id_product = '4',status_jurnal ='2',tgl_trans = sekarang, #akad.tanggal,
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

def jurnal_pelunasan_barang_sama_non_anggota_lebih_nondenda(akad, user):
    D = decimal.Decimal
    sekarang = datetime.date.today()
    sama = AdmGadaiUlangMapper.objects.get(item='16')
    a_titipan_pencairan = sama.coa_1
    a_titipan_pelunasan =sama.coa_5
    a_anggota = sama.coa
    a_pendapatan_denda = sama.coa_6
    a_pendapatan_jasa = sama.coa_2

    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (akad.norek(), akad.agnasabah.nama),kode_cabang = akad.gerai.kode_cabang,
        tgl_trans = sekarang, nobukti=akad.norek(),cu=user,mu=user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pencairan,
        debet = round(D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) ),kredit =  0,
        id_product = '4',status_jurnal ='2',tgl_trans = sekarang,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_titipan_pelunasan,
        debet =((D(akad.nilai_gu)) + D((akad.denda_gu)) + D((akad.jasa_gu))) - (D(akad.nilai) - D(akad.adm_all()) - D(akad.jasa_all())- D(akad.beasimpan_all()) ),kredit = 0,
        id_product = '4',status_jurnal ='2',tgl_trans = sekarang,
        id_cabang =akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_anggota,
        kredit = D(akad.nilai_gu),debet =0  ,id_product = '4',status_jurnal ='2',tgl_trans = sekarang, 
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_Barang_sama"), id_coa = a_pendapatan_denda,
        debet = 0,kredit = D(float(akad.denda_gu)),id_product = '4',status_jurnal ='2',tgl_trans = sekarang, 
        id_cabang = akad.gerai.kode_cabang,id_unit= 300)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('manop','asmanpjb')))
def otorisasi_pelunasan_gu(request):
    manop = ManopPelunasanGu.objects.filter(status='1')
    template = 'manop/otorisasi_pelunasan_gu.html'
    variables = RequestContext(request, {'manop': manop})    
    return render_to_response(template, variables)

def edit_view_gu(request, object_id):
    user = request.user
    sekarang = datetime.date.today()
    manop = get_object_or_404(ManopPelunasanGu, id=object_id)
    cc = manop.gu.id
    plns = Pelunasan.objects.get(pk=cc) 
    form = MyGuForm(request.POST or None, instance=manop,
        initial={'tanggal': sekarang,'nilai': int(manop.gu.nilai),
        'denda':int(manop.gu.denda_kendaraan) + int(manop.gu.denda),
        'bea_jasa':int(manop.gu.bea_jasa)+ int(manop.gu.bea_jasa_kendaraan)})
    if form.is_valid():
        nilai = form.cleaned_data['nilai']
        denda = form.cleaned_data['denda']
        bea_jasa = form.cleaned_data['bea_jasa']
        status = form.cleaned_data['status']
        note = form.cleaned_data['note']
        #form.save()
        if manop.gu.pelunasan.jenis_transaksi == '1':
            plns.nilai = nilai
            plns.bea_jasa = bea_jasa
            plns.bea_jasa_kendaraan = 0
            plns.denda = denda
            plns.denda_kendaraan = 0            
            plns.save()
            akad = AkadGadai.objects.get(id = plns.pelunasan.id)
            akad.status_oto_akad_gu = 2
            akad.save()
            mnp = ManopPelunasanGu.objects.get(gu =plns.id)
            mnp.denda = denda
            mnp.denda_kendaraan = plns.denda_kendaraan
            mnp.bea_jasa_kendaraan = plns.denda_kendaraan
            mnp.bea_jasa = bea_jasa
            mnp.nilai =nilai
            mnp.status = status
            mnp.note = note
            mnp.cu = user
            mnp.mu = user
            mnp.save()            
            messages.add_message(request, messages.INFO,'### Pelunasan Gadai Ulang Berhasil 1 ###')
        else:
            plns.nilai = nilai
            plns.bea_jasa_kendaraan = bea_jasa
            plns.bea_jasa = 0
            plns.denda = 0
            plns.denda_kendaraan = denda
            plns.save()
            akad = AkadGadai.objects.get(id = plns.pelunasan.id)
            akad.status_oto_akad_gu = 2
            akad.save()
            mnp = ManopPelunasanGu.objects.get(gu =plns.id)
            mnp.denda = 0
            mnp.denda_kendaraan = denda
            mnp.bea_jasa_kendaraan = bea_jasa
            mnp.bea_jasa = 0
            mnp.nilai =nilai
            mnp.status = status
            mnp.note = note
            mnp.cu = user
            mnp.mu = user
            mnp.save()            
            messages.add_message(request, messages.INFO,'### PELUNASAN GADAI ULANG BERHASIL 2###')
            return HttpResponseRedirect('/manop/otorisasi_pelunasan_gu/')
       
    variables = RequestContext(request, {'ag': manop, 'form': form})
    return render_to_response('manop/edit_template_gu.html', variables)
def oto_plns_manop(request, object_id):
    ag = Pelunasan.objects.get(id=object_id)
    #pln = ag.pelunasan_set.all()
    #ps = pln[0]
    tanggal_sekarang = datetime.date.today()
    form = Verifikasi_Pelunasan_ManOpForm(initial={'tanggal': tanggal_sekarang})
    form.fields['pelunasan'].widget = forms.HiddenInput()
    form.fields['manop'].widget = forms.HiddenInput()
    
    template = 'manop/oto_plns_manop.html'
    variable = RequestContext(request, {'ag': ag,'form': form})
    return render_to_response(template,variable) 

#### IMPORT AKADGADAI ALL JURNALL #####

@login_required
@user_passes_test(lambda u: u.groups.filter(name='manop'))
def daftarpelunasan(request):
    manop = Pelunasan.objects.filter(status_pelunasan=2)
    
    template = 'manop/listpelunasan.html'
    variables = RequestContext(request, {'manop': manop})    
    return render_to_response(template, variables)

def menu_plns_manop(request, object_id):
    ag = AkadGadai.objects.get(id=object_id)
    pln = ag.pelunasan_set.all()
    ps = pln[0]
    a = datetime.date.today()
    form = Verifikasi_Pelunasan_ManOpForm(initial={'tanggal': a,'pelunasan':ps,})
    form.fields['pelunasan'].widget = forms.HiddenInput()
    form.fields['manop'].widget = forms.HiddenInput()
    
    template = 'manop/menu_pelunasan_manop.html'
    variable = RequestContext(request, {
        'ag': ag,
        'form': form})
    return render_to_response(template,variable) 

def pelunasan_manop(request, object_id):
    ag = AkadGadai.objects.get(id=object_id)
    pln = ag.pelunasan_set.all()
    ps = pln[0]
    sekarang = datetime.date.today()
    if request.method == 'POST':
        f = Verifikasi_Pelunasan_ManOpForm(request.POST)
        if f.is_valid():
            pelunasan = f.cleaned_data['pelunasan']   
            manop = f.cleaned_data['manop']   
            tanggal = f.cleaned_data['tanggal']
            status = f.cleaned_data['status']
            note = f.cleaned_data['note']
            f = ManopGadai(pelunasan=ps, tanggal=tanggal, status=status, note = note)
            f.save()
            if f.status == '1':
                ag.status_transaksi = u'1'
                ag.lunas = ps.tanggal
                ag.os_pokok = 0
                ag.save()
                ps.status_pelunasan = 1
                ps.save()
                #print ps
                jurnal_pelunasan_manop(ps, request.user)
                messages.add_message(request, messages.INFO,'### PENGAJUAN DITERIMA ###')    
            elif f.status == '2':
                a = ps
                a.delete()
                b = f
                f.delete()
                #ag.save()    
                messages.add_message(request, messages.INFO,'### PENGAJUAN DITOLAK ###')                
            return HttpResponseRedirect('/manop/daftarpelunasan/')
        else:
            variables = RequestContext(request, {'object': ag, 'form': f})
            return render_to_response('manop/menu_pelunasan_manop.html', variables)

def jurnal_pelunasan_manop(ps, user):
    D = decimal.Decimal
    a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
    a_pinjaman_anggota = get_object_or_404(Tbl_Akun, id=163L)
    a_denda = get_object_or_404(Tbl_Akun, id=442L)
    a_pdp_jasa = get_object_or_404(Tbl_Akun, id='416')
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pelunasan: NoRek: %s an: %s  ' % (ps.pelunasan.norek(), ps.pelunasan.agnasabah.nama),
        kode_cabang = ps.pelunasan.gerai.kode_cabang,
        tgl_trans =ps.tanggal,cu = user, mu = user,nobukti=ps.pelunasan.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_titipan_pelunasan,
        kredit = 0,debet = D(str(ps.nilai + ps.denda + ps.bea_jasa)),id_product = '4',status_jurnal ='2',tgl_trans =ps.tanggal,
        id_cabang =ps.gerai.kode_cabang,id_unit= 300)
     
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_denda,
        debet = 0,kredit = ps.denda,id_product = '4',status_jurnal ='2',tgl_trans =ps.tanggal,
        id_cabang =ps.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pdp_jasa,
        debet = 0,kredit = ps.bea_jasa,id_product = '4',status_jurnal ='2',tgl_trans =ps.tanggal,
        id_cabang =ps.pelunasan.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Pelunasan_adm"), id_coa = a_pinjaman_anggota,
        debet = 0,kredit = ps.nilai ,id_product = '4',status_jurnal ='2',tgl_trans =ps.tanggal,
        id_cabang =ps.pelunasan.gerai.kode_cabang,id_unit= 300)

@login_required
def laporan_rekap_dan_rinci(request):
    rekap = Tbl_Cabang.objects.all()
    start_date = None
    end_date = datetime.date(2002,01,01)
    id_cabang = None
    report = None
    jenis_laporan = None
    form = Filter_PencairanForm()
    plns = []
    
    if 'start_date' in request.GET and request.GET['start_date'] and 'cetak' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        report = request.GET['report']
        jenis_laporan = request.GET['jenis_laporan']
        ### rincian Piutang View Gabungan
        if id_cabang == '500'and jenis_laporan == '1' and report == '3':
            plns = []
            rekap = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in =( '1','6','7','8','9','10','5')).order_by('gerai')
            template = 'manop/piutang/rincian_piutang.html'
            variables = RequestContext(request, {'form':form,'total_nilai':sum([p.nilai for p in rekap]),'lapur': rekap ,\
                'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang})
            return render_to_response(template, variables)
        ### Akhir rincian Piutang View Gabungan
       
        ### rincian Piutang View Pergerai
        elif jenis_laporan == '1' and report == '3':            
            rekap = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in =( '1','6', '7','8','9','10','5')).\
                filter(gerai__kode_cabang = id_cabang)
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'manop/piutang/rincian_piutang.html'
            variables = RequestContext(request, {'form':form,'lapur': rekap ,'total_nilai':sum([p.nilai for p in rekap]),'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang})
            return render_to_response(template, variables)
        ### Akhir rincian Piutang View Pergerai   
    
        ### Rekap Piutang View
        elif jenis_laporan == '2' and report == '3':
            plns = []
            start_date = request.GET['start_date']
            end_date = request.GET['end_date']        
            trans = []
            for k in rekap:
                if k.akadgadai_set.exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(tanggal__range=(start_date,end_date)).count()>=0:
                    plns.append({'k':k,'kode_cabang':k.kode,'nama_cabang':k.nama,
                        'all_barang':k.all_barang(start_date,end_date),'nominal_all_barang':sum([p.nilai for p in k.nominal_all_barang(start_date,end_date)]),
                        'hp':k.hp_filter(start_date,end_date),'nominal_hp':sum([p.nilai for p in k.nominal_hp_filter(start_date,end_date)]),
                        'laptop':k.laptop_filter(start_date,end_date),'nominal_laptop':sum([p.nilai for p in k.nominal_laptop_filter(start_date,end_date)]),
                        'kamera':k.kamera_filter(start_date,end_date),'nominal_kamera':sum([p.nilai for p in k.nominal_kamera_filter(start_date,end_date)]),
                        'ps':k.ps_filter(start_date,end_date),'nominal_ps':sum([p.nilai for p in k.nominal_ps_filter(start_date,end_date)]),
                        'tv':k.tv_filter(start_date,end_date),'nominal_tv':sum([p.nilai for p in k.nominal_tv_filter(start_date,end_date)]),
                        'motor':k.motor_filter(start_date,end_date),'nominal_motor':sum([p.nilai for p in k.nominal_motor_filter(start_date,end_date)]),
                        'mobil':k.mobil_filter(start_date,end_date),'nominal_mobil':sum([p.nilai for p in k.nominal_mobil_filter(start_date,end_date)]),
                        })
            start_date = start_date
            end_date = end_date
            all_aktif = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5'))
            noa_all_aktif = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).count()
            total_nominal_hp= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=1)
            total_hp = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=1).count()
            total_nominal_laptop= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=2)
            total_laptop = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=2).count()
            total_nominal_kamera= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=3)
            total_kamera = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=3).count()
            total_nominal_ps= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=4)
            total_ps = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=4).count()
            total_nominal_tv= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=5)
            total_tv = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=5).count()
            total_nominal_motor= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_kendaraan=1)
            total_motor = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('LUNAS','LUNAS TERJUAL')).filter(barang__jenis_kendaraan=1).count()
            total_nominal_mobil= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_kendaraan=2)
            total_mobil = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_kendaraan=2).count()
      
            template = 'manop/piutang/rekap_piutang.html'
            variables = RequestContext(request, {'form':form,'plns': plns ,'start_date':start_date,'end_date':end_date,
                                                 'total_barang':noa_all_aktif,
                                                 'total_nominal_all_barang':float(sum([a.nilai for a in all_aktif])),
                                                 'total_hp':total_hp,'total_nominal_hp':sum([a.nilai for a in total_nominal_hp]),
                                                 'total_laptop':total_laptop,'total_nominal_laptop':sum([a.nilai for a in total_nominal_laptop]),
                                                 'total_kamera':total_kamera,'total_nominal_kamera':sum([a.nilai for a in total_nominal_kamera]),
                                                 'total_ps':total_ps,'total_nominal_ps':sum([a.nilai for a in total_nominal_ps]),
                                                 'total_tv':total_tv,'total_nominal_tv':sum([a.nilai for a in total_nominal_tv]),
                                                 'total_motor':total_motor,'total_nominal_motor':sum([a.nilai for a in total_nominal_motor]),
                                                 'total_mobil':total_mobil,'total_nominal_mobil':sum([a.nilai for a in total_nominal_mobil]),
                                                })
            return render_to_response(template, variables)
        ### Akhir Rekap Piutang View
        
        ### rincian Piutang pdf Gabungan
        elif id_cabang == '500'and jenis_laporan == '1' and report == '2':
            rekap = AkadGadai.objects.all().exclude(status_transaksi__in =('1','6','7','8','9','10','5')).filter(tanggal__range=(start_date,end_date)).order_by('gerai')
            template1 = 'manop/piutang/cetak_rincian_piutang.html'
            variables = RequestContext(request, {'form':form,
            'total_nilai':sum([p.nilai for p in rekap]),
            'lapur': rekap ,'start_date':start_date,
            'end_date':end_date,'id_cabang':id_cabang})
            return render_to_response(template1,variables)
        ### Akhir rincian Piutang pdf Gabungan
        
        ### rincian Piutang pdf Pergerai
        elif jenis_laporan == '1' and report == '2':
            rekap = AkadGadai.objects.all().exclude(status_transaksi__in =('1','6','7','8','9','10','5')).filter(tanggal__range=(start_date,end_date)).\
                filter(gerai__kode_cabang = id_cabang)
            template1 = 'manop/piutang/cetak_rincian_piutang.html'
            variables = RequestContext(request, {'form':form,
            'total_nilai':sum([p.nilai for p in rekap]),
            'lapur': rekap ,'start_date':start_date,
            'end_date':end_date,'id_cabang':id_cabang})
            return render_to_response(template1,variables)
        ### Akhir rincian Piutang pdf
        
        ### Rekap Piutang pdf
        elif jenis_laporan == '2' and report == '2':
            plns = []
            start_date = request.GET['start_date']
            end_date = request.GET['end_date']        
            trans = []
            for k in rekap:
                if k.akadgadai_set.exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(tanggal__range=(start_date,end_date)).count()>=0:
                    plns.append({'k':k,'kode_cabang':k.kode,'nama_cabang':k.nama,
                        'all_barang':k.all_barang(start_date,end_date),'nominal_all_barang':sum([p.nilai for p in k.nominal_all_barang(start_date,end_date)]),
                        'hp':k.hp_filter(start_date,end_date),'nominal_hp':sum([p.nilai for p in k.nominal_hp_filter(start_date,end_date)]),
                        'laptop':k.laptop_filter(start_date,end_date),'nominal_laptop':sum([p.nilai for p in k.nominal_laptop_filter(start_date,end_date)]),
                        'kamera':k.kamera_filter(start_date,end_date),'nominal_kamera':sum([p.nilai for p in k.nominal_kamera_filter(start_date,end_date)]),
                        'ps':k.ps_filter(start_date,end_date),'nominal_ps':sum([p.nilai for p in k.nominal_ps_filter(start_date,end_date)]),
                        'tv':k.tv_filter(start_date,end_date),'nominal_tv':sum([p.nilai for p in k.nominal_tv_filter(start_date,end_date)]),
                        'motor':k.motor_filter(start_date,end_date),'nominal_motor':sum([p.nilai for p in k.nominal_motor_filter(start_date,end_date)]),
                        'mobil':k.mobil_filter(start_date,end_date),'nominal_mobil':sum([p.nilai for p in k.nominal_mobil_filter(start_date,end_date)]),
                        })
            start_date = start_date
            end_date = end_date
            all_aktif = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5'))
            noa_all_aktif = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).count()
            total_nominal_hp= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=1)
            total_hp = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=1).count()
            total_nominal_laptop= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=2)
            total_laptop = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=2).count()
            total_nominal_kamera= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=3)
            total_kamera = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=3).count()
            total_nominal_ps= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=4)
            total_ps = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=4).count()
            total_nominal_tv= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=5)
            total_tv = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_barang=5).count()
            total_nominal_motor= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_kendaraan=1)
            total_motor = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_kendaraan=1).count()
            total_nominal_mobil= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_kendaraan=2)
            total_mobil = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','6','7','8','9','10','5')).filter(barang__jenis_kendaraan=2).count()
      
            template1 = 'manop/piutang/cetak_rekap_piutang.html'
            variables = RequestContext(request, {'form':form,'plns': plns ,'start_date':start_date,'end_date':end_date,
                                                 'total_barang':noa_all_aktif,
                                                 'total_nominal_all_barang':float(sum([a.nilai for a in all_aktif])),
                                                 'total_hp':total_hp,'total_nominal_hp':sum([a.nilai for a in total_nominal_hp]),
                                                 'total_laptop':total_laptop,'total_nominal_laptop':sum([a.nilai for a in total_nominal_laptop]),
                                                 'total_kamera':total_kamera,'total_nominal_kamera':sum([a.nilai for a in total_nominal_kamera]),
                                                 'total_ps':total_ps,'total_nominal_ps':sum([a.nilai for a in total_nominal_ps]),
                                                 'total_tv':total_tv,'total_nominal_tv':sum([a.nilai for a in total_nominal_tv]),
                                                 'total_motor':total_motor,'total_nominal_motor':sum([a.nilai for a in total_nominal_motor]),
                                                 'total_mobil':total_mobil,'total_nominal_mobil':sum([a.nilai for a in total_nominal_mobil]),
                                                })
            return render_to_response(template1, variables)
        ### Akhir rekap Piutang Pdf

        ### rincian Piutang excel Gabungan
        elif id_cabang == '500' and jenis_laporan == '1' and report == '1':
            akad = AkadGadai.objects.all()
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
            worksheet.set_column(10, 10, 10)
            worksheet.set_column(11, 11, 10)
           
        
            worksheet.merge_range('A1:K1', 'LAPORAN PIUTANG', merge_format1)
            worksheet.merge_range('A2:K2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama Nasabah', merge_format)
            worksheet.merge_range('D4:D5', 'Tgl Pencairan', merge_format)
            worksheet.merge_range('E4:E5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('F4:F5', 'Jenis Barang', merge_format)
            worksheet.merge_range('G4:G5', 'Barang', merge_format)
            worksheet.merge_range('H4:H5', 'Status Barang', merge_format)
            worksheet.merge_range('I4:I5', 'Nilai', merge_format)

            row = 5
            col = 0
           
            for t in akad.exclude(status_transaksi__in =('1','6','7','8','9','10','5')).filter(tanggal__range=(start_date,end_date)).order_by('gerai'):
                worksheet.write_string(row, col , t.norek())
                worksheet.write_string(row, col + 1 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.agnasabah.nama)
                worksheet.write_datetime(row, col + 3,t.tanggal,date_format)
                worksheet.write_datetime(row, col + 4 , t.jatuhtempo,date_format)
                worksheet.write_string(row, col + 5,t.jenis_barang_all())
                worksheet.write_string(row, col + 6 ,t.kode_barang_all())
                worksheet.write_string(row, col + 7 ,t.sts_trans_excel())
                worksheet.write_number(row, col + 8 ,t.nilai,money_format)

                row += 1 
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=LAPORAN_PINJAMAN_GABUNGAN.xlsx"
            return response
        ### Akhir rincian Piutang excel Gabungan
        
        ### rincian Piutang excel Pergerai
        elif jenis_laporan == '1' and report == '1':
            akad = AkadGadai.objects.all()
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
            worksheet.set_column(10, 10, 10)
            worksheet.set_column(11, 11, 10)
           
            worksheet.merge_range('A1:K1', 'LAPORAN PIUTANG', merge_format1)
            worksheet.merge_range('A2:K2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama Nasabah', merge_format)
            worksheet.merge_range('D4:D5', 'Tgl Pencairan', merge_format)
            worksheet.merge_range('E4:E5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('F4:F5', 'Jenis Barang', merge_format)
            worksheet.merge_range('G4:G5', 'Barang', merge_format)
            worksheet.merge_range('H4:H5', 'Status Barang', merge_format)
            worksheet.merge_range('I4:I5', 'Nilai', merge_format)

            row = 5
            col = 0
           
            for t in akad.exclude(status_transaksi__in =('1','6','7','8','9','10','5')).filter(tanggal__range=(start_date,end_date)).\
                filter(gerai__kode_cabang = id_cabang).order_by('gerai'):
                worksheet.write_string(row, col , t.norek())
                worksheet.write_string(row, col + 1 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.agnasabah.nama)
                worksheet.write_datetime(row, col + 3,t.tanggal,date_format)
                worksheet.write_datetime(row, col + 4 , t.jatuhtempo,date_format)
                worksheet.write_string(row, col + 5,t.jenis_barang_all())
                worksheet.write_string(row, col + 6 ,t.kode_barang_all())
                worksheet.write_string(row, col + 7 ,t.sts_trans_excel())
                worksheet.write_number(row, col + 8 ,t.nilai,money_format)

                row += 1 
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=LAPORAN_PINJAMAN_GABUNGAN.xlsx"
            return response
            ### Akhir rincian Piutang excel Pergerai

            ### Rekap Piutang excel
        elif jenis_laporan == '2' and report == '1':
            start_date = request.GET['start_date']
            end_date = request.GET['end_date']
            start_date = start_date
            end_date = end_date        
            trans = []
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': 0, 'fg_color': '#D7E4BC'})        
        
            money_format = workbook.add_format({'num_format': '#,##0'})
            date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
            merge_format = workbook.add_format({'bold': 1,'border': 6,'align': 'center','valign': 'vcenter','fg_color': '#D7E4BC'})
            merge_format1 = workbook.add_format({'bold': 1,'border': 6,'align': 'center','valign': 'vcenter','fg_color': '#C0C0C0'})
            bold1 = workbook.add_format({'bold': 0, 'fg_color': '#C0C0C0'})        

            worksheet.set_column(0, 0, 6) 
            worksheet.set_column(1, 1, 18)
            worksheet.set_column(2, 2, 10)
            worksheet.set_column(3, 3, 10)
            worksheet.set_column(4, 4, 10)
            worksheet.set_column(5, 5, 10)
            worksheet.set_column(6, 6, 10)
            worksheet.set_column(7, 7, 10)
            worksheet.set_column(8, 7, 10)
            worksheet.set_column(9, 9, 10)
            worksheet.set_column(10, 10, 10)
            worksheet.set_column(11, 11, 11)
            worksheet.set_column(12, 12, 12)
            worksheet.set_column(13, 13, 13)
            worksheet.set_column(14, 14, 14)

            worksheet.merge_range('A1:R1', 'REKAPITULASI PINJAMAN', merge_format)
            worksheet.merge_range('A2:R2', 'Periode :'+ start_date + " s.d " + end_date, merge_format)
            worksheet.merge_range('A3:A4', 'KODE', merge_format)
            worksheet.merge_range('B3:B4', 'GERAI', merge_format)
            worksheet.merge_range('C3:R3', 'AKTIF', merge_format)
            worksheet.write('C4', 'Jml Barang', bold)
            worksheet.write('D4', 'Nominal Barang', bold)
            worksheet.write('E4', 'HP', bold)
            worksheet.write('F4', 'Nominal HP', bold)
            worksheet.write('G4', 'Laptop', bold)
            worksheet.write('H4', 'Nominal Laptop', bold)
            worksheet.write('I4', 'Kamera', bold)
            worksheet.write('J4', 'Nominal Kamera', bold)
            worksheet.write('K4', 'PS', bold)
            worksheet.write('L4', 'Nominal PS', bold)
            worksheet.write('M4', 'TV', bold)
            worksheet.write('N4', 'Nominal TV', bold)
            worksheet.write('O4', 'Motor', bold)
            worksheet.write('P4', 'Nominal Motor', bold)
            worksheet.write('Q4', 'Mobil', bold)
            worksheet.write('R4', 'Nominal Mobil', bold)

            row = 4
            col = 0

            for k in rekap:
                #if k.akadgadai_set.filter(status_transaksi=None).filter(tanggal__range=(start_date,end_date)).count()>=0:
                if k.akadgadai_set.exclude(status_transaksi__in =('1','6','7','8','9','10','5')).filter(tanggal__range=(start_date,end_date)).count()>=0:
                    plns.append({'k':k,'aktif':k.aktif_nasabah_harian_filter(start_date,end_date),'kode_cabang':k.kode_cabang,'nama_cabang':k.nama_cabang,
                        'all_barang':k.all_barang(start_date,end_date),'nominal_all_barang':sum([p.nilai for p in k.nominal_all_barang(start_date,end_date)]),
                        'hp':k.hp_filter(start_date,end_date),'nominal_hp':sum([p.nilai for p in k.nominal_hp_filter(start_date,end_date)]),
                        'laptop':k.laptop_filter(start_date,end_date),'nominal_laptop':sum([p.nilai for p in k.nominal_laptop_filter(start_date,end_date)]),
                        'kamera':k.kamera_filter(start_date,end_date),'nominal_kamera':sum([p.nilai for p in k.nominal_kamera_filter(start_date,end_date)]),
                        'ps':k.ps_filter(start_date,end_date),'nominal_ps':sum([p.nilai for p in k.nominal_ps_filter(start_date,end_date)]),
                        'tv':k.tv_filter(start_date,end_date),'nominal_tv':sum([p.nilai for p in k.nominal_tv_filter(start_date,end_date)]),
                        'motor':k.motor_filter(start_date,end_date),'nominal_motor':sum([p.nilai for p in k.nominal_motor_filter(start_date,end_date)]),
                        'mobil':k.mobil_filter(start_date,end_date),'nominal_mobil':sum([p.nilai for p in k.nominal_mobil_filter(start_date,end_date)]),
                    
                        })              
       
                    start_date = start_date
                    end_date = end_date
                    worksheet.write_string(row, col , k.kode_cabang)
                    worksheet.write_string(row, col + 1, k.nama_cabang)
                    worksheet.write_number(row, col + 2, k.all_barang(start_date,end_date), money_format)
                    worksheet.write_number(row, col + 3, sum([p.nilai for p in k.nominal_all_barang(start_date,end_date)]), money_format)
                    worksheet.write_number(row, col + 4, k.hp_filter(start_date,end_date), money_format)
                    worksheet.write_number(row, col + 5, sum([p.nilai for p in k.nominal_hp_filter(start_date,end_date)]), money_format)
                    worksheet.write_number(row, col + 6, k.laptop_filter(start_date,end_date),money_format)
                    worksheet.write_number(row, col + 7, sum([p.nilai for p in k.nominal_laptop_filter(start_date,end_date)]),money_format)
                    worksheet.write_number(row, col + 8, k.kamera_filter(start_date,end_date),money_format)
                    worksheet.write_number(row, col + 9, sum([p.nilai for p in k.nominal_kamera_filter(start_date,end_date)]),money_format)
                    worksheet.write_number(row, col + 10, k.ps_filter(start_date,end_date),money_format)
                    worksheet.write_number(row, col + 11, sum([p.nilai for p in k.nominal_ps_filter(start_date,end_date)]),money_format)
                    worksheet.write_number(row, col + 12, k.tv_filter(start_date,end_date),money_format)
                    worksheet.write_number(row, col + 13, sum([p.nilai for p in k.nominal_tv_filter(start_date,end_date)]),money_format)
                    worksheet.write_number(row, col + 14, k.motor_filter(start_date,end_date),money_format)
                    worksheet.write_number(row, col + 15, sum([p.nilai for p in k.nominal_motor_filter(start_date,end_date)]),money_format)
                    worksheet.write_number(row, col + 16, k.mobil_filter(start_date,end_date),money_format)
                    worksheet.write_number(row, col + 17, sum([p.nilai for p in k.nominal_mobil_filter(start_date,end_date)]),money_format)


                    row += 1
            worksheet.write(row, 0, 'Total', bold)
            worksheet.write(row, 2, '=SUM(C5:C25)', money_format)
            worksheet.write(row, 3, '=SUM(D5:D25)', money_format)
            worksheet.write(row, 4, '=SUM(E5:E25)', money_format)
            worksheet.write(row, 5, '=SUM(F5:F25)', money_format)
            worksheet.write(row, 6, '=SUM(G5:G25)', money_format)
            worksheet.write(row, 7, '=SUM(H5:H25)', money_format)
            worksheet.write(row, 8, '=SUM(I5:I25)', money_format)
            worksheet.write(row, 9, '=SUM(J5:J25)', money_format)
            worksheet.write(row, 10, '=SUM(K5:K25)', money_format)
            worksheet.write(row, 11, '=SUM(L5:L25)', money_format)
            worksheet.write(row, 12, '=SUM(M5:M25)', money_format)
            worksheet.write(row, 13, '=SUM(N5:N25)', money_format)
            worksheet.write(row, 14, '=SUM(O5:O25)', money_format)
            worksheet.write(row, 15, '=SUM(P5:P25)', money_format)
            worksheet.write(row, 16, '=SUM(Q5:Q25)', money_format)
            worksheet.write(row, 17, '=SUM(R5:R25)', money_format)
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=rekap_Laporan_pinjaman.xlsx" #filename=rekap_barang_aktif_dan_lapur.xlsx"    
            return response       
            ### Akhir Piutang Excel
  
    else:
        form = Filter_PencairanForm()
        template = 'manop/piutang/rincian_piutang.html'
    variable = RequestContext(request,{'form':form})
    return render_to_response(template,variable)


def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['manop','baranglapur','admops','abh','staffops','asmanpjb','kadiv'])

def delete(request,object_id):
    lapur = Lapur.objects.get(pk=object_id)
    lapur.delete()
    variable = RequestContext(request,{'lapur':lapur})
    return render_to_response('manop/lapur_barang/',variable)

def lunasterjual_barang(request):
    start_date = None
    end_date = None
    id_cabang = None
    form = Filter_PencairanForm()
    plns = []
    if 'start_date' in request.GET and request.GET['start_date'] and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500':
            plns = []
            rekap = LunasTerjual.objects.filter(status = '1').filter(tanggal__range=(start_date,end_date))
            template = 'manop/laporan/lapur/laporan_lunasterjual.html'
            variables = RequestContext(request, {'lunas': rekap ,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,\
                'total_ayda': sum([p.aglunas.total_akad_ayda() for p in rekap]),\
                'nilai_lelang_tot':sum([p.aglunas.hargalelang() for p in rekap]),'tot_kred':sum([p.aglunas.nilai for p in rekap]),\
                'total_untung': sum([p.aglunas.untung_rugi_ayda() for p in rekap if p.aglunas.untung_rugi_ayda() > 0]),\
                'total_rugi': sum([p.aglunas.untung_rugi_ayda() * -1  for p in rekap if p.aglunas.untung_rugi_ayda() < 0])})
            return render_to_response(template, variables)
        else:            
            rekap = LunasTerjual.objects.filter(status = '1').filter(tanggal__range=(start_date,end_date)).filter(aglunas__gerai__kode_cabang = id_cabang)
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'manop/laporan/lapur/laporan_lunasterjual.html'
            variables = RequestContext(request, {'lunas': rekap ,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang})
            return render_to_response(template, variables)
    if 'start_date' in request.GET and request.GET['start_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500':
            plns = []
            rekap = LunasTerjual.objects.filter(status = '1').filter(tanggal__range=(start_date,end_date))
            template = 'manop/laporan/lapur/laporan_lunasterjual_pdf.html'
            variables = RequestContext(request, {'lunas': rekap ,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang})
            return render_to_response(template, variables)
        else:            
            rekap = Lapur.objects.filter(status = '1').filter(tanggal__range=(start_date,end_date)).filter(aglapur__gerai = id_cabang)
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'manop/laporan/lapur/laporan_lunasterjual_pdf.html'
            variables = RequestContext(request, {'lunas': rekap ,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang})
            return render_to_response(template, variables)
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']         
        if id_cabang == '500' :
            akad = LunasTerjual.objects.all()
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
            worksheet.set_column(10, 10, 10)
            worksheet.set_column(11, 11, 10)
            
        
            worksheet.merge_range('A1:K1', 'LAPORAN BARANG LUNAS JUAL ', merge_format1)
            worksheet.merge_range('A2:K2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama Nasabah', merge_format)
            worksheet.merge_range('D4:D5', 'Tgl Pencairan', merge_format)
            worksheet.merge_range('E4:E5', 'Jangka Waktu', merge_format)
            worksheet.merge_range('F4:F5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('G4:G5', 'Tgl Lunas', merge_format)
            worksheet.merge_range('H4:H5', 'Nama Pembeli', merge_format)
            worksheet.merge_range('I4:I5', 'Nilai Akad', merge_format)
            worksheet.merge_range('J4:J5', 'Nilai Lelang', merge_format)
            worksheet.merge_range('K4:K5', 'Nilai Untung', merge_format)
            row = 5
            col = 0
            
            for t in akad.filter(status = '1').filter(tanggal__range=(start_date,end_date)):
                worksheet.write_string(row, col , t.aglunas.norek())
                worksheet.write_string(row, col + 1 , t.aglunas.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.aglunas.agnasabah.nama)
                worksheet.write_datetime(row, col + 3 , t.aglunas.tanggal,date_format)
                worksheet.write_string(row, col + 4 , t.aglunas.jw_all())
                worksheet.write_datetime(row, col + 5 , t.aglunas.jatuhtempo,date_format)
                worksheet.write_datetime(row, col + 6 ,t.tanggal,date_format )
                worksheet.write_string(row, col + 7 ,t.aglunas.namalelang())
                worksheet.write_number(row, col + 8 ,t.aglunas.nilai,money_format)
                worksheet.write_number(row, col + 9 ,t.aglunas.hargalelang(),money_format)
                worksheet.write_number(row, col + 10 ,t.aglunas.nilai_lelang(),money_format)
                row += 1 
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Laporan_lunasjual_gabungan.xlsx"
            return response
        else:
            akad= LunasTerjual.objects.filter(status = '1').filter(tanggal__range=(start_date,end_date)).filter(aglunas__gerai = id_cabang)
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
            worksheet.set_column(10, 10, 10)
            worksheet.set_column(11, 11, 10)
            
        
            worksheet.merge_range('A1:K1', 'LAPORAN BARANG LUNAS JUAL ', merge_format1)
            worksheet.merge_range('A2:K2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama Nasabah', merge_format)
            worksheet.merge_range('D4:D5', 'Tgl Pencairan', merge_format)
            worksheet.merge_range('E4:E5', 'Jangka Waktu', merge_format)
            worksheet.merge_range('F4:F5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('G4:G5', 'Tgl Lunas', merge_format)
            worksheet.merge_range('H4:H5', 'Nama Pembeli', merge_format)
            worksheet.merge_range('I4:I5', 'Nilai Akad', merge_format)
            worksheet.merge_range('J4:J5', 'Nilai Lelang', merge_format)
            worksheet.merge_range('K4:K5', 'Nilai Untung', merge_format) 

            row = 5
            col = 0
            for t in akad.filter(status = '1').filter(tanggal__range=(start_date,end_date)).filter(aglunas__gerai = id_cabang):
                worksheet.write_string(row, col , t.aglunas.norek())
                worksheet.write_string(row, col + 1 , t.aglunas.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.aglunas.agnasabah.nama)
                worksheet.write_datetime(row, col + 3 , t.aglunas.tanggal,date_format)
                worksheet.write_string(row, col + 4 , t.aglunas.jw_all())
                worksheet.write_datetime(row, col + 5 , t.aglunas.jatuhtempo,date_format)
                worksheet.write_datetime(row, col + 6 ,t.tanggal,date_format )
                worksheet.write_string(row, col + 7 ,t.aglunas.namalelang())
                worksheet.write_number(row, col + 8 ,t.aglunas.nilai,money_format)
                worksheet.write_number(row, col + 9 ,t.aglunas.hargalelang(),money_format)
                worksheet.write_number(row, col + 10 ,t.aglunas.nilai_lelang(),money_format)
                row += 1
            workbook.close()
            output.seek(0)
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Laporan_Perpanjangan.xlsx"
            return response
        
    else:
        template='manop/laporan/lapur/laporan_lunasterjual.html'
        variable = RequestContext(request,{'form':form})
        return render_to_response(template,variable)

def lapur_barang(request):###teddy27042015
    kp = []
    start_date = None
    end_date = None
    id_cabang = None
    report = None
    form = Filter_PencairanForm()
    plns = []
    print report
    if 'start_date' in request.GET and request.GET['end_date']  and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        report = request.GET['report']
        if id_cabang == '500' and report == '3':
            plns = []
            rekap = Lapur.objects.filter(status = '1').filter(tanggal__range=(start_date,end_date)).filter(aglapur__status_transaksi = '6')
            template = 'manop/laporan/lapur/laporan_lapur.html'
            variables = RequestContext(request, {'form':form,'lapur': rekap ,'start_date':start_date,'end_date':end_date,\
                'id_cabang':id_cabang,'total':sum([p.nilai for p in rekap]),\
                'total_plafon':sum([p.nilai for p in rekap])})
            return render_to_response(template, variables)
        elif id_cabang == id_cabang and report =='3':            
            rekap = Lapur.objects.filter(status = '1').filter(tanggal__range=(start_date,end_date)).filter(aglapur__gerai__kode_cabang = id_cabang)\
                .filter(aglapur__status_transaksi = '6')
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'manop/laporan/lapur/laporan_lapur.html'
            variables = RequestContext(request, {'form':form,'lapur': rekap ,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,\
                'total':sum([p.nilai for p in rekap]),\
                'total_plafon':sum([p.nilai for p in rekap])})
            return render_to_response(template, variables)
    
        elif id_cabang == '500' and report == '2':
            plns = []
            rekap = Lapur.objects.filter(status = '1').filter(tanggal__range=(start_date,end_date)).filter(aglapur__status_transaksi = '6')
            template = 'manop/laporan/lapur/laporan_lapur_pdf.html'
            variables = RequestContext(request, {'form':form,'lapur': rekap ,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,\
                'total':sum([p.aglapur.nilai for p in rekap]),\
                'total_plafon':sum([p.nilai for p in rekap])})
            return render_to_response(template, variables)
        elif id_cabang == id_cabang and report =='2':            
            rekap = Lapur.objects.filter(status = '1').filter(tanggal__range=(start_date,end_date)).filter(aglapur__gerai__kode_cabang = id_cabang)
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'manop/laporan/lapur/laporan_lapur_pdf.html'
            variables = RequestContext(request, {'form':form,'lapur': rekap ,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,\
                'total':sum([p.aglapur.nilai for p in rekap]),\
                'total_plafon':sum([p.nilai for p in rekap])})
            return render_to_response(template, variables)
    
        elif id_cabang == '500' and report == '1':
            akad = Lapur.objects.filter(status = '1').filter(tanggal__range=(start_date,end_date)).filter(aglapur__status_transaksi = '6')
            #akad= Lapur.objects.filter(status = '1').filter(tanggal__range=(start_date,end_date)).filter(aglapur__gerai = id_cabang)
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
            
        
            worksheet.merge_range('A1:I1', 'LAPORAN BARANG AYDA GABUNGAN', merge_format1)
            worksheet.merge_range('A2:I2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Norek Ayda', merge_format)
            worksheet.merge_range('C4:C5', 'Jenis Barang', merge_format)
            worksheet.merge_range('D4:D5', 'Barang', merge_format)
            worksheet.merge_range('E4:E5', 'Tanggal Akad', merge_format)
            worksheet.merge_range('F4:F5', 'JATUH TEMPO', merge_format)

            worksheet.merge_range('G4:G5', 'Jangka Waktu', merge_format)
            worksheet.merge_range('H4:H5', 'Tgl Ayda', merge_format)
            worksheet.merge_range('I4:I5', 'Eks Debitur', merge_format)
            worksheet.merge_range('J4:J5', 'Gerai', merge_format)
            worksheet.merge_range('K4:K5', 'Plafon', merge_format)
            worksheet.merge_range('L4:L5', 'Nilai Ayda', merge_format)
            row = 5
            col = 0
            rekap = Lapur.objects.filter(status = '1').filter(tanggal__range=(start_date,end_date)).filter(aglapur__status_transaksi = '6')
            aa = sum([a.aglapur.nilai for a in rekap])
            bb = sum([a.nilai for a in rekap])
            for t in akad.filter(status = '1').filter(tanggal__range=(start_date,end_date)):
                worksheet.write_string(row, col , t.aglapur.norek())
                worksheet.write_string(row, col + 1 , t.norek_lapur())
                worksheet.write_string(row, col + 2 , t.aglapur.jenis_barang_all())
                worksheet.write_string(row, col + 3 , t.aglapur.barang.merk + '' + t.aglapur.barang.type)
                worksheet.write_datetime(row, col + 4 ,t.aglapur.tanggal,date_format )
                worksheet.write_datetime(row, col + 5 ,t.aglapur.jatuhtempo,date_format )
                if t.aglapur.jenis_transaksi == '2':
                    worksheet.write_string(row, col + 6, t.aglapur.jangka_waktu_kendaraan + 'Bulan')
                else:
                    worksheet.write_string(row, col + 6, t.aglapur.jangka_waktu + 'Hari')
                worksheet.write_datetime(row, col + 7 ,t.tanggal,date_format )
                worksheet.write_string(row, col + 8 , t.aglapur.agnasabah.nama)
                worksheet.write_string(row, col + 9, t.aglapur.gerai.nama_cabang)
                worksheet.write_number(row, col + 10, t.aglapur.nilai, money_format)
                worksheet.write_number(row, col + 11, t.nilai, money_format)
                row += 1 
            
            worksheet.write(row,0, 'Total', bold)

            worksheet.write(row, 10, aa, money_format)
            worksheet.write(row, 11, bb, money_format)

            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Laporan_Lapur_gabungan.xlsx"
            return response
        else:
            akad= Lapur.objects.filter(status = '1').filter(tanggal__range=(start_date,end_date)).filter(aglapur__gerai__kode_cabang = id_cabang).\
                filter(aglapur__status_transaksi = '6')
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
            
        
            worksheet.merge_range('A1:I1', 'LAPORAN BARANG AYDA PER GERAI', merge_format1)
            worksheet.merge_range('A2:I2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Norek Ayda', merge_format)
            worksheet.merge_range('C4:C5', 'Jenis Barang', merge_format)
            worksheet.merge_range('D4:D5', 'Barang', merge_format)
            worksheet.merge_range('E4:E5', 'Plafon', merge_format)
            worksheet.merge_range('F4:F5', 'Nilai Ayda', merge_format)
            worksheet.merge_range('G4:G5', 'Tgl Lapur', merge_format)
            worksheet.merge_range('H4:H5', 'Eks Debitur', merge_format)
            worksheet.merge_range('I4:I5', 'Gerai', merge_format)
            worksheet.merge_range('J4:J5', 'Plafon', merge_format)
            worksheet.merge_range('K4:K5', 'Nilai Ayda', merge_format)

            row = 5
            col = 0
            rekap = Lapur.objects.filter(status = '1').filter(tanggal__range=(start_date,end_date)).filter(aglapur__status_transaksi = '6').filter(aglapur__gerai__kode_cabang = id_cabang)
            aa = sum([a.aglapur.nilai for a in rekap])
            bb = sum([a.nilai for a in rekap])
            for t in rekap:
                worksheet.write_string(row, col , t.aglapur.norek())
                worksheet.write_string(row, col + 1 , t.norek_lapur())
                worksheet.write_string(row, col + 2 , t.aglapur.jenis_barang_all())
                worksheet.write_string(row, col + 3 , t.aglapur.barang.merk + '' + t.aglapur.barang.type)
                if t.aglapur.jenis_transaksi == '2':
                    worksheet.write_string(row, col + 5, t.aglapur.jangka_waktu_kendaraan + 'Bulan')
                else:
                    worksheet.write_string(row, col + 5, t.aglapur.jangka_waktu + 'Hari')
                
                worksheet.write_datetime(row, col + 6 ,t.tanggal,date_format )
                worksheet.write_string(row, col + 7 , t.aglapur.agnasabah.nama)
                worksheet.write_string(row, col + 8, t.aglapur.gerai.nama_cabang)
                worksheet.write_number(row, col + 9, t.aglapur.nilai, money_format)
                worksheet.write_number(row, col + 10, t.nilai, money_format)
                row += 1
            
            worksheet.write(row,0, 'Total', bold)    

            worksheet.write(row, 9, aa, money_format)
            worksheet.write(row, 10, bb, money_format)
            workbook.close()

            output.seek(0)
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Laporan_Perpanjangan.xlsx"
            return response
    ###realtime    
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET :
        end_date = request.GET['end_date']
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        report = request.GET['report']
        if id_cabang == '500' and report == '3':
            akad= AkadGadai.objects.filter(status_transaksi =('LAPUR')).filter(tanggal_lelang__range=(start_date,end_date))
            for k in akad:
                kp.append(k)
            total_nilai = 0
            for b in kp:
                total_nilai += b.nilai 
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'manop/laporan/lapur/laporan_lapur.html'
            variables = RequestContext(request, {'form':form,'kp':kp,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,'nilai':total_nilai})     
            return render_to_response(template, variables)
        elif id_cabang == id_cabang and report == '3':
            akad= AkadGadai.objects.filter(status_transaksi= ('LAPUR')).filter(tanggal_lelang__range=(start_date,end_date)).filter(gerai__kode_cabang= id_cabang)
            for k in akad:
                kp.append(k)
            total_nilai = 0
            for b in kp:
                total_nilai += b.nilai
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'manop/laporan/lapur/laporan_lapur.html'
            variables = RequestContext(request, {'form':form,'kp':kp,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,'nilai':total_nilai})
            return render_to_response(template, variables)
        elif id_cabang == '500' and report == '2':
            akad= AkadGadai.objects.filter(status_transaksi=('LAPUR')).filter(tanggal_lelang__range=(start_date,end_date))
            for k in akad:
                kp.append(k)
            total_nilai = 0
            for b in kp:
                total_nilai += b.nilai    
            template = 'manop/lelang/rincian_lelang_pdf.html'
            variables = RequestContext(request, {'form':form,'kp':kp,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,'nilai':total_nilai})
            return render_to_response(template, variables)
        elif id_cabang == id_cabang and report == '2':
            akad= AkadGadai.objects.filter(status_transaksi=('LAPUR')).filter(tanggal_lelang__range=(start_date,end_date)).\
                filter(gerai__kode_cabang= id_cabang)
            for k in akad:
                kp.append(k)
            total_nilai = 0
            for b in kp:
                total_nilai += b.nilai    
            template = 'manop/lelang/rincian_lelang_pdf.html'
            variables = RequestContext(request, {'form':form,'kp':kp,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,'nilai':total_nilai})
            return render_to_response(template, variables)
        
        elif id_cabang == '500' and report == '1':
            akad= AkadGadai.objects.filter(status_transaksi =('LAPUR')).filter(tanggal_lelang__range=(start_date,end_date))
            for k in akad:
                kp.append(k)
            a = sum([b.nilai for b in akad ])
            c = sum([b.jasa for b in akad ]) 
            d = sum([b.adm for b in akad ]) 
            e = sum([b.biayasimpan for b in akad ]) 
            f = start_date
            g = end_date
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': 0})
            bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            money_format = workbook.add_format({'num_format': '#,##0'})
            date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
            merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            merge_format1 = workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter',})
        
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
            worksheet.set_column(10, 10, 10)
        
            worksheet.merge_range('A1:K1', 'DATA LELANG ', merge_format1)
            worksheet.merge_range('A2:K2', 'PERIODE ', merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Nama', merge_format)
            worksheet.merge_range('C4:C5', 'Gerai', merge_format)
            worksheet.merge_range('D4:D5', 'Tgl Lelang', merge_format)
            
            worksheet.merge_range('E4:E5', 'Tgl Akad', merge_format)
            worksheet.merge_range('F4:F5', 'JW (hari)', merge_format)
            worksheet.merge_range('G4:G5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('H4:H5', 'Status', merge_format)
            worksheet.merge_range('I4:I5', 'Nilai', merge_format)
            worksheet.merge_range('J4:J5', 'Jenis Barang', merge_format)
            worksheet.merge_range('K4:K5', 'Barang', merge_format)
    
            row = 5
            col = 0
            for t in akad:
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.agnasabah.nama)
                worksheet.write_string(row, col + 2 , t.gerai.nama)
                worksheet.write_datetime(row, col + 3 , t.tanggal_lelang,date_format)
                worksheet.write_datetime(row, col + 4 , t.tanggal,date_format)
                worksheet.write_number(row, col + 5, t.jw_all(), money_format)
                worksheet.write_datetime(row, col + 6, t.jatuhtempo,date_format)
                worksheet.write_string(row, col + 7, t.status_transaksi)
                worksheet.write_number(row, col + 8, t.nilai, money_format)
                worksheet.write_string(row, col + 9, t.jenis_barang_all())
                worksheet.write_string(row, col + 10, t.barang.merk +' ' + t.barang.type)
                row += 1
    
            worksheet.write(row,4, 'Total', bold)    
            worksheet.write(row,8, a, money_format)
        
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=LELANG.xlsx"
            return response  ###filter(gerai__id= id_cabang)
        elif id_cabang == id_cabang and report == '1':
            akad= AkadGadai.objects.filter(status_transaksi =('LAPUR')).filter(tanggal_lelang__range=(start_date,end_date)).filter(gerai__id= id_cabang)
            for k in akad:
                kp.append(k)
            a = sum([b.nilai for b in akad ])
            c = sum([b.jasa for b in akad ]) 
            d = sum([b.adm for b in akad ]) 
            e = sum([b.biayasimpan for b in akad ]) 
            f = start_date
            g = end_date
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': 0})
            bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            money_format = workbook.add_format({'num_format': '#,##0'})
            date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
            merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            merge_format1 = workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter',})
        
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
            worksheet.set_column(10, 10, 10)
        
            worksheet.merge_range('A1:K1', 'DATA LELANG ', merge_format1)
            worksheet.merge_range('A2:K2', 'PERIODE ', merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Nama', merge_format)
            worksheet.merge_range('C4:C5', 'Gerai', merge_format)
            worksheet.merge_range('D4:D5', 'Tgl Lelang', merge_format)
            
            worksheet.merge_range('E4:E5', 'Tgl Akad', merge_format)
            worksheet.merge_range('F4:F5', 'JW (hari)', merge_format)
            worksheet.merge_range('G4:G5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('H4:H5', 'Status', merge_format)
            worksheet.merge_range('I4:I5', 'Nilai', merge_format)
            worksheet.merge_range('J4:J5', 'Jenis Barang', merge_format)
            worksheet.merge_range('K4:K5', 'Barang', merge_format)
    
            row = 5
            col = 0
            for t in akad:
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.agnasabah.nama)
                worksheet.write_string(row, col + 2 , t.gerai.nama)
                worksheet.write_datetime(row, col + 3 , t.tanggal_lelang,date_format)
                worksheet.write_datetime(row, col + 4 , t.tanggal,date_format)
                worksheet.write_number(row, col + 5, t.jw_all(), money_format)
                worksheet.write_datetime(row, col + 6, t.jatuhtempo,date_format)
                worksheet.write_string(row, col + 7, t.status_transaksi)
                worksheet.write_number(row, col + 8, t.nilai, money_format)
                worksheet.write_string(row, col + 9, t.jenis_barang_all())
                worksheet.write_string(row, col + 10, t.barang.merk +' ' + t.barang.type)
                row += 1
    
            worksheet.write(row,4, 'Total', bold)    
            worksheet.write(row,8, a, money_format)
        
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=LELANG.xlsx"
            return response
            
    else:
        template='manop/laporan/lapur/laporan_lapur.html'
        variable = RequestContext(request,{'form':form})
        return render_to_response(template,variable)

def rekap_barang_aktif_dan_lapur(request):
    rekap = Tbl_Cabang.objects.all()
    plns = []
    lpr=[]
    form = Filter_PencairanForm()
    start_date = None
    end_date = None
    id_cabang = None
    if 'start_date' in request.GET and request.GET['start_date'] and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']        
        trans = []
        for k in rekap:
            if k.akadgadai_set.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(tanggal__range=(start_date,end_date)).count()>=0:
                plns.append({'k':k,'kode_cabang':k.kode_cabang,'nama_cabang':k.nama_cabang,
                    'all_barang':k.all_barang(start_date,end_date),'nominal_all_barang':sum([p.nilai for p in k.nominal_all_barang(start_date,end_date)]),
                    'hp':k.hp_filter(start_date,end_date),'nominal_hp':sum([p.nilai for p in k.nominal_hp_filter(start_date,end_date)]),
                    'laptop':k.laptop_filter(start_date,end_date),'nominal_laptop':sum([p.nilai for p in k.nominal_laptop_filter(start_date,end_date)]),
                    'kamera':k.kamera_filter(start_date,end_date),'nominal_kamera':sum([p.nilai for p in k.nominal_kamera_filter(start_date,end_date)]),
                    'ps':k.ps_filter(start_date,end_date),'nominal_ps':sum([p.nilai for p in k.nominal_ps_filter(start_date,end_date)]),
                    'tv':k.tv_filter(start_date,end_date),'nominal_tv':sum([p.nilai for p in k.nominal_tv_filter(start_date,end_date)]),
                    'motor':k.motor_filter(start_date,end_date),'nominal_motor':sum([p.nilai for p in k.nominal_motor_filter(start_date,end_date)]),
                    'mobil':k.mobil_filter(start_date,end_date),'nominal_mobil':sum([p.nilai for p in k.nominal_mobil_filter(start_date,end_date)]),
                    
                    })
        
        for l in rekap:
            if l.akadgadai_set.filter(status_transaksi= "6").filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').count()>=0:
                lpr.append({'l':l,'kode_cabang':l.kode_cabang,'nama_cabang':l.nama_cabang,
                    'all_barang':l.lpr_all_barang(start_date,end_date),'nominal_all_barang':sum([p.nilai for p in l.lpr_nominal_all_barang(start_date,end_date)]),
                    'hp':l.lpr_hp_filter(start_date,end_date),'nominal_hp':sum([p.nilai for p in l.lpr_nominal_hp_filter(start_date,end_date)]),
                    'laptop':l.lpr_laptop_filter(start_date,end_date),'nominal_laptop':sum([p.nilai for p in l.lpr_nominal_laptop_filter(start_date,end_date)]),
                    'kamera':l.lpr_kamera_filter(start_date,end_date),'nominal_kamera':sum([p.nilai for p in l.lpr_nominal_kamera_filter(start_date,end_date)]),
                    'ps':l.lpr_ps_filter(start_date,end_date),'nominal_ps':sum([p.nilai for p in l.lpr_nominal_ps_filter(start_date,end_date)]),
                    'tv':l.lpr_tv_filter(start_date,end_date),'nominal_tv':sum([p.nilai for p in l.lpr_nominal_tv_filter(start_date,end_date)]),
                    'motor':l.lpr_motor_filter(start_date,end_date),'nominal_motor':sum([p.nilai for p in l.lpr_nominal_motor_filter(start_date,end_date)]),
                    'mobil':l.lpr_mobil_filter(start_date,end_date),'nominal_mobil':sum([p.nilai for p in l.lpr_nominal_mobil_filter(start_date,end_date)]),
                    
                    })
               
        
        start_date = start_date
        end_date = end_date
        print start_date
        all_aktif = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10'))
        noa_all_aktif = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).count()
        total_nominal_hp= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(barang__jenis_barang=1)
        total_hp = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(barang__jenis_barang=1).count()
        total_nominal_laptop= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(barang__jenis_barang=2)
        total_laptop = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(barang__jenis_barang=2).count()
        total_nominal_kamera= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(barang__jenis_barang=3)
        total_kamera = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(barang__jenis_barang=3).count()
        total_nominal_ps= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(barang__jenis_barang=4)
        total_ps = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(barang__jenis_barang=4).count()
        total_nominal_tv= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(barang__jenis_barang=5)
        total_tv = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(barang__jenis_barang=5).count()
        total_nominal_motor= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(barang__jenis_kendaraan=1)
        total_motor = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(barang__jenis_kendaraan=1).count()
        total_nominal_mobil= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(barang__jenis_kendaraan=2)
        total_mobil = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).filter(barang__jenis_kendaraan=2).count()
        
        all_lapur = AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6")
        noa_all_lapur = AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").count()
        lpr_total_nominal_hp= AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=1)
        lpr_total_hp = AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=1).count()
        lpr_total_nominal_laptop= AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=2)
        lpr_total_laptop = AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=2).count()
        lpr_total_nominal_kamera= AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=3)
        lpr_total_kamera = AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=3).count()
        lpr_total_nominal_ps= AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=4)
        lpr_total_ps = AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=4).count()
        lpr_total_nominal_tv= AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=5)
        lpr_total_tv = AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=5).count()
        lpr_total_nominal_motor= AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_kendaraan=1)
        lpr_total_motor = AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_kendaraan=1).count()
        lpr_total_nominal_mobil= AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_kendaraan=2)
        lpr_total_mobil = AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_kendaraan=2).count()
        template = 'manop/filter/rekap_barang_aktif_dan_lapur.html'
        variables = RequestContext(request, {'plns': plns ,'start_date':start_date,'end_date':end_date,
                                             'total_barang':noa_all_aktif,
                                             'total_nominal_all_barang':float(sum([a.nilai for a in all_aktif])),
                                             'total_hp':total_hp,'total_nominal_hp':sum([a.nilai for a in total_nominal_hp]),
                                             'total_laptop':total_laptop,'total_nominal_laptop':sum([a.nilai for a in total_nominal_laptop]),
                                             'total_kamera':total_kamera,'total_nominal_kamera':sum([a.nilai for a in total_nominal_kamera]),
                                             'total_ps':total_ps,'total_nominal_ps':sum([a.nilai for a in total_nominal_ps]),
                                             'total_tv':total_tv,'total_nominal_tv':sum([a.nilai for a in total_nominal_tv]),
                                             'total_motor':total_motor,'total_nominal_motor':sum([a.nilai for a in total_nominal_motor]),
                                             'total_mobil':total_mobil,'total_nominal_mobil':sum([a.nilai for a in total_nominal_mobil]),
                                             
                                             'lpr':lpr,
                                             'lpr_total_barang':noa_all_lapur,
                                             'lpr_total_nominal_all_barang':float(sum([a.nilai for a in all_lapur])),
                                             'lpr_total_hp':lpr_total_hp,'lpr_total_nominal_hp':sum([a.nilai for a in lpr_total_nominal_hp]),
                                             'lpr_total_laptop':lpr_total_laptop,'lpr_total_nominal_laptop':sum([a.nilai for a in lpr_total_nominal_laptop]),
                                             'lpr_total_kamera':lpr_total_kamera,'lpr_total_nominal_kamera':sum([a.nilai for a in lpr_total_nominal_kamera]),
                                             'lpr_total_ps':lpr_total_ps,'lpr_total_nominal_ps':sum([a.nilai for a in lpr_total_nominal_ps]),
                                             'lpr_total_tv':lpr_total_tv,'lpr_total_nominal_tv':sum([a.nilai for a in lpr_total_nominal_tv]),
                                             'lpr_total_motor':lpr_total_motor,'lpr_total_nominal_motor':sum([a.nilai for a in lpr_total_nominal_motor]),
                                             'lpr_total_mobil':lpr_total_mobil,'lpr_total_nominal_mobil':sum([a.nilai for a in lpr_total_nominal_mobil]),
                                             })
        return render_to_response(template, variables)
    ##---
    if 'start_date' in request.GET and request.GET['start_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']        
        trans = []
        for k in rekap:
            if k.akadgadai_set.filter(status_transaksi=None).filter(tanggal__range=(start_date,end_date)).count()>=0:
                plns.append({'k':k,'kode_cabang':k.kode_cabang,'nama_cabang':k.nama_cabang,
                    'all_barang':k.all_barang(start_date,end_date),'nominal_all_barang':sum([p.nilai for p in k.nominal_all_barang(start_date,end_date)]),
                    'hp':k.hp_filter(start_date,end_date),'nominal_hp':sum([p.nilai for p in k.nominal_hp_filter(start_date,end_date)]),
                    'laptop':k.laptop_filter(start_date,end_date),'nominal_laptop':sum([p.nilai for p in k.nominal_laptop_filter(start_date,end_date)]),
                    'kamera':k.kamera_filter(start_date,end_date),'nominal_kamera':sum([p.nilai for p in k.nominal_kamera_filter(start_date,end_date)]),
                    'ps':k.ps_filter(start_date,end_date),'nominal_ps':sum([p.nilai for p in k.nominal_ps_filter(start_date,end_date)]),
                    'tv':k.tv_filter(start_date,end_date),'nominal_tv':sum([p.nilai for p in k.nominal_tv_filter(start_date,end_date)]),
                    'motor':k.motor_filter(start_date,end_date),'nominal_motor':sum([p.nilai for p in k.nominal_motor_filter(start_date,end_date)]),
                    'mobil':k.mobil_filter(start_date,end_date),'nominal_mobil':sum([p.nilai for p in k.nominal_mobil_filter(start_date,end_date)]),
                    
                    })
        
        for l in rekap:
            if l.akadgadai_set.filter(status_transaksi= 6).filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').count()>=0:
                lpr.append({'l':l,'kode_cabang':l.kode_cabang,'nama_cabang':l.nama_cabang,
                    'all_barang':l.lpr_all_barang(start_date,end_date),'nominal_all_barang':sum([p.nilai for p in l.lpr_nominal_all_barang(start_date,end_date)]),
                    'hp':l.lpr_hp_filter(start_date,end_date),'nominal_hp':sum([p.nilai for p in l.lpr_nominal_hp_filter(start_date,end_date)]),
                    'laptop':l.lpr_laptop_filter(start_date,end_date),'nominal_laptop':sum([p.nilai for p in l.lpr_nominal_laptop_filter(start_date,end_date)]),
                    'kamera':l.lpr_kamera_filter(start_date,end_date),'nominal_kamera':sum([p.nilai for p in l.lpr_nominal_kamera_filter(start_date,end_date)]),
                    'ps':l.lpr_ps_filter(start_date,end_date),'nominal_ps':sum([p.nilai for p in l.lpr_nominal_ps_filter(start_date,end_date)]),
                    'tv':l.lpr_tv_filter(start_date,end_date),'nominal_tv':sum([p.nilai for p in l.lpr_nominal_tv_filter(start_date,end_date)]),
                    'motor':l.lpr_motor_filter(start_date,end_date),'nominal_motor':sum([p.nilai for p in l.lpr_nominal_motor_filter(start_date,end_date)]),
                    'mobil':l.lpr_mobil_filter(start_date,end_date),'nominal_mobil':sum([p.nilai for p in l.lpr_nominal_mobil_filter(start_date,end_date)]),
                    
                    })
               
        
        start_date = start_date
        end_date = end_date
        print start_date
        all_aktif = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(status_transaksi=None)
        noa_all_aktif = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(status_transaksi=None).count()
        total_nominal_hp= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(status_transaksi=None).filter(barang__jenis_barang=1)
        total_hp = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(status_transaksi=None).filter(barang__jenis_barang=1).count()
        total_nominal_laptop= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(status_transaksi=None).filter(barang__jenis_barang=2)
        total_laptop = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(status_transaksi=None).filter(barang__jenis_barang=2).count()
        total_nominal_kamera= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(status_transaksi=None).filter(barang__jenis_barang=3)
        total_kamera = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(status_transaksi=None).filter(barang__jenis_barang=3).count()
        total_nominal_ps= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(status_transaksi=None).filter(barang__jenis_barang=4)
        total_ps = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(status_transaksi=None).filter(barang__jenis_barang=4).count()
        total_nominal_tv= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(status_transaksi=None).filter(barang__jenis_barang=5)
        total_tv = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(status_transaksi=None).filter(barang__jenis_barang=5).count()
        total_nominal_motor= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(status_transaksi=None).filter(barang__jenis_kendaraan=1)
        total_motor = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(status_transaksi=None).filter(barang__jenis_kendaraan=1).count()
        total_nominal_mobil= AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(status_transaksi=None).filter(barang__jenis_kendaraan=2)
        total_mobil = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(status_transaksi=None).filter(barang__jenis_kendaraan=2).count()
        
        all_lapur = AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6")
        noa_all_lapur = AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").count()
        lpr_total_nominal_hp= AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=1)
        lpr_total_hp = AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=1).count()
        lpr_total_nominal_laptop= AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=2)
        lpr_total_laptop = AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=2).count()
        lpr_total_nominal_kamera= AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=3)
        lpr_total_kamera = AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=3).count()
        lpr_total_nominal_ps= AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=4)
        lpr_total_ps = AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=4).count()
        lpr_total_nominal_tv= AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=5)
        lpr_total_tv = AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_barang=5).count()
        lpr_total_nominal_motor= AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_kendaraan=1)
        lpr_total_motor = AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_kendaraan=1).count()
        lpr_total_nominal_mobil= AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_kendaraan=2)
        lpr_total_mobil = AkadGadai.objects.filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').filter(status_transaksi="6").filter(barang__jenis_kendaraan=2).count()
        template1 = 'manop/filter/cetak_barang_aktif_dan_lapur.html'
        variables = RequestContext(request, {'plns': plns ,'start_date':start_date,'end_date':end_date,
                                             'total_barang':noa_all_aktif,
                                             'total_nominal_all_barang':float(sum([a.nilai for a in all_aktif])),
                                             'total_hp':total_hp,'total_nominal_hp':sum([a.nilai for a in total_nominal_hp]),
                                             'total_laptop':total_laptop,'total_nominal_laptop':sum([a.nilai for a in total_nominal_laptop]),
                                             'total_kamera':total_kamera,'total_nominal_kamera':sum([a.nilai for a in total_nominal_kamera]),
                                             'total_ps':total_ps,'total_nominal_ps':sum([a.nilai for a in total_nominal_ps]),
                                             'total_tv':total_tv,'total_nominal_tv':sum([a.nilai for a in total_nominal_tv]),
                                             'total_motor':total_motor,'total_nominal_motor':sum([a.nilai for a in total_nominal_motor]),
                                             'total_mobil':total_mobil,'total_nominal_mobil':sum([a.nilai for a in total_nominal_mobil]),
                                             
                                             'lpr':lpr,
                                             'lpr_total_barang':noa_all_lapur,
                                             'lpr_total_nominal_all_barang':float(sum([a.nilai for a in all_lapur])),
                                             'lpr_total_hp':lpr_total_hp,'lpr_total_nominal_hp':sum([a.nilai for a in lpr_total_nominal_hp]),
                                             'lpr_total_laptop':lpr_total_laptop,'lpr_total_nominal_laptop':sum([a.nilai for a in lpr_total_nominal_laptop]),
                                             'lpr_total_kamera':lpr_total_kamera,'lpr_total_nominal_kamera':sum([a.nilai for a in lpr_total_nominal_kamera]),
                                             'lpr_total_ps':lpr_total_ps,'lpr_total_nominal_ps':sum([a.nilai for a in lpr_total_nominal_ps]),
                                             'lpr_total_tv':lpr_total_tv,'lpr_total_nominal_tv':sum([a.nilai for a in lpr_total_nominal_tv]),
                                             'lpr_total_motor':lpr_total_motor,'lpr_total_nominal_motor':sum([a.nilai for a in lpr_total_nominal_motor]),
                                             'lpr_total_mobil':lpr_total_mobil,'lpr_total_nominal_mobil':sum([a.nilai for a in lpr_total_nominal_mobil]),
                                             })
        return render_to_response(template1, variables)

    elif  'start_date' in request.GET and request.GET['start_date'] and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        start_date = start_date
        end_date = end_date        
        trans = []
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 0, 'fg_color': '#D7E4BC'})        
        
        money_format = workbook.add_format({'num_format': '#,##0'})
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        #merge_format = workbook.add_format({'bold':True, 'border':6,'align':'center','valign':'vcenter'})
        merge_format = workbook.add_format({'bold': 1,'border': 6,'align': 'center','valign': 'vcenter','fg_color': '#D7E4BC'})
        merge_format1 = workbook.add_format({'bold': 1,'border': 6,'align': 'center','valign': 'vcenter','fg_color': '#C0C0C0'})
        bold1 = workbook.add_format({'bold': 0, 'fg_color': '#C0C0C0'})        

        #worksheet.merge_range('A1:O1', 'Transaksi Pencairan Div Pjb', merge_format)
        #worksheet.merge_range('A2:O2', 'Periode :'+ start_date + " s.d " + end_date, merge_format)
        worksheet.set_column(0, 0, 6) 
        worksheet.set_column(1, 1, 18)
        worksheet.set_column(2, 2, 10)
        worksheet.set_column(3, 3, 10)
        worksheet.set_column(4, 4, 10)
        worksheet.set_column(5, 5, 10)
        worksheet.set_column(6, 6, 10)
        worksheet.set_column(7, 7, 10)
        worksheet.set_column(8, 7, 10)
        worksheet.set_column(9, 9, 10)
        worksheet.set_column(10, 10, 10)
        worksheet.set_column(11, 11, 11)
        worksheet.set_column(12, 12, 12)
        worksheet.set_column(13, 13, 13)
        worksheet.set_column(14, 14, 14)

        #worksheet.merge_range('A1:O1', 'REKAP BARANG AKTIF DAN BARANG LAPUR', merge_format)
        worksheet.merge_range('A1:R1', 'REKAP BARANG AKTIF', merge_format)
        worksheet.merge_range('A2:R2', 'Periode :'+ start_date + " s.d " + end_date, merge_format)
        worksheet.merge_range('A3:A4', 'KODE', merge_format)
        worksheet.merge_range('B3:B4', 'GERAI', merge_format)
        worksheet.merge_range('C3:R3', 'AKTIF', merge_format)
        worksheet.write('C4', 'Jml Barang', bold)
        worksheet.write('D4', 'Nominal Barang', bold)
        worksheet.write('E4', 'HP', bold)
        worksheet.write('F4', 'Nominal HP', bold)
        worksheet.write('G4', 'Laptop', bold)
        worksheet.write('H4', 'Nominal Laptop', bold)
        worksheet.write('I4', 'Kamera', bold)
        worksheet.write('J4', 'Nominal Kamera', bold)
        worksheet.write('K4', 'PS', bold)
        worksheet.write('L4', 'Nominal PS', bold)
        worksheet.write('M4', 'TV', bold)
        worksheet.write('N4', 'Nominal TV', bold)
        worksheet.write('O4', 'Motor', bold)
        worksheet.write('P4', 'Nominal Motor', bold)
        worksheet.write('Q4', 'Mobil', bold)
        worksheet.write('R4', 'Nominal Mobil', bold)
        row = 4
        col = 0


        for k in rekap:
            if k.akadgadai_set.filter(status_transaksi=None).filter(tanggal__range=(start_date,end_date)).count()>=0:
                plns.append({'k':k,'aktif':k.aktif_nasabah_harian_filter(start_date,end_date),'kode_cabang':k.kode_cabang,\
                    'nama_cabang':k.nama_cabang,'all_barang':k.all_barang(start_date,end_date),\
                    'nominal_all_barang':sum([p.nilai for p in k.nominal_all_barang(start_date,end_date)]),
                    'hp':k.hp_filter(start_date,end_date),'nominal_hp':sum([p.nilai for p in k.nominal_hp_filter(start_date,end_date)]),
                    'laptop':k.laptop_filter(start_date,end_date),\
                    'nominal_laptop':sum([p.nilai for p in k.nominal_laptop_filter(start_date,end_date)]),
                    'kamera':k.kamera_filter(start_date,end_date),\
                    'nominal_kamera':sum([p.nilai for p in k.nominal_kamera_filter(start_date,end_date)]),
                    'ps':k.ps_filter(start_date,end_date),'nominal_ps':sum([p.nilai for p in k.nominal_ps_filter(start_date,end_date)]),
                    'tv':k.tv_filter(start_date,end_date),'nominal_tv':sum([p.nilai for p in k.nominal_tv_filter(start_date,end_date)]),
                    'motor':k.motor_filter(start_date,end_date),'nominal_motor':sum([p.nilai for p in k.nominal_motor_filter(start_date,end_date)]),
                    'mobil':k.mobil_filter(start_date,end_date),\
                    'nominal_mobil':sum([p.nilai for p in k.nominal_mobil_filter(start_date,end_date)]),                  
                    })              
       
                start_date = start_date
                end_date = end_date
                worksheet.write_string(row, col , k.kode_cabang )
                worksheet.write_string(row, col + 1, k.nama_cabang)
                worksheet.write_number(row, col + 2, k.all_barang(start_date,end_date), money_format)
                worksheet.write_number(row, col + 3, sum([p.nilai for p in k.nominal_all_barang(start_date,end_date)]), money_format)
                worksheet.write_number(row, col + 4, k.hp_filter(start_date,end_date), money_format)
                worksheet.write_number(row, col + 5, sum([p.nilai for p in k.nominal_hp_filter(start_date,end_date)]), money_format)
                worksheet.write_number(row, col + 6, k.laptop_filter(start_date,end_date),money_format)
                worksheet.write_number(row, col + 7, sum([p.nilai for p in k.nominal_laptop_filter(start_date,end_date)]),money_format)
                worksheet.write_number(row, col + 8, k.kamera_filter(start_date,end_date),money_format)
                worksheet.write_number(row, col + 9, sum([p.nilai for p in k.nominal_kamera_filter(start_date,end_date)]),money_format)
                worksheet.write_number(row, col + 10, k.ps_filter(start_date,end_date),money_format)
                worksheet.write_number(row, col + 11, sum([p.nilai for p in k.nominal_ps_filter(start_date,end_date)]),money_format)
                worksheet.write_number(row, col + 12, k.tv_filter(start_date,end_date),money_format)
                worksheet.write_number(row, col + 13, sum([p.nilai for p in k.nominal_tv_filter(start_date,end_date)]),money_format)
                worksheet.write_number(row, col + 14, k.motor_filter(start_date,end_date),money_format)
                worksheet.write_number(row, col + 15, sum([p.nilai for p in k.nominal_motor_filter(start_date,end_date)]),money_format)
                worksheet.write_number(row, col + 16, k.mobil_filter(start_date,end_date),money_format)
                worksheet.write_number(row, col + 17, sum([p.nilai for p in k.nominal_mobil_filter(start_date,end_date)]),money_format)


                row += 1
        worksheet.write(row, 0, 'Total', bold)
        worksheet.write(row, 2, '=SUM(C5:C25)', money_format)
        worksheet.write(row, 3, '=SUM(D5:D25)', money_format)
        worksheet.write(row, 4, '=SUM(E5:E25)', money_format)
        worksheet.write(row, 5, '=SUM(F5:F25)', money_format)
        worksheet.write(row, 6, '=SUM(G5:G25)', money_format)
        worksheet.write(row, 7, '=SUM(H5:H25)', money_format)
        worksheet.write(row, 8, '=SUM(I5:I25)', money_format)
        worksheet.write(row, 9, '=SUM(J5:J25)', money_format)
        worksheet.write(row, 10, '=SUM(K5:K25)', money_format)
        worksheet.write(row, 11, '=SUM(L5:L25)', money_format)
        worksheet.write(row, 12, '=SUM(M5:M25)', money_format)
        worksheet.write(row, 13, '=SUM(N5:N25)', money_format)
        worksheet.write(row, 14, '=SUM(O5:O25)', money_format)
        worksheet.write(row, 15, '=SUM(P5:P25)', money_format)
        worksheet.write(row, 16, '=SUM(Q5:Q25)', money_format)
        worksheet.write(row, 17, '=SUM(R5:R25)', money_format)
        workbook.close()    
        output.seek(0)    
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=rekap_barang_aktif.xlsx" #filename=rekap_barang_aktif_dan_lapur.xlsx"    
        return response

    elif  'start_date' in request.GET and request.GET['start_date'] and 'submit_empat' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        start_date = start_date
        end_date = end_date        
        trans = []
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 0, 'fg_color': '#D7E4BC'})        
        
        money_format = workbook.add_format({'num_format': '#,##0'})
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        #merge_format = workbook.add_format({'bold':True, 'border':6,'align':'center','valign':'vcenter'})
        merge_format = workbook.add_format({'bold': 1,'border': 6,'align': 'center','valign': 'vcenter','fg_color': '#D7E4BC'})
        merge_format1 = workbook.add_format({'bold': 1,'border': 6,'align': 'center','valign': 'vcenter','fg_color': '#C0C0C0'})
        bold1 = workbook.add_format({'bold': 0, 'fg_color': '#C0C0C0'})        


        worksheet.set_column(0, 0, 6) 
        worksheet.set_column(1, 1, 18)
        worksheet.set_column(2, 2, 10)
        worksheet.set_column(3, 3, 10)
        worksheet.set_column(4, 4, 10)
        worksheet.set_column(5, 5, 10)
        worksheet.set_column(6, 6, 10)
        worksheet.set_column(7, 7, 10)
        worksheet.set_column(8, 7, 10)
        worksheet.set_column(9, 9, 10)
        worksheet.set_column(10, 10, 10)
        worksheet.set_column(11, 11, 11)
        worksheet.set_column(12, 12, 12)
        worksheet.set_column(13, 13, 13)
        worksheet.set_column(14, 14, 14)

        worksheet.merge_range('A1:R1', 'REKAP BARANG AYDA', merge_format)
        worksheet.merge_range('A2:R2', 'Periode :'+ start_date + " s.d " + end_date, merge_format)        
        worksheet.merge_range('A3:A4', 'KODE', merge_format)
        worksheet.merge_range('B3:B4', 'GERAI', merge_format)
        worksheet.merge_range('C3:R3', 'LAPUR', merge_format)
        worksheet.write('C4', 'Jml Barang', bold)
        worksheet.write('D4', 'Nominal Barang', bold)
        worksheet.write('E4', 'HP', bold)
        worksheet.write('F4', 'Nominal HP', bold)
        worksheet.write('G4', 'Laptop', bold)
        worksheet.write('H4', 'Nominal Laptop', bold)
        worksheet.write('I4', 'Kamera', bold)
        worksheet.write('J4', 'Nominal Kamera', bold)
        worksheet.write('K4', 'PS', bold)
        worksheet.write('L4', 'Nominal PS', bold)
        worksheet.write('M4', 'TV', bold)
        worksheet.write('N4', 'Nominal TV', bold)
        worksheet.write('O4', 'Motor', bold)
        worksheet.write('P4', 'Nominal Motor', bold)
        worksheet.write('Q4', 'Mobil', bold)
        worksheet.write('R4', 'Nominal Mobil', bold)
    
        row = 4
        col = 0

            
        for l in rekap:
            if l.akadgadai_set.filter(status_transaksi= '6').filter(lapur__tanggal__range=(start_date,end_date),lapur__status = '1').count()>=0:
                lpr.append({'l':l,'kode_cabang':l.kode_cabang,'nama_cabang':l.nama_cabang,
                    'all_barang':l.lpr_all_barang(start_date,end_date),'nominal_all_barang':sum([p.nilai for p in l.lpr_nominal_all_barang(start_date,end_date)]),
                    'hp':l.lpr_hp_filter(start_date,end_date),'nominal_hp':sum([p.nilai for p in l.lpr_nominal_hp_filter(start_date,end_date)]),
                    'laptop':l.lpr_laptop_filter(start_date,end_date),'nominal_laptop':sum([p.nilai for p in l.lpr_nominal_laptop_filter(start_date,end_date)]),
                    'kamera':l.lpr_kamera_filter(start_date,end_date),'nominal_kamera':sum([p.nilai for p in l.lpr_nominal_kamera_filter(start_date,end_date)]),
                    'ps':l.lpr_ps_filter(start_date,end_date),'nominal_ps':sum([p.nilai for p in l.lpr_nominal_ps_filter(start_date,end_date)]),
                    'tv':l.lpr_tv_filter(start_date,end_date),'nominal_tv':sum([p.nilai for p in l.lpr_nominal_tv_filter(start_date,end_date)]),
                    'motor':l.lpr_motor_filter(start_date,end_date),'nominal_motor':sum([p.nilai for p in l.lpr_nominal_motor_filter(start_date,end_date)]),
                    'mobil':l.lpr_mobil_filter(start_date,end_date),'nominal_mobil':sum([p.nilai for p in l.lpr_nominal_mobil_filter(start_date,end_date)]),
                    
                    })        

                start_date = start_date
                end_date = end_date
                worksheet.write_string(row, col , l.kode_cabang)
                worksheet.write_string(row, col + 1, l.nama_cabang)
                worksheet.write_number(row, col + 2, l.lpr_all_barang(start_date,end_date),money_format)
                worksheet.write_number(row, col + 3, sum([p.nilai for p in l.lpr_nominal_all_barang(start_date,end_date)]), money_format)
                worksheet.write_number(row, col + 4, l.lpr_hp_filter(start_date,end_date), money_format)
                worksheet.write_number(row, col + 5, sum([p.nilai for p in l.lpr_nominal_hp_filter(start_date,end_date)]), money_format)
                worksheet.write_number(row, col + 6, l.lpr_laptop_filter(start_date,end_date), money_format)
                worksheet.write_number(row, col + 7, sum([p.nilai for p in l.lpr_nominal_laptop_filter(start_date,end_date)]),money_format)
                worksheet.write_number(row, col + 8, l.lpr_kamera_filter(start_date,end_date),money_format)
                worksheet.write_number(row, col + 9, sum([p.nilai for p in l.lpr_nominal_kamera_filter(start_date,end_date)]),money_format)
                worksheet.write_number(row, col + 10, l.lpr_ps_filter(start_date,end_date),money_format)
                worksheet.write_number(row, col + 11, sum([p.nilai for p in l.lpr_nominal_ps_filter(start_date,end_date)]),money_format)
                worksheet.write_number(row, col + 12, l.lpr_tv_filter(start_date,end_date),money_format)
                worksheet.write_number(row, col + 13, sum([p.nilai for p in l.lpr_nominal_tv_filter(start_date,end_date)]),money_format)
                worksheet.write_number(row, col + 14, l.lpr_motor_filter(start_date,end_date),money_format)
                worksheet.write_number(row, col + 15, sum([p.nilai for p in l.lpr_nominal_motor_filter(start_date,end_date)]),money_format)
                worksheet.write_number(row, col + 16, l.lpr_mobil_filter(start_date,end_date),money_format)
                worksheet.write_number(row, col + 17, sum([p.nilai for p in l.lpr_nominal_mobil_filter(start_date,end_date)]),money_format)

                row += 1
        worksheet.write(row, 0, 'Total', bold)
        worksheet.write(row, 2, '=SUM(C5:C25)', money_format)
        worksheet.write(row, 3, '=SUM(D5:D25)', money_format)
        worksheet.write(row, 4, '=SUM(E5:E25)', money_format)
        worksheet.write(row, 5, '=SUM(F5:F25)', money_format)
        worksheet.write(row, 6, '=SUM(G5:G25)', money_format)
        worksheet.write(row, 7, '=SUM(H5:H25)', money_format)
        worksheet.write(row, 8, '=SUM(I5:I25)', money_format)
        worksheet.write(row, 9, '=SUM(J5:J25)', money_format)
        worksheet.write(row, 10, '=SUM(K5:K25)', money_format)
        worksheet.write(row, 11, '=SUM(L5:L25)', money_format)
        worksheet.write(row, 12, '=SUM(M5:M25)', money_format)
        worksheet.write(row, 13, '=SUM(N5:N25)', money_format)
        worksheet.write(row, 14, '=SUM(O5:O25)', money_format)
        worksheet.write(row, 15, '=SUM(P5:P25)', money_format)
        worksheet.write(row, 16, '=SUM(Q5:Q25)', money_format)
        worksheet.write(row, 17, '=SUM(R5:R25)', money_format)
        workbook.close()    
        output.seek(0)    
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=rekap_barang_lapur.xlsx"    
        return response

    else:
        template='manop/filter/rekap_barang_aktif_dan_lapur.html'
        variable = RequestContext(request,{'form':form})
        return render_to_response(template,variable)

@login_required
@user_passes_test(is_in_multiple_groups)
def perpanjangan_gerai(request):
    kp = []
    #nacab = Tbl_Cabang.objects.get(kode_cabang=object_id)
    #kocab = object_id
    #akad= Pelunasan.objects.filter(lunas__isnull = False)
    start_date = None
    end_date = None
    form = AkadGadaiForm()
    all = []
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET :
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        
        if id_cabang == '500' :
            akad= Perpanjang.objects.filter(agkredit__lunas__isnull = True).filter(tanggal__range=(start_date,end_date)).order_by('gerai')
            for k in akad:
                kp.append(k)
                
                start_date = start_date
                end_date = end_date
                id_cabang = id_cabang
            template='manop/perpanjang/rekap_perpanjang_hari.html'
            variable = RequestContext(request,{'tes':kp,
            'form':form,'id_cabang':id_cabang,'start_date':start_date,'end_date':end_date,
            'start_date':start_date,
            'end_date':end_date,
            'nilai': sum([b.nilai for b in kp ]),
            #'jasa': sum([b.jasa for b in kp ]),
            #'adm': sum([b.adm for b in kp ]),
            #'simpan': sum([b.biayasimpan for b in kp ]),
            #'bersih' : sum([b.jumlah_biaya for b in kp ]),
            })
            return render_to_response(template,variable)
        else:
            akad= Perpanjang.objects.filter(agkredit__lunas__isnull = True).filter(tanggal__range=(start_date,end_date)).filter(gerai__id = id_cabang)
            for k in akad:
                kp.append(k)
                start_date = start_date
                end_date = end_date
                id_cabang = id_cabang
            template= 'manop/perpanjang/rekap_perpanjang_hari.html'
            variable = RequestContext(request,{'tes':kp,
            'form':form,'id_cabang':id_cabang,
            'start_date':start_date,
            'end_date':end_date,
            'nilai': sum([b.nilai for b in kp ]),
            #'jasa': sum([b.jasa for b in kp ]),
            #'adm': sum([b.adm for b in kp ]),
            #'simpan': sum([b.biayasimpan for b in kp ]),
            #'bersih' : sum([b.jumlah_biaya for b in kp ]),
            })
            return render_to_response(template,variable)
    
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            akad= Perpanjang.objects.filter(agkredit__lunas__isnull = True).filter(tanggal__range=(start_date,end_date)).order_by('gerai')
            for k in akad:
                kp.append(k)
            template1= 'manop/perpanjang/cetak_perpanjang_hari.html'
            variable = RequestContext(request,{'tes':kp,
            'form':form,
            'start_date':start_date,
            'end_date':end_date,
            'id_cabang':id_cabang,
            'nilai': sum([b.nilai for b in kp ]),
 
            })
            return render_to_response(template1,variable)
        else:
            akad= Perpanjang.objects.filter(agkredit__lunas__isnull = True).filter(tanggal__range=(start_date,end_date)).filter(gerai__id = id_cabang)
            for k in akad:
                kp.append(k)
            template1= 'manop/perpanjang/cetak_perpanjang_hari.html'
            variable = RequestContext(request,{'tes':kp,
            'form':form,'id_cabang':id_cabang,
            'start_date':start_date,
            'end_date':end_date,
            'nilai': sum([b.nilai for b in kp ]),
            })
            return render_to_response(template1,variable)

    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']         
        if id_cabang == '500' :
            akad= Perpanjang.objects.filter(agkredit__lunas__isnull = True).filter(tanggal__range=(start_date,end_date)).order_by('gerai')
            for k in akad:
                kp.append(k)
            a = sum([b.agkredit.nilai for b in kp ])
            c = sum([b.agkredit.jasa for b in kp ]) 
            d = sum([b.agkredit.adm for b in kp ]) 
            e = sum([b.agkredit.biayasimpan for b in kp ])
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
            worksheet.set_column(10, 10, 10)
            worksheet.set_column(11, 11, 10)
            worksheet.set_column(12, 12, 10)
            worksheet.set_column(13, 13, 10)
            worksheet.set_column(14, 14, 10)
            worksheet.set_column(15, 15, 10)
            worksheet.set_column(16, 16, 10)
            worksheet.set_column(17, 17, 10)
            worksheet.set_column(18, 18, 10)
            worksheet.set_column(19, 19, 10)
            worksheet.set_column(20, 20, 10)
            worksheet.set_column(21, 21, 10)
            worksheet.set_column(22, 22, 10)
        
            worksheet.merge_range('A1:T1', 'LAPORAN PERPANJANGAN ', merge_format1)
            worksheet.merge_range('A2:T2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Nama', merge_format)
            worksheet.merge_range('C4:C5', 'No Identitas', merge_format)
            worksheet.merge_range('D4:D5', 'Tempat Lahir', merge_format)
            worksheet.merge_range('E4:E5', 'Tgl Lahir', merge_format)
            worksheet.merge_range('F4:F5', 'Jenis Kelamin', merge_format)
            worksheet.merge_range('G4:G5', 'No Tlp', merge_format)
            worksheet.merge_range('H4:H5', 'Alamat Identitas', merge_format)
            worksheet.merge_range('I4:I5', 'Alamat Domisili', merge_format)
            worksheet.merge_range('J4:J5', 'No Tlp Domisili', merge_format)
            worksheet.merge_range('K4:K5', 'Gerai', merge_format)
            worksheet.merge_range('L4:L5', 'Tgl Perpanjang', merge_format)
            worksheet.merge_range('M4:M5', 'JW (hari)', merge_format)
            worksheet.merge_range('N4:N5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('O4:O5', 'Jenis Transaksi', merge_format)
            worksheet.merge_range('P4:P5', 'Barang', merge_format)
            worksheet.merge_range('Q4:Q5', 'Nilai', merge_format)
            worksheet.merge_range('R4:T4', 'Pendapatan (Rp)', merge_format)
            worksheet.write('R5', 'Jasa (Rp)',  bold1)
            worksheet.write('S5', 'Adm (Rp)', bold1)
            worksheet.write('T5', 'Bea Simpan (Rp)', bold1)

            row = 5
            col = 0
            for t in kp:
                worksheet.write_string(row, col , t.agkredit.norek() )
                worksheet.write_string(row, col + 1 , t.agkredit.agnasabah.nama)
                
                
                worksheet.write_string(row, col + 2 , t.agkredit.agnasabah.no_ktp)
                worksheet.write_string(row, col + 3 , t.agkredit.agnasabah.tempat)
                worksheet.write_datetime(row, col + 4 , t.agkredit.agnasabah.tgl_lahir,date_format)
                worksheet.write_string(row, col + 5 ,t.agkredit.agnasabah.jenis_kelamin )
                worksheet.write_string(row, col + 6 ,t.agkredit.agnasabah.telepon_ktp + ' ' + '/' +  ' ' +t.agkredit.agnasabah.hp_ktp )
                worksheet.write_string(row, col + 7 , t.agkredit.agnasabah.alamat_ktp  + ' ' + 'No' + ' ' + t.agkredit.agnasabah.no_rumah_ktp + ' ' + 'Rt' + ' ' + t.agkredit.agnasabah.rt_ktp + ' ' + 'Rw' + ' ' + t.agkredit.agnasabah.rw_ktp + ' ' + ' Kelurahan' +' ' + t.agkredit.agnasabah.kelurahan_ktp + ' ' + ' kecamatan' + ' ' + t.agkredit.agnasabah.kecamatan_ktp )
                worksheet.write_string(row, col + 8 ,t.agkredit.agnasabah.alamat_domisili + ' ' + 'No ' + ' ' + t.agkredit.agnasabah.no_rumah_domisili + ' ' + 'Rt' +' ' + t.agkredit.agnasabah.rt_domisili + ' ' + 'Rw' + ' ' + t.agkredit.agnasabah.rw_domisili + ' ' + 'Kelurahan' + ' ' +t.agkredit.agnasabah.kelurahan_domisili + ' ' + 'Kecamatan' + ' ' + t.agkredit.agnasabah.kecamatan_domisili + ' ' + 'Kota Madya' + ' ' + t.agkredit.agnasabah.kotamadya_domisili + ' ' + 'Kabupaten' + ' ' + t.agkredit.agnasabah.kabupaten_domisili )
                worksheet.write_string(row, col + 9 , t.agkredit.agnasabah.hp_domisili + ' ' + '-' + ' ' +t.agkredit.agnasabah.telepon_domisili)
            
                worksheet.write_string(row, col + 10 , t.gerai.nama)
                worksheet.write_datetime(row, col + 11 , t.tanggal,date_format)
                worksheet.write_number(row, col + 12, t.agkredit.jw_all(), money_format)
                worksheet.write_datetime(row, col + 13, t.agkredit.jatuhtempo, date_format)
                worksheet.write_number(row, col + 14, t.agkredit.jenis_transaksi,money_format)
                worksheet.write_string(row, col + 15, t.agkredit.__unic_barang__())
                worksheet.write_number(row, col + 16, t.agkredit.nilai, money_format)
                worksheet.write_number(row, col + 17, t.agkredit.jasa, money_format)
                worksheet.write_number(row, col + 18, t.agkredit.adm, money_format)
                worksheet.write_number(row, col + 19, t.agkredit.biayasimpan, money_format)
                row += 1

            worksheet.write(row,4, 'Total', bold)    
            worksheet.write(row,16, a, money_format)
            worksheet.write(row, 17, c, money_format)
            worksheet.write(row, 18, d, money_format)
            worksheet.write(row, 19, e, money_format)
       
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Laporan_Perpanjangan_gabungan.xlsx"
            return response
        else:
            akad= Perpanjang.objects.filter(agkredit__lunas__isnull = True).filter(tanggal__range=(start_date,end_date)).filter(gerai__id = id_cabang)
            for k in akad:
                kp.append(k)
            a = sum([b.agkredit.nilai for b in kp ])
            c = sum([b.agkredit.jasa for b in kp ]) 
            d = sum([b.agkredit.adm for b in kp ]) 
            e = sum([b.agkredit.biayasimpan for b in kp ])
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
            worksheet.set_column(10, 10, 10)
            worksheet.set_column(11, 11, 10)
            worksheet.set_column(12, 12, 10)
            worksheet.set_column(13, 13, 10)
            worksheet.set_column(14, 14, 10)
            worksheet.set_column(15, 15, 10)
            worksheet.set_column(16, 16, 10)
            worksheet.set_column(17, 17, 10)
            worksheet.set_column(18, 18, 10)
            worksheet.set_column(19, 19, 10)
            worksheet.set_column(20, 20, 10)
            worksheet.set_column(21, 21, 10)
            worksheet.set_column(22, 22, 10)
        
            worksheet.merge_range('A1:T1', 'LAPORAN PERPANJANGAN ', merge_format1)
            worksheet.merge_range('A2:T2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Nama', merge_format)
            worksheet.merge_range('C4:C5', 'No Identitas', merge_format)
            worksheet.merge_range('D4:D5', 'Tempat Lahir', merge_format)
            worksheet.merge_range('E4:E5', 'Tgl Lahir', merge_format)
            worksheet.merge_range('F4:F5', 'Jenis Kelamin', merge_format)
            worksheet.merge_range('G4:G5', 'No Tlp', merge_format)
            worksheet.merge_range('H4:H5', 'Alamat Identitas', merge_format)
            worksheet.merge_range('I4:I5', 'Alamat Domisili', merge_format)
            worksheet.merge_range('J4:J5', 'No Tlp Domisili', merge_format)
            worksheet.merge_range('K4:K5', 'Gerai', merge_format)
            worksheet.merge_range('L4:L5', 'Tgl Perpanjang', merge_format)
            worksheet.merge_range('M4:M5', 'JW (hari)', merge_format)
            worksheet.merge_range('N4:N5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('O4:O5', 'Jenis Transaksi', merge_format)
            worksheet.merge_range('P4:P5', 'Barang', merge_format)
            worksheet.merge_range('Q4:Q5', 'Nilai', merge_format)
            worksheet.merge_range('R4:T4', 'Pendapatan (Rp)', merge_format)
            worksheet.write('R5', 'Jasa (Rp)',  bold1)
            worksheet.write('S5', 'Adm (Rp)', bold1)
            worksheet.write('T5', 'Bea Simpan (Rp)', bold1)      

            row = 5
            col = 0
            for t in kp:
                worksheet.write_string(row, col , t.agkredit.norek() )
                worksheet.write_string(row, col + 1 , t.agkredit.agnasabah.nama)
                
                
                worksheet.write_string(row, col + 2 , t.agkredit.agnasabah.no_ktp)
                worksheet.write_string(row, col + 3 , t.agkredit.agnasabah.tempat)
                worksheet.write_datetime(row, col + 4 , t.agkredit.agnasabah.tgl_lahir,date_format)
                worksheet.write_string(row, col + 5 ,t.agkredit.agnasabah.jenis_kelamin )
                worksheet.write_string(row, col + 6 ,t.agkredit.agnasabah.telepon_ktp + ' ' + '/' +  ' ' +t.agkredit.agnasabah.hp_ktp )
                worksheet.write_string(row, col + 7 , t.agkredit.agnasabah.alamat_ktp  + ' ' + 'No' + ' ' + t.agkredit.agnasabah.no_rumah_ktp + ' ' + 'Rt' + ' ' + t.agkredit.agnasabah.rt_ktp + ' ' + 'Rw' + ' ' + t.agkredit.agnasabah.rw_ktp + ' ' + ' Kelurahan' +' ' + t.agkredit.agnasabah.kelurahan_ktp + ' ' + ' kecamatan' + ' ' + t.agkredit.agnasabah.kecamatan_ktp )
                worksheet.write_string(row, col + 8 ,t.agkredit.agnasabah.alamat_domisili + ' ' + 'No ' + ' ' + t.agkredit.agnasabah.no_rumah_domisili + ' ' + 'Rt' +' ' + t.agkredit.agnasabah.rt_domisili + ' ' + 'Rw' + ' ' + t.agkredit.agnasabah.rw_domisili + ' ' + 'Kelurahan' + ' ' +t.agkredit.agnasabah.kelurahan_domisili + ' ' + 'Kecamatan' + ' ' + t.agkredit.agnasabah.kecamatan_domisili + ' ' + 'Kota Madya' + ' ' + t.agkredit.agnasabah.kotamadya_domisili + ' ' + 'Kabupaten' + ' ' + t.agkredit.agnasabah.kabupaten_domisili )
                worksheet.write_string(row, col + 9 , t.agkredit.agnasabah.hp_domisili + ' ' + '-' + ' ' +t.agkredit.agnasabah.telepon_domisili)
            
                worksheet.write_string(row, col + 10 , t.gerai.nama)
                worksheet.write_datetime(row, col + 11 , t.tanggal,date_format)
                worksheet.write_number(row, col + 12, t.agkredit.jw_all(), money_format)
                worksheet.write_datetime(row, col + 13, t.agkredit.jatuhtempo, date_format)
                worksheet.write_number(row, col + 14, t.agkredit.jenis_transaksi,money_format)
                worksheet.write_string(row, col + 15, t.agkredit.__unic_barang__())
                worksheet.write_number(row, col + 16, t.agkredit.nilai, money_format)
                worksheet.write_number(row, col + 17, t.agkredit.jasa, money_format)
                worksheet.write_number(row, col + 18, t.agkredit.adm, money_format)
                worksheet.write_number(row, col + 19, t.agkredit.biayasimpan, money_format)
                row += 1

            worksheet.write(row,4, 'Total', bold)    
            worksheet.write(row,16, a, money_format)
            worksheet.write(row, 17, c, money_format)
            worksheet.write(row, 18, d, money_format)
            worksheet.write(row, 19, e, money_format)
        

            workbook.close()
            output.seek(0)
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Laporan_Perpanjangan.xlsx"
            return response

    else:
        variables = RequestContext(request, {'form': form})
        return render_to_response('manop/perpanjang/rekap_perpanjang_hari.html', variables)

@login_required
@user_passes_test(is_in_multiple_groups)
def pelunasan_gerai(request):
    start_date = None
    end_date = None
    form = SearchForm()
    kp = []
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET :
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        
        if id_cabang == '500' :
            akad= Pelunasan.objects.filter(pelunasan__lunas__isnull = False).filter(pelunasan__lunas__range=(start_date,end_date)).order_by('gerai').filter(pelunasan__status_transaksi = 1)
            template='manop/pelunasan/rekap_pelunasan_hari.html'
            variable = RequestContext(request,{'tes':akad,
            'form':form,'id_cabang':id_cabang,'start_date':start_date,'end_date':end_date,
            'start_date':start_date,'end_date':end_date,'nilai': sum([b.nilai for b in akad ]),})
            return render_to_response(template,variable)
        else:
            akad= Pelunasan.objects.filter(pelunasan__lunas__isnull = False).filter(pelunasan__lunas__range=(start_date,end_date)).filter(gerai__kode_cabang = id_cabang).filter(pelunasan__status_transaksi = 1)
            template= 'manop/pelunasan/rekap_pelunasan_hari.html'
            variable = RequestContext(request,{'tes':akad,'form':form,'id_cabang':id_cabang,'start_date':start_date,
            'end_date':end_date,'nilai': sum([b.nilai for b in akad ]),})
            return render_to_response(template,variable)
    
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            akad= Pelunasan.objects.filter(pelunasan__lunas__isnull = False).filter(pelunasan__lunas__range=(start_date,end_date)).order_by('gerai').filter(pelunasan__status_transaksi = 1)
            template1= 'manop/pelunasan/cetak_pelunasan_hari.html'
            variable = RequestContext(request,{'tes':akad,'form':form,'start_date':start_date,'end_date':end_date,
            'id_cabang':id_cabang,'nilai': sum([b.nilai for b in akad ]),})
            return render_to_response(template1,variable)
        else:
            akad= Pelunasan.objects.filter(pelunasan__lunas__isnull = False).filter(pelunasan__lunas__range=(start_date,end_date)).filter(gerai__kode_cabang = id_cabang).filter(pelunasan__status_transaksi = 1)
            template1= 'manop/pelunasan/cetak_pelunasan_hari.html'
            variable = RequestContext(request,{'tes':akad,'form':form,'id_cabang':id_cabang,'start_date':start_date,'end_date':end_date,
            'nilai': sum([b.nilai for b in akad ]),})
            return render_to_response(template1,variable)

    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']         
        if id_cabang == '500' :
            akad= Pelunasan.objects.filter(pelunasan__lunas__isnull = False).filter(pelunasan__lunas__range=(start_date,end_date)).order_by('gerai').filter(pelunasan__status_transaksi = 1)
            a = sum([b.pelunasan.nilai for b in akad ])
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
        
            worksheet.merge_range('A1:H1', 'LAPORAN PELUNASAN GABUNGAN', merge_format1)
            worksheet.merge_range('A2:H2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama', merge_format)
            worksheet.merge_range('D4:D5', 'Barang', merge_format)
            worksheet.merge_range('E4:E5', 'Tanggal', merge_format)
            worksheet.merge_range('F4:F5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('G4:G5', 'Tgl Pelunasan', merge_format)
            worksheet.merge_range('H4:H5', 'Pinjaman (Rp)', merge_format)
            row = 5
            col = 0
            for t in akad:
                worksheet.write_string(row, col , t.pelunasan.norek() )
                worksheet.write_string(row, col + 1 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.pelunasan.agnasabah.nama)                
                worksheet.write_string(row, col + 3 , t.pelunasan.barang.type + '' + t.pelunasan.barang.merk )
                worksheet.write_datetime(row, col + 4 ,t.tanggal,date_format)
                worksheet.write_datetime(row, col + 5 ,t.pelunasan.jatuhtempo,date_format )
                worksheet.write_datetime(row, col + 6 ,t.tanggal,date_format)
                worksheet.write_number(row, col + 7 , t.pelunasan.nilai,money_format)                 
                row += 1

            worksheet.write(row,4, 'Total', bold)    
            worksheet.write(row,7, a, money_format)

            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Laporan_Pelunasan_gabungan.xlsx"
            return response
        else:
            akad= Pelunasan.objects.filter(pelunasan__lunas__isnull = False).filter(pelunasan__lunas__range=(start_date,end_date)).filter(gerai__kode_cabang = id_cabang).filter(pelunasan__status_transaksi = 1)
            
            a = sum([b.pelunasan.nilai for b in akad ])

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
        
            worksheet.merge_range('A1:H1', 'LAPORAN PELUNASAN GERAI', merge_format1)
            worksheet.merge_range('A2:H2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama', merge_format)
            worksheet.merge_range('D4:D5', 'Barang', merge_format)
            worksheet.merge_range('E4:E5', 'Tanggal', merge_format)
            worksheet.merge_range('F4:F5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('G4:G5', 'Tgl Pelunasan', merge_format)
            worksheet.merge_range('H4:H5', 'Pinjaman (Rp)', merge_format)
            row = 5
            col = 0
            for t in akad:
                worksheet.write_string(row, col , t.pelunasan.norek() )
                worksheet.write_string(row, col + 1 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.pelunasan.agnasabah.nama)                
                worksheet.write_string(row, col + 3 , t.pelunasan.barang.type + '' + t.pelunasan.barang.merk )
                worksheet.write_datetime(row, col + 4 ,t.tanggal,date_format)
                worksheet.write_datetime(row, col + 5 ,t.pelunasan.jatuhtempo,date_format )
                worksheet.write_datetime(row, col + 6 ,t.tanggal,date_format)
                worksheet.write_number(row, col + 7 , t.pelunasan.nilai,money_format)                 
                row += 1
            worksheet.write(row,4, 'Total', bold)
            worksheet.write(row,7, a, money_format)        
            workbook.close()
            output.seek(0)
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Laporan_Pelunasan.xlsx"
            return response

    else:
        variables = RequestContext(request, {'form': form})
        return render_to_response('manop/pelunasan/rekap_pelunasan_hari.html', variables)


def rincian_barang_di_gerai(request):
    akad= AkadGadai.objects.filter(status_permintaan__in=('1','3')).filter(sts_tdr = None)
    start_date = None
    end_date = None
    form = SearchForm()
    #form = AkadGadaiForm()
    all = []
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET :
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            for (l) in akad:
                tb = AkadGadai.objects.filter(sts_tdr__isnull = True).filter(tanggal_pengiriman__range =(start_date,end_date)).order_by('gerai')
                start_date = start_date
                end_date = end_date
                id_cabang = id_cabang
            template='manop/baranggerai/rekap_barang_di_gerai.html'
            variable = RequestContext(request,{'tes':tb,'form':form,
            'form':form,'id_cabang':id_cabang,'start_date':start_date,'end_date':end_date,'nilai': sum([b.nilai for b in tb ])})
            return render_to_response(template,variable)
        else:
            for (l) in akad:
                tb = AkadGadai.objects.filter(sts_tdr__isnull = True).filter(tanggal_pengiriman__range =(start_date,end_date)).\
                    filter(gerai__kode_cabang = id_cabang)
                start_date = start_date
                end_date = end_date
                id_cabang = id_cabang
            template='manop/baranggerai/rekap_barang_di_gerai.html'
            variable = RequestContext(request,{'tes':tb,'form':form,
            'form':form,'id_cabang':id_cabang,'start_date':start_date,'end_date':end_date,'nilai': sum([b.nilai for b in tb ])})            
            return render_to_response(template,variable)
    
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            for (l) in akad:
                tb = AkadGadai.objects.filter(sts_tdr__isnull = True).filter(tanggal_pengiriman__range =(start_date,end_date)).order_by('gerai')
            template1= 'manop/baranggerai/cetak_barang_di_gerai.html'
            variable = RequestContext(request,{'tes':tb,'form':form,
            'form':form,'id_cabang':id_cabang,'start_date':start_date,'end_date':end_date,'nilai': sum([b.nilai for b in tb ])})
            return render_to_response(template1,variable)
        else:
            for (l) in akad:
                tb = AkadGadai.objects.filter(sts_tdr__isnull = True).filter(tanggal_pengiriman__range =(start_date,end_date)).order_by('gerai').\
                    filter(gerai__kode_cabang = id_cabang)
            template1= 'manop/baranggerai/cetak_barang_di_gerai.html'
            variable = RequestContext(request,{'tes':tb,'form':form,
            'form':form,'id_cabang':id_cabang,
            'start_date':start_date,
            'end_date':end_date,
            'nilai': sum([b.nilai for b in tb ]),
            'jasa': sum([b.jasa for b in tb ]),
            'adm': sum([b.nilai_adm for b in tb ]),
            'simpan': sum([b.biayasimpan for b in tb ]),
            'bersih' : sum([b.jumlah_biaya for b in tb ]),})
            return render_to_response(template1,variable)

    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']         
        if id_cabang == '500':
            for (l) in akad:
                tb = AkadGadai.objects.filter(sts_tdr__isnull = True).filter(tanggal_pengiriman__range =(start_date,end_date)).order_by('gerai')
            a = sum([b.nilai for b in tb ])
            c = sum([b.jasa for b in tb ]) 
            d = sum([b.nilai_adm for b in tb ]) 
            e = 0 
            f = start_date
            g = end_date
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': 0})
            bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            money_format = workbook.add_format({'num_format': '#,##0'})
            date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
            merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            merge_format1 = workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter',})
        
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
            worksheet.set_column(10, 10, 10)
        
            worksheet.merge_range('A1:I1', 'DATA BARANG PEMESANAN YANG MASIH DIGERAI UNIT PJB', merge_format1)
            worksheet.merge_range('A2:I2', 'PERIODE '+ f + " s.d " + g, merge_format1)
  
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama', merge_format)
            worksheet.merge_range('D4:D5', 'Barang', merge_format)
            worksheet.merge_range('E4:E5', 'Tgl Akad', merge_format)
            worksheet.merge_range('F4:F5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('G4:G5', 'Tgl Permintaan', merge_format)
            worksheet.merge_range('H4:H5', 'Tgl Pengiriman', merge_format)
            worksheet.merge_range('I4:I5', 'Nilai', merge_format)
            

            row = 5
            col = 0
            for t in tb:
    
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.agnasabah.nama)
                worksheet.write_string(row, col + 3 , t.barang.get_jenis_barang_display() + '-' + t.barang.merk + '-' + t.barang.type + '-' + t.barang.sn)
                worksheet.write_datetime(row, col + 4 , t.tanggal,date_format)
                worksheet.write_datetime(row, col + 5, t.jatuhtempo, date_format)
                worksheet.write_datetime(row, col + 6, t.tanggal_permintaan, date_format)
                worksheet.write_datetime(row, col + 7, t.tanggal_pengiriman, date_format)
                worksheet.write_number(row, col + 8, t.nilai, money_format)
                
                row += 1
            
            worksheet.write(row,4, 'Total', bold)
            worksheet.write(row,8, a, money_format)
       
        
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=BARANG_YANG_MASIH_DIGERAI_GABUNGAN.xlsx"
            return response
        else:
            for (l) in akad:
                tb = AkadGadai.objects.filter(sts_tdr__isnull = True).filter(tanggal_pengiriman__range =(start_date,end_date)).order_by('gerai').filter(gerai__id = id_cabang)
            a = sum([b.nilai for b in tb ])
            f = start_date
            g = end_date
            #h = nacab.nama_cabang
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': 0})
            bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            money_format = workbook.add_format({'num_format': '#,##0'})
            date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
            merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            merge_format1 = workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter',})
            worksheet.set_column(0, 0, 10)
            worksheet.set_column(1, 1, 18)
            worksheet.set_column(2, 2, 11)
            worksheet.set_column(3, 3, 12)
            worksheet.set_column(4, 4, 10)
            worksheet.set_column(5, 5, 10)
            worksheet.set_column(6, 6, 10)
            worksheet.set_column(7, 7, 10)
            worksheet.set_column(8, 8, 10)
            worksheet.set_column(9, 9, 10)
            worksheet.set_column(10, 10, 10)

            worksheet.merge_range('A1:I1', 'DATA BARANG PEMESANAN YANG MASIH DIGERAI UNIT PJB', merge_format1)
            worksheet.merge_range('A2:I2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama', merge_format)
            worksheet.merge_range('D4:D5', 'Barang', merge_format)
            worksheet.merge_range('E4:E5', 'Tgl Akad', merge_format)
            worksheet.merge_range('F4:F5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('G4:G5', 'Tgl Permintaan', merge_format)
            worksheet.merge_range('H4:H5', 'Tgl Pengiriman', merge_format)
            worksheet.merge_range('I4:I5', 'Nilai', merge_format)


            row = 5
            col = 0
            for t in tb:
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.agnasabah.nama)
                worksheet.write_string(row, col + 3 , t.barang.get_jenis_barang_display() + '-' + t.barang.merk + '-' + t.barang.type + '-' + t.barang.sn)
                worksheet.write_datetime(row, col + 4 , t.tanggal,date_format)
                worksheet.write_datetime(row, col + 5, t.jatuhtempo, date_format)
                worksheet.write_datetime(row, col + 6, t.tanggal_permintaan, date_format)
                worksheet.write_datetime(row, col + 7, t.tanggal_pengiriman, date_format)
                worksheet.write_number(row, col + 8, t.nilai, money_format)
                row += 1
            worksheet.write(row,4, 'Total', bold)
            worksheet.write(row,8, a, money_format)
            

            workbook.close()
            output.seek(0)
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=BARANG_YANG_MASIH_DIGERAI.xlsx"
            return response

    else:
        variables = RequestContext(request, {'form': form})
        return render_to_response('manop/baranggerai/rekap_barang_di_gerai.html', variables)

### PEJUALAN AYDA
def penjualan_ayda(request,object_id):
    ag = AkadGadai.objects.get(id=object_id)
    lapur = ag.lapur_set.all()
    sekarang = datetime.date.today()
    #form = PelunasanForm(initial={'pelunasan': ag.id,'gerai': ag.gerai.id, 'tanggal': sekarang.date,'nilai': ag.nilai})
    form = BarangLelangForm(initial={'aglelang': ag.id,'tgl_lelang': sekarang})
    form.fields['aglelang'].widget = forms.HiddenInput()
    template = 'manop/penjualan_ayda.html'
    variable = RequestContext(request, {'ag': ag,'form': form,'lapur':lapur})
    return render_to_response(template,variable)
### AKHIR PENJUALAN AYDA





def lelang_manop(request, object_id):
    ag = AkadGadai.objects.get(id=object_id)
    D = decimal.Decimal
    sekarang = datetime.date.today()
    if request.method == 'POST':
        form = BarangLelangForm(request.POST)
        if form.is_valid() :            
            aglelang = form.cleaned_data['aglelang']
            tgl_lelang = form.cleaned_data['tgl_lelang']
            harga_jual = form.cleaned_data['harga_jual']
            nama_pembeli = form.cleaned_data['nama_pembeli']
            no_identitas = form.cleaned_data['no_identitas']
            alamat_pembeli = form.cleaned_data['alamat_pembeli']
            no_telp = form.cleaned_data['no_telp']
            jenis = form.cleaned_data['jenis']
            form = BarangLelang(aglelang = aglelang,tgl_lelang = tgl_lelang, harga_jual = harga_jual,nama_pembeli = nama_pembeli,\
            no_identitas = no_identitas,alamat_pembeli = alamat_pembeli,no_telp = no_telp,jenis=jenis)
            form.save()

            #Jika Penjualan Lebih BESAR dari Nilai Pinjaman GERAI JAKARTA
            if form.jenis == '1':
                if form.harga_jual > ag.total_akad_ayda() :
                    jurnal_penjualan_ayda_untung(form, request.user)
                    messages.add_message(request, messages.INFO, 'Jurnal Transaksi penjualan Anggota Laba KAS Berhasil 2937')
                if form.harga_jual < ag.total_akad_ayda() :
                    jurnal_penjualan_ayda_rugi(form, request.user)
                    messages.add_message(request, messages.INFO, 'Jurnal Transaksi penjualan Anggota Rugi KAS Berhasil 2940')
                if form.harga_jual == ag.total_akad_ayda() :
                    jurnal_penjualan_ayda_sama(form, request.user)
                    messages.add_message(request, messages.INFO, 'Jurnal Transaksi penjualan Anggota Sama KAS Berhasil 2943')
            if form.jenis == '2':
                if form.harga_jual > ag.total_akad_ayda() :
                    jurnal_penjualan_ayda_untung_bank(form, request.user)
                    messages.add_message(request, messages.INFO, 'Jurnal Transaksi penjualan Anggota Laba BANK Berhasil 2947')
                if form.harga_jual < ag.total_akad_ayda() :
                    jurnal_penjualan_ayda_rugi_bank(form, request.user)
                    messages.add_message(request, messages.INFO, 'Jurnal Transaksi penjualan Anggota Rugi BANK Berhasil 2950')
                if form.harga_jual == ag.total_akad_ayda() :
                    jurnal_penjualan_ayda_sama_bank(form, request.user)
                    messages.add_message(request, messages.INFO, 'Jurnal Transaksi penjualan Anggota Sama BANK Berhasil 2953')

	    forms= PelunasanManopForm(request.POST)
	    forms = Pelunasan(pelunasan = ag,tanggal = sekarang,nilai = ag.nilai,terlambat_kendaraan = 0 ,denda_kendaraan = 0 ,\
	    gerai = ag.gerai,terlambat = 0 ,denda = 0 , bea_jasa = 0,jenis_barang = ag.jenis_transaksi , bea_jasa_kendaraan = 0 )
	    forms.save()    
	    ag.lunas = datetime.date.today()
	    ag.status_transaksi = 7
	    ag.sts_tdr = '1'
	    ag.tanggal_lelang = datetime.date.today()
	    ag.save()
	    lunas = LunasTerjual(aglunas = ag,status ='1',tanggal=ag.tanggal_lelang)
	    lunas.save()
            lpr = ag.lapur_set.all()
            lpr.update(status = '2',tanggal=ag.tanggal_lelang)
            messages.add_message(request, messages.INFO, 'Akadgadai Telah Lelang')                
        return HttpResponseRedirect(ag.get_absolute_url_manop())
    else:
        variables = RequestContext(request, {'object': ag, 'form': form})
        return render_to_response('akadgadai/lelang_manop.html', variables)  

def jurnal_penjualan_ayda_sama_bank(form, user):
    D = decimal.Decimal
    bm = AydaMapper.objects.get(item='4')
    ayda_pusat = bm.debet_penjualan_rugi
    ayda_gerai = bm.kredit_penjualan

    jurnal = Jurnal.objects.create(diskripsi= 'Penjualan Ayda Bank A/n %s  Norek %s' % (form.aglelang.agnasabah.nama,form.aglelang.norek()),
        kode_cabang = user.profile.gerai.kode_cabang,object_id=form.aglelang.id,
        tgl_trans = form.tgl_lelang,cu = user, mu = user,
        nobukti=form.aglelang.norek())
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("AYDA_PUSAT_BANK"), id_coa = ayda_pusat,
        kredit = 0,debet =D(form.harga_jual),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300,deskripsi= 'Penjualan Ayda Bank %s' % (form.aglelang.norek()))
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("AYDA_PUSAT_BANK"), id_coa = ayda_gerai,
        debet = 0,kredit = D(form.aglelang.total_akad_ayda()),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300,deskripsi= 'Penjualan Ayda Bank %s' % (form.aglelang.norek()))

def jurnal_penjualan_ayda_untung_bank(form, user):
    D = decimal.Decimal
    bm = AydaMapper.objects.get(item='4')
    ayda_pusat = bm.debet_penjualan_rugi
    ayda_gerai = bm.kredit_penjualan
    ayda_gerai1 = bm.kredit_penjualan_ayda

    jurnal = Jurnal.objects.create(diskripsi= 'Penjualan Ayda Bank A/n %s  Norek %s' % (form.aglelang.agnasabah.nama,form.aglelang.norek()),
        kode_cabang = user.profile.gerai.kode_cabang,object_id=form.aglelang.id,
        tgl_trans = form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("AYDA_PUSAT_BANK"), id_coa = ayda_pusat,
        kredit = 0,debet =D(form.harga_jual),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300,
        deskripsi= 'Penjualan Ayda Bank %s' %(form.aglelang.norek()))
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("AYDA_PUSAT_BANK"), id_coa = ayda_gerai,
        debet = 0,kredit = D(form.aglelang.total_akad_ayda()),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300,
        deskripsi= 'Penjualan Ayda Bank %s' %(form.aglelang.norek()))
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("AYDA_PUSAT_BANK"), id_coa = ayda_gerai1,
        debet = 0,kredit = D(form.harga_jual) - D(form.aglelang.total_akad_ayda()),id_product = '4',status_jurnal ='2',
        tgl_trans =form.tgl_lelang,id_cabang =user.profile.gerai.kode_cabang,id_unit= 300,
        deskripsi= 'Penjualan Ayda Bank %s' %(form.aglelang.norek()))

def jurnal_penjualan_ayda_rugi_bank(form, user):
    D = decimal.Decimal
    bm = AydaMapper.objects.get(item='4')
    ayda_pusat = bm.debet_penjualan_untung
    ayda_gerai = bm.debet_penjualan_rugi
    ayda_gerai1 = bm.kredit_penjualan

    jurnal = Jurnal.objects.create(diskripsi= 'Penjualan Ayda Bank A/n %s  Norek %s' % (form.aglelang.agnasabah.nama,form.aglelang.norek()),
        kode_cabang = user.profile.gerai.kode_cabang,object_id=form.aglelang.id,
        tgl_trans = form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("AYDA_PUSAT_BANK"), id_coa = ayda_pusat,
        kredit = 0,debet =(D(form.harga_jual) - D(form.aglelang.total_akad_ayda())) * -1,
        id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,id_cabang =user.profile.gerai.kode_cabang,id_unit= 300,
        deskripsi= 'Penjualan Ayda Bank %s' %(form.aglelang.norek()))
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("AYDA_PUSAT_BANK"), id_coa = ayda_gerai,
        kredit = 0,debet=  D(form.harga_jual),
        id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,id_cabang =user.profile.gerai.kode_cabang,id_unit= 300,
        deskripsi= 'Penjualan Ayda Bank %s' %(form.aglelang.norek()))
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("AYDA_PUSAT_BANK"), id_coa = ayda_gerai1,
        debet = 0,kredit = D(form.aglelang.total_akad_ayda()),
        id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,id_cabang =user.profile.gerai.kode_cabang,id_unit= 300,
        deskripsi= 'Penjualan Ayda Bank %s' %(form.aglelang.norek()))


def jurnal_penjualan_ayda_sama(form, user):
    D = decimal.Decimal
    bm = AydaMapper.objects.get(item='5')
    ayda_pusat = bm.debet_penjualan_rugi
    ayda_gerai = bm.kredit_penjualan

    jurnal = Jurnal.objects.create(diskripsi= 'Penjualan Ayda Kas A/n %s  Norek %s' % (form.aglelang.agnasabah.nama,form.aglelang.norek()),
        kode_cabang = user.profile.gerai.kode_cabang,object_id=form.aglelang.id,
        tgl_trans = form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("AYDA_PUSAT"), id_coa = ayda_pusat,
        kredit = 0,debet =D(form.harga_jual),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300,deskripsi= 'Penjualan Ayda Kas %s' % (form.aglelang.norek()))
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("AYDA_PUSAT"), id_coa = ayda_gerai,
        debet = 0,kredit = D(form.aglelang.total_akad_ayda()),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300,deskripsi= 'Penjualan Ayda Kas %s' % (form.aglelang.norek()))

def jurnal_penjualan_ayda_untung(form, user):
    D = decimal.Decimal
    bm = AydaMapper.objects.get(item='5')
    ayda_pusat = bm.debet_penjualan_rugi
    ayda_gerai = bm.kredit_penjualan
    ayda_gerai1 = bm.kredit_penjualan_ayda
       
    jurnal = Jurnal.objects.create(diskripsi= 'Penjualan Ayda Kas A/n %s  Norek %s' % (form.aglelang.agnasabah.nama,form.aglelang.norek()),
        kode_cabang = user.profile.gerai.kode_cabang,object_id=form.aglelang.id,
        tgl_trans = form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("AYDA_PUSAT"), id_coa = ayda_pusat,
        kredit = 0,debet =D(form.harga_jual),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300,
        deskripsi= 'Penjualan Ayda Kas %s' %(form.aglelang.norek()))
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("AYDA_PUSAT"), id_coa = ayda_gerai,
        debet = 0,kredit = D(form.aglelang.total_akad_ayda()),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300,
        deskripsi= 'Penjualan Ayda Kas %s' %(form.aglelang.norek()))
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("AYDA_PUSAT"), id_coa = ayda_gerai1,
        debet = 0,kredit = D(form.harga_jual) - D(form.aglelang.total_akad_ayda()),id_product = '4',status_jurnal ='2',
        tgl_trans =form.tgl_lelang,id_cabang =user.profile.gerai.kode_cabang,id_unit= 300,
        deskripsi= 'Penjualan Ayda Kas %s' %(form.aglelang.norek()))

def jurnal_penjualan_ayda_rugi(form, user):
    D = decimal.Decimal
    bm = AydaMapper.objects.get(item='5')
    ayda_pusat = bm.debet_penjualan_untung
    ayda_gerai = bm.debet_penjualan_rugi
    ayda_gerai1 = bm.kredit_penjualan
       
    jurnal = Jurnal.objects.create(diskripsi= 'Penjualan Ayda Kas A/n %s  Norek %s' % (form.aglelang.agnasabah.nama,form.aglelang.norek()),
        kode_cabang = user.profile.gerai.kode_cabang,object_id=form.aglelang.id,
        tgl_trans = form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("AYDA_PUSAT"), id_coa = ayda_pusat,
        kredit = 0,debet =(D(form.harga_jual) - D(form.aglelang.total_akad_ayda())) * -1,
        id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,id_cabang =user.profile.gerai.kode_cabang,id_unit= 300,
        deskripsi= 'Penjualan Ayda Kas %s' %(form.aglelang.norek()))
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("AYDA_PUSAT"), id_coa = ayda_gerai,
        kredit = 0,debet=  D(form.harga_jual),
        id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,id_cabang =user.profile.gerai.kode_cabang,id_unit= 300,
        deskripsi= 'Penjualan Ayda Kas %s' %(form.aglelang.norek()))
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("AYDA_PUSAT"), id_coa = ayda_gerai1,
        debet = 0,kredit = D(form.aglelang.total_akad_ayda()),
        id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,id_cabang =user.profile.gerai.kode_cabang,id_unit= 300,
        deskripsi= 'Penjualan Ayda Kas %s' %(form.aglelang.norek()))
##Jika Penjualan Lebih Besar dari Nilai Pinjaman

def jurnal_lelang_adm_lebih_anggota(form, user):
    D = decimal.Decimal
    lebih = GeraiPenjualanMapper.objects.get(item = '6')
    a_titipan_pelunasan = lebih.coa1
    a_pinjaman_non_anggota = lebih.coa2
    a_pdp_jasa = lebih.coa3

    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang adm: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
        kode_cabang = form.aglelang.gerai.kode_cabang,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_adm"), id_coa = a_titipan_pelunasan,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_adm"), id_coa = a_pinjaman_non_anggota,
        kredit = D(str(form.aglelang.nilai)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_adm"), id_coa = a_pdp_jasa,
        kredit = D(str(form.harga_jual)) - D(str(form.aglelang.nilai)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)


def jurnal_lelang_adm_lebih(form, user):
    D = decimal.Decimal
    lebih = GeraiPenjualanMapper.objects.get(item = '1')#,ke_cabang=form.aglelang.gerai)
    a_titipan_pelunasan = lebih.coa1
    a_pinjaman_non_anggota = lebih.coa2
    a_pdp_jasa = lebih.coa3
   
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang adm: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
        kode_cabang = form.aglelang.gerai.kode_cabang,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_adm"), id_coa = a_titipan_pelunasan,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_adm"), id_coa = a_pinjaman_non_anggota,
        kredit = D(str(form.aglelang.nilai)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_adm"), id_coa = a_pdp_jasa,
        kredit = D(str(form.harga_jual)) - D(str(form.aglelang.nilai)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

##Jika Penjualan SAMA DENGAN Nilai Pinjaman
def jurnal_lelang_adm_pas_anggota(form, user):
    D = decimal.Decimal
    kurang = GeraiPenjualanMapper.objects.get(item = '7')
    a_titipan_pelunasan = kurang.coa1
    a_pinjaman_non_anggota = kurang.coa2
    #a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
    #a_pinjaman_non_anggota = get_object_or_404(Tbl_Akun, id=166L)

    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang adm: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
        kode_cabang = form.aglelang.gerai.kode_cabang,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_adm"), id_coa = a_titipan_pelunasan,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_adm"), id_coa = a_pinjaman_non_anggota,
        kredit = D(str(form.aglelang.nilai)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)


def jurnal_lelang_adm_pas(form, user):
    D = decimal.Decimal
    kurang = GeraiPenjualanMapper.objects.get(item = '2')
    a_titipan_pelunasan = kurang.coa1
    a_pinjaman_non_anggota = kurang.coa2
    #a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
    #a_pinjaman_non_anggota = get_object_or_404(Tbl_Akun, id=166L)
    
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang adm: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
        kode_cabang = form.aglelang.gerai.kode_cabang,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_adm"), id_coa = a_titipan_pelunasan,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_adm"), id_coa = a_pinjaman_non_anggota,
        kredit = D(str(form.aglelang.nilai)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

##Jika Penjualan LEBIH KECIL dari Nilai Pinjaman
def jurnal_lelang_adm_kurang_anggota(form, user):
    D = decimal.Decimal
    kurang = GeraiPenjualanMapper.objects.get(item = '8')
    a_titipan_pelunasan = kurang.coa1
    a_pinjaman_non_anggota = kurang.coa2
    a_ppap = kurang.coa3

    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang adm: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
        kode_cabang = form.aglelang.gerai.kode_cabang,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_adm"), id_coa = a_ppap,
        kredit = 0 ,debet = D(str(form.aglelang.nilai)) - D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_adm"), id_coa = a_titipan_pelunasan,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_adm"), id_coa = a_pinjaman_non_anggota,
        kredit = D(str(form.aglelang.nilai)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)


def jurnal_lelang_adm_kurang(form, user):
    D = decimal.Decimal
    kurang = GeraiPenjualanMapper.objects.get(item = '3')
    a_titipan_pelunasan = kurang.coa1
    a_pinjaman_non_anggota = kurang.coa2
    a_ppap = kurang.coa3
   
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang adm: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
        kode_cabang = form.aglelang.gerai.kode_cabang,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_adm"), id_coa = a_ppap,
        kredit = 0 ,debet = D(str(form.aglelang.nilai)) - D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_adm"), id_coa = a_titipan_pelunasan,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_adm"), id_coa = a_pinjaman_non_anggota,
        kredit = D(str(form.aglelang.nilai)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

    

##PENJUALAN GERAI JAKARTA
def jurnal_lelang_kasir_jakarta(form, user):
    D = decimal.Decimal
    pjl = GeraiPenjualanMapper.objects.get(item ='4',cabang=form.aglelang.gerai)
    a_kas = pjl.coa1
    a_titipan_pelunasan = pjl.coa2
    #a_kas = get_object_or_404(Tbl_Akun, id=7L)
    #a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
        
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang pusat: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
        kode_cabang = 300,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_kas,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =300,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_titipan_pelunasan,
        kredit = D(str(form.harga_jual)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =300,id_unit= 300)

def jurnal_lelang_kasir_jakarta_bank(form, user):
    D = decimal.Decimal
    pjl = GeraiPenjualanMapper.objects.get(item ='5',cabang=form.aglelang.gerai)
    a_bank = pjl.coa1
    a_titipan_pelunasan = pjl.coa2
    #a_kas = get_object_or_404(Tbl_Akun, id=7L)
    #a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)

    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang Pusat: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
        kode_cabang = 300,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir_bank"), id_coa = a_bank,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =300,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir_bank"), id_coa = a_titipan_pelunasan,
        kredit = D(str(form.harga_jual)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =300,id_unit= 300)

##PENJUALAN GERAI SUCI
def jurnal_lelang_kasir_suci(form, user):
    D = decimal.Decimal
    a_kas = get_object_or_404(Tbl_Akun, id=609L)
    a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
        
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang Pusat: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
        kode_cabang = 300,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_kas,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =300,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_titipan_pelunasan,
        kredit = D(str(form.harga_jual)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =300,id_unit= 300)

##PENJUALAN GERAI DU
def jurnal_lelang_kasir_du(form, user):
    D = decimal.Decimal
    a_kas = get_object_or_404(Tbl_Akun, id=610L)
    a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
        
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang Pusat: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
        kode_cabang = 300,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_kas,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =300,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_titipan_pelunasan,
        kredit = D(str(form.harga_jual)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =300,id_unit= 300)

##PENJUALAN GERAI BALUBUR
def jurnal_lelang_kasir_balubur(form, user):
    D = decimal.Decimal
    a_kas = get_object_or_404(Tbl_Akun, id=611L)
    a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
        
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang Pusat: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
        kode_cabang = 300,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_kas,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =300,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_titipan_pelunasan,
        kredit = D(str(form.harga_jual)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =300,id_unit= 300)

##PENJUALAN GERAI HILIR
def jurnal_lelang_kasir_hilir(form, user):
    D = decimal.Decimal
    a_kas = get_object_or_404(Tbl_Akun, id=613L)
    a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
        
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang Pusat: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
	kode_cabang = 300,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_kas,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =300,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_titipan_pelunasan,
        kredit = D(str(form.harga_jual)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =300,id_unit= 300)

##PENJUALAN GERAI KOPO
def jurnal_lelang_kasir_kopo(form, user):
    D = decimal.Decimal
    a_kas = get_object_or_404(Tbl_Akun, id=614L)
    a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
        
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang Pusat: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
	kode_cabang = 300,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_kas,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =300,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_titipan_pelunasan,
        kredit = D(str(form.harga_jual)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =300,id_unit= 300)

##PENJUALAN GERAI CIBIRU
def jurnal_lelang_kasir_cibiru(form, user):
    D = decimal.Decimal
    a_kas = get_object_or_404(Tbl_Akun, id=615L)
    a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
        
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang Pusat: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
	kode_cabang = 300,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_kas,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =300,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_titipan_pelunasan,
        kredit = D(str(form.harga_jual)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =300,id_unit= 300)

##PENJUALAN GERAI CIPACING
def jurnal_lelang_kasir_cipacing(form, user):
    D = decimal.Decimal
    a_kas = get_object_or_404(Tbl_Akun, id=616L)
    a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
        
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang kasir: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
	kode_cabang = form.aglelang.gerai.kode_cabang,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_kas,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_titipan_pelunasan,
        kredit = D(str(form.harga_jual)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

##PENJUALAN GERAI JATINANGOR
def jurnal_lelang_kasir_jatinangor(form, user):
    D = decimal.Decimal
    a_kas = get_object_or_404(Tbl_Akun, id=617L)
    a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
        
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang kasir: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
	kode_cabang = form.aglelang.gerai.kode_cabang,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_kas,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_titipan_pelunasan,
        kredit = D(str(form.harga_jual)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

##PENJUALAN GERAI CIMAHI
def jurnal_lelang_kasir_cimahi(form, user):
    D = decimal.Decimal
    a_kas = get_object_or_404(Tbl_Akun, id=618L)
    a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
        
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang kasir: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
	kode_cabang = form.aglelang.gerai.kode_cabang,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_kas,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_titipan_pelunasan,
        kredit = D(str(form.harga_jual)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

##PENJUALAN GERAI BUAH BATU
def jurnal_lelang_kasir_bubat(form, user):
    D = decimal.Decimal
    a_kas = get_object_or_404(Tbl_Akun, id=619L)
    a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
        
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang kasir: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
	kode_cabang = form.aglelang.gerai.kode_cabang,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_kas,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_titipan_pelunasan,
        kredit = D(str(form.harga_jual)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

##PENJUALAN GERAI MARANATA
def jurnal_lelang_kasir_maranata(form, user):
    D = decimal.Decimal
    a_kas = get_object_or_404(Tbl_Akun, id=622L)
    a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
        
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang kasir: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
	kode_cabang = form.aglelang.gerai.kode_cabang,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_kas,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_titipan_pelunasan,
        kredit = D(str(form.harga_jual)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

##PENJUALAN GERAI CIREBON
def jurnal_lelang_kasir_cirebon(form, user):
    D = decimal.Decimal
    a_kas = get_object_or_404(Tbl_Akun, id=624L)
    a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
        
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang kasir: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
	kode_cabang = form.aglelang.gerai.kode_cabang,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_kas,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_titipan_pelunasan,
        kredit = D(str(form.harga_jual)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

##PENJUALAN GERAI CIUMBELEUIT
def jurnal_lelang_kasir_ciumbeleuit(form, user):
    D = decimal.Decimal
    a_kas = get_object_or_404(Tbl_Akun, id=626L)
    a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
        
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang kasir: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
	kode_cabang = form.aglelang.gerai.kode_cabang,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_kas,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_titipan_pelunasan,
        kredit = D(str(form.harga_jual)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

##PENJUALAN GERAI UBER
def jurnal_lelang_kasir_uber(form, user):
    D = decimal.Decimal
    a_kas = get_object_or_404(Tbl_Akun, id=627L)
    a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
        
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang kasir: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
	kode_cabang = form.aglelang.gerai.kode_cabang,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_kas,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_titipan_pelunasan,
        kredit = D(str(form.harga_jual)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)

##PENJUALAN GERAI CIWASTRA
def jurnal_lelang_kasir_uber(form, user):
    D = decimal.Decimal
    a_kas = get_object_or_404(Tbl_Akun, id=628L)
    a_titipan_pelunasan = get_object_or_404(Tbl_Akun, id=287L)
        
    jurnal = Jurnal.objects.create(
        diskripsi= 'Penjualan lelang kasir: NoRek: %s an: %s  ' % (form.aglelang.norek(), form.aglelang.agnasabah.nama),
	kode_cabang = form.aglelang.gerai.kode_cabang,
        tgl_trans =form.tgl_lelang,cu = user, mu = user,nobukti=form.aglelang.norek())
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_kas,
        kredit = 0,debet = D(str(form.harga_jual)),id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)
    
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("Penjualan_lelang_kasir"), id_coa = a_titipan_pelunasan,
        kredit = D(str(form.harga_jual)),debet = 0,id_product = '4',status_jurnal ='2',tgl_trans =form.tgl_lelang,
        id_cabang =form.aglelang.gerai.kode_cabang,id_unit= 300)


def show(request,object_id):
    ag = AkadGadai.objects.get(id=object_id)
    sekarang = datetime.date.today()
    #form = PelunasanForm(initial={'pelunasan': ag.id,'gerai': ag.gerai.id, 'tanggal': sekarang.date,'nilai': ag.nilai})
    form = BarangLelangForm(initial={'aglelang': ag.id,'tgl_lelang': sekarang})
    form.fields['aglelang'].widget = forms.HiddenInput()
    template = 'manop/lunas_lelang_show.html'
    variable = RequestContext(request, {'ag': ag,'form': form})
    return render_to_response(template,variable)

def list_nsb(request):
    manop = AkadGadai.objects.filter(status_taksir=2)    
    template = 'manop/manop_nsb.html'
    variables = RequestContext(request, {'manop': manop})    
    return render_to_response(template, variables)

def cari(request):
    rekening=request.GET['rekening']    
    try:
        ag=AkadGadai.objects.get(id=int(rekening))
        return HttpResponseRedirect("/manop/%s/show/" % ag.id)
    except:
        messages.add_message(request, messages.INFO,'No rekening tidak ditemukan.')
        return HttpResponseRedirect("/akadgadai/")

def reset_status_lainlain(request):
    for i in request.POST.getlist('id_pilih'):
        #sekarang = datetime.date.today()
        akad = AkadGadai.objects.get(id=(i))
        #sts = StatusGadai.objects.all()
        akad.status_transaksi = None 
        akad.tanggal_lelang = None
        messages.add_message(request, messages.INFO,' RESET STATUS OK.')
        akad.save()
        #sts.create(agstatus=akad, status_akad=1, tanggal_status = sekarang)
    return HttpResponseRedirect('/manop/rincian_lainlain/')

def reset_status_hilang(request):
    for i in request.POST.getlist('id_pilih'):
        akad = AkadGadai.objects.get(id=(i))
        akad.status_transaksi = None
        akad.tanggal_lelang = None
        messages.add_message(request, messages.INFO,' RESET STATUS OK.')
        akad.save()
    return HttpResponseRedirect('/manop/rincian_hilang/')

@login_required
def reset_status(request):
    for i in request.POST.getlist('id_pilih'):
        akad = AkadGadai.objects.get(id=(i))
        akad.status_transaksi = None 
        akad.tanggal_lelang = None
        messages.add_message(request, messages.INFO,' RESET STATUS OK.')
        akad.save()        
    return HttpResponseRedirect('/manop/rincian_lelang/')

@login_required
def rincian_jatuhtempo(request):
    start_date = None
    end_date = None
    form = SearchForm()
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET :
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500':
            tb = AkadGadai.objects.filter(jatuhtempo__range=(start_date,end_date)).exclude(status_transaksi__in = ('1','2','4','5','6','7','8','9','10')).order_by('gerai')
            template='manop/laporan/rekap_jatuhtempo.html'
            variable = RequestContext(request,{'tes':tb,
            'form':form,'id_cabang':id_cabang,'start_date':start_date,'end_date':end_date,
            'start_date':start_date,'end_date':end_date,'nilai': sum([b.nilai for b in tb ])})
            return render_to_response(template,variable)
        else:
            tb = AkadGadai.objects.filter(jatuhtempo__range=(start_date,end_date)).exclude(status_transaksi__in = ('1','2','4','5','6','7','8','9','10')).\
                filter(gerai__kode_cabang = id_cabang).order_by('gerai')
            template='manop/laporan/rekap_jatuhtempo.html'
            variable = RequestContext(request,{'tes':tb,'form':form,'id_cabang':id_cabang,'start_date':start_date,
            'end_date':end_date,'nilai': sum([b.nilai for b in tb ]) })
            return render_to_response(template,variable)
    
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            tb = AkadGadai.objects.filter(jatuhtempo__range=(start_date,end_date)).exclude(status_transaksi__in = ('1','2','4','5','6','7','8','9','10')).order_by('gerai')
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template1= 'manop/laporan/cetak_rekap_jatuhtempo.html'
            variable = RequestContext(request,{'tes':tb,'form':form,'start_date':start_date,'end_date':end_date,
            'id_cabang':id_cabang,'nilai': sum([b.nilai for b in tb ])})
            return render_to_response(template1,variable)
        else:
            tb = AkadGadai.objects.filter(jatuhtempo__range=(start_date,end_date)).exclude(status_transaksi__in = ('1','2','4','5','6','7','8','9','10')).filter(gerai__kode_cabang = id_cabang).order_by('gerai')
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template1= 'manop/laporan/cetak_rekap_jatuhtempo.html'
            variable = RequestContext(request,{'tes':tb,'form':form,'id_cabang':id_cabang,'start_date':start_date,'end_date':end_date,
            'id_cabang':id_cabang,'nilai': sum([b.nilai for b in tb ])})
            return render_to_response(template1,variable)

    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']         
        if id_cabang == '500':
            tb = AkadGadai.objects.filter(jatuhtempo__range=(start_date,end_date)).exclude(status_transaksi__in = ('1','2','4','5','6','7','8','9','10')).order_by('gerai')
            a = sum([b.nilai for b in tb ])
            f = start_date
            g = end_date
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': 0})
            bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            money_format = workbook.add_format({'num_format': '#,##0'})
            date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
            merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            merge_format1 = workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter',})
        
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
            worksheet.set_column(10, 10, 10)
        
            worksheet.merge_range('A1:J1', 'LAPORAN JATUH TEMPO GABUNGAN', merge_format1)
            worksheet.merge_range('A2:J2', 'PERIODE '+ f + " sd " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Nama', merge_format)
            worksheet.merge_range('C4:C5', 'Gerai', merge_format)
            worksheet.merge_range('D4:D5', 'Tgl Akad', merge_format)
            worksheet.merge_range('E4:E5', 'JW (hari)', merge_format)
            worksheet.merge_range('F4:F5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('G4:G5', 'Jenis Transaksi', merge_format)
            worksheet.merge_range('H4:H5', 'Nilai', merge_format)
            worksheet.merge_range('I4:I5', 'Barang', merge_format)
            worksheet.merge_range('J4:J5', 'Jenis Barang', merge_format)
            worksheet.merge_range('K4:K5', 'Status', merge_format)
            row = 5
            col = 0
            for t in tb:
                worksheet.write_string(row, col , t.norek())
                worksheet.write_string(row, col + 1 , t.agnasabah.nama )
                worksheet.write_string(row, col + 2 , t.gerai.nama_cabang)
                worksheet.write_datetime(row, col + 3 , t.tanggal, date_format )
                worksheet.write(row, col + 4, t.jw_all())
                worksheet.write_datetime(row, col + 5, t.jatuhtempo, date_format)
                worksheet.write_string(row, col + 6, t.get_jenis_transaksi_display())
                worksheet.write_number(row, col + 7, t.nilai, money_format)
                worksheet.write_string(row, col + 8, t.barang.type + '' + t.barang.merk )
                worksheet.write_string(row, col + 9, t.get_jenis_transaksi_display())
                if t.status_transaksi == None:                                  
                    worksheet.write_string(row, col + 10, 'Aktif')
                else:
                    worksheet.write_string(row, col + 10, t.get_status_transaksi_display())
                row += 1
            
            worksheet.write(row,4, 'Total', bold)
            worksheet.write(row,7, a, money_format)
        
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Laporan_Jatuhtempo_Gabungan.xlsx"
            return response
        else:
            tb = AkadGadai.objects.filter(jatuhtempo__range=(start_date,end_date)).filter(gerai__kode_cabang = id_cabang).\
                exclude(status_transaksi__in = ('1','2','4','5','6','7','8','9','10')).order_by('gerai')
            a = sum([b.nilai for b in tb ])
            f = start_date
            g = end_date
            #h = nacab.nama_cabang
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': 0})
            bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            money_format = workbook.add_format({'num_format': '#,##0'})
            date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
            merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            merge_format1 = workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter',})
            worksheet.set_column(0, 0, 10)
            worksheet.set_column(1, 1, 18)
            worksheet.set_column(2, 2, 11)
            worksheet.set_column(3, 3, 12)
            worksheet.set_column(4, 4, 10)
            worksheet.set_column(5, 5, 10)
            worksheet.set_column(6, 6, 10)
            worksheet.set_column(7, 7, 10)
            worksheet.set_column(8, 8, 10)
            worksheet.set_column(9, 9, 10)
            worksheet.set_column(10, 10, 10)

            worksheet.merge_range('A1:J1', 'LAPORAN JATUH TEMPO PERGERAI ', merge_format1)
            worksheet.merge_range('A2:J2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Nama', merge_format)
            worksheet.merge_range('C4:C5', 'Gerai', merge_format)
            worksheet.merge_range('D4:D5', 'Tgl Akad', merge_format)
            worksheet.merge_range('E4:E5', 'JW (hari)', merge_format)
            worksheet.merge_range('F4:F5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('G4:G5', 'Jenis Transaksi', merge_format)
            worksheet.merge_range('H4:H5', 'Nilai', merge_format)
            worksheet.merge_range('I4:I5', 'Barang', merge_format)
            worksheet.merge_range('J4:J5', 'Jenis Barang', merge_format)
            worksheet.merge_range('K4:K5', 'Status', merge_format)
            row = 5
            col = 0
            for t in tb:
                worksheet.write_string(row, col , t.norek())
                worksheet.write_string(row, col + 1 , t.agnasabah.nama )
                worksheet.write_string(row, col + 2 , t.gerai.nama_cabang)
                worksheet.write_datetime(row, col + 3 , t.tanggal, date_format )
                worksheet.write(row, col + 4, t.jw_all())
                worksheet.write_datetime(row, col + 5, t.jatuhtempo, date_format)
                worksheet.write_string(row, col + 6, t.get_jenis_transaksi_display())
                worksheet.write_number(row, col + 7, t.nilai, money_format)
                worksheet.write_string(row, col + 8, t.barang.type + '' + t.barang.merk )
                worksheet.write_string(row, col + 9, t.get_jenis_transaksi_display())
                if t.status_transaksi == None:
                    worksheet.write_string(row, col + 10, 'Aktif')
                else:
                    worksheet.write_string(row, col + 10, t.get_status_transaksi_display())
                row += 1
            worksheet.write(row,4, 'Total', bold)
            worksheet.write(row,7, a, money_format)

            workbook.close()
            output.seek(0)
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Laporan_Jatuhtempo.xlsx"
            return response

    else:
        variables = RequestContext(request, {'form': form})
        return render_to_response('manop/laporan/rekap_jatuhtempo.html', variables)


@login_required
def rincian_hilang(request):    
    kp = []
    start_date = None
    end_date = None
    id_cabang = None
    form = SearchForm()
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET:
        end_date = request.GET['end_date']
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            akad= AkadGadai.objects.filter(status_transaksi =('9')).filter(lelang__range=(start_date,end_date))
            for k in akad:
                kp.append(k)
            total_nilai = total_jasa = total_adm = total_beasimpan = total_all =0
            for b in kp:
                total_nilai += b.nilai
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'manop/hilang/rincian_hilang.html'
            variables = RequestContext(request, {'kp':kp,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,'nilai':total_nilai,\
                'form':form})
            return render_to_response(template, variables)
        else:
            akad= AkadGadai.objects.filter(status_transaksi= ('9')).filter(lelang__range=(start_date,end_date)).filter(gerai__kode_cabang= id_cabang)
            for k in akad:
                kp.append(k)
            total_nilai = total_jasa = total_adm = total_beasimpan = total_all =0
            for b in kp:
                total_nilai += b.nilai
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'manop/hilang/rincian_hilang.html'
            variables = RequestContext(request, {'kp':kp,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,\
                'form':form,'nilai':total_nilai})
            return render_to_response(template, variables)
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        end_date = request.GET['end_date']
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        akad= AkadGadai.objects.filter(status_transaksi =('9')).filter(lelang__range=(start_date,end_date))
        for k in akad:
            kp.append(k)
        total_nilai = total_jasa = total_adm = total_beasimpan = total_all =0
        for b in kp:
            total_nilai += b.nilai
        template = 'manop/hilang/rincian_hilang_pdf.html'
        variables = RequestContext(request, {'kp':kp,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,'nilai':total_nilai,\
            'form':form})
        return render_to_response(template, variables)
    
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        end_date = request.GET['end_date']
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        akad= AkadGadai.objects.filter(status_transaksi =('9')).filter(lelang__range=(start_date,end_date))
        for k in akad:
            kp.append(k)
        a = sum([b.nilai for b in akad ])
        c = sum([b.jasa for b in akad ]) 
        d = sum([b.adm for b in akad ]) 
        e = sum([b.biayasimpan for b in akad ]) 
        f = start_date
        g = end_date
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 0})
        bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
        money_format = workbook.add_format({'num_format': '#,##0'})
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
        merge_format1 = workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter',})
    
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
        worksheet.set_column(10, 10, 10)
    
        worksheet.merge_range('A1:K1', 'DATA BARANG HILANG ', merge_format1)
        worksheet.merge_range('A2:K2', 'PERIODE ', merge_format1)
        worksheet.merge_range('A4:A5', 'Norek ', merge_format)
        worksheet.merge_range('B4:B5', 'Nama', merge_format)
        worksheet.merge_range('C4:C5', 'Gerai', merge_format)
        worksheet.merge_range('D4:D5', 'Tgl Lelang', merge_format)
        
        worksheet.merge_range('E4:E5', 'Tgl Akad', merge_format)
        worksheet.merge_range('F4:F5', 'JW (hari)', merge_format)
        worksheet.merge_range('G4:G5', 'Jatuh Tempo', merge_format)
        worksheet.merge_range('H4:H5', 'Status', merge_format)
        worksheet.merge_range('I4:I5', 'Nilai', merge_format)
        worksheet.merge_range('J4:L5', 'Pendapatan (Rp)', merge_format)
        worksheet.write('J5', 'Jasa (Rp)',  bold1)
        worksheet.write('K5', 'Adm (Rp)', bold1)
        worksheet.write('L5', 'Bea Simpan (Rp)', bold1)
        worksheet.merge_range('M4:M5', 'BARANG', merge_format)

        row = 5
        col = 0
        for t in akad:
            worksheet.write_string(row, col , t.norek() )
            worksheet.write_string(row, col + 1 , t.agnasabah.nama)
            worksheet.write_string(row, col + 2 , t.gerai.nama_cabang)
            worksheet.write_datetime(row, col + 3 , t.tanggal_lelang,date_format)
            worksheet.write_datetime(row, col + 4 , t.tanggal,date_format)
            worksheet.write_number(row, col + 5, t.jw_all(), money_format)
            worksheet.write_datetime(row, col + 6, t.jatuhtempo,date_format)
            worksheet.write_string(row, col + 7, t.status_transaksi)
            worksheet.write_number(row, col + 8, t.nilai, money_format)
            worksheet.write_number(row, col + 9, t.jasa, money_format)
            worksheet.write_number(row, col + 10, t.adm, money_format)
            worksheet.write_number(row, col + 11, t.biayasimpan, money_format)
            worksheet.write_string(row, col + 12, t.barang.merk +' ' + t.barang.type)
            row += 1

        worksheet.write(row,4, 'Total', bold)    
        worksheet.write(row,8, a, money_format)
        worksheet.write(row, 9, c, money_format)
        worksheet.write(row, 10, d, money_format)
        worksheet.write(row, 11, e, money_format)
    
        workbook.close()    
        output.seek(0)    
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=LELANG.xlsx"
        return response
    else:
        template = 'manop/hilang/rincian_hilang.html'
        variables = RequestContext(request, {'kp': kp,'form':form })
        return render_to_response(template, variables)

@login_required
def rincian_lainlain(request):    
    kp = []
    start_date = None
    end_date = None
    id_cabang = None
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET:
        end_date = request.GET['end_date']
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            akad= AkadGadai.objects.filter(status_transaksi =('LAIN-LAIN')).filter(tanggal_lelang__range=(start_date,end_date))
            for k in akad:
                kp.append(k)
            total_nilai = total_jasa = total_adm = total_beasimpan = total_all =0
            for b in kp:
                total_nilai += b.nilai
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'manop/lainlain/rincian_lainlain.html'
            variables = RequestContext(request, {'kp':kp,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,'nilai':total_nilai})
            return render_to_response(template, variables)
        else:
            akad= AkadGadai.objects.filter(status_transaksi= ('LAIN-LAIN')).filter(tanggal_lelang__range=(start_date,end_date)).filter(gerai__kode_cabang = id_cabang)
            for k in akad:
                kp.append(k)
            total_nilai = total_jasa = total_adm = total_beasimpan = total_all =0
            for b in kp:
                total_nilai += b.nilai
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'manop/lainlain/rincian_lainlain.html'
            variables = RequestContext(request, {'kp':kp,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,'nilai':total_nilai})
            return render_to_response(template, variables)
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        end_date = request.GET['end_date']
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        akad= AkadGadai.objects.filter(status_transaksi =('LAIN-LAIN')).filter(tanggal_lelang__range=(start_date,end_date))
        for k in akad:
            kp.append(k)
        total_nilai = total_jasa = total_adm = total_beasimpan = total_all =0
        for b in kp:
            total_nilai += b.nilai
        template = 'manop/lainlain/rincian_lainlain_pdf.html'
        variables = RequestContext(request, {'kp':kp,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,'nilai':total_nilai})
        return render_to_response(template, variables)
    
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        end_date = request.GET['end_date']
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        akad= AkadGadai.objects.filter(status_transaksi =('LAIN-LAIN')).filter(tanggal_lelang__range=(start_date,end_date))
        for k in akad:
            kp.append(k)
        a = sum([b.nilai for b in akad ])
        c = sum([b.jasa for b in akad ]) 
        d = sum([b.adm for b in akad ]) 
        e = sum([b.biayasimpan for b in akad ]) 
        f = start_date
        g = end_date
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 0})
        bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
        money_format = workbook.add_format({'num_format': '#,##0'})
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
        merge_format1 = workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter',})
    
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
        worksheet.set_column(10, 10, 10)
    
        worksheet.merge_range('A1:K1', 'DATA BARANG HILANG ', merge_format1)
        worksheet.merge_range('A2:K2', 'PERIODE ', merge_format1)
        worksheet.merge_range('A4:A5', 'Norek ', merge_format)
        worksheet.merge_range('B4:B5', 'Nama', merge_format)
        worksheet.merge_range('C4:C5', 'Gerai', merge_format)
        worksheet.merge_range('D4:D5', 'Tgl Lelang', merge_format)
        
        worksheet.merge_range('E4:E5', 'Tgl Akad', merge_format)
        worksheet.merge_range('F4:F5', 'JW (hari)', merge_format)
        worksheet.merge_range('G4:G5', 'Jatuh Tempo', merge_format)
        worksheet.merge_range('H4:H5', 'Status', merge_format)
        worksheet.merge_range('I4:I5', 'Nilai', merge_format)
        worksheet.merge_range('J4:L5', 'Pendapatan (Rp)', merge_format)
        worksheet.write('J5', 'Jasa (Rp)',  bold1)
        worksheet.write('K5', 'Adm (Rp)', bold1)
        worksheet.write('L5', 'Bea Simpan (Rp)', bold1)
        worksheet.merge_range('M4:M5', 'BARANG', merge_format)

        row = 5
        col = 0
        for t in akad:
            worksheet.write_string(row, col , t.norek() )
            worksheet.write_string(row, col + 1 , t.agnasabah.nama)
            worksheet.write_string(row, col + 2 , t.gerai.nama)
            worksheet.write_datetime(row, col + 3 , t.tanggal_lelang,date_format)
            worksheet.write_datetime(row, col + 4 , t.tanggal,date_format)
            worksheet.write_number(row, col + 5, t.jw_all(), money_format)
            worksheet.write_datetime(row, col + 6, t.jatuhtempo,date_format)
            worksheet.write_string(row, col + 7, t.status_transaksi)
            worksheet.write_number(row, col + 8, t.nilai, money_format)
            worksheet.write_number(row, col + 9, t.jasa, money_format)
            worksheet.write_number(row, col + 10, t.adm, money_format)
            worksheet.write_number(row, col + 11, t.biayasimpan, money_format)
            worksheet.write_string(row, col + 12, t.barang.merk +' ' + t.barang.type)
            row += 1

        worksheet.write(row,4, 'Total', bold)    
        worksheet.write(row,8, a, money_format)
        worksheet.write(row, 9, c, money_format)
        worksheet.write(row, 10, d, money_format)
        worksheet.write(row, 11, e, money_format)
    
        workbook.close()    
        output.seek(0)    
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=LAIN-LAIN.xlsx"
        return response
    else:
        template = 'manop/lainlain/rincian_lainlain.html'
        variables = RequestContext(request, {'kp': kp })
        return render_to_response(template, variables)

def rincian_piutang(request):
    gerai = Tbl_Cabang.objects.all()
    akad= AkadGadai.objects.all()
    kp = []
    start_date = datetime.date(2002,01,01)
    end_date = None
    id_cabang = None
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET:
        end_date = request.GET['end_date']
        start_date = start_date
        for k in gerai:
            if k.akadgadai_set.filter(lunas__isnull= True).filter(tanggal__range=(start_date,end_date)).count() > 0:
                kp.append({'kode':k.kode,'nama':k.nama,'piutang':k.piutang,'aktif':k.aktif,'get_banyak_lunas':k.get_banyak_lunas,'all_aktif':k.all_aktif,
                    'piutang_a':k.piutang_a,'total_piutang_jasa':k.total_piutang_jasa,'total_piutang_beasimpan':k.total_piutang_beasimpan,'total_piutang_denda':k.total_piutang_denda})
                #start_date = start_date
                #print start_date
            start_date = start_date
            end_date = end_date
            print start_date
            all_lunas = Pelunasan.objects.filter(tanggal__range=(start_date,end_date))
            all_pk_lunas = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(lunas__isnull=True)
            all_pk_prpj = Perpanjang.objects.filter(tanggal__range=(start_date,end_date))
            all_pencairan = AkadGadai.objects.filter(tanggal__range=(start_date,end_date))
    
        template = 'manop/piutang/piutang.html'
        variables = RequestContext(request, {'kp':kp,'akad' : len(all_pk_lunas),'lunas' : len(all_lunas),'total_noa':(len(all_pk_lunas) + len(all_lunas)),\
            'total_cair':sum([p.nilai for p in all_pencairan]),})
        #'kp': kp ,'nkp' : len(kp),'aktif' : total_aktif,'npk' : total_akad,'piutang' : total_piutang,'piutang_a' : total_piutang_a,'lunas' : total_pelunasan,
        #'jasa': total_piutang_jasa,'denda': total_piutang_denda,'beasimpan': total_piutang_beasimpan,'akadlunas':total_banyak_lunas,'totalakad':total_all_aktif})
        return render_to_response(template, variables)
    
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        end_date = request.GET['end_date']
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
    
        template1 = 'manop/piutang/rekappiutang.html'
        variables = RequestContext(request, {
        'kp': kp ,'nkp' : len(kp),'aktif' : total_aktif,'npk' : total_akad,'piutang' : total_piutang,'piutang_a' : total_piutang_a,'lunas' : total_pelunasan,
        'jasa': total_piutang_jasa,'denda': total_piutang_denda,'beasimpan': total_piutang_beasimpan,'akadlunas':total_banyak_lunas,'totalakad':total_all_aktif})
        return render_to_response(template1, variables)
    
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        end_date = request.GET['end_date']        
        for (l) in akad:
            start_date = datetime.date(2002,02,2)
            tb = AkadGadai.objects.filter(lunas__isnull =True).filter(tanggal__range=(start_date,end_date)).order_by('gerai')
        a = sum([b.nilai for b in tb ])
        c = sum([b.jasa for b in tb ]) 
        d = sum([b.adm for b in tb ]) 
        e = sum([b.biayasimpan for b in tb ]) 
        f = start_date
        #g = end_date
      
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 0})
        bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#C0C0C0'})
        money_format = workbook.add_format({'num_format': '#,##0'})
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        date_format1 = workbook.add_format({'num_format': 'yyyy-mm-dd'})
        merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#C0C0C0'})
        merge_format1 = workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter',})
        
    
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
        worksheet.set_column(10, 10, 10)
    
        worksheet.merge_range('A1:K1', 'RINCIAN PIUTANG DIV PJB ', merge_format1)
        worksheet.write('A2', 'PERIODE ')
        worksheet.write_datetime('B2', start_date ,date_format)
        worksheet.write('C2', 's.d')  
        worksheet.write('D2', end_date, date_format)
        worksheet.merge_range('A4:A5', 'Norek ', merge_format)
        worksheet.merge_range('B4:B5', 'Nama', merge_format)
        worksheet.merge_range('C4:C5', 'Gerai', merge_format)
        worksheet.merge_range('D4:D5', 'Tgl Akad', merge_format)
        worksheet.merge_range('E4:E5', 'JW (hari)', merge_format)
        worksheet.merge_range('F4:F5', 'Jatuh Tempo', merge_format)
        worksheet.merge_range('G4:G5', 'Jenis Transaksi', merge_format)
        worksheet.merge_range('H4:H5', 'Nilai', merge_format)
        worksheet.merge_range('I4:K4', 'Pendapatan (Rp)', merge_format)
        worksheet.write('I5', 'Jasa (Rp)',  bold1)
        worksheet.write('J5', 'Adm (Rp)', bold1)
        worksheet.write('K5', 'Bea Simpan (Rp)', bold1)

        row = 5
        col = 0
        for t in tb:
            worksheet.write_string(row, col , t.norek() )
            worksheet.write_string(row, col + 1 , t.agnasabah.nama)
            worksheet.write_string(row, col + 2 , t.gerai.nama)
            worksheet.write_datetime(row, col + 3 , t.tanggal,date_format)
            worksheet.write_number(row, col + 4, t.jw_all(), money_format)
            worksheet.write_datetime(row, col + 5 , t.jatuhtempo, date_format)
            worksheet.write_number(row, col + 6, t.jenis_transaksi, money_format)
            worksheet.write_number(row, col + 7, t.nilai, money_format)
            worksheet.write_number(row, col + 8, t.jasa, money_format)
            worksheet.write_number(row, col + 9, t.adm, money_format)
            worksheet.write_number(row, col + 10, t.biayasimpan, money_format)
            row += 1

        worksheet.write(row,4, 'Total', bold)    
        worksheet.write(row,7, a, money_format)
        worksheet.write(row, 8, c, money_format)
        worksheet.write(row, 9, d, money_format)
        worksheet.write(row, 10, e, money_format)
    
        workbook.close()    
        output.seek(0)    
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=Laporan_Piutang.xlsx"
        return response
    
    else:
        template = 'manop/piutang/piutang.html'
        variables = RequestContext(request, {'kp': kp })
        return render_to_response(template, variables)

def rincian_lelang(request):    
    kp = []
    form = SearchForm()
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET:
        end_date = request.GET['end_date']
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        start_date = start_date
        end_date = end_date
        id_cabang = id_cabang
        if id_cabang == '500' :
            akad= AkadGadai.objects.filter(status_transaksi__in=('6','7')).filter(lunas__range=(start_date,end_date))
            for k in akad:
                kp.append(k)
            total_nilai = 0
            for b in kp:
                total_nilai += b.nilai 
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'manop/lelang/rincian_lelang.html'
            variables = RequestContext(request, {'kp':kp,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,\
                'nilai':total_nilai,'form':form})     
            return render_to_response(template, variables)
        else:
            akad= AkadGadai.objects.filter(status_transaksi__in=('6','7')).filter(lunas__range=(start_date,end_date)).\
                filter(gerai__kode_cabang= id_cabang)
            for k in akad:
                kp.append(k)
            total_nilai = 0
            for b in kp:
                total_nilai += b.nilai
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'manop/lelang/rincian_lelang.html'
            variables = RequestContext(request, {'kp':kp,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,\
                'nilai':total_nilai,'form':form})
            return render_to_response(template, variables)
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        end_date = request.GET['end_date']
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            akad= AkadGadai.objects.filter(status_transaksi__in=('6','7')).filter(lunas__range=(start_date,end_date))
            for k in akad:
                kp.append(k)
            total_nilai = 0
            for b in kp:
                total_nilai += b.nilai    
            template = 'manop/lelang/rincian_lelang_pdf.html'
            variables = RequestContext(request, {'kp':kp,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,\
                'form':form,'nilai':total_nilai})
            return render_to_response(template, variables)
        else:
            akad= AkadGadai.objects.filter(status_transaksi__in=('6','7')).filter(lunas__range=(start_date,end_date)).\
                filter(gerai__kode_cabang= id_cabang)
            for k in akad:
                kp.append(k)
            total_nilai = 0
            for b in kp:
                total_nilai += b.nilai    
            template = 'manop/lelang/rincian_lelang_pdf.html'
            variables = RequestContext(request, {'kp':kp,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,\
                'form':form,'nilai':total_nilai})
            return render_to_response(template, variables)
    
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        end_date = request.GET['end_date']
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500':
            akad= AkadGadai.objects.filter(status_transaksi__in=('6','7')).filter(lunas__range=(start_date,end_date))
            for k in akad:
                kp.append(k)
            a = sum([b.nilai for b in akad ])
            f = start_date
            g = end_date
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': 0})
            bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            money_format = workbook.add_format({'num_format': '#,##0'})
            date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
            merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            merge_format1 = workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter',})
        
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
            worksheet.set_column(10, 10, 10)
        
            worksheet.merge_range('A1:I1', 'DATA LELANG ', merge_format1)
            worksheet.merge_range('A2:I2', 'PERIODE ', merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Nama', merge_format)
            worksheet.merge_range('C4:C5', 'Gerai', merge_format)
            worksheet.merge_range('D4:D5', 'Tgl Ayda', merge_format)            
            worksheet.merge_range('E4:E5', 'Tgl Akad', merge_format)
            worksheet.merge_range('F4:F5', 'JW ', merge_format)
            worksheet.merge_range('G4:G5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('H4:H5', 'Status', merge_format)
            worksheet.merge_range('I4:I5', 'Nilai', merge_format)
            worksheet.merge_range('J4:J5', 'Barang', merge_format)

            row = 5
            col = 0
            for t in akad:
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.agnasabah.nama)
                worksheet.write_string(row, col + 2 , t.gerai.nama_cabang)
                worksheet.write_datetime(row, col + 3 , t.lunas,date_format)
                worksheet.write_datetime(row, col + 4 , t.tanggal,date_format)
                worksheet.write_string(row, col + 10, t.jw_all())
                worksheet.write_datetime(row, col + 6, t.jatuhtempo,date_format)
                worksheet.write_string(row, col + 7, t.status_transaksi)
                worksheet.write_number(row, col + 8, t.nilai, money_format)
                worksheet.write_string(row, col + 9, t.barang.merk +' ' + t.barang.type)
                row += 1

            worksheet.write(row,4, 'Total', bold)    
            worksheet.write(row,8, a, money_format)
        
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=LELANG.xlsx"
            return response
        else:
            akad= AkadGadai.objects.filter(status_transaksi__in=('6','7')).filter(lunas__range=(start_date,end_date)).filter(gerai__kode_cabang= id_cabang)
            for k in akad:
                kp.append(k)
            a = sum([b.nilai for b in akad ])
            f = start_date
            g = end_date
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': 0})
            bold1 = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            money_format = workbook.add_format({'num_format': '#,##0'})
            date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
            merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': '#EB9100'})
            merge_format1 = workbook.add_format({'bold': 1,'align': 'center','valign': 'vcenter',})
        
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
            worksheet.set_column(10, 10, 10)
        
            worksheet.merge_range('A1:I1', 'DATA LELANG ', merge_format1)
            worksheet.merge_range('A2:I2', 'PERIODE ', merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Nama', merge_format)
            worksheet.merge_range('C4:C5', 'Gerai', merge_format)
            worksheet.merge_range('D4:D5', 'Tgl Lelang', merge_format)
            
            worksheet.merge_range('E4:E5', 'Tgl Akad', merge_format)
            worksheet.merge_range('F4:F5', 'JW (hari)', merge_format)
            worksheet.merge_range('G4:G5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('H4:H5', 'Status', merge_format)
            worksheet.merge_range('I4:I5', 'Nilai', merge_format)
            worksheet.merge_range('J4:J5', 'Barang', merge_format)

            row = 5
            col = 0
            for t in akad:
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.agnasabah.nama)
                worksheet.write_string(row, col + 2 , t.gerai.nama)
                worksheet.write_datetime(row, col + 3 , t.tanggal_lelang,date_format)
                worksheet.write_datetime(row, col + 4 , t.tanggal,date_format)
                worksheet.write_number(row, col + 5, t.jw_all(), money_format)
                worksheet.write_datetime(row, col + 6, t.jatuhtempo,date_format)
                worksheet.write_string(row, col + 7, t.status_transaksi)
                worksheet.write_number(row, col + 8, t.nilai, money_format)
                worksheet.write_string(row, col + 9, t.barang.merk +' ' + t.barang.type)
                row += 1

            worksheet.write(row,4, 'Total', bold)    
            worksheet.write(row,8, a, money_format)
        
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=LELANG.xlsx"
            return response
    else:
        template = 'manop/lelang/rincian_lelang.html'
        variables = RequestContext(request, {'kp': kp,'form':form })
        return render_to_response(template, variables)        

def lunas(request):
    akad = AkadGadai.objects.all()
    template='manop/manop_search.html'
    variable = RequestContext(request,{'akad': akad})
    return render_to_response(template,variable)

def cariplns(request):
    rekening=request.GET['rekening']
    try:
        akad=AkadGadai.objects.get(id=int(rekening))
        return HttpResponseRedirect("/akadgadai/%s/show/" % akad.id)
    except:
        messages.add_message(request, messages.INFO,'No rekening tidak ditemukan.')
        return HttpResponseRedirect("/")

def update_status(request,object_id):
    akad= AkadGadai.objects.get(id=object_id)
    akad.status_transaksi=request.POST['status_transaksi']
    akad.tanggal_lelang=request.POST['tanggal_lelang']
    akad.save()
    if akad.status_transaksi == 'AYDA':
        lapur =  Lapur(aglapur = akad,status = '1',jasa=akad.hitung_jasa_ayda(),denda=akad.denda_all_transaksi(),
            terlambat= akad.hari_terlambat(),tanggal = akad.tanggal_lelang,nilai=akad.nilai,gerai = akad.gerai.kode_cabang)
        lapur.save()
        history = HistoryLapur(aglapur = akad,status = '1',jasa= akad.hitung_jasa_ayda(),denda= akad.denda_all_transaksi(),
            terlambat= akad.hari_terlambat(),tanggal = akad.tanggal_lelang,nilai= akad.nilai,gerai = akad.gerai.kode_cabang)
        history.save()
        jurnal_ayda(lapur, request.user)
        akad.status_transaksi = 6
        akad.sts_tdr = None
        akad.save()
        messages.add_message(request, messages.INFO,"JURNAL AYDA PUSAT (4359)")
        if akad.agnasabah.jenis_keanggotaan == '1':
            jurnal_ayda_anggota(lapur,request.user)
            messages.add_message(request, messages.INFO,"JURNAL AYDA CABANG ANGGOTA (4362)")
        else:
            jurnal_ayda_nonanggota(lapur,request.user)
            messages.add_message(request, messages.INFO,"JURNAL AYDA CABANG NONANGGOTA (4365)")
    elif akad.status_transaksi == 'HILANG':
        hilang =  Hilang(aghilang = akad,status = '1',tanggal = akad.tanggal_lelang)
        hilang.save()
        akad.status_transaksi = 9
        akad.sts_tdr = None
        akad.save()
        messages.add_message(request, messages.INFO,'STATUS PERUBAH BARANG HILANG BERHASIL.')
    elif akad.status_transaksi == 'LAIN-LAIN':
        lain = Lainlain(aglain = akad,status = '1',tanggal = akad.tanggal_lelang)
        lain.save()
        akad.status_transaksi = 10
        akad.sts_tdr = None
        akad.save() 
        messages.add_message(request, messages.INFO,'STATUS PERUBAH BARANG BERHASIL.')    
    return HttpResponseRedirect('/manop/%s/show/' % akad.id)
    

def jurnal_ayda(lapur, user):
    D = decimal.Decimal
    bm = AydaMapper.objects.get(item='1', cabang=lapur.aglapur.gerai)
    ayda_pusat = bm.debet
    ayda_gerai = bm.kredit
       
    jurnal = Jurnal.objects.create(diskripsi= 'Pengambilalihan Barang Gadai atas Nama %s Norek %s'%(lapur.aglapur.agnasabah.nama,lapur.aglapur.norek()),
        kode_cabang = user.profile.gerai.kode_cabang,object_id=lapur.aglapur.id,
        tgl_trans = lapur.tanggal,cu = user, mu = user)
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("PENJUALAN_AYDA_PUSAT"), id_coa = ayda_pusat,
        kredit = 0,debet =D(lapur.nilai),id_product = '4',status_jurnal ='2',tgl_trans =lapur.tanggal,#+ D(lapur.jasa) + D(lapur.denda)
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("PENJUALAN_AYDA_PUSAT"), id_coa = ayda_gerai,
        debet = 0,kredit = D(lapur.nilai),id_product = '4',status_jurnal ='2',tgl_trans =lapur.tanggal,#+ D(lapur.jasa) + D(lapur.denda)
        id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

def jurnal_ayda_anggota(lapur, user):
    D = decimal.Decimal
    bm = AydaMapper.objects.get(item='2')
    ayda_pusat = bm.debet
    ayda_gerai = bm.kredit
    debet_ayda_cabang = bm.debet_lawan
    kredit_ayda_pinjaman = bm.kredit_lawan
    #kredit_ayda_denda = bm.kredit_lawan1
    #kredit_ayda_jasa = bm.kredit_lawan2
    jurnal = Jurnal.objects.create(diskripsi= 'Pengambilalihan Barang Gadai atas Nama %s Norek %s'%(lapur.aglapur.agnasabah.nama,lapur.aglapur.norek()),
        kode_cabang =lapur.aglapur.gerai.kode_cabang,object_id=lapur.aglapur.id,
        tgl_trans = lapur.tanggal,cu = user, mu = user)
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("PENJUALAN_AYDA_CABANG"), id_coa = debet_ayda_cabang,
        kredit = 0,debet = D(lapur.nilai),id_product = '4',status_jurnal ='2',tgl_trans =lapur.tanggal,#+ D(lapur.jasa) + D(lapur.denda)
        id_cabang =lapur.aglapur.gerai.kode_cabang,id_unit= 300)
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("PENJUALAN_AYDA_CABANG"), id_coa = kredit_ayda_pinjaman,
        debet = 0,kredit = D(lapur.nilai),id_product = '4',status_jurnal ='2',tgl_trans =lapur.tanggal,
        id_cabang =lapur.aglapur.gerai.kode_cabang,id_unit= 300)
    #jurnal.tbl_transaksi_set.create(jenis = '%s' % ("PENJUALAN_AYDA_CABANG"), id_coa = kredit_ayda_denda,
        #debet = 0,kredit = D(lapur.denda),id_product = '4',status_jurnal ='2',tgl_trans =lapur.tanggal,
        #id_cabang =lapur.aglapur.gerai.kode_cabang,id_unit= 300)
    #jurnal.tbl_transaksi_set.create(jenis = '%s' % ("PENJUALAN_AYDA_CABANG"), id_coa = kredit_ayda_jasa,
        #debet = 0,kredit = D(lapur.jasa),id_product = '4',status_jurnal ='2',tgl_trans =lapur.tanggal,
        #id_cabang =lapur.aglapur.gerai.kode_cabang,id_unit= 300)

def jurnal_ayda_nonanggota(lapur, user):
    D = decimal.Decimal
    bm = AydaMapper.objects.get(item='3')
    ayda_pusat = bm.debet
    ayda_gerai = bm.kredit 
    debet_ayda_cabang = bm.debet_lawan
    kredit_ayda_pinjaman = bm.kredit_lawan
    #kredit_ayda_denda = bm.kredit_lawan1
    #kredit_ayda_jasa = bm.kredit_lawan2
    jurnal = Jurnal.objects.create(diskripsi= 'Pengambilalihan Barang Gadai atas Nama %s Norek %s'%(lapur.aglapur.agnasabah.nama,lapur.aglapur.norek()),
        kode_cabang =lapur.aglapur.gerai.kode_cabang,object_id=lapur.aglapur.id,
        tgl_trans = lapur.tanggal,cu = user, mu = user)
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("PENJUALAN_AYDA_CABANG"), id_coa = debet_ayda_cabang,
        kredit = 0,debet = D(lapur.nilai),id_product = '4',status_jurnal ='2',tgl_trans =lapur.tanggal,#+ D(lapur.jasa) + D(lapur.denda)
        id_cabang =lapur.aglapur.gerai.kode_cabang,id_unit= 300)
    jurnal.tbl_transaksi_set.create(jenis = '%s' % ("PENJUALAN_AYDA_CABANG"), id_coa = kredit_ayda_pinjaman,
        debet = 0,kredit = D(lapur.nilai),id_product = '4',status_jurnal ='2',tgl_trans =lapur.tanggal,
        id_cabang =lapur.aglapur.gerai.kode_cabang,id_unit= 300)
    #jurnal.tbl_transaksi_set.create(jenis = '%s' % ("PENJUALAN_AYDA_CABANG"), id_coa = kredit_ayda_denda,
        #debet = 0,kredit = D(lapur.denda),id_product = '4',status_jurnal ='2',tgl_trans =lapur.tanggal,
        #id_cabang =lapur.aglapur.gerai.kode_cabang,id_unit= 300)
    #jurnal.tbl_transaksi_set.create(jenis = '%s' % ("PENJUALAN_AYDA_CABANG"), id_coa = kredit_ayda_jasa,
        #debet = 0,kredit = D(lapur.jasa),id_product = '4',status_jurnal ='2',tgl_trans =lapur.tanggal,
        #id_cabang =lapur.aglapur.gerai.kode_cabang,id_unit= 300)

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in
    =('manop','baranglapur','admops','abh','staffops','asmanpjb','kadiv','KEUANGAN','admin')))
def total_harian_filter(request):
    awal_system = datetime.date(2000,1,1)
    rekap = Tbl_Cabang.objects.filter(status_aktif = 1)
    plns = []
    form = Filter_PencairanForm()
    start_date = None
    end_date = None
    id_cabang = None
    if 'start_date' in request.GET and request.GET['start_date'] and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        trans = []
        for k in rekap:
            if k.akadgadai_set.filter(tanggal__range=(start_date,end_date)).filter(kepalagerai__status = 1).count()>=0:
                plns.append({'k':k,'aktif':k.aktif_nasabah_harian_filter(start_date,end_date),'kode_cabang':k.kode_cabang,'nama_cabang':k.nama_cabang,
                    'nilai_cair': k.nilai_pencairan_harian_filter(start_date,end_date),
                    'noa_cair':k.aktif_harian_filter(start_date, end_date),
                    'noa_lunas':k.aktif_plns_harian_filter(start_date, end_date),
                    'nilai_pelunasan':k.plns_nilai_harian_filter( start_date,end_date),
                    't_jasa':k.total_harian_jasa_filter(start_date,end_date),
                    't_denda':k.total_harian_denda_filter(start_date,end_date),
                    't_beasimpan':k.total_harian_beasimpan_filter(start_date,end_date),
                    't_adm':k.adm_harian_filter(start_date,end_date),
                    't_jual': k.ll_harga(start_date,end_date),
                    't_akumulasi':k.akumulasi_pendapatan_harian_filter(start_date,end_date),
                    'noa_ayda':k.noa_ayda(start_date, end_date),
                    'nilai_ayda':k.nilai_ayda(start_date, end_date),
                    'noa_ayda_history':k.noa_ayda_history(start_date, end_date),
                    'nilai_ayda_history':k.nilai_ayda_history(start_date, end_date),
                    'total_noa_ayda_lunas':k.total_noa_ayda_lunas(start_date, end_date),
                    'total_nilai_ayda_lunas':k.total_nilai_ayda_lunas(start_date, end_date),
                    'nilai_jual_ayda':k.nilai_jual_ayda(start_date, end_date),
                    'nilai_jasa_terlambat_plns':k.nilai_jasa_terlambat_plns(start_date,end_date),
                    'piutang':k.rekap_piutang(end_date),
                    })
        all_pk = Pelunasan.objects.filter(tanggal__range=(start_date,end_date)).filter(pelunasan__status_transaksi = 1)
        all_pk_lunas = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(kepalagerai__status = 1)
        barang = BarangLelang.objects.filter(tgl_lelang__range=(start_date,end_date))
        lapur_1 = Lapur.objects.filter(tanggal__range=(start_date,end_date)).filter(status = 1)
        lapur_2 = HistoryLapur.objects.filter(tanggal__range=(start_date,end_date))
        jual_ayda = Lapur.objects.filter(tanggal__range=(start_date,end_date)).filter(status = 2)
        piu = AkadGadai.objects.filter(tanggal__lt=end_date).exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10'))
        total_noa = AkadGadai.objects.filter(tanggal__range=(start_date,end_date))
        template =  'manop/filter/total_harian_filter_piutang.html' #'manop/filter/total_harian_filter.html'
        variables = RequestContext(request, {'plns': plns ,'aktif_nasabah_harian' : total_noa.count(),
            'total_cair':sum([p.nilai for p in all_pk_lunas]),
            'aktif_lunas' : all_pk.count(),'total_lunas':sum([p.nilai for p in all_pk]),
            'jasa':sum([p.tot_jasa_kend_elek for p in all_pk_lunas]),
            'denda':  (sum([p.total_denda_filter for p in all_pk])) ,
            'bea_simpan': (sum([p.tot_simpan_kend_elek for p in all_pk_lunas])) ,
            'adm': sum([p.tot_adm_kend_elek for p in all_pk_lunas]) ,
            't_pendapatan': float(sum([p.tot_jasa_kend_elek for p in all_pk_lunas])) + float((sum([p.total_denda_filter for p in all_pk]))) +
                float(sum([p.tot_adm_kend_elek for p in all_pk_lunas])) + (sum([ p.tt_jual() for p in barang ])) +
                (sum([p.tot_simpan_kend_elek for p in all_pk_lunas])) + float(sum([a.bea_jasa_kendaraan for a in all_pk]) +
                sum([a.bea_jasa for a in all_pk])),
            'jasa_terlambat': 0,
            't_noa': all_pk_lunas.count()  + all_pk.count(),
            'total_jual':(sum([ p.tt_jual() for p in barang ])),
            'start_date':start_date,'end_date':end_date,
            'total_noa_real_ayda':lapur_1.count(),
            'total_nilai_real_ayda':(sum([ p.nilai for p in lapur_1 ])),
            'total_noa_ayda_history':lapur_2.count(),
            'total_nilai_ayda_history':(sum([ p.nilai for p in lapur_2 ])),
            'total_noa_plns':lapur_2.count() + all_pk.count(),
            'total_nilai_plns':(sum([ p.nilai for p in lapur_2 ])) +(sum([ p.nilai for p in all_pk ])),
            'total_nilai_penjualan':(sum([ p.nilai for p in jual_ayda ])),
            'total_jasa_terlambat':sum([a.bea_jasa_kendaraan for a in all_pk]) + sum([a.bea_jasa for a in all_pk]),
            'total_piu':sum([a.nilai for a in piu])
            })
        return render_to_response(template, variables)

    elif  'start_date' in request.GET and request.GET['start_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        trans = []
        for k in rekap:
            if k.akadgadai_set.filter(tanggal__range=(start_date,end_date)).filter(kepalagerai__status = 1).count()>=0:
                plns.append({'k':k,'aktif':k.aktif_nasabah_harian_filter(start_date,end_date),'kode_cabang':k.kode_cabang,'nama_cabang':k.nama_cabang,
                    'nilai_cair': k.nilai_pencairan_harian_filter(start_date,end_date),
                    'noa_cair':k.aktif_harian_filter(start_date, end_date),
                    'noa_lunas':k.aktif_plns_harian_filter(start_date, end_date),
                    'nilai_pelunasan':k.plns_nilai_harian_filter( start_date,end_date),
                    't_jasa':k.total_harian_jasa_filter(start_date,end_date),
                    't_denda':k.total_harian_denda_filter(start_date,end_date),
                    't_beasimpan':k.total_harian_beasimpan_filter(start_date,end_date),
                    't_adm':k.adm_harian_filter(start_date,end_date),
                    't_jual': k.ll_harga(start_date,end_date),
                    't_akumulasi':k.akumulasi_pendapatan_harian_filter(start_date,end_date),
                    'noa_ayda':k.noa_ayda(start_date, end_date),
                    'nilai_ayda':k.nilai_ayda(start_date, end_date),
                    'noa_ayda_history':k.noa_ayda_history(start_date, end_date),
                    'nilai_ayda_history':k.nilai_ayda_history(start_date, end_date),
                    'total_noa_ayda_lunas':k.total_noa_ayda_lunas(start_date, end_date),
                    'total_nilai_ayda_lunas':k.total_nilai_ayda_lunas(start_date, end_date),
                    'nilai_jual_ayda':k.nilai_jual_ayda(start_date, end_date),
                    'nilai_jasa_terlambat_plns':k.nilai_jasa_terlambat_plns(start_date,end_date),
                    'piutang':k.rekap_piutang(end_date),
                    })

        start_date = start_date
        end_date = end_date
        all_pk = Pelunasan.objects.filter(tanggal__range=(start_date,end_date)).filter(pelunasan__status_transaksi = 1)
        all_pk_lunas = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).filter(kepalagerai__status = 1)
        barang = BarangLelang.objects.filter(tgl_lelang__range=(start_date,end_date))
        lapur_1 = Lapur.objects.filter(tanggal__range=(start_date,end_date)).filter(status = 1)
        jual_ayda = Lapur.objects.filter(tanggal__range=(start_date,end_date)).filter(status = 2)
        piu = AkadGadai.objects.filter(tanggal__lt=end_date).exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10'))


        template =  'manop/filter/total_harian_filter_pdf.html' #'manop/filter/total_harian_filter.html'
        variables = RequestContext(request, {'plns': plns ,'aktif_nasabah_harian' : all_pk_lunas.count(),
            'total_cair':sum([p.nilai for p in all_pk_lunas]),
            'aktif_lunas' : all_pk.count(),'total_lunas':sum([p.nilai for p in all_pk]),
            'jasa':sum([p.tot_jasa_kend_elek for p in all_pk_lunas]), #sum([p.total_jasa_plns for p in all_pk])+ sum([p.tot_jasa_kend_elek for p in all_pk_lunas]),
            'denda':  (sum([p.total_denda_filter for p in all_pk])) ,
            'bea_simpan': (sum([p.tot_simpan_kend_elek for p in all_pk_lunas])) ,
            'adm': sum([p.tot_adm_kend_elek for p in all_pk_lunas]) ,
            't_pendapatan': float(sum([p.tot_jasa_kend_elek for p in all_pk_lunas])) +# float(sum([p.total_jasa_plns for p in all_pk])) +
                float((sum([p.total_denda_filter for p in all_pk]))) + float(sum([p.tot_adm_kend_elek for p in all_pk_lunas])) +
                (sum([ p.tt_jual() for p in barang ])) + (sum([p.tot_simpan_kend_elek for p in all_pk_lunas])) +
                 float(sum([a.bea_jasa_kendaraan for a in all_pk]) + sum([a.bea_jasa for a in all_pk])),
            'jasa_terlambat': 0,
            't_noa': all_pk_lunas.count()  + all_pk.count(),
            'total_jual':(sum([ p.tt_jual() for p in barang ])),
            'start_date':start_date,'end_date':end_date,
            'total_noa_ayda':lapur_1.count(),
            'total_nilai_ayda':(sum([ p.nilai for p in lapur_1 ])),
            'total_noa_plns':lapur_1.count() + all_pk.count(),
            'total_nilai_plns':(sum([ p.nilai for p in lapur_1 ])) +(sum([ p.nilai for p in all_pk ])),
            'total_nilai_penjualan':(sum([ p.nilai for p in jual_ayda ])),
            'total_jasa_terlambat':sum([a.bea_jasa_kendaraan for a in all_pk]) + sum([a.bea_jasa for a in all_pk]),
            'total_piu':sum([a.nilai for a in piu])
            })
        return render_to_response(template, variables)

    
    elif  'start_date' in request.GET and request.GET['start_date'] and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        start_date = start_date
        end_date = end_date        
        trans = []

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 0, 'fg_color': '#D7E4BC'})        
        
        money_format = workbook.add_format({'num_format': '#,##0'})
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        merge_format = workbook.add_format({
            'bold':     True,
            'border':   6,
            'align':    'center',
            'valign':   'vcenter',
            'fg_color': '#D7E4BC',
            
        })

        worksheet.merge_range('A1:U1', 'Transaksi Pencairan Div Pjb', merge_format)
        worksheet.merge_range('A2:U2', 'Periode :'+ start_date + " s.d " + end_date, merge_format)
        worksheet.set_column(0, 0, 6) 
        worksheet.set_column(1, 1, 18)
        worksheet.set_column(2, 2, 10)
        worksheet.set_column(3, 3, 10)
        worksheet.set_column(4, 4, 10)
        worksheet.set_column(5, 5, 10)
        worksheet.set_column(6, 6, 10)
        worksheet.set_column(7, 7, 10)
        worksheet.set_column(8, 7, 10)
        worksheet.set_column(9, 9, 10)
        worksheet.set_column(10, 10, 10)
        worksheet.set_column(11, 11, 11)
        worksheet.set_column(12, 12, 12)

        worksheet.merge_range('A3:A4', 'KODE', merge_format)
        worksheet.merge_range('B3:B4', 'GERAI', merge_format)
        worksheet.merge_range('C3:D3', 'PENCAIRAN', merge_format)
        worksheet.write('C4', 'NOA PNCR', bold)
        worksheet.write('D4', 'NILAI PNCR ', bold)
        worksheet.merge_range('E3:J3', 'PELUNASAN', merge_format)
        worksheet.write('E4', 'NOA PLNS', bold)
        worksheet.write('F4', 'NILAI PLNS ', bold)
        worksheet.write('G4', 'NOA AYDA HISTORY', bold)
        worksheet.write('H4', 'NILAI AYDA HISTORY', bold)
        worksheet.write('I4', 'TOTAL NOA PLNS', bold)
        worksheet.write('J4', 'TOTAL NILAI PLNS ', bold)
        worksheet.merge_range('K3:L3', 'REAL AYDA', merge_format)
        worksheet.merge_range('M3:M4', 'PENJUALAN AYDA', merge_format)
        worksheet.merge_range('N3:T3', 'PENDAPATAN', merge_format)
        worksheet.write('K4', 'NOA AYDA HISTORY', bold)
        worksheet.write('L4', 'NILAI AYDA HISTORY(Rp)', bold)
        worksheet.write('N4', 'JASA', bold)
        worksheet.write('O4', 'JASA TERLAMBAT', bold)
        worksheet.write('P4', 'DENDA', bold)
        worksheet.write('Q4', 'BEASIMPAN', bold)
        worksheet.write('R4', 'ADM', bold)
        worksheet.write('S4', 'LABA PENJUALAN AYDA', bold)
        worksheet.write('T4', 'T.PENDAPATAN ', bold)
        worksheet.merge_range('U3:U4', 'PIUTANG', merge_format)

        row = 4
        col = 0
        for k in rekap:
            if k.akadgadai_set.filter(tanggal__range=(start_date,end_date)).filter(kepalagerai__status = 1).count()>=0:
                plns.append({'k':k,'aktif':k.aktif_nasabah_harian_filter(start_date,end_date),'kode_cabang':k.kode_cabang,'nama_cabang':k.nama_cabang,
                    'nilai_cair': k.nilai_pencairan_harian_filter(start_date,end_date),
                    'noa_cair':k.aktif_harian_filter(start_date, end_date),
                    'noa_lunas':k.aktif_plns_harian_filter(start_date, end_date),
                    'nilai_pelunasan':k.plns_nilai_harian_filter( start_date,end_date),
                    't_jasa':k.total_harian_jasa_filter(start_date,end_date),
                    't_denda':k.total_harian_denda_filter(start_date,end_date),
                    't_beasimpan':k.total_harian_beasimpan_filter(start_date,end_date),
                    't_adm':k.adm_harian_filter(start_date,end_date),
                    't_jual': k.ll_harga(start_date,end_date),
                    't_akumulasi':k.akumulasi_pendapatan_harian_filter(start_date,end_date),
                    'noa_ayda':k.noa_ayda(start_date, end_date),
                    'nilai_ayda':k.nilai_ayda(start_date, end_date),
                    'noa_ayda_history':k.noa_ayda_history(start_date, end_date),
                    'nilai_ayda_history':k.nilai_ayda_history(start_date, end_date),
                    'total_noa_ayda_lunas':k.total_noa_ayda_lunas(start_date, end_date),
                    'total_nilai_ayda_lunas':k.total_nilai_ayda_lunas(start_date, end_date),
                    'nilai_jual_ayda':k.nilai_jual_ayda(start_date, end_date),
                    'nilai_jasa_terlambat_plns':k.nilai_jasa_terlambat_plns(start_date,end_date)
                    })  

                start_date = start_date
                end_date = end_date

                worksheet.write(row, col , k.kode_cabang )                
                worksheet.write_string(row, col + 1, k.nama_cabang )
                worksheet.write_number(row, col + 2, k.aktif_harian_filter(start_date, end_date), money_format)
                worksheet.write_number(row, col + 3, k.nilai_pencairan_harian_filter(start_date,end_date), money_format)
                worksheet.write_number(row, col + 4, k.aktif_plns_harian_filter(start_date, end_date), money_format)
                worksheet.write_number(row, col + 5, k.plns_nilai_harian_filter( start_date,end_date),money_format)
                worksheet.write_number(row, col + 6, k.noa_ayda_history(start_date, end_date),money_format)
                worksheet.write_number(row, col + 7, k.nilai_ayda_history(start_date, end_date),money_format)
                worksheet.write_number(row, col + 8, k.total_noa_ayda_lunas(start_date, end_date),money_format)
                worksheet.write_number(row, col + 9, k.total_nilai_ayda_lunas(start_date, end_date),money_format)
                worksheet.write_number(row, col + 10, k.noa_ayda(start_date, end_date),money_format)
                worksheet.write_number(row, col + 11, k.nilai_ayda(start_date, end_date),money_format)
                worksheet.write_number(row, col + 12, k.nilai_jual_ayda(start_date, end_date),money_format)
                worksheet.write_number(row, col + 13, k.total_harian_jasa_filter(start_date, end_date),money_format)
                worksheet.write_number(row, col + 14, k.nilai_jasa_terlambat_plns(start_date, end_date),money_format)
                worksheet.write_number(row, col + 15, k.total_harian_denda_filter(start_date, end_date),money_format)
                worksheet.write_number(row, col + 16, k.total_harian_beasimpan_filter(start_date, end_date),money_format)
                worksheet.write_number(row, col + 17, k.adm_harian_filter(start_date, end_date),money_format)
                worksheet.write_number(row, col + 18, k.ll_harga(start_date, end_date),money_format)
                worksheet.write_number(row, col + 16, k.total_harian_beasimpan_filter(start_date, end_date),money_format)
                worksheet.write_number(row, col + 17, k.adm_harian_filter(start_date, end_date),money_format)
                worksheet.write_number(row, col + 18, k.ll_harga(start_date, end_date),money_format)
                worksheet.write_number(row, col + 19, k.akumulasi_pendapatan_harian_filter(start_date,end_date),money_format)
                worksheet.write_number(row, col + 20, k.rekap_piutang(end_date),money_format)
                row += 1
        '''
        worksheet.merge_range('A3:A4', 'KODE', merge_format)
        worksheet.merge_range('B3:B4', 'GERAI', merge_format)
        worksheet.merge_range('C3:D3', 'PENCAIRAN', merge_format)
        worksheet.write('C4', 'NOA PNCR', bold)
        worksheet.write('D4', 'NILAI PNCR ', bold)
        worksheet.merge_range('E3:J3', 'PELUNASAN', merge_format)
        worksheet.write('E4', 'NOA PLNS', bold)
        worksheet.write('F4', 'NILAI PLNS ', bold)
        worksheet.write('G4', 'NOA AYDA', bold)
        worksheet.write('H4', 'NILAI AYDA ', bold)
        worksheet.write('I4', 'TOTAL NOA PLNS', bold)
        worksheet.write('J4', 'TOTAL NILAI PLNS ', bold)
        worksheet.merge_range('K3:K4', 'PENJUALAN AYDA', merge_format)
        worksheet.merge_range('L3:R3', 'PENDAPATAN', merge_format)
        worksheet.write('L4', 'JASA', bold)
        worksheet.write('M4', 'JASA TERLAMBAT', bold)
        worksheet.write('N4', 'DENDA', bold)
        worksheet.write('O4', 'BEASIMPAN', bold)
        worksheet.write('P4', 'ADM', bold)
        worksheet.write('Q4', 'LABA PENJUALAN AYDA', bold)
        worksheet.write('R4', 'T.PENDAPATAN ', bold)
        worksheet.merge_range('S3:S4', 'PIUTANG', merge_format)

        row = 4
        col = 0
        for k in rekap:
            if k.akadgadai_set.filter(tanggal__range=(start_date,end_date)).filter(kepalagerai__status = 1).count()>=0:
                plns.append({'k':k,'aktif':k.aktif_nasabah_harian_filter(start_date,end_date),'kode_cabang':k.kode_cabang,'nama_cabang':k.nama_cabang,
                    'nilai_cair': k.nilai_pencairan_harian_filter(start_date,end_date),
                    'noa_cair':k.aktif_harian_filter(start_date, end_date),
                    'noa_lunas':k.aktif_plns_harian_filter(start_date, end_date),
                    'nilai_pelunasan':k.plns_nilai_harian_filter( start_date,end_date),
                    't_jasa':k.total_harian_jasa_filter(start_date,end_date),
                    't_denda':k.total_harian_denda_filter(start_date,end_date),
                    't_beasimpan':k.total_harian_beasimpan_filter(start_date,end_date),
                    't_adm':k.adm_harian_filter(start_date,end_date),
                    't_jual': k.ll_harga(start_date,end_date),
                    't_akumulasi':k.akumulasi_pendapatan_harian_filter(start_date,end_date),
                    'noa_ayda':k.noa_ayda(start_date, end_date),
                    'nilai_ayda':k.nilai_ayda(start_date, end_date),
                    'noa_ayda_history':k.noa_ayda_history(start_date, end_date),
                    'nilai_ayda_history':k.nilai_ayda_history(start_date, end_date),
                    'total_noa_ayda_lunas':k.total_noa_ayda_lunas(start_date, end_date),
                    'total_nilai_ayda_lunas':k.total_nilai_ayda_lunas(start_date, end_date),
                    'nilai_jual_ayda':k.nilai_jual_ayda(start_date, end_date),
                    'nilai_jasa_terlambat_plns':k.nilai_jasa_terlambat_plns(start_date,end_date)
                    })  

                start_date = start_date
                end_date = end_date
    
                worksheet.write(row, col , k.kode_cabang )                
                worksheet.write_string(row, col + 1, k.nama_cabang )
                worksheet.write_number(row, col + 2, k.aktif_harian_filter(start_date, end_date), money_format)
                worksheet.write_number(row, col + 3, k.nilai_pencairan_harian_filter(start_date,end_date), money_format)
                worksheet.write_number(row, col + 4, k.aktif_plns_harian_filter(start_date, end_date), money_format)
                worksheet.write_number(row, col + 5, k.plns_nilai_harian_filter( start_date,end_date),money_format)
                worksheet.write_number(row, col + 6, k.noa_ayda(start_date, end_date),money_format)
                worksheet.write_number(row, col + 7, k.nilai_ayda(start_date, end_date),money_format)
                worksheet.write_number(row, col + 8, k.total_noa_ayda_lunas(start_date, end_date),money_format)
                worksheet.write_number(row, col + 9, k.total_nilai_ayda_lunas(start_date, end_date),money_format)
                worksheet.write_number(row, col + 10, k.nilai_jual_ayda(start_date, end_date),money_format)
                worksheet.write_number(row, col + 11, k.total_harian_jasa_filter(start_date,end_date),money_format)
                worksheet.write_number(row, col + 12, k.nilai_jasa_terlambat_plns(start_date,end_date),money_format)
                worksheet.write_number(row, col + 13, k.total_harian_denda_filter(start_date,end_date),money_format)
                worksheet.write_number(row, col + 14, k.total_harian_beasimpan_filter(start_date,end_date),money_format)
                worksheet.write_number(row, col + 15, k.adm_harian_filter(start_date,end_date),money_format)
                worksheet.write_number(row, col + 16, k.ll_harga(start_date,end_date),money_format)
                worksheet.write_number(row, col + 17, k.akumulasi_pendapatan_harian_filter(start_date,end_date),money_format)
                worksheet.write_number(row, col + 18, k.rekap_piutang(end_date),money_format)
                row += 1
                ''' 
        workbook.close()    
        output.seek(0)    
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=rekap_pjb.xlsx"    
        return response        
    else:
        template='manop/filter/total_harian_filter.html'
        variable = RequestContext(request,{'form':form})
        return render_to_response(template,variable)

@login_required
@user_passes_test(is_in_multiple_groups)
def pencairan_gerai(request):
    akad= AkadGadai.objects.all()
    start_date = None
    end_date = None
    form = SearchForm()
    all = []
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET :
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            tb = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(kepalagerai__status = 1).order_by('gerai')
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template='manop/laporan/rekaphari.html'
            variable = RequestContext(request,{'tes':tb,
            'form':form,'id_cabang':id_cabang,'start_date':start_date,'end_date':end_date,'start_date':start_date,
            'end_date':end_date,'nilai': sum([b.nilai for b in tb ]),'jasa': sum([b.jasa for b in tb ]),
            'adm': sum([b.adm for b in tb ]) + sum([b.adm_kendaraan for b in tb]),'simpan': sum([b.biayasimpan for b in tb ]) + sum([b.beasimpan_kendaraan for b in tb]),
            'bersih' : sum([b.jumlah_biaya for b in tb ]),})
            return render_to_response(template,variable)
        else:
            tb = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(gerai__kode_cabang = id_cabang).filter(kepalagerai__status = 1)
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template='manop/laporan/rekaphari.html'
            variable = RequestContext(request,{'tes':tb,'form':form,'id_cabang':id_cabang,'start_date':start_date,
            'end_date':end_date,'nilai': sum([b.nilai for b in tb ]),'jasa': sum([b.jasa for b in tb ]),
            'adm': sum([b.adm for b in tb ]) + sum([b.adm_kendaraan for b in tb]),'simpan': sum([b.biayasimpan for b in tb ]) + sum([b.beasimpan_kendaraan for b in tb]),
            'bersih' : sum([b.jumlah_biaya for b in tb ]),})
            return render_to_response(template,variable)
    
    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            tb = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(kepalagerai__status = 1).order_by('gerai')
            template1= 'manop/laporan/cetak_rekaphari.html'
            variable = RequestContext(request,{'tes':tb,'form':form,'start_date':start_date,'end_date':end_date,
            'id_cabang':id_cabang,'nilai': sum([b.nilai for b in tb ]),'jasa': sum([b.jasa for b in tb ]),
            'adm': sum([b.adm for b in tb ]) + sum([b.adm_kendaraan for b in tb]),'simpan': sum([b.biayasimpan for b in tb ]) + sum([b.beasimpan_kendaraan for b in tb]),
            'bersih' : sum([b.jumlah_biaya for b in tb ]),})
            return render_to_response(template1,variable)
        else:
            tb = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(gerai__kode_cabang = id_cabang).filter(kepalagerai__status = 1)
            template1= 'manop/laporan/cetak_rekaphari.html'
            variable = RequestContext(request,{'tes':tb,'form':form,'id_cabang':id_cabang,
            'start_date':start_date,'end_date':end_date,'nilai': sum([b.nilai for b in tb ]),
            'jasa': sum([b.jasa for b in tb ]),'adm': sum([b.adm for b in tb ]) + sum([b.adm_kendaraan for b in tb]),
            'simpan': sum([b.biayasimpan for b in tb ]) + sum([b.beasimpan_kendaraan for b in tb]),'bersih' : sum([b.jumlah_biaya for b in tb ]),})
            return render_to_response(template1,variable)

    elif 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']         
        if id_cabang == '500':
            tb = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(kepalagerai__status = 1).order_by('gerai')
            a = sum([b.nilai for b in tb ])
            c = sum([b.jasa for b in tb ]) 
            d = sum([b.adm for b in tb ]) 
            e = sum([b.biayasimpan for b in tb ]) 
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
            worksheet.set_column(10, 10, 10)
            worksheet.set_column(11, 11, 10)
            worksheet.set_column(12, 12, 10)
            worksheet.set_column(13, 13, 10)
        
            worksheet.merge_range('A1:L1', 'LAPORAN PENCAIRAN DAN GADAI ULANG GABUNGAN', merge_format1)
            worksheet.merge_range('A2:L2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Nama', merge_format)
            worksheet.merge_range('C4:C5', 'Alamat Identitas', merge_format)
            worksheet.merge_range('D4:D5', 'No Identitas', merge_format)
            worksheet.merge_range('E4:E5', 'No Telepon', merge_format)
            worksheet.merge_range('F4:F5', 'Jenis Barang', merge_format)
            worksheet.merge_range('G4:G5', 'Barang', merge_format)
            worksheet.merge_range('H4:H5', 'Tgl Akad', merge_format)
            worksheet.merge_range('I4:I5', 'Jangka Waktu', merge_format)
            worksheet.merge_range('J4:J5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('K4:K5', 'Nilai',  merge_format)
            worksheet.merge_range('L4:L5', 'Gerai', merge_format)
            worksheet.merge_range('M4:M5', 'Status', merge_format)

            row = 5
            col = 0
            for t in tb:
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.agnasabah.nama)
                worksheet.write_string(row, col + 2 , t.agnasabah.alamat_ktp)
                worksheet.write_string(row, col + 3 , t.agnasabah.no_ktp)
                worksheet.write_string(row, col + 4 , t.agnasabah.telepon_ktp)
                worksheet.write_string(row, col + 5 , t.barang.get_jenis_barang_display())
                worksheet.write_string(row, col + 6 , t.barang.merk)
                worksheet.write_datetime(row, col + 7 , t.tanggal,date_format)
                worksheet.write(row, col + 8 , t.jw_all())
                worksheet.write_datetime(row, col + 9, t.jatuhtempo, date_format)
                worksheet.write_number(row, col + 10, t.nilai, money_format)
                worksheet.write_string(row, col + 11 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 12, t.get_jns_gu_display())

                row += 1

            worksheet.write(row,4, 'Total', bold)    
            worksheet.write(row,8, a, money_format)
            worksheet.write(row, 9, c, money_format)
            worksheet.write(row, 10, d, money_format)
            worksheet.write(row, 11, e, money_format)
        
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Laporan_Pencairan.xlsx"
            return response
        else:
            tb = AkadGadai.objects.filter(tanggal__range=(start_date,end_date)).exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(gerai__kode_cabang = id_cabang).filter(kepalagerai__status = 1)
            a = sum([b.nilai for b in tb ])
            c = sum([b.jasa for b in tb ]) 
            d = sum([b.adm for b in tb ]) 
            e = sum([b.biayasimpan for b in tb ]) 
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
            worksheet.set_column(10, 10, 10)
            worksheet.set_column(11, 11, 10)
            worksheet.set_column(12, 12, 10)
            worksheet.set_column(13, 13, 10)
            worksheet.merge_range('A1:L1', 'LAPORAN PENCAIRAN DAN GADAI ULANG', merge_format1)
            worksheet.merge_range('A2:L2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Nama', merge_format)
            worksheet.merge_range('C4:C5', 'Alamat Identitas', merge_format)
            worksheet.merge_range('D4:D5', 'No Identitas', merge_format)
            worksheet.merge_range('E4:E5', 'No Telepon', merge_format)
            worksheet.merge_range('F4:F5', 'Jenis Barang', merge_format)
            worksheet.merge_range('G4:G5', 'Barang', merge_format)
            worksheet.merge_range('H4:H5', 'Tgl Akad', merge_format)
            worksheet.merge_range('I4:I5', 'Jangka Waktu', merge_format)
            worksheet.merge_range('J4:J5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('K4:K5', 'Nilai',  merge_format)
            worksheet.merge_range('L4:L5', 'Gerai', merge_format)
            worksheet.merge_range('M4:M5', 'Status', merge_format)
            row = 5
            col = 0
            for t in tb:
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.agnasabah.nama)
                worksheet.write_string(row, col + 2 , t.agnasabah.alamat_ktp)
                worksheet.write_string(row, col + 3 , t.agnasabah.no_ktp)
                worksheet.write_string(row, col + 4 , t.agnasabah.telepon_ktp)
                worksheet.write_string(row, col + 5 , t.barang.get_jenis_barang_display())
                worksheet.write_string(row, col + 6 , t.barang.merk)
                worksheet.write_datetime(row, col + 7 , t.tanggal,date_format)
                worksheet.write(row, col + 8 , t.jw_all())
                worksheet.write_datetime(row, col + 9, t.jatuhtempo, date_format)
                worksheet.write_number(row, col + 10, t.nilai, money_format)
                worksheet.write_string(row, col + 11 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 12, t.get_jns_gu_display()) 
 
                row += 1

            worksheet.write(row,4, 'Total', bold)    
            worksheet.write(row,8, a, money_format)
            worksheet.write(row,9, c, money_format)
            worksheet.write(row,10, d, money_format)
            worksheet.write(row,11, e, money_format)
            workbook.close()
            output.seek(0)
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=Laporan_Pencairan.xlsx"
            return response
    else:
        variables = RequestContext(request, {'form': form})
        return render_to_response('manop/laporan/rekaphari.html', variables)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('manop','asmanpjb')))
def list(request):
    manop = AkadGadai.objects.filter(status_taksir=2)
    
    template = 'manop/manop.html'
    variables = RequestContext(request, {'manop': manop})    
    return render_to_response(template, variables)

def list_cari(request):
    manop = AkadGadai.objects.filter(status_taksir=2)
    
    template = 'manop/manop_cari.html'
    variables = RequestContext(request, {'manop': manop})    
    return render_to_response(template, variables)

