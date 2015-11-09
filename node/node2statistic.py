# -*- coding: utf-8 -*-


#import os, sys
#path = os.path.abspath(".")
#sys.path.insert(0, path)
#os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'

import json, socket, memcache
from node_common import *

CACHE_HOST = ['127.0.0.1:11211']
mc = memcache.Client(CACHE_HOST)


def getTopnApps(n):
    req_topn = {
            "op"    : "get_topn_apps",
            "topn"  : n,
            "expand": "",
    }
    ret = sendMsgToStatic(json.dumps(req_topn))
    try:
        return json.loads(ret[LEN_HEAD:])["apps"]
    except Exception, e:
        print "getTopnApps, e", e
        return False

# 直连版
def getAppTopnSids(appids, n):
    req = json.dumps({
            "op"    :   "batch_get_app_topn_sids",
            "appids" :   appids,
            "topn"  :   n,
            "expand":   "",
    })
    ret = sendMsgToStatic(req)
    try:
        return json.loads(ret)["apps"]
    except Exception, e:
        print "getAppTopnSids", e
        return False


# cache版, 兼容直连格式
def getAppTopnSidsFromCache(appids, n):
    # 收到多个appids时 强制认为是取所有应用top1
    if len(appids) > 1:
        return mc.get("top1s")
    j = mc.get(str(appids[0]))
    return j


#getAppTopnSids([100492,100767,100815,100824,100877,100905,100907,101213,102850,103350], 12)

