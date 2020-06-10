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
from gadai.appgadai.gudang.forms import *

def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['manop','baranglapur','admops','gudang','KEPALAGUDANG','GUDANGAKTIF','asmanpjb','staffops','superuser'])

@login_required
@user_passes_test(is_in_multiple_groups)
def data_gudang_barang_aktif(request):    
    kp = []
    start_date = None
    end_date = None
    id_cabang = None
    id_barang = None
    form = SearchGudangForm()
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET:
        end_date = request.GET['end_date']
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        id_barang = request.GET['id_barang']

        ## cbng All - brng All
        if id_cabang == '500' and id_barang =='500' :
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).\
                filter(tanggal__range=(start_date,end_date)).order_by('gerai')
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'gudang/barang/barang_gudang_aktif.html'
            variables = RequestContext(request, {'kp':akad,'start_date':start_date,'form':form,'end_date':end_date,'id_cabang':id_cabang,\
                'nilai':sum([a.nilai for a in akad])})
            return render_to_response(template, variables)

        ## cbng All - brng Id
        elif id_cabang == '500' :
            if id_barang == '6':
                akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                    filter(tanggal__range=(start_date,end_date)).filter(barang__jenis_kendaraan = '1' )
            elif id_barang == '7':
                akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                    filter(barang__jenis_kendaraan= '2').filter(tanggal__range=(start_date,end_date)).order_by('gerai')
            else:
                akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                    filter(barang__jenis_barang= id_barang).filter(tanggal__range=(start_date,end_date)).order_by('gerai')
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'gudang/barang/barang_gudang_aktif.html'
            variables = RequestContext(request, {'kp':akad,'form':form,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,\
                'nilai':sum([a.nilai for a in akad])})
            return render_to_response(template, variables)

        ## cbng Id - brng All
        elif id_barang == '500' :
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(gerai__kode_cabang= id_cabang).filter(tanggal__range=(start_date,end_date)).order_by('barang')
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'gudang/barang/barang_gudang_aktif.html'
            variables = RequestContext(request, {'kp':akad,'form':form,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,\
                'nilai':sum([a.nilai for a in akad])})
            return render_to_response(template, variables)
            
        ## cbng Id - brng MOTOR
        elif id_barang == '6':
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(tanggal__range=(start_date,end_date)).filter(gerai__kode_cabang= id_cabang).filter(barang__jenis_kendaraan = '1' )
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'gudang/barang/barang_gudang_aktif.html'
            variables = RequestContext(request, {'kp':akad,'start_date':start_date,'form':form,'end_date':end_date,'id_cabang':id_cabang,\
                'nilai':sum([a.nilai for a in akad])})
            return render_to_response(template, variables)
            
        ## cbng Id - brng MOBIL
        elif id_barang == '7':
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(tanggal__range=(start_date,end_date)).filter(gerai__kode_cabang = id_cabang).filter(barang__jenis_kendaraan= '2')
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'gudang/barang/barang_gudang_aktif.html'
            variables = RequestContext(request, {'kp':akad,'start_date':start_date,'form':form,'end_date':end_date,'id_cabang':id_cabang,\
                'nilai':sum([a.nilai for a in akad])})
            return render_to_response(template, variables)

        ## cbng All - brng Id MOTOR
        elif id_cabang == '500' and id_barang == '6':
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(tanggal__range=(start_date,end_date)).filter(barang__jenis_kendaraan= '1')
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'gudang/barang/barang_gudang_aktif.html'
            variables = RequestContext(request, {'kp':kp,'start_date':start_date,'form':form,'end_date':end_date,'id_cabang':id_cabang,\
                'nilai':sum([a.nilai for a in akad])})
            return render_to_response(template, variables)
        
        ## cbng All - brng Id MOBIL
        elif id_cabang == '500' and id_barang == '7':
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(barang__jenis_kendaraan= '2').filter(tanggal__range=(start_date,end_date)).order_by('gerai')
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'gudang/barang/barang_gudang_aktif.html'
            variables = RequestContext(request, {'kp':akad,'start_date':start_date,'form':form,'end_date':end_date,'id_cabang':id_cabang,\
                'nilai':sum([a.nilai for a in akad])})
            return render_to_response(template, variables)
        ## cbng Id - brng Id
        else:
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(tanggal__range=(start_date,end_date)).filter(gerai__kode_cabang= id_cabang).filter(barang__jenis_barang= id_barang)
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'gudang/barang/barang_gudang_aktif.html'
            variables = RequestContext(request, {'kp':akad,'start_date':start_date,'form':form,'end_date':end_date,'id_cabang':id_cabang,
                'nilai':sum([a.nilai for a in akad])})
            return render_to_response(template, variables)

    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        end_date = request.GET['end_date']
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        id_barang = request.GET['id_barang']

        ## cbng All - brng All
        if id_cabang == '500' and id_barang =='500' :
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(tanggal__range=(start_date,end_date)).order_by('gerai')
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template1 = 'gudang/barang/cetak_barang_gudang_aktif.html'
            variables = RequestContext(request, {'kp':akad,'start_date':start_date,'form':form,'end_date':end_date,'id_cabang':id_cabang,
                'nilai':sum([a.nilai for a in akad])})
            return render_to_response(template1, variables)
        
        ## cbng All - brng Id MOTOR
        elif id_cabang == '500' and id_barang =='6' :
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(tanggal__range=(start_date,end_date)).filter(barang__jenis_kendaraan= '1').order_by('gerai')
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template1 = 'gudang/barang/cetak_barang_gudang_aktif.html'
            variables = RequestContext(request, {'kp':akad,'start_date':start_date,'form':form,'end_date':end_date,'id_cabang':id_cabang,\
                'nilai':sum([a.nilai for a in akad])})
            return render_to_response(template1, variables)
        
        ## cbng All - brng Id MOBIL
        elif id_cabang == '500' and id_barang =='7' :
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(barang__jenis_kendaraan= '2').filter(tanggal__range=(start_date,end_date)).order_by('gerai')
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template1 = 'gudang/barang/cetak_barang_gudang_aktif.html'
            variables = RequestContext(request, {'kp':akad,'start_date':start_date,'form':form,'end_date':end_date,'id_cabang':id_cabang,\
                'nilai':sum([a.nilai for a in akad])})
            return render_to_response(template1, variables)

        ## cbng All - brng Id
        elif id_cabang == '500' :
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(barang__jenis_barang= id_barang).filter(tanggal__range=(start_date,end_date)).order_by('gerai')
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template1 = 'gudang/barang/cetak_barang_gudang_aktif.html'
            variables = RequestContext(request, {'kp':akad,'start_date':start_date,'form':form,'end_date':end_date,'id_cabang':id_cabang,\
                'nilai':sum([a.nilai for a in akad])})
            return render_to_response(template1, variables)

        ## cbng Id - brng All
        elif id_barang == '500' :
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(gerai__kode_cabang= id_cabang).filter(tanggal__range=(start_date,end_date)).order_by('barang')
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template1 = 'gudang/barang/cetak_barang_gudang_aktif.html'
            variables = RequestContext(request, {'kp':akad,'start_date':start_date,'form':form,'end_date':end_date,'id_cabang':id_cabang,\
                'nilai':sum([a.nilai for a in akad])})
            return render_to_response(template1, variables)
            
        ## cbng Id - brng MOTOR
        elif id_barang == '6':
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(gerai__id= id_cabang).filter(tanggal__range=(start_date,end_date)).filter(barang__jenis_kendaraan = '1' )
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template1 = 'gudang/barang/cetak_barang_gudang_aktif.html'
            variables = RequestContext(request, {'kp':akad,'start_date':start_date,'form':form,'end_date':end_date,'id_cabang':id_cabang,\
                'nilai':sum([a.nilai for a in akad])})
            return render_to_response(template1, variables)
            
        ## cbng Id - brng MOBIL
        elif id_barang == '7':
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(tanggal__range=(start_date,end_date)).filter(gerai__kode_cabang= id_cabang).filter(barang__jenis_kendaraan= '2')
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template1 = 'gudang/barang/cetak_barang_gudang_aktif.html'
            variables = RequestContext(request, {'kp':akad,'start_date':start_date,'form':form,'end_date':end_date,'id_cabang':id_cabang,\
                'nilai':sum([a.nilai for a in akad])})
            return render_to_response(template1, variables)

        ## cbng Id - brng Id
        else:
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(tanggal__range=(start_date,end_date)).filter(gerai__kode_cabang= id_cabang).filter(barang__jenis_barang= id_barang)
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template1 = 'gudang/barang/cetak_barang_gudang_aktif.html'
            variables = RequestContext(request, {'kp':akad,'start_date':start_date,'form':form,'end_date':end_date,'id_cabang':id_cabang,\
                'nilai':sum([a.nilai for a in akad])})
            return render_to_response(template1, variables)

    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        end_date = request.GET['end_date']
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        id_barang = request.GET['id_barang']
        ## cbng All - brng All
        if id_cabang == '500' and id_barang =='500' :
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8','9','10')).\
                filter(tanggal__range=(start_date,end_date)).order_by('gerai')
            a = sum([b.nilai for b in akad ])
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
            
        
            worksheet.merge_range('A1:N1', 'LAPORAN DATA BARANG GUDANG AKTIF ', merge_format1)
            worksheet.merge_range('A2:N2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama', merge_format)
            worksheet.merge_range('D4:D5', 'Jenis Barang', merge_format)
            worksheet.merge_range('E4:E5', 'Barang', merge_format)
            worksheet.merge_range('F4:F5', 'Status Barang', merge_format)
            worksheet.merge_range('G4:G5', 'Tanggal Akad', merge_format)
            worksheet.merge_range('H4:H5', 'JW', merge_format)
            worksheet.merge_range('I4:I5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('J4:J5', 'Nilai', merge_format)
            worksheet.merge_range('K4:N4', 'Data Gudang', merge_format)
            worksheet.write_string('K5', 'Ruang', merge_format)
            worksheet.write_string('L5', 'Lemari', merge_format)
            worksheet.write_string('M5', 'Rak', merge_format)
            worksheet.write_string('N5', 'Row', merge_format)
            

            row = 5
            col = 0
            for t in akad:
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.agnasabah.nama)
                worksheet.write_string(row, col + 3 , t.jenis_barang_all())
                worksheet.write_string(row, col + 4 , t.kode_barang_all())
                worksheet.write_string(row, col + 5, 'Aktif')
                worksheet.write_datetime(row, col + 6, t.tanggal, date_format)
                if t.jw_all():
                    worksheet.write_string(row, col + 7, t.jw_all())
                else:
                    worksheet.write_string(row, col + 7, '-')
                worksheet.write_datetime(row, col + 8, t.jatuhtempo, date_format)
                worksheet.write_number(row, col + 9, t.nilai, money_format)
                if t.ruang_barang == None:                
                    worksheet.write_string(row, col + 10, '0')
                else:
                   worksheet.write_string(row, col + 10, t.ruang_barang)
                if t.lemari_barang == None:
                    worksheet.write_string(row, col + 11, '0')
                else:
                    worksheet.write_string(row, col + 11, t.lemari_barang)
                if t.rak_barang == None:
                    worksheet.write_string(row, col + 12, '0')
                else:
                    worksheet.write_string(row, col + 12, t.rak_barang)
                if t.row_barang == None:
                    worksheet.write_string(row, col + 13, '0')
                else:
                    worksheet.write_string(row, col + 13, t.row_barang)                
                row += 1

            worksheet.write(row,3, 'Total', bold)    
            worksheet.write(row,9, a, money_format)
           
       
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename= barang_gudang_aktif.xlsx"
            return response
        
        ## cbng All - brng Id MOTOR
        elif id_cabang == '500' and id_barang =='6' :
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(tanggal__range=(start_date,end_date)).filter(barang__jenis_kendaraan= '1').order_by('gerai')
            a = sum([b.nilai for b in akad ])            
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
            
        
            worksheet.merge_range('A1:N1', 'LAPORAN DATA BARANG GUDANG AKTIF GERAI ', merge_format1)
            worksheet.merge_range('A2:N2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama', merge_format)
            worksheet.merge_range('D4:D5', 'Jenis Barang', merge_format)
            worksheet.merge_range('E4:E5', 'Barang', merge_format)
            worksheet.merge_range('F4:F5', 'Status Barang', merge_format)
            worksheet.merge_range('G4:G5', 'Tanggal Akad', merge_format)
            worksheet.merge_range('H4:H5', 'JW', merge_format)
            worksheet.merge_range('I4:I5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('J4:J5', 'Nilai', merge_format)
            worksheet.merge_range('K4:N4', 'Data Gudang', merge_format)
            worksheet.write_string('K5', 'Ruang')
            worksheet.write_string('L5', 'Lemari')
            worksheet.write_string('M5', 'Rak')
            worksheet.write_string('N5', 'Row')
            

            row = 6
            col = 0
            for t in akad:
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.agnasabah.nama)
                worksheet.write_string(row, col + 3 , t.jenis_barang_all())
                worksheet.write_string(row, col + 4 , t.kode_barang_all())
                worksheet.write_string(row, col + 5, 'Aktif')
                worksheet.write_datetime(row, col + 6, t.tanggal, date_format)
                if t.jw_all():
                    worksheet.write_string(row, col + 7, t.jw_all())
                else:
                    worksheet.write_string(row, col + 7, '-')
                worksheet.write_datetime(row, col + 8, t.jatuhtempo, date_format)
                worksheet.write_number(row, col + 9, t.nilai, money_format)
                if t.ruang_barang == None:
                    worksheet.write_string(row, col + 10, '0')
                else:
                   worksheet.write_string(row, col + 10, t.ruang_barang)
                if t.lemari_barang == None:
                    worksheet.write_string(row, col + 11, '0')
                else:
                    worksheet.write_string(row, col + 11, t.lemari_barang)
                if t.rak_barang == None:
                    worksheet.write_string(row, col + 12, '0')
                else:
                    worksheet.write_string(row, col + 12, t.rak_barang)
                if t.row_barang == None:
                    worksheet.write_string(row, col + 13, '0')
                else:
                    worksheet.write_string(row, col + 13, t.row_barang)
                row += 1
            worksheet.write(row,3, 'Total', bold)    
            worksheet.write(row,9, a, money_format)
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename= barang_gudang_aktif.xlsx"
            return response
        
        ## cbng All - brng Id MOBIL
        elif id_cabang == '500' and id_barang =='7' :
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(barang__jenis_kendaraan= '2').filter(tanggal__range=(start_date,end_date)).order_by('gerai')
            a = sum([b.nilai for b in akad ])
            
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
            
        
            worksheet.merge_range('A1:N1', 'LAPORAN DATA BARANG GUDANG AKTIF ', merge_format1)
            worksheet.merge_range('A2:N2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama', merge_format)
            worksheet.merge_range('D4:D5', 'Jenis Barang', merge_format)
            worksheet.merge_range('E4:E5', 'Barang', merge_format)
            worksheet.merge_range('F4:F5', 'Status Barang', merge_format)
            worksheet.merge_range('G4:G5', 'Tanggal Akad', merge_format)
            worksheet.merge_range('H4:H5', 'JW', merge_format)
            worksheet.merge_range('I4:I5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('J4:J5', 'Nilai', merge_format)
            worksheet.merge_range('K4:N4', 'Data Gudang', merge_format)
            worksheet.write_string('K5', 'Ruang')
            worksheet.write_string('L5', 'Lemari')
            worksheet.write_string('M5', 'Rak')
            worksheet.write_string('N5', 'Row')

            row = 6
            col = 0
            for t in akad:
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.agnasabah.nama)
                worksheet.write_string(row, col + 3 , t.jenis_barang_all())
                worksheet.write_string(row, col + 4 , t.kode_barang_all())
                worksheet.write_string(row, col + 5, 'Aktif')
                worksheet.write_datetime(row, col + 6, t.tanggal, date_format)
                if t.jw_all:
                    worksheet.write_string(row, col + 7, t.jw_all())
                else:
                    worksheet.write_string(row, col + 7, '-')

                worksheet.write_datetime(row, col + 8, t.jatuhtempo, date_format)
                worksheet.write_number(row, col + 9, t.nilai, money_format)
                if t.ruang_barang == None:
                    worksheet.write_string(row, col + 10, '0')
                else:
                   worksheet.write_string(row, col + 10, t.ruang_barang)
                if t.lemari_barang == None:
                    worksheet.write_string(row, col + 11, '0')
                else:
                    worksheet.write_string(row, col + 11, t.lemari_barang)
                if t.rak_barang == None:
                    worksheet.write_string(row, col + 12, '0')
                else:
                    worksheet.write_string(row, col + 12, t.rak_barang)
                if t.row_barang == None:
                    worksheet.write_string(row, col + 13, '0')
                else:
                    worksheet.write_string(row, col + 13, t.row_barang)                
                
                row += 1

            worksheet.write(row,3, 'Total', bold)    
            worksheet.write(row,9, a, money_format)
           
       
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename= barang_gudang_aktif.xlsx"
            return response

        ## cbng All - brng Id
        elif id_cabang == '500' :
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(barang__jenis_barang= id_barang).filter(tanggal__range=(start_date,end_date)).order_by('gerai')
            a = sum([b.nilai for b in akad ])            
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
            
        
            worksheet.merge_range('A1:N1', 'LAPORAN DATA BARANG GUDANG AKTIF ', merge_format1)
            worksheet.merge_range('A2:N2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama', merge_format)
            worksheet.merge_range('D4:D5', 'Jenis Barang', merge_format)
            worksheet.merge_range('E4:E5', 'Barang', merge_format)
            worksheet.merge_range('F4:F5', 'Status Barang', merge_format)
            worksheet.merge_range('G4:G5', 'Tanggal Akad', merge_format)
            worksheet.merge_range('H4:H5', 'JW', merge_format)
            worksheet.merge_range('I4:I5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('J4:J5', 'Nilai', merge_format)
            worksheet.merge_range('K4:N4', 'Data Gudang', merge_format)
            worksheet.write_string('K5', 'Ruang')
            worksheet.write_string('L5', 'Lemari')
            worksheet.write_string('M5', 'Rak')
            worksheet.write_string('N5', 'Row')

            row = 6
            col = 0
            for t in akad:
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.agnasabah.nama)
                worksheet.write_string(row, col + 3 , t.jenis_barang_all())
                worksheet.write_string(row, col + 4 , t.kode_barang_all())
                worksheet.write_string(row, col + 5, 'Aktif')
                worksheet.write_datetime(row, col + 6, t.tanggal, date_format)
                if t.jw_all():
                    worksheet.write_string(row, col + 7, t.jw_all())
                else:
                    worksheet.write_string(row, col + 7, '-')
                worksheet.write_datetime(row, col + 8, t.jatuhtempo, date_format)
                worksheet.write_number(row, col + 9, t.nilai, money_format)
                if t.ruang_barang == None:
                    worksheet.write_string(row, col + 10, '0')
                else:
                   worksheet.write_string(row, col + 10, t.ruang_barang)
                if t.lemari_barang == None:
                    worksheet.write_string(row, col + 11, '0')
                else:
                    worksheet.write_string(row, col + 11, t.lemari_barang)
                if t.rak_barang == None:
                    worksheet.write_string(row, col + 12, '0')
                else:
                    worksheet.write_string(row, col + 12, t.rak_barang)
                if t.row_barang == None:
                    worksheet.write_string(row, col + 13, '0')
                else:
                    worksheet.write_string(row, col + 13, t.row_barang)                
                
                row += 1

            worksheet.write(row,3, 'Total', bold)    
            worksheet.write(row,9, a, money_format)
           
       
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename= barang_gudang_aktif.xlsx"
            return response

        ## cbng Id - brng All
        elif id_barang == '500' :
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(gerai__kode_cabang= id_cabang).filter(tanggal__range=(start_date,end_date)).order_by('barang')
            a = sum([b.nilai for b in akad ])
            
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
            
        
            worksheet.merge_range('A1:N1', 'LAPORAN DATA BARANG GUDANG AKTIF ', merge_format1)
            worksheet.merge_range('A2:N2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama', merge_format)
            worksheet.merge_range('D4:D5', 'Jenis Barang', merge_format)
            worksheet.merge_range('E4:E5', 'Barang', merge_format)
            worksheet.merge_range('F4:F5', 'Status Barang', merge_format)
            worksheet.merge_range('G4:G5', 'Tanggal Akad', merge_format)
            worksheet.merge_range('H4:H5', 'JW', merge_format)
            worksheet.merge_range('I4:I5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('J4:J5', 'Nilai', merge_format)
            worksheet.merge_range('K4:N4', 'Data Gudang', merge_format)
            worksheet.write_string('K5', 'Ruang')
            worksheet.write_string('L5', 'Lemari')
            worksheet.write_string('M5', 'Rak')
            worksheet.write_string('N5', 'Row')
            
            row = 6
            col = 0
            for t in akad:
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.agnasabah.nama)
                worksheet.write_string(row, col + 3 , t.jenis_barang_all())
                worksheet.write_string(row, col + 4 , t.kode_barang_all())
                worksheet.write_string(row, col + 5, 'Aktif')
                worksheet.write_datetime(row, col + 6, t.tanggal, date_format)
                if t.jw_all():
                    worksheet.write_string(row, col + 7, t.jw_all())
                else:
                    worksheet.write_string(row, col + 7, '-')
                worksheet.write_datetime(row, col + 8, t.jatuhtempo, date_format)
                worksheet.write_number(row, col + 9, t.nilai, money_format)
                if t.ruang_barang == None:
                    worksheet.write_string(row, col + 10, '0')
                else:
                   worksheet.write_string(row, col + 10, t.ruang_barang)
                if t.lemari_barang == None:
                    worksheet.write_string(row, col + 11, '0')
                else:
                    worksheet.write_string(row, col + 11, t.lemari_barang)
                if t.rak_barang == None:
                    worksheet.write_string(row, col + 12, '0')
                else:
                    worksheet.write_string(row, col + 12, t.rak_barang)
                if t.row_barang == None:
                    worksheet.write_string(row, col + 13, '0')
                else:
                    worksheet.write_string(row, col + 13, t.row_barang)                
                
                row += 1

            worksheet.write(row,3, 'Total', bold)    
            worksheet.write(row,9, a, money_format)
           
       
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename= barang_gudang_aktif.xlsx"
            return response
            
        ## cbng Id - brng MOTOR
        elif id_barang == '6':
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(gerai__kode_cabang= id_cabang).filter(tanggal__range=(start_date,end_date)).filter(barang__jenis_kendaraan = '1' )
            a = sum([b.nilai for b in akad ])            
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
            
        
            worksheet.merge_range('A1:N1', 'LAPORAN DATA BARANG GUDANG AKTIF ', merge_format1)
            worksheet.merge_range('A2:N2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama', merge_format)
            worksheet.merge_range('D4:D5', 'Jenis Barang', merge_format)
            worksheet.merge_range('E4:E5', 'Barang', merge_format)
            worksheet.merge_range('F4:F5', 'Status Barang', merge_format)
            worksheet.merge_range('G4:G5', 'Tanggal Akad', merge_format)
            worksheet.merge_range('H4:H5', 'JW', merge_format)
            worksheet.merge_range('I4:I5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('J4:J5', 'Nilai', merge_format)
            worksheet.merge_range('K4:N4', 'Data Gudang', merge_format)
            worksheet.write_string('K5', 'Ruang')
            worksheet.write_string('L5', 'Lemari')
            worksheet.write_string('M5', 'Rak')
            worksheet.write_string('N5', 'Row')

            row = 6
            col = 0
            for t in akad:
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.agnasabah.nama)
                worksheet.write_string(row, col + 3 , t.jenis_barang_all())
                worksheet.write_string(row, col + 4 , t.kode_barang_all())
                worksheet.write_string(row, col + 5, 'Aktif')
                worksheet.write_datetime(row, col + 6, t.tanggal, date_format)
                if t.jw_all():
                    worksheet.write_string(row, col + 7, t.jw_all())
                else:
                    worksheet.write_string(row, col + 7, t.jw_all())
                worksheet.write_datetime(row, col + 8, t.jatuhtempo, date_format)
                worksheet.write_number(row, col + 9, t.nilai, money_format)
                if t.ruang_barang == None:
                    worksheet.write_string(row, col + 10, '0')
                else:
                   worksheet.write_string(row, col + 10, t.ruang_barang)
                if t.lemari_barang == None:
                    worksheet.write_string(row, col + 11, '0')
                else:
                    worksheet.write_string(row, col + 11, t.lemari_barang)
                if t.rak_barang == None:
                    worksheet.write_string(row, col + 12, '0')
                else:
                    worksheet.write_string(row, col + 12, t.rak_barang)
                if t.row_barang == None:
                    worksheet.write_string(row, col + 13, '0')
                else:
                    worksheet.write_string(row, col + 13, t.row_barang)                
                
                row += 1

            worksheet.write(row,3, 'Total', bold)    
            worksheet.write(row,9, a, money_format)
           
       
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename= barang_gudang_aktif.xlsx"
            return response
            
        ## cbng Id - brng MOBIL
        elif id_barang == '7':
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(gerai__kode_cabang= id_cabang).filter(tanggal__range=(start_date,end_date)).filter(barang__jenis_kendaraan = '1' )
            a = sum([b.nilai for b in akad ])
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
            
        
            worksheet.merge_range('A1:N1', 'LAPORAN DATA BARANG GUDANG AKTIF ', merge_format1)
            worksheet.merge_range('A2:N2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama', merge_format)
            worksheet.merge_range('D4:D5', 'Jenis Barang', merge_format)
            worksheet.merge_range('E4:E5', 'Barang', merge_format)
            worksheet.merge_range('F4:F5', 'Status Barang', merge_format)
            worksheet.merge_range('G4:G5', 'Tanggal Akad', merge_format)
            worksheet.merge_range('H4:H5', 'JW', merge_format)
            worksheet.merge_range('I4:I5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('J4:J5', 'Nilai', merge_format)
            worksheet.merge_range('K4:N4', 'Data Gudang', merge_format)
            worksheet.write_string('K5', 'Ruang')
            worksheet.write_string('L5', 'Lemari')
            worksheet.write_string('M5', 'Rak')
            worksheet.write_string('N5', 'Row') 

            row = 6
            col = 0
            for t in akad:
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.agnasabah.nama)
                worksheet.write_string(row, col + 3 , t.jenis_barang_all())
                worksheet.write_string(row, col + 4 , t.kode_barang_all())
                worksheet.write_string(row, col + 5, 'Aktif')
                worksheet.write_datetime(row, col + 6, t.tanggal, date_format)
                if t.jw_all():
                    worksheet.write_string(row, col + 7, t.jw_all())
                else:
                    worksheet.write_string(row, col + 7, '-')
                worksheet.write_datetime(row, col + 8, t.jatuhtempo, date_format)
                worksheet.write_number(row, col + 9, t.nilai, money_format)
                if t.ruang_barang == None:
                    worksheet.write_string(row, col + 10, '0')
                else:
                   worksheet.write_string(row, col + 10, t.ruang_barang)
                if t.lemari_barang == None:
                    worksheet.write_string(row, col + 11, '0')
                else:
                    worksheet.write_string(row, col + 11, t.lemari_barang)
                if t.rak_barang == None:
                    worksheet.write_string(row, col + 12, '0')
                else:
                    worksheet.write_string(row, col + 12, t.rak_barang)
                if t.row_barang == None:
                    worksheet.write_string(row, col + 13, '0')
                else:
                    worksheet.write_string(row, col + 13, t.row_barang)                
                
                row += 1

            worksheet.write(row,3, 'Total', bold)    
            worksheet.write(row,9, a, money_format)
           
       
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename= barang_gudang_aktif.xlsx"
            return response

        ## cbng Id - brng Id
        else:
            akad= AkadGadai.objects.exclude(status_transaksi__in=('1','2','4','5','6','7','8')).\
                filter(tanggal__range=(start_date,end_date)).filter(gerai__kode_cabang= id_cabang).filter(barang__jenis_barang= id_barang)
            a = sum([b.nilai for b in akad ])            
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
            
        
            worksheet.merge_range('A1:N1', 'LAPORAN DATA BARANG GUDANG AKTIF ', merge_format1)
            worksheet.merge_range('A2:N2', 'PERIODE '+ f + " s.d " + g, merge_format1)
            worksheet.merge_range('A4:A5', 'Norek ', merge_format)
            worksheet.merge_range('B4:B5', 'Gerai', merge_format)
            worksheet.merge_range('C4:C5', 'Nama', merge_format)
            worksheet.merge_range('D4:D5', 'Jenis Barang', merge_format)
            worksheet.merge_range('E4:E5', 'Barang', merge_format)
            worksheet.merge_range('F4:F5', 'Status Barang', merge_format)
            worksheet.merge_range('G4:G5', 'Tanggal Akad', merge_format)
            worksheet.merge_range('H4:H5', 'JW', merge_format)
            worksheet.merge_range('I4:I5', 'Jatuh Tempo', merge_format)
            worksheet.merge_range('J4:J5', 'Nilai', merge_format)
            worksheet.merge_range('K4:N4', 'Data Gudang', merge_format)
            worksheet.write_string('K5', 'Ruang')
            worksheet.write_string('L5', 'Lemari')
            worksheet.write_string('M5', 'Rak')
            worksheet.write_string('N5', 'Row')

            row = 6
            col = 0
            for t in akad:
                worksheet.write_string(row, col , t.norek() )
                worksheet.write_string(row, col + 1 , t.gerai.nama_cabang)
                worksheet.write_string(row, col + 2 , t.agnasabah.nama)
                worksheet.write_string(row, col + 3 , t.jenis_barang_all())
                worksheet.write_string(row, col + 4 , t.kode_barang_all())
                worksheet.write_string(row, col + 5, 'Aktif')
                worksheet.write_datetime(row, col + 6, t.tanggal, date_format)
                worksheet.write_string(row, col + 7, t.jangka_waktu)
                worksheet.write_datetime(row, col + 8, t.jatuhtempo, date_format)
                worksheet.write_number(row, col + 9, t.nilai, money_format)
                if t.ruang_barang == None:
                    worksheet.write_string(row, col + 10, '0')
                else:
                   worksheet.write_string(row, col + 10, t.ruang_barang)
                if t.lemari_barang == None:
                    worksheet.write_string(row, col + 11, '0')
                else:
                    worksheet.write_string(row, col + 11, t.lemari_barang)
                if t.rak_barang == None:
                    worksheet.write_string(row, col + 12, '0')
                else:
                    worksheet.write_string(row, col + 12, t.rak_barang)
                if t.row_barang == None:
                    worksheet.write_string(row, col + 13, '0')
                else:
                    worksheet.write_string(row, col + 13, t.row_barang)
                row += 1
            worksheet.write(row,3, 'Total', bold)    
            worksheet.write(row,9, a, money_format)         
       
            workbook.close()    
            output.seek(0)    
            response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename= barang_gudang_aktif.xlsx"
            return response
    else:
        template = 'gudang/barang/barang_gudang_aktif.html'
        variables = RequestContext(request, {'kp': kp ,'form':form})
        return render_to_response(template, variables)











