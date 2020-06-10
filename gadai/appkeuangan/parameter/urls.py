from django.conf.urls.defaults import *
from gadai.appgadai.models import Tbl_Akun
from gadai.appkeuangan.parameter.views import *


urlpatterns = patterns('',
    url(r'^(?P<object_id>\d+)/edit_aydamapper/$', edit_aydamapper),
    url(r'^aydamapper/$', aydamapper),
    url(r'^(?P<object_id>\d+)/edit_rak_kasir_plns/$', edit_rak_kasir_plns), 
    url(r'^rak_kasir_plns/$', rak_kasir_plns),
    url(r'^(?P<object_id>\d+)/edit_rak_pusat/$', edit_rak_pusat), 
    url(r'^rak_pusat/$', rak_pusat),
    url(r'^(?P<object_id>\d+)/edit_biaya_pusat/$', edit_biaya_pusat), 
    url(r'^biaya_pusat/$', biaya_pusat),
    url(r'^(?P<object_id>\d+)/edit_materai_pusat/$', edit_materai_pusat), 
    url(r'^materai_pusat/$', materai_pusat),
    url(r'^(?P<object_id>\d+)/edit_materai_mapper/$', edit_materai_mapper),    
    url(r'^materai_mapper/$', materai_mapper),
    url(r'^(?P<object_id>\d+)/edit_uangmuka_gerai/$', edit_uangmuka_gerai),    
    url(r'^uangmuka_gerai/$', uangmuka_gerai),
    url(r'^(?P<object_id>\d+)/edit_manage_akun/$', edit_manage_akun),    
    url(r'^manage_akun/$', manage_akun),
    url(r'^(?P<object_id>\d+)/edit_pelunasan_kasir/$', edit_pelunasan_kasir),
    url(r'^jurnal_pelunasan_kasir/$',jurnal_pelunasan_kasir),
    url(r'^(?P<object_id>\d+)/edit_jurnal_pelunasan_adm/$', edit_jurnal_pelunasan_adm),
    url(r'^jurnal_pelunasan_adm/$', jurnal_pelunasan_adm),
    url(r'^(?P<object_id>\d+)/edit_pencairan_adm/$', edit_pencairan_adm),    
    url(r'^pencairan_adm/$', pencairan_adm), 
    url(r'^(?P<object_id>\d+)/edit_gadai_ulang_adm/$', edit_gadai_ulang_adm),
    url(r'^gadai_ulang_adm/$',gadai_ulang_adm),
    url(r'^(?P<object_id>\d+)/edit_penjualan_barang/$', edit_penjualan_barang),
    url(r'^jurnal_penjualan_barang/$',jurnal_penjualan_barang),
    url(r'^(?P<object_id>\d+)/edit_pnks/$', edit_pnks),
    url(r'^jurnal_penambahan_kas_bank/$',jurnal_penambahan_kas_bank),
    url(r'^(?P<object_id>\d+)/edit_pencairan_kasir_bank/$', edit_pencairan_kasir_bank),
    url(r'^(?P<object_id>\d+)/edit_jurnal_kas_bank/$', edit_jurnal_kas_bank),
    url(r'^jurnal_pusat_kas_bank/$',jurnal_pusat_kas_bank),
    url(r'^pencairan_kasir_bank/$', pencairan_kasir_bank),
    url(r'^pencairan_kasir/$', pencairan_kasir),
    url(r'^gadai_ulang/$', gadai_ulang),  
    url(r'^(?P<object_id>\d+)/edit/$', edit),
    url(r'^(?P<object_id>\d+)/edit_pencairan_kasir/$', edit_pencairan_kasir),
    url(r'^jurnal_panjar/$',jurnal_panjar),
    url(r'^(?P<object_id>\d+)/hapus_jurnal/$', hapus_jurnal),
    url(r'^jurnal_biaya/$',jurnal_biaya),
    url(r'^(?P<object_id>\d+)/edit_biaya/$', edit_biaya),
    url(r'^(?P<object_id>\d+)/hapus_jurnal_biaya/$', hapus_jurnal_biaya),
)

