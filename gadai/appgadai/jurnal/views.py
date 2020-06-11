from django.shortcuts import render_to_response, get_object_or_404,render
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect,HttpResponse
import xlwt
import io
import xlsxwriter
from datetime import datetime
from gadai.xlsxwriter.workbook import Workbook
import datetime
from gadai.appgadai.jurnal.forms import *
from gadai.appgadai.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

def jurnal_koreksi(request,object_id,user,form_class):
    user = request.user
    sekarang = datetime.date.today()
    Tbl_Transaksi_KoreksiFormset = get_ordereditem_formset(form_class, extra=1, can_delete=True)
    ju = Jurnal.objects.all()
    show = Tbl_Transaksi.objects.filter(status_jurnal=1,jurnal__cu__id = user.id).filter(tgl_trans= sekarang).\
        filter(jenis=('GL_GL_JUNAL_KOREKSI'))
    order = Tbl_Transaksi.objects.all()
    if request.method == 'POST':
        form = MainJurnalKoreksiForm(request.POST)
        formset = Tbl_Transaksi_KoreksiFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            tgl_trans = form.cleaned_data['tgl_trans']
            #j_status = form.cleaned_data['j_status']
            jurnal = Jurnal.objects.create(tgl_trans=tgl_trans,diskripsi='GL_GL_JUNAL_KOREKSI',kode_cabang=user.profile.gerai.kode_cabang,cu=user,mu=user)
            #jurnal_asli = Jurnal.objects.create(tgl_trans=tgl_trans,diskripsi='GL_GL_PUSAT_BANK',cu=user,mu=user,kode_cabang=user.profile.gerai.kode_cabang)
            for itemform in formset.forms:
                koderekening = itemform.cleaned_data['koderekening']
                kdd = koderekening[:8]
                if koderekening:
                    rekening = Tbl_Akun.objects.get(coa=kdd)
                    if not rekening:
                        message_set.create( messages.add_message(request, messages.INFO,"Kode Rekening Tidak Ditemukan"))
                        return HttpResponseRedirect('/jurnal/%s/%s/jurnal_koreksi/'% (object_id,user.id))
                    debet = itemform.cleaned_data['debet']
                    kredit = itemform.cleaned_data['kredit']
                    deskripsi = itemform.cleaned_data['deskripsi']
                    id_cabang = itemform.cleaned_data['id_cabang']
                    debet = debet
                    kredit = kredit
                itemjurnal = Tbl_Transaksi.objects.create(id_coa= rekening,debet=debet,kredit=kredit,\
                    tgl_trans=tgl_trans,no_trans =jurnal.no_akad,jurnal = jurnal,id_product=4,status_jurnal=1,\
                    id_cabang=id_cabang,id_unit=300,jenis='GL_GL_JUNAL_KOREKSI',deskripsi=deskripsi)
            messages.add_message(request, messages.INFO,"Jurnal Koreksi telah disimpan dengan sukses")

            return HttpResponseRedirect('/jurnal/%s/%s/jurnal_koreksi/'% (object_id,user.id))
        else:
            message_set.create(messages.add_message(request, messages.INFO,"Form Tidak Valid"))
        var = {'form': form, 'formset': formset,'show':show,'cabang':object_id}
    else:
        var = {'form': MainJurnalKoreksiForm(), 'formset': Tbl_Transaksi_KoreksiFormset(),'show':show,'cabang':object_id}
    variables = RequestContext(request, var)
    return render_to_response('jurnal/add_baru_koreksi.html', variables)

def jurnal_post_koreksi(request):
    user = request.user
    for i in request.POST.getlist('id_pilih'):        
        gl = Jurnal.objects.get(id=(i))
        jurnal = gl.tbl_transaksi_set.filter(tgl_trans= datetime.date.today()) 
        for mutasi in jurnal:
            mutasi.status_jurnal = 2
            mutasi.save() 
            gl.kode_cabang = mutasi.id_cabang
            gl.save()
    return HttpResponseRedirect("/jurnal/%s/%s/jurnal_koreksi/" % (user.profile.gerai.kode_cabang,user.id))

def hapus_jurnal_koreksi(request,object_id):
    us = request.user 
    tbl = Jurnal.objects.get(id=object_id)   
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Penghapusan Jurnal Berhasil')
    return HttpResponseRedirect('/jurnal/%s/%s/jurnal_koreksi/'% (us.profile.gerai.kode_cabang,us.id))


@login_required
def laporan_kas_uang_muka(request):
    ledger = Tbl_Transaksi.objects.all()
    user = request.user
    rekap = []
    saldo_awal = []
    start_date = None
    end_date = None
    id_cabang = 300
    akumulasi_debet = 0
    akumulasi_kredit = 0
    form = SearchForm()
    all = []
    sld = sum([a.saldo for a in Tbl_Transaksi.objects.filter(jurnal__kode_cabang = id_cabang).filter(tgl_trans=start_date).\
        filter(jenis = ('SALDOKASGERAI'))])
    
    if 'start_date' in request.GET and request.GET['end_date']  and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        akumulasi_debet = 0
        akumulasi_kredit = 0
        saldo_awal = Tbl_TransaksiKeu.objects.filter(tgl_trans=start_date).filter(id_coa__coa = '13.06.03').\
            filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI')
        tb = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(id_coa__coa = '13.06.03').\
            filter(id_cabang = 300).exclude(jenis = 'SALDOKASGERAI').filter(status_jurnal = 2)
        tes = Tbl_TransaksiKeu.objects.filter(tgl_trans=start_date).filter(status_jurnal = 2).filter(id_coa__coa = '13.06.03').\
            filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI').count()
        for t in tb: 
            akumulasi_debet += t.debet
            akumulasi_kredit += t.kredit 
            all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'cu':t.jurnal.cu,
                'saldo_akhir_mutasi':  (t.id_coa.saldo_uang_muka_pusat(start_date) + akumulasi_debet - akumulasi_kredit)  ,\
                'deskripsi': t.deskripsi,'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,\
                'coa':t.id_coa.coa,'nobukti': t.jurnal.no_akad,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa,\
                'saldo_pjb':t.id_coa.saldo_kas(start_date)})
        if tes >= 1:
            template='report_baru/ledger/search/laporan_kas_uang_muka.html'
            variable = RequestContext(request,{'ledger':all,'saldo_awal':sum([p.saldo for p in saldo_awal]),'cu':user,\
                'total_debet':akumulasi_debet,'total_kredit':akumulasi_kredit,\
                'saldo_akhir':sum([p.saldo for p in saldo_awal]) + akumulasi_debet - akumulasi_kredit,'form':form,\
                'start_date':start_date,'id_cabang':id_cabang,'end_date':end_date,\
                'saldo_petty_cash':(sum([p.saldo for p in saldo_awal]) + akumulasi_debet) - akumulasi_kredit,
                'nilai_ditambahkan':((sum([p.saldo for p in saldo_awal]) + akumulasi_debet) - akumulasi_kredit)})
            return render_to_response(template,variable)
        else:
            sl = 0
            try:
                dd = Tbl_TransaksiKeu.objects.filter(tgl_trans__lt=start_date).filter(id_coa__coa = '13.06.03').\
                    filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI').latest('id')
                sl = dd.saldo
            except Tbl_TransaksiKeu.DoesNotExist:
                sl = 0
            template= 'report_baru/ledger/search/laporan_kas_uang_muka.html'
            variable = RequestContext(request,{'ledger':all,'saldo_awal':sl,'cu':user,'total_debet':akumulasi_debet,\
                'total_kredit':akumulasi_kredit,'total_debet':sum ([a.debet for a in tb]),'total_kredit':sum ([a.kredit for a in tb]),\
                'saldo_akhir':sl + akumulasi_debet - akumulasi_kredit,'form':form,'start_date':start_date,\
                'id_cabang':id_cabang,'end_date':end_date,\
                'saldo_petty_cash':(sum([p.saldo for p in saldo_awal]) + akumulasi_debet) - akumulasi_kredit,
                'nilai_ditambahkan':((sum([p.saldo for p in saldo_awal]) + akumulasi_debet) - akumulasi_kredit)})
            return render_to_response(template,variable)


    if 'start_date' in request.GET and request.GET['end_date']  and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        akumulasi_debet = 0
        akumulasi_kredit = 0
        saldo_awal = Tbl_TransaksiKeu.objects.filter(tgl_trans=start_date).filter(id_coa__coa = '13.06.03').\
            filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI').filter(status_jurnal = 2)
        tb = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(status_jurnal = 2).filter(id_coa__coa = '13.06.03').\
            filter(id_cabang = 300).exclude(jenis = 'SALDOKASGERAI')
        tes = Tbl_TransaksiKeu.objects.filter(tgl_trans=start_date).filter(id_coa__coa = '13.06.03').\
            filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI').count()
        for t in tb:
            akumulasi_debet += t.debet
            akumulasi_kredit += t.kredit
            all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'cu':t.jurnal.cu,
                'saldo_akhir_mutasi':  (t.id_coa.saldo_kas_pusat_besar(start_date) + akumulasi_debet - akumulasi_kredit)  ,\
                'deskripsi': t.deskripsi,'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,\
                'coa':t.id_coa.coa,'nobukti': t.jurnal.no_akad,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa,\
                'saldo_pjb':t.id_coa.saldo_kas(start_date)})
        if tes >= 1:
            template= 'report_baru/ledger/search/cetak_laporan_kas_uang_muka.html'
            variable = RequestContext(request,{'ledger':all,'saldo_awal':sum([p.saldo for p in saldo_awal]),'cu':user,\
                'total_debet':akumulasi_debet,'total_kredit':akumulasi_kredit,\
                'saldo_akhir':sum([p.saldo for p in saldo_awal]) + akumulasi_debet - akumulasi_kredit,'form':form,\
                'start_date':start_date,'id_cabang':id_cabang,'end_date':end_date,\
                'saldo_petty_cash':(sum([p.saldo for p in saldo_awal]) + akumulasi_debet) - akumulasi_kredit,
                'nilai_ditambahkan':((sum([p.saldo for p in saldo_awal]) + akumulasi_debet) - akumulasi_kredit)})
            return render_to_response(template,variable)
        else:
            sl = 0
            try:
                dd = Tbl_TransaksiKeu.objects.filter(tgl_trans__lt=start_date).filter(id_coa__coa = '13.06.03').\
                    filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI').latest('id')
                sl = dd.saldo
            except Tbl_TransaksiKeu.DoesNotExist:
                sl = 0
            template= 'report_baru/ledger/search/cetak_laporan_kas_uang_muka.html'
            variable = RequestContext(request,{'ledger':all,'saldo_awal':sl,'cu':user,'total_debet':akumulasi_debet,\
                'total_kredit':akumulasi_kredit,'total_debet':sum ([a.debet for a in tb]),'total_kredit':sum ([a.kredit for a in tb]),\
                'saldo_akhir':sl + akumulasi_debet - akumulasi_kredit,'form':form,'start_date':start_date,\
                'id_cabang':id_cabang,'end_date':end_date,\
                'saldo_petty_cash':(sum([p.saldo for p in saldo_awal]) + akumulasi_debet) - akumulasi_kredit,
                'nilai_ditambahkan':((sum([p.saldo for p in saldo_awal]) + akumulasi_debet) - akumulasi_kredit)})
            return render_to_response(template,variable)

    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        akumulasi_debet = 0
        akumulasi_kredit = 0
        s_awal = Tbl_TransaksiKeu.objects.filter(tgl_trans=start_date).filter(id_coa__coa = '13.06.03').filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI')
        saldo_awal_lates = Tbl_TransaksiKeu.objects.filter(tgl_trans__lt=start_date).filter(id_coa__coa = '13.06.03').filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI').order_by('-id')
        aa =saldo_awal_lates[0]
        saldo_terakhir = aa.saldo
        saldo_awal =sum([p.saldo for p in s_awal])


        total_saldo_br = (saldo_awal + akumulasi_debet) - akumulasi_kredit
        total_saldo_sbl = (saldo_terakhir + akumulasi_debet) - akumulasi_kredit

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

        worksheet.merge_range('A1:F1', 'LAPORAN KAS KECIL PUSAT PJB', merge_format)
        worksheet.merge_range('A2:F2', 'Periode :' +' '+ start_date + ' ' + 'S/D' + ' ' +start_date, merge_format)
        worksheet.merge_range('A3:F3', 'AKUN :11.05.01', merge_format)

        worksheet.write('A5:A6', 'Tanggal', bold)
        worksheet.write('B5:B6', 'Keterangan', bold)
        worksheet.write('C5:C6', 'User', bold)
        worksheet.write('D5:D6', 'Debet (Rp.)', bold)
        worksheet.write('E5:E6', 'Kredit (Rp.)', bold)
        worksheet.write('F5:F6', 'SALDO (Rp.)', bold)
        worksheet.write('B6', 'Saldo Awal', bold)
        if saldo_awal != 0:
            worksheet.write('F6', saldo_awal, money_format)
        else:
            worksheet.write('F6', saldo_terakhir, money_format)
        row = 1
        col = 0

        tb = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(status_jurnal = 2).filter(id_coa__coa = '13.06.03').filter(id_cabang = 300).exclude(jenis = 'SALDOKASGERAI')
        tes = Tbl_TransaksiKeu.objects.filter(tgl_trans=start_date).filter(id_coa__coa = '13.06.03').filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI').count()
        
        for t in tb:
            akumulasi_debet += t.debet
            akumulasi_kredit += t.kredit
            saldo_akhir_mutasi = t.id_coa.saldo_kas_pusat_besar(start_date) + akumulasi_debet - akumulasi_kredit
            saldo_akhir_mutasi_akhir = saldo_terakhir + akumulasi_debet - akumulasi_kredit
            
            print t.id_coa.saldo_kas_pusat_besar(start_date)
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            total_debet = akumulasi_debet
            total_kredit = akumulasi_kredit

            worksheet.write_datetime(row +5, col , t.tgl_trans, date_format)
            worksheet.write_string(row +5, col + 1 , (t.deskripsi + '-' + t.deskripsi))
            worksheet.write_string(row +5, col + 2 , 'hh')
            worksheet.write_number(row +5, col + 3,t.debet, money_format)
            worksheet.write_number(row +5, col + 4,t.kredit, money_format)
            if saldo_awal != 0:
                worksheet.write_number(row +5, col + 5,saldo_akhir_mutasi, money_format)
            else:
                worksheet.write_number(row +5, col + 5,saldo_akhir_mutasi_akhir, money_format)
            row += 1
        worksheet.write(row +5,1, 'Total', bold)    
        worksheet.write(row +5,3, akumulasi_debet, money_format)
        worksheet.write(row +5,4, akumulasi_kredit, money_format)
        worksheet.write(row +6,1, 'Saldo Akhir Petty Cash Hari ini', bold)    
        worksheet.write(row +6,5, total_saldo_br, money_format)
        worksheet.write(row +7,1, 'Total Yang Harus Ditambahkan', bold)    
        worksheet.write(row +7,5, saldo_akhir_mutasi, money_format)
        worksheet.write(row +8,1, 'Total Dana Petty Cash (Impress Fund)', bold)    
        #worksheet.write(row +8,5, saldo_limit, money_format)


        workbook.close()    
        output.seek(0)    
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=Laporan_Pelunasan_gabungan.xlsx"
        return response

    else:
        variables = RequestContext(request, {'form': form,'ag':ledger})
        return render_to_response('report_baru/ledger/search/laporan_kas_uang_muka.html', variables)

