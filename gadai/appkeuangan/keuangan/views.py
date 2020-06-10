from django.shortcuts import render_to_response, get_object_or_404,render,redirect
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
import datetime
from gadai.appgadai.jurnal.forms import *
from gadai.appkeuangan.models import *
from gadai.appgadai.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import timedelta 
from gadai.appkeuangan.keuangan.forms import *

def input_posting_akhir_tahun(request,object_id):
    pilih = object_id
    sekarang = datetime.date.today()
    tahun_depan = sekarang.year + 1
    sal = Tbl_TransaksiKeu.objects.filter(id_cabang = pilih,tgl_trans__year = tahun_depan).order_by('id')
    id_awal = sal[0]
    tgl_awal = id_awal.tgl_trans

    po = Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan = "PO",id_cabang = pilih,tgl_trans = tgl_awal)
    pno = Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan = "PNO",id_cabang = pilih,tgl_trans = tgl_awal)
    bo = Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan = "BO",id_cabang = pilih,tgl_trans = tgl_awal)
    bno = Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan = "BNO",id_cabang = pilih,tgl_trans = tgl_awal)

    saldo_po = sum([a.saldo for a in po])
    saldo_pno = sum([a.saldo for a in pno])
    saldo_bo = sum([a.saldo for a in bo])
    saldo_bno = sum([a.saldo for a in bno])

    sal_shu_blom_dibagikan = ( saldo_po + saldo_pno ) - (saldo_bo + saldo_bno)
    
    form = PostingAkhirTahunForm(initial={'tanggal':tgl_awal,'saldo_shu':int(sal_shu_blom_dibagikan)}) 
    template = 'keuangan/input_posting_akhir_tahun.html'
    variable = RequestContext(request, {'form': form,'pilih':pilih})
    return render_to_response(template,variable)

def eksekusi_posting_akhir_tahun(request,object_id):
    pilih = object_id
    sekarang = datetime.date.today()
    tahun_depan = sekarang.year + 1
    sal = Tbl_TransaksiKeu.objects.filter(id_cabang = pilih,tgl_trans__year = tahun_depan).order_by('id')
    id_awal = sal[0]
    tgl_awal = id_awal.tgl_trans

    po = Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan = "PO",id_cabang = pilih,tgl_trans = tgl_awal)
    pno = Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan = "PNO",id_cabang = pilih,tgl_trans = tgl_awal)
    bo = Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan = "BO",id_cabang = pilih,tgl_trans = tgl_awal)
    bno = Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan = "BNO",id_cabang = pilih,tgl_trans = tgl_awal)
    saldo_po = sum([a.saldo for a in po])
    saldo_pno = sum([a.saldo for a in pno])
    saldo_bo = sum([a.saldo for a in bo])
    saldo_bno = sum([a.saldo for a in bno])
    sal_shu_blom_dibagikan = ( saldo_po + saldo_pno ) - (saldo_bo + saldo_bno)

    shu_bagi = Tbl_TransaksiKeu.objects.get(id_coa__coa = "35.03.00",id_cabang = pilih,tgl_trans = tgl_awal)
    shu_bagi.saldo = sal_shu_blom_dibagikan
    shu_bagi.save()

    nol = Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan__in = ("PO","PNO","BO","BNO"),id_cabang = pilih,tgl_trans = tgl_awal)
    nol.update(saldo = 0)
    nol_juga = Tbl_TransaksiKeu.objects.filter(id_coa__coa = "35.04.00",id_cabang = pilih,tgl_trans = tgl_awal)
    nol_juga.update(saldo = 0)
    messages.add_message(request, messages.INFO,'### Posting AKhir Tahun selesai ###.')
    return HttpResponseRedirect('/rkeuangan/posting_akhir_tahun/')


def posting_akhir_tahun(request):
    sekarang = datetime.date.today()
    tahun_depan = sekarang.year + 1
    cabang = Tbl_Cabang.objects.filter(status_aktif = 1)
    tahun_depan = sekarang.year + 1
    sal = Tbl_TransaksiKeu.objects.filter(tgl_trans__year = tahun_depan).count()

    variables = RequestContext(request, {'sekarang':sekarang,'cbg':cabang,'ada':sal})
    return render_to_response('keuangan/show_posting_akhir_tahun.html', variables)

###Akhir Posting Akir tahun
##tes Revisi Posting
def revisiposting(request):
    sekarang = datetime.date.today()
    form = RevisiPostingForm()
    template = 'manop/revisi_posting.html'
    #template = 'kasir/kasir_pelunasan.html'
    variable = RequestContext(request, {'form':form,})
    return render_to_response(template,variable)

def eksekusi_revisiposting(request):
    user = request.user
    if request.method == 'POST':
        f = RevisiPostingForm(request.POST)
        if f.is_valid():
            gerai = f.cleaned_data['gerai']
            tgl_trans = f.cleaned_data['tgl_trans']
            print gerai,tgl_trans
            if gerai == '500' :
                messages.add_message(request, messages.INFO,'### MAAF GABUNGAN DAN PUSAT TIDAK DAPAT DI REVISI ###.')
            else:
                jukeu = JurnalKeuangan.objects.filter(tgl_trans = tgl_trans).filter(kode_cabang =gerai)
                jukeu.delete()
            #Update lagi Transaksi yang telah terposting ke posisi sebelum posting sintaks:
                trans = Tbl_Transaksi.objects.filter(id_cabang =gerai).filter(tgl_trans=tgl_trans).filter(status_posting = 1).filter(posting =2)
                trans.update(status_posting = 1,posting=1)
            #Update Posisi Saldo Yang hari sebelum sekarang jadi psisi kemaren
                aa = Tbl_TransaksiKeu.objects.filter(jenis='SALDOKASGERAI').filter(id_cabang=gerai).filter(status_jurnal = 3).filter(tgl_trans = tgl_trans)
                aa.update(status_jurnal =2)
            #tbl postinggerai dihapus
                a = PostingGerai.objects.filter(kode_cabang = gerai).filter(tanggal= tgl_trans)
                a.delete()
                messages.add_message(request, messages.INFO,'### SILAHKAN POSTING ULANG DI GERAI ###.')
            return HttpResponseRedirect('/')
        else:
            variables = RequestContext(request,{ 'form': form})
            return render_to_response('manop/revisi_posting.html', variables)
    else:
        form  = RevisiPostingForm()
    variables = RequestContext(request, {'form': form,})
    return render_to_response('manop/revisi_posting.html', variables)
##Akhir Revisi Posting


def mastertiket_rak_pusat(request,object_id):
    sekarang = datetime.date.today()  
    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=object_id).filter(status_jurnal=u'2').\
        filter(jenis__in=(u'Pelunasan_kasir_kas_rak',u'Pelunasan_kasir_bank_pusat_rak','GL_GL_RAK_PUSAT_CABANG',u'GL_GL_PENAMBAHAN_PUSAT_BANK',\
            u'GL_GL_PENAMBAHAN_PUSAT_KAS',u'GL_GL_PENGELUARAN_PUSAT_BANK','GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI',\
            u'GL_GL_PENGELUARAN_PUSAT_KAS',u'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI','GL_GL_RAK_PUSAT','GL_GL_PENGEMBALIAN_PUSAT_BANK',\
            'GL_GL_PENGEMBALIAN_PUSAT_BANK_RAK'))  
    template = 'keuangan/mastertiket_rakpusat.html'
    variables = RequestContext(request, {'user':User,'g':gr,'total_debet': sum([p.debet for p in gr]),\
        'total_kredit': sum([p.kredit for p in gr])})
    return render_to_response(template, variables)

