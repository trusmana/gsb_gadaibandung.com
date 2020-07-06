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
from gadai.appkeuangan.report.forms import SearchForm,FilterNewForm

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('staffops','administrator')))
def lapur_barang_new(request):###teddy27042015
    kp = []
    start_date = None
    end_date = None
    id_cabang = None
    report = None
    form = FilterNewForm()
    plns = []
    if 'start_date' in request.GET and request.GET['end_date']  and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        barang = request.GET['barang']
        kendaraan = request.GET['kendaraan']
        status_barang = request.GET['status_barang']
        report = request.GET['report']
        if id_cabang == '500' and report == '3' and barang =='0' and kendaraan =='0' and status_barang == '1':
            gabung_all = _get_gabung_all(start_date,end_date)
            return render(request, 'manop/laporan/lapur/laporan_lapur_new.html',{'form':form,'lapur': gabung_all ,
                'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,'total':sum([p.nilai for p in gabung_all]),
                'total_plafon':sum([p.nilai for p in gabung_all])})
        elif id_cabang == '500' and report == '3' and barang == barang and kendaraan =='0' and status_barang == '1':
            gabung_all = _get_gabung_all_barang(start_date,end_date,barang)
            return render(request,'manop/laporan/lapur/laporan_lapur_new.html', {'form':form,'lapur': gabung_all ,'start_date':start_date,
                'end_date':end_date,'id_cabang':id_cabang,'total':sum([p.nilai for p in gabung_all]),
                'total_plafon':sum([p.nilai for p in gabung_all])})
        elif id_cabang == '500' and report == '3' and barang == '0' and kendaraan == kendaraan and status_barang == '1':
            gabung_all = _get_gabung_all_kendaraan(start_date,end_date,kendaraan)
            return render(request,'manop/laporan/lapur/laporan_lapur_new.html', {'form':form,'lapur': gabung_all ,'start_date':start_date,
                'end_date':end_date,'id_cabang':id_cabang,'total':sum([p.nilai for p in gabung_all]),
                'total_plafon':sum([p.nilai for p in gabung_all])})
        elif id_cabang == id_cabang and barang =='0' and kendaraan =='0' and status_barang == '1' and report =='3':
            rekap = Lapur.objects.filter(status = '1',tanggal__range=(start_date,end_date),aglapur__gerai__kode_cabang =
                    id_cabang,aglapur__status_transaksi = '6')
            template = 'manop/laporan/lapur/laporan_lapur_new.html'
            variables = RequestContext(request, {'form':form,'lapur': rekap ,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,\
                'total':sum([p.nilai for p in rekap]),'total_plafon':sum([p.nilai for p in rekap])})
            return render_to_response(template, variables)
        elif id_cabang == '500' and report == '2':
            plns = []
            rekap = Lapur.objects.filter(status = '1').filter(tanggal__range=(start_date,end_date)).filter(aglapur__status_transaksi = '6')
            template = 'manop/laporan/lapur/laporan_lapur_pdf.html'
            variables = RequestContext(request, {'form':form,'lapur': rekap ,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,\
                'total':sum([p.aglapur.nilai for p in rekap]),'total_plafon':sum([p.nilai for p in rekap])})
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

        elif id_cabang == '500' and report == '1' and barang =='0' and kendaraan =='0' and status_barang == '1':
            akad = Lapur.objects.filter(status = '1',tanggal__range=(start_date,end_date),aglapur__status_transaksi = '6')
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

        elif id_cabang == '500' and report == '1' and barang ==barang and kendaraan =='0' and status_barang == '1':
            akad = Lapur.objects.filter(status = '1',tanggal__range=(start_date,end_date),aglapur__status_transaksi = '6',
                aglapur__barang__jenis_barang = barang)
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

        elif id_cabang == '500' and report == '1' and barang =='0' and kendaraan == kendaraan and status_barang == '1':
            akad = Lapur.objects.filter(status = '1',tanggal__range=(start_date,end_date),aglapur__status_transaksi = '6',
                aglapur__barang__jenis_kendaraan = kendaraan)
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


        elif id_cabang == id_cabang and report == '1' and barang =='0' and kendaraan =='0' and status_barang == '1':
            akad= Lapur.objects.filter(status = '1',tanggal__range=(start_date,end_date),aglapur__gerai__kode_cabang =
                    id_cabang,aglapur__status_transaksi = '6')
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
            rekap = Lapur.objects.filter(status = '1',tanggal__range=(start_date,end_date),aglapur__status_transaksi = '6',
                aglapur__gerai__kode_cabang = id_cabang)
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

        elif id_cabang == id_cabang and report == '1' and barang ==barang and kendaraan =='0' and status_barang == '1':
            akad = Lapur.objects.filter(status = '1',tanggal__range=(start_date,end_date),aglapur__status_transaksi = '6',
                aglapur__barang__jenis_barang = barang)
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

        elif id_cabang == id_cabang and report == '1' and barang =='0' and kendaraan == kendaraan and status_barang == '1':
            akad = Lapur.objects.filter(status = '1',tanggal__range=(start_date,end_date),aglapur__status_transaksi = '6',
                aglapur__barang__jenis_kendaraan = kendaraan)
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


    template='manop/laporan/lapur/laporan_lapur_new.html'
    variable = RequestContext(request,{'form':form})
    return render_to_response(template,variable)


def _get_gabung_all(start_date,end_date):
    rekap = Lapur.objects.filter(status = '1',tanggal__range=(start_date,end_date),aglapur__status_transaksi = '6')
    return rekap

def _get_gabung_all_barang(start_date,end_date,barang):
    rekap = Lapur.objects.filter(status = '1',tanggal__range=(start_date,end_date),aglapur__status_transaksi = '6',
        aglapur__barang__jenis_barang = barang)
    return rekap

def _get_gabung_all_kendaraan(start_date,end_date,kendaraan):
    rekap = Lapur.objects.filter(status = '1',tanggal__range=(start_date,end_date),aglapur__status_transaksi = '6',
        aglapur__barang__jenis_kendaraan = kendaraan)
    return rekap

