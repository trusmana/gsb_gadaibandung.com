from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update
from gadai.appgadai.models import *
from gadai.appgadai.perpanjang.views import *


urlpatterns = patterns('',
    url(r'^(?P<object_id>\d+)/cetak/$', cetak),
    url(r'^(?P<object_id>\d+)/cetak_kendaraan/$', cetak_kendaraan),
    url(r'^$', list),
    url(r'^arsip/$',  list_day),
    url(r'^arsip_bulan/$',  list_month),
    url(r'^rekap_tahun/$',  list_year),
    url(r'^(?P<object_id>\d+)/hari/$', rekaphari),
    url(r'^terbit/(?P<year>\d{4})/(?P<month>\d{2})/csv/$', terbit_bulan_csv),
    url(r'^(?P<object_id>\d+)/edit/$', create_update.update_object, {'form_class': Edit_PerpanjangForm, 'template_name': 'perpanjang/edit.html'}),
    url(r'^(?P<object_id>\d+)/rekapbulan/$', rekapbulan),
)