def edit_saldo(request,object_id,jurnal):
    post = get_object_or_404(Tbl_TransaksiKeu, id=object_id)
    if request.method == "POST":
        form = TbTransForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/rkeuangan/saldo_gerai/')
    else:
        form = TbTransForm(instance=post)
        form.fields['jurnal'].queryset = JurnalKeuangan.objects.filter(id=jurnal) 
    return render(request, 'keuangan/saldo_edit.html', {'form': form,'id':object_id,'jurnal':jurnal}) 

def create_saldo(request):
    user = request.user
    if request.POST:
        form = Tbl_TransForm(request.POST)
        if form.is_valid():
            tgl_trans = form.cleaned_data['tgl_trans']
            diskripsi = form.cleaned_data['diskripsi']
            kode_cabang = form.cleaned_data['kode_cabang']
            id_coa = form.cleaned_data['id_coa']
            jenis = form.cleaned_data['jenis']
            debet = form.cleaned_data['debet']
            kredit = form.cleaned_data['kredit']
            id_unit = form.cleaned_data['id_unit']
            id_product = form.cleaned_data['id_product']
            status_jurnal = form.cleaned_data['status_jurnal']
            saldo = form.cleaned_data['saldo']
            #jurnal = Jurnal(nobukti='00000',diskripsi=diskripsi,kode_cabang=kode_cabang,tgl_trans=tgl_trans,cu=user,mu=user)
            #jurnal.save()
            #transaksi = Tbl_Transaksi(id_coa=id_coa,jurnal=jurnal,no_trans = 000,jenis=jenis,debet=0,kredit=0,id_cabang=kode_cabang,\
                #id_unit=id_unit,id_product=id_product,status_jurnal=status_jurnal,tgl_trans=tgl_trans,deskripsi=diskripsi,saldo=saldo)
            #transaksi.save()

            jurnalkeu = JurnalKeuangan(nobukti='00000',diskripsi=diskripsi,kode_cabang=kode_cabang.kode_cabang,tgl_trans=tgl_trans,cu=user,mu=user)
            jurnalkeu.save()
            transaksikeu = Tbl_TransaksiKeu(id_coa=id_coa,jurnal=jurnalkeu,no_trans = 000,jenis=jenis,debet=0,kredit=0,id_cabang=kode_cabang.kode_cabang,\
                id_unit=id_unit,id_product=id_product,status_jurnal=status_jurnal,tgl_trans=tgl_trans,deskripsi=diskripsi,saldo=saldo)
            transaksikeu.save()

            messages.add_message(request, messages.INFO,"SALDO TERSIMPAN")
            return HttpResponseRedirect('/rkeuangan/saldo_gerai/')
    else:
        form = Tbl_TransForm()
    variable = RequestContext(request, {'form': form})
    return render_to_response('keuangan/create_saldo.html',variable)

def saldo_gerai(request):
    sekarang = datetime.date.today()   
    trans = []    
    form = Tbl_AkunForm()
    if 'start_date' in request.GET and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        akumulasi_debet =0
        akumulasi_kredit = 0
        start_date = start_date
        id_cabang = id_cabang
        if id_cabang == '500':
            ledger_search = Tbl_TransaksiKeu.objects.filter(tgl_trans=(start_date)).filter(status_jurnal__in=('2','3')).filter(jenis__in = ('SALDOKASGERAI','SALDOBANKGERAI')).exclude(id_coa__view_unit__in =('100','200')).order_by('id')
            for t in ledger_search:
                trans.append({'t':t, 'deskripsi': t.id_coa.deskripsi,'saldo':t.saldo,
                    'diskripsi' : t.jurnal.diskripsi, 'coa':t.id_coa.coa, 'nobukti': t.jurnal.nobukti,\
                     'tgl_trans':t.tgl_trans,'id_coa':t.id_coa})
                start_date = start_date
                id_cabang = id_cabang
                total_debet = akumulasi_debet
                total_kredit = akumulasi_kredit
        else:
            ledger_search = Tbl_TransaksiKeu.objects.filter(tgl_trans=(start_date)).filter(id_cabang=id_cabang).filter(status_jurnal__in=('2','3')).\
                filter(jenis__in = ('SALDOKASGERAI','SALDOBANKGERAI')).exclude(id_coa__view_unit__in =('100','200'))
            for t in ledger_search:
                trans.append({'t':t, 'deskripsi': t.id_coa.deskripsi,'saldo':t.saldo,'id':t.jurnal.id,'id_tt':t.id,
                    'diskripsi' : t.jurnal.diskripsi,  'coa':t.id_coa.coa, 'nobukti': t.jurnal.nobukti,\
                     'tgl_trans':t.tgl_trans,'id_coa':t.id_coa})

        start_date = start_date
        id_cabang = id_cabang
        total_debet = akumulasi_debet
        total_kredit = akumulasi_kredit

        template='keuangan/saldo_gerai.html'
        variable = RequestContext(request,{'form':form,'ledger_search':trans,'id_cabang':id_cabang,'start_date':start_date})
        return render_to_response(template,variable)
    else:
        template='keuangan/saldo_gerai.html'
        variable = RequestContext(request,{'form':form})
        return render_to_response(template,variable)

def posting_tanggal(request,object_id):
    pilih = object_id
    sekarang = datetime.date.today()
    relatif = relativedelta(days=1)
    tgl_sekarang = sekarang 
    sbl_tanggal = sekarang - relatif
    form = KeuanganPusatForm(initial={'tanggal':tgl_sekarang,'kode_cabang':(pilih)}) 
    template = 'keuangan/posting_tanggal.html'
    variable = RequestContext(request, {'form': form,'pilih':pilih})
    return render_to_response(template,variable)

