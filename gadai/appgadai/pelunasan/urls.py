from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update
from gadai.appgadai.models import *
from gadai.appgadai.pelunasan.views import *


urlpatterns = patterns('',
    url(r'^(?P<object_id>\d+)/kw_sbg_plns/$',kw_sbg_plns),
    url(r'^(?P<object_id>\d+)/kwlunas_val/$',kwlunas_val),
    url(r'^(?P<object_id>\d+)/kwlunas/$', kwlunas),
    url(r'^(?P<object_id>\d+)/kwlunas_kendaraan/$', kwlunas_kendaraan),
    url(r'^$', list),
    url(r'^arsip/$',  list_day),
    url(r'^rekapbulan/$',  prpj_bulan),
    url(r'^rekap_tahun/$',  list_year), 
    url(r'^(?P<object_id>\d+)/hari/$', rekaphari),
    url(r'^(?P<object_id>\d+)/rekapbulan/$', rekapbulan),
    url(r'^(?P<object_id>\d+)/edit/$', create_update.update_object, {'form_class': Edit_PelunasanForm, 'template_name': 'pelunasan/edit.html'}),
)