@login_required
def laporan_kas_kecil(request):
    ledger = Tbl_Transaksi.objects.all()
    limit = Limit_PetyCash.objects.filter(status = 1)
    saldo_limit = sum([a.nilai for a in limit])
   
    user = request.user
    rekap = []
    saldo_awal = []
    start_date = None
    end_date = None
    id_cabang = 300
    akumulasi_debet = 0
    akumulasi_kredit = 0
    form = SearchForm()
    all = []
    sld = sum([a.saldo for a in Tbl_Transaksi.objects.filter(jurnal__kode_cabang = id_cabang).filter(tgl_trans=start_date).\
        filter(jenis = ('SALDOKASGERAI'))])
    
    if 'start_date' in request.GET and request.GET['end_date']  and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        akumulasi_debet = 0
        akumulasi_kredit = 0
        saldo_awal = Tbl_TransaksiKeu.objects.filter(tgl_trans=start_date).filter(id_coa__coa = '11.01.05').\
            filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI')
        tb = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(id_coa__coa = '11.01.05').\
            filter(id_cabang = 300).exclude(jenis = 'SALDOKASGERAI').filter(status_jurnal = 2)
        tes = Tbl_TransaksiKeu.objects.filter(tgl_trans=start_date).filter(status_jurnal = 2).filter(id_coa__coa = '11.01.05').\
            filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI').count()
        for t in tb: 
            akumulasi_debet += t.debet
            akumulasi_kredit += t.kredit 
            all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'cu':t.jurnal.cu,
                'saldo_akhir_mutasi':  (t.id_coa.saldo_kas_pusat_besar(start_date) + akumulasi_debet - akumulasi_kredit)  ,\
                'deskripsi': t.deskripsi,'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,\
                'coa':t.id_coa.coa,'nobukti': t.jurnal.no_akad,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa,\
                'saldo_pjb':t.id_coa.saldo_kas(start_date)})
        if tes >= 1:
            template='report_baru/ledger/search/laporan_kas_kecil.html'
            variable = RequestContext(request,{'ledger':all,'saldo_awal':sum([p.saldo for p in saldo_awal]),'cu':user,\
                'saldo_limit':saldo_limit,'total_debet':akumulasi_debet,'total_kredit':akumulasi_kredit,\
                'saldo_akhir':sum([p.saldo for p in saldo_awal]) + akumulasi_debet - akumulasi_kredit,'form':form,\
                'start_date':start_date,'id_cabang':id_cabang,'end_date':end_date,\
                'saldo_petty_cash':(sum([p.saldo for p in saldo_awal]) + akumulasi_debet) - akumulasi_kredit,
                'nilai_ditambahkan':saldo_limit -((sum([p.saldo for p in saldo_awal]) + akumulasi_debet) - akumulasi_kredit)})
            return render_to_response(template,variable)
        else:
            sl = 0
            try:
                dd = Tbl_TransaksiKeu.objects.filter(tgl_trans__lt=start_date).filter(id_coa__coa = '11.01.05').\
                    filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI').latest('id')
                sl = dd.saldo
            except Tbl_TransaksiKeu.DoesNotExist:
                sl = 0
            template='report_baru/ledger/search/laporan_kas_kecil.html'
            variable = RequestContext(request,{'ledger':all,'saldo_awal':sl,'cu':user,'total_debet':akumulasi_debet,\
                'total_kredit':akumulasi_kredit,'total_debet':sum ([a.debet for a in tb]),'total_kredit':sum ([a.kredit for a in tb]),\
                'saldo_limit':saldo_limit,'saldo_akhir':sl + akumulasi_debet - akumulasi_kredit,'form':form,'start_date':start_date,\
                'id_cabang':id_cabang,'end_date':end_date,\
                'saldo_petty_cash':(sum([p.saldo for p in saldo_awal]) + akumulasi_debet) - akumulasi_kredit,
                'nilai_ditambahkan':saldo_limit -((sum([p.saldo for p in saldo_awal]) + akumulasi_debet) - akumulasi_kredit)})
            return render_to_response(template,variable)


    if 'start_date' in request.GET and request.GET['end_date']  and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        akumulasi_debet = 0
        akumulasi_kredit = 0
        saldo_awal = Tbl_TransaksiKeu.objects.filter(tgl_trans=start_date).filter(id_coa__coa = '11.01.05').\
            filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI').filter(status_jurnal = 2)
        tb = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(status_jurnal = 2).filter(id_coa__coa = '11.01.05').\
            filter(id_cabang = 300).exclude(jenis = 'SALDOKASGERAI')
        tes = Tbl_TransaksiKeu.objects.filter(tgl_trans=start_date).filter(id_coa__coa = '11.01.05').\
            filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI').count()
        for t in tb:
            akumulasi_debet += t.debet
            akumulasi_kredit += t.kredit
            all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'cu':t.jurnal.cu,
                'saldo_akhir_mutasi':  (t.id_coa.saldo_kas_pusat_besar(start_date) + akumulasi_debet - akumulasi_kredit)  ,\
                'deskripsi': t.deskripsi,'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,\
                'coa':t.id_coa.coa,'nobukti': t.jurnal.no_akad,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa,\
                'saldo_pjb':t.id_coa.saldo_kas(start_date)})
        if tes >= 1:
            template='report_baru/ledger/search/cetak_laporan_kas_kecil.html'
            variable = RequestContext(request,{'ledger':all,'saldo_awal':sum([p.saldo for p in saldo_awal]),'cu':user,\
                'saldo_limit':saldo_limit,'total_debet':akumulasi_debet,'total_kredit':akumulasi_kredit,\
                'saldo_akhir':sum([p.saldo for p in saldo_awal]) + akumulasi_debet - akumulasi_kredit,'form':form,\
                'start_date':start_date,'id_cabang':id_cabang,'end_date':end_date,\
                'saldo_petty_cash':(sum([p.saldo for p in saldo_awal]) + akumulasi_debet) - akumulasi_kredit,
                'nilai_ditambahkan':saldo_limit -((sum([p.saldo for p in saldo_awal]) + akumulasi_debet) - akumulasi_kredit)})
            return render_to_response(template,variable)
        else:
            sl = 0
            try:
                dd = Tbl_TransaksiKeu.objects.filter(tgl_trans__lt=start_date).filter(id_coa__coa = '11.01.05').\
                    filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI').latest('id')
                sl = dd.saldo
            except Tbl_TransaksiKeu.DoesNotExist:
                sl = 0
            template='report_baru/ledger/search/cetak_laporan_kas_kecil.html'
            variable = RequestContext(request,{'ledger':all,'saldo_awal':sl,'cu':user,'total_debet':akumulasi_debet,\
                'total_kredit':akumulasi_kredit,'total_debet':sum ([a.debet for a in tb]),'total_kredit':sum ([a.kredit for a in tb]),\
                'saldo_limit':saldo_limit,'saldo_akhir':sl + akumulasi_debet - akumulasi_kredit,'form':form,'start_date':start_date,\
                'id_cabang':id_cabang,'end_date':end_date,\
                'saldo_petty_cash':(sum([p.saldo for p in saldo_awal]) + akumulasi_debet) - akumulasi_kredit,
                'nilai_ditambahkan':saldo_limit -((sum([p.saldo for p in saldo_awal]) + akumulasi_debet) - akumulasi_kredit)})
            return render_to_response(template,variable)

    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        akumulasi_debet = 0
        akumulasi_kredit = 0
        s_awal = Tbl_TransaksiKeu.objects.filter(tgl_trans=start_date).filter(id_coa__coa = '11.01.05').filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI')
        saldo_awal_lates = Tbl_TransaksiKeu.objects.filter(tgl_trans__lt=start_date).filter(id_coa__coa = '11.01.05').filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI').order_by('-id')
        aa =saldo_awal_lates[0]
        saldo_terakhir = aa.saldo
        saldo_awal =sum([p.saldo for p in s_awal])


        total_saldo_br = (saldo_awal + akumulasi_debet) - akumulasi_kredit
        total_saldo_sbl = (saldo_terakhir + akumulasi_debet) - akumulasi_kredit

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

        worksheet.merge_range('A1:F1', 'LAPORAN KAS KECIL PUSAT PJB', merge_format)
        worksheet.merge_range('A2:F2', 'Periode :' +' '+ start_date + ' ' + 'S/D' + ' ' +start_date, merge_format)
        worksheet.merge_range('A3:F3', 'AKUN :11.05.01', merge_format)

        worksheet.write('A5:A6', 'Tanggal', bold)
        worksheet.write('B5:B6', 'Keterangan', bold)
        worksheet.write('C5:C6', 'User', bold)
        worksheet.write('D5:D6', 'Debet (Rp.)', bold)
        worksheet.write('E5:E6', 'Kredit (Rp.)', bold)
        worksheet.write('F5:F6', 'SALDO (Rp.)', bold)
        worksheet.write('B6', 'Saldo Awal', bold)
        if saldo_awal != 0:
            worksheet.write('F6', saldo_awal, money_format)
        else:
            worksheet.write('F6', saldo_terakhir, money_format)
        row = 1
        col = 0

        tb = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(status_jurnal = 2).filter(id_coa__coa = '11.01.05').filter(id_cabang = 300).exclude(jenis = 'SALDOKASGERAI')
        tes = Tbl_TransaksiKeu.objects.filter(tgl_trans=start_date).filter(id_coa__coa = '11.01.05').filter(id_cabang = 300).filter(jenis = 'SALDOKASGERAI').count()
        
        for t in tb:
            akumulasi_debet += t.debet
            akumulasi_kredit += t.kredit
            saldo_akhir_mutasi = t.id_coa.saldo_kas_pusat_besar(start_date) + akumulasi_debet - akumulasi_kredit
            saldo_akhir_mutasi_akhir = saldo_terakhir + akumulasi_debet - akumulasi_kredit
            
            print t.id_coa.saldo_kas_pusat_besar(start_date)
            start_date = start_date
            end_date = end_date
            id_cabang = id_cabang
            total_debet = akumulasi_debet
            total_kredit = akumulasi_kredit

            worksheet.write_datetime(row +5, col , t.tgl_trans, date_format)
            worksheet.write_string(row +5, col + 1 , (t.deskripsi + '-' + t.deskripsi))
            worksheet.write_string(row +5, col + 2 , 'hh')
            worksheet.write_number(row +5, col + 3,t.debet, money_format)
            worksheet.write_number(row +5, col + 4,t.kredit, money_format)
            if saldo_awal != 0:
                worksheet.write_number(row +5, col + 5,saldo_akhir_mutasi, money_format)
            else:
                worksheet.write_number(row +5, col + 5,saldo_akhir_mutasi_akhir, money_format)
            row += 1
        worksheet.write(row +5,1, 'Total', bold)    
        worksheet.write(row +5,3, akumulasi_debet, money_format)
        worksheet.write(row +5,4, akumulasi_kredit, money_format)
        worksheet.write(row +6,1, 'Saldo Akhir Petty Cash Hari ini', bold)    
        worksheet.write(row +6,5, total_saldo_br, money_format)
        worksheet.write(row +7,1, 'Total Yang Harus Ditambahkan', bold)    
        worksheet.write(row +7,5, saldo_akhir_mutasi, money_format)
        worksheet.write(row +8,1, 'Total Dana Petty Cash (Impress Fund)', bold)    
        worksheet.write(row +8,5, saldo_limit, money_format)


        workbook.close()    
        output.seek(0)    
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=Laporan_Pelunasan_gabungan.xlsx"
        return response

    else:
        variables = RequestContext(request, {'form': form,'ag':ledger})
        return render_to_response('report_baru/ledger/search/laporan_kas_kecil.html', variables)

