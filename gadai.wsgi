import os
import sys
sys.path = ['/var/www/gadai'] + sys.path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gadai.settings")
#os.environ['DJANGO_SETTINGS_MODULE'] = 'gadai.settings'
import django.core.handlers.wsgi
application =  django.core.handlers.wsgi.WSGIHandler()


