from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from gadai.appgadai.models import *
from django import forms
import os, string
from django.conf import settings
from gadai.appgadai.templatetags.terbilang import terbilang
from gadai.appgadai.templatetags.number_format import number_format
from gadai.appgadai.biaya.forms import BiayaForm
import datetime
import decimal
from gadai.appgadai.templatetags.number_format import number_format
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

def biaya_post_pusat(request):
    user = request.user
    for i in request.POST.getlist('id_pilih'):        
        gl = Jurnal.objects.get(id=(i))
        jurnal = gl.tbl_transaksi_set.filter(tgl_trans= datetime.date.today())
        for mutasi in jurnal:
            mutasi.status_jurnal = 2 
            #mutasi.deskripsi = gl.diskripsi 
            mutasi.save()         
            messages.add_message(request, messages.INFO, 'Jurnal Tersimpan') 
    return HttpResponseRedirect("/keuangan/%s/add_pusat/" % user.profile.gerai.kode_cabang)

def cari(request):
	rekening=request.GET['rekening']

	try:
		ag=AkadGadai.objects.get(id=int(rekening))
		return HttpResponseRedirect("/biaya/%s/show/" % ag.id)
	except:
		request.user.message_set.create(message="No rekening tidak ditemukan.")
		return HttpResponseRedirect("/biaya/")

def edit(request,object_id):
	biy=Biaya.objects.get(id=object_id)

	template='biaya/edit.html'
	variable = RequestContext(request,{'biy': biy})
	return render_to_response(template,variable)

def hapus_jurnal(request,object_id):
    user = request.user
    tbl = Jurnal.objects.get(id=object_id)
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Penghapusan Jurnal Berhasil')
    return HttpResponseRedirect("/biaya/%s/add/" % user.profile.gerai.kode_cabang)

def hapus_jurnal_jurnal(request,object_id):
    user = request.user
    tbl = Jurnal.objects.get(id=object_id)
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Penghapusan Jurnal Berhasil')
    return HttpResponseRedirect("/keuangan/%s/add_pusat/" % user.profile.gerai.kode_cabang)


def biaya_post(request):
    user = request.user
    for i in request.POST.getlist('id_pilih'):        
        gl = Jurnal.objects.get(id=(i))
        jurnal = gl.tbl_transaksi_set.filter(tgl_trans= datetime.date.today()).filter(jurnal__id =gl.id) 
        for mutasi in jurnal:
            mutasi.status_jurnal = 2  
            mutasi.save()         
            messages.add_message(request, messages.INFO, 'Jurnal Tersimpan') 
    return HttpResponseRedirect("/biaya/%s/add/" % user.profile.gerai.kode_cabang)

def show(request,object_id):
	ag = Biaya.objects.get(id=object_id)
	sekarang = datetime.datetime.now()
	template = 'biaya/show.html'
	variable = RequestContext(request, {
		'ag': ag})
	return render_to_response(template,variable)

