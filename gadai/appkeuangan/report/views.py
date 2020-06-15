from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404,render,redirect
from gadai.appgadai.gerai.views import*
from gadai.appgadai.models import *
import datetime
from gadai.appgadai.templatetags.number_format import number_format
from gadai.appgadai.models import Tbl_Cabang,AkadGadai,AKUN
from django import forms
from gadai.appgadai.templatetags.terbilang import terbilang
from django.contrib import messages
from gadai.appkeuangan.models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from gadai.appgadai.jurnal.forms import *
from gadai.appkeuangan.report.forms import *
import xlwt
import io
import xlsxwriter
from dateutil import parser

def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['KEUANGAN1','KEUANGAN2','KEUANGAN'])
@login_required

def laporan_kembaligu(request):
    start_date = None
    end_date = None
    id_cabang = None
    form =Format_laporanForm()
    awal = datetime.date(2016,11,1)
    plns = []
    if 'end_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET:
        #start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500':
            ##All Gerai
            ag = AkadGadai.objects.filter(tanggal__range=(awal,end_date))#.filter(lunas = sekarang)
            titip_gu = TitipanAkadUlang.objects.filter(norek__in = ag).filter(status = 2)
            ttp_gu =titip_gu.count()
            total_titip_gu = sum([a.nilai for a in titip_gu])

            titip_plns = TitipanPelunasan.objects.filter(norek__in = ag).filter(status = 2)
            ttp_plns =titip_plns.count()
            total_titip_plns = sum([a.nilai for a in titip_plns])

            total_titip_gu_plns = total_titip_gu + total_titip_plns


            template = 'kasir/laporan/laporan_kembaligu.html'
            variable = RequestContext(request, {'ag': ag,'total_titip_gu':total_titip_gu,'titip_gu':titip_gu,
                       'total_titip_plns':total_titip_plns,'titip_plns':titip_plns,'total_titip_gu_plns':total_titip_gu_plns})
            return render_to_response(template, variable) 
        else:
            ##Pergerai
            ag = AkadGadai.objects.filter(tanggal__range=(awal,end_date)).filter(gerai__kode_cabang = id_cabang)#.filter(lunas = sekarang)
            titip_gu = TitipanAkadUlang.objects.filter(norek__in = ag).filter(status = 2)
            ttp_gu =titip_gu.count()
            total_titip_gu = sum([a.nilai for a in titip_gu])

            titip_plns = TitipanPelunasan.objects.filter(norek__in = ag).filter(status = 2)
            ttp_plns =titip_plns.count()
            total_titip_plns = sum([a.nilai for a in titip_plns])

            total_titip_gu_plns = total_titip_gu + total_titip_plns

            tbl_cab = Tbl_Cabang.objects.get(kode_cabang = id_cabang)
            template = 'kasir/laporan/laporan_kembaligu.html'
            variable = RequestContext(request, {'ag': ag,'total_titip_gu':total_titip_gu,'titip_gu':titip_gu,'tbl_cab':tbl_cab,
                       'total_titip_plns':total_titip_plns,'titip_plns':titip_plns,'total_titip_gu_plns':total_titip_gu_plns})
            return render_to_response(template, variable) 

    else:
        template = 'kasir/laporan/cari_titipan_gu.html'
        variable = RequestContext(request,{'form':form})
        return render_to_response(template,variable)

@login_required
def posting_tanggal_pusat(request,object_id):
    pilih = object_id
    sekarang = datetime.date.today()
    relatif = relativedelta(days=1)
    tgl_sekarang = sekarang 
    sbl_tanggal = sekarang - relatif
    s_awal = sum([a.saldo_sekarang for a in Jurnal.objects.filter(kode_cabang=pilih)])

    form = KeuanganPusatForm(initial={'tanggal':tgl_sekarang,'kode_cabang':(pilih)}) 
    template = 'keuangan/posting_tanggal_pusat.html'
    variable = RequestContext(request, {'form': form,'pilih':pilih})
    return render_to_response(template,variable)
@login_required
def tanggal_posting_pusat(request,object_id):
    user = request.user
    kode_cabang = object_id
    id_cabang = object_id
    sekarang = datetime.date.today()
    if request.method == 'POST':
        form = KeuanganPusatForm(request.POST)
        if form.is_valid():
            tanggal = form.cleaned_data['tanggal']
            kode_cabang = form.cleaned_data['kode_cabang']
            saldo = form.cleaned_data['saldo']
            note = form.cleaned_data['note']
            tanggal_sbl = form.cleaned_data['tanggal_sbl']
            simpan = KeuanganPusat(tanggal_sbl = tanggal_sbl, tanggal = tanggal, saldo = 0, kode_cabang = kode_cabang, note = note,\
                cu = request.user, mu=request.user)
            simpan.save()
            
            akun = Tbl_Akun.objects.all()#filter(view_unit__in = (300,0,1))
            tanggal_sbl = simpan.tanggal #datetime.date.today()
            relatif = relativedelta(days=1)
            tgl_posting = tanggal + relatif
            akumulasi_debet = 0
            akumulasi_kredit = 0
            for ls in akun:
                akumulasi_debet = ls.total_debet_count()
                akumulasi_kredit = ls.total_kredit_count()
                
                if  ls.total_debet_count() >= 0 and ls.total_kredit_count() >= 0 or ls.total_debet_count() >= 0 and ls.total_kredit_count() >= 0 or\
                    ls.total_debet_count() >= 0 and ls.total_kredit_count() >= 0 :
                    if ls.coa[0:1] == str(2) or ls.coa[0:1] == str(3) or ls.coa[0:1] == str(4) or\
                        ls.coa[0:1] == str(6) :

                        jurnalk = JurnalKeuangan(nobukti ='00000',tgl_trans= tgl_posting,kode_cabang=simpan.kode_cabang,cu=user,\
                            mu= user,diskripsi='SALDOAWAL')
                        jurnalk.save()
                        tblk = Tbl_TransaksiKeu(debet=0,kredit=0,jurnal=jurnalk,tgl_trans= tgl_posting,id_coa=ls,jenis='SALDOKASGERAI',\
                            id_cabang=simpan.kode_cabang,id_unit=300,id_product=4,status_jurnal=2,deskripsi='SALDOKASGERAI',\
                            saldo = ls.saldo_kas_ref_laporan_gerai(sekarang,id_cabang) + ls.total_kredit_count() - ls.total_debet_count())
                        tblk.save()
                    else:                        
                        jurnalk = JurnalKeuangan(nobukti ='00000',tgl_trans= tgl_posting,kode_cabang=simpan.kode_cabang,cu=user,\
                            mu= user,diskripsi='SALDOAWAL')
                        jurnalk.save()
                        tblk = Tbl_TransaksiKeu(debet=0,kredit=0,jurnal=jurnalk,tgl_trans= tgl_posting,id_coa=ls,jenis='SALDOKASGERAI',\
                            id_cabang=simpan.kode_cabang,id_unit=300,id_product=4,status_jurnal=2,deskripsi='SALDOKASGERAI',\
                            saldo = ls.saldo_kas_ref_laporan_gerai(sekarang,id_cabang) + ls.total_debet_count() - ls.total_kredit_count())
                        tblk.save() 

                #bb = Tbl_TransaksiKeu.objects.filter(id_coa = ls.id).filter(jenis='SALDOKASGERAI').filter(id_cabang=kode_cabang).filter(status_jurnal = 2).filter(tgl_trans__lt = tgl_posting)
                #bb.update(status_jurnal =3)
                #tbl.update(posting = 2)
        messages.add_message(request, messages.INFO,"JURNAL POSTING Pusat OK")
        return HttpResponseRedirect('/rkeuangan/posting_gerai_count/')
    else:
        form = PostingTglForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('kasir/view/menu_postting_pusat.html', variables)

@user_passes_test(is_in_multiple_groups)
@login_required
def rekapitulasi_transaksi_pusat(request):
    user = request.user
    ledger = Tbl_Transaksi.objects.all()
    banyak = ledger.all
    start_date = None
    id_cabang = 300
    jenis =None
    akumulasi_debet =0
    akumulasi_kredit = 0
    sekarang = datetime.date.today()
    start_date =sekarang
    all = []
    ledger_search = Tbl_Transaksi.objects.filter(tgl_trans=(sekarang)).filter(status_jurnal=2).filter(id_cabang =300).order_by('id')
    for (l,k) in AKUN:
        akumulasi_debet = 0
        akumulasi_kredit = 0
        tb = Tbl_Transaksi.objects.filter(id_coa = l).filter(tgl_trans=(sekarang)).filter(status_jurnal = 2).filter(id_cabang =300).order_by('id_coa')
        for t in tb: 
            if t.id_coa.coa[0:1] == str(2) or t.id_coa.coa[0:1] == str(3) or t.id_coa.coa[0:1] == str(4) or\
                t.id_coa.coa[0:1] == str(6) :
                akumulasi_debet += t.debet
                akumulasi_kredit += t.kredit 
                all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'diskripsi':t.deskripsi,'tanggal':t.tgl_trans,
                    'id_coa':t.id_coa,'tgl_trans':t.tgl_trans,'tiket':t.jurnal.no_akad,\
                    'saldo_pusat':t.id_coa.saldo_kas_laporan_gerai(start_date,id_cabang),
                    'cu':t.jurnal.cu,
                    'saldo_akhir': (t.id_coa.saldo_kas_ref_laporan_gerai(start_date,id_cabang) + akumulasi_kredit - akumulasi_debet)})
            else:
                akumulasi_debet += t.debet
                akumulasi_kredit += t.kredit
                all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'diskripsi':t.deskripsi,'tanggal':t.tgl_trans,
                    'id_coa':t.id_coa,'tgl_trans':t.tgl_trans,'tiket':t.jurnal.no_akad,
                    'saldo_pusat':t.id_coa.saldo_kas_laporan_gerai(start_date,id_cabang),
                    'cu':t.jurnal.cu,'saldo_akhir':(t.id_coa.saldo_kas_laporan_gerai(start_date,id_cabang) + akumulasi_debet - akumulasi_kredit)})

    gr = Tbl_Transaksi.objects.filter(tgl_trans=sekarang,status_jurnal='2',id_cabang='300')
    template = 'kasir/view/menu_postting_pusat.html'
    variables = RequestContext(request, {'ledger':all,'start_date':start_date,'cabang':user.profile.gerai.kode_cabang})
    return render_to_response(template, variables)

@user_passes_test(is_in_multiple_groups)
@login_required
def hapus_jurnal(request,object_id):
    user = request.user
    tbl = Jurnal.objects.get(id=object_id)   
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Penghapusan Jurnal Berhasil')
    return HttpResponseRedirect("/rreport/rekapitulasi_transaksi_pusat/" )


@user_passes_test(is_in_multiple_groups)
@login_required
def edit_refisi_jurnal(request,object_id):
    post = get_object_or_404(Tbl_Transaksi, id=object_id)
    jurnal = Jurnal.objects.get(pk = post.jurnal.id)
    if request.method == "POST":
        form = Tbl_TransaksiRefForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect('/rreport/%s/show_refisi_jurnal/' % jurnal.id)
    else:
        form = Tbl_TransaksiRefForm(instance=post)
    return render(request, 'keuangan/edit_refisi_jurnal.html', {'form': form,'id':object_id})

@user_passes_test(is_in_multiple_groups)
@login_required
def hapus_jurnal_refisi(request,object_id):
    user = request.user
    tbl = Jurnal.objects.get(id=object_id)   
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Penghapusan Jurnal Berhasil')
    return HttpResponseRedirect("/rreport/refisi_jurnal_harian/" )

@user_passes_test(is_in_multiple_groups)
@login_required
def show_refisi_jurnal(request,object_id):
    post = Jurnal.objects.get(pk=object_id)
    tbl = Tbl_Transaksi.objects.filter(jurnal__id = object_id)
    variable = RequestContext(request,{'show':tbl})
    return render_to_response( 'keuangan/show_refisi_jurnal.html',variable)

@login_required
def refisi_jurnal_harian(request):
    sekarang = datetime.date.today()   
    trans = []    
    form = RefisiJurnalForm()
    if 'start_date' in request.GET and 'submit_satu' in request.GET:
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        akumulasi_debet =0
        akumulasi_kredit = 0
        start_date = start_date
        id_cabang = id_cabang
        if id_cabang == '500':
            ledger_search = Jurnal.objects.filter(tgl_trans=(start_date)).filter(kode_cabang=id_cabang).order_by('id')
            for t in ledger_search:
                trans.append({'t':t, 'deskripsi': t.id_coa.deskripsi,'saldo':t.saldo,'no_akad':t.no_akad,
                    'diskripsi' : t.jurnal.diskripsi, 'kepala_coa': t.kepala_coa, 'coa':t.id_coa.coa, 'nobukti': t.jurnal.nobukti,\
                     'tgl_trans':t.tgl_trans,'id_coa':t.id_coa})
        else:
            ledger_search = Jurnal.objects.filter(tgl_trans=(start_date)).filter(kode_cabang=id_cabang).order_by('id')
            for t in ledger_search:
                trans.append({'t':t,'tgl_trans':t.tgl_trans,'nobukti':t.nobukti,'id':t.id,'no_akad':t.no_akad})

        template='keuangan/refisi_jurnal.html'
        variable = RequestContext(request,{'form':form,'ledger_search':trans,'id_cabang':id_cabang,'start_date':start_date})
        return render_to_response(template,variable)
    else:
        template='keuangan/refisi_jurnal.html'
        variable = RequestContext(request,{'form':form})
        return render_to_response(template,variable)

