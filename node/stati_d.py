# -*- coding: utf-8 -*-

# django setting
import os, sys
path = os.path.abspath("..")
sys.path.insert(0, path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'

import time, memcache, json, urllib, random, syslog
from node2statistic import getAppTopnSids, mc

syslog.openlog("broker-stati-d")

APPIDS = (101213, 100767, 100877, 103350, 102850, 100907, 100905, 100824, 100815, 100492)
TOPN = 12   # 排名数
APPIDS_CACHE_TIME = 60 * 5
INTERVAL = 60

#BROKER_HOST = ("http://222.88.95.242:3737/", "http://121.14.39.131:3737/")
BROKER_HOST = ("http://127.0.0.1/", )
SUBFIX = "getallreleaseapp/?new"


def getAppids():
    appids = mc.get("APPIDS")
    if not appids:
        try:
            host = random.choice(BROKER_HOST)
            url = host + SUBFIX
            u = urllib.urlopen(url)
            appids = json.loads(u.read())
            mc.set("APPIDS", appids, APPIDS_CACHE_TIME)
            syslog.syslog("get from url")
        except:
            appids = APPIDS
            syslog.syslog("get from const")
    else:
        syslog.syslog("get from cache")
    return appids


# 兼容格式 [{"sids":[{"usercount":1, "sid":1}...], "appid":appid}...]
def cacheTopn():
    ret = getAppTopnSids(getAppids(), TOPN)
    top1s = []
    for r in ret:
        appid = r["appid"]
        sids = r["sids"]
        # 单个应用的前12名
        top12 = json.dumps([{"sids":sids, "appid":appid}])
        # 所有上线应用的第一名
        top1s.append({"sids":[sids[0]] if sids else [], "appid":appid})
        mc.set(str(appid), top12)
    mc.set("top1s", json.dumps(top1s))


import daemon
with daemon.DaemonContext(stdout=sys.stdout, stderr=sys.stderr):
    while True:
        cacheTopn()
        time.sleep(INTERVAL)

