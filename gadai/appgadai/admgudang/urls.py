from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update, date_based
from gadai.appgadai.admgudang.views import *

urlpatterns = patterns('',
    url(r'^(?P<object_id>\d+)/verifikasi_datagudang/$', verifikasi_datagudang),
    url(r'^(?P<object_id>\d+)/verifikasi_dataretur/$', verifikasi_dataretur),
    url(r'^data_retur_gaktif/$', data_retur_gaktif),
)
