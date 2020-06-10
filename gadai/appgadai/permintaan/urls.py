from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update
from gadai.appgadai.models import *
from gadai.appgadai.permintaan.views import *
from gadai.appgadai.permintaan.forms import *

urlpatterns = patterns('',
    url(r'^cabang/cari/$', cabang_search),
    url(r'^update_permintaan_gudang/$', update_permintaan_gudang),
    url(r'^input_permintaan_gudang/$', input_permintaan_gudang),
    url(r'^$',  list),
    url(r'^arsip/$',  list_day),
    url(r'^permintaan/add/$',  permintaan_gudang),
    url(r'^(?P<object_id>\d+)/hari/$', rekapkirimhari),
    url(r'^arsip_month/$',  list_month),
    url(r'^rekap_tahun/$',  list_year),
    url(r'^(?P<object_id>\d+)/reset_status_barang_gudang/$', reset_status_barang_gudang),
)
