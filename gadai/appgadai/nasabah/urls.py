from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update
from gadai.appgadai.nasabah.views import *
from gadai.appgadai.models import *
from django.core.urlresolvers import reverse
from django.views.generic.simple import redirect_to
from django.core.urlresolvers import reverse_lazy
from gadai.appgadai.nasabah.form import *

urlpatterns = patterns('',
    url(r'^(?P<object_id>\d+)/(?P<akad>\d+)/edit_nasabahgerai/$', edit_nasabahgerai),
    url(r'^$', list_detail.object_list, {'queryset': Nasabah.objects.all().order_by('-id')[:20], 'template_name': 'nasabah/index.html'}),
    url(r'^(?P<object_id>\d+)/show/$',show),
    url(r'add/$', add),
    url(r'^(?P<object_id>\d+)/edit/$', create_update.update_object, {'form_class': EditNasabahForm, 'template_name': 'nasabah/edit.html'}),
    #url(r'^(?P<object_id>\d+)/edit/$', create_update.update_object, {'model': Nasabah, 'template_name': 'nasabah/edit.html'}),
    url(r'^cari/$',cari),
    url(r'^(?P<object_id>\d+)/addnasabah/', addnasabah),
    url(r'^(?P<object_id>\d+)/(?P<akad>\d+)/edit_nasabah/$', edit_nasabah),
    ### 17-04-2013
    url(r'^cari_nama/$',cari_nama),
    ###1 Agustus 2016
    url(r'^(?P<object_id>\d+)/history_gu/',history_gu),
    url(r'^(?P<object_id>\d+)/edit_barang/',edit_barang),
    url(r'list_param/$', list_param),
    url(r'^(?P<object_id>\d+)/edit_param/',edit_param),
    url(r'^(?P<object_id>\d+)/input_edit_param/',input_edit_param),
    url(r'^(?P<object_id>\d+)/input_edit_history_gu/',input_edit_history_gu),
    url(r'add_param/$', add_param),
    url(r'^(?P<object_id>\d+)/blacklist_edit/', blacklist_edit),
    url(r'^(?P<object_id>\d+)/input_blacklist/', input_blacklist),
)