def tanggal_posting(request,object_id):
    user = request.user
    kode_cabang = object_id
    sekarang = datetime.date.today()
    if request.method == 'POST':
        form = KeuanganPusatForm(request.POST)
        if form.is_valid():
            tanggal = form.cleaned_data['tanggal']
            kode_cabang = form.cleaned_data['kode_cabang']
            saldo = form.cleaned_data['saldo']
            note = form.cleaned_data['note']
            tanggal_sbl = form.cleaned_data['tanggal_sbl']
            simpan = KeuanganPusat(tanggal_sbl = tanggal_sbl, tanggal = tanggal, saldo = saldo, kode_cabang = kode_cabang, note = note,
                cu = request.user, mu=request.user)
            simpan.save()
            jurnal_awalc = Jurnal.objects.filter(tgl_trans=simpan.tanggal_sbl).filter(kode_cabang=simpan.kode_cabang).exclude(nobukti='00000')
            total_hari = (simpan.tanggal - simpan.tanggal_sbl).days + 1
            saldo = Tbl_Transaksi.objects.filter(id_cabang = simpan.kode_cabang).filter(debet = 0).filter(kredit = 0).\
                filter(jenis='SALDOKASGERAI').filter(tgl_trans=simpan.tanggal_sbl)
            #akun = Tbl_Akun.objects.all()

            akun = Tbl_Akun.objects.all()#filter(view_unit__in = (300,0,1))
            tanggal_sbl = simpan.tanggal_sbl #simpan.tanggal #datetime.date.today()
            relatif = relativedelta(days=1)
            tgl_posting = tanggal + relatif

            pendapatan = Tbl_Akun.objects.get(pk = 406)
            pendapatan_non = Tbl_Akun.objects.get(pk = 540)
            beban = Tbl_Akun.objects.get(pk = 449)
            beban_non = Tbl_Akun.objects.get(pk = 547)
            id_cabang = simpan.kode_cabang

            saldo_shu = ((pendapatan.pdp_lb_rugi_saldo_gabungan_posting(start_date=tanggal_sbl,id_cabang=id_cabang) +\
            pendapatan_non.pdp_non_lb_rugi_saldo_gabungan_posting( start_date=tanggal_sbl,end_date = tanggal_sbl,id_cabang=id_cabang)) +\
            pendapatan_non.pdp_non_lb_rugi_kredit_gabungan_posting(start_date=tanggal_sbl, end_date=tanggal_sbl,id_cabang=id_cabang) + \
            pendapatan.pdp_lb_rugi_debet_gabungan_posting(start_date=tanggal_sbl, end_date=tanggal_sbl,id_cabang=id_cabang) +\
            (pendapatan.pdp_lb_rugi_kredit_gabungan_posting(start_date=tanggal_sbl,end_date = tanggal_sbl,id_cabang=id_cabang) +\
            pendapatan_non.pdp_non_lb_rugi_debet_gabungan_posting(start_date=tanggal_sbl,end_date = tanggal_sbl,id_cabang=id_cabang))) -\
            ((beban.beban_lb_rugi_saldo_gabungan_posting(start_date=tanggal_sbl,id_cabang=id_cabang) +\
            beban_non.pdp_non_lb_rugi_saldo_gabungan_posting( start_date=tanggal_sbl,end_date = tanggal_sbl,id_cabang=id_cabang)) -\
            (beban.beban_lb_rugi_kredit_gabungan_posting(start_date=tanggal_sbl,end_date = tanggal_sbl,id_cabang=id_cabang) +\
            beban_non.beban_non_lb_rugi_kredit_gabungan_posting(start_date=tanggal_sbl,end_date= tanggal_sbl,id_cabang=id_cabang)) +\
            (beban.beban_lb_rugi_debet_gabungan_posting(start_date=tanggal_sbl,end_date = tanggal_sbl,id_cabang=id_cabang) +\
            beban_non.beban_non_lb_rugi_debet_gabungan_posting(start_date=tanggal_sbl,end_date=tanggal_sbl,id_cabang=id_cabang)))

            for ls in akun:
                aa = Tbl_TransaksiKeu.objects.filter(id_coa = ls.id).filter(jenis='SALDOKASGERAI').filter(id_cabang=kode_cabang).filter(status_jurnal = 2)
                sasa = sum([b.saldo for b in aa])
                tbl = Tbl_Transaksi.objects.filter(id_coa = ls.id).filter(tgl_trans=tanggal_sbl).filter(id_cabang=kode_cabang)
                akumulasi_debet = sum([b.debet for b in tbl])
                akumulasi_kredit = sum ([b.kredit for b in tbl])
                tes_saldo = sasa + akumulasi_debet - akumulasi_kredit
                tes_saldo1 = sasa + akumulasi_kredit - akumulasi_debet

                jurnalk = JurnalKeuangan(nobukti ='00000',tgl_trans= sekarang,kode_cabang=simpan.kode_cabang,cu=user,\
                mu= user,diskripsi='SALDOAWAL')
                jurnalk.save()

                if ls.coa == '35.04.00':
                    tblk = Tbl_TransaksiKeu(debet=0,kredit=0,jurnal=jurnalk,tgl_trans= tgl_posting,id_coa=ls,jenis='SALDOKASGERAI',\
                    id_cabang=simpan.kode_cabang,id_unit=300,id_product=4,status_jurnal=2,saldo = saldo_shu)
                    tblk.save()
 
                elif ls.coa[:1] == '1' or ls.coa[:1] == '5' or ls.coa[:1] == '7':
                    tblk = Tbl_TransaksiKeu(debet=0,kredit=0,jurnal=jurnalk,tgl_trans= tgl_posting,id_coa=ls,jenis='SALDOKASGERAI',\
                    id_cabang=simpan.kode_cabang,id_unit=300,id_product=4,status_jurnal=2,saldo = tes_saldo)
                    tblk.save()
                elif ls.coa[:1] == '2' or ls.coa[:1] == '3' or ls.coa[:1] == '4' or ls.coa[:1] == '6':
                    tblk = Tbl_TransaksiKeu(debet=0,kredit=0,jurnal=jurnalk,tgl_trans= tgl_posting,id_coa=ls,jenis='SALDOKASGERAI',\
                    id_cabang=simpan.kode_cabang,id_unit=300,id_product=4,status_jurnal=2,saldo = tes_saldo1)
                    tblk.save()

                bb = Tbl_TransaksiKeu.objects.filter(id_coa = ls.id).filter(jenis='SALDOKASGERAI').filter(id_cabang=kode_cabang).filter(status_jurnal = 2).filter(tgl_trans__lt = tgl_posting)
                bb.update(status_jurnal =3)
                tbl.update(posting = 2)
                bray_posting = PostingGerai.objects.filter(kode_cabang=simpan.kode_cabang,tanggal =sekarang)
                bray_posting.update(status_posting_pusat =1)
        messages.add_message(request, messages.INFO,"JURNAL POSTING GERAI OK")
        return HttpResponseRedirect('/rkeuangan/posting_gerai_count/')
    else:
        form = PostingTglForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('biaya/addbiayapusat.html', variables)

def posting_kas(request):
    sekarang = datetime.date.today()
    besok = sekarang + timedelta(days=1)
    for i in request.POST.getlist('id_pilih'):
        cabang = Tbl_Cabang.objects.get(kode_cabang = (i))
        pendapatan_kredit = sum([a.pendapatan_kredit for a in Jurnal.objects.filter(tgl_trans =sekarang)])
        pendapatan_kredit_filter = sum([a.pendapatan_kredit_filter for a in Jurnal.objects.filter(tgl_trans =sekarang)])
        pengeluaran_debet = sum([a.pengeluaran_debet for a in Jurnal.objects.filter(tgl_trans =sekarang)])
        pengeluaran_kredit = sum([a.pengeluaran_kredit for a in Jurnal.objects.filter(tgl_trans =sekarang)])
        setoran_saldo = sum([a.setoran_saldo for a in Jurnal.objects.filter(tgl_trans =sekarang)])
        hitung_saldo = ((pendapatan_kredit_filter + pendapatan_kredit) - (pengeluaran_debet + pengeluaran_kredit)) - (setoran_saldo)
        jurnal = Jurnal(diskripsi = 'SALDO AWAL',tgl_trans = besok,kode_cabang = i,nobukti ='00000')
        jurnal.save()
        coa_kas = Tbl_Akun.objects.filter(kode_cabang=i).filter(coa__contains= '11.01').filter(view_unit = 300)
        for b in coa_kas:
            kode_coa = b
            saldo_hitung = Tbl_Transaksi(jurnal = jurnal,id_coa = kode_coa,jenis ='SALDOAWAL',tgl_trans = besok,status_jurnal = 0,
                id_product =300,id_unit = 2,kredit=0,debet=0,saldo = hitung_saldo,id_cabang = 0)
            saldo_hitung.save()
        tsk_jurnal = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(status_jurnal = 2)
        for transaksi in tsk_jurnal:
            transaksi1 = Jurnal(diskripsi = 'SALDOCOA',tgl_trans = sekarang,kode_cabang = i,nobukti ='11111')            
            transaksi1.save()
            transaksi2 = Tbl_Transaksi(jurnal = transaksi1,id_coa = transaksi.id_coa,jenis ='SALDOCOA',tgl_trans = (sekarang ),status_jurnal = 0,
                id_product =400,id_unit = 300,kredit=0,debet=0,saldo = hitung_saldo,id_cabang = i)            
            transaksi2.save()
            messages.add_message(request, messages.INFO,' POSTING TRANSAKSI JURNAL BERHASIL')
        cari = Tbl_Transaksi.objects.filter(jurnal__kode_cabang=cabang.kode_cabang).filter(tgl_trans =sekarang)
        cari.update(status_jurnal = 3,status_posting = 2)
    return HttpResponseRedirect('/rkeuangan/posting_gerai_count/')

