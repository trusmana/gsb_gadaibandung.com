from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update, date_based

from gadai.appgadai.models import Biaya

from django.views.generic.simple import direct_to_template
from django.forms import ModelForm
from gadai.appgadai.biaya.views import *
from gadai.appgadai.models import *


urlpatterns = patterns('',
    url(r'^(?P<object_id>\d+)/hapus_jurnal_jurnal/$', hapus_jurnal_jurnal),
    url(r'^(?P<object_id>\d+)/hapus_jurnal/$', hapus_jurnal),
    url(r'^$',  list),
    url(r'^(?P<object_id>\d+)/show/$',show),
    url(r'^add/$',add),
    url(r'^(?P<object_id>\d+)/edit/$', create_update.update_object, {'form_class': BiayaForm, 'template_name': 'biaya/edit.html'}),
    url(r'^biaya_post/add/$', biaya_post),
    url(r'^biaya_post/add_post_pusat/$', biaya_post_pusat),
)