## MASTER TIKET GABUNGAN ADM
@login_required
@user_passes_test(lambda u: u.groups.filter(name='ADM_GERAI'))
def mastertiket_gabungan(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    cabang = Tbl_Cabang.objects.get(kode_cabang=cab)
    sekarang = datetime.date.today()
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=cab).filter(status_jurnal= 2).filter(jenis__in=(u'Pencairan',\
        u'Pencairan_barang_sama',u'Pelunasan_Barang_sama',u'Pelunasan_Barang_sama_nilai_lebih',u'Pelunasan_Barang_sama',\
        u'Pelunasan_Barang_sama_nilai_lebih',u'Penjualan_lelang_adm','PENJUALAN_AYDA_CABANG',
        u'Pelunasan_adm',u'Pelunasan_adm_diskon','Pelunasan_kasir_rak1','Pelunasan_kasir_bank_rak1',
        u'Pelunasan_Barang_sama',u'Pelunasan_Barang_sama_nilai_lebih',
        'PENJUALAN_AYDA_CABANG'
        ))
    template = 'ledger/mastertiket_gabungan.html'
    variables = RequestContext(request, {'cabang':cabang,'g': gr,'total_debet': sum([p.debet for p in gr]),'total_kredit': sum([p.kredit for p in gr])})
    return render_to_response(template, variables)
## AKHIR MASTER TIKET GABUNGAN ADM

def gl_gl_pusat(request,object_id,user,form_class):
    user = request.user
    sekarang = datetime.date.today()
    Tbl_Transaksi_History_glFormset = get_ordereditem_formset(form_class, extra=1, can_delete=True)
    ju = Jurnal_History.objects.all()
    show = Tbl_Transaksi.objects.filter(status_jurnal=1,jurnal__cu__id = user.id).filter(id_cabang=object_id).filter(tgl_trans= sekarang).\
        filter(jenis=('GL_GL_PUSAT')).filter(jurnal__diskripsi ='GL_GL_PUSAT_BANK')
    order = Tbl_Transaksi_History.objects.all()
    if request.method == 'POST':
        form = MainJurnalglForm(request.POST)
        formset = Tbl_Transaksi_History_glFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            tgl_trans = form.cleaned_data['tgl_trans']
            jurnal = Jurnal_History.objects.create(tgl_trans=tgl_trans,diskripsi='GL_GL_PUSAT',kode_cabang=user.profile.gerai.kode_cabang)
            jurnal_asli = Jurnal.objects.create(tgl_trans=tgl_trans,diskripsi='GL_GL_PUSAT_BANK',cu=user,mu=user,kode_cabang=user.profile.gerai.kode_cabang)
            for itemform in formset.forms:
                koderekening = itemform.cleaned_data['koderekening']
                kdd = koderekening[:8]
                if koderekening:
                    rekening = Tbl_Akun.objects.get(coa=kdd)                    
                    if not rekening:
                        message_set.create( messages.add_message(request, messages.INFO,"Kode Rekening Tidak Ditemukan"))
                        return HttpResponseRedirect('/jurnal/%s/%s/gl_gl_pusat/'% (object_id,user.id))
                    debet = itemform.cleaned_data['debet']
                    kredit = itemform.cleaned_data['kredit']
                    deskripsi = itemform.cleaned_data['deskripsi']
                    debet = debet
                    kredit = kredit
                if jurnal.j_status == '1':
                    itemjurnal = Tbl_Transaksi_History.objects.create(id_coa= rekening,debet=debet,kredit=kredit,\
                        tgl_trans=tgl_trans,no_trans =jurnal.no_akad,jurnal_h = jurnal,id_product=4,status_jurnal=1,\
                        id_cabang=300,id_unit=300,jenis='GL_GL_PUSAT_BANK',deskripsi=deskripsi)
                    itemju = Tbl_Transaksi.objects.create(id_coa= rekening,debet=debet,kredit=kredit,tgl_trans=tgl_trans,\
                        no_trans =jurnal.no_akad,jurnal = jurnal_asli,id_product=4,status_jurnal=1,id_cabang=0,id_unit=300,\
                        jenis='GL_GL_PUSAT_BANK',deskripsi=deskripsi)
                else:
                    itemjurnal = Tbl_Transaksi_History.objects.create(id_coa= rekening,debet=debet,kredit=kredit,tgl_trans=tgl_trans,\
                        no_trans =jurnal.no_akad,jurnal_h = jurnal,id_product=4,status_jurnal=1,id_cabang=300,id_unit=300,\
                        jenis='GL_GL_PUSAT',deskripsi=deskripsi)
                    itemju = Tbl_Transaksi.objects.create(id_coa= rekening,debet=debet,kredit=kredit,tgl_trans=tgl_trans,\
                        no_trans =jurnal.no_akad,jurnal = jurnal_asli,id_product=4,status_jurnal=1,id_cabang=300,id_unit=300,\
                        jenis='GL_GL_PUSAT',deskripsi=deskripsi)              
            messages.add_message(request, messages.INFO,"Jurnal telah disimpan dengan sukses")
            return HttpResponseRedirect('/jurnal/%s/%s/gl_gl_pusat/'% (object_id,user.id))
        else:
            messages.add_message(request, messages.INFO,"Form Tidak Valid")
            #request.user.message_set.create(messages.add_message(request, messages.INFO,"Form Tidak Valid"))
        var = {'form': form, 'formset': formset,'show':show,'cabang':object_id}
    else:
        var = {'form': MainJurnalForm(), 'formset': Tbl_Transaksi_History_glFormset(),'show':show,'cabang':object_id}
    variables = RequestContext(request, var)
    return render_to_response('jurnal/add_gl_pusat.html', variables)


def jurnal_post_gl(request):
    user = request.user
    for i in request.POST.getlist('id_pilih'):        
        gl = Jurnal.objects.get(id=(i))
        jurnal = gl.tbl_transaksi_set.filter(tgl_trans= datetime.date.today()) 
        for mutasi in jurnal:
            mutasi.status_jurnal = 2
            mutasi.save() 
    return HttpResponseRedirect("/jurnal/%s/%s/gl_gl_pusat/" % (user.profile.gerai.kode_cabang,user.id))

def hapus_gl(request,object_id):
    user = request.user
    tbl = Jurnal.objects.get(id=object_id)   
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Penghapusan Jurnal Berhasil')
    return HttpResponseRedirect("/jurnal/%s/%s/gl_gl_pusat/" % (user.profile.gerai.kode_cabang,user.id))


def jurnal_post(request):
    user = request.user
    for i in request.POST.getlist('id_pilih'):        
        gl = Jurnal_History.objects.get(id=(i))
        jurnal = gl.ordered_items.filter(tgl_trans= datetime.date.today()).filter(jurnal_h__id =gl.id) 

        for mutasi in jurnal:
            mutasi.status_jurnal = 2
            mutasi.save() 
        if mutasi.id_cabang == mutasi.id_cabang_tuju:
            messages.add_message(request, messages.INFO,' Transaksi  Rak Terposting.')                
        else:
            jurnal_biaya_rak_cabang(mutasi, request.user)
            messages.add_message(request, messages.INFO,' Transaksi Jurnal Berhasil .')
    return HttpResponseRedirect("/jurnal/%s/%s/add_baru_h/" % (user.profile.gerai.kode_cabang,user.id))

def jurnal_biaya_rak_cabang(mutasi, user):
    D = decimal.Decimal
    coa_bea = Jurnal_History.objects.get(pk = mutasi.jurnal_h.id)
    bm = RakPusatMapper.objects.get(cabang__kode_cabang = mutasi.id_cabang_tuju)
    a_rak_cabang = bm.coa_rak_cabang
    a_rak_pusat = bm.coa_rak_pusat
    ######jurnal2

    jurnal = Jurnal.objects.create(
        diskripsi= 'GL RAK CABANG ',kode_cabang = mutasi.id_cabang_tuju,object_id=mutasi.id,
        tgl_trans = mutasi.tgl_trans,cu = user, mu = user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_RAK_CABANG "), id_coa = mutasi.jurnal_h.coa_rak_pusat,deskripsi = mutasi.deskripsi,
        kredit = 0,debet = D(mutasi.debet) + D(mutasi.kredit),id_product = '5',status_jurnal ='2',tgl_trans =mutasi.tgl_trans,
        id_cabang =mutasi.id_cabang_tuju,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_RAK_CABANG"), id_coa = a_rak_pusat,deskripsi = mutasi.deskripsi,
        debet = 0,kredit = D(mutasi.debet) + D(mutasi.kredit),id_product = '5',status_jurnal ='2',tgl_trans =mutasi.tgl_trans,
        id_cabang =mutasi.id_cabang_tuju,id_unit= 300)
    #### pusat
    jurnal = Jurnal.objects.create(
        diskripsi= 'GL RAK PUSAT ',kode_cabang = 300,object_id=mutasi.id,
        tgl_trans = mutasi.tgl_trans,cu = user, mu = user)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_RAK_PUSAT "),id_coa = a_rak_cabang ,deskripsi = mutasi.deskripsi,
        kredit = 0,debet = D(mutasi.debet) + D(mutasi.kredit),id_product = '5',status_jurnal ='2',tgl_trans =mutasi.tgl_trans,
        id_cabang =300,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_RAK_PUSAT"), id_coa = mutasi.id_coa , deskripsi = mutasi.deskripsi,
        debet = 0,kredit = D(mutasi.debet) + D(mutasi.kredit),id_product = '5',status_jurnal ='2',tgl_trans =mutasi.tgl_trans,
        id_cabang =300,id_unit= 300)
    delet = Jurnal_History.objects.get(pk= mutasi.jurnal_h.id).delete()



def hapus_jurnal_h(request,object_id):
    user = request.user
    tbl = Jurnal_History.objects.get(id=object_id)   
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Penghapusan Jurnal Berhasil')
    return HttpResponseRedirect("/jurnal/%s/%s/add_baru_h/" % (user.profile.gerai.kode_cabang,user.id))


def hapus(request,object_id):
    tbl = Tbl_Transaksi.objects.get(id=object_id)
    ju = tbl.jurnal.id
    ju.delete()
    messages.add_message(request, messages.INFO, 'Penghapusan Jurnal Berhasil')
    return HttpResponseRedirect(tbl.get_absolute_url() )

def akun_search(request):
    '''Fasilitas cari kode atau nama COA - ajaxed untuk saat entry jurnal'''
    query = request.GET.get('q', '')
    if query:
        qset = (Q(deskripsi__icontains=query) or Q(coa__icontains=query))
        results = Tbl_Akun.objects.filter(qset).distinct()
        if request.GET.has_key('jurnal'):
            results = [r for r in results if r.is_child() == True]
        if request.GET.has_key('ajax'):
            return render_to_response("jurnal/ajax_result.html", {'object_list': results})
    return HttpResponseRedirect("/")