def cari_post(request):
    akad = Tbl_Transaksi.objects.all()
    template='keuangan/cari_posting.html'
    variable = RequestContext(request,{'akad': akad})
    return render_to_response(template,variable)

def search_gerai_post(request):
    tanggal=request.GET['tanggal']
    try:
        jurnal=Tbl_Transaksi.objects.filter(tanggal=(tanggal))
        return HttpResponseRedirect("/rkeuangan/%s/posting_gerai_tanggal/" % jurnal.id)
    except:
        messages.add_message(request, messages.INFO,'Tanggal sudah di posting')
        return HttpResponseRedirect("/rkeuangan/search_gerai_post/")
    
def posting_gerai_tanggal(request,tanggal):
    sekarang = datetime.date.today()
    cabang = Tbl_Cabang.objects.filter(status_aktif = 1)
    posting = Tbl_Transaksi.objects.filter(tgl_trans = sekarang).exclude(status_posting =7).filter(id_cabang__in= cabang).filter(tgl_trans=sekarang)
    cbg = []
    for row in cabang:
        transaksi = sum([a.cari_pencairan for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)])
        transaksi_nonfilter = sum([a.cari_pencairan_nonfilter for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)])
        transaksi_nonfilter_debet = sum([a.cari_pencairan_nonfilter_debet for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).\
            filter(tgl_trans=sekarang)])
        ###### BATAS PINJAMAN
        biaya = sum([a.cari_biaya_debet for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)])
        pendapatan = sum([a.transaksi_pdpt_geraifilter for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)])
        pendapatan_jual = sum([a.transaksi_penjualan_gerai for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)])
        #### SALDO KAS
        pendapatan_kredit = sum([a.pendapatan_kredit for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)])
        pendapatan_kredit_filter = sum([a.pendapatan_kredit_filter for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).\
             filter(tgl_trans=sekarang)])
        pengeluaran_debet = sum([a.pengeluaran_debet for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)])
        pengeluaran_kredit = sum([a.pengeluaran_kredit for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)])
        status_post = [a.tot_trans_jurnal for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)]
        post =sum(status_post)
        ter_post = [a.status_posting for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)]
        sts_post = sum(ter_post)
        cbg.append({
            'coa': Tbl_Transaksi.objects.filter(tgl_trans = sekarang).exclude(status_posting =7).filter(id_coa_id__kode_cabang= row.kode_cabang),
            'cabang': row.nama_cabang,'total_pinjaman':(transaksi + transaksi_nonfilter + transaksi_nonfilter_debet),'total_biaya':biaya,
            'total_pendapatan':(pendapatan + pendapatan_jual),'postting':(post),'sts_post':(sts_post),'kode_cabang':row.kode_cabang,
            'saldo_kas': (pendapatan_kredit_filter + pendapatan_kredit) - (pengeluaran_debet + pengeluaran_kredit),
             })
    variables = RequestContext(request, {'posting':posting,'sekarang':sekarang,'cbg':cbg,})
    return render_to_response('keuangan/posting_gerai_tanggal.html', variables)

'''
def posting_gerai_count(request):
    sekarang = datetime.date.today()
    cabang = Tbl_Cabang.objects.all()
    posting = Tbl_Transaksi.objects.filter(tgl_trans = sekarang).exclude(status_posting =7).filter(id_cabang__in= cabang).filter(tgl_trans=sekarang)
    cbg = []
    for row in cabang:
        transaksi = sum([a.cari_pencairan for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)])
        transaksi_nonfilter = sum([a.cari_pencairan_nonfilter for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)])
        transaksi_nonfilter_debet = sum([a.cari_pencairan_nonfilter_debet for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).\
            filter(tgl_trans=sekarang)])
        ###### BATAS PINJAMAN
        biaya = sum([a.cari_biaya_debet for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)])
        pendapatan = sum([a.transaksi_pdpt_geraifilter for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)])
        pendapatan_jual = sum([a.transaksi_penjualan_gerai for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)])
        #### SALDO KAS
        pendapatan_kredit = sum([a.pendapatan_kredit for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)])
        pendapatan_kredit_filter = sum([a.pendapatan_kredit_filter for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).\
             filter(tgl_trans=sekarang)])
        pengeluaran_debet = sum([a.pengeluaran_debet for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)])
        pengeluaran_kredit = sum([a.pengeluaran_kredit for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)])
        status_post = [a.tot_trans_jurnal for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)]
        post =sum(status_post)
        ter_post = [a.status_posting for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)]
        sts_post = sum(ter_post)
        cbg.append({
            'coa': Tbl_Transaksi.objects.filter(tgl_trans = sekarang).exclude(status_posting =7).filter(id_coa_id__kode_cabang= row.kode_cabang),
            'cabang': row.nama_cabang,'total_pinjaman':(transaksi + transaksi_nonfilter + transaksi_nonfilter_debet),'total_biaya':biaya,
            'total_pendapatan':(pendapatan + pendapatan_jual),'postting':(post),'sts_post':(sts_post),'kode_cabang':row.kode_cabang,
            'saldo_kas': (pendapatan_kredit_filter + pendapatan_kredit) - (pengeluaran_debet + pengeluaran_kredit),
             })
    variables = RequestContext(request, {'posting':posting,'sekarang':sekarang,'cbg':cbg,})
    return render_to_response('keuangan/posting_count_gerai.html', variables)
'''
def posting_gerai_count(request):
    sekarang = datetime.date.today()
    cabang = Tbl_Cabang.objects.filter(status_aktif = 1)
    cbg = []
    for row in cabang:
        bray_posting = PostingGerai.objects.filter(kode_cabang=row.kode_cabang,tanggal =sekarang,status_posting_pusat = None)
        tes_posting = bray_posting.count()
        status_post = [a.tot_trans_jurnal for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)]
        post =sum(status_post)
        #poston = [a.postingon for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)]
        postoff = [a.postingoff for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)]
        #ter_post = [a.status_posting for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang).filter(tgl_trans=sekarang)]
        #sts_post = sum(ter_post)
        #postingon = sum(poston)
        postingoff = sum(postoff)
        #cbg.append({'tes_posting':tes_posting,'cabang': row.nama_cabang,'postting':(post),'sts_post':(sts_post),\
            #'kode_cabang':row.kode_cabang,'posting_on':postingon,'posting_off':postingoff})
        cbg.append({'tes_posting':tes_posting,'cabang': row.nama_cabang,'postting':(post),'kode_cabang':row.kode_cabang,\
            'posting_off':postingoff})
    variables = RequestContext(request, {'tes_posting':tes_posting,'sekarang':sekarang,'cbg':cbg,})
    return render_to_response('keuangan/posting_count_gerai.html', variables)


