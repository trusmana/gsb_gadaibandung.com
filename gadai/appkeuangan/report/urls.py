from django.conf.urls.defaults import *
from gadai.appgadai.models import *
from gadai.appkeuangan.report.views import *

urlpatterns = patterns('',
    url(r'^laporan_kembaligu/$', laporan_kembaligu),
    url(r'^(?P<object_id>\d+)/tanggal_posting_pusat/$', tanggal_posting_pusat),
    url(r'^(?P<object_id>\d+)/posting_tanggal_pusat/$', posting_tanggal_pusat),
    url(r'^rekapitulasi_transaksi_pusat/$', rekapitulasi_transaksi_pusat),
    url(r'^(?P<object_id>\d+)/hapus_jurnal/$', hapus_jurnal),
    url(r'^(?P<object_id>\d+)/show_refisi_jurnal/$', show_refisi_jurnal),
    url(r'^(?P<object_id>\d+)/hapus_jurnal_refisi/$', hapus_jurnal_refisi),
    url(r'^(?P<object_id>\d+)/edit_refisi_jurnal/$', edit_refisi_jurnal),
    url(r'^refisi_jurnal_harian/$', refisi_jurnal_harian),

    url(r'^index_keu/$', index_keu),
    url(r'^buku_besar_all_keu/$', buku_besar_all_keu),
    url(r'^buku_besar_keu/$', buku_besar),
    url(r'^neraca_percobaan_keu/$', neraca_percobaan),
    url(r'^neraca_keu/$', neraca),
    url(r'^laba_rugi_keu/$', laba_rugi),
    url(r'^(?P<object_id>\d+)/slip_setoran_titipan_gu/$',slip_setoran_titipan_gu),
    url(r'^(?P<object_id>\d+)/kembali_gu/$', kembaligu),
    #url(r'^baru_beda_barang/$', baru_beda_barang),
    #url(r'^(?P<object_id>\d+)/barang_beda/$',barang_beda),#############nasabah lama,barang sama   
)
