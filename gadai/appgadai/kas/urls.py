from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update, date_based
from gadai.appgadai.models import MutasiKas, KasBank
from gadai.appgadai.kas.forms import MutasiKasForm
from gadai.appgadai.kas.views import rekening_show,mutasikas_add,mutasikas_bulan,rekening_pindahbuku
import datetime

MONTH_SHOW = 3 * 30
now = datetime.date.today()
since = now - datetime.timedelta(MONTH_SHOW)
date_list = MutasiKas.objects.filter(tanggal__gt=since).dates('tanggal', 'day')

cashflow_list = [{'tanggal': d,
        'penerimaan': sum([m.nilai for m in MutasiKas.objects.filter(tanggal=d) if m.is_debet]),
        'pengeluaran': sum([abs(m.nilai) for m in MutasiKas.objects.filter(tanggal=d) if not m.is_debet])} for d in date_list]


urlpatterns = patterns('',
    url(r'^$',  list_detail.object_list, {
        'queryset': MutasiKas.objects.all(),
        'template_name': 'kas/mutasikas_archive.html',
        'extra_context': {'cashflow_list': cashflow_list, 
            'date_list': MutasiKas.objects.dates('tanggal', 'month')}}),
    url(r'^add/$', mutasikas_add),
    url(r'^arsip/(?P<tahun>\d{4})/(?P<bulan>\d{2})/$', mutasikas_bulan),
    url(r'^rekening/(?P<object_id>\d+)/$', rekening_show),
    url(r'rekening/pindahbuku/', rekening_pindahbuku),
)
