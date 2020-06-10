from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update
from gadai.appgadai.models import *
from gadai.appgadai.report.views import *

urlpatterns = patterns('',
    url(r'^$',  list),
    url(r'^(?P<object_id>\d+)/$', tampil),
    #url(r'^agingharian/$', list_detail.object_list, {'queryset': Tbl_Cabang.objects.all(), 'template_name': 'report/detailhari.html'}),
    url(r'^cetakagingharian$', list_detail.object_list, {'queryset': Tbl_Cabang.objects.all(), 'template_name': 'report/cetakdetailhari.html'}),
    url(r'^agingharian/$', agingharian),
)

