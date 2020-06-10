from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update, date_based
from django.views.generic.simple import direct_to_template
from django.forms import ModelForm
from gadai.appgadai.biayamaterai.views import *
from gadai.appgadai.models import Biaya_Materai


urlpatterns = patterns('',
    #url(r'^(?P<object_id>\d+)/hapus_jurnal/$', hapus_jurnal),
    #url(r'^$',  list),
    #url(r'^(?P<object_id>\d+)/show/$',show),
    url(r'^(?P<object_id>\d+)/add/$',add),
    #url(r'^biaya_post/add/$', biaya_post),
)
