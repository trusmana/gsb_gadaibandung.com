from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update, date_based

from django.views.generic.simple import direct_to_template
from django.forms import ModelForm
from gadai.appgadai.gerai.views import *
from gadai.appgadai.models import *

urlpatterns = patterns('',
    url(r'^daftar_user/$',daftar_user),
    url(r'^aktifkan_user/$',aktifkan_user),
    url(r'^keluar/$',keluar),
    url(r'^(?P<object_id>\d+)/status_pencairan_gerai/$', status_pencairan_gerai),
    url(r'^filter_rekap/$',filter_rekap),
    url(r'^(?P<object_id>\d+)/cetak_status_barang/$',cetak_status_barang),
    url(r'^(?P<object_id>\d+)/status_barang_gerai/$',status_barang_gerai),
    url(r'^(?P<object_id>\d+)/plan_gerai/$',plan_jatuh_tempo_gerai),
    url(r'^(?P<object_id>\d+)/barang_sama_oto_manop/(?P<barang>\d+)/(?P<taksir>\d+)/$',barang_sama_oto_manop),
    url(r'^(?P<object_id>\d+)/pelunasan_gu_sbl/$',pelunasan_gu_sbl),
    url(r'^(?P<object_id>\d+)/batal_lunas_barangsama/(?P<barang>\d+)/(?P<taksir>\d+)/$',batal_lunas_barangsama),
    url(r'^baru_beda_barang/$', baru_beda_barang),
    url(r'^(?P<object_id>\d+)/barang_beda/$',barang_beda),#############nasabah lama,barang sama   
    url(r'^baru/$', baru),
    #url(r'^(?P<object_id>\d+)/barang_sama/$',barang_sama),#############nasabah lama,barang sama  
    url(r'^(?P<object_id>\d+)/barang_sama/(?P<barang>\d+)/(?P<taksir>\d+)/$',barang_sama),
    url(r'^(?P<object_id>\d+)/show/$',show),
    url(r'rekapunit/$', rekapunit),
    url(r'^(?P<object_id>\d+)/rekap/$', cetak_rekap), 
    url(r'^(?P<object_id>\d+)/rekapbln/$', rekap_bulan), 
    url(r'^(?P<object_id>\d+)/rekapneraca/$', neracaunit),
    url(r'^(?P<object_id>\d+)/piutang/$', piutang_bulan), 
    url(r'^(?P<object_id>\d+)/suratjalan/$',sjalan),
    ####modif
    url(r'^$',  list),
    url(r'^arsip/$',  list_day),
    url(r'^rekapbulan/$',  gerai_bulan),
    url(r'^(?P<object_id>\d+)/hari/$', rekaphari),
    url(r'^(?P<object_id>\d+)/rekapbulan/$', rekapbulan),
    url(r'^rekap_tahun/$',  list_year), 
    url(r'rekap_allgerai_harian/$', rekap_allgerai_harian),
    url(r'prpj_allgerai_harian/$', prpj_allgerai_harian),
    url(r'pelunasan_allgerai_harian/$', pelunasan_allgerai_harian),
    url(r'total_harian/$', total_harian),
    url(r'simulasi/$',simulasi),
    ###REQUEST MANOP GADAI REKAP PENCAIRAN PRPJ PLNS ALL GERAI (PAK DEDI) (02 APRIL 2013) 
    url(r'^pencairan_bulanan_allgerai/$', pencairan_bulanan_allgerai),
    url(r'prpj_bulanan_allgerai/$', prpj_bulanan_allgerai),
    url(r'plns_bulanan_allgerai/$', plns_bulanan_allgerai),
    ### firman 15 april 13
    url(r'rekap_biaya_harian/$', rekap_biaya_harian),
    url(r'rekap_pendapatan_gerai/$',rekap_pendapatan_gerai),
    url(r'rekap_pengeluaran_gerai/$',rekap_pengeluaran_gerai),
    url(r'^list_hari/$', list_hari),
    url(r'^list_bulan/$', list_bulan),
    url(r'^list_tahun/$', list_tahun),
    ###Permintaan gerai
    url(r'^permintaan/add/$', permintaan),
    url(r'^(?P<object_id>\d+)/hapus/$',hapus_permintaan),
    url(r'^(?P<object_id>\d+)/cetakminta/$',cetakminta),
)