def posisi_kas(request):
    skr = datetime.date.today()
    cabang = Tbl_Cabang.objects.all()
    cbg =[]
    for row in cabang:
        s_awal = sum([a.saldo_sekarang for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang)])
        pendapatan_kredit = sum([a.pendapatan_kredit for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang)])### PENGELUARAN kredit
        pendapatan_kredit_filter = sum([a.pendapatan_kredit_filter for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang)])### kredit filter
        pengeluaran_debet = sum([a.pengeluaran_debet for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang)])### PENGELUARAN DEBET
        pengeluaran_kredit = sum([a.pengeluaran_kredit for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang)])### PENGELUARAN DEBET
        setoran_saldo = sum([a.setoran_saldo for a in Jurnal.objects.filter(kode_cabang=row.kode_cabang)])### PENGELUARAN DEBET
        cbg.append({'cabang':row.nama_cabang,'pendapatan':(pendapatan_kredit_filter + pendapatan_kredit),
        'pengeluaran': (pengeluaran_debet + pengeluaran_kredit),'saldo_awal':s_awal,
        'saldo_akhir': ( s_awal  + pendapatan_kredit_filter + pendapatan_kredit) - (pengeluaran_debet + pengeluaran_kredit),
        'saldo_yg_disetorkan':(setoran_saldo),
        'saldo_gerai':((s_awal + pendapatan_kredit_filter + pendapatan_kredit) - (pengeluaran_debet + pengeluaran_kredit)) - (setoran_saldo),
        })    
    variables = RequestContext(request, {'list':cbg})
    return render_to_response('keuangan/posisi_kas.html', variables)

'''
def antar_bank_aktiva(request,object_id):
    saldo_awal = 0
    sekarang = datetime.date.today()
    coa = dict([[k, 0] for k,v in COA_BANK])
    balik = dict([[k, 0] for k,v in ID_BALIK])
    tbl = Tbl_Cabang.objects.filter(kode_unit = 300)
    jrn_pendapatan = Tbl_Transaksi.objects.filter(id_cabang = object_id).filter(debet__gt =0).filter(tgl_trans = sekarang).\
        filter(id_coa_id__in=coa).filter(jenis__in=('GL_GL_PUSAT_BANK','AYDA_PUSAT_BANK','GL_GL_PUSAT'))
    jrn_pengeluaran = Tbl_Transaksi.objects.filter(id_cabang=object_id).filter(kredit__gt =0).filter(tgl_trans= sekarang).\
        filter(id_coa_id__in=coa).filter(jenis__in=('GL_GL_PUSAT','AYDA_PUSAT_BANK'))

    pendapatan_jakarta = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju=301).filter(debet__gt =0).filter(id_coa_id =132).\
        filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)
    pengeluaran_jakarta = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju=301).filter(kredit__gt =0).filter(id_coa_id =(132)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)

    pendapatan_suci = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(debet__gt =0).filter(id_cabang_tuju=302).filter(id_coa_id__in =(4,132)).\
        filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)
    pengeluaran_suci = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(kredit__gt =0).filter(id_cabang_tuju=302).filter(id_coa_id =(132)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)

    pendapatan_du = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju=303).filter(debet__gt =0).filter(id_coa_id__in =(4,132)).\
        filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)
    pengeluaran_du = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju=303).filter(kredit__gt =0).filter(id_coa_id =(132)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)

    pendapatan_blbr = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju=304).filter(debet__gt =0).filter(id_coa_id__in =(4,132)).\
        filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)
    pengeluaran_blbr = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju=304).filter(kredit__gt =0).filter(id_coa_id =(132)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)

    pendapatan_gh = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju=306).filter(debet__gt =0).filter(id_coa_id__in =(4,132)).\
        filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)
    pengeluaran_gh = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju=306).filter(kredit__gt =0).filter(id_coa_id =(132)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)

    pendapatan_kopo = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju=307).filter(debet__gt =0).filter(id_coa_id__in =(4,132)).\
        filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)
    pengeluaran_kopo = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju=307).filter(kredit__gt =0).filter(id_coa_id =(132)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)

    pendapatan_cibiru = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju=308).filter(debet__gt =0).filter(id_coa_id__in =(4,132)).\
        filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)
    pengeluaran_cibiru = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju=308).filter(kredit__gt =0).filter(id_coa_id =(132)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)

    pendapatan_cipacing = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju=309).filter(debet__gt =0).filter(id_coa_id__in =(4,132)).\
        filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)
    pengeluaran_cipacing = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju=309).filter(kredit__gt =0).filter(id_coa_id =(132)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)

    pendapatan_jtngr = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju=310).filter(debet__gt =0).filter(id_coa_id__in =(4,132)).\
        filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)
    pengeluaran_jtngr = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju=310).filter(kredit__gt =0).filter(id_coa_id =(132)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)

    pendapatan_cimahi = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju=311).filter(debet__gt =0).filter(id_coa_id__in =(4,132)).\
        filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)
    pengeluaran_cimahi = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju=311).filter(kredit__gt =0).filter(id_coa_id =(132)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)

    pendapatan_buahbatu = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju=312).filter(debet__gt =0).filter(id_coa_id__in =(4,132)).\
        filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)
    pengeluaran_buahbatu = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju= 312).filter(kredit__gt =0).filter(id_coa_id =(132)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)

    pendapatan_marnat = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju= 315).filter(debet__gt =0).filter(id_coa_id__in =(4,132)).\
        filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)
    pengeluaran_marnat = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju= 315).filter(kredit__gt =0).filter(id_coa_id =(132)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)

    pendapatan_cirebon = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju= 317).filter(debet__gt =0).filter(id_coa_id__in =(4,132)).\
        filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)
    pengeluaran_cirebon = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju= 317).filter(kredit__gt =0).filter(id_coa_id =(132)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)

    pendapatan_cimbuleuit = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju= 319).filter(debet__gt =0).filter(id_coa_id__in =(4,132)).\
        filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)
    pengeluaran_cimbuleuit = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju= 319).filter(kredit__gt =0).filter(id_coa_id =(132)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)

    pendapatan_ujungberung = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju= 320).filter(debet__gt =0).filter(id_coa_id__in =(4,132)).\
        filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)
    pengeluaran_ujungberung = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju= 320).filter(kredit__gt =0).filter(id_coa_id =(132)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)

    pendapatan_ciwastra = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju= 321).filter(debet__gt =0).filter(id_coa_id__in =(4,132)).\
        filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)
    pengeluaran_ciwastra = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju= 321).filter(kredit__gt =0).filter(id_coa_id =(132)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)

    pendapatan_bojongsoang = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju= 322).filter(debet__gt =0).filter(id_coa_id__in =(4,132)).\
        filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)
    pengeluaran_bojongsoang = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(id_cabang_tuju= 322).filter(kredit__gt =0).filter(id_coa_id =(132)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)

    #pdp_all_debet = Tbl_Transaksi.objects.filter(id_coa_id=(4)).filter(id_cabang_tuju__in=balik).filter(jenis='GL_GL_PENAMBAHAN_PUSAT_BANK').\
        #filter(debet__gt= 0).filter(tgl_trans= sekarang)
    pdp_all_debet = Tbl_Transaksi.objects.filter(jenis__in=('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(debet__gt= 0).filter(tgl_trans= sekarang)
    #pdp_all_kredit = Tbl_Transaksi.objects.filter(id_coa_id=(132)).filter(id_cabang_tuju__in=balik).filter(jenis='GL_GL_PENGELUARAN_PUSAT_BANK').\
        #filter(kredit__gt =0).filter(tgl_trans= sekarang)
    pdp_all_kredit = Tbl_Transaksi.objects.filter(jenis='GL_GL_PENGELUARAN_PUSAT_BANK').filter(kredit__gt =0).filter(tgl_trans= sekarang)
    variables = RequestContext(request, {
        'jrn_pendapatan':jrn_pendapatan,'jrn_pengeluaran':jrn_pengeluaran,
        'kas_debit_jkt':sum([p.debet for p in pendapatan_jakarta]),'kas_kredit_jkt':sum([p.kredit for p in pengeluaran_jakarta]),
        'kas_debit_suci':sum([p.debet for p in pendapatan_suci]),'kas_kredit_suci':sum([p.kredit for p in pengeluaran_suci]),
        'kas_debit_du':sum([p.debet for p in pendapatan_du]),'kas_kredit_du':sum([p.kredit for p in pengeluaran_du]),
        'kas_debit_blbr':sum([p.debet for p in pendapatan_blbr]),'kas_kredit_blbr':sum([p.kredit for p in pengeluaran_blbr]),
        'kas_debit_gh':sum([p.debet for p in pendapatan_gh]),'kas_kredit_gh':sum([p.kredit for p in pengeluaran_gh]),
        'kas_debit_kopo':sum([p.debet for p in pendapatan_kopo]),'kas_kredit_kopo':sum([p.kredit for p in pengeluaran_kopo]),
        'kas_debit_cibiru':sum([p.debet for p in pendapatan_cibiru]),'kas_kredit_cibiru':sum([p.kredit for p in pengeluaran_cibiru]),
        'kas_debit_cipacing':sum([p.debet for p in pendapatan_cipacing]),'kas_kredit_cipacing':sum([p.kredit for p in pengeluaran_cipacing]),
        'kas_debit_jtngr':sum([p.debet for p in pendapatan_jtngr]),'kas_kredit_jtngr':sum([p.kredit for p in pengeluaran_jtngr]),
        'kas_debit_cimahi':sum([p.debet for p in pendapatan_cimahi]),'kas_kredit_cimahi':sum([p.kredit for p in pengeluaran_cimahi]),
        'kas_debit_buahbatu':sum([p.debet for p in pendapatan_buahbatu]),'kas_kredit_buahbatu':sum([p.kredit for p in pengeluaran_buahbatu]),
        'kas_debit_marnat':sum([p.debet for p in pendapatan_marnat]),'kas_kredit_marnat':sum([p.kredit for p in pengeluaran_marnat]),
        'kas_debit_cirebon':sum([p.debet for p in pendapatan_cirebon]),'kas_kredit_cirebon':sum([p.kredit for p in pengeluaran_cirebon]),
        'kas_debit_cimbuleuit':sum([p.debet for p in pendapatan_cimbuleuit]),'kas_kredit_cimbuleuit':sum([p.kredit for p in pengeluaran_cimbuleuit]),
        'kas_debit_ujungberung':sum([p.debet for p in pendapatan_ujungberung]),
        'kas_kredit_ujungberung':sum([p.kredit for p in pengeluaran_ujungberung]),
        'kas_debit_ciwastra':sum([p.debet for p in pendapatan_ciwastra]),'kas_kredit_ciwastra':sum([p.kredit for p in pengeluaran_ciwastra]),
        'kas_debit_bojongsoang':sum([p.debet for p in pendapatan_bojongsoang]),
        'kas_kredit_bojongsoang':sum([p.kredit for p in pengeluaran_bojongsoang]),'pendapatan': (sum([p.debet for p in pdp_all_debet])),
        'j_pendapatan':(sum([p.debet for p in jrn_pendapatan])),'j_pengeluaran' : (sum([p.kredit for p in jrn_pengeluaran])),
        'pengeluaran':(sum([p.kredit for p in pdp_all_kredit])),'saldo_awal_bank':saldo_awal,
        'saldo_akhir_bank':((sum([p.debet for p in pdp_all_debet])) - (sum([p.kredit for p in pdp_all_kredit]))) +\
            ((sum([p.debet for p in jrn_pendapatan])) - (sum([p.kredit for p in jrn_pengeluaran]))),
         })
    return render_to_response('jurnal/laporan_antar_bank_aktiva.html', variables)
'''