def list(request):
	bea = Biaya.objects.all()
	paginator = Paginator(bea, 50)

	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		bea = paginator.page(page)
	except (EmptyPage, InvalidPage):
		bea = paginator.page(paginator.num_pages)

	template='biaya/index.html'
	variable = RequestContext(request,{'bea': bea})
	return render_to_response(template,variable)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def add(request):
	sekarang = datetime.date.today()
        user = request.user
        cab =  user.profile.gerai.kode_cabang
	c = cab
	bea = Tbl_Transaksi.objects.filter(tgl_trans=sekarang).filter(id_cabang=cab).filter(status_jurnal = 1L).\
	filter(jenis__in=( u'GL_GL_CABANG',u'GL_GL_PUSAT_UK',u'GL_GL_PUSAT',u'GL_GL_BIAYA_GERAI','GL_GL_CABANG_PENGEMBALIAN','PENGELUARAN_KE_GERAI',\
                'GL_GL_PENAMBAHAN_GERAI','GL_GL_PENAMBAHAN_BANK','GL_GL_PENAMBAHAN_KAS','GL_GL_PENGELUARAN_KAS_PUSAT','GL_GL_PENAMBAHAN_BANK_RAK',\
		'GL_GL_PENGEMBALIAN_GERAI','GL_GL_PENGEMBALIAN_PUSAT','GL_GL_PENAMBAHAN_SALDO','GL_GL_PENGELUARAN_BANK','Penerimaan Materai',\
                'GL_GL_PENGELUARAN_BANK_PUSAT','GL_GL_PENGELUARAN_KAS','GL_GL_PENAMBAHAN_PUSAT_BANK','GL_GL_PENGEMBALIAN_PUSAT_BANK',\
		'GL_GL_PENGEMBALIAN_UK','GL_GL_CABANG_UK','PENGELURAN_BANK_PUSAT','GL_GL_PENGELUARAN_BANK_RAK','GL_GL_PENGEMBALIAN_PUSAT_BANK_RAK',\
                'GL_GL_PENGEMBALIAN_SALDO_GERAI','GL_GL_PENGEMBALIAN_BANK_CABANG_RAK','GL_GL_PENGELUARAN_PUSAT_BANK','GL_GL_CABANG_ADM_BANK'))

	if request.method == "POST":
		form = BiayaForm(request.POST)
		if form.is_valid():
			#gerai = form.cleaned_data['gerai']
			tanggal = form.cleaned_data['tanggal']
			listrik = form.cleaned_data['listrik']
			ket_listrik = form.cleaned_data['ket_listrik']
			pdam  = form.cleaned_data['pdam']
			ket_pdam = form.cleaned_data['ket_pdam']
			telpon = form.cleaned_data['telpon']
			ket_telpon = form.cleaned_data['ket_telpon']
			majalah = form.cleaned_data['majalah']
			ket_majalah = form.cleaned_data['ket_majalah']
			penambahan_saldo = form.cleaned_data['penambahan_saldo']
			ket_penambahan_saldo = form.cleaned_data['ket_penambahan_saldo']
			pengembalian_saldo = form.cleaned_data['pengembalian_saldo']
			ket_pengembalian_saldo = form.cleaned_data['ket_pengembalian_saldo']
			penambahan_uk = form.cleaned_data['penambahan_uk']
			ket_penambahan_uk = form.cleaned_data['ket_penambahan_uk']
			pengembalian_uk = form.cleaned_data['pengembalian_uk']
			ket_pengembalian_uk = form.cleaned_data['ket_pengembalian_uk']

			palkir = form.cleaned_data['palkir']
			ket_palkir = form.cleaned_data['ket_palkir']
			bbm = form.cleaned_data['bbm']
			ket_bbm = form.cleaned_data['ket_bbm']
			materai = form.cleaned_data['materai']
			ket_materai = form.cleaned_data['ket_materai']
			pemb_lingkungan = form.cleaned_data['pemb_lingkungan']
			ket_pemb_lingkungan = form.cleaned_data['ket_pemb_lingkungan']
			sumbangan = form.cleaned_data['sumbangan']
			ket_sumbangan = form.cleaned_data['ket_sumbangan']
			perlengkapan = form.cleaned_data['perlengkapan']
			ket_perlengkapan = form.cleaned_data['ket_perlengkapan']
			konsumsi = form.cleaned_data['konsumsi']
			ket_konsumsi = form.cleaned_data['ket_konsumsi']
			foto_copy  = form.cleaned_data['foto_copy']
			ket_foto_copy = form.cleaned_data['ket_foto_copy']
			lain_lain = form.cleaned_data['lain_lain']
			ket_lain_lain = form.cleaned_data['ket_lain_lain']
			js_trans = form.cleaned_data['js_trans']
			antar_gerai = form.cleaned_data['antar_gerai']
			js_trans_kembali = form.cleaned_data['js_trans_kembali']
			antar_gerai_kembali = form.cleaned_data['antar_gerai_kembali']

			jenis_transaksi_listrik	= form.cleaned_data['jenis_transaksi_listrik']
			jenis_transaksi_pdam	= form.cleaned_data['jenis_transaksi_pdam']
			jenis_transaksi_telepon	= form.cleaned_data['jenis_transaksi_telepon']
			jenis_transaksi_foto_copy	= form.cleaned_data['jenis_transaksi_foto_copy']
			jenis_transaksi_majalah	= form.cleaned_data['jenis_transaksi_majalah']
			jenis_transaksi_palkir	= form.cleaned_data['jenis_transaksi_palkir']
			jenis_transaksi_bbm	= form.cleaned_data['jenis_transaksi_bbm']
			jenis_transaksi_materai	= form.cleaned_data['jenis_transaksi_materai']
			jenis_transaksi_pemb_lingkungan	= form.cleaned_data['jenis_transaksi_pemb_lingkungan']
			jenis_transaksi_sumbangan	= form.cleaned_data['jenis_transaksi_sumbangan']
			jenis_transaksi_perlengkapan	= form.cleaned_data['jenis_transaksi_perlengkapan']
			jenis_transaksi_konsumsi	= form.cleaned_data['jenis_transaksi_konsumsi']
			jenis_transaksi_nilai_lain_lain= form.cleaned_data['jenis_transaksi_nilai_lain_lain']

                        #### TAMBAHAN BIAYA BANK DAN PENGIRIMAN
                        jenis_transaksi_biaya_bank = form.cleaned_data['jenis_transaksi_biaya_bank']
                        biaya_bank = form.cleaned_data['biaya_bank']
                        ket_biaya_bank = form.cleaned_data['ket_biaya_bank']
                        jenis_transaksi_pengiriman = form.cleaned_data['jenis_transaksi_pengiriman']
                        pengiriman = form.cleaned_data['pengiriman']
                        ket_pengiriman = form.cleaned_data['ket_pengiriman']
                        #### AKHIR TAMBAHAN BIAYA BANK DAN PENGIRIMAN

			biaya = Biaya(gerai = user.profile.gerai,tanggal = tanggal,listrik = listrik,ket_listrik = ket_listrik,\
                            pdam  = pdam,ket_pdam = ket_pdam,telpon = telpon,ket_telpon = ket_telpon,majalah = majalah,ket_majalah = ket_majalah,\
                            penambahan_saldo = penambahan_saldo,ket_penambahan_saldo = ket_penambahan_saldo,\
			    pengembalian_saldo = pengembalian_saldo,ket_pengembalian_saldo = ket_pengembalian_saldo,\
                            penambahan_uk = penambahan_uk,ket_penambahan_uk = ket_penambahan_uk,\
			    pengembalian_uk = pengembalian_uk,ket_pengembalian_uk = ket_pengembalian_uk,palkir = palkir,
			    ket_palkir = ket_palkir,bbm = bbm,ket_bbm = ket_bbm,
			    materai = materai,ket_materai = ket_materai,
			    foto_copy  = foto_copy,ket_foto_copy = ket_foto_copy,pemb_lingkungan= pemb_lingkungan,\
			    ket_pemb_lingkungan = ket_pemb_lingkungan,
			    sumbangan  = sumbangan,ket_sumbangan = ket_sumbangan,perlengkapan  = perlengkapan,ket_perlengkapan = ket_perlengkapan,
			    konsumsi  = konsumsi,ket_konsumsi = ket_konsumsi,\
			    js_trans_kembali=js_trans_kembali,\
			    antar_gerai=antar_gerai,js_trans = js_trans,antar_gerai_kembali = antar_gerai_kembali,\
			    jenis_transaksi_listrik= jenis_transaksi_listrik,jenis_transaksi_pdam= jenis_transaksi_pdam,\
				jenis_transaksi_telepon	= jenis_transaksi_telepon,jenis_transaksi_foto_copy= jenis_transaksi_foto_copy,
				jenis_transaksi_majalah	= jenis_transaksi_majalah,
				jenis_transaksi_palkir	= jenis_transaksi_palkir,jenis_transaksi_bbm	= jenis_transaksi_bbm,
				jenis_transaksi_materai	= jenis_transaksi_materai,jenis_transaksi_pemb_lingkungan= jenis_transaksi_pemb_lingkungan,\
				jenis_transaksi_sumbangan= jenis_transaksi_sumbangan,jenis_transaksi_konsumsi= jenis_transaksi_konsumsi,\
                                jenis_transaksi_perlengkapan= jenis_transaksi_perlengkapan,jenis_transaksi_biaya_bank = jenis_transaksi_biaya_bank,\
                                biaya_bank = biaya_bank,ket_biaya_bank = ket_biaya_bank,jenis_transaksi_pengiriman = jenis_transaksi_pengiriman,\
                                pengiriman = pengiriman,ket_pengiriman = ket_pengiriman)
			biaya.save()
			if biaya.jenis_transaksi_materai =='3':
				mat = Biaya_Materai_Cab(gerai = user.profile.gerai,tanggal = tanggal,saldo_awal = 0,saldo_akhir = 0,nilai = materai,\
                                    keterangan = 'Lain-Lain',norek = 0,status = 0)
				mat.save()

			####LISTRIK PER GERAI
			if biaya.listrik > 0 and biaya.jenis_transaksi_listrik == '2': #
                            jurnal_biaya_listrik_panjar(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (176)")
			if biaya.listrik > 0 and biaya.jenis_transaksi_listrik == '1':
                            jurnal_biaya_listrik(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (179)")
			####LISTRIK PER GERAI
			####BIAAYA BBM PANJAR DAN KAS
			if biaya.bbm > 0 and biaya.jenis_transaksi_bbm == '2':#
                            jurnal_biaya_bbm_panjar(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (184)")
			if biaya.bbm > 0 and biaya.jenis_transaksi_bbm == '1' :
			    jurnal_biaya_bbm(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (187)")
			####BIAYA BBM PANJAR DAN KAS
			if biaya.foto_copy > 0 and biaya.jenis_transaksi_foto_copy == '2':#
                            jurnal_biaya_foto_copy_panjar(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (191)")
			if biaya.foto_copy > 0 and biaya.jenis_transaksi_foto_copy == '1':
			    jurnal_biaya_foto_copy(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (194)")
                        ####BIAYA FOTOCOPY PANJAR DAN KA
			if biaya.pdam > 0 and biaya.jenis_transaksi_pdam == '2':#
                            jurnal_biaya_pdam_panjar(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (198)")
			if biaya.pdam > 0 and biaya.jenis_transaksi_pdam == '1':
			    jurnal_biaya_pdam(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (201)")
			####BIAYA PDAM PANJAR DAN KAS

			if biaya.telpon > 0 and biaya.jenis_transaksi_telepon == '2':
                            jurnal_biaya_telpon_panjar(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (206)")
			if biaya.telpon > 0 and biaya.jenis_transaksi_telepon == '1':
			    jurnal_biaya_telpon(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (209")
			####BIAYA TELEPON PANJAR DAN KAS

			if biaya.majalah > 0 and biaya.jenis_transaksi_majalah == '2':#
                            jurnal_biaya_majalah_panjar(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (214)")
			if biaya.majalah > 0 and biaya.jenis_transaksi_majalah == '1':
                            jurnal_biaya_majalah(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (217)")
			####MAJALAH per gerai

			####air minum per gerai

			if biaya.palkir > 0 and biaya.jenis_transaksi_palkir == '2':#
                            jurnal_biaya_palkir_panjar(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (224)")
			if biaya.palkir > 0 and biaya.jenis_transaksi_palkir == '1':
                            jurnal_biaya_parkir(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (227)")
			####parkir per gerai


			####pulsa per gerai
			if biaya.materai> 0 and biaya.jenis_transaksi_materai== '2':#
                            jurnal_biaya_materai_panjar(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (234)")
			if biaya.materai > 0 and biaya.jenis_transaksi_materai== '1':
                            jurnal_biaya_materai(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (237)")
			if biaya.materai > 0 and biaya.jenis_transaksi_materai=='3':
                            jurnal_biaya_materai_lain_lain(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (240)")

			####materai per gerai

			if biaya.pemb_lingkungan> 0 and biaya.jenis_transaksi_pemb_lingkungan== '2':#
                            jurnal_biaya_pemb_lingkungan_panjar(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (246)")
			if biaya.pemb_lingkungan > 0 and biaya.jenis_transaksi_pemb_lingkungan == '1':
                            jurnal_biaya_pemb_lingkungan(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (249)")
			###sumbangan
			if biaya.sumbangan > 0 and biaya.jenis_transaksi_sumbangan== '2':#
                            jurnal_biaya_sumbangan_panjar(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (253)")
			if biaya.sumbangan > 0 and biaya.jenis_transaksi_sumbangan== '1':
                            jurnal_biaya_sumbangan(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (256)")
			####sumbangan per gerai

			###perlengkapan
			if biaya.perlengkapan> 0 and biaya.jenis_transaksi_perlengkapan== '2':#
                            jurnal_biaya_perlengkapan_panjar(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (262)")
			####perlengkapan per gerai
                        if biaya.perlengkapan > 0 and biaya.jenis_transaksi_perlengkapan== '1' :
                            jurnal_biaya_perlengkapan(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (266)")
			####perlengkapan per gerai

			###konsumsi
			if biaya.konsumsi> 0 and biaya.jenis_transaksi_konsumsi== '2':#
                            jurnal_biaya_konsumsi_panjar(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (272)")
			if biaya.konsumsi > 0 and biaya.jenis_transaksi_konsumsi== '1' :
                            jurnal_biaya_konsumsi(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (275)")
			####sumbangan per gerai

			

			#####penambahan uang muka dan Pengembalian REGINA
			if biaya.penambahan_uk > 0 :#
                            jurnal_biaya_penambahan_uk(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (283)")
			if biaya.pengembalian_uk > 0 :#
                            jurnal_biaya_pengembalian_uk(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (286)")
                        #####pengembalian UK
			###Penambahan SALDO BANK DAN KAS
                        if biaya.penambahan_saldo > 0 and biaya.js_trans == 'BANK':# 
                            jurnal_biaya_penambahan_saldo_bank_debet_kredit(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (291)")
			if biaya.penambahan_saldo > 0 and biaya.js_trans == 'KAS' and biaya.antar_gerai != user.profile.gerai:#
                            jurnal_biaya_penambahan_saldo_kas_debet_kredit(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (294)")
                        if biaya.penambahan_saldo > 0 and biaya.js_trans == 'KAS' and biaya.antar_gerai == user.profile.gerai:#
                            jurnal_biaya_penambahan_saldo_kas_debet_kredit_gerai(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (297)")
			###Penambahan SALDO BANK DAN KAS

			### PENGEMBALIAN SALDO BANK Dan KAS
                        if biaya.pengembalian_saldo > 0 and biaya.js_trans_kembali == 'BANK' and \
                            biaya.antar_gerai_kembali.kode_cabang != user.profile.gerai.kode_cabang and\
                            biaya.antar_gerai_kembali.kode_cabang  != '300':#
                            jurnal_biaya_pengembalian_saldo_antarbank_debet_bank_pusat(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (328)")
			if biaya.pengembalian_saldo > 0 and biaya.js_trans_kembali == 'BANK' and biaya.antar_gerai_kembali.kode_cabang  == '300':#
                            jurnal_biaya_pengembalian_saldo_antarbank_debet_bank_pusat_bank_rak(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (329)")
			if biaya.pengembalian_saldo > 0 and biaya.js_trans_kembali == 'KAS' and biaya.antar_gerai_kembali != user.profile.gerai\
                            and biaya.antar_gerai_kembali.kode_cabang  != '300' :#
                            jurnal_biaya_pengembalian_saldo_antarbank_debet_kas_pusat(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (306)")
                        if biaya.pengembalian_saldo > 0 and biaya.js_trans_kembali == 'KAS' and biaya.antar_gerai_kembali.kode_cabang  == '300':#
                            jurnal_biaya_pengembalian_saldo_antarbank_debet_bank_pusat_cabang(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (325)")
			### PENGEMBALIAN SALDO BANK Dan KAS

                        ##Tambahan Bank dan Pengiriman
                        if biaya.pengiriman> 0 and biaya.jenis_transaksi_pengiriman== '2':#
                            jurnal_biaya_pengiriman_panjar(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (348)")
                        if biaya.pengiriman > 0 and biaya.jenis_transaksi_pengiriman== '1' :
                            jurnal_biaya_pengiriman(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (351)")
	                if biaya.biaya_bank > 0 and biaya.jenis_transaksi_biaya_bank== '1':#
                            jurnal_biaya_adm_bank(biaya, request.user)
                            messages.add_message(request, messages.INFO,"JURNAL TELAH TERSIMPAN (355)")

			return HttpResponseRedirect('/biaya/%s/add/' % (cab))
		else:
			form  = BiayaForm()
			form.fields['gerai'].queryset = Tbl_Cabang.objects.filter(kode_cabang=cab)
		variables = RequestContext(request, {'form': form,'bea':bea,'c':object_id,'total_kredit': sum([p.kredit for p in bea]),'total_debet': sum([p.kredit for p in bea])})
		return HttpResponseRedirect('/biaya/%s/add/' % (cab))
	else:
		form  = BiayaForm()
		form.fields['gerai'].queryset = Tbl_Cabang.objects.filter(kode_cabang=cab)
	variables = RequestContext(request, {'form': form,'bea':bea,'c':cab,'total_kredit': sum([p.kredit for p in bea]),'total_debet': sum([p.kredit for p in bea])})
	return render_to_response('biaya/addbiaya.html', variables)



#### BIAYA ADM DAM PENGIRIMAN
def jurnal_biaya_adm_bank(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='adm_bank', cabang=user.profile.gerai)
    a_bank_debet = bm.coa_debet
    a_bank_kredit = bm.coa
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Adm Bank',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_biaya_bank)
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_CABANG_ADM_BANK"), id_coa = a_bank_debet,
        kredit = 0,debet = D((biaya.biaya_bank)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_CABANG_ADM_BANK"), id_coa = a_bank_kredit,
        debet = 0,kredit = D((biaya.biaya_bank)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_pengiriman(biaya, user):
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='pengiriman', cabang=user.profile.gerai)
    a_pengiriman_debet = bm.coa_debet
    a_pengiriman_kredit = bm.coa
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Pengiriman',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pengiriman)
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_pengiriman_debet,
        kredit = 0,debet = D((biaya.pengiriman)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_pengiriman_kredit,
        debet = 0,kredit = D((biaya.pengiriman)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_pengiriman_panjar(biaya, user):######panjar atau u" muka 30 april
    D = decimal.Decimal
    bm = BiayaMapper.objects.get(item='pengiriman', cabang=user.profile.gerai)
    a_pengiriman_debet = bm.coa_debet
    a_pengiriman_kredit = bm.coa_uk 
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pembayaran Uang Muka Pengiriman',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pengiriman)
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_pengiriman_debet,
        kredit = 0,debet = D((biaya.pengiriman)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_pengiriman_kredit,
        debet = 0,kredit = D((biaya.pengiriman)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_pengembalian_saldo_antarbank_debet_bank_pusat_bank_rak(biaya, user):
    D = decimal.Decimal
    bm = PenKasBankMapper.objects.get(item='pengembalian_saldo_antarbank_bank', cabang=user.profile.gerai,ke_cabang=biaya.antar_gerai_kembali,
        jenis = biaya.js_trans_kembali)
    a_pengembalian_saldo_debet = bm.coa
    a_pengembalian_saldo_kredit = bm.coa_kredit
    a_pengembalian_saldo_debet_jakarta = bm.coa_lawan
    a_pengembalian_saldo_kredit_jakarta = bm.coa_kredit_lawan
    a_rak_cabang =bm.debet_rak_cabang
    a_rak_pusat = bm.kredit_rak_pusat
    jurnal = Jurnal.objects.create(
            diskripsi= 'Pengeluaran ke Gerai %s melalui %s ' % (biaya.antar_gerai_kembali,biaya.js_trans_kembali),
            kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
            tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pengembalian_saldo)

    jurnal.tbl_transaksi_set.create(
            jenis = '%s' % ("GL_GL_PENGEMBALIAN_BANK_CABANG_RAK"), id_coa = a_pengembalian_saldo_debet,
            kredit = 0,debet = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
            id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
            jenis = '%s' % ("GL_GL_PENGEMBALIAN_BANK_CABANG_RAK"), id_coa = a_pengembalian_saldo_kredit,
            debet = 0,kredit = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
            id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    ####rak pusat
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengeluaran ke %s melalui %s ' % (biaya.antar_gerai_kembali ,biaya.js_trans_kembali ),\
        kode_cabang =user.profile.gerai.parent.kode_cabang,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pengembalian_saldo)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_RAK_PUSAT"), id_coa = a_pengembalian_saldo_debet_jakarta,
        kredit = 0,debet = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang_tuju = user.profile.gerai.kode_cabang,id_unit= 300,id_cabang = biaya.antar_gerai_kembali.kode_cabang )
        #id_cabang =user.profile.gerai.parent.kode_cabang,id_unit= 300,id_cabang_tuju =biaya.antar_gerai_kembali.kode_cabang )###untuk transaksi pusat status_jurnal ='2'

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_RAK_PUSAT"), id_coa = a_pengembalian_saldo_kredit_jakarta,
        debet = 0,kredit = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang_tuju =user.profile.gerai.kode_cabang,id_unit= 300,id_cabang =biaya.antar_gerai_kembali.kode_cabang )#status_jurnal ='2'###untuk transaksi pusat 



def jurnal_biaya_pengembalian_saldo_antarbank_debet_bank_pusat_cabang(biaya, user):
    D = decimal.Decimal
    bm = PenKasBankMapper.objects.get(item='pengembalian_saldo_antarbank_kas', cabang=user.profile.gerai,\
    ke_cabang = biaya.antar_gerai_kembali,jenis = biaya.js_trans_kembali)
    a_pengembalian_saldo_debet = bm.coa
    a_pengembalian_saldo_kredit = bm.coa_kredit
    a_rak_lawan_debet =bm.coa_lawan
    a_rak_lawan_kredit = bm.coa_kredit_lawan
    a_rak_debet_pusat =bm.debet_rak_cabang
    a_rak_kredit_pusat = bm.kredit_rak_pusat
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengeluaran melalui kas dari %s ke  %s ' % (user.profile.gerai,biaya.antar_gerai_kembali),
        kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pengembalian_saldo)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_SALDO_GERAI"), id_coa = a_pengembalian_saldo_debet,
        kredit = 0,debet = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_PENGEMBALIAN_SALDO_GERAI"), id_coa = a_pengembalian_saldo_kredit,
        debet = 0,kredit = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)


##### PENGEMBALIAN uang muka
def jurnal_biaya_pengembalian_uk(biaya, user):
        D = decimal.Decimal
        bm = UangMukaGeraiMapper.objects.get(item='2', cabang=user.profile.gerai)
        a_pengembalian_uk_debet = bm.debet_pengembalian_uk
        a_pengembalian_uk_kredit = bm.kredit_pengembalian_uk
        jurnal = Jurnal.objects.create(
                diskripsi= 'Pengembalian Uang Muka',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
                tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pengembalian_uk)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_PENGEMBALIAN_UK"), id_coa = a_pengembalian_uk_debet,
                kredit = 0,debet = D((biaya.pengembalian_uk)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_PENGEMBALIAN_UK"), id_coa = a_pengembalian_uk_kredit,
                debet = 0,kredit = D((biaya.pengembalian_uk)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

###Teddy jakarta Penambahan SALDO bank

def jurnal_biaya_penambahan_saldo_bank_debet_kredit(biaya, user):
        D = decimal.Decimal
        bm = PenKasBankMapper.objects.get(item='penambahan_saldo_debet_bank', cabang=user.profile.gerai,jenis = biaya.js_trans)
	a_penambahan_saldo_debet = bm.coa
        a_penambahan_saldo_kredit = bm.coa_kredit
        jurnal = Jurnal.objects.create(
                diskripsi= 'Penarikan Tunai dari rekening bank  %s ' % (biaya.antar_gerai),kode_cabang = biaya.gerai.kode_cabang,\
                object_id=biaya.id,
                tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_PENAMBAHAN_BANK"), id_coa = a_penambahan_saldo_debet,
                kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_PENAMBAHAN_BANK"), id_coa = a_penambahan_saldo_kredit,
                debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

###Teddy jakarta Penambahan SALDO bank

###Teddy jakarta Penambahan SALDO KAS
def jurnal_biaya_penambahan_saldo_kas_debet_kredit(biaya, user):
        D = decimal.Decimal
        bm = PenKasBankMapper.objects.get(item='penambahan_saldo_debet_kas', cabang=user.profile.gerai,jenis = biaya.js_trans)
        a_penambahan_saldo_debet = bm.coa
        a_penambahan_saldo_kredit = bm.coa_kredit

        jurnal = Jurnal.objects.create(
                diskripsi= 'Penerimaan Setoran Dari Gerai %s ' % (biaya.antar_gerai),kode_cabang = biaya.gerai.kode_cabang,\
                object_id=biaya.id,
                tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_PENAMBAHAN_KAS"), id_coa = a_penambahan_saldo_debet,
                kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_PENAMBAHAN_KAS"), id_coa = a_penambahan_saldo_kredit,
                debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_penambahan_saldo_kas_debet_kredit_gerai(biaya, user):
        D = decimal.Decimal
        bm = PenKasBankMapper.objects.get(item='penambahan_saldo_debet_kas', cabang=user.profile.gerai,jenis = biaya.js_trans)
        a_penambahan_saldo_debet = bm.coa
        a_penambahan_saldo_kredit = bm.coa_kredit

        jurnal = Jurnal.objects.create(
                diskripsi= 'Penarikan Setoran Dari Bank %s ' % (biaya.antar_gerai),kode_cabang = biaya.gerai.kode_cabang,\
                object_id=biaya.id,
                tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_saldo)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_PENAMBAHAN_KAS"), id_coa = a_penambahan_saldo_debet,
                kredit = 0,debet = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_PENAMBAHAN_KAS"), id_coa = a_penambahan_saldo_kredit,
                debet = 0,kredit = D((biaya.penambahan_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =user.profile.gerai.kode_cabang,id_unit= 300)

###Teddy jakarta Penambahan SALDO KAS


#####PENGEMBALIAN SALDO BANK DAN KAS
def jurnal_biaya_pengembalian_saldo_antarbank_debet_bank_pusat(biaya, user):
    D = decimal.Decimal
    bm = PenKasBankMapper.objects.get(item='pengembalian_saldo_antarbank_bank', cabang=user.profile.gerai,ke_cabang=biaya.antar_gerai_kembali,
        jenis = biaya.js_trans_kembali)
    a_pengembalian_saldo_debet = bm.coa
    a_pengembalian_saldo_kredit = bm.coa_kredit
    a_pengembalian_saldo_debet_jakarta = bm.coa_lawan
    a_pengembalian_saldo_kredit_jakarta = bm.coa_kredit_lawan
    a_rak_cabang =bm.debet_rak_cabang
    a_rak_pusat = bm.kredit_rak_pusat
    jurnal = Jurnal.objects.create(
            diskripsi= 'Pengeluaran ke Gerai %s melalui %s ' % (biaya.antar_gerai_kembali,biaya.js_trans_kembali),
            kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
            tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pengembalian_saldo)

    jurnal.tbl_transaksi_set.create(
            jenis = '%s' % ("GL_GL_PENGELUARAN_BANK_RAK"), id_coa = a_pengembalian_saldo_debet,
            kredit = 0,debet = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
            id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
            jenis = '%s' % ("GL_GL_PENGELUARAN_BANK_RAK"), id_coa = a_pengembalian_saldo_kredit,
            debet = 0,kredit = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
            id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
    
    #####Cabang Tuju 
    jurnal = Jurnal.objects.create(diskripsi= 'Penerimaan dari Gerai %s melalui %s ' % (biaya.gerai.nama_cabang,biaya.js_trans_kembali),
            kode_cabang = biaya.antar_gerai_kembali.kode_cabang,object_id=biaya.id,
            tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pengembalian_saldo)

    jurnal.tbl_transaksi_set.create(
            jenis = '%s' % ("GL_GL_PENAMBAHAN_BANK_RAK"), id_coa = a_pengembalian_saldo_debet_jakarta,
            kredit = 0,debet = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
            id_cabang =biaya.antar_gerai_kembali.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
            jenis = '%s' % ("GL_GL_PENAMBAHAN_BANK_RAK"), id_coa = a_pengembalian_saldo_kredit_jakarta,
            debet = 0,kredit = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
            id_cabang = biaya.antar_gerai_kembali.kode_cabang,id_unit= 300)
    ####rak pusat
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengeluaran ke %s melalui %s ' % (biaya.antar_gerai_kembali ,biaya.js_trans_kembali ),\
        kode_cabang =user.profile.gerai.parent.kode_cabang,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pengembalian_saldo)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_RAK_PUSAT"), id_coa = a_rak_cabang,
        kredit = 0,debet = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='2',tgl_trans =biaya.tanggal,
        id_cabang =user.profile.gerai.parent.kode_cabang,id_unit= 300,id_cabang_tuju =biaya.antar_gerai_kembali.kode_cabang )###untuk transaksi pusat

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_RAK_PUSAT"), id_coa = a_rak_pusat,
        debet = 0,kredit = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='2',tgl_trans =biaya.tanggal,
        id_cabang =user.profile.gerai.parent.kode_cabang,id_unit= 300,id_cabang_tuju =biaya.antar_gerai_kembali.kode_cabang )###untuk transaksi pusat 

def jurnal_biaya_pengembalian_saldo_antarbank_debet_kas_pusat(biaya, user):
    D = decimal.Decimal
    bm = PenKasBankMapper.objects.get(item='pengembalian_saldo_antarbank_kas', cabang=user.profile.gerai,\
    ke_cabang = biaya.antar_gerai_kembali,jenis = biaya.js_trans_kembali)
    a_pengembalian_saldo_debet = bm.coa
    a_pengembalian_saldo_kredit = bm.coa_kredit
    a_rak_lawan_debet =bm.coa_lawan
    a_rak_lawan_kredit = bm.coa_kredit_lawan
    a_rak_debet_pusat =bm.debet_rak_cabang
    a_rak_kredit_pusat = bm.kredit_rak_pusat
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengeluaran melalui kas dari %s ke  %s ' % (user.profile.gerai,biaya.antar_gerai_kembali),
        kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pengembalian_saldo)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("PENGELUARAN_KE_GERAI"), id_coa = a_pengembalian_saldo_debet,
        kredit = 0,debet = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("PENGELUARAN_KE_GERAI"), id_coa = a_pengembalian_saldo_kredit,
        debet = 0,kredit = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
        id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

    
    #######PUSAT
    ########RAK GERAI PUSAT
    jurnal = Jurnal.objects.create(
        diskripsi= 'Pengeluaran Antar Gerai %s melalui %s ' % (biaya.antar_gerai_kembali ,biaya.js_trans_kembali ),
        kode_cabang =user.profile.gerai.parent.kode_cabang,
        tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pengembalian_saldo)

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_RAK_PUSAT_CABANG"), id_coa = a_rak_debet_pusat,
        kredit = 0,debet = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='2',tgl_trans =biaya.tanggal,
        id_cabang =user.profile.gerai.parent.kode_cabang,id_unit= 300,id_cabang_tuju =user.profile.gerai.parent.kode_cabang )

    jurnal.tbl_transaksi_set.create(
        jenis = '%s' % ("GL_GL_RAK_PUSAT_CABANG"), id_coa = a_rak_kredit_pusat,
        debet = 0,kredit = D((biaya.pengembalian_saldo)),id_product = '4',status_jurnal ='2',tgl_trans =biaya.tanggal,
        id_cabang =user.profile.gerai.parent.kode_cabang,id_unit= 300,id_cabang_tuju =user.profile.gerai.parent.kode_cabang )
#####PENGEMBALIAN SALDO BANK dan Kas

#####PENAMBAHAN uang muka
def jurnal_biaya_penambahan_uk(biaya, user):
	D = decimal.Decimal
        bm =UangMukaGeraiMapper.objects.get(item='1', cabang=user.profile.gerai)
	a_penambahan_uk_kredit = bm.kredit_pengambilan_uk
	a_penambahan_uk_debet = bm.debet_pengambilan_uk
	#a_penambahan_uk_debet = get_object_or_404(Tbl_Akun, id=247L)
        #bm = BiayaMapper.objects.get(item='penambahan_uk', cabang=user.profile.gerai)
	#a_penambahan_uk_kredit = bm.coa
	#a_penambahan_uk_kredit = get_object_or_404(Tbl_Akun, id=7L)
	jurnal = Jurnal.objects.create(
		diskripsi= 'Pengambilan Uang Muka',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_penambahan_uk)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = a_penambahan_uk_debet,
		kredit = 0,debet = D((biaya.penambahan_uk)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_PUSAT_UK"), id_coa = a_penambahan_uk_kredit,
		debet = 0,kredit = D((biaya.penambahan_uk)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
#####PENAMBAHAN uang muka


####BIAYA LISTRIK PANJAR DAN KAS
def jurnal_biaya_listrik(biaya, user):
	D = decimal.Decimal
	bm = BiayaMapper.objects.get(item='listrik', cabang=user.profile.gerai)
	a_listrik_kredit = bm.coa
        a_listrik_debet = bm.coa_debet 
	#a_listrik_kredit = get_object_or_404(Tbl_Akun, id=7L)
	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran Listrik',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_listrik)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_listrik_debet,
		kredit = 0,debet = D((biaya.listrik)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_listrik_kredit,
		debet = 0,kredit = D((biaya.listrik)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_listrik_panjar(biaya, user):######panjar atau u" muka 30 april
	D = decimal.Decimal
        bm = BiayaMapper.objects.get(item='listrik', cabang=user.profile.gerai)
	a_listrik_debet = bm.coa_debet
	a_listrik_kredit = bm.coa_uk
	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran Uang Muka Listrik',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_listrik)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_listrik_debet,
		kredit = 0,debet = D((biaya.listrik)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_listrik_kredit,
		debet = 0,kredit = D((biaya.listrik)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
#####BIAYA LISTRIK PANJAR DAN KAS
'''
def jurnal_biaya_perlengkapan_panjar(biaya, user):######panjar atau u" muka 30 april
	D = decimal.Decimal
	a_listrik_debet = get_object_or_404(Tbl_Akun, id=521L)
	a_listrik_kredit = get_object_or_404(Tbl_Akun, id=247L)
	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran Uang Muka Perlengkapan',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_perlengkapan)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_listrik_debet,
		kredit = 0,debet = D((biaya.perlengkapan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_listrik_kredit,
		debet = 0,kredit = D((biaya.perlengkapan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
'''

###BBM PER GERAI
def jurnal_biaya_bbm(biaya, user):
        D = decimal.Decimal
        bm = BiayaMapper.objects.get(item='bbm', cabang=user.profile.gerai)
        a_bbm_kredit = bm.coa
        a_bbm_debet = bm.coa_debet
        jurnal = Jurnal.objects.create(
                diskripsi= 'Pembayaran BBM',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
                tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_bbm)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_bbm_debet,
                kredit = 0,debet = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_bbm_kredit,
                debet = 0,kredit = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300)


def jurnal_biaya_bbm_panjar(biaya, user):######panjar atau u" muka 30 april
	D = decimal.Decimal
        bm = BiayaMapper.objects.get(item='bbm', cabang=user.profile.gerai)
        a_bbm_debet = bm.coa_debet
        a_bbm_kredit = bm.coa_uk
	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran Uang Muka BBM',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_bbm)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_bbm_debet,
		kredit = 0,debet = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_bbm_kredit,
		debet = 0,kredit = D((biaya.bbm)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

###FOTOCOPY PER GERAI
def jurnal_biaya_foto_copy(biaya, user):
        D = decimal.Decimal
        bm = BiayaMapper.objects.get(item='fotocopy', cabang=user.profile.gerai)
        a_foto_copy_kredit = bm.coa
        a_foto_copy_debet  = bm.coa_debet 
        #a_foto_copy_kredit = get_object_or_404(Tbl_Akun, id=7L)
        jurnal = Jurnal.objects.create(
                diskripsi= 'Pembayaran Foto Copy',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
                tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_foto_copy)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_foto_copy_debet,
                kredit = 0,debet = D((biaya.foto_copy)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_foto_copy_kredit,
                debet = 0,kredit = D((biaya.foto_copy)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_foto_copy_panjar(biaya, user):######panjar atau u" muka 30 april
	D = decimal.Decimal
        bm = BiayaMapper.objects.get(item='fotocopy', cabang=user.profile.gerai)
	a_foto_copy_debet = bm.coa_debet
	a_foto_copy_kredit = bm.coa_uk
	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran Uang Muka Foto Copy ',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_foto_copy)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_foto_copy_debet,
		kredit = 0,debet = D((biaya.foto_copy)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_foto_copy_kredit,
		debet = 0,kredit = D((biaya.foto_copy)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

###PDAM PER GERAI
def jurnal_biaya_pdam(biaya, user):
	D = decimal.Decimal
        bm = BiayaMapper.objects.get(item='pdam', cabang=user.profile.gerai)
        a_pdam_kredit = bm.coa
        a_pdam_debet = bm.coa_debet
	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran PDAM',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pdam)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_pdam_debet,
		kredit = 0,debet = D((biaya.pdam)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_pdam_kredit,
		debet = 0,kredit = D((biaya.pdam)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_pdam_panjar(biaya, user):######panjar atau u" muka 30 april
	D = decimal.Decimal
        bm = BiayaMapper.objects.get(item='pdam', cabang=user.profile.gerai)
	a_pdam_debet = bm.coa_debet
	a_pdam_kredit = bm.coa_uk
	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran Uang Muka PDAM',
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pdam)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_pdam_debet,
		kredit = 0,debet = D((biaya.pdam)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_pdam_kredit,
		debet = 0,kredit = D((biaya.pdam)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

###Telepon PER GERAI
def jurnal_biaya_telpon(biaya, user):
	D = decimal.Decimal
        bm = BiayaMapper.objects.get(item='telepon', cabang=user.profile.gerai)
        a_telpon_kredit = bm.coa
	a_telpon_debet = bm.coa_debet
	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran Telpon',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_telpon)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_telpon_debet,
		kredit = 0,debet = D((biaya.telpon)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_telpon_kredit,
		debet = 0,kredit = D((biaya.telpon)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_telpon_panjar(biaya, user):######panjar atau u" muka 30 april
	D = decimal.Decimal
        bm = BiayaMapper.objects.get(item='telepon', cabang=user.profile.gerai)
        a_telpon_debet = bm.coa_debet
        a_telpon_kredit = bm.coa_uk
	#a_telpon_debet = get_object_or_404(Tbl_Akun, id=517L)
	#a_telpon_kredit = get_object_or_404(Tbl_Akun, id=247L)
	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran Uang Muka Telepon',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_telpon)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_telpon_debet,
		kredit = 0,debet = D((biaya.telpon)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_telpon_kredit,
		debet = 0,kredit = D((biaya.telpon)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

###Majalah PER GERAI
def jurnal_biaya_majalah(biaya, user):
        D = decimal.Decimal
        bm = BiayaMapper.objects.get(item='majalah', cabang=user.profile.gerai)
        a_majalah_debet = bm.coa_debet
        a_majalah_kredit = bm.coa
        jurnal = Jurnal.objects.create(
                diskripsi= 'Pembayaran Majalah',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
                tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_majalah)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_majalah_debet,
                kredit = 0,debet = D((biaya.majalah)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_majalah_kredit,
                debet = 0,kredit = D((biaya.majalah)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_majalah_panjar(biaya, user):######panjar atau u" muka 30 april
	D = decimal.Decimal
        bm = BiayaMapper.objects.get(item='majalah', cabang=user.profile.gerai)
        a_majalah_debet = bm.coa_debet
        a_majalah_kredit = bm.coa_uk

	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran Uang Muka Majalah',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_majalah)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_majalah_debet,
		kredit = 0,debet = D((biaya.majalah)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_majalah_kredit,
		debet = 0,kredit = D((biaya.majalah)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

###PARKIR PER GERAI
def jurnal_biaya_parkir(biaya, user):
        D = decimal.Decimal
        bm = BiayaMapper.objects.get(item='parkir', cabang=user.profile.gerai)
        a_parkir_kredit = bm.coa
        a_parkir_debet = bm.coa_debet

        jurnal = Jurnal.objects.create(
                diskripsi= 'Pembayaran Parkir',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
                tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_palkir)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_parkir_debet,
                kredit = 0,debet = D((biaya.palkir)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_parkir_kredit,
                debet = 0,kredit = D((biaya.palkir)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300)


def jurnal_biaya_palkir_panjar(biaya, user):######panjar atau u" muka 30 april
	D = decimal.Decimal
        bm = BiayaMapper.objects.get(item='parkir', cabang=user.profile.gerai)
        a_palkir_debet = bm.coa_debet
        a_palkir_kredit = bm.coa_uk
	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran Uang Muka Palkir',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_palkir)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_palkir_debet,
		kredit = 0,debet = D((biaya.palkir)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_palkir_kredit,
		debet = 0,kredit = D((biaya.palkir)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)


###MATERAI PER GERAI
def jurnal_biaya_materai(biaya, user):
	D = decimal.Decimal
        bm = MateraiMapper.objects.get(item='1', cabang=user.profile.gerai)
	a_materai_debet = bm.coa1
	a_persediaan_materai_kredit = bm.coa2
   
	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran Materai',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_materai)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_materai_debet,
		kredit = 0,debet = D((biaya.materai)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_persediaan_materai_kredit,#a_materai_kredit,
		debet = 0,kredit = D((biaya.materai)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_materai_panjar(biaya, user):######panjar atau u" muka 30 april
	D = decimal.Decimal
        bm = MateraiMapper.objects.get(item='2')
        a_materai_debet = bm.coa2
        a_materai_kredit = bm.coa3

	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran Uang Muka Materai',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_materai)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_materai_kredit,
                kredit = 0,debet = D((biaya.materai)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_materai_debet,
		debet = 0,kredit = D((biaya.materai)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)


def jurnal_biaya_materai_lain_lain(biaya, user):######panjar atau u" muka 30 april
	D = decimal.Decimal
        bm = MateraiMapper.objects.get(item='3')
        a_biaya_materai_debet = bm.coa3
        a_persediaan_materai_kredit = bm.coa4

	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran Uang Muka Materai',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_materai)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_biaya_materai_debet,
		kredit = 0,debet = D((biaya.materai)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_persediaan_materai_kredit,
		debet = 0,kredit = D((biaya.materai)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
###Pemb Lingkungan PER GERAI
def jurnal_biaya_pemb_lingkungan(biaya, user):
        D = decimal.Decimal
        #a_pemb_lingkungan_debet = get_object_or_404(Tbl_Akun, id=525L)
        bm = BiayaMapper.objects.get(item='lingkungan', cabang=user.profile.gerai)
        a_pemb_lingkungan_debet = bm.coa_debet
        a_pemb_lingkungan_kredit = bm.coa
        #a_pemb_lingkungan_kredit = get_object_or_404(Tbl_Akun, id=7L)
        jurnal = Jurnal.objects.create(
                diskripsi= 'Pembayaran Pembinaan Lingkungan',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
                tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pemb_lingkungan)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_pemb_lingkungan_debet,
                kredit = 0,debet = D((biaya.pemb_lingkungan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_pemb_lingkungan_kredit,
                debet = 0,kredit = D((biaya.pemb_lingkungan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_pemb_lingkungan_panjar(biaya, user):######panjar atau u" muka 30 april
	#D = decimal.Decimal
	#a_materai_debet = get_object_or_404(Tbl_Akun, id=525L)
	#a_materai_kredit = get_object_or_404(Tbl_Akun, id=247L)
        D = decimal.Decimal
        bm = BiayaMapper.objects.get(item='lingkungan', cabang=user.profile.gerai)
        a_materai_debet = bm.coa_debet #get_object_or_404(Tbl_Akun, id=527L)
        a_materai_kredit = bm.coa_uk
	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran Uang Muka Pembinaan Lingkungan',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_pemb_lingkungan)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_materai_debet,
		kredit = 0,debet = D((biaya.pemb_lingkungan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_materai_kredit,
		debet = 0,kredit = D((biaya.pemb_lingkungan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
####PEMB LINGKUNGAN panjar per gerai

###SUMBANGAN PER GERAI
def jurnal_biaya_sumbangan(biaya, user):
        D = decimal.Decimal
        bm = BiayaMapper.objects.get(item='sumbangan', cabang=user.profile.gerai)
        a_sumbangan_debet = bm.coa_debet
        a_sumbangan_kredit = bm.coa
        jurnal = Jurnal.objects.create(
                diskripsi= 'Pembayaran Sumbangan',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
                tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_sumbangan)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_sumbangan_debet,
                kredit = 0,debet = D((biaya.sumbangan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

        jurnal.tbl_transaksi_set.create(
                jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_sumbangan_kredit,
                debet = 0,kredit = D((biaya.sumbangan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
                id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_sumbangan_panjar(biaya, user):######panjar atau u" muka 30 april
	D = decimal.Decimal
        bm = BiayaMapper.objects.get(item='sumbangan', cabang=user.profile.gerai)
	a_materai_debet = bm.coa_debet #get_object_or_404(Tbl_Akun, id=527L)
	a_materai_kredit = bm.coa_uk #get_object_or_404(Tbl_Akun, id=247L)
	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran Uang Muka Sumbangan',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_sumbangan)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_materai_debet,
		kredit = 0,debet = D((biaya.sumbangan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_materai_kredit,
		debet = 0,kredit = D((biaya.sumbangan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
####SUMBANGAN panjar per gerai

###perlengkapan PER GERAI
def jurnal_biaya_perlengkapan(biaya, user):
	D = decimal.Decimal
	#a_perlengkapan_debet = get_object_or_404(Tbl_Akun, id=521L)
        bm = BiayaMapper.objects.get(item='perlengkapan', cabang=user.profile.gerai)
        a_perlengkapan_debet = bm.coa_debet
        a_perlengkapan_kredit = bm.coa
	#a_perlengkapan_kredit = get_object_or_404(Tbl_Akun, id=7L)
	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran Perlengkapan',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_perlengkapan)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_perlengkapan_debet,
		kredit = 0,debet = D((biaya.perlengkapan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_perlengkapan_kredit,
		debet = 0,kredit = D((biaya.perlengkapan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_perlengkapan_panjar(biaya, user):
        D = decimal.Decimal
        bm = BiayaMapper.objects.get(item='perlengkapan', cabang=user.profile.gerai)
        a_perlengkapan_debet = bm.coa_debet
        a_perlengkapan_kredit = bm.coa_uk

	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran Perlengkapan Panjar',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_perlengkapan)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_perlengkapan_debet,
		kredit = 0,debet = D((biaya.perlengkapan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_perlengkapan_kredit,
		debet = 0,kredit = D((biaya.perlengkapan)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
####perlengkapan per gerai

###konsumsi PER GERAI
def jurnal_biaya_konsumsi(biaya, user):
	D = decimal.Decimal
        bm = BiayaMapper.objects.get(item='konsumsi', cabang=user.profile.gerai)
        a_konsumsi_debet = bm.coa_debet
	a_konsumsi_kredit = bm.coa
	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran Konsumsi',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_konsumsi_debet,
		kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG"), id_coa = a_konsumsi_kredit,
		debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

def jurnal_biaya_konsumsi_panjar(biaya, user):######panjar atau u" muka 30 april
	D = decimal.Decimal
        bm = BiayaMapper.objects.get(item='konsumsi', cabang=user.profile.gerai)
        a_perlengkapan_debet = bm.coa_debet 
        a_perlengkapan_kredit = bm.coa_uk

	jurnal = Jurnal.objects.create(
		diskripsi= 'Pembayaran Uang Muka Konsumsi',kode_cabang = biaya.gerai.kode_cabang,object_id=biaya.id,
		tgl_trans = biaya.tanggal,cu = user, mu = user,nobukti=biaya.ket_konsumsi)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_materai_debet,
		kredit = 0,debet = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)

	jurnal.tbl_transaksi_set.create(
		jenis = '%s' % ("GL_GL_CABANG_UK"), id_coa = a_materai_kredit,
		debet = 0,kredit = D((biaya.konsumsi)),id_product = '4',status_jurnal ='1',tgl_trans =biaya.tanggal,
		id_cabang =biaya.gerai.kode_cabang,id_unit= 300)
###KOnsumsi panjar per gerai
