from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.static import serve
from django.views.generic import list_detail, create_update
admin.autodiscover()
from django.conf import settings
import os
from gadai.appgadai.views import homepage

urlpatterns = patterns('',
    url(r'^pencairan/',include('gadai.appgadai.pencairan.urls')),
    url(r'^gudang/',include('gadai.appgadai.gudang.urls')),
    url(r'^admgudang/',include('gadai.appgadai.admgudang.urls')),
    url(r'^parameter/',include('gadai.appkeuangan.parameter.urls')),
    url(r'^rreport/',include('gadai.appkeuangan.report.urls')),
    url(r'^rkeuangan/',include('gadai.appkeuangan.keuangan.urls')),
    url(r'^parameterjurnal/',include('gadai.appgadai.parameterjurnal.urls')),
    url(r'^materaicabang/',include('gadai.appgadai.materaicabang.urls')),
    url(r'^kplgerai/',include('gadai.appgadai.kplgerai.urls')),
    url(r'^mankeu/',include('gadai.appgadai.mankeu.urls')),
    url(r'^kasirgerai/', include('gadai.appgadai.kasirgerai.urls')),
    url(r'^manop/',include('gadai.appgadai.manop.urls')),
    url(r'^accounts/',include('gadai.accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',homepage),
    url(r'^setting/',    include('gadai.appgadai.setting.urls')),
    url(r'^akadgadai/', include('gadai.appgadai.akadgadai.urls')),
    url(r'^gerai/', include('gadai.appgadai.gerai.urls')),
    url(r'^nasabah/', include('gadai.appgadai.nasabah.urls')),
    url(r'^taksir/', include('gadai.appgadai.taksir.urls')),
    url(r'^jurnal/',include('gadai.appgadai.jurnal.urls')),
    url(r'^barang/',include('gadai.appgadai.barang.urls')),
    url(r'^pelunasan/',include('gadai.appgadai.pelunasan.urls')),
    url(r'^biaya/',include('gadai.appgadai.biaya.urls')),
    url(r'^lelang/',include('gadai.appgadai.lelang.urls')),##firman
    url(r'^piutang/',include('gadai.appgadai.piutang.urls')),
    url(r'^permintaan/',include('gadai.appgadai.permintaan.urls')),
    url(r'^report/',include('gadai.appgadai.report.urls')),
    url(r'^keuangan/',include('gadai.appgadai.keuangan.urls')),
    url(r'^biayamaterai/',include('gadai.appgadai.biayamaterai.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', serve, {'document_root' : os.path.join(os.path.dirname(__file__),("static"))})
    )
