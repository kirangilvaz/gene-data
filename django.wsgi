import os, sys
import django.core.handlers.wsgi

sys.path.append('c:/wamp/www/geneticanalysis/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'geneticanalysis.settings'  
application = django.core.handlers.wsgi.WSGIHandler()