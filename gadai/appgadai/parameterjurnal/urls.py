from django.conf.urls.defaults import *
from gadai.appgadai.models import *
import datetime
from gadai.appgadai.parameterjurnal.views import *
from django.views.generic import list_detail, create_update, date_based

urlpatterns = patterns('',
    url(r'^jurnal_biaya/$',jurnal_biaya),
    url(r'^add/$', add),
    url(r'^(?P<object_id>\d+)/hapus_jurnal/$', hapus_jurnal),
    url(r'^(?P<object_id>\d+)/edit/$', create_update.update_object, {'form_class': BiayaMapperForm, 'template_name': 'keuangan/parameter/edit.html'}),
    url(r'^jurnal_panjar/$',jurnal_panjar),
    url(r'^add_panjar/$', add_panjar),
    url(r'^add_parameter_materai/$',add_parameter_materai),
    url(r'^jurnal_materai/$',jurnal_materai),
    url(r'^(?P<object_id>\d+)/hapus_jurnal_materai/$',hapus_jurnal_materai),
    url(r'^(?P<object_id>\d+)/edit_materai/$', create_update.update_object, {'form_class': MateraiMapperForm, 'template_name': 'keuangan/parameter/edit_materai.html'}),

)
