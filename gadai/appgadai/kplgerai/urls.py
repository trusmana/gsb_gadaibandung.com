from django.conf.urls.defaults import *
from django.views.generic import create_update
import urllib
from gadai.appgadai.models import Tbl_Akun
from gadai.appgadai.kplgerai.views import *

urlpatterns = patterns('',
    url(r'^price_list/$',price_list),
    url(r'^(?P<object_id>\d+)/verifikasi_kg_gu/$', verifikasi_kg_gu),
    url(r'^(?P<object_id>\d+)/approve_gu/$', approve_gu),
    url(r'^(?P<object_id>\d+)/app_edit/$',app_edit),
    url(r'^(?P<object_id>\d+)/edit_akad/$',edit_akad),
    url(r'^(?P<object_id>\d+)/reset_status_tolak/$', reset_status_tolak),
    url(r'^(?P<object_id>\d+)/data_approve_kplg/$', data_approve_kplg),
    url(r'^(?P<object_id>\d+)/verifikasi_kg_pencairan/$', verifikasi_kg_pencairan),
    url(r'^(?P<object_id>\d+)/approve_pencairan/$', approve_pencairan),
    url(r'^(?P<object_id>\d+)/buku_besar_cabang/$', buku_besar_cabang),
    url(r'^(?P<object_id>\d+)/list/$', list),
    url(r'^(?P<object_id>\d+)/neraca_percobaan/$', neraca_percobaan), 
    url(r'^(?P<object_id>\d+)/neraca/$', neraca),
    url(r'^(?P<object_id>\d+)/labarugi/$', labarugi),
    url(r'^(?P<object_id>\d+)/pencairan_gerai/$', pencairan_gerai),
    url(r'^(?P<object_id>\d+)/pelunasan_gerai/$', pelunasan_gerai),
    url(r'^all_transaksi/$',all_transaksi),
    url(r'^(?P<object_id>\d+)/approve_kpg_all/$', approve_kpg_all),
)