def add_baru_h(request,object_id,user,form_class):
    user = request.user
    sekarang = datetime.date.today()
    Tbl_Transaksi_HistoryFormset = get_ordereditem_formset(form_class, extra=1, can_delete=True)
    ju = Jurnal_History.objects.all()
    show = Tbl_Transaksi_History.objects.filter(status_jurnal=1,jurnal_h__cu__id = user.id).filter(id_cabang=object_id).filter(tgl_trans= sekarang).\
        filter(jenis=('GL_GL_RAK_PUSAT'))
    order = Tbl_Transaksi_History.objects.all()
    if request.method == 'POST':
        form = MainJurnalForm(request.POST)
        formset = Tbl_Transaksi_HistoryFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            tgl_trans = form.cleaned_data['tgl_trans']
            #j_status = form.cleaned_data['j_status']
            jurnal = Jurnal_History.objects.create(tgl_trans=tgl_trans,diskripsi='GL_GL_RAK_PUSAT',kode_cabang=user.profile.gerai.kode_cabang,cu=user,mu=user)
            #jurnal_asli = Jurnal.objects.create(tgl_trans=tgl_trans,diskripsi='GL_GL_PUSAT_BANK',cu=user,mu=user,kode_cabang=user.profile.gerai.kode_cabang)
            for itemform in formset.forms:
                koderekening = itemform.cleaned_data['koderekening']
                kdd = koderekening[:8]
                if koderekening:
                    rekening = Tbl_Akun.objects.get(coa=kdd)                    
                    if not rekening:
                        message_set.create( messages.add_message(request, messages.INFO,"Kode Rekening Tidak Ditemukan"))
                        return HttpResponseRedirect('/jurnal/%s/%s/add_baru_h/'% (object_id,user.id))
                    debet = itemform.cleaned_data['debet']
                    kredit = itemform.cleaned_data['kredit']
                    deskripsi = itemform.cleaned_data['deskripsi']
                    id_cabang = itemform.cleaned_data['id_cabang']
                    debet = debet
                    kredit = kredit
                if jurnal.j_status == '1':
                    itemjurnal = Tbl_Transaksi_History.objects.create(id_coa= rekening,debet=debet,kredit=kredit,\
                        tgl_trans=tgl_trans,no_trans =jurnal.no_akad,jurnal_h = jurnal,id_product=5,status_jurnal=1,id_cabang_tuju = id_cabang,\
                        id_cabang=300,id_unit=300,jenis='GL_GL_RAK_PUSAT',deskripsi=deskripsi)
                    #itemju = Tbl_Transaksi.objects.create(id_coa= rekening,debet=debet,kredit=kredit,tgl_trans=tgl_trans,\
                        #no_trans =jurnal.no_akad,jurnal = jurnal_asli,id_product=4,status_jurnal=1,id_cabang=0,id_unit=300,\
                        #id_cabang_tuju = id_cabang,jenis='GL_GL_PUSAT_BANK',deskripsi=deskripsi)
                else:
                    itemjurnal = Tbl_Transaksi_History.objects.create(id_coa= rekening,debet=debet,kredit=kredit,tgl_trans=tgl_trans,\
                        no_trans =jurnal.no_akad,jurnal_h = jurnal,id_product=5,status_jurnal=1,id_cabang=300,id_unit=300,id_cabang_tuju = id_cabang,\
                        jenis='GL_GL_RAK_PUSAT',deskripsi=deskripsi)
                    #itemju = Tbl_Transaksi.objects.create(id_coa= rekening,debet=debet,kredit=kredit,tgl_trans=tgl_trans,\
                        #no_trans =jurnal.no_akad,jurnal = jurnal_asli,id_product=4,status_jurnal=1,id_cabang=300,id_unit=300,\
                        #id_cabang_tuju = id_cabang,jenis='GL_GL_PUSAT',deskripsi=deskripsi) 
                
            messages.add_message(request, messages.INFO,"Jurnal telah disimpan dengan sukses")
            return HttpResponseRedirect('/jurnal/%s/%s/add_baru_h/'% (object_id,user.id))
        else:
            message_set.create(messages.add_message(request, messages.INFO,"Form Tidak Valid"))
        var = {'form': form, 'formset': formset,'show':show,'cabang':object_id}
    else:
        var = {'form': MainJurnalForm(), 'formset': Tbl_Transaksi_HistoryFormset(),'show':show,'cabang':object_id}
    variables = RequestContext(request, var)
    return render_to_response('jurnal/add_baru.html', variables)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def gl_glcabang(request,object_id,form_class):
    sekarang = datetime.date.today()
    Tbl_Transaksi_HistoryFormset = get_ordereditem_formset(form_class, extra=1, can_delete=True)
    ju = Jurnal_History.objects.all()
    show = Tbl_Transaksi.objects.all().filter(status_jurnal=1).filter(id_cabang=object_id).filter(tgl_trans= sekarang).\
        filter(jenis__in=('GL_GL_CABANG','GL_GL_CABANG_BANK','GL_GL_JUNAL_PENDAPATAN'))
    order = Tbl_Transaksi_History.objects.all()
    user = request.user
    if request.method == 'POST':
        form = MainJurnalForm(request.POST)
        formset = Tbl_Transaksi_HistoryFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            tgl_trans = form.cleaned_data['tgl_trans']
            j_status = form.cleaned_data['j_status']
            jurnal = Jurnal_History.objects.create(tgl_trans=tgl_trans,diskripsi='gl gl cabang',j_status=j_status)
            jurnal_asli = Jurnal.objects.create(tgl_trans=tgl_trans,diskripsi='gl gl cabang',cu=user,mu=user,\
                kode_cabang=user.profile.gerai.kode_cabang)
            for itemform in formset.forms:
                koderekening = itemform.cleaned_data['koderekening']
                kdd = koderekening[:8]
                if koderekening:
                    rekening = Tbl_Akun.objects.get(coa=kdd)                    
                    if not rekening:
                        message_set.create( messages.add_message(request, messages.INFO,"Kode Rekening Tidak Ditemukan"))
                        return HttpResponseRedirect('/jurnal/%s/gl_glcabang/'% (object_id))
                    debet = itemform.cleaned_data['debet']
                    kredit = itemform.cleaned_data['kredit']
                    deskripsi = itemform.cleaned_data['deskripsi']
                    debet = debet
                    kredit = kredit
                if jurnal.j_status == '1':
                    itemjurnal = Tbl_Transaksi_History.objects.create(id_coa= rekening,debet=debet,kredit=kredit,\
                        tgl_trans=tgl_trans,no_trans =jurnal.no_akad,jurnal_h = jurnal,id_product=4,status_jurnal=1,\
                        id_cabang=user.profile.gerai.kode_cabang,id_unit=300,jenis='GL_GL_CABANG_BANK',deskripsi=deskripsi)
                    itemju = Tbl_Transaksi.objects.create(id_coa= rekening,debet=debet,kredit=kredit,tgl_trans=tgl_trans,\
                        no_trans =jurnal.no_akad,jurnal = jurnal_asli,id_product=4,status_jurnal=1,id_cabang=user.profile.gerai.kode_cabang,\
                        id_unit=300,jenis='GL_GL_CABANG_BANK',deskripsi=deskripsi)
                if jurnal.j_status == '2':
                    itemjurnal = Tbl_Transaksi_History.objects.create(id_coa= rekening,debet=debet,kredit=kredit,\
                        tgl_trans=tgl_trans,no_trans =jurnal.no_akad,jurnal_h = jurnal,id_product=4,status_jurnal=1,\
                        id_cabang=user.profile.gerai.kode_cabang,id_unit=300,jenis='GL_GL_JUNAL_PENDAPATAN',deskripsi=deskripsi)
                    itemju = Tbl_Transaksi.objects.create(id_coa= rekening,debet=debet,kredit=kredit,tgl_trans=tgl_trans,\
                        no_trans =jurnal.no_akad,jurnal = jurnal_asli,id_product=4,status_jurnal=1,id_cabang=user.profile.gerai.kode_cabang,\
                        id_unit=300,jenis='GL_GL_JUNAL_PENDAPATAN',deskripsi=deskripsi)
                else:
                    itemjurnal = Tbl_Transaksi_History.objects.create(id_coa= rekening,debet=debet,kredit=kredit,tgl_trans=tgl_trans,\
                        no_trans =jurnal.no_akad,jurnal_h = jurnal,id_product=4,status_jurnal=1,id_cabang=user.profile.gerai.kode_cabang,id_unit=300,\
                        jenis='GL_GL_CABANG',deskripsi=deskripsi)
                    itemju = Tbl_Transaksi.objects.create(id_coa= rekening,debet=debet,kredit=kredit,tgl_trans=tgl_trans,\
                        no_trans =jurnal.no_akad,jurnal = jurnal_asli,id_product=4,status_jurnal=1,id_cabang=user.profile.gerai.kode_cabang,\
                        id_unit=300,jenis='GL_GL_CABANG',deskripsi=deskripsi) 
            messages.add_message(request, messages.INFO,"Jurnal telah disimpan dengan baik")
            return HttpResponseRedirect('/jurnal/%s/gl_glcabang/'% (object_id))
        else:
            request.user.message_set.create(messages.add_message(request, messages.INFO,"Form Tidak Valid"))
        var = {'form': form, 'formset': formset,'show':show,'cabang':object_id}
    else:
        var = {'form': MainJurnalForm(), 'formset': Tbl_Transaksi_HistoryFormset(),'show':show,'cabang':object_id}
    variables = RequestContext(request, var)
    return render_to_response('jurnal/gl_glcabang.html', variables)



def hapus_glglcabang(request,object_id):
    user = request.user
    tbl = Jurnal.objects.get(id=object_id)   
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Jurnal Berhasil Dihapus')
    return HttpResponseRedirect("/jurnal/%s/gl_glcabang/" % user.profile.gerai.kode_cabang)

def jurnal_glpost(request):
    user = request.user
    for i in request.POST.getlist('id_pilih'):        
        gl = Jurnal.objects.get(id=(i))
        jurnal = gl.tbl_transaksi_set.filter(tgl_trans= datetime.date.today()).filter(jurnal__id =gl.id) 

        for mutasi in jurnal:
            mutasi.status_jurnal = 2
            mutasi.save() 
            messages.add_message(request, messages.INFO,' Transaksi GL Berhasil.')
    return HttpResponseRedirect("/jurnal/%s/gl_glcabang/" % user.profile.gerai.kode_cabang)
    #for i in request.POST.getlist('id_pilih'):
        #gl = Tbl_Transaksi.objects.get(id=(i))
        #gl.status_jurnal = 2
        #gl.save()
        #messages.add_message(request, messages.INFO,' Input GL manual Cabang Berhasil.')
    #return HttpResponseRedirect(gl.get_absolute_url_batal_jurnal_glcabang())


def add_baru(request, form_class):
    sekarang = datetime.date.today()
    Tbl_TransaksiFormset = get_ordereditem_formset(form_class, extra=1, can_delete=True)
    show = Tbl_Transaksi.objects.all().filter(status_jurnal=1).filter(tgl_trans= sekarang).filter(jenis='GL_GL')
    order = Tbl_Transaksi.objects.all()
    if request.method == 'POST':
        form = MainJurnalForm(request.POST)
        formset = Tbl_TransaksiFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            gerai = form.cleaned_data['gerai']
            diskripsi = form.cleaned_data['diskripsi']
            tgl_trans = form.cleaned_data['tgl_trans']
            jurnal = Jurnal.objects.create(diskripsi=diskripsi,tgl_trans=tgl_trans)
            for itemform in formset.forms:
                id_coa = itemform.cleaned_data['id_coa']
                debet = itemform.cleaned_data['debet']
                kredit = itemform.cleaned_data['kredit']
                debet = debet
                kredit = kredit
                itemjurnal = Tbl_Transaksi.objects.create(id_coa= id_coa,debet=debet,kredit=kredit,tgl_trans=tgl_trans,#datetime.date.today(),
                    jurnal = jurnal,id_product=4,status_jurnal=1,id_cabang=1,id_unit=300,jenis='GL_GL')
            messages.add_message(request, messages.INFO,"Jurnal telah disimpan dengan sukses")
    else:
        form = MainJurnalForm()
        formset = Tbl_TransaksiFormset()
    return render_to_response('jurnal/add_baru.html', {'form': form, 'formset': formset,'show':show},
        context_instance=RequestContext(request))


def add_staff(request,object_id):
    show = Tbl_Transaksi.objects.all().filter(status_jurnal=1).filter(id_cabang=0).filter(jenis='GL_GL')
    Tbl_TransaksiFormSet = formset_factory(Tbl_TransaksiForm, extra=1,max_num=1)
    if request.method == 'POST':
        formset = Tbl_TransaksiFormSet(request.POST)
        form = MainJurnalForm(request.POST)
        if formset.is_valid() and form.is_valid():
            nobukti = form.cleaned_data['nobukti']
            diskripsi = form.cleaned_data['diskripsi']
            tgl_trans = form.cleaned_data['tgl_trans']
            #nilai = form.cleaned_data['nilai']
            jurnal = Jurnal.objects.create(diskripsi=diskripsi,tgl_trans=tgl_trans,nobukti=nobukti)
            for itemform in formset.forms:
                id_coa = itemform.cleaned_data['id_coa']
                debet = itemform.cleaned_data['debet']
                kredit = itemform.cleaned_data['kredit']
                gerai = itemform.cleaned_data['gerai']
                #is_debet = itemform.cleaned_data['is_debet']
                #if is_debet  == None:
                    #debet = nilai
                    #kredit = 0
                #else:
                    #debet = 0
                    #kredit = nilai
                debet = debet
                kredit = kredit
                itemjurnal = Tbl_Transaksi.objects.create(id_coa= id_coa,debet=debet,kredit=kredit,tgl_trans=tgl_trans,#datetime.date.today(),
                    jurnal = jurnal,id_product=4,status_jurnal=1,id_cabang=object_id,id_unit=300,jenis='GL_GL',antar_kantor=gerai)
                
            messages.add_message(request, messages.INFO,"Jurnal telah disimpan dengan sukses")
            return HttpResponseRedirect(itemjurnal.get_absolute_url_staff())
        else:
            messages.add_message(request, messages.INFO,"ADA NILAI YANG BELUM ANDA MASUKAN")
        var = {'form': form, 'formset': formset,'show':show}
    else:
        var = {'form': MainJurnalForm(), 'formset': Tbl_TransaksiFormSet(initial= [{"is_debet":True}, {"is_debet":False}]),'show':show}
    variables = RequestContext(request, var)
    return render_to_response('jurnal/add_gl_gl.html', variables)

