from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update, date_based
from django.views.generic.simple import direct_to_template
from django.forms import ModelForm
from gadai.appgadai.pencairan.views import *
from gadai.appgadai.models import *
from gadai.appgadai.pencairan.forms import *

urlpatterns = patterns('',
    url(r'^prd/param_produk/$',parameter_produk),
    url(r'^prd/param_laptop/$',parameter_laptop),
    url(r'^add_hp_1bulan/(?P<jenis>\d+)/(?P<jenis_barang>\d+)/$',add_hp_1bulan),
    url(r'^add_laptop_1bulan/(?P<jenis>\d+)/(?P<jenis_barang>\d+)/$',add_laptop_1bulan),
    url(r'^add_motor_3bulan/(?P<jenis>\d+)/(?P<jenis_barang>\d+)/$',add_motor_3bulan),
    url(r'^produk/$',produk),    
)


