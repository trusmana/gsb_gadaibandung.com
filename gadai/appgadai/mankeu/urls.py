from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update, date_based
from gadai.appgadai.mankeu.views import *
from gadai.appgadai.models import *

urlpatterns = patterns('',
    url(r'^index/$', index),                       
    url(r'^approve_mankeu_all/$', approve_mankeu_all),
    url(r'^laba_rugi_month/$', laba_rugi_month),
    url(r'^neraca_pjb_month/$', neraca_pjb_month),                       
    url(r'^rekapitulasi_transaksi_gl_gl/$', rekapitulasi_transaksi_gl_gl),                       
    url(r'^$', list),
    url(r'^(?P<object_id>\d+)/approve_mankeu/$', approve_mankeu),
    url(r'^(?P<object_id>\d+)/verifikasi_mankeu/$', verifikasi_mankeu),
    url(r'^rekapitulasi_transaksi_gl_gl_nonkas/$', rekapitulasi_transaksi_gl_gl_nonkas),
)
