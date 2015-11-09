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


for abi in AppBasicInfo.objects.filter(am_appid=107272):
    print json.loads(abi.expand)

