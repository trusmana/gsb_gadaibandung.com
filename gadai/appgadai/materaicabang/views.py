from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import date_based
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from gadai.appgadai.models import *
from gadai.appgadai.materaicabang.forms import *

@login_required
@user_passes_test(lambda u: u.groups.filter(name='KASIR_GERAI'))
def materai_cabang(request):
    user = request.user
    cab =  user.profile.gerai.kode_cabang
    sekarang  = datetime.date.today()
    saldo_gerai= Tbl_TransaksiKeu.objects.filter(id_cabang=cab,id_coa__coa__contains= '13.04.03',tgl_trans= sekarang,status_jurnal = 2)
    saldo =Tbl_TransaksiKeu.objects.filter(id_cabang=cab,jenis = 'Penerimaan Materai',tgl_trans= sekarang,debet__gt= 0,status_jurnal = 2)
    materai_pencairan = Tbl_Transaksi.objects.filter(id_cabang=cab,tgl_trans= sekarang,id_coa_id = 231,\
        status_jurnal = 2,jenis__in =('Pencairan','Pencairan_Barang_sama'))
    kiriman_materai_pusat = Tbl_Transaksi.objects.filter(id_cabang = cab,jenis = 'Penerimaan Materai',\
        id_coa__coa = '13.04.03',tgl_trans = sekarang)
    materai_lain_lain = Tbl_Transaksi.objects.filter(id_cabang=cab,tgl_trans=sekarang,jenis= 'Lain-Lain')
    variables = RequestContext(request, {'mat': saldo,'saldo_gerai':sum([a.saldo for a in saldo_gerai]),
        'kiriman_materai_pusat':kiriman_materai_pusat,
        'mat_lain_lain': materai_lain_lain,
        'mat_nilai_lain_lain':sum([a.kredit for a in materai_lain_lain]),
        'mat_pencairan':materai_pencairan,
        'mat_nilai_pencairan':sum([a.kredit for a in materai_pencairan]),
        'saldo': sum([a.debet for a in saldo])+ sum([a.saldo for a in saldo_gerai]) + sum([a.debet for a in kiriman_materai_pusat]),
        'saldo_akhir':(sum([a.debet for a in saldo])+ sum([a.saldo for a in saldo_gerai]) + sum([a.debet for a in kiriman_materai_pusat]) ) - sum([a.kredit for a in materai_pencairan]),
        })
    return render_to_response('materaicabang/materaicabang.html', variables)