@login_required
def kembaligu(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    ag = AkadGadai.objects.filter(gerai__kode_cabang = cab)#.filter(lunas = sekarang)
    titip = TitipanAkadUlang.objects.filter(norek__in = ag).filter(status = 2)
    total_titip = sum([a.nilai for a in titip])
    template = 'kasir/laporan/show_kembaligu.html'
    variable = RequestContext(request, {
        'ag': ag,'total_titip':total_titip,'titip':titip})
    return render_to_response(template,variable)

@login_required
def slip_setoran_titipan_gu(request, object_id):
    user = request.user
    pk = TitipanAkadUlang.objects.get(id=object_id)
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s.pdf' % pk.norek
    c = canvas.Canvas(response, pagesize=(9.5*inch, 11*inch))
    c.setTitle("kwitansi %s" % pk.norek)
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
        trk=p.tanggal
        dd=patokan.month-trk.month
        yy=patokan.year-trk.year


    header1=(4.25 *inch, (5.3 + 5.5) * inch)
    colom1 = (0.5*inch, (4.3 + 5.5) *inch)
            #ke kiri  ke atas ke bawah
    colom2 = (6.7*inch, (4.5 + 5.5) *inch)
    colom3 = (6.0*inch, (4.8 + 4.5) *inch)
    colom4 = (0.5*inch, (3.7 + 4.2) *inch)

    header2=(8.25 *inch, (2.75 + 2.5) * inch)    
    header3=(4.25 *inch, (2.8 + 2.65) * inch)        
    #header2=(4.25 *inch, (5.3 + 5.5) * inch)
    colom5 = (0.5*inch, (2.15 + 2.3) *inch)
    #ke kiri  ke atas ke bawah
    colom6 = (6.7*inch, (2.15 + 2.5) *inch)
    colom7 = (0.5*inch, (3.0 + 1.5) *inch)
    colom8 = (0.5*inch, (1.5 + 1.1) *inch)
    tb=terbilang(pk.nilai)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/logoksu_hitamputih.png'), 1.0*inch, (5.5 + 1.5) * inch, width=200.5/17.5*0.51*inch,height=120/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 0.5*inch, (4.85 + 5.5) * inch, width=30/17.5*0.51*inch,height=25/17.5*0.51*inch,mask=None)
    
    x,y = header1
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Courier-Bold", 14)
    c.drawString(5.8 * inch , y-0.35* inch, "SLIP SETORAN TITIPAN G. ULANG")
    c.line( 5.8 * inch , y-0.39* inch , 9.3 * inch ,y-0.39* inch ) ; y -=y1
    c.setFont("Courier-Bold", 11)
    c.drawString(5.8 * inch , y-0.42*inch,"%s" % (pk.akad_gerai())); y -=y1    
    c.setFont("Courier-Bold", 16)
    c.drawString(x-2.8*inch, y+0.20*inch, "KSU RIZKY ABADI"); y -=y1
    c.setFont("Courier",8)
    c.drawString(x-2.8*inch, y+0.20*inch, "Badan Hukum No.518/BH.88-DISKOP/THN.2007 Tgl 27 Desember 2007"); y -=y1
    c.drawString(x-2.8*inch, y+0.20*inch, "Jln Cisaranten Kulon IV No.55 Bandung Tlp: 022-7808443"); y -=y1
    kb = str.upper(str(pk.akad_gerai()))
  
    c.setFont("Courier",8)
    # garis Paling atas
    c.line( x-3.75* inch , y+0.172* inch , 5.5 * inch ,y+0.172* inch) ; y -=y1
    #garis Paling Bawah
    c.line( x-3.75* inch , y-0.0* inch , 5.5 * inch ,y-0.0* inch) ; y -=y1
    #garis paling kiri
    c.line( x-3.75* inch , y+0.37* inch , x-3.75* inch ,y+0.1* inch) 
    #garis paling kanan
    c.line( 5.5 * inch , y+0.37* inch , 5.5 * inch ,y+0.1* inch)   
    

    ####KOLOM 2 Dua Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    ## Barcode
    c.setFont("Courier", 7)
    c.drawString(600, 785, "%s" % sekarang.strftime('[%-b][%Y]') )
    barcode = code128.Code128("%s" % pk.akad_norek())
    barcode.drawOn(c, 195*mm, 268*mm)
               
            
    c.setFont("Courier", 11)
    x,y = colom2
    y1 = 0.165 * inch
    c.setFont("Courier", 9)
    c.drawString(x, y, "No PK"); 
    c.drawString(x+1.2*inch, y, ": %s" % (pk.akad_norek())); y -=y1
    c.drawString(x, y, "Tgl Transaksi");
    c.drawString(x+1.2*inch, y, ": %s" % (pk.tanggal.strftime('%d %b %Y'))); y -=2*y1
    
    ####KOLOM 3 Tilu Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    c.setFont("Courier-Bold", 14)
               
            
    c.setFont("Courier", 11)
    x,y = colom3
    y1 = 0.165 * inch
    c.setFont("Courier-Bold", 9)
    ####AKHiR KOLOM 3 Tilu Coy

    ####KOLOM 1 hiji Coy
    x,y = colom1
    y1 = 0.165 * inch
    
    c.setFont("Courier", 11)
    c.drawString(x, y+0.0*inch, "KSU RIZKY ABADI sudah menerima," ); y -=2*y1
    c.drawString(x, y, "Titipan Setoran G. Ulang Jaminan" )
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s|%s|%s" % (pk.akad_merk_barang(),pk.akad_type_barang(),pk.akad_sn_barang()  )); y -=1*y1
    c.drawString(x, y, "Titipan Sebesar")
    c.drawString(x+3.1*inch, y,": Rp.")
    c.drawRightString(x+4.5*inch, y,"%s"% (number_format(pk.nilai))); y -=2*y1
    c.drawString(x, y, "Nomor Debitur")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s" % (pk.akad_nonas())); y -=1*y1
    c.drawString(x, y, "Nama")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s" % (pk.nama())); y -=y1
    c.drawString(x, y, "Alamat")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s, No. %s RT/RW %s/%s " % (pk.akad_alamat(), pk.akad_no_rumah(),pk.akad_rt(),pk.akad_rt())); y -=y1    
    c.drawString(x+3.3*inch, y,"Kel. %s, Kec. %s Kota/Kab %s/%s " % (pk.akad_kelurahan_ktp(), pk.akad_kecamatan_ktp(),pk.akad_kotamadya_ktp(),pk.akad_kabupaten_ktp())); y -=y1    
    c.drawString(x, y, "Jenis Pinjaman")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"Titipan Setoran Gadai Ulang Jaminan"); y -=1.5*y1    


    ####KOLOM 4 Opat Coy
    x,y = colom4
    y1 = 0.165 * inch

    c.setFont("Courier-Bold", 11)
    c.drawString(x,y,  " ## %s Rupiah ##"  % tb.title()); y -=10*y1
    
    # garis Paling atas
    c.line( x, y+1.8*inch , 9.0 * inch , y+1.8*inch )
    #garis Paling Bawah
    c.line( x, y+1.55*inch , 9.0 * inch , y+1.55*inch )
    #garis paling kiri
    c.line( x, y+1.8*inch , x , y+1.55*inch )
    #garis paling kanan
    c.line( 9.0 * inch, y+1.8*inch ,9.0 * inch , y+1.55*inch )
    
    c.setFont("Courier",11)
    c.drawString(x+6.9*inch, y+1.4*inch, "Bandung, %s" % sekarang.strftime('%d %b %Y') )
    c.drawString(x, y+1.2*inch, "Kasir Gerai,")
    c.drawString(x+6.9*inch, y+1.2*inch, "Debitur,") ; 
    #c.line(410, 488, 500, 488)
    c.drawString(x,y+0.3*inch, "%s"%(user.profile.gerai.nama_kasir))
    c.drawString(x+6.9*inch,y+0.3*inch,"%s"%(pk.nama())) 
    #c.line(550, 488, 650, 488)
    c.setFont("Courier",8)
    c.drawString(x, y, "*Kwitansi ini sah apabila telah di validasi di tanda tangan dan di stample*"); y -=y1
    c.drawString(x, y, " Lembar 1/3 Gerai, Asli "); y -=y1
    c.drawString(x-2.5 * inch, y," - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - " )

    #######BARUUUU 123
    tb=terbilang(pk.nilai)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/logoksu_hitamputih.png'), 1.0*inch, (0.2 + 1.5) * inch, width=200.5/17.5*0.51*inch,height=120/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 0.5*inch, (-0.5 + 5.5) * inch, width=30/17.5*0.51*inch,height=25/17.5*0.51*inch,mask=None)
    
    x,y = header3
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Courier-Bold", 14)
    c.drawString(5.8 * inch , y-0.35* inch, "SLIP SETORAN TITIPAN G. ULANG")
    c.line( 5.8 * inch , y-0.39* inch , 9.3 * inch ,y-0.39* inch ) ; y -=y1
    c.setFont("Courier-Bold", 11)
    c.drawString(5.8 * inch , y-0.42*inch,"%s" % (pk.akad_gerai())); y -=y1    
    c.setFont("Courier-Bold", 16)
    c.drawString(x-2.8*inch, y+0.20*inch, "KSU RIZKY ABADI"); y -=y1
    c.setFont("Courier",8)
    c.drawString(x-2.8*inch, y+0.20*inch, "Badan Hukum No.518/BH.88-DISKOP/THN.2007 Tgl 27 Desember 2007"); y -=y1
    c.drawString(x-2.8*inch, y+0.20*inch, "Jln Cisaranten Kulon IV No.55 Bandung Tlp: 022-7808443"); y -=y1
    kb = str.upper(str(pk.akad_gerai()))
  
    c.setFont("Courier",8)
    # garis Paling atas
    c.line( x-3.75* inch , y+0.172* inch , 5.5 * inch ,y+0.172* inch) ; y -=y1
    #garis Paling Bawah
    c.line( x-3.75* inch , y-0.0* inch , 5.5 * inch ,y-0.0* inch) ; y -=y1
    #garis paling kiri
    c.line( x-3.75* inch , y+0.37* inch , x-3.75* inch ,y+0.1* inch) 
    #garis paling kanan
    c.line( 5.5 * inch , y+0.37* inch , 5.5 * inch ,y+0.1* inch)   
    

    ####KOLOM 2 Dua Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    ## Barcode
    c.setFont("Courier", 7)
    c.drawString(600, 400, "%s" % sekarang.strftime('[%-b][%Y]') )
    barcode = code128.Code128("%s" % pk.akad_norek())
    barcode.drawOn(c, 195*mm, 132*mm)
               
            
    c.setFont("Courier", 11)
    x,y = colom6
    y1 = 0.165 * inch
    c.setFont("Courier", 9)
    c.drawString(x, y, "No PK"); 
    c.drawString(x+1.2*inch, y, ": %s" % (pk.akad_norek())); y -=y1
    c.drawString(x, y, "Tgl Transaksi");
    c.drawString(x+1.2*inch, y, ": %s" % (pk.tanggal.strftime('%d %b %Y'))); y -=2*y1
    
    ####KOLOM 3 Tilu Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    c.setFont("Courier-Bold", 14)
               
            
    c.setFont("Courier", 11)
    x,y = colom3
    y1 = 0.165 * inch
    c.setFont("Courier-Bold", 9)
    ####AKHiR KOLOM 3 Tilu Coy

    ####KOLOM 1 hiji Coy
    x,y = colom7
    y1 = 0.165 * inch
    
    c.setFont("Courier", 11)
    c.drawString(x, y+0.0*inch, "KSU RIZKY ABADI sudah menerima," ); y -=2*y1
    c.drawString(x, y, "Titipan Setoran G. Ulang Jaminan" )
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s|%s|%s" % (pk.akad_merk_barang(),pk.akad_type_barang(),pk.akad_sn_barang()  )); y -=1*y1
    c.drawString(x, y, "Titipan Sebesar")
    c.drawString(x+3.1*inch, y,": Rp.")
    c.drawRightString(x+4.5*inch, y,"%s"% (number_format(pk.nilai))); y -=2*y1
    c.drawString(x, y, "Nomor Debitur")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s" % (pk.akad_nonas())); y -=1*y1
    c.drawString(x, y, "Nama")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s" % (pk.nama())); y -=y1
    c.drawString(x, y, "Alamat")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s, No. %s RT/RW %s/%s " % (pk.akad_alamat(), pk.akad_no_rumah(),pk.akad_rt(),pk.akad_rt())); y -=y1    
    c.drawString(x+3.3*inch, y,"Kel. %s, Kec. %s Kota/Kab %s/%s " % (pk.akad_kelurahan_ktp(), pk.akad_kecamatan_ktp(),pk.akad_kotamadya_ktp(),pk.akad_kabupaten_ktp())); y -=y1    
    c.drawString(x, y, "Jenis Pinjaman")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"Titipan Setoran Gadai Ulang Jaminan"); y -=1.5*y1    


    ####KOLOM 4 Opat Coy
    x,y = colom8
    y1 = 0.165 * inch

    c.setFont("Courier-Bold", 11)
    c.drawString(x,y,  " ## %s Rupiah ##"  % tb.title()); y -=10*y1
    
    # garis Paling atas
    c.line( x, y+1.8*inch , 9.0 * inch , y+1.8*inch )
    #garis Paling Bawah
    c.line( x, y+1.55*inch , 9.0 * inch , y+1.55*inch )
    #garis paling kiri
    c.line( x, y+1.8*inch , x , y+1.55*inch )
    #garis paling kanan
    c.line( 9.0 * inch, y+1.8*inch ,9.0 * inch , y+1.55*inch )
    
    c.setFont("Courier",11)
    c.drawString(x+6.9*inch, y+1.4*inch, "Bandung, %s" % sekarang.strftime('%d %b %Y') )
    c.drawString(x, y+1.2*inch, "Kasir Gerai,")
    c.drawString(x+6.9*inch, y+1.2*inch, "Debitur,") ; 
    #c.line(410, 488, 500, 488)
    c.drawString(x,y+0.3*inch, "%s"%(user.profile.gerai.nama_kasir))
    c.drawString(x+6.9*inch,y+0.3*inch,"%s"%(pk.nama())) 
    #c.line(550, 488, 650, 488)
    c.setFont("Courier",8)
    c.drawString(x, y, "*Kwitansi ini sah apabila telah di validasi di tanda tangan dan di stample*"); y -=y1
    c.drawString(x, y, " Lembar 2/3 Pusat, Copy "); y -=y1

    c.showPage()
    c.save()


