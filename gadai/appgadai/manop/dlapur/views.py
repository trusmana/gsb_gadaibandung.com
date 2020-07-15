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
from gadai.appgadai.akadgadai.forms import Peminjaman,Lapur
from gadai.appgadai.manop.forms import *
from django.shortcuts import render_to_response, get_object_or_404,render,redirect
from gadai.appkeuangan.report.forms import SearchForm,FilterNewForm
from gadai.appkeuangan.models import Menu
from gadai.appgadai.manop.dlapur.forms import DataLapurnaForm

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('staffops','administrator','MANOP')))
def sh_kondisi_lapur(request):
    da= Kondisi_Lapur.objects.filter(tanggal__isnull = False)
    list = []
    for a in da:
        list.append({'name':a.klapur,'id':a.klapur.id,'tanggal':a.tanggal,'ket':a.keterangan,'user':a.cu})
    return render(request,'manop/laporan/lapur/kondisi_data_lapur.html',{'data':list})


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('staffops','administrator','MANOP')))
def show_data_ref(request,pk):
    data= Lapur.objects.get(id=pk)
    return render(request,'manop/laporan/lapur/show_sts_lapur.html',{'data':data})

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('staffops','administrator','MANOP')))
def sts_lpr(request,pk):
    user = request.user
    nsb = get_object_or_404(Lapur, id=pk)
    if request.method == "POST":
        form = DataLapurnaForm(request.POST,nsb)
        if form.is_valid():
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

            layar_tv = form.cleaned_data['layar_tv']
            kondisi_layar_tv = form.cleaned_data['kondisi_layar_tv']
            remote = form.cleaned_data['remote']
            kondisi_remote = form.cleaned_data['kondisi_remote']

            harddisk  = form.cleaned_data['harddisk']
            kondisi_harddisk = form.cleaned_data['kondisi_harddisk']
            stick  = form.cleaned_data['stick']
            kondisi_stick = form.cleaned_data['kondisi_stick']
            hdmi  = form.cleaned_data['hdmi']
            kondisi_hdmi = form.cleaned_data['kondisi_hdmi']
            keterangan = form.cleaned_data['keterangan']
            simpan = Kondisi_Lapur(klapur= nsb,cu = user,mu =user,tanggal= datetime.date.today(),charger=charger,
                kondisi_charger=kondisi_charger,batre=batre,kondisi_batre=kondisi_batre, keybord=keybord,cassing= cassing,
                kondisi_cassing= kondisi_cassing,layar=layar,kondisi_layar=kondisi_layar,lensa=lensa
                ,kondisi_lensa=kondisi_lensa,batre_kamera=batre_kamera,kondisi_batre_kamera=kondisi_batre_kamera,cassing_kamera=cassing_kamera,
                kondisi_cassing_kamera= kondisi_cassing_kamera,layar_tv=layar_tv,kondisi_layar_tv=kondisi_layar_tv,remote=remote,
                kondisi_remote=kondisi_remote,harddisk=harddisk,kondisi_harddisk= kondisi_harddisk,stick=stick,
                kondisi_stick=kondisi_stick,hdmi =hdmi,kondisi_hdmi=kondisi_hdmi,keterangan=keterangan)
            simpan.save()
            messages.add_message(request, messages.INFO, 'Data Sudah Tersimpan.')
            return HttpResponseRedirect('/manop/dlapur/sh_kondisi_lapur/' )
    else:
        form = DataLapurnaForm()
    return render(request,'manop/laporan/lapur/input_sts_lapur.html',{'nsb':nsb,'form':form})

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('staffops','administrator','MANOP')))
def barang_pinjam(request):
    pnj = Peminjaman.objects.filter(status='1')
    user = request.user
    sekarang = datetime.date.today()
    cek_menu = user.menuitem_set.all().count()
    cek_group = user.groups.all()
    menu = Menu.objects.filter(akses_grup__in=(cek_group)).filter(status_aktif = True)
    return render(request,'manop/laporan/lapur/laporan_barang_pinjam.html',{'pnj':pnj,'menu':menu,'cek_menu':cek_menu})

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('staffops','administrator','MANOP')))
def lapur_barang_new(request):
    user = request.user
    sekarang = datetime.date.today()
    cek_menu = user.menuitem_set.all().count()
    cek_group = user.groups.all()
    menu = Menu.objects.filter(akses_grup__in=(cek_group)).filter(status_aktif = True)
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
                'total_plafon':sum([p.nilai for p in gabung_all]),'cek_menu': cek_menu, 'menu':menu})
        elif id_cabang == '500' and report == '3' and barang == barang and kendaraan =='0' and status_barang == '1':
            gabung_all = _get_gabung_all_barang(start_date,end_date,barang)
            return render(request,'manop/laporan/lapur/laporan_lapur_new.html', {'form':form,'lapur': gabung_all ,'start_date':start_date,
                'end_date':end_date,'id_cabang':id_cabang,'total':sum([p.nilai for p in gabung_all]),
                'total_plafon':sum([p.nilai for p in gabung_all]),'cek_menu': cek_menu, 'menu':menu})
        elif id_cabang == '500' and report == '3' and barang == '0' and kendaraan == kendaraan and status_barang == '1':
            gabung_all = _get_gabung_all_kendaraan(start_date,end_date,kendaraan)
            return render(request,'manop/laporan/lapur/laporan_lapur_new.html', {'form':form,'lapur': gabung_all ,'start_date':start_date,
                'end_date':end_date,'id_cabang':id_cabang,'total':sum([p.nilai for p in gabung_all]),
                'total_plafon':sum([p.nilai for p in gabung_all]),'cek_menu': cek_menu, 'menu':menu})
        elif id_cabang == id_cabang and barang =='0' and kendaraan =='0' and status_barang == '1' and report =='3':
            rekap = Lapur.objects.filter(status = '1',tanggal__range=(start_date,end_date),aglapur__gerai__kode_cabang =
                    id_cabang,aglapur__status_transaksi = '6')
            template = 'manop/laporan/lapur/laporan_lapur_new.html'
            variables = RequestContext(request, {'form':form,'lapur': rekap ,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,\
                'total':sum([p.nilai for p in rekap]),'total_plafon':sum([p.nilai for p in rekap]),'cek_menu': cek_menu, 'menu':menu})
            return render_to_response(template, variables)
        elif id_cabang == '500' and report == '2':
            plns = []
            rekap = Lapur.objects.filter(status = '1').filter(tanggal__range=(start_date,end_date)).filter(aglapur__status_transaksi = '6')
            template = 'manop/laporan/lapur/laporan_lapur_pdf.html'
            variables = RequestContext(request, {'form':form,'lapur': rekap ,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,\
                'total':sum([p.aglapur.nilai for p in rekap]),'total_plafon':sum([p.nilai for p in rekap]),'cek_menu':
                cek_menu, 'menu':menu})
            return render_to_response(template, variables)
        elif id_cabang == id_cabang and report =='2':
            rekap = Lapur.objects.filter(status = '1').filter(tanggal__range=(start_date,end_date)).filter(aglapur__gerai__kode_cabang = id_cabang)
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            template = 'manop/laporan/lapur/laporan_lapur_pdf.html'
            variables = RequestContext(request, {'form':form,'lapur': rekap ,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,\
                'total':sum([p.aglapur.nilai for p in rekap]),'total_plafon':sum([p.nilai for p in rekap]),'cek_menu': cek_menu, 'menu':menu})
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
    variable = RequestContext(request,{'form':form,'cek_menu': cek_menu, 'menu':menu})
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

