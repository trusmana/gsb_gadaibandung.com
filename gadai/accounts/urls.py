from django.conf.urls.defaults import patterns
from django.contrib.auth import views as authviews

urlpatterns = patterns('', 
    (r'^login/$',                authviews.login),
    (r'^logout/$',               authviews.logout_then_login),
    (r'^password/change/$',      authviews.password_change),
    (r'^password/change/done/$', authviews.password_change_done),
)
