from django.conf.urls.defaults import *
from gadai.appgadai.models import Tbl_Akun
from gadai.appkeuangan.keuangan.views import *


urlpatterns = patterns('',
    url(r'^posting_akhir_tahun/$', posting_akhir_tahun),
    url(r'^(?P<object_id>\d+)/input_posting_akhir_tahun/$',input_posting_akhir_tahun),
    url(r'^(?P<object_id>\d+)/eksekusi_posting_akhir_tahun/$',eksekusi_posting_akhir_tahun),
    url(r'^revisiposting/$', revisiposting),
    url(r'^eksekusi_revisiposting/$', eksekusi_revisiposting),
    url(r'^range_laporan_materai/$', range_laporan_materai),
    url(r'^cari_post/$', cari_post),
    url(r'^search_gerai_post/$', search_gerai_post),
    url(r'^(?P<object_id>\d+)/posting_gerai_tanggal/$', posting_gerai_tanggal),
    url(r'^(?P<object_id>\d+)/mastertiket_rak_pusat/$', mastertiket_rak_pusat),
    url(r'^(?P<object_id>\d+)/laporan_materai/$', laporan_materai),
    url(r'^posting_gerai_count/$', posting_gerai_count),
    url(r'^posisi_kas/$', posisi_kas),
    url(r'^(?P<object_id>\d+)/antar_bank_aktiva/$', antar_bank_aktiva),
    url(r'^(?P<object_id>\d+)/laporan_kas_besar/$', laporan_kas_besar),
    url(r'^posting_kas/$', posting_kas),
    url(r'^(?P<object_id>\d+)/posting_tanggal/$',posting_tanggal),
    url(r'^(?P<object_id>\d+)/tanggal_posting/$',tanggal_posting),
    url(r'^saldo_gerai/$', saldo_gerai),
    url(r'^create_saldo/$', create_saldo),
    url(r'^(?P<object_id>\d+)/(?P<jurnal>\d+)/edit_saldo/$', edit_saldo),
)