#################################################################    
    header1=(4.25 *inch, (5.3 + 5.5) * inch)
    colom1 = (0.5*inch, (4.3 + 5.5) *inch)
            #ke kiri  ke atas ke bawah
    colom2 = (6.7*inch, (4.5 + 5.5) *inch)
    colom3 = (6.0*inch, (4.8 + 4.5) *inch)
    colom4 = (0.5*inch, (3.7 + 4.2) *inch)

    header2=(8.25 *inch, (2.75 + 2.5) * inch)    
    header3=(4.25 *inch, (2.8 + 2.65) * inch)        
    #header2=(4.25 *inch, (5.3 + 5.5) * inch)
    colom5 = (0.5*inch, (2.15 + 2.3) *inch)
            #ke kiri  ke atas ke bawah
    colom6 = (6.7*inch, (2.15 + 2.3) *inch)
    colom7 = (0.5*inch, (3.0 + 1.5) *inch)
    colom8 = (0.5*inch, (1.5 + 1.1) *inch)
    tb=terbilang(pk.nilai)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/img/logoksu_hitamputih.png'), 1.0*inch, (5.5 + 1.5) * inch, width=200.5/17.5*0.51*inch,height=120/17.5*0.51*inch)
    c.drawImage(os.path.join(settings.PROJECT_ROOT, 'static/images/logoksu.png'), 0.5*inch, (4.85 + 5.5) * inch, width=30/17.5*0.51*inch,height=25/17.5*0.51*inch,mask=None)
    
    x,y = header1
    y1 = 0.10 * inch

    y -=1*y1
    c.setFont("Courier-Bold", 14)
    c.drawString(5.8 * inch , y-0.35* inch, "SLIP SETORAN TITIPAN G. ULANG")
    c.line( 5.8 * inch , y-0.39* inch , 9.3 * inch ,y-0.39* inch ) ; y -=y1
    c.setFont("Courier-Bold", 11)
    c.drawString(5.8 * inch , y-0.42*inch,"%s" % (pk.akad_gerai())); y -=y1    
    c.setFont("Courier-Bold", 16)
    c.drawString(x-2.8*inch, y+0.20*inch, "KSU RIZKY ABADI"); y -=y1
    c.setFont("Courier",8)
    c.drawString(x-2.8*inch, y+0.20*inch, "Badan Hukum No.518/BH.88-DISKOP/THN.2007 Tgl 27 Desember 2007"); y -=y1
    c.drawString(x-2.8*inch, y+0.20*inch, "Jln Cisaranten Kulon IV No.55 Bandung Tlp: 022-7808443"); y -=y1
    kb = str.upper(str(pk.akad_gerai()))
  
    c.setFont("Courier",8)
    # garis Paling atas
    c.line( x-3.75* inch , y+0.172* inch , 5.5 * inch ,y+0.172* inch) ; y -=y1
    #garis Paling Bawah
    c.line( x-3.75* inch , y-0.0* inch , 5.5 * inch ,y-0.0* inch) ; y -=y1
    #garis paling kiri
    c.line( x-3.75* inch , y+0.37* inch , x-3.75* inch ,y+0.1* inch) 
    #garis paling kanan
    c.line( 5.5 * inch , y+0.37* inch , 5.5 * inch ,y+0.1* inch)   
    

    ####KOLOM 2 Dua Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    ## Barcode
    c.setFont("Courier", 7)
    c.drawString(600, 785, "%s" % sekarang.strftime('[%-b][%Y]') )
    barcode = code128.Code128("%s" % pk.akad_norek())
    barcode.drawOn(c, 195*mm, 268*mm)
               
            
    c.setFont("Courier", 11)
    x,y = colom2
    y1 = 0.165 * inch
    c.setFont("Courier", 9)
    c.drawString(x, y, "No PK"); 
    c.drawString(x+1.2*inch, y, ": %s" % (pk.akad_norek())); y -=y1
    c.drawString(x, y, "Tgl Transaksi");
    c.drawString(x+1.2*inch, y, ": %s" % (pk.tanggal.strftime('%d %b %Y'))); y -=2*y1
    
    ####KOLOM 3 Tilu Coy
    y -=  2 * y1
    y2 = y + 0.1 * inch
    c.setFont("Courier-Bold", 14)
               
            
    c.setFont("Courier", 11)
    x,y = colom3
    y1 = 0.165 * inch
    c.setFont("Courier-Bold", 9)
    ####AKHiR KOLOM 3 Tilu Coy

    ####KOLOM 1 hiji Coy
    x,y = colom1
    y1 = 0.165 * inch
    
    c.setFont("Courier", 11)
    c.drawString(x, y+0.0*inch, "KSU RIZKY ABADI sudah menerima," ); y -=2*y1
    c.drawString(x, y, "Titipan Setoran G. Ulang Jaminan" )
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s|%s|%s" % (pk.akad_merk_barang(),pk.akad_type_barang(),pk.akad_sn_barang()  )); y -=1*y1
    c.drawString(x, y, "Titipan Sebesar")
    c.drawString(x+3.1*inch, y,": Rp.")
    c.drawRightString(x+4.5*inch, y,"%s"% (number_format(pk.nilai))); y -=2*y1
    c.drawString(x, y, "Nomor Debitur")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s" % (pk.akad_nonas())); y -=1*y1
    c.drawString(x, y, "Nama")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s" % (pk.nama())); y -=y1
    c.drawString(x, y, "Alamat")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"%s, No. %s RT/RW %s/%s " % (pk.akad_alamat(), pk.akad_no_rumah(),pk.akad_rt(),pk.akad_rt())); y -=y1    
    c.drawString(x+3.3*inch, y,"Kel. %s, Kec. %s Kota/Kab %s/%s " % (pk.akad_kelurahan_ktp(), pk.akad_kecamatan_ktp(),pk.akad_kotamadya_ktp(),pk.akad_kabupaten_ktp())); y -=y1    
    c.drawString(x, y, "Jenis Pinjaman")
    c.drawString(x+3.1*inch, y,": ")
    c.drawString(x+3.3*inch, y,"Titipan Setoran Gadai Ulang Jaminan"); y -=1.5*y1    


    ####KOLOM 4 Opat Coy
    x,y = colom4
    y1 = 0.165 * inch

    c.setFont("Courier-Bold", 11)
    c.drawString(x,y,  " ## %s Rupiah ##"  % tb.title()); y -=10*y1
    
    # garis Paling atas
    c.line( x, y+1.8*inch , 9.0 * inch , y+1.8*inch )
    #garis Paling Bawah
    c.line( x, y+1.55*inch , 9.0 * inch , y+1.55*inch )
    #garis paling kiri
    c.line( x, y+1.8*inch , x , y+1.55*inch )
    #garis paling kanan
    c.line( 9.0 * inch, y+1.8*inch ,9.0 * inch , y+1.55*inch )
    
    c.setFont("Courier",11)
    c.drawString(x+6.9*inch, y+1.4*inch, "Bandung, %s" % sekarang.strftime('%d %b %Y') )
    c.drawString(x, y+1.2*inch, "Kasir Gerai,")
    c.drawString(x+6.9*inch, y+1.2*inch, "Debitur,") ; 
    #c.line(410, 488, 500, 488)
    c.drawString(x,y+0.3*inch, "%s"%(user.profile.gerai.nama_kasir))
    c.drawString(x+6.9*inch,y+0.3*inch,"%s"%(pk.nama())) 
    #c.line(550, 488, 650, 488)
    c.setFont("Courier",8)
    c.drawString(x, y, "*Kwitansi ini sah apabila telah di validasi di tanda tangan dan di stample*"); y -=y1
    c.drawString(x, y, " Lembar 3/3 Nasabah, Copy "); y -=y1
    c.drawString(x-2.5 * inch, y," - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - " )
    c.showPage()
    c.save()
    return response

def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['KEUANGAN','SUPERUSER','MANKEU','KEUANGAN_PJB'])

@login_required
@user_passes_test(is_in_multiple_groups)
def index_keu(request): 
    jurnal_list = Tbl_Transaksi.objects.all()
    trans=[]
    form = SearchForm()
    start_date = None
    end_date = None
    id_cabang = None
    jenis = None
    if 'id_cabang' in request.GET and request.GET['id_cabang'] and 'start_date' in request.GET and request.GET['end_date']:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        jenis =request.GET['jenis']
        if id_cabang == '500' and jenis == '1':###NONPOSTING GABUNG
            ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).\
                filter(status_jurnal = 2).exclude(jenis = ('SALDOKASGERAI'))
            trans = []
            for l in ledger_search:           
                trans.append(l)
            start_date = start_date
            id_cabang = id_cabang
            end_date = end_date
            template='report_baru/jurnal/index.html'
            variable = RequestContext(request, {'jurnal_list': trans,'total_debet': sum([p.debet for p in trans]),\
                'total_kredit': sum([p.kredit for p in trans]),'form':form,
                'start_date':start_date,'id_cabang':id_cabang,'end_date':end_date})
            return render_to_response(template,variable)

        elif id_cabang != '500' and jenis == '1':###NONPOSTING PERCABANG
            ledger_search = Tbl_Transaksi.objects.filter(jurnal__kode_cabang = id_cabang).filter(tgl_trans__range=(start_date,end_date)).\
                filter(status_jurnal = 2).exclude(jenis = ('SALDOKASGERAI'))
            trans = []
            for l in ledger_search:           
                trans.append(l)
            start_date = start_date
            id_cabang = id_cabang
            end_date = end_date

            template='report_baru/jurnal/index.html'
            variable = RequestContext(request, {'jurnal_list': trans,'total_debet': sum([p.debet for p in trans]),\
                'total_kredit': sum([p.kredit for p in trans]),'form':form,
                'start_date':start_date,'id_cabang':id_cabang,'end_date':end_date})
            return render_to_response(template,variable)
        ## After Posting
        elif id_cabang == '500' and jenis == '2':###POSTING GABUNGAN
            ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).\
            filter(status_jurnal= 3).exclude(jenis = ('SALDOKASGERAI'))
            trans = []
            for l in ledger_search:
                trans.append(l)
            start_date = start_date
            id_cabang = id_cabang
            end_date = end_date
            template1 ='report_baru/jurnal/index.html'
            variable = RequestContext(request, {'jurnal_list': trans,'total_debet': sum([p.debet for p in trans]),\
                'total_kredit': sum([p.kredit for p in trans]),'form':form,
                'start_date':start_date,'id_cabang':id_cabang,'end_date':end_date})
            return render_to_response(template1,variable)

        elif id_cabang != '500' and jenis == '2':###POSTING PER CABANG
            ledger_search = Tbl_TransaksiKeu.objects.filter(jurnal__kode_cabang = id_cabang).filter(tgl_trans__range=(start_date,end_date)).\
                filter(status_jurnal= 2).exclude(jenis = ('SALDOKASGERAI'))
            trans = []
            for l in ledger_search:
                trans.append(l)
            start_date = start_date
            id_cabang = id_cabang
            end_date = end_date
            template ='report_baru/jurnal/index.html'
            variable = RequestContext(request, {'jurnal_list': trans,'total_debet': sum([p.debet for p in trans]),\
                'total_kredit': sum([p.kredit for p in trans]),'form':form,
                'start_date':start_date,'id_cabang':id_cabang,'end_date':end_date})
            return render_to_response(template,variable)
        elif id_cabang == '500' and jenis == '3':###CETAK POSTING GABUNG
            start_date = request.GET['start_date']
            end_date = request.GET['end_date']
            id_cabang = request.GET['id_cabang']
            ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).\
                filter(status_jurnal= 2).exclude(jenis = ('SALDOKASGERAI'))
            trans = []
            for l in ledger_search:
                trans.append(l)
            start_date = start_date
            id_cabang = id_cabang
            end_date = end_date
            template= 'report_baru/jurnal/cetak_jurnal_transaksi.html'
            variable = RequestContext(request, {'jurnal_list': trans,'total_debet': sum([p.debet for p in trans]),\
                    'total_kredit': sum([p.kredit for p in trans]),'form':form,
                    'start_date':start_date,'id_cabang':id_cabang,'end_date':end_date})
            return render_to_response(template,variable)
        elif id_cabang != '500' and jenis == '3':###CETAK POSTING PERCABANG
            start_date = request.GET['start_date']
            end_date = request.GET['end_date']
            id_cabang = request.GET['id_cabang']
            ledger_search = Tbl_Transaksi.objects.filter(jurnal__kode_cabang = id_cabang).filter(tgl_trans__range=(start_date,end_date)).\
                filter(status_jurnal= 2).exclude(jenis = ('SALDOKASGERAI'))
            trans = []
            for l in ledger_search:
                trans.append(l)
            start_date = start_date
            id_cabang = id_cabang
            end_date = end_date
            template= 'report_baru/jurnal/cetak_jurnal_transaksi.html'
            variable = RequestContext(request, {'jurnal_list': trans,'total_debet': sum([p.debet for p in trans]),\
                    'total_kredit': sum([p.kredit for p in trans]),'form':form,
                    'start_date':start_date,'id_cabang':id_cabang,'end_date':end_date})
            return render_to_response(template,variable)
    else:
        template = 'report_baru/jurnal/index.html'
        variable = RequestContext(request, {'jurnal_list': trans,'total_debet': sum([p.debet for p in trans]),\
            'total_kredit': sum([p.kredit for p in trans]),'form':form,
            'start_date':start_date,'id_cabang':id_cabang,'end_date':end_date})
        return render_to_response(template,variable)

