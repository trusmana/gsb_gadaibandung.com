from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update, simple

from gadai.appgadai.models import *
from gadai.appgadai.piutang.views import *

urlpatterns = patterns('',
    url(r'rekappiutang/$', rekappiutang),
)