def antar_bank_aktiva(request, object_id):
    gr = Tbl_Cabang.objects.filter(status_aktif = 1)
    sekarang = datetime.date.today()
    
    saldo_awal_tbl = Tbl_TransaksiKeu.objects.filter(id_coa__coa= '11.05.01').filter(id_cabang = '300').filter(tgl_trans = datetime.date.today())
    saldo_awal = sum([a.saldo for a in saldo_awal_tbl])
    coa = dict([[k, 0] for k,v in COA_BANK])
    balik = dict([[k, 0] for k,v in ID_BALIK])
    tbl = Tbl_Cabang.objects.filter(kode_unit = 300)
    jrn_pendapatan = Tbl_Transaksi.objects.filter(id_cabang = object_id).filter(debet__gt =0).filter(tgl_trans = sekarang).filter(id_coa__coa__startswith='11.05').filter(jenis__in=('GL_GL_PUSAT_BANK','AYDA_PUSAT_BANK','GL_GL_PUSAT'))
    jrn_pengeluaran = Tbl_Transaksi.objects.filter(id_cabang=object_id).filter(kredit__gt =0).filter(tgl_trans= sekarang).filter(id_coa__coa__startswith='11.05').filter(jenis__in=('GL_GL_PUSAT','AYDA_PUSAT_BANK'))
    pengeluaran_1 = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(kredit__gt =0).filter(id_coa_id =(132)).filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_BANK').filter(tgl_trans= sekarang)
    pendapatan_1 = Tbl_Transaksi.objects.filter(id_cabang= 300).filter(debet__gt =0).filter(id_coa_id__in =(4,132)).filter(jenis__in = ('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(tgl_trans= sekarang)


    pdp_all_debet = Tbl_Transaksi.objects.filter(jenis__in=('GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_RAK_PUSAT')).filter(debet__gt= 0).filter(tgl_trans= sekarang)
    pdp_all_kredit = Tbl_Transaksi.objects.filter(jenis='GL_GL_PENGELUARAN_PUSAT_BANK').filter(kredit__gt =0).filter(tgl_trans= sekarang)
    template = 'jurnal/laporan_antar_bank_aktiva.html'
    variables = RequestContext(request, {
        'gr':gr,'saldo_awal_bank':saldo_awal,
        'j_pendapatan':(sum([p.debet for p in jrn_pendapatan])),'j_pengeluaran' : (sum([p.kredit for p in jrn_pengeluaran])),
        'jrn_pendapatan':jrn_pendapatan,'jrn_pengeluaran':jrn_pengeluaran,
        'total_penerimaan': sum([a.debet for a in pendapatan_1]),
        'total_pengeluaran': sum([a.kredit for a in pengeluaran_1]),
        'saldo_akhir_bank':saldo_awal + ((sum([p.debet for p in pdp_all_debet])) - (sum([p.kredit for p in pdp_all_kredit]))) +\
            ((sum([p.debet for p in jrn_pendapatan])) - (sum([p.kredit for p in jrn_pengeluaran]))),
    })
    return render_to_response(template,variables)

def laporan_kas_besar(request, object_id):
    sekarang = datetime.date.today() 
    gr = Tbl_Cabang.objects.filter(status_aktif = 1)
    saldo_awal_tbl = Tbl_TransaksiKeu.objects.filter(id_coa__coa= '11.01.01').filter(id_cabang = '300').filter(tgl_trans = sekarang)
    saldo_awal = sum([a.saldo for a in saldo_awal_tbl])
    #coa_kas_besar = dict([[k, 0] for k,v in COA_KAS_BESAR])
    pdp_all_debet = Tbl_Transaksi.objects.filter(jenis='GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(debet__gt= 0).filter(tgl_trans= sekarang)
    pdp_all_kredit = Tbl_Transaksi.objects.filter(jenis='GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(kredit__gt =0).filter(tgl_trans= sekarang)
    pendapatan_1 = Tbl_Transaksi.objects.filter(id_unit = 300).filter(debet__gt =0).filter(id_coa__id= 4).filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran_1 = Tbl_Transaksi.objects.filter(id_unit = 300).filter(kredit__gt =0).filter(id_coa__id=4).filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    jrn_pendapatan = Tbl_Transaksi.objects.filter(jenis__in=('GL_GL_PUSAT','AYDA_PUSAT')).filter(status_jurnal=2).filter(id_cabang=object_id).filter(tgl_trans= sekarang).filter(debet__gt=0).filter(id_coa_id=4)
    jrn_pengeluaran = Tbl_Transaksi.objects.filter(id_cabang=object_id).filter(kredit__gt= 0).filter(status_jurnal=2).filter(id_coa_id=4).filter(tgl_trans= sekarang).filter(jenis='GL_GL_PUSAT').filter(tgl_trans= sekarang)
    template = 'jurnal/laporan_kas_besar.html'
    variables = RequestContext(request, {
        'gr':gr,'saldo_awal_bank':saldo_awal,
        'j_pendapatan':(sum([p.debet for p in jrn_pendapatan])),'j_pengeluaran' : (sum([p.kredit for p in jrn_pengeluaran])),
        'jrn_pendapatan':jrn_pendapatan,'jrn_pengeluaran':jrn_pengeluaran,
        'total_penerimaan': sum([a.debet for a in pendapatan_1]),
        'total_pengeluaran': sum([a.kredit for a in pengeluaran_1]),
        'saldo_akhir_bank': saldo_awal + ((sum([p.debet for p in pdp_all_debet])) - (sum([p.kredit for p in pdp_all_kredit]))) +\
            ((sum([p.debet for p in jrn_pendapatan])) - (sum([p.kredit for p in jrn_pengeluaran]))),
    })
    return render_to_response(template,variables)
'''
def laporan_kas_besar(request,object_id):
    saldo_awal = 0
    sekarang = datetime.date.today()
    tbl = Tbl_Cabang.objects.filter(kode_unit = 300)
    coa = dict([[k, 0] for k,v in COA_KAS])
    coa_kas_besar = dict([[k, 0] for k,v in COA_KAS_BESAR])
    balik = dict([[k, 0] for k,v in ID_BALIK])
    jrn_pendapatan = Tbl_Transaksi.objects.filter(jenis__in=('GL_GL_PUSAT','AYDA_PUSAT')).filter(status_jurnal=2).filter(id_cabang=object_id).\
	filter(tgl_trans= sekarang).filter(debet__gt=0).filter(id_coa_id__in=coa_kas_besar)
    jrn_pengeluaran = Tbl_Transaksi.objects.filter(id_cabang=object_id).filter(kredit__gt= 0).filter(status_jurnal=2).filter(id_coa_id__in=coa_kas_besar).\
        filter(tgl_trans= sekarang).filter(jenis='GL_GL_PUSAT').filter(tgl_trans= sekarang)
    pendapatan_jakarta = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=301).filter(debet__gt =0).filter(id_coa_id =(4)).\
        filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran_jakarta = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=301).filter(kredit__gt =0).filter(id_coa_id =(4)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)    
    pendapatan_suci = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=302).filter(debet__gt =0).filter(id_coa_id =(4)).\
        filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran_suci = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=302).filter(kredit__gt =0).filter(id_coa_id =(4)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pendapatan_du = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=303).filter(debet__gt =0).filter(id_coa_id =(4)).\
        filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran_du = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=303).filter(kredit__gt =0).filter(id_coa_id =(4)).\
        filter(jenis = 'GL_GL_PENGELURAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)  
    pendapatan_blbr = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=304).filter(debet__gt =0).filter(id_coa_id =(4)).\
        filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran_blbr = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=304).filter(kredit__gt =0).filter(id_coa_id =(4)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pendapatan_gh = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=306).filter(debet__gt =0).filter(id_coa_id =(4)).\
        filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran_gh = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=306).filter(kredit__gt =0).filter(id_coa_id =(4)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pendapatan_kopo = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=307).filter(debet__gt =0).filter(id_coa_id =(4)).\
        filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran_kopo = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=307).filter(kredit__gt =0).filter(id_coa_id =(4)).\
        filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pendapatan_cibiru = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=308).filter(debet__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran_cibiru = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=308).filter(kredit__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pendapatan_cipacing = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=309).filter(debet__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran_cipacing = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=309).filter(kredit__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pendapatan_jtngr = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=310).filter(debet__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran_jtngr = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=310).filter(kredit__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pendapatan_cimahi = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=311).filter(debet__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran_cimahi = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=311).filter(kredit__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pendapatan_buahbatu = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=312).filter(debet__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran_buahbatu = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=312).filter(kredit__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pendapatan_marnat = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=315).filter(debet__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran_marnat = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=315).filter(kredit__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pendapatan_cirebon = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=317).filter(debet__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran_cirebon = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=317).filter(kredit__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pendapatan_cimbuleuit = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=319).filter(debet__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran_cimbuleuit = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=319).filter(kredit__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pendapatan_ujungberung = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=320).filter(debet__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran_ujungberung = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=320).filter(kredit__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pendapatan_ciwastra = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=321).filter(debet__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran_ciwastra = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=321).filter(kredit__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pendapatan_bojongsoang = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=322).filter(debet__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    pengeluaran_bojongsoang = Tbl_Transaksi.objects.filter(id_unit = 300).filter(id_cabang_tuju=322).filter(kredit__gt =0).filter(id_coa_id =(4)).\
       filter(jenis = 'GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(tgl_trans= sekarang)
    #pdp_all_debet = Tbl_Transaksi.objects.filter(id_coa_id=(4)).filter(id_cabang_tuju__in=balik).filter(jenis='GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').\
        #filter(debet__gt= 0).filter(tgl_trans= sekarang)
    pdp_all_debet = Tbl_Transaksi.objects.filter(jenis='GL_GL_PENAMBAHAN_PUSAT_KAS_GERAI').filter(debet__gt= 0).filter(tgl_trans= sekarang)

    #pdp_all_kredit = Tbl_Transaksi.objects.filter(id_coa_id=(4)).filter(id_cabang_tuju__in=balik).filter(jenis='GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').\
        #filter(kredit__gt =0).filter(tgl_trans= sekarang)
    pdp_all_kredit = Tbl_Transaksi.objects.filter(jenis='GL_GL_PENGELUARAN_PUSAT_KAS_GERAI').filter(kredit__gt =0).filter(tgl_trans= sekarang)

    variables = RequestContext(request, {
        'jrn_pendapatan':jrn_pendapatan,'jrn_pengeluaran':jrn_pengeluaran,
        'kas_debit_jkt':sum([p.debet for p in pendapatan_jakarta]),'kas_kredit_jkt':sum([p.kredit for p in pengeluaran_jakarta]),
        'kas_debit_suci':sum([p.debet for p in pendapatan_suci]),'kas_kredit_suci':sum([p.kredit for p in pengeluaran_suci]),
        'kas_debit_du':sum([p.debet for p in pendapatan_du]),'kas_kredit_du':sum([p.kredit for p in pengeluaran_du]),
        'kas_debit_blbr':sum([p.debet for p in pendapatan_blbr]),'kas_kredit_blbr':sum([p.kredit for p in pengeluaran_blbr]),
        'kas_debit_gh':sum([p.debet for p in pendapatan_gh]),'kas_kredit_gh':sum([p.kredit for p in pengeluaran_gh]),
        'kas_debit_kopo':sum([p.debet for p in pendapatan_kopo]),'kas_kredit_kopo':sum([p.kredit for p in pengeluaran_kopo]),
        'kas_debit_cibiru':sum([p.debet for p in pendapatan_cibiru]),'kas_kredit_cibiru':sum([p.kredit for p in pengeluaran_cibiru]),
        'kas_debit_cipacing':sum([p.debet for p in pendapatan_cipacing]),'kas_kredit_cipacing':sum([p.kredit for p in pengeluaran_cipacing]),
        'kas_debit_jtngr':sum([p.debet for p in pendapatan_jtngr]),'kas_kredit_jtngr':sum([p.kredit for p in pengeluaran_jtngr]),
        'kas_debit_cimahi':sum([p.debet for p in pendapatan_cimahi]),'kas_kredit_cimahi':sum([p.kredit for p in pengeluaran_cimahi]),
        'kas_debit_buahbatu':sum([p.debet for p in pendapatan_buahbatu]),'kas_kredit_buahbatu':sum([p.kredit for p in pengeluaran_buahbatu]),
        'kas_debit_marnat':sum([p.debet for p in pendapatan_marnat]),'kas_kredit_marnat':sum([p.kredit for p in pengeluaran_marnat]),
        'kas_debit_cirebon':sum([p.debet for p in pendapatan_cirebon]),'kas_kredit_cirebon':sum([p.kredit for p in pengeluaran_cirebon]),
        'kas_debit_cimbuleuit':sum([p.debet for p in pendapatan_cimbuleuit]),'kas_kredit_cimbuleuit':sum([p.kredit for p in pengeluaran_cimbuleuit]),
        'kas_debit_ujungberung':sum([p.debet for p in pendapatan_ujungberung]),
        'kas_kredit_ujungberung':sum([p.kredit for p in pengeluaran_ujungberung]),'kas_debit_ciwastra':sum([p.debet for p in pendapatan_ciwastra]),
        'kas_kredit_ciwastra':sum([p.kredit for p in pengeluaran_ciwastra]),'kas_debit_bojongsoang':sum([p.debet for p in pendapatan_bojongsoang]),
        'kas_kredit_bojongsoang':sum([p.kredit for p in pengeluaran_bojongsoang]),'saldo_awal_bank':saldo_awal,        
        'pendapatan':(sum([p.debet for p in pdp_all_debet])),'pengeluaran':(sum([p.kredit for p in pdp_all_kredit])),
        'j_pendapatan':(sum([p.debet for p in jrn_pendapatan])),'j_pengeluaran' : (sum([p.kredit for p in jrn_pengeluaran])),
        'saldo_akhir_bank':((sum([p.debet for p in pdp_all_debet])) - (sum([p.kredit for p in pdp_all_kredit]))) +\
            ((sum([p.debet for p in jrn_pendapatan])) - (sum([p.kredit for p in jrn_pengeluaran]))),
        })
    return render_to_response('jurnal/laporan_kas_besar.html', variables)
'''
def laporan_materai(request,object_id):
    sekarang = datetime.date.today()
    cab = Tbl_Cabang.objects.filter(status_aktif = 1)
    pembelian = Tbl_Transaksi.objects.filter(jenis = 'PEMBELIAN MATERAI PUSAT').filter(tgl_trans= sekarang).filter(debet__gt= 0).filter(status_jurnal = 2)
    penjualan = Tbl_Transaksi.objects.filter(jenis = 'PENJUALAN MATERAI PUSAT').filter(tgl_trans= sekarang).filter(debet__gt= 0).filter(status_jurnal = 2)
    saldo = Tbl_TransaksiKeu.objects.filter(id_coa__coa= '13.04.03').filter(tgl_trans= sekarang).filter(status_jurnal = 2)
    permintaan = Tbl_Transaksi.objects.filter(jenis = 'Penerimaan Materai').filter(tgl_trans= sekarang).filter(debet__gt= 0).filter(status_jurnal = 2)
    pemakaian = Tbl_Transaksi.objects.filter(id_coa_id = 231).filter(tgl_trans= sekarang).filter(kredit__gt= 0).filter(status_jurnal = 2).filter(jenis__in =('Pencairan','Pencairan_Barang_sama'))

    template='keuangan/laporan_materai.html'
    variable = RequestContext(request,{'cabang':cab,'total_beli':sum([a.debet for a in pembelian]),'total_saldo':sum([a.saldo for a in saldo]),\
            'total_permintaan':sum([a.debet for a in permintaan]),'total_pemakaian':sum([a.kredit for a in pemakaian]),'total_jual':sum([a.debet for a in penjualan]),
            'total_saldo_akhir':sum([a.debet for a in pembelian]) + sum([a.saldo for a in saldo]) + sum([a.debet for a in permintaan]) })
    return render_to_response(template,variable)


def range_laporan_materai(request):
    cab = Tbl_Cabang.objects.filter(status_aktif =1)

    start_date = None
    end_date = None
    akun=[]
    form = SearchForm()
    if 'submit_satu' in request.GET and request.GET['start_date'] and request.GET['end_date']:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        for c in cab :
            akun.append({'c':c,'nama_cabang':c.nama_cabang,'range_saldo_materai':c.range_saldo_materai(start_date),\
                'range_permintaan_materai':c.range_permintaan_materai(start_date,end_date),
                'range_pembelian_materai_pusat':c.range_pembelian_materai_pusat(start_date,end_date),
                'range_pemakaian_materai':c.range_pemakaian_materai(start_date,end_date),
                'range_saldo_akhir_materai':c.range_saldo_akhir_materai(start_date,end_date),
                'range_penjualan_materai_pusat':c.range_penjualan_materai_pusat(start_date,end_date),
                'pcs_materai':c.pcs_materai(start_date,end_date)})
            start_date = start_date
            end_date = end_date
        template='keuangan/range_laporan_materai.html'
        variable = RequestContext(request,{'akun':akun,'start_date':start_date,'form':form})
        return render_to_response(template,variable)

    if 'submit_dua' in request.GET and request.GET['start_date'] and request.GET['end_date']:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        for c in cab :
            akun.append({'c':c,'nama_cabang':c.nama_cabang,'range_saldo_materai':c.range_saldo_materai(start_date),\
                'range_permintaan_materai':c.range_permintaan_materai(start_date,end_date),
                'range_pembelian_materai_pusat':c.range_pembelian_materai_pusat(start_date,end_date),
                'range_pemakaian_materai':c.range_pemakaian_materai(start_date,end_date),
                'range_saldo_akhir_materai':c.range_saldo_akhir_materai(start_date,end_date),
                'range_penjualan_materai_pusat':c.range_penjualan_materai_pusat(start_date,end_date),
                'pcs_materai':c.pcs_materai(start_date,end_date)})
            start_date = start_date
            end_date = end_date
        template='keuangan/range_cetak_laporan_materai.html'
        variable = RequestContext(request,{'akun':akun,'start_date':start_date,'form':form,'end_date':end_date})
        return render_to_response(template,variable)

    else:
        template='keuangan/range_laporan_materai.html'
        variable = RequestContext(request,{'akun':akun,'start_date':start_date,'end_date':end_date,'form':form})
        return render_to_response(template,variable)