@login_required
def buku_besar_all_keu(request):
    ledger = Tbl_Transaksi.objects.all()
    banyak = ledger.all
    start_date = None
    id_cabang = None
    jenis =None
    akumulasi_debet =0
    akumulasi_kredit = 0
    transaksi =  banyak.im_class(Tbl_Transaksi)
    fil = transaksi.filter(status_jurnal = 1)
    jumlah_debet = sum([n.debet for n in fil])
    jumlah_kredit = sum([n.kredit for n in fil])
    saldo_awal = jumlah_debet - jumlah_kredit
    a = jumlah_debet + jumlah_kredit
    akumulasi_pokok_plafon = 0
    form = SearchForm()
    all = []
    sld = sum([a.saldo for a in Tbl_Transaksi.objects.filter(jurnal__kode_cabang = id_cabang).filter(tgl_trans=start_date).\
        filter(jenis = ('SALDOKASGERAI'))])
    lb_akun = Tbl_Akun.objects.exclude(view_unit__in=("100","200"))
    ##GABUNGAN
    if 'id_cabang' in request.GET and request.GET['id_cabang'] and 'start_date' in request.GET and 'end_date' in request.GET and 'submit_satu' in request.GET: 
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        jenis = request.GET['jenis']
        if id_cabang == '500' and jenis == '1' :#####NONPOSTING GABUNG    
            for aa in lb_akun:
                akumulasi_debet = 0
                akumulasi_kredit = 0
                tb = Tbl_Transaksi.objects.filter(id_coa__id = aa.id).filter(tgl_trans__range=(start_date,end_date)).filter(status_jurnal = 2).\
                    exclude(jenis = ('SALDOKASGERAI')).order_by('id_coa')
                for t in tb: 
                    if t.id_coa.coa[0:1] == str(2) or t.id_coa.coa[0:1] == str(3) or t.id_coa.coa[0:1] == str(4) or\
                        t.id_coa.coa[0:1] == str(6) :
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit 
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'cu':t.jurnal.cu,
                            'saldo_akhir':  (t.id_coa.saldo_kas_laporan(start_date) + akumulasi_kredit - akumulasi_debet)  ,\
                            'deskripsi': t.id_coa.deskripsi,'diskripsi' : t.deskripsi,'kepala_coa': t.kepala_coa,\
                            'id_jurnal':t.jurnal.id,'ket':t.jurnal.diskripsi,'keterangan':t.jurnal.nobukti,\
                            'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa,\
                            'saldo_pjb':t.id_coa.saldo_kas_laporan(start_date)})
                    else:
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit 
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir':(t.id_coa.saldo_kas_laporan(start_date) + akumulasi_debet -\
                            akumulasi_kredit)  ,'deskripsi': t.id_coa.deskripsi,'diskripsi' : t.deskripsi,'kepala_coa': t.kepala_coa,\
                            'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa,'cu':t.jurnal.cu,\
                            'id_jurnal':t.jurnal.id,'ket':t.jurnal.diskripsi,'keterangan':t.jurnal.nobukti,\
                            'saldo_pjb':t.id_coa.saldo_kas_laporan(start_date)})# (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)
        ##CABANG
        elif id_cabang != '500' and jenis == '1' :#####NONPOSTING PERCABANG
            for aa in lb_akun:
                akumulasi_debet = 0
                akumulasi_kredit = 0
                tb = Tbl_Transaksi.objects.filter(id_coa__id = aa.id).filter(tgl_trans__range=(start_date,end_date)).filter(id_cabang= id_cabang).\
                exclude(jenis = ('SALDOKASGERAI')).filter(status_jurnal = 2)
                for t in tb:
                    if t.id_coa.coa[0:1] == str(2) or t.id_coa.coa[0:1] == str(3) or t.id_coa.coa[0:1] == str(4) or\
                        t.id_coa.coa[0:1] == str(6):
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit 
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,
                            'saldo_akhir':  (t.id_coa.saldo_kas_ref_laporan_gerai(start_date,id_cabang) + akumulasi_kredit - akumulasi_debet)  ,\
                            'deskripsi': t.id_coa.deskripsi,'diskripsi' : t.deskripsi,'kepala_coa': t.kepala_coa,\
                            'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa,'cu':t.jurnal.cu,\
                            'id_jurnal':t.jurnal.id,'ket':t.jurnal.diskripsi,'keterangan':t.jurnal.nobukti,\
                            'saldo_pjb':t.id_coa.saldo_kas_laporan_gerai(start_date,id_cabang)})
                    else:
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit 
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,
                            'saldo_akhir':(t.id_coa.saldo_kas_laporan_gerai(start_date,id_cabang) + akumulasi_debet -\
                            akumulasi_kredit)  ,'deskripsi': t.id_coa.deskripsi,'diskripsi' : t.deskripsi,'kepala_coa': t.kepala_coa,\
                            'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa,'cu':t.jurnal.cu,\
                            'id_jurnal':t.jurnal.id,'ket':t.jurnal.diskripsi,'keterangan':t.jurnal.nobukti,\
                            'saldo_pjb':t.id_coa.saldo_kas_laporan_gerai(start_date,id_cabang)})# (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)

        elif id_cabang == '500' and jenis == '2' :#####POSTING GABUNG    
            for aa in lb_akun:
                akumulasi_debet = 0
                akumulasi_kredit = 0
                tb = Tbl_TransaksiKeu.objects.filter(id_coa__id = aa.id).filter(tgl_trans=start_date).filter(status_jurnal = 2).\
                exclude(jenis = ('SALDOKASGERAI')).order_by('id_coa')
                for t in tb: 
                    if t.id_coa.coa[0:1] == str(2) or t.id_coa.coa[0:1] == str(3) or t.id_coa.coa[0:1] == str(4) or\
                        t.id_coa.coa[0:1] == str(6) :
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit 
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,
                            'saldo_akhir':  (t.id_coa.saldo_kas(start_date) + akumulasi_kredit - akumulasi_debet)  ,\
                            'deskripsi': t.id_coa.deskripsi,'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,\
                            'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa,'cu':t.jurnal.cu,\
                            'saldo_pjb':t.id_coa.saldo_kas(start_date)})
                    else:
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit 
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir':(t.id_coa.saldo_kas(start_date) + akumulasi_debet -\
                            akumulasi_kredit)  ,'deskripsi': t.id_coa.deskripsi,'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,\
                            'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa,'cu':t.jurnal.cu,\
                            'saldo_pjb':t.id_coa.saldo_kas(start_date)})# (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)

        elif id_cabang != '500' and jenis == '2' :#####POSTING PERCABANG  
            for aa in lb_akun:
                akumulasi_debet = 0
                akumulasi_kredit = 0
                tb = Tbl_Transaksi.objects.filter(id_coa__id = aa.id).filter(tgl_trans=start_date).filter(id_cabang= id_cabang).\
                exclude(jenis = ('SALDOKASGERAI')).filter(status_jurnal = 3)
                for t in tb: 
                    if t.id_coa.coa[0:1] == str(2) or t.id_coa.coa[0:1] == str(3) or t.id_coa.coa[0:1] == str(4) or\
                        t.id_coa.coa[0:1] == str(6) :
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit 
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'cu':t.jurnal.cu,
                            'saldo_akhir':  (t.id_coa.saldo_kas(start_date) + akumulasi_kredit - akumulasi_debet)  ,\
                            'deskripsi': t.id_coa.deskripsi,'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,\
                            'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa,\
                            'saldo_pjb':t.id_coa.saldo_kas(start_date)})
                    else:
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit 
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir':(t.id_coa.saldo_kas(start_date) + akumulasi_debet -\
                            akumulasi_kredit)  ,'deskripsi': t.id_coa.deskripsi,'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,\
                            'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa,'cu':t.jurnal.cu,\
                            'saldo_pjb':t.saldo})# (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)

        template='report_baru/ledger/search/search_buku_besar_all.html'
        variable = RequestContext(request,{'ledger':all,'saldo':saldo_awal,'form':form,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang})
        return render_to_response(template,variable)
    
    if 'id_cabang' in request.GET and request.GET['id_cabang'] and 'start_date' in request.GET and 'submit_dua' in request.GET:######NON POSTING CETAK
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        jenis = request.GET['jenis'] 
        if id_cabang == '500' and jenis == '3' :#####NONPOSTING GABUNG    
            for aa in lb_akun:
                akumulasi_debet = 0
                akumulasi_kredit = 0
                tb = Tbl_Transaksi.objects.filter(id_coa__id = aa.id).filter(tgl_trans__range=(start_date,end_date)).filter(status_jurnal = 2).\
                    exclude(jenis = ('SALDOKASGERAI')).order_by('id_coa')
                for t in tb: 
                    if t.id_coa.coa[0:1] == str(2) or t.id_coa.coa[0:1] == str(3) or t.id_coa.coa[0:1] == str(4) or\
                        t.id_coa.coa[0:1] == str(6) :
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit 
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'cu':t.jurnal.cu,
                            'saldo_akhir':  (t.id_coa.saldo_kas_laporan(start_date) + akumulasi_kredit - akumulasi_debet)  ,\
                            'deskripsi': t.id_coa.deskripsi,'diskripsi' : t.deskripsi,'kepala_coa': t.kepala_coa,\
                            'id_jurnal':t.jurnal.id,'ket':t.jurnal.diskripsi,'keterangan':t.jurnal.nobukti,\
                            'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa,\
                            'saldo_pjb':t.id_coa.saldo_kas_laporan(start_date)})
                    else:
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit 
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir':(t.id_coa.saldo_kas_laporan(start_date) + akumulasi_debet -\
                            akumulasi_kredit)  ,'deskripsi': t.id_coa.deskripsi,'diskripsi' : t.deskripsi,'kepala_coa': t.kepala_coa,\
                            'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa,'cu':t.jurnal.cu,\
                            'id_jurnal':t.jurnal.id,'ket':t.jurnal.diskripsi,'keterangan':t.jurnal.nobukti,\
                            'saldo_pjb':t.id_coa.saldo_kas_laporan(start_date)})# (t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)

        elif id_cabang != '500' and jenis == '3':
            for aa in lb_akun:
                akumulasi_debet = 0
                akumulasi_kredit = 0
                tb = Tbl_Transaksi.objects.filter(id_coa__id = aa.id).filter(tgl_trans__range=(start_date,end_date)).filter(id_cabang= id_cabang).\
                exclude(jenis = ('SALDOKASGERAI')).filter(status_jurnal = 2)
                for t in tb:
                    if t.id_coa.coa[0:1] == str(2) or t.id_coa.coa[0:1] == str(3) or t.id_coa.coa[0:1] == str(4) or\
                        t.id_coa.coa[0:1] == str(6):
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit 
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,
                            'saldo_akhir':  (t.id_coa.saldo_kas_ref_laporan_gerai(start_date,id_cabang) + akumulasi_kredit - akumulasi_debet)  ,\
                            'deskripsi': t.id_coa.deskripsi,'diskripsi' : t.deskripsi,'kepala_coa': t.kepala_coa,\
                            'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa,'cu':t.jurnal.cu,\
                            'id_jurnal':t.jurnal.id,'ket':t.jurnal.diskripsi,'keterangan':t.jurnal.nobukti,\
                            'saldo_pjb':t.id_coa.saldo_kas_laporan_gerai(start_date,id_cabang)})
                    else:
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit 
                        all.append({'t':t,'debet':t.debet,'kredit':t.kredit,
                            'saldo_akhir':(t.id_coa.saldo_kas_laporan_gerai(start_date,id_cabang) + akumulasi_debet -\
                            akumulasi_kredit)  ,'deskripsi': t.id_coa.deskripsi,'diskripsi' : t.deskripsi,'kepala_coa': t.kepala_coa,\
                            'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa,'cu':t.jurnal.cu,\
                            'id_jurnal':t.jurnal.id,'ket':t.jurnal.diskripsi,'keterangan':t.jurnal.nobukti,\
                            'saldo_pjb':t.id_coa.saldo_kas_laporan_gerai(start_date,id_cabang)})
        template='report_baru/ledger/search/cetak_buku_besar_all.html'
        variable = RequestContext(request,{'ledger':all,'saldo':saldo_awal,'form':form,'start_date':start_date,'id_cabang':id_cabang})
        return render_to_response(template,variable)
        
    if 'id_cabang' in request.GET and request.GET['id_cabang'] and 'start_date' in request.GET and 'submit_tiga' in request.GET:######NON POSTING
        start_date = request.GET['start_date']
        id_cabang = request.GET['id_cabang']
        jenis = request.GET['jenis'] 
        if id_cabang == '500' and jenis == '4':
            for aa in lb_akun:
                tb = Tbl_Transaksi.objects.filter(id_coa__id = aa.id ).filter(tgl_trans=start_date).filter(status_jurnal=3).\
                exclude(jenis = ('SALDOKASGERAI'))
                for t in tb:
                    all.append(t)
        elif id_cabang != '500' and jenis == '4':
            for aa in lb_akun:
                tb = Tbl_Transaksi.objects.filter(id_coa__id = aa.id ).filter(tgl_trans=start_date).filter(id_cabang=id_cabang).\
                    exclude(jenis = ('SALDOKASGERAI')).filter(status_jurnal=3)
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
        return render_to_response('report_baru/ledger/search/search_buku_besar_all.html', variables)


@login_required
def buku_besar(request):
    ledger = Tbl_Transaksi.objects.all()
    sekarang = datetime.date.today()
    saldo = 0
    start_date = None
    end_date = None
    id_cabang = None
    total_debet = 0
    total_kredit = 0    
    form = SearchForm()
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_tiga' in request.GET:### Sudah Posting
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_coa = request.GET['id_coa']
        id_cabang = request.GET['id_cabang']
        trans = []
        b = Tbl_Akun.objects.get(id=int(id_coa))
        #sld = sum([a.saldo for a in Tbl_Transaksi.objects.filter(jurnal__kode_cabang = id_cabang).\
            #filter(jenis = ('SALDOKASGERAI'))])
        sld = sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(jurnal__kode_cabang = id_cabang).\
            filter(jenis = ('SALDOKASGERAI'))])
        akumulasi_debet =0
        akumulasi_kredit = 0
        start_date = start_date
        end_date = end_date
        id_cabang = id_cabang
        if id_cabang == '500':
            ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(status_jurnal=3).\
                filter(id_coa=id_coa).exclude(jenis =( 'SALDOKASGERAI')).order_by('tgl_trans')
            for l in ledger_search:
                for t in l.jurnal.tbl_transaksi_set.filter(id_coa=b):
                    akumulasi_debet += t.debet
                    akumulasi_kredit += t.kredit
                    trans.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir': (t.id_coa.saldo_pjb + akumulasi_debet -\
                        akumulasi_kredit),'deskripsi': t.deskripsi,'diskripsi' : t.jurnal.diskripsi,\
                        'kepala_coa': t.kepala_coa,'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,\
                        'id_coa':t.id_coa})
                    start_date = start_date
                    end_date = end_date
                    id_cabang = id_cabang
                    total_debet = akumulasi_debet
                    total_kredit = akumulasi_kredit
                    saldo = t.saldo_awalhari(id_cabang,start_date)#(t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)

        else:
            ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(id_cabang=id_cabang).\
                filter(status_jurnal=3).filter(id_coa=id_coa).order_by('tgl_trans')
            for l in ledger_search:
                for t in l.jurnal.tbl_transaksi_set.filter(id_coa=b).filter(id_cabang=id_cabang):
                    ##pasiva
                    akumulasi_debet += t.debet
                    akumulasi_kredit += t.kredit
                    #if t.id_coa.coa[0:1] == str(2) or t.id_coa.coa[0:1] == str(3) or t.id_coa.coa[0:1] == str(4) or t.id_coa.coa[0:2] == str(60) :
                    if l.id_coa.jenis_laporan == 'PO' or l.id_coa.jenis_laporan == 'PNO' or l.id_coa.jenis_laporan == 'P' or l.id_coa.jenis_laporan == 'E' :
                        trans.append({'t':t, 'debet':t.debet, 'kredit':t.kredit, 'saldo_akhir': (t.id_coa.saldo_kas_posting + akumulasi_kredit -\
                            akumulasi_debet) , 'deskripsi': t.deskripsi,'saldo_awal':t.saldo,
                            'diskripsi' : t.jurnal.diskripsi, 'kepala_coa': t.kepala_coa, 'coa':t.id_coa.coa, 'nobukti': t.jurnal.nobukti,\
                            'tgl_trans':t.tgl_trans,'id_coa':t.id_coa})
                    else:
                        trans.append({'t':t, 'debet':t.debet, 'kredit':t.kredit, 'saldo_akhir': (t.id_coa.saldo_kas_posting + akumulasi_debet -\
                            akumulasi_kredit) , 'deskripsi': t.deskripsi,'saldo_awal':t.saldo,
                            'diskripsi' : t.jurnal.diskripsi, 'kepala_coa': t.kepala_coa, 'coa':t.id_coa.coa, 'nobukti': t.jurnal.nobukti,\
                            'tgl_trans':t.tgl_trans,'id_coa':t.id_coa})

                    start_date = start_date
                    end_date = end_date
                    id_cabang = id_cabang
                    total_debet = akumulasi_debet
                    total_kredit = akumulasi_kredit

        template='report_baru/ledger/search/search_buku_besar.html'
        variable = RequestContext(request,{'form':form,'ledger_search':trans,'kode':Tbl_Akun.objects.get(id=int(id_coa)),'saldo_akhir':saldo,
            'total_kredit':total_debet,'total_debet': total_kredit ,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,})
        return render_to_response(template,variable)

    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET:###NON POSTING
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_coa = request.GET['id_coa']
        id_cabang = request.GET['id_cabang']
        trans = []
        b = Tbl_Akun.objects.get(id=int(id_coa))
        sld = sum([a.saldo for a in Tbl_Transaksi.objects.filter(jurnal__kode_cabang = id_cabang).\
            filter(jenis =('SALDOKASGERAI')).filter(id_coa = id_coa)])
        akumulasi_debet =0
        akumulasi_kredit = 0
        start_date = start_date
        end_date = end_date
        id_cabang = id_cabang
        if id_cabang == '500':
            ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(status_jurnal=2).\
                filter(id_coa=id_coa).exclude(jenis = ('SALDOKASGERAI')).order_by('tgl_trans')
            for l in ledger_search:
                for t in l.jurnal.tbl_transaksi_set.filter(id_coa=b):
                    if t.id_coa.jenis_laporan == 'PO' or t.id_coa.jenis_laporan == 'PNO' or t.id_coa.jenis_laporan == 'P' or t.id_coa.jenis_laporan == 'E' :
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit
                        trans.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir': (t.id_coa.saldo_kas_laporan(start_date) - akumulasi_debet +\
                        akumulasi_kredit) ,'deskripsi': t.deskripsi,'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,\
                        'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa,\
                        'saldo_awal':t.id_coa.saldo_kas_laporan(start_date)})
                        start_date = start_date
                        end_date = end_date
                        id_cabang = id_cabang
                        total_debet = akumulasi_debet
                        total_kredit = akumulasi_kredit
                        saldo = sld + akumulasi_debet - akumulasi_kredit #(t.id_coa.saldo_pjb + akumulasi_debet - akumulasi_kredit)

                    else:
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit
                        trans.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir': (t.id_coa.saldo_kas_laporan(start_date) + akumulasi_debet -\
                        akumulasi_kredit) ,'deskripsi': t.deskripsi,'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,\
                        'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa,\
                        'saldo_awal':t.id_coa.saldo_kas_laporan(start_date)})
                        start_date = start_date
                        end_date = end_date
                        id_cabang = id_cabang
                        total_debet = akumulasi_debet
                        total_kredit = akumulasi_kredit
                        saldo = sld + akumulasi_debet - akumulasi_kredit

        else:
            ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(id_cabang=id_cabang).\
                filter(status_jurnal=2).filter(id_coa=id_coa).order_by('tgl_trans')
            for l in ledger_search:
                for t in l.jurnal.tbl_transaksi_set.filter(id_coa=b).filter(id_cabang=id_cabang).filter(tgl_trans__range = (start_date,end_date)):
                    #if t.id_coa.coa[0:1] == str(2) or t.id_coa.coa[0:1] == str(3) or t.id_coa.coa[0:1] == str(4) or t.id_coa.coa[0:2] == str(6) :
                    if l.id_coa.jenis_laporan == 'PO' or l.id_coa.jenis_laporan == 'PNO' or l.id_coa.jenis_laporan == 'P' or l.id_coa.jenis_laporan == 'E' :
                    	akumulasi_debet += t.debet
                    	akumulasi_kredit += t.kredit
                    	trans.append({'t':t, 'debet':t.debet, 'kredit':t.kredit,\
                            'saldo_akhir': t.id_coa.saldo_kas_ref_laporan_gerai(start_date,id_cabang) + akumulasi_kredit - akumulasi_debet,\
                            'deskripsi': t.deskripsi,'diskripsi' : t.jurnal.diskripsi, 'kepala_coa': t.kepala_coa,\
                            'saldo_awal':t.id_coa.saldo_kas_ref_laporan_gerai(start_date,id_cabang),'coa':t.id_coa.coa, 'nobukti': t.jurnal.nobukti,\
                            'tgl_trans':t.tgl_trans,'id_coa':t.id_coa})
                    else:
                        akumulasi_debet += t.debet
                        akumulasi_kredit += t.kredit
                        trans.append({'t':t, 'debet':t.debet, 'kredit':t.kredit,\
                                'saldo_akhir': t.id_coa.saldo_kas_laporan_gerai(start_date,id_cabang) + akumulasi_debet - akumulasi_kredit,\
                                'deskripsi': t.id_coa.deskripsi,'diskripsi' : t.jurnal.diskripsi, 'kepala_coa': t.kepala_coa,\
                                'saldo_awal':t.id_coa.saldo_kas_laporan_gerai(start_date,id_cabang),'coa':t.id_coa.coa, 'nobukti': t.jurnal.nobukti,\
                                'tgl_trans':t.tgl_trans, 'id_coa':t.id_coa})
                    start_date = start_date
                    end_date = end_date
                    id_cabang = id_cabang
                    total_debet = akumulasi_debet
                    total_kredit = akumulasi_kredit
                    saldo = sld + akumulasi_debet - akumulasi_kredit      

        template='report_baru/ledger/search/search_buku_besar.html'
        variable = RequestContext(request,{'form':form,'ledger_search':trans,'kode':Tbl_Akun.objects.get(id=int(id_coa)),\
            'total_kredit':total_debet,'total_debet': total_kredit ,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang})
        return render_to_response(template,variable)
    
    if 'start_date' in request.GET and request.GET['end_date'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_coa = request.GET['id_coa']
        id_cabang = request.GET['id_cabang']
        ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).filter(id_cabang=id_cabang).\
            filter(status_jurnal=1).exclude(jenis__ = ('SALDOKASGERAI','SALDOBANKGERAI')).order_by('id')
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
                    trans.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir': (t.id_coa.saldo_pjb + akumulasi_debet -\
                    akumulasi_kredit)  ,'deskripsi': t.id_coa.deskripsi,'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,\
                    'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa})
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
                ledger_search = Tbl_Transaksi.objects.filter(tgl_trans__range=(start_date,end_date)).\
                    filter(status_jurnal=1).exclude(jenis__in = ('SALDOKASGERAI','SALDOBANKGERAI')).order_by('id')
                for t in l.jurnal.tbl_transaksi_set.filter(id_coa=b).filter(id_cabang=id_cabang):
                    akumulasi_debet += t.debet
                    akumulasi_kredit += t.kredit
                    trans.append({'t':t,'debet':t.debet,'kredit':t.kredit,'saldo_akhir': (t.id_coa.saldo_pjb + akumulasi_debet -\
                    akumulasi_kredit)  ,'deskripsi': t.id_coa.deskripsi,'diskripsi' : t.jurnal.diskripsi,'kepala_coa': t.kepala_coa,\
                    'coa':t.id_coa.coa,'nobukti': t.jurnal.nobukti,'tgl_trans':t.tgl_trans,'id_coa':t.id_coa})
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
        template='report_baru/ledger/search/search_buku_besar.html'
        variable = RequestContext(request,{'form':form})
        return render_to_response(template,variable)