def add_staff_non_kas(request,object_id):
    sekarang = datetime.date.today()
    show = Tbl_Transaksi.objects.filter(status_jurnal=1).filter(id_cabang=object_id).filter(tgl_trans=sekarang).filter(jenis='GL_GL_NON_KAS')
    Tbl_TransaksiFormSet = formset_factory(Tbl_TransaksiForm, extra=1,max_num=1)
    if request.method == 'POST':
        formset = Tbl_TransaksiFormSet(request.POST)
        form = MainJurnalForm(request.POST)
        if formset.is_valid() and form.is_valid():
            nobukti = form.cleaned_data['nobukti']
            diskripsi = form.cleaned_data['diskripsi']
            tgl_trans = form.cleaned_data['tgl_trans']
            #nilai = form.cleaned_data['nilai']
            jurnal = Jurnal.objects.create(diskripsi=diskripsi,tgl_trans=tgl_trans,nobukti=nobukti)
            for itemform in formset.forms:
                id_coa = itemform.cleaned_data['id_coa']
                debet = itemform.cleaned_data['debet']
                kredit = itemform.cleaned_data['kredit']
                gerai =itemform.cleaned_data['gerai']
                debet = debet
                kredit = kredit
                itemjurnal = Tbl_Transaksi.objects.create(id_coa= id_coa,debet=debet,kredit=kredit,tgl_trans= tgl_trans,#datetime.date.today(),
                    jurnal = jurnal,id_product=4,status_jurnal=1,id_cabang=object_id,id_unit=300,jenis='GL_GL_NON_KAS',antar_kantor=gerai)
                
            messages.add_message(request, messages.INFO,"Jurnal telah disimpan dengan sukses")
            return HttpResponseRedirect(itemjurnal.get_absolute_url_non_staff())
        else:
            messages.add_message(request, messages.INFO,"ADA NILAI YANG BELUM ANDA MASUKAN")
        var = {'form': form, 'formset': formset,'show':show}
    else:
        var = {'form': MainJurnalForm(), 'formset': Tbl_TransaksiFormSet(initial= [{"is_debet":True}, {"is_debet":False}]),'show':show,
               'total_debet': sum([p.debet for p in show]),'total_kredit': sum([p.kredit for p in show])}
    variables = RequestContext(request, var)
    return render_to_response('jurnal/add_gl_gl_non_kas.html', variables)    


def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['KEUANGAN','SUPERUSER','MANKEU'])
@login_required
@user_passes_test(is_in_multiple_groups)
def index(request): 
    jurnal_list = Tbl_Transaksi.objects.all()
    trans=[]
    form = Tbl_AkunForm()
    start_date = None
    end_date = None
    id_cabang = None
    if 'id_cabang' in request.GET and request.GET['id_cabang']  and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        ledger_search = Tbl_Transaksi.objects.filter(id_cabang=id_cabang).filter(tgl_trans__range=(start_date,end_date)).\
            filter(status_jurnal = 2)   
        trans = []
        for l in ledger_search:           
            trans.append(l)
        start_date = start_date
        id_cabang = id_cabang
        end_date = end_date
    
        template='jurnal/index.html'
        variable = RequestContext(request, {'jurnal_list': trans,'total_debet': sum([p.debet for p in trans]),'total_kredit': sum([p.kredit for p in trans]),
                'start_date':start_date,'id_cabang':id_cabang,'end_date':start_date})

    elif 'id_cabang' in request.GET and request.GET['id_cabang']  and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        ledger_search = Tbl_Transaksi.objects.filter(id_cabang=id_cabang).filter(tgl_trans__range=(start_date,end_date)).\
            filter(status_jurnal__in=(2,3))
        trans = []
        for l in ledger_search:
            trans.append(l)
        start_date = start_date
        id_cabang = id_cabang
        end_date = end_date

        template1= 'jurnal/cetak_jurnal_transaksi.html'
        variable = RequestContext(request, {'jurnal_list': trans,'total_debet': sum([p.debet for p in trans]),'total_kredit': sum([p.kredit for p in trans]),
                'start_date':start_date,'id_cabang':id_cabang,'end_date':start_date})
        return render_to_response(template1,variable)

    elif 'id_cabang' in request.GET and request.GET['id_cabang']  and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        ledger_search = Tbl_Transaksi.objects.filter(id_cabang=id_cabang).filter(tgl_trans__range=(start_date,end_date)).\
            filter(status_jurnal = 3)
        trans = []
        for l in ledger_search:
            trans.append(l)
        start_date = start_date
        id_cabang = id_cabang
        end_date = end_date

        template3='jurnal/index.html'
        variable = RequestContext(request, {'jurnal_list': trans,'total_debet': sum([p.debet for p in trans]),'total_kredit': sum([p.kredit for p in trans]),
                'start_date':start_date,'id_cabang':id_cabang,'end_date':start_date})
        return render_to_response(template3,variable)

    else:
        template = 'jurnal/index.html'
        variable = RequestContext(request, {'jurnal_list': trans,'total_debet': sum([p.debet for p in trans]),'total_kredit': sum([p.kredit for p in trans]),
            'start_date':start_date,'id_cabang':id_cabang,'end_date':start_date})
        return render_to_response(template,variable)


def index_all(request): 
    jurnal_list = Tbl_Transaksi.objects.all()
    ledger_search = Tbl_Transaksi.objects.all() 
    all = []
    for l in ledger_search:
        all.append(l)
    variables = RequestContext(request, {'jurnal': all,'total_debet': sum([p.debet for p in all]),'total_kredit': sum([p.kredit for p in all])})
    return render_to_response('jurnal/index.html', variables)

def show(request, object_id):
    jurnal = get_object_or_404(Jurnal, id=object_id)
    variables = RequestContext(request, {'jurnal': jurnal})
    return render_to_response('jurnal/show.html', variables)

def mastertiket_setoran_pengeluaran_gerai(request,object_id):
    sekarang = datetime.date.today()
    #user = request.user
    mastertiket
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=object_id).filter(status_jurnal=2).\
        filter(jenis__in=(u'GL_GL_PENAMBAHAN_PUSAT_BANK',u'GL_GL_PENAMBAHAN_PUSAT_KAS',u'GL_GL_PENGELUARAN_PUSAT_BANK',
        'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI',\
        u'GL_GL_PENGELUARAN_PUSAT_KAS',u'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI','GL_GL_RAK_PUSAT','GL_GL_PENGEMBALIAN_PUSAT_BANK',\
        'GL_GL_PENGEMBALIAN_PUSAT_BANK_RAK'))   
    template = 'ledger/mastertiket_setoran_pengeluaran.html'
    variables = RequestContext(request, {'user':User,'g':gr,'total_debet': sum([p.debet for p in gr]),'total_kredit': sum([p.kredit for p in gr])})
    return render_to_response(template, variables)


def mastertiket_ayda_pusat(request,object_id):
    cabang = Tbl_Cabang.objects.get(kode_cabang=object_id)
    sekarang = datetime.date.today()
    #user = request.user
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=object_id).filter(status_jurnal=2).filter(jenis = 'PENJUALAN_AYDA_PUSAT')
    template = 'ledger/mastertiket_ayda_pusat.html'
    variables = RequestContext(request, {'cabang':cabang,'user':User,'g':gr,'total_debet': sum([p.debet for p in gr]),'total_kredit': sum([p.kredit for p in gr])})
    return render_to_response(template, variables)

def mastertiket_penjualan_ayda(request,object_id):
    cabang = Tbl_Cabang.objects.get(kode_cabang=object_id)
    sekarang = datetime.date.today()
    #user = request.user
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=object_id).filter(status_jurnal=2).filter(jenis__in =('AYDA_PUSAT','AYDA_PUSAT_BANK'))
    template = 'ledger/mastertiket_penjualan_ayda.html'
    variables = RequestContext(request, {'cabang':cabang,'user':User,'g':gr,'total_debet': sum([p.debet for p in gr]),'total_kredit': sum([p.kredit for p in gr])})
    return render_to_response(template, variables)

def mastertiket(request):
    sekarang = datetime.date.today()
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    cabang = Tbl_Cabang.objects.get(kode_cabang=cab)
    template = 'ledger/mastertiket_pencairan.html'
    variables = RequestContext(request, {'cabang':cabang,'user':User})
    return render(request,'ledger/mastertiket_pencairan.html',{'cabang':cabang,'user':user})

def mastertiket_pencairan(request,object_id):
    dari = None
    hingga = None
    cabang = None
    if  'dari' in request.GET and request.GET['hingga']:
        cabang = Tbl_Cabang.objects.get(kode_cabang=object_id)
        dari = request.GET['dari']
        hingga = request.GET['hingga']
        gr = Tbl_Transaksi.objects.filter(tgl_trans__range=(dari,hingga)).filter(id_cabang=object_id).filter(status_jurnal= 2).filter(jenis__in=(u'Pencairan',u'Pencairan_barang_sama'))
    else:
        gr = Tbl_Transaksi.objects.all()
    variables = RequestContext(request, {'cabang':cabang,'g': gr,'total_debet': sum([p.debet for p in gr]),'total_kredit': sum([p.kredit for p in gr])})
    return render_to_response('ledger/mastertiket.html', variables)

### MASTER TIKET PELUNASAN ADM GADAI ULANG BARANG SAMA
@login_required
@user_passes_test(lambda u: u.groups.filter(name='ADM_GERAI'))
def mastertiket_adm_pelunasan_gadai_ulang(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    cabang = Tbl_Cabang.objects.get(kode_cabang=cab)
    sekarang = datetime.date.today()
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=cab,status_jurnal=2,jenis__in=(u'Pelunasan_Barang_sama',\
        u'Pelunasan_Barang_sama_nilai_lebih'))
    return render(request,'ledger/mastertiket_adm_pelunasan_gu.html', {'cabang':cabang,'user':user,'g':gr,\
        'total_debet': sum([p.debet for p in gr]),'total_kredit': sum([p.kredit for p in gr])})
### AKHIR MASTER TIKET PELUNASAN ADM GADAI ULANG BARANG SAMA

def mastertiket_adm_pelunasan(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    cabang = Tbl_Cabang.objects.get(kode_cabang=cab)
    sekarang = datetime.date.today()
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang,id_cabang=cab,status_jurnal=2,jenis__in=(u'Pelunasan_adm',\
        u'Pelunasan_adm_diskon','Pelunasan_kasir_rak1','Pelunasan_kasir_bank_rak1'))
    return render(request,'ledger/mastertiket_adm_pelunasan.html', {'cabang':cabang,'user':User,'g':gr,
        'total_debet': sum([p.debet for p in gr]),'total_kredit': sum([p.kredit for p in gr])})

def mastertiket_adm_penjualan_pelelangan(request,object_id):
    cabang = Tbl_Cabang.objects.get(kode_cabang=object_id)
    sekarang = datetime.date.today()
    #user = request.user
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=object_id).filter(status_jurnal=2).filter(jenis=u'Penjualan_lelang_adm')
    template = 'ledger/mastertiket_adm_pejualan_pelelangan.html'
    variables = RequestContext(request, {'cabang':cabang,'user':User,'g':gr,'total_debet': sum([p.debet for p in gr]),'total_kredit': sum([p.kredit for p in gr])})
    return render_to_response(template, variables)

def master_tiket_Pelunasan_Gadai_Ulang_kasir(request,object_id):
    sekarang = datetime.date.today()
    cabang = Tbl_Cabang.objects.get(kode_cabang=object_id)
    #user = request.user
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=object_id).filter(status_jurnal=2).\
        filter(jenis__in=(u'Pelunasan_gu_kasir_nilai_sblm_kurang_bol',u'Pelunasan_gu_kasir_nilai_sblm_lebih_pol',\
        u'Pelunasan_Gadai_Ulang_kasir',u'Pelunasan_Gadai_Ulang_kasir_nilai_pinjaman_lebih',u'Pelunasan_gu_kasir_nilai_sblm_lebih',\
        u'Pelunasan_gu_kasir_nilai_sblm_kurang',u'Pelunasan_Gadai_Ulang_kasir_pinjaman_besar_tp',u'Pelunasan_Gadai_Ulang_kasir_pinjaman_besar',\
        u'Pelunasan_gu_kasir_nilai_sblm_lebih_tp',u'Pelunasan_gu_kasir_nilai_sblm_lebih_bl',u'Pelunasan_gu_kasir_nilai_sblm_lebih',\
        u'Pelunasan_gu_kasir_nilai_sblm_kurang_kas',u'Pelunasan_gu_kasir_nilai_sblm_kurang_pdl',u'Pelunasan_Gadai_Ulang_kasir_bank',\
        u'Pelunasan_gu_bank_nilai_sblm_lebih',u'Pelunasan_gu_bank_nilai_sblm_lebih_pol','Pelunasan_gu_kasir_nilai_sblm_kurang_bank',\
       'Pelunasan_gu_kasir_nilai_sblm_kurang_bol_bank','Pelunasan_gu_kasir_nilai_sblm_lebih_bank_10_bol',\
       'Pelunasan_gu_kasir_nilai_sblm_kurang_bank_bol','Pelunasan_gu_kasir_nilai_sblm_lebih_bank_10','Pelunasan_Gadai_ulang_kasir_bank_kelebihan_transfer_pendapatan','Pelunasan_kasir_bank'))
    template = 'ledger/mastertiket_pelunasan_gadai_ulang_kasir.html'
    variables = RequestContext(request, {'cabang':cabang,'user':User,'g':gr,'total_debet': sum([p.debet for p in gr]),'total_kredit': sum([p.kredit for p in gr])})
    return render_to_response(template, variables)


