from django.contrib.auth.decorators import login_required, user_passes_test
from gadai.appgadai.models import Tbl_Cabang,Pelunasan,BarangLelang,Lapur,AkadGadai,HistoryLapur
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response,render
from gadai.xlsxwriter.workbook import Workbook
from gadai.appgadai.manop.forms import Filter_PencairanForm
import datetime


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in =('manop','baranglapur','admops','staffops','asmanpjb','admin')))
def total_harian_filter_new(request):
    awal_system = datetime.date(2000,1,1)
    rekap = Tbl_Cabang.objects.filter(status_aktif = 1)
    plns = []
    form = Filter_PencairanForm()
    if 'start_date' in request.GET and request.GET['start_date'] and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        for k in rekap:
            plns.append({'k':k,'aktif':k.aktif_nasabah_harian_filter(start_date,end_date),'kode_cabang':k.kode_cabang,
                'nama_cabang':k.nama_cabang,
                'nilai_cair': k.nilai_pencairan_harian_filter(start_date,end_date),
                'noa_cair':k.aktif_harian_filter(start_date, end_date)

                })
        return render(request,'manop/filter/total_harian_filter_new.html',{'plns': plns ,'start_date':start_date,'end_date':end_date})

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
            'bold':     True, 'border':   6,'align':    'center',
            'valign':   'vcenter','fg_color': '#D7E4BC', })

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
        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=rekap_pjb.xlsx"
        return response
    else:
        template='manop/filter/total_harian_filter_new.html'
        variable = RequestContext(request,{'form':form})
        return render_to_response(template,variable)

