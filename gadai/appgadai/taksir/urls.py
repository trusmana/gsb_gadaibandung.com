from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update, date_based
from gadai.appgadai.models import Taksir
from gadai.appgadai.taksir.views import *

urlpatterns = patterns('',
    url(r'^add/$',add),
    url(r'^$',  list),
    url(r'^(?P<object_id>\d+)/show/$',show),
    url(r'add/$', add),
    url(r'^(?P<object_id>\d+)/edit/$',edit),
    #url(r'^(?P<object_id>\d+)/delete/$',delete),
    #url(r'^(?P<object_id>\d+)/edit/$', create_update.update_object, {'model': Taksir, 'template_name': 'taksir/edit.html'}),
    url(r'^cari/$',cari),
    #url(r'^(?P<object_id>\d+)/delete/$', create_update.delete_object, {'model': Taksir , 'post_delete_redirect': '/taksir/', 'template_name': 'taksir/confirm_delete.html'}),
)
