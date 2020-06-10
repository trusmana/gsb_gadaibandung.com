from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update, date_based
from gadai.appgadai.models import *
from gadai.appgadai.materaicabang.forms import *
from gadai.appgadai.materaicabang.views import *
import datetime

urlpatterns = patterns('',
    url(r'^(?P<object_id>\d+)/biaya_materai/$',materai_cabang),
)