def mastertiket_kasir_penjualan_pelelangan(request,object_id):
    sekarang = datetime.date.today()
    #user = request.user
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=object_id).filter(status_jurnal=2).\
        filter(jenis__in=(u'Penjualan_lelang_kasir',u'Penjualan_lelang_kasir_bank'))
    template = 'ledger/mastertiket_kasir_pejualan_pelelangan.html'
    variables = RequestContext(request, {'user':User,'g':gr,'total_debet': sum([p.debet for p in gr]),'total_kredit': sum([p.kredit for p in gr])})
    return render_to_response(template, variables)

def cetak_neraca_pjb(request):
    ledger = Tbl_Transaksi.objects.all()
    form = Tbl_AkunForm()
    if 'start_date' in request.GET and request.GET['start_date']:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_coa = request.GET['id_coa']
        id_cabang = request.GET['id_cabang']
        ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(id_coa=id_coa).filter(id_cabang=id_cabang).order_by('id')                
    else:
        template='ledger/cetakledger.html'
        variable = RequestContext(request,{'form':form})
        return render_to_response(template,variable)
                    
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=bukubesar_%s_coa_%s.xls' % (id_coa, id_cabang)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("bukubesar_%s_coa_%s" % (id_coa, id_cabang))
    
    row_num = 0
    
    columns = [
        (u"KODE UNIT", 6000),(u"KODE CABANG", 25000),(u"TANGGAL ", 6000),(u"COA", 6000),(u"DESKRIPSI", 6000),(u"DEBET", 6000),
        (u"KREDIT", 6000),                          
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1
    
    for cetak in ledger_search:
        row_num += 1
        row = [
            cetak.id_unit, cetak.id_cabang,cetak.tgl_trans,cetak.id_coa.coa,cetak.id_coa.deskripsi,cetak.debet,cetak.kredit,                                            
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response

#### NERACA HARIAN
def neraca_pjb(request):
    #form = BukuBesarForm()
    cab = Tbl_Cabang.objects.all()
    lb_akun = Tbl_Akun.objects.filter(view_unit__in =('0','300')).filter(jenis__in = ('a','p')).order_by('coa')
    t_debet = 0
    t_kredit = 0
    t_saldo_akhir = 0
    start_date = None
    id_cabang = None
    akun =[]
    if  'id_cabang' in request.GET and request.GET['id_cabang']:       
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            for c in lb_akun :
                akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.kredit_gabung_hari(id_cabang,start_date),'debet':c.debet_gabung_hari(id_cabang,start_date),
                    'coa':c.coa,'id':c.id,'id_cabang':300 + (int(id_cabang)) ,'header_parent':c.header_parent,'saldo_awal': c.saldo_pjb,
                    'saldo_akhir':  c.kredit_gabung_hari(id_cabang,start_date) - c.debet_gabung_hari(id_cabang,start_date)})
                #t_debet += c.total_debet_nenek(id_cabang,start_date,end_date)
                #t_kredit += c.total_kredit_nenek(id_cabang,start_date,end_date)
                start_date = start_date
                id_cabang = id_cabang
        else:
            for c in lb_akun :
                akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.kredit_hari(id_cabang,start_date),'debet':c.debet_hari(id_cabang,start_date),'coa':c.coa,
                    'id':c.id,'id_cabang': 300 + (int(id_cabang)) ,'header_parent':c.header_parent,
                    'saldo_akhir': (c.saldo_awalhari(id_cabang,start_date)) + (c.kredit_hari(id_cabang,start_date)) - (c.debet_hari(id_cabang,start_date)) ,
                    'saldo_awal': (c.saldo_awalhari(id_cabang,start_date)), })
                t_debet += c.debet_hari(id_cabang,start_date)
                t_kredit += c.kredit_hari(id_cabang,start_date)
                start_date = start_date
                id_cabang = id_cabang
    variable = RequestContext(request,{'akun':akun,'total_debet':t_debet,'total_kredit':t_kredit,'total_saldo_akhir':t_saldo_akhir,
        'start_date':start_date,'id_cabang':id_cabang})
    return render_to_response('ledger/neraca_pjb.html',variable)



def kasir_post(request):
    for i in request.POST.getlist('id_pilih'):
        gl = Tbl_Transaksi.objects.get(id=(i))
        gl.status_jurnal = 1
        gl.jenis = 'GL_GL_PUSAT'
        messages.add_message(request, messages.INFO,' Input GL manual Terposting.')
        gl.save()        
    return HttpResponseRedirect(gl.get_absolute_url())

def kasir_post_non_kas(request):
    for i in request.POST.getlist('id_pilih'):
        gl = Tbl_Transaksi.objects.get(id=int(i))
        gl.status_jurnal = 1
        gl.jenis = 'GL_GL_NON_KAS'
        messages.add_message(request, messages.INFO,' Input GL Non Kas Berhasil.')
        gl.save()
    return HttpResponseRedirect(gl.get_absolute_url())    

####LABA RUGI HARIAN
def laba_rugi(request):
    lb_akun = Tbl_Akun.objects.filter(view_unit__in=('300','0')).filter(jenis="l")
    t_debet = 0
    t_kredit = 0
    t_saldo_akhir = 0
    start_date = None
    end_date = None
    id_cabang = None
    akun =[]
    for c in lb_akun :
        if  'id_cabang' in request.GET and request.GET['id_cabang']:
            start_date = request.GET['start_date']
            end_date = request.GET['end_date']
            id_cabang = request.GET['id_cabang']            
            akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.my_kredit(id_cabang,start_date,end_date),'debet':c.my_debet(id_cabang,start_date,end_date),#'saldo_awal':saldo_dk ,
                'coa':c.coa,'id':c.id,'id_cabang':300 + (int(id_cabang)) ,'header_parent':c.header_parent,
                'saldo_akhir': c.view_saldo_akhir(id_cabang,start_date,end_date),
                'saldo_awal': c.saldo_pjb,})
            start_date = start_date
            id_cabang = id_cabang
            end_date = end_date    

    template='ledger/labarugi.html'
    variable = RequestContext(request,{'akun':akun,'total_debet':t_debet,'total_kredit':t_kredit,'total_saldo_akhir':t_saldo_akhir,
        'start_date':start_date,'id_cabang':id_cabang,'end_date':end_date})
    return render_to_response(template,variable)
####LABA RUGI HARIAN


def cetak_laba_rugi(request):    
    lb_akun = Tbl_Akun.objects.filter(jenis="l").filter(view_unit__in=('0','300'))
    t_debet = 0
    t_kredit = 0
    t_saldo_akhir = 0
    akun =[]
   
    if 'id_cabang' in request.GET and request.GET['id_cabang']:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        for c in lb_akun :
            akun.append(c)
            print akun
    else:        
        template = 'ledger/cetak/cetaklabarugi.html'
        variable = RequestContext(request,{'akun':akun})
        return render_to_response(template,variable)

    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=labarugi_%s_coa_%s.xls' #% (id_coa, id_cabang)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("bukubesar_%s_coa_%s" )#% (id_coa, id_cabang))
    
    row_num = 0

    
    columns = [
        (u"DESKRIPSI", 25000),(u"COA", 5000),(u"DEBET", 2500),(u"KREDIT ", 3000),        
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style.alignment.wrap = 1
    
    for cetak in akun:
        row_num += 1
        row = [
            cetak.deskripsi,cetak.coa,cetak.get_jumlah_debet(),cetak.get_jumlah_kredit(),                                            
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response
    
def neraca_percobaan(request):
    lb_akun = Tbl_Akun.objects.filter(view_unit__in=("0","300")).order_by('coa')
    t_debet = 0
    t_kredit = 0
    t_saldo_akhir = 0
    start_date = None
    end_date = None
    id_cabang = None
    akun=[]
    form = Tbl_AkunForm()
    if  'id_cabang' in request.GET and request.GET['id_cabang'] and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            for c in lb_akun :
                akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.my_kredit_gabung(id_cabang,start_date,end_date),'debet':c.my_debet_gabung(id_cabang,start_date,end_date),
                    'coa':c.coa,'id':c.id,'id_cabang':300 + (int(id_cabang)) ,'header_parent':c.header_parent,'saldo_awal': c.saldo_pjb,
                    'saldo_akhir':  c.view_saldo_akhir_gabung(id_cabang,start_date,end_date)})
                t_debet += c.total_debet_nenek(id_cabang,start_date,end_date)
                t_kredit += c.total_kredit_nenek(id_cabang,start_date,end_date)
                start_date = start_date
                end_date = end_date
                id_cabang = id_cabang
        else:
            for c in lb_akun :
                akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.my_kredit(id_cabang,start_date,end_date),
                    'debet':c.my_debet(id_cabang,start_date,end_date),
                    'coa':c.coa,'id':c.id,'id_cabang':300 + (int(id_cabang)) ,'header_parent':c.header_parent,'saldo_awal': c.saldo_pjb,
                    'saldo_akhir':  c.my_debet(id_cabang,start_date,end_date) - c.my_kredit(id_cabang,start_date,end_date)})
                #t_debet += c.total_debet_nenek(id_cabang,start_date,end_date)
                #t_kredit += c.total_kredit_nenek(id_cabang,start_date,end_date)
                start_date = start_date
                end_date = end_date
                id_cabang = id_cabang
                
        template='ledger/neraca_percobaan.html'
        variable = RequestContext(request,{'akun':akun,'total_saldo_akhir':t_saldo_akhir,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang})
        return render_to_response(template,variable)

    elif  'id_cabang' in request.GET and request.GET['id_cabang'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            for c in lb_akun :
                akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.my_kredit_gabung(id_cabang,start_date,end_date),'debet':c.my_debet_gabung(id_cabang,start_date,end_date),
                    'coa':c.coa,'id':c.id,'id_cabang':300 + (int(id_cabang)) ,'header_parent':c.header_parent,'saldo_awal': c.saldo_pjb,
                    'saldo_akhir':  c.view_saldo_akhir_gabung(id_cabang,start_date,end_date)})
                t_debet += c.total_debet_nenek(id_cabang,start_date,end_date)
                t_kredit += c.total_kredit_nenek(id_cabang,start_date,end_date)
                start_date = start_date
                end_date = end_date
                id_cabang = id_cabang
        else:
            for c in lb_akun :
                akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.my_kredit(id_cabang,start_date,end_date),'debet':c.my_debet(id_cabang,start_date,end_date),
                    'coa':c.coa,'id':c.id,'id_cabang':300 + (int(id_cabang)) ,'header_parent':c.header_parent,'saldo_awal': c.saldo_pjb,
                    'saldo_akhir':  c.view_saldo_akhir(id_cabang,start_date,end_date)})
                t_debet += c.total_debet_nenek(id_cabang,start_date,end_date)
                t_kredit += c.total_kredit_nenek(id_cabang,start_date,end_date)
                start_date = start_date
                end_date = end_date
                id_cabang = id_cabang

        template='ledger/cetak_neraca_percobaan.html'
        variable = RequestContext(request,{'akun':akun,'total_saldo_akhir':t_saldo_akhir,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang})
        return render_to_response(template,variable)
    else:
        template='ledger/neraca_percobaan.html'
        variable = RequestContext(request,{'form':form})
        return render_to_response(template,variable)


