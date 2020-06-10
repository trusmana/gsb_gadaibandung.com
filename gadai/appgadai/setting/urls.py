from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update
from django.contrib.auth.models import User

from gadai.appgadai.setting.views import *

urlpatterns = patterns('',
    (r'user/add/$', add_user),
    (r'^user/(?P<object_id>\d+)/edit/$', add_user),
    (r'^user/$', list_detail.object_list, {'queryset': User.objects.all(), 'template_name': 'user/list.html'}),
)