@login_required
def neraca_percobaan(request):
    lb_akun = Tbl_Akun.objects.filter(view_unit__in=("0","1","300")).filter(jenis_laporan__in= ("A","P","E","PO","PNO","BO","BNO")).order_by('coa')
    t_debet = 0
    t_kredit = 0
    t_saldo_akhir = 0
    start_date = None
    end_date = None
    id_cabang = None
    akun=[]
    form = SearchForm()
    ####NON POSTTING
    if  'id_cabang' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET:
        sekarang = datetime.date.today()
        tahun  = sekarang.year
        bulan = 1
        tanggal = 1        
        if tahun == 2017:
            tangga_awal = datetime.date(2017,3,1)
        else:
            tangga_awal = datetime.date(tahun,bulan,tanggal)
        start_date = tangga_awal
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        tanggal_shu = parser.parse(end_date) + relativedelta(days=1)
        posisi_tgl = tanggal_shu.date()
        tanggal_saldo = parser.parse(end_date) - relativedelta(days=1)
        posisi_tgl_saldo = tanggal_saldo.date()
        if id_cabang == '500' :
            for c in lb_akun:
                if c.jenis_laporan == 'PO' or c.jenis_laporan == 'PNO' or c.jenis_laporan == 'P' :
                    akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.my_kredit_gabung_neraca(start_date,end_date),\
                        'debet':c.my_debet_gabung_neraca(start_date,end_date),
                        'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent,\
                        'saldo_awal': c.view_saldo_awal_gabungan_neraca(start_date),
                        'saldo_akhir':  c.view_saldo_akhir_gabung_neraca(start_date,end_date)})

                elif c.coa == '35.04.00':
                    akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.my_kredit_gabung_neraca(start_date,end_date),\
                        'debet':c.my_debet_gabung_neraca(start_date,end_date),
                        'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent,\
                        'saldo_awal': c.view_saldo_awal_gabungan_neraca(start_date),
                        'saldo_akhir': c.total_shu_cabang_laporan_gabungan(posisi_tgl)})
                else :
                    akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.my_kredit_gabung_neraca(start_date,end_date),\
                        'debet':c.my_debet_gabung_neraca(start_date,end_date),
                        'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent,\
                        'saldo_awal': c.view_saldo_awal_gabungan_neraca(start_date),
                        'saldo_akhir':  c.view_saldo_akhir_gabung_neraca(start_date,end_date)})

        else:
            for c in lb_akun:
                if c.jenis_laporan == 'PO' or c.jenis_laporan == 'PNO' or c.jenis_laporan == 'P'  :
                    akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.my_kredit_neraca(id_cabang,start_date,end_date),
                        'debet':c.my_debet_neraca(id_cabang,start_date,end_date),
                        'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent,\
                        'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),
                        'saldo_akhir': c.view_saldo_awal_gbg(id_cabang,start_date)+ c.my_kredit_neraca(id_cabang,start_date, end_date) - \
                        c.my_debet_neraca(id_cabang,start_date, end_date)})
                elif c.coa == '30.00.00':
                    akun.append({'debet': c.my_debet_neraca(id_cabang,start_date,end_date),
                          'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),
                          'kredit':c.my_kredit_neraca(id_cabang,start_date,end_date),
                          'saldo_akhir':c.total_shu_cabang(id_cabang,start_date,end_date) + \
                          c.view_saldo_awal_gbg(id_cabang,start_date)+ c.my_debet_neraca(id_cabang,start_date,end_date)-\
                          c.my_kredit_neraca(id_cabang,start_date,end_date),
                          'c':c,'deskripsi':c.deskripsi,'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent})
                elif c.coa == '35.00.00':
                    akun.append({'debet': c.my_debet_neraca(id_cabang,start_date,end_date),
                          'kredit':c.my_kredit_neraca(id_cabang,start_date,end_date),
                          'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),
                          'saldo_akhir': c.total_shu_cabang(id_cabang,start_date,end_date)+ c.my_debet_neraca(id_cabang,start_date,end_date) - \
                           c.my_kredit_neraca(id_cabang,start_date,end_date),
                          'c':c,'deskripsi':c.deskripsi,'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent})
                elif c.coa == '35.04.00':
                    akun.append({'debet': c.my_debet_neraca(id_cabang,start_date,end_date),
                          'kredit':c.my_kredit_neraca(id_cabang,start_date,end_date),
                          'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),
                          'saldo_akhir': c.total_shu_cabang_laporan_gerai(id_cabang,posisi_tgl),
                          'c':c,'deskripsi':c.deskripsi,'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent})
                else:
                    akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.my_kredit_neraca(id_cabang,start_date,end_date),
                        'debet':c.my_debet_neraca(id_cabang,start_date,end_date),
                        'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent,\
                        'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),
                        'saldo_akhir': c.view_saldo_awal_gbg(id_cabang,start_date)+ c.my_debet_neraca(id_cabang,start_date,end_date) - \
                        c.my_kredit_neraca(id_cabang,start_date,end_date)})
                    start_date = start_date
                    end_date = end_date
                    id_cabang = id_cabang
                
        template='report_baru/ledger/neraca_percobaan.html'
        variable = RequestContext(request,{'akun':akun,'total_saldo_akhir':t_saldo_akhir,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,'form':form})
        return render_to_response(template,variable)

    elif  'id_cabang' in request.GET and request.GET['id_cabang'] and 'submit_dua' in request.GET:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        if id_cabang == '500' :
            for c in lb_akun:
                if c.jenis_laporan == 'PO' or c.jenis_laporan == 'PNO' or c.jenis_laporan == 'P':
                    akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.my_kredit_gabung_neraca(start_date,end_date),\
                        'debet':c.my_debet_gabung_neraca(start_date,end_date),
                        'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent,\
                        'saldo_awal': c.view_saldo_awal_gabungan_neraca(start_date),
                        'saldo_akhir':  c.view_saldo_akhir_gabung_neraca(start_date,end_date)})                    
                elif c.coa == '30.00.00':
                    akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.my_kredit_gabung_neraca(start_date,end_date),\
                        'debet':c.my_debet_gabung_neraca(start_date,end_date),
                        'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent,\
                        'saldo_awal': c.view_saldo_awal_gabungan_neraca(start_date),
                        'saldo_akhir': c.total_shu_gerai(start_date,end_date) +c.view_saldo_akhir_gabung_neraca(start_date,end_date)})
 
                elif c.coa == '35.00.00':
                    akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.my_kredit_gabung_neraca(start_date,end_date),\
                        'debet':c.my_debet_gabung_neraca(start_date,end_date),
                        'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent,\
                        'saldo_awal': c.view_saldo_awal_gabungan_neraca(start_date),
                        'saldo_akhir': c.total_shu_gerai(start_date,end_date)})

                elif c.coa == '35.04.00':
                    akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.my_kredit_gabung_neraca(start_date,end_date),\
                        'debet':c.my_debet_gabung_neraca(start_date,end_date),
                        'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent,\
                        'saldo_awal': c.view_saldo_awal_gabungan_neraca(start_date),
                        'saldo_akhir': c.total_shu_gerai(start_date,end_date)})
                else :
                    akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.my_kredit_gabung_neraca(start_date,end_date),\
                        'debet':c.my_debet_gabung_neraca(start_date,end_date),
                        'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent,\
                        'saldo_awal': c.view_saldo_awal_gabungan_neraca(start_date),
                        'saldo_akhir':  total_shu_cabang_laporan_gabungan(posisi_tgl)})
                    start_date = start_date
                    end_date = end_date
                    id_cabang = id_cabang

        else:
            for c in lb_akun:
                if c.jenis_laporan == 'PO' or c.jenis_laporan == 'PNO' or c.jenis_laporan == 'P' :
                    akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.my_kredit_neraca(id_cabang,start_date,end_date),
                        'debet':c.my_debet_neraca(id_cabang,start_date,end_date),
                        'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent,\
                        'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),
                        'saldo_akhir': c.view_saldo_awal_gbg(id_cabang,start_date)+ c.my_kredit_neraca(id_cabang,start_date, end_date) - \
                        c.my_debet_neraca(id_cabang,start_date, end_date)})
                elif c.coa == '30.00.00':
                    akun.append({'debet': c.my_debet_neraca(id_cabang,start_date,end_date),
                          'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),
                          'kredit':c.my_kredit_neraca(id_cabang,start_date,end_date),
                          'saldo_akhir':c.total_shu_cabang(id_cabang,start_date,end_date) + \
                          c.view_saldo_awal_gbg(id_cabang,start_date)+ c.my_debet_neraca(id_cabang,start_date,end_date)-\
                          c.my_kredit_neraca(id_cabang,start_date,end_date),
                          'c':c,'deskripsi':c.deskripsi,'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent})
                elif c.coa == '35.00.00':
                    akun.append({'debet': c.my_debet_neraca(id_cabang,start_date,end_date),
                          'kredit':c.my_kredit_neraca(id_cabang,start_date,end_date),
                          'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),
                          'saldo_akhir': c.total_shu_cabang(id_cabang,start_date,end_date)+ c.my_debet_neraca(id_cabang,start_date,end_date) - \
                           c.my_kredit_neraca(id_cabang,start_date,end_date),
                          'c':c,'deskripsi':c.deskripsi,'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent})
                elif c.coa == '35.04.00':
                    akun.append({'debet': c.my_debet_neraca(id_cabang,start_date,end_date),
                          'kredit':c.my_kredit_neraca(id_cabang,start_date,end_date),
                          'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),
                          'saldo_akhir':c.total_shu_cabang_laporan_gabungan(posisi_tgl),
                          'c':c,'deskripsi':c.deskripsi,'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent})
                else:
                    akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.my_kredit_neraca(id_cabang,start_date,end_date),
                        'debet':c.my_debet_neraca(id_cabang,start_date,end_date),
                        'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent,\
                        'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),
                        'saldo_akhir': c.view_saldo_awal_gbg(id_cabang,start_date)+ c.my_debet_neraca(id_cabang,start_date,end_date) - \
                        c.my_kredit_neraca(id_cabang,start_date,end_date)})
                    start_date = start_date
                    end_date = end_date
                    id_cabang = id_cabang

        template='report_baru/ledger/cetak_neraca_percobaan.html'
        variable = RequestContext(request,{'akun':akun,'total_saldo_akhir':t_saldo_akhir,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,'form':form})
        return render_to_response(template,variable)
    else:
        template='report_baru/ledger/neraca_percobaan.html'
        variable = RequestContext(request,{'form':form})
        return render_to_response(template,variable)

@login_required
def neraca(request):
    #lb_akun = Tbl_Akun.objects.filter(view_unit__in=("0","300")).filter(jenis__in= ("A","P")).filter(layer__in =(2,5)).order_by('coa')
    lb_akun = Tbl_Akun.objects.exclude(view_unit__in=("100","200")).filter(jenis_laporan__in= ("A","P","E")).order_by('coa')
    aktiva = Tbl_Akun.objects.get(pk = 1)
    pasiva = Tbl_Akun.objects.get(pk = 266)
    ekuitas = Tbl_Akun.objects.get(pk = 388)
    shu = Tbl_Akun.objects.get(pk=405)
    shu_dibagikan = Tbl_Akun.objects.get(pk=404)
    modal_penyerta = Tbl_Akun.objects.get(pk=393)
    akun=[]
    form = SearchForm()
    if  'id_cabang' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET:######NON POSTING
        sekarang = datetime.date.today()
        #tahun  = sekarang.year
        #bulan = 1
        #tanggal = 1        
        #if tahun == 2017:
            #tangga_awal = datetime.date(2017,3,1)
        #else:
            #tangga_awal = datetime.date(tahun,bulan,tanggal)
        #start_date = tangga_awal
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        tanggal_shu = parser.parse(end_date) + relativedelta(days=1)
        posisi_tgl = tanggal_shu.date()
        tanggal_saldo = parser.parse(end_date) - relativedelta(days=1)
        posisi_tgl_saldo = tanggal_saldo.date()  
        ### Tambahan Firman Buat mencari tanggal Saldo awal tiap tahun
        patokan_tgl_saldo_awal =end_date[0:4]
        thn = int(patokan_tgl_saldo_awal)
        if id_cabang == '500' :
            sal = Tbl_TransaksiKeu.objects.filter(tgl_trans__year = thn).order_by('id')
            id_awal = sal[0]
            start_date = id_awal.tgl_trans
        else:
            sal = Tbl_TransaksiKeu.objects.filter(id_cabang = id_cabang,tgl_trans__year = thn).order_by('id')
            id_awal = sal[0]
            start_date = id_awal.tgl_trans
        ##Akhir Tambahan
        if id_cabang == '500' :
            for c in lb_akun :
                if c.jenis_laporan == 'P' :
                    akun.append({'c':c,'deskripsi':c.deskripsi, 'coa':c.coa,'id':c.id,'id_cabang': id_cabang ,'header_parent':c.header_parent,
                        'saldo_awal':c.view_saldo_awal_gabungan_neraca(start_date),
                        'saldo_akhir':  c.view_saldo_akhir_gabung_neraca(start_date,end_date)})
                elif c.coa == '30.00.00':
                    akun.append({'c':c,'deskripsi':c.deskripsi, 'coa':c.coa,'id':c.id,'id_cabang': id_cabang ,'header_parent':c.header_parent,
                        'saldo_awal':c.view_saldo_awal_gabungan_neraca(start_date),
                        'saldo_akhir': c.total_shu_cabang_laporan_gabungan(posisi_tgl) + c.shu_dibagikan(posisi_tgl) + \
                            c.hitung_modal_penyerta(posisi_tgl) })
                elif c.coa == '35.00.00':
                    akun.append({'c':c,'deskripsi':c.deskripsi, 'coa':c.coa,'id':c.id,'id_cabang': id_cabang ,'header_parent':c.header_parent,
                        'saldo_awal':c.view_saldo_awal_gabungan_neraca(start_date),
                        'saldo_akhir': c.total_shu_cabang_laporan_gabungan(posisi_tgl) + c.shu_dibagikan(posisi_tgl)})
                elif c.coa == '35.04.00':
                    akun.append({'c':c,'deskripsi':c.deskripsi, 'coa':c.coa,'id':c.id,'id_cabang': id_cabang ,'header_parent':c.header_parent,
                        'saldo_awal':c.view_saldo_awal_gabungan_neraca(start_date),
                        'saldo_akhir':  c.total_shu_cabang_laporan_gabungan(posisi_tgl)})
                else:
                    akun.append({'c':c,'deskripsi':c.deskripsi, 'coa':c.coa,'id':c.id,'id_cabang': id_cabang ,'header_parent':c.header_parent,
                        'saldo_awal':c.view_saldo_awal_gabungan_neraca(start_date),
                        'saldo_akhir':  c.view_saldo_akhir_gabung_neraca(start_date,end_date)})
                start_date = start_date
                end_date = end_date
                id_cabang = id_cabang
        else:
            for c in lb_akun :
                #if c.coa[0:1] == str(2) or c.coa[0:1] == str(30) or c.coa[0:1] == str(40) or c.coa[0:1] == str(6) :
                if c.jenis_laporan == 'P' :
                    akun.append({'c':c,'deskripsi':c.deskripsi, 'coa':c.coa,'id':c.id,'id_cabang': id_cabang ,'header_parent':c.header_parent,
                        'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),
                        'saldo_akhir': c.view_saldo_awal_gbg(id_cabang,start_date) + c.my_kredit_neraca(id_cabang,start_date,end_date)- \
                            c.my_debet_neraca(id_cabang,start_date,end_date)})
                elif c.coa == '30.00.00':
                    akun.append({'saldo_akhir':c.total_shu_cabang_laporan_gerai(id_cabang,posisi_tgl) + \
                          c.view_saldo_awal_gbg(id_cabang,start_date)+ c.my_debet_neraca(id_cabang,start_date,end_date)-\
                          c.my_kredit_neraca(id_cabang,start_date,end_date),
                          'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),\
                          'c':c,'deskripsi':c.deskripsi,'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent})
                #elif c.coa == '35.00.00':
                    #akun.append({'saldo_akhir':c.total_shu_cabang_laporan_gerai(id_cabang,posisi_tgl),
                        #'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),\
                        #'c':c,'deskripsi':c.deskripsi,'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent})
                elif c.coa == '35.00.00':
                    akun.append({'saldo_akhir':c.total_shu_cabang_laporan_gerai(id_cabang,posisi_tgl) + \
                        (c.view_saldo_awal_gbg(id_cabang,start_date)+ c.my_debet_neraca(id_cabang,start_date,end_date)-\
                            c.my_kredit_neraca(id_cabang,start_date,end_date)),
                        'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),\
                        'c':c,'deskripsi':c.deskripsi,'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent})
                elif c.coa == '35.04.00':
                    akun.append({'saldo_akhir':c.total_shu_cabang_laporan_gerai(id_cabang,posisi_tgl),
                        'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),\
                        'c':c,'deskripsi':c.deskripsi,'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent})
                else:
                    akun.append({'c':c,'deskripsi':c.deskripsi,'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent,
                        'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),\
                        'saldo_akhir': c.view_saldo_awal_gbg(id_cabang,start_date)+ c.my_debet_neraca(id_cabang,start_date,end_date)-\
                            c.my_kredit_neraca(id_cabang,start_date,end_date)})
                start_date = start_date
                end_date = end_date
                id_cabang = id_cabang
                
        template='report_baru/ledger/neraca.html'
        variable = RequestContext(request,{'akun':akun,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,'form':form,
                    #'neraca_saldo_akhir_count': (aktiva.neraca_saldo_count(id_cabang = id_cabang, start_date=start_date) + \
                        #aktiva.neraca_debet_count(id_cabang = id_cabang, start_date=start_date,end_date=end_date)) -\
                        #aktiva.neraca_kredit_count(id_cabang = id_cabang, start_date=start_date,end_date = end_date),
                    'neraca_saldo_akhir_count':(sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan =('A')).\
                        filter(id_cabang =id_cabang).filter(tgl_trans =(posisi_tgl))])),
                    'neraca_saldo_akhir_count_gabung':(sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan =('A')).\
                        filter(tgl_trans =(posisi_tgl))])),
                    #'total_saldo_akhir_ekopasi':sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan =('P')).\
                        #filter(id_cabang =id_cabang).filter(tgl_trans =(posisi_tgl))]) + \
                        #ekuitas.total_shu_cabang_laporan_gerai(id_cabang=id_cabang,posisi_tgl=posisi_tgl),
                    'total_saldo_akhir_ekopasi':(ekuitas.total_shu_cabang_laporan_gerai(id_cabang=id_cabang,posisi_tgl=posisi_tgl) +
                        sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan =('E')).\
                        filter(id_cabang =id_cabang).filter(tgl_trans =(posisi_tgl)).filter(id_coa__id = shu_dibagikan.id)])) +
                        (sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan =('E')).\
                        filter(id_cabang =id_cabang).filter(tgl_trans =(posisi_tgl)).filter(id_coa__id = modal_penyerta.id)])) +
                        (sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan =('P')).\
                        filter(id_cabang =id_cabang).filter(tgl_trans =(posisi_tgl))])),

                   'total_saldo_akhir_ekopasi_gabungan':(ekuitas.total_shu_cabang_laporan_gabungan(posisi_tgl=posisi_tgl) +
                        sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan =('E')).\
                        filter(tgl_trans =(posisi_tgl)).filter(id_coa__id = shu_dibagikan.id)])) +
                        (sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan =('E')).\
                        filter(tgl_trans =(posisi_tgl)).filter(id_coa__id = modal_penyerta.id)])) +
                        (sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan =('P')).\
                        filter(tgl_trans =(posisi_tgl))]))}) 
        return render_to_response(template,variable)

    elif  'id_cabang' in request.GET and request.GET['id_cabang'] and 'submit_dua' in request.GET:
        sekarang = datetime.date.today()
        tahun  = sekarang.year
        bulan = 1
        tanggal = 1        
        #if tahun == 2017:
            #tangga_awal = datetime.date(2017,3,1)
        #else:
            #tangga_awal = datetime.date(tahun,bulan,tanggal)
        #start_date = tangga_awal
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']
        tanggal_shu = parser.parse(end_date) + relativedelta(days=1)
        posisi_tgl = tanggal_shu.date()
        tanggal_saldo = parser.parse(end_date) - relativedelta(days=1)
        posisi_tgl_saldo = tanggal_saldo.date() 
        if id_cabang == '500' :
            sal = Tbl_TransaksiKeu.objects.filter(tgl_trans__year = thn).order_by('id')
            id_awal = sal[0]
            start_date = id_awal.tgl_trans
        else:
            sal = Tbl_TransaksiKeu.objects.filter(id_cabang = id_cabang,tgl_trans__year = thn).order_by('id')
            id_awal = sal[0]
            start_date = id_awal.tgl_trans

        if id_cabang == '500' :
            for c in lb_akun :
                if c.jenis_laporan == 'P' :
                    akun.append({'c':c,'deskripsi':c.deskripsi, 'coa':c.coa,'id':c.id,'id_cabang': id_cabang ,'header_parent':c.header_parent,
                        'saldo_awal':c.view_saldo_awal_gabungan_neraca(start_date),
                        'saldo_akhir':  c.view_saldo_akhir_gabung_neraca(start_date,end_date)})
                elif c.coa == '30.00.00':
                    akun.append({'c':c,'deskripsi':c.deskripsi, 'coa':c.coa,'id':c.id,'id_cabang': id_cabang ,'header_parent':c.header_parent,
                        'saldo_awal':c.view_saldo_awal_gabungan_neraca(start_date),
                        'saldo_akhir': c.total_shu_cabang_laporan_gerai(id_cabang,posisi_tgl) + c.view_saldo_akhir_gabung_neraca(start_date,end_date)})
                elif c.coa == '35.00.00':
                    akun.append({'c':c,'deskripsi':c.deskripsi, 'coa':c.coa,'id':c.id,'id_cabang': id_cabang ,'header_parent':c.header_parent,
                        'saldo_awal':c.view_saldo_awal_gabungan_neraca(start_date),
                        'saldo_akhir': c.total_shu_cabang_laporan_gabungan(posisi_tgl)})
                elif c.coa == '35.04.00':
                    akun.append({'c':c,'deskripsi':c.deskripsi, 'coa':c.coa,'id':c.id,'id_cabang': id_cabang ,'header_parent':c.header_parent,
                        'saldo_awal':c.view_saldo_awal_gabungan_neraca(start_date),
                        'saldo_akhir':  c.total_shu_cabang_laporan_gabungan(posisi_tgl)})
                else:
                    akun.append({'c':c,'deskripsi':c.deskripsi, 'coa':c.coa,'id':c.id,'id_cabang': id_cabang ,'header_parent':c.header_parent,
                        'saldo_awal':c.view_saldo_awal_gabungan_neraca(start_date),
                        'saldo_akhir':  c.view_saldo_akhir_gabung_neraca(start_date,end_date)})
                start_date = start_date
                end_date = end_date
                id_cabang = id_cabang
        else:
            for c in lb_akun :
                #if c.coa[0:1] == str(2) or c.coa[0:1] == str(30) or c.coa[0:1] == str(40) or c.coa[0:1] == str(6) :
                if c.jenis_laporan == 'P' :
                    akun.append({'c':c,'deskripsi':c.deskripsi, 'coa':c.coa,'id':c.id,'id_cabang': id_cabang ,'header_parent':c.header_parent,
                        'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),
                        'saldo_akhir': c.view_saldo_awal_gbg(id_cabang,start_date) + c.my_kredit_neraca(id_cabang,start_date,end_date)- \
                            c.my_debet_neraca(id_cabang,start_date,end_date)})
                elif c.coa == '30.00.00':
                    akun.append({'saldo_akhir':c.total_shu_cabang_laporan_gerai(id_cabang,posisi_tgl) + \
                          c.view_saldo_awal_gbg(id_cabang,start_date)+ c.my_debet_neraca(id_cabang,start_date,end_date)-\
                          c.my_kredit_neraca(id_cabang,start_date,end_date),
                          'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),\
                          'c':c,'deskripsi':c.deskripsi,'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent})
                #elif c.coa == '35.00.00':
                    #akun.append({'saldo_akhir':c.total_shu_cabang_laporan_gerai(id_cabang,posisi_tgl),
                        #'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),\
                        #'c':c,'deskripsi':c.deskripsi,'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent})
                elif c.coa == '35.00.00':
                    akun.append({'saldo_akhir':c.total_shu_cabang_laporan_gerai(id_cabang,posisi_tgl) + \
                        (c.view_saldo_awal_gbg(id_cabang,start_date)+ c.my_debet_neraca(id_cabang,start_date,end_date)-\
                            c.my_kredit_neraca(id_cabang,start_date,end_date)),
                        'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),\
                        'c':c,'deskripsi':c.deskripsi,'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent})
                elif c.coa == '35.04.00':
                    akun.append({'saldo_akhir':c.total_shu_cabang_laporan_gerai(id_cabang,posisi_tgl),
                        'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),\
                        'c':c,'deskripsi':c.deskripsi,'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent})
                else:
                    akun.append({'c':c,'deskripsi':c.deskripsi,'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent,
                        'saldo_awal': c.view_saldo_awal_gbg(id_cabang,start_date),\
                        'saldo_akhir': c.view_saldo_awal_gbg(id_cabang,start_date)+ c.my_debet_neraca(id_cabang,start_date,end_date)-\
                            c.my_kredit_neraca(id_cabang,start_date,end_date)})
                start_date = start_date
                end_date = end_date
                id_cabang = id_cabang

        template='report_baru/ledger/cetak_neraca.html'
        variable = RequestContext(request,{'akun':akun,'start_date':start_date,'end_date':end_date,'id_cabang':id_cabang,'form':form,
                    'neraca_saldo_akhir_count':(sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan =('A')).\
                        filter(id_cabang =id_cabang).filter(tgl_trans =(posisi_tgl))])),
                    #'neraca_saldo_akhir_count': (aktiva.neraca_saldo_count(id_cabang = id_cabang, start_date=start_date) + \
                        #aktiva.neraca_debet_count(id_cabang = id_cabang, start_date=start_date,end_date=end_date)) -\
                        #aktiva.neraca_kredit_count(id_cabang = id_cabang, start_date=start_date,end_date = end_date),
                    #'total_saldo_akhir_ekopasi':sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan =('P')).\
                        #filter(id_cabang =id_cabang).filter(tgl_trans =(posisi_tgl))]) + \
                        #ekuitas.total_shu_cabang_laporan_gerai(id_cabang=id_cabang,posisi_tgl=posisi_tgl),
                    'total_saldo_akhir_ekopasi':(ekuitas.total_shu_cabang_laporan_gerai(id_cabang=id_cabang,posisi_tgl=posisi_tgl) +
                        sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan =('E')).\
                        filter(id_cabang =id_cabang).filter(tgl_trans =(posisi_tgl)).filter(id_coa__id = shu_dibagikan.id)])) +
                        (sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan =('E')).\
                        filter(id_cabang =id_cabang).filter(tgl_trans =(posisi_tgl)).filter(id_coa__id = modal_penyerta.id)])) +
                        (sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan =('P')).\
                        filter(id_cabang =id_cabang).filter(tgl_trans =(posisi_tgl))])),

                    'total_saldo_akhir_ekopasi_gabungan':sum([a.saldo for a in Tbl_TransaksiKeu.objects.filter(id_coa__jenis_laporan =('P')).\
                        filter(tgl_trans =(posisi_tgl))]) + \
                        ekuitas.total_shu_cabang_laporan_gerai(id_cabang=id_cabang,posisi_tgl=posisi_tgl),})
        return render_to_response(template,variable)
    else:
        template='report_baru/ledger/neraca.html'
        variable = RequestContext(request,{'form':form,})
        return render_to_response(template,variable)