def cetak_neraca_percobaan(request):
    sekarang =datetime.date.today()
    ledger = Tbl_Transaksi.objects.all()
    form = Tbl_AkunForm()
    if 'start_date' in request.GET and request.GET['start_date']:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).order_by('id')                
    else:
        template='ledger/cetak/cetak_neraca_percobaan.html'
        variable = RequestContext(request,{'form':form})
        return render_to_response(template,variable)
                    
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=neracapercobaan_%s.xls' % (sekarang)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("neracapercobaab_%s" % (sekarang))
    
    row_num = 0
    
    columns = [
        (u"KODE UNIT", 6000),(u"KODE CABANG", 25000),(u"TANGGAL ", 6000),(u"COA", 6000),(u"DESKRIPSI", 6000),(u"DEBET", 6000),
        (u"KREDIT", 6000),                          
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1
    
    for cetak in ledger_search:
        row_num += 1
        row = [
            cetak.id_unit, cetak.id_cabang,cetak.tgl_trans,cetak.id_coa.coa,cetak.id_coa.deskripsi,cetak.debet,cetak.kredit,                                            
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response

def buku_besar(request):
    ledger = Tbl_Transaksi.objects.all()
    saldo = 0
    start_date = None
    end_date = None
    id_cabang = None
    total_debet = 0
    total_kredit = 0    
    form = Tbl_AkunForm()
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_coa = request.GET['id_coa']
        id_cabang = request.GET['id_cabang']
        #ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(id_cabang=id_cabang).filter(status_jurnal=1).order_by('id')
        trans = []
        b = Tbl_Akun.objects.get(id=int(id_coa))
        akumulasi_debet =0
        akumulasi_kredit = 0
        start_date = start_date
        end_date = end_date
        id_cabang = id_cabang
        if id_cabang == '500':
            ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(status_jurnal=2).filter(id_coa=id_coa).order_by('id')
            for l in ledger_search:
                for t in l.jurnal.tbl_transaksi_set.filter(id_coa=b):
                    akumulasi_debet += t.debet
                    akumulasi_kredit += t.kredit
                    trans.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir': (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)  ,'deskripsi': t.id_coa.deskripsi,\
                        'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,\
                        'id_coa':t.id_coa})
                    start_date = start_date
                    end_date = end_date
                    id_cabang = id_cabang
                    total_debet = akumulasi_debet
                    total_kredit = akumulasi_kredit
                    saldo = (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)

        else:
            ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(id_cabang=id_cabang).filter(status_jurnal=2).filter(id_coa=id_coa).order_by('id')
            for l in ledger_search:
                for t in l.jurnal.tbl_transaksi_set.filter(id_coa=b).filter(id_cabang=id_cabang):
                    akumulasi_debet += t.debet
                    akumulasi_kredit += t.kredit
                    trans.append({'t':t, 'debet':t.debet, 'kredit':t.kredit, 'saldo_akhir': (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit) , 'deskripsi': t.id_coa.deskripsi,\
                        'diskripsi' : t.jurnal.diskripsi, 'kepala_coa': t.kepala_coa, 'coa':t.id_coa.coa, 'nobukti': t.jurnal.nobukti, 'tgl_trans':t.tgl_trans,\
                        'id_coa':t.id_coa})
                    start_date = start_date
                    end_date = end_date
                    id_cabang = id_cabang
                    total_debet = akumulasi_debet
                    total_kredit = akumulasi_kredit
                    saldo = (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)        

        template='ledger/search/search_buku_besar.html'
        variable = RequestContext(request,{'form':form,'ledger_search':trans,'kode':Tbl_Akun.objects.get(id=int(id_coa)),'saldo_akhir':saldo,
            'total_kredit':total_debet,'total_debet': total_kredit ,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,
            'saldo':b.saldo_pjb})
        return render_to_response(template,variable)
    
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_coa = request.GET['id_coa']
        id_cabang = request.GET['id_cabang']
        ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(id_cabang=id_cabang).filter(status_jurnal=1).order_by('id')
        trans = []
        b = Tbl_Akun.objects.get(id=int(id_coa))
        akumulasi_debet =0
        akumulasi_kredit = 0
        start_date = start_date
        end_date = end_date
        id_cabang = id_cabang
        
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 0})
        money_format = workbook.add_format({'num_format': '#,##0'})
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        worksheet.set_column(0, 0, 10) 
        worksheet.set_column(1, 1, 15)
        worksheet.set_column(2, 2, 11)
        worksheet.set_column(3, 3, 37)
        worksheet.set_column(4, 4, 10)
        worksheet.set_column(5, 5, 10)
        worksheet.set_column(6, 6, 10)
        
        worksheet.write('A1', 'Tanggal', bold)
        worksheet.write('B1', 'Nomor Bukti', bold)
        worksheet.write('C1', 'COA', bold)
        worksheet.write('D1', 'Keterangan', bold)
        worksheet.write('E1', 'Debet', bold)
        worksheet.write('F1', 'Kredit', bold)
        worksheet.write('G1', 'Saldo', bold)        
        row = 1
        col = 0
        if id_cabang == '500':
            ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(status_jurnal=1).order_by('id')
            for l in ledger_search:
                for t in l.jurnal.tbl_transaksi_set.filter(id_coa=b):
                    akumulasi_debet += t.debet
                    akumulasi_kredit += t.kredit
                    trans.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir': (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)  ,'deskripsi': t.id_coa.deskripsi,\
                        'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,\
                        'id_coa':t.id_coa})
                    start_date = start_date
                    end_date = end_date
                    id_cabang = id_cabang
                    total_debet = akumulasi_debet
                    total_kredit = akumulasi_kredit
                    saldo = (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)
                    tanggal = t.tgl_trans

                    worksheet.write_datetime(row, col , tanggal, date_format )
                    worksheet.write_string(row, col + 1 , t.jurnal.nobukti )
                    worksheet.write_string(row, col + 2 , t.gabung_kode_coa() )
                    worksheet.write_string(row, col + 3 , t.jurnal.diskripsi )
                    worksheet.write_number  (row, col + 4, t.debet, money_format)
                    worksheet.write_number  (row, col + 5, t.kredit, money_format)
                    worksheet.write_number  (row, col + 6,(t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit),money_format)
                    row += 1

        else:
            for l in ledger_search:
                ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(status_jurnal=1).order_by('id')
                for t in l.jurnal.tbl_transaksi_set.filter(id_coa=b).filter(id_cabang=id_cabang):
                    akumulasi_debet += t.debet
                    akumulasi_kredit += t.kredit
                    trans.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir': (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)  ,'deskripsi': t.id_coa.deskripsi,\
                        'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,\
                        'id_coa':t.id_coa})
                    start_date = start_date
                    end_date = end_date
                    id_cabang = id_cabang
                    total_debet = akumulasi_debet
                    total_kredit = akumulasi_kredit
                    saldo = (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)
                    tanggal = t.tgl_trans
                    worksheet.write_datetime(row, col , tanggal, date_format )
                    worksheet.write_string(row, col + 1 , t.jurnal.nobukti )
                    worksheet.write_string(row, col + 2 , t.gabung_kode_coa() )
                    worksheet.write_string(row, col + 3 , t.jurnal.diskripsi )
                    worksheet.write_number  (row, col + 4, t.debet, money_format)
                    worksheet.write_number  (row, col + 5, t.kredit, money_format)
                    worksheet.write_number  (row, col + 6,(t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit),money_format)
                    row += 1
        worksheet.write(row, 0, 'Total', bold)
        worksheet.write(row, 4, '=SUM(E2:E27)', money_format)
        worksheet.write(row, 5, '=SUM(F2:F27)', money_format)
        workbook.close()    
        output.seek(0)    
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=bukubesar_pjb).xlsx"    
        return response
        
    else:
        template='ledger/search/search_buku_besar.html'
        variable = RequestContext(request,{'form':form})
        return render_to_response(template,variable)

def buku_besar_all(request):
    ledger = Tbl_Transaksi.objects.all()
    banyak = ledger.all
    start_date = None
    end_date = None
    id_cabang = None
    akumulasi_debet =0
    akumulasi_kredit = 0
    transaksi =  banyak.im_class(Tbl_Transaksi)
    fil = transaksi.filter(status_jurnal = 1)
    jumlah_debet = sum([n.debet for n in fil])
    jumlah_kredit = sum([n.kredit for n in fil])
    saldo_awal = jumlah_debet - jumlah_kredit
    a = jumlah_debet + jumlah_kredit
    akumulasi_pokok_plafon = 0
    form = Tbl_AkunForm()
    all = []
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET :
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500':
            for (l,k) in AKUN:
                tb = Tbl_Transaksi.objects.filter(id_coa = l ).filter(tgl_trans__range=(start_date,end_date)).filter(status_jurnal =(2))
                akumulasi_debet = 0
                akumulasi_kredit = 0
                for t in tb:
                    if t.id_coa.coa[0:2] == str(20) or t.id_coa.coa[0:2] == str(21) or t.id_coa.coa[0:2] == str(22) or t.id_coa.coa[0:2] == str(23) or t.id_coa.coa[0:2] == str(30) or \
                        t.id_coa.coa[0:2] == str(31) or t.id_coa.coa[0:2] == str(32) or t.id_coa.coa[0:2] == str(33) or t.id_coa.coa[0:2] == str(34) or t.id_coa.coa[0:2] == str(35) or \
                        t.id_coa.coa[0:2] == str(40) or t.id_coa.coa[0:2] == str(41) or t.id_coa.coa[0:2] == str(60) or t.id_coa.coa[0:2] == str(61):
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir':  (t.id_coa.saldo_pjb + akumulasi_kredit - akumulasi_debet)  ,'deskripsi': t.id_coa.deskripsi,\
                        'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,\
                        'id_coa':t.id_coa,'saldo_pjb':t.id_coa.saldo_pjb})# (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)
                    else:
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir':  (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)  ,'deskripsi': t.id_coa.deskripsi,\
                        'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,\
                        'id_coa':t.id_coa,'saldo_pjb':t.id_coa.saldo_pjb})# (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)
        else:
            for (l,k) in AKUN:
                tb = Tbl_Transaksi.objects.filter(id_coa = l ).filter(tgl_trans__range=(start_date,end_date)).\
                    filter(id_cabang=id_cabang).filter(status_jurnal = 2)
                akumulasi_debet = 0
                akumulasi_kredit = 0
                print tb
                for t in tb:
                    if t.id_coa.coa[0:2] == str(20) or t.id_coa.coa[0:2] == str(21) or t.id_coa.coa[0:2] == str(22) or t.id_coa.coa[0:2] == str(23) or t.id_coa.coa[0:2] == str(30) or \
                        t.id_coa.coa[0:2] == str(31) or t.id_coa.coa[0:2] == str(32) or t.id_coa.coa[0:2] == str(33) or t.id_coa.coa[0:2] == str(34) or t.id_coa.coa[0:2] == str(35) or \
                        t.id_coa.coa[0:2] == str(40) or t.id_coa.coa[0:2] == str(41) or t.id_coa.coa[0:2] == str(60) or t.id_coa.coa[0:2] == str(61):
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir':  (t.id_coa.saldo_pjb + akumulasi_kredit - akumulasi_debet)  ,'deskripsi': t.id_coa.deskripsi,\
                        'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,\
                        'id_coa':t.id_coa,'saldo_pjb':t.id_coa.saldo_pjb})# (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)
                    else:
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir':  (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)  ,'deskripsi': t.id_coa.deskripsi,\
                        'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,\
                        'id_coa':t.id_coa,'saldo_pjb':t.id_coa.saldo_pjb})# (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)
        template='ledger/search/search_buku_besar_all.html'
        variable = RequestContext(request,{'ledger':all,'saldo':saldo_awal,'form':form,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang})
        return render_to_response(template,variable)
    
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        
        if id_cabang == '500':
            for (l,k) in AKUN:
                tb = Tbl_Transaksi.objects.filter(id_coa = l ).filter(tgl_trans__range=(start_date,end_date)).filter(status_jurnal= 2)
                akumulasi_debet = 0
                akumulasi_kredit = 0
                for t in tb:
                    if t.id_coa.coa[0:2] == str(20) or t.id_coa.coa[0:2] == str(21) or t.id_coa.coa[0:2] == str(22) or t.id_coa.coa[0:2] == str(23) or t.id_coa.coa[0:2] == str(30) or \
                        t.id_coa.coa[0:2] == str(31) or t.id_coa.coa[0:2] == str(32) or t.id_coa.coa[0:2] == str(33) or t.id_coa.coa[0:2] == str(34) or t.id_coa.coa[0:2] == str(35) or \
                        t.id_coa.coa[0:2] == str(40) or t.id_coa.coa[0:2] == str(41) or t.id_coa.coa[0:2] == str(60) or t.id_coa.coa[0:2] == str(61):
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir':  (t.id_coa.saldo_pjb + akumulasi_kredit - akumulasi_debet)  ,'deskripsi': t.id_coa.deskripsi,\
                        'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,\
                        'id_coa':t.id_coa,'saldo_pjb':t.id_coa.saldo_pjb})# (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)
                    else:
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir':  (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)  ,'deskripsi': t.id_coa.deskripsi,\
                        'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,\
                        'id_coa':t.id_coa,'saldo_pjb':t.id_coa.saldo_pjb})# (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)
        else:
            for (l,k) in AKUN:
                tb = Tbl_Transaksi.objects.filter(id_coa = l).filter(tgl_trans__range=(start_date,end_date))\
                    .filter(id_cabang=id_cabang).filter(status_jurnal=2)
                for t in tb:
                    if t.id_coa.coa[0:2] == str(20) or t.id_coa.coa[0:2] == str(21) or t.id_coa.coa[0:2] == str(22) or t.id_coa.coa[0:2] == str(23) or t.id_coa.coa[0:2] == str(30) or \
                        t.id_coa.coa[0:2] == str(31) or t.id_coa.coa[0:2] == str(32) or t.id_coa.coa[0:2] == str(33) or t.id_coa.coa[0:2] == str(34) or t.id_coa.coa[0:2] == str(35) or \
                        t.id_coa.coa[0:2] == str(40) or t.id_coa.coa[0:2] == str(41) or t.id_coa.coa[0:2] == str(60) or t.id_coa.coa[0:2] == str(61):
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir':  (t.id_coa.saldo_pjb + akumulasi_kredit - akumulasi_debet)  ,'deskripsi': t.id_coa.deskripsi,\
                        'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,\
                        'id_coa':t.id_coa,'saldo_pjb':t.id_coa.saldo_pjb})# (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)
                    else:
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir':  (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)  ,'deskripsi': t.id_coa.deskripsi,\
                        'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,\
                        'id_coa':t.id_coa,'saldo_pjb':t.id_coa.saldo_pjb})# (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)
        template1='ledger/search/cetak_buku_besar_all.html'
        variable = RequestContext(request,{'ledger':all,'saldo':saldo_awal,'form':form,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang})
        return render_to_response(template1,variable)
    
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        
        if id_cabang == '500':
            for (l,k) in AKUN:
                tb = Tbl_Transaksi.objects.filter(id_coa = l ).filter(tgl_trans__range=(start_date,end_date)).filter(status_jurnal=2)
                for t in tb:
                    all.append(t)
        else:
            for (l,k) in AKUN:
                tb = Tbl_Transaksi.objects.filter(id_coa = l ).filter(tgl_trans__range=(start_date,end_date)).filter(id_cabang=id_cabang).\
                    filter(status_jurnal=2)
                for t in tb:
                    all.append(t)
        
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 0})
        money_format = workbook.add_format({'num_format': '#,##0'})
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        worksheet.set_column(0, 0, 10) 
        worksheet.set_column(1, 1, 15)
        worksheet.set_column(2, 2, 11)
        worksheet.set_column(3, 3, 37)
        worksheet.set_column(4, 4, 10)
        worksheet.set_column(5, 5, 10)
        worksheet.set_column(6, 6, 10)
        
        worksheet.write('A1', 'Tanggal', bold)
        worksheet.write('B1', 'Nomor Bukti', bold)
        worksheet.write('C1', 'COA', bold)
        worksheet.write('D1', 'Keterangan', bold)
        worksheet.write('E1', 'Debet', bold)
        worksheet.write('F1', 'Kredit', bold)
        worksheet.write('G1', 'Saldo', bold)        
        row = 1
        col = 0
        for t in all:
            akumulasi_debet += t.debet
            akumulasi_kredit += t.kredit
            worksheet.write_datetime(row, col , t.tgl_trans, date_format )
            worksheet.write_string(row, col + 1 , t.jurnal.nobukti )
            worksheet.write_string(row, col + 2 , t.gabung_kode_coa() )
            worksheet.write_string(row, col + 3 , t.jurnal.diskripsi )
            worksheet.write_number  (row, col + 4, t.debet, money_format)
            worksheet.write_number  (row, col + 5, t.kredit, money_format)
            worksheet.write_number  (row, col + 6,(t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit),money_format)
            row += 1
        worksheet.write(row, 0, 'Total', bold)
        worksheet.write(row, 4, '=SUM(E2:E27)', money_format)
        worksheet.write(row, 5, '=SUM(F2:F27)', money_format)
        workbook.close()    
        output.seek(0)    
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=bukubesar_pjb_all).xlsx"    
        return response
        
    else:
        variables = RequestContext(request, {'form': form,'ag':ledger})
        return render_to_response('ledger/search/search_buku_besar_all.html', variables)
                
