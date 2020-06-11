from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update, date_based
from gadai.appgadai.models import AkadGadai
from django.views.generic.simple import direct_to_template
from django.forms import ModelForm
from gadai.appgadai.akadgadai.views import *
from gadai.appgadai.models import *
from gadai.appgadai.akadgadai.forms import *

urlpatterns = patterns('',
    url(r'^(?P<object_id>\d+)/upload_pk/$',upload_pk),
    url(r'^(?P<object_id>\d+)/hapus_dobel/$',hapus_dobel),
    url(r'^(?P<object_id>\d+)/eksekusi_hapus_dobel/$',eksekusi_hapus_dobel),
    url(r'^cari_sop/$', cari_sop),
    url(r'^tambah_sop/$', tambah_sop),

    url(r'^export_saldo/$', export_saldo),
    url(r'^(?P<object_id>\d+)/batal_lunas_saja/$', batal_lunas_saja),
    url(r'^(?P<object_id>\d+)/delete_akad/$',delete_akad),
    url(r'^(?P<object_id>\d+)/batal_cair_manop/$', batal_cair_manop),
    url(r'^data_tolak/$',data_tolak),
    url(r'^(?P<object_id>\d+)/kw_gu/$',kwitansi_gu),
    url(r'^(?P<object_id>\d+)/tampil_kondisi_barang/$',tampil_kondisi_barang),
    url(r'^(?P<object_id>\d+)/diskon_pelunasan/$', diskon_pelunasan),
    url(r'^(?P<object_id>\d+)/skl/$', skl),
    url(r'^import/$', import_ag),
    url(r'^cariplns/$', cariplns),
    url(r'^(?P<object_id>\d+)/plns/$', plns),
    url(r'^(?P<object_id>\d+)/pelunasan/$', pelunasan),
    url(r'^(?P<object_id>\d+)/kw_val/$',kw_val),
    url(r'^lunas/$', lunas),    
    
    url(r'^$',  list),
    url(r'^(?P<object_id>\d+)/show/$',show),
    url(r'^add/$',add),
    url(r'^hitung_jatuhtempo_perpanjang_2_kendaraan/$',hitung_jatuhtempo_perpanjang_2_kendaraan),    
    url(r'^(?P<object_id>\d+)/label/$',label),
    url(r'^(?P<object_id>\d+)/prints1/$',kw_sbg),
    url(r'^(?P<object_id>\d+)/kw_sbg_gu/$',kw_sbg_gu),
    url(r'^(?P<object_id>\d+)/prints2/$',kwitansi), 
    url(r'^(?P<object_id>\d+)/prints5/$',tterima),
    url(r'^(?P<object_id>\d+)/teguran/$',teguran),    
    url(r'^(?P<object_id>\d+)/perpanjang/$',perpanjang),
    url(r'^baru/$', baru),
    url(r'^cari/$',cari),
    url(r'^(?P<object_id>\d+)/batal_lunas/$', batal_lunas),
    url(r'^terbit_akad/(?P<year>\d{4})/(?P<month>\d{2})/csv/$', akad_terbit_bulan_csv),
    url(r'^terbit_prpj/(?P<year>\d{4})/(?P<month>\d{2})/csv/$', prpj_terbit_bulan_csv),
    url(r'^terbit_pelunasan/(?P<year>\d{4})/(?P<month>\d{2})/csv/$', pelunasan_terbit_bulan_csv),
    url(r'^(?P<object_id>\d+)/motor/$',kwitansi_motor),
    url(r'^(?P<object_id>\d+)/edit/$', create_update.update_object, {'form_class': Edit_AkadForm, 'template_name': 'akadgadai/edit.html'}),
    url(r'^(?P<object_id>\d+)/view_verifikasi_manop/$', view_verifikasi_manop),
    url(r'^(?P<object_id>\d+)/verifikasi_manop/$', verifikasi_manop),
    url(r'^(?P<object_id>\d+)/keanggotaan/$',keanggotaan),
    url(r'^(?P<object_id>\d+)/pengundurandiri/$',pengundurandiri),
    url(r'^(?P<object_id>\d+)/pk/$',pk),
    url(r'^(?P<object_id>\d+)/view_verifikasi_manop/$', view_verifikasi_manop),
    url(r'^(?P<object_id>\d+)/verifikasi_manop/$', verifikasi_manop),
)


