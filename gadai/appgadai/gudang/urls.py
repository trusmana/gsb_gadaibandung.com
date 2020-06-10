from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update, date_based
from gadai.appgadai.gudang.views import *
from gadai.appgadai.models import *

urlpatterns = patterns('',
    url(r'data_gudang_barang_aktif/$',data_gudang_barang_aktif),
)