def cetak_buku_besar(request):    
    ledger = Tbl_Transaksi.objects.all()
    banyak = ledger.all
    transaksi =  banyak.im_class(Tbl_Transaksi)
    fil = transaksi.filter(status_jurnal = 1)
    jumlah_debet = sum([n.debet for n in fil])
    jumlah_kredit = sum([n.kredit for n in fil])
    saldo_awal = jumlah_debet - jumlah_kredit
    form = Tbl_AkunForm()
    if 'start_date' in request.GET and request.GET['start_date']:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_coa = request.GET['id_coa']
        id_cabang = request.GET['id_cabang']
        ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(id_coa=id_coa).filter(id_cabang=id_cabang).order_by('id')
        trans = []
        for l in ledger_search:
            for t in l.jurnal.tbl_transaksi_set.all():
                trans.append(t)
                
               
    else:
        template = 'ledger/cetak/cetak_buku_besar.html'
        variable = RequestContext(request,{'form':form})
        return render_to_response(template,variable)
    
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=bukubesar.xls' 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("sheet" ) #(id_coa, id_cabang))
    
    row_num = 0
    
    columns = [
        (u"KODE UNIT", 6000),(u"KODE CABANG", 25000),(u"TANGGAL ", 6000),(u"COA", 6000),(u"DESKRIPSI", 6000),(u"DEBET", 6000),
        (u"KREDIT", 6000),                          
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    #font_style = xlwt.XFStyle(num_format_str='YYYY-MM-DD')
    font_style.alignment.wrap = 1
    
    for cetak in ledger_search:
        row_num += 1
        row = [
            cetak.id_unit, cetak.id_cabang,cetak.tgl_trans,cetak.id_coa.coa,cetak.id_coa.deskripsi,cetak.debet,cetak.kredit,                                            
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response
    '''
        
    
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('sheet')
    
    date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
    bold = workbook.add_format({'bold': True})
    money = workbook.add_format({'num_format': '#,###0'})
    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1
    # Write some data headers.
    worksheet.write('A1', 'Nomor', bold)
    worksheet.write('B1', 'Tanggal', bold)
    worksheet.write('C1', 'No Bukti', bold)
    worksheet.write('D1', 'Kode Coa', bold)    
    worksheet.write('E1', 'Nama Coa', bold)
   
    # Some data we want to write to the worksheet.
    #date_time = datetime.date.today()
    #expenses = (
        #['Rent', 1000,date_time],
        #['Gas',   100,date_time],
        #['Food',  300,date_time],
        #['Gym',    50,date_time],
    #)
    a_list = []

    for g in Tbl_Transaksi.objects.all():
        a_list.append({'obj': g})
   
    data = sorted(a_list)
   
    # Start from the first cell below the headers.
    row_num = 1
    col_num = 0
   
    # Iterate over the data and write it out row by row.
    #for nomor, tanggal,nobukti in (data):
    #for i in (data):
        #print i
        #worksheet.write(row, col,id_trans)
        #worksheet.write(row, col + 1, tanggal, money)
        #worksheet.write_datetime(row, col + 2,nobukti, date_format)
        #worksheet.write(i, 0, getattr(row['obj'],'id_unit'))
        #worksheet.write_datetime(i, col + 1, getattr(row['obj'], 'tgl_tran', date_format))
        #row += 1
    for cetak in ledger_search:
        row_num += 1
        row = [
            cetak.id_unit, cetak.id_cabang,cetak.tgl_trans,cetak.id_coa.coa,cetak.id_coa.deskripsi,cetak.debet,cetak.kredit,                                            
        ]
        #for col_num in xrange(len(row)):
            #worksheet.write(row, col_num, row[col_num], font_style)   
    # Write a total using a formula.
    #worksheet.write(row, 0, 'Total',       bold)
    #worksheet.write(row, 1, '=SUM(B2:B5)', money)

    workbook.close()
    filename = 'ExcelReport.xlsx'
    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=bukubesar.xlsx' 
    return response
    '''       


def hapus_jurnal(request,object_id):
    tbl = Tbl_Transaksi.objects.get(id=object_id)   
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Penghapusan Jurnal Berhasil')
    return HttpResponseRedirect(tbl.get_absolute_url_batal_jurnal() )
    
def ledger_show(request, object_id):
    akun = get_object_or_404(Tbl_Akun, pk=object_id)
    variables = RequestContext(request, {'akun': akun})
    return render_to_response('ledger/show.html', variables)
    
def akun_list(request):
    akun_list = Tbl_Akun.objects.all().order_by('coa')
    variables = RequestContext(request, {'object_list': akun_list})
    return render_to_response('akun/list.html', variables)

def add(request,object_id):
    sekarang = datetime.date.today()
    show = Tbl_Transaksi.objects.all().filter(status_jurnal=1).filter(id_cabang=object_id).filter(tgl_trans= sekarang).filter(jenis='GL_GL')
    Tbl_TransaksiFormSet = formset_factory(Tbl_TransaksiForm, extra=1,max_num=1)
    if request.method == 'POST':
        formset = Tbl_TransaksiFormSet(request.POST)
        form = MainJurnalForm(request.POST)
        if formset.is_valid() and form.is_valid():
            nobukti = form.cleaned_data['nobukti']
            diskripsi = form.cleaned_data['diskripsi']
            tgl_trans = form.cleaned_data['tgl_trans']
            status_jurnal = form.cleaned_data['status_jurnal']
            #nilai = form.cleaned_data['nilai']
            jurnal = Jurnal.objects.create(diskripsi=diskripsi,tgl_trans=tgl_trans,nobukti=nobukti,status_jurnal=status_jurnal)
            for itemform in formset.forms:
                id_coa = itemform.cleaned_data['id_coa']
                debet = itemform.cleaned_data['debet']
                kredit = itemform.cleaned_data['kredit']
                gerai = itemform.cleaned_data['gerai']
                #if is_debet  == None:
                    #debet = nilai
                    #kredit = 0
                #else:
                    #debet = 0
                    #kredit = nilai
                debet = debet
                kredit = kredit
                itemjurnal = Tbl_Transaksi.objects.create(id_coa= id_coa,debet=debet,kredit=kredit,tgl_trans=tgl_trans,#datetime.date.today(),
                    jurnal = jurnal,id_product=4,status_jurnal=1,id_cabang=object_id,id_unit=300,jenis='GL_GL',antar_kantor=gerai)
                
            messages.add_message(request, messages.INFO,"Jurnal telah disimpan dengan sukses")
            return HttpResponseRedirect(itemjurnal.get_absolute_url())
        else:
            messages.add_message(request, messages.INFO,"ADA NILAI YANG BELUM ANDA MASUKAN")
        var = {'form': form, 'formset': formset,'show':show}
    else:
        var = {'form': MainJurnalForm(), 'formset': Tbl_TransaksiFormSet(initial= [{"is_debet":True}, {"is_debet":False}]),'show':show}
    variables = RequestContext(request, var)
    return render_to_response('jurnal/add.html', variables)

def add_non_kas(request,object_id):
    sekarang = datetime.date.today()
    show = Tbl_Transaksi.objects.filter(status_jurnal=1).filter(id_cabang=object_id).filter(tgl_trans=sekarang).filter(jenis='GL_GL_NON_KAS')
    Tbl_TransaksiFormSet = formset_factory(Tbl_TransaksiForm, extra=1,max_num=1)
    if request.method == 'POST':
        formset = Tbl_TransaksiFormSet(request.POST)
        form = MainJurnalForm(request.POST)
        if formset.is_valid() and form.is_valid():
            nobukti = form.cleaned_data['nobukti']
            diskripsi = form.cleaned_data['diskripsi']
            tgl_trans = form.cleaned_data['tgl_trans']
            #nilai = form.cleaned_data['nilai']
            jurnal = Jurnal.objects.create(diskripsi=diskripsi,tgl_trans=tgl_trans,nobukti=nobukti)
            for itemform in formset.forms:
                id_coa = itemform.cleaned_data['id_coa']
                debet = itemform.cleaned_data['debet']
                kredit = itemform.cleaned_data['kredit']
		gerai =itemform.cleaned_data['gerai']
                debet = debet
                kredit = kredit
                itemjurnal = Tbl_Transaksi.objects.create(id_coa= id_coa,debet=debet,kredit=kredit,tgl_trans=tgl_trans,#datetime.date.today(),
                    jurnal = jurnal,id_product=4,status_jurnal=1,id_cabang=object_id,id_unit=300,jenis='GL_GL_NON_KAS',antar_kantor=gerai)
                
            messages.add_message(request, messages.INFO,"Jurnal telah disimpan dengan sukses")
            return HttpResponseRedirect(itemjurnal.get_absolute_url_non())
        else:
            messages.add_message(request, messages.INFO,"ADA NILAI YANG BELUM ANDA MASUKAN")
        var = {'form': form, 'formset': formset,'show':show}
    else:
        var = {'form': MainJurnalForm(), 'formset': Tbl_TransaksiFormSet(initial= [{"is_debet":True}, {"is_debet":False}]),'show':show,
               'total_debet': sum([p.debet for p in show]),'total_kredit': sum([p.kredit for p in show])}
    variables = RequestContext(request, var)
    return render_to_response('jurnal/add_non_kas.html', variables)




