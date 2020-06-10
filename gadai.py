#import os,sys
#sys.path.insert(0, '/var/www/gadai')
#sys.path.append('/var/www')
#sys.path.append('/var/www/gadai')
#sys.path = ['/var/www/gadai'] + sys.path
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gadai.settings")
#os.environ['DJANGO_SETTINGS_MODULE'] = 'gadai.settings'
#import django.core.handlers.wsgi
#application =  django.core.handlers.wsgi.WSGIHandler()
#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()

import sys, os
sys.stdout = sys.stderr
sys.path.insert(0, "/var/www")
sys.path.insert(1, "/var/www/gadai")
os.chdir("/var/www/gadai")
os.environ['DJANGO_SETTINGS_MODULE'] = "gadai.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()  
