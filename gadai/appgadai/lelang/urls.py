from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update, date_based
from gadai.appgadai.lelang.views import *
from gadai.appgadai.models import BarangLelang

urlpatterns = patterns('',
    url(r'^$', list),
    url(r'^jual/$',jual),
    url(r'^(?P<object_id>\d+)/lapur/$',lapur),
    url(r'^(?P<object_id>\d+)/prints2/$',kuitansi),
)
