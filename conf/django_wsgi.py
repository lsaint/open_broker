import os
import sys
#sys.stdout = sys.stderr


if not os.path.dirname(__file__) in sys.path[:1]:
    sys.path.insert(0, os.path.abspath("..") + "/web/")

print __file__
print os.path.dirname(__file__)
print sys.path

os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
