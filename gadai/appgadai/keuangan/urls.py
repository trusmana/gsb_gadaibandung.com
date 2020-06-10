from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update, date_based
from gadai.appgadai.models import Biaya
from django.views.generic.simple import direct_to_template
from django.forms import ModelForm
from gadai.appgadai.keuangan.views import *
from gadai.appgadai.models import *


urlpatterns = patterns('',
    url(r'^(?P<object_id>\d+)/add_gerai/$',add_gerai),
    url(r'^(?P<object_id>\d+)/hapus_jurnal_penyetoran/$', hapus_jurnal_penyetoran),
    url(r'^(?P<object_id>\d+)/hapus_jurnal_add/$', hapus_jurnal_add),
    url(r'^(?P<object_id>\d+)/(?P<user>\d+)/mastertiket_gl_gl_pusat/$',mastertiket_gl_gl_pusat),
    url(r'^(?P<object_id>\d+)/hapus_jurnal_pusat/$', hapus_jurnal_pusat),
    url(r'^$',  list),
    url(r'^(?P<object_id>\d+)/show/$',show),
    url(r'^(?P<object_id>\d+)/add/$',add),
    url(r'^(?P<object_id>\d+)/add_pusat/$',add_pusat),
    url(r'^(?P<object_id>\d+)/edit/$', create_update.update_object, {'form_class': BiayasForm, 'template_name': 'biaya/edit.html'}),
    url(r'^biaya_post/add/$', biaya_post),
)