####LABA RUGI HARIAN
####LABA RUGI HARIAN
@login_required
def laba_rugi(request):
    #lb_akun = Tbl_Akun.objects.filter(view_unit__in=('300','0','1')).filter(jenis_laporan__in=('PO','BO','PNO','BNO')).order_by('coa')
    lb_akun = Tbl_Akun.objects.exclude(view_unit__in=('100','200')).filter(jenis_laporan__in=('PO','BO','PNO','BNO')).order_by('coa')
    pendapatan = Tbl_Akun.objects.get(pk = 406)
    pendapatan_non = Tbl_Akun.objects.get(pk = 540)
    beban = Tbl_Akun.objects.get(pk = 449)
    beban_non = Tbl_Akun.objects.get(pk = 547)
    t_debet = 0
    t_kredit = 0
    t_saldo_akhir = 0
    start_date = None
    end_date = None
    id_cabang = None
    akun =[]
    form = SearchForm()
    
    if  'id_cabang' in request.GET and request.GET['end_date'] and 'submit_satu' in request.GET:## Non Posting
        #start_date = datetime.date(2017,3,1)
        end_date = request.GET['end_date']
        id_cabang = request.GET['id_cabang']

        posisi = parser.parse(end_date) + relativedelta(days=1)
        posisi_tgl = posisi.date()
        #print posisi_tgl
        ### Tambahan Firman Untuk Mencari Salado yang pertama tiap tahun
        patokan_tgl_saldo_awal =end_date[0:4]
        thn = int(patokan_tgl_saldo_awal)
        if id_cabang == '500' :
            sal = Tbl_TransaksiKeu.objects.filter(tgl_trans__year = thn).order_by('id')
            id_awal = sal[0]
            start_date = id_awal.tgl_trans
        else:
            sal = Tbl_TransaksiKeu.objects.filter(id_cabang = id_cabang,tgl_trans__year = thn).order_by('id')
            id_awal = sal[0]
            start_date = id_awal.tgl_trans

        ### Akhir Tambahan
        ##Untuk Gabungan SALDO
        pendapatan1 = Tbl_TransaksiKeu.objects.filter(tgl_trans = (end_date)).filter(id_unit__in = (0,1,300)).filter(id_coa__jenis_laporan ='PO')
        pendapatan_non1 = Tbl_TransaksiKeu.objects.filter(tgl_trans = (end_date)).filter(id_unit__in = (0,1,300)).filter(id_coa__jenis_laporan ='PNO')
        beban1 = Tbl_TransaksiKeu.objects.filter(tgl_trans = (end_date)).filter(id_unit = (300)).filter(id_coa__jenis_laporan ='BO').filter(status_jurnal__in= ('2','3'))
        beban_non1 = Tbl_TransaksiKeu.objects.filter(tgl_trans = (end_date)).filter(id_unit__in = (0,1,300)).filter(id_coa__jenis_laporan ='BNO')
        ###REFISI TEDI 06 NOV 2016
        pd1 = Tbl_TransaksiKeu.objects.filter(tgl_trans = (start_date)).filter(id_unit__in = (0,1,300)).filter(id_coa__jenis_laporan ='PO')
        pd_non1 = Tbl_TransaksiKeu.objects.filter(tgl_trans = (start_date)).filter(id_unit__in = (0,1,300)).filter(id_coa__jenis_laporan ='PNO')
        bn1 = Tbl_TransaksiKeu.objects.filter(tgl_trans = (start_date)).filter(id_unit__in = (0,1,300)).filter(id_coa__jenis_laporan ='BO')
        bn_non1 = Tbl_TransaksiKeu.objects.filter(tgl_trans = (start_date)).filter(id_unit__in = (0,1,300)).filter(id_coa__jenis_laporan ='BNO')
        ###REFISI TEDI 06 NOV 2016


        ##Untuk Pergerai SALDO
        gr_pendapatan1 = Tbl_TransaksiKeu.objects.filter(tgl_trans = (posisi_tgl)).filter(id_unit__in = (0,1,300)).filter(id_cabang = id_cabang).filter(id_coa__jenis_laporan ='PO')
        gr_pendapatan_non1 = Tbl_TransaksiKeu.objects.filter(tgl_trans = (posisi_tgl)).filter(id_unit__in = (0,1,300)).filter(id_cabang = id_cabang).filter(id_coa__jenis_laporan ='PNO')
        gr_beban1 = Tbl_TransaksiKeu.objects.filter(tgl_trans = (posisi_tgl)).filter(id_unit__in = (0,1,300)).filter(id_cabang = id_cabang).filter(id_coa__jenis_laporan ='BO')
        gr_beban_non1 = Tbl_TransaksiKeu.objects.filter(tgl_trans = (posisi_tgl)).filter(id_unit__in = (0,1,300)).filter(id_cabang = id_cabang).filter(id_coa__jenis_laporan ='BNO')

        ##Untuk Gabungan Kredit Dan Debet
        kr_db_pend = Tbl_Transaksi.objects.filter(tgl_trans__range = (start_date,end_date)).filter(id_unit__in = (0,1,300)).filter(id_coa__jenis_laporan ='PO')
        kr_db_pend_non = Tbl_Transaksi.objects.filter(tgl_trans__range = (start_date,end_date)).filter(id_unit__in = (0,1,300)).filter(id_coa__jenis_laporan ='PNO')
        kr_db_beban = Tbl_Transaksi.objects.filter(tgl_trans__range = (start_date,end_date)).filter(id_unit__in = (0,1,300)).filter(id_coa__jenis_laporan ='BO')
        kr_db_beban_non = Tbl_Transaksi.objects.filter(tgl_trans__range = (start_date,end_date)).filter(id_unit__in = (0,1,300)).filter(id_coa__jenis_laporan ='BNO')

        ##Untuk Pergerai Kredit
        kr_db_gr_pend = Tbl_Transaksi.objects.filter(tgl_trans__range = (start_date,end_date)).filter(id_unit__in = (0,1,300)).filter(id_cabang = id_cabang).filter(id_coa__jenis_laporan ='PO')
        kr_db_gr_pend_non = Tbl_Transaksi.objects.filter(tgl_trans__range = (start_date,end_date)).filter(id_unit__in = (0,1,300)).filter(id_cabang = id_cabang).filter(id_coa__jenis_laporan ='PNO')
        kr_db_gr_beban = Tbl_Transaksi.objects.filter(tgl_trans__range = (start_date,end_date)).filter(id_unit__in = (0,1,300)).filter(id_cabang = id_cabang).filter(id_coa__jenis_laporan ='BO')
        kr_db_gr_beban_non = Tbl_Transaksi.objects.filter(tgl_trans__range = (start_date,end_date)).filter(id_unit__in = (0,1,300)).filter(id_cabang = id_cabang).filter(id_coa__jenis_laporan ='BNO')

        if id_cabang == '500' :
            for c in lb_akun :
                if  'id_cabang' in request.GET and request.GET['id_cabang']:
                    if  c.jenis_laporan == 'PO' or c.jenis_laporan =='PNO':
                        akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.kredit_shu_nonpos_lr_gabungan(id_cabang,start_date,end_date),\
                            'debet':c.debet_shu_nonpos_lr_gabungan(id_cabang,start_date,end_date),
                            'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent,
                            'saldo_awal': c.saldo_awal_nonposting_shu_lr_gabungan(id_cabang,start_date),
                            'saldo_akhir': c.saldo_awal_nonposting_shu_lr_gabungan(id_cabang,start_date) + \
                            c.kredit_shu_nonpos_lr_gabungan(id_cabang,start_date, end_date) - c.debet_shu_nonpos_lr_gabungan(id_cabang,start_date,end_date)})
                    elif  c.jenis_laporan == 'BO' or c.jenis_laporan =='BNO':
                        akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.kredit_shu_nonpos_lr_gabungan(id_cabang,start_date,end_date),\
                            'debet':c.debet_shu_nonpos_lr_gabungan(id_cabang,start_date,end_date),
                            'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent,
                            'saldo_awal': c.saldo_awal_nonposting_shu_lr_gabungan(id_cabang,start_date),
                            'saldo_akhir': c.saldo_awal_nonposting_shu_lr_gabungan(id_cabang,start_date) +\
                            c.debet_shu_nonpos_lr_gabungan(id_cabang,start_date,end_date)- c.kredit_shu_nonpos_lr_gabungan(id_cabang,start_date,end_date)})
                    start_date = start_date
                    end_date = end_date
                    id_cabang = id_cabang

                    s_pend1 = sum([c.saldo for c in pd1]) + sum([c.kredit for c in kr_db_pend]) - sum([c.debet for c in kr_db_pend])
                    s_pend2 = sum([c.saldo for c in pd_non1]) + sum([c.kredit for c in kr_db_pend_non]) - sum([c.debet for c in kr_db_pend_non])
                    s_trans_pend = (sum([c.kredit for c in kr_db_pend]) + sum([c.kredit for c in kr_db_pend]))
                    s_b1 = sum([c.saldo for c in bn1]) + (sum([c.debet for c in kr_db_beban]) - sum([c.kredit for c in kr_db_beban]))
                    s_bn2 = sum([c.saldo for c in bn_non1]) + (sum([c.debet for c in kr_db_beban_non]) - sum([c.kredit for c in kr_db_beban_non]))
                    s_beban = (sum([c.saldo for c in beban1 ]) + sum([c.saldo for c in beban_non1]))
                    s_trans_beban = (sum([c.debet for c in kr_db_beban]) + sum([c.debet for c in kr_db_beban_non]))
                    total_pendapatan = (s_pend1) + (s_pend2) 
                    total_beban = (s_b1) + (s_bn2)
                    pdp_kurang_beban = (s_pend1) + (s_pend2) -((s_b1) + (s_bn2))
            template1='report_baru/ledger/labarugi.html'
            variables = RequestContext(request,{'akun':akun,'total_debet':t_debet,'total_kredit':t_kredit,'total_saldo_akhir':t_saldo_akhir,
                'start_date':start_date,'id_cabang':id_cabang,'form':form,'end_date':end_date,
                'total_lr_pdp_saldo_akhir': total_pendapatan,
                'total_lr_beban_saldo_akhir': total_beban,
                'total_lr_pdp_beban_saldo_akhir': pdp_kurang_beban})
                
            return render_to_response(template1,variables)
        else:       
            for c in lb_akun : 
                if  'id_cabang' in request.GET and request.GET['id_cabang']:
                    #if  c.coa[0:2] == str(40) or c.coa[0:2] == str(41) or c.coa[0:2] == str(60) or c.coa[0:2] == str(61):
                    if c.jenis_laporan == 'PO' or c.jenis_laporan =='PNO':
                        akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.kredit_shu_nonpos_cabang(id_cabang,start_date,end_date),\
                            'debet':c.debet_shu_nonpos_cabang(id_cabang,start_date,end_date),
                            'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent,
                            'saldo_awal': c.saldo_awal_nonposting_shu(id_cabang,start_date),
                            'saldo_akhir': c.saldo_awal_nonposting_shu(id_cabang,start_date) + \
                            c.kredit_shu_nonpos_cabang(id_cabang,start_date, end_date) - \
                            c.debet_shu_nonpos_cabang(id_cabang,start_date,end_date)})
                    else:
                        akun.append({'c':c,'deskripsi':c.deskripsi,'kredit':c.kredit_shu_nonpos_cabang(id_cabang,start_date,end_date),\
                            'debet':c.debet_shu_nonpos_cabang(id_cabang,start_date,end_date),
                            'coa':c.coa,'id':c.id,'id_cabang':id_cabang ,'header_parent':c.header_parent,
                            'saldo_awal': c.saldo_awal_nonposting_shu(id_cabang,start_date),
                            'saldo_akhir': c.saldo_awal_nonposting_shu(id_cabang,start_date) + c.debet_shu_nonpos_cabang(id_cabang,start_date,end_date)-\
                            c.kredit_shu_nonpos_cabang(id_cabang,start_date,end_date)})
                    start_date = start_date
                    end_date = end_date
                    id_cabang = id_cabang

                    s_pend = sum([c.saldo for c in gr_pendapatan1]) + sum([c.saldo for c in gr_pendapatan_non1])
                    s_trans_pend = (sum([c.kredit for c in kr_db_gr_pend]) + sum([c.kredit for c in kr_db_gr_pend_non]))
                    s_beban = (sum([c.saldo for c in gr_beban1]) + sum([c.saldo for c in gr_beban_non1]))
                    s_trans_beban = (sum([c.debet for c in kr_db_gr_beban]) + sum([c.debet for c in kr_db_gr_beban_non]))

            template='report_baru/ledger/labarugi.html'
            variable = RequestContext(request,{'akun':akun,'total_debet':t_debet,'total_kredit':t_kredit,'total_saldo_akhir':t_saldo_akhir,
                'start_date':start_date,'id_cabang':id_cabang,'form':form,\
                'total_lr_pdp_saldo_akhir': s_pend,'end_date':end_date,
                'total_lr_beban_saldo_akhir': s_beban,
                'total_lr_pdp_beban_saldo_akhir': s_pend - s_beban})#(s_pend + s_trans_pend) - (s_beban + s_trans_beban)})
            return render_to_response(template,variable)
    else:
        template =  'report_baru/ledger/labarugi.html'
        variable = RequestContext(request,{'akun':akun,'total_debet':t_debet,'total_kredit':t_kredit,'total_saldo_akhir':t_saldo_akhir,
            'start_date':start_date,'id_cabang':id_cabang,'form':form})
        return render_to_response(template,variable)
####LABA RUGI HARIAN
####LABA RUGI HARIAN



