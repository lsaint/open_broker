# -*- coding: utf-8 -*-

#import os, sys
#path = os.path.abspath(".")
#sys.path.insert(0, path)
#os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'

import json

from node_common import *


g_cloud_save = {"appid":0, "uri":1}


@resultDecorator(False)
def enableCloudSave(appid):
    c = {}
    c.update(g_cloud_save)
    c["appid"] = appid
    jn = json.dumps(c)
    ret = sendMsgToCloud(jn)
    return json.loads(ret)["return"] == 1


#print enableCloudSave(105059)

