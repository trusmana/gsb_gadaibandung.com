from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update, date_based
from gadai.appgadai.manop.views import *
from gadai.appgadai.models import *
from gadai.appgadai.manop.report import views as report
from gadai.appgadai.manop.manage import views as manop
from gadai.appgadai.manop.dlapur import views as lapur
from gadai.appgadai.manop.daktif import views as aktif

urlpatterns = patterns('',
    url(r'(?P<pk>\d+)/(?P<barang>\d+)/(?P<check>\d+)/cetak_bap/$',aktif.cetak_bap),
    url(r'data_bap/$',aktif.data_bap),
    url(r'proses_ver/$',aktif.proses_ver),
    url(r'rekap_gu/$',manop.rekap_gu),
    url(r'(?P<object_id>\d+)/(?P<akad>\d+)/edit_nasabah_new/$',manop.edit_nasabah_new),
    url(r'(?P<object_id>\d+)/show_new/$',manop.show_new),
    url(r'(?P<pk>\d+)/(?P<object_id>\d+)/cek_kredit/$',aktif.cek_kredit),
    url(r'cek_kgaktif/$',aktif.cek_kgaktif),
    url(r'(?P<pk>\d+)/(?P<object_id>\d+)/show_data_bap/$',aktif.show_data_bap),
    url(r'(?P<pk>\d+)/input_bapna/$',aktif.input_bapna),
    url(r'data_kredit_kmr/$',aktif.data_kredit_kmr),
    url(r'sh_kondisi_lapur/$',lapur.sh_kondisi_lapur),
    url(r'(?P<pk>\d+)/show_data_ref/$',lapur.show_data_ref),
    url(r'(?P<pk>\d+)/sts_lpr/$',lapur.sts_lpr),
    url(r'dlapur/barang_pinjam/$',lapur.barang_pinjam),
    url(r'dlapur/lapur_barang_new/$',lapur.lapur_barang_new),
    url(r'manage/report_oto_pelunasan/$',manop.report_oto_pelunasan),
    url(r'manage/report_taksiran/$',manop.report_taksiran),
    url(r'(?P<object_id>\d+)/aktif_tombol_gu/$',manop.aktif_tombol_gu),
    url(r'(?P<object_id>\d+)/show_manop/$',manop.show_manop),
    url(r'manage/list_cari_baru/$',manop.list_cari_baru),
    url(r'manage/(?P<pk>\d+)/menu_update/$',manop.menu_update),
    url(r'manage/menu_item/$', manop.menu_item),
    url(r'all_data_cair/$', all_data_cair),
    url(r'pencairan_gerai_saja/$', pencairan_gerai_saja),
    url(r'^(?P<object_id>\d+)/menu_penjualan_ayda_esekusi/$',menu_penjualan_ayda_esekusi),
    url(r'^rekap_noa_baru/$', rekap_noa_baru),
    url(r'^(?P<object_id>\d+)/input_edit_sts_kw/$',input_edit_sts_kw),
    url(r'^(?P<object_id>\d+)/edit_sts_kw/$',edit_sts_kw),
    url(r'^menu_penjualan_ayda/$', menu_penjualan_ayda),
    url(r'^(?P<object_id>\d+)/penjualan_ayda/$', penjualan_ayda),
    url(r'^otorisasi_pelunasan_gu/$', otorisasi_pelunasan_gu),
    url(r'^(?P<object_id>\d+)/edit_view_gu/$', edit_view_gu),
    url(r'^(?P<object_id>\d+)/edit_manage_gerai/$', edit_manage_gerai),    
    url(r'^manage_gerai/$', manage_gerai),     
    url(r'^(?P<object_id>\d+)/edit_manage_userprofile/$', edit_manage_userprofile),    
    url(r'^manage_userprofile/$', manage_userprofile),    
    url(r'^(?P<object_id>\d+)/edit_manage_user/$', edit_manage_user),    
    url(r'^manage_user/$', manage_user),
    url(r'^cari/$', cari),
    url(r'^cari_jurnal/$', cari_jurnal),
    url(r'^(?P<object_id>\d+)/jurnal_ref/$', jurnal_ref),

    url(r'^(?P<object_id>\d+)/edit_view/$', edit_view),
    url(r'^$', list),
    url(r'^(?P<object_id>\d+)/oto_plns_manop/$', oto_plns_manop),
    url(r'^(?P<object_id>\d+)/menu_plns_manop/$', menu_plns_manop),
    url(r'^(?P<object_id>\d+)/pelunasan_manop/$', pelunasan_manop),
    url(r'^daftarpelunasan/$', daftarpelunasan),
    url(r'^otorisasi_pelunasan/$', otorisasi_pelunasan),
    url(r'^(?P<object_id>\d+)/update_status/$', update_status),
    url(r'^list_cari/$',list_cari),
    url(r'^laporan_rekap_dan_rinci/$',laporan_rekap_dan_rinci),
    url(r'^(?P<object_id>\d+)/delete/$',delete),
    url(r'lunasterjual_barang/$', lunasterjual_barang), 
    url(r'lapur_barang/$', lapur_barang), 
    url(r'rincian_lainlain/$', rincian_lainlain), 
    url(r'^reset_status_lainlain/$',reset_status_lainlain),
    url(r'aktif_lapur/$',rekap_barang_aktif_dan_lapur),
    url(r'barang_di_gerai/$', rincian_barang_di_gerai),
    url(r'^(?P<object_id>\d+)/show/$',show),
    url(r'^cari/$',cari),
    url(r'^list_nsb/$',list_nsb),
    url(r'^reset_status_hilang/$', reset_status_hilang),
    url(r'^reset_status/$', reset_status),
    url(r'rincian_jatuhtempo/$', rincian_jatuhtempo),
    url(r'rincian_hilang/$', rincian_hilang),
    url(r'rincian_piutang/$', rincian_piutang),
    url(r'rincian_lelang/$', rincian_lelang),
    url(r'^lunas/$', lunas),
    url(r'^cariplns/$', cariplns),
    url(r'^(?P<object_id>\d+)/update_status/$', update_status),
    url(r'^$', list),
    url(r'^list_cari/$',list_cari),
    url(r'^(?P<object_id>\d+)/lelang_manop/$', lelang_manop),
    url(r'pencairan_gerai/$', pencairan_gerai),
    url(r'perpanjangan_gerai/$',perpanjangan_gerai),
    url(r'pelunasan_gerai/$',pelunasan_gerai),
    url(r'total_harian_filter/$', total_harian_filter),
    url(r'total_harian_filter_new/$', report.total_harian_filter_new),
)
