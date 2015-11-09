# coding:utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import os, sys, json


path = os.path.abspath("../..")
if path not in sys.path:
    sys.path.insert(0, path)

#print sys.path

os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'

from web.ctrl.models import *

from django.db import connection, models

from node.node2appmgr import *

addModifyVersion(103350, None, **{"verurl":"http://dl.open.yy.com/opdata/app/103350/1336615248/kk.7z", "vermd5":"2415854e7514045111e90a0a3446d56b", "verid":2})

