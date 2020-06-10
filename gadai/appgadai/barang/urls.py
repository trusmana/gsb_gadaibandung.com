from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update
from gadai.appgadai.models import *
from gadai.appgadai.barang.views import *
from gadai.appgadai.barang.forms import *

urlpatterns = patterns('',
    url(r'^(?P<object_id>\d+)/all/$', all),
    url(r'^(?P<object_id>\d+)/edit_barang/$', create_update.update_object, {'form_class': Edit_BarangForm, 'template_name': 'barang/edit_barang.html'}),
    url(r'^cari_norek/$',cari_norek),
    url(r'^(?P<object_id>\d+)/(?P<akad>\d+)/rak_pusat/$',rak_pusat),
    url(r'^(?P<object_id>\d+)/(?P<akad>\d+)/rak_input/$',rak_input),
    url(r'^(?P<object_id>\d+)/tampil_cari/$',tampil_cari),
    url(r'^(?P<object_id>\d+)/edit/$', edit),
    url(r'^caribarang/$', caribarang),
    url(r'^caribrg/$', caribrg),
    url(r'^(?P<object_id>\d+)/tampil/$', tampil),
    url(r'^daftarjatuhtempo/$',daftarjatuhtempo),
    url(r'^cetakdaftarjatuhtempo/$',cetakdaftarjatuhtempo),
    url(r'^jatuhtempo_harian/$',jatuhtempo_harian),
    url(r'^jatuhtempo_bulanan/$',jatuhtempo_bulanan),
    url(r'^jatuhtempo_tahunan/$',jatuhtempo_tahunan),
    url(r'^(?P<object_id>\d+)/tampil/$',tampil),
    url(r'^$',  list),
    #url(r'^(?P<object_id>\d+)/rak/$', create_update.update_object, {'form_class': BarangForm, 'template_name': 'barang/rak.html'}),
    url(r'^(?P<object_id>\d+)/rak/$', rak),
    url(r'^(?P<object_id>\d+)/history/$', history),
    url(r'^(?P<object_id>\d+)/$', show),
    url(r'^(?P<object_id>\d+)/daftar_barang_gerai$', daftar_barang_gerai),
    url(r'^arsip/$',  list_day),
    url(r'^arsip_month/$',  list_month),
    url(r'^arsip_year/$',  list_year),
    url(r'^gudang/add/$', status_barang),
    #url(r'^barang_gerai$', list_detail.object_list, {'queryset': GeraiGadai.objects.all(), 'template_name': 'barang/barang_gerai.html'}),
    url(r'barang_gerai/$', barang_gerai),
    url(r'^(?P<object_id>\d+)/lebih/$', lebih),
    url(r'^(?P<object_id>\d+)/barang_aktif_gerai/$', barang_aktif_gerai), 
    url(r'^(?P<object_id>\d+)/barang_aktif_harian/$', barang_aktif_harian), 
    url(r'^(?P<object_id>\d+)/barang_lunas_gerai/$', barang_lunas_gerai), 
    url(r'^(?P<object_id>\d+)/barang_lunas_harian/$', barang_lunas_harian), 
    url(r'^(?P<object_id>\d+)/barang_lunas_bulanan/$', barang_lunas_bulanan), 
    ###rekap###
    url(r'^(?P<object_id>\d+)/dafnom/$', dafnom),
    url(r'^(?P<object_id>\d+)/dafnom_bulan/$', dafnom_bulan),
    url(r'^(?P<object_id>\d+)/dafnom_tahun/$', dafnom_tahun),
    url(r'^add/$',newBarang),###popup
    ###menu gerai non lunas
    #url(r'^(?P<object_id>\d+)/barangnonlunas/$', barangnonlunas),
    url(r'^barangnonlunas/$', barangnonlunas),
    url(r'^xls_jatuh_tempo/',xls_jatuh_tempo),
)

