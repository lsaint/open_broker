## -*- coding:utf-8 -*-

import json

from django.http import *
from django.shortcuts import *
from django.core import serializers
from django.db import connections
from django.db.models import Q

from web.ctrl.models import *
from web.view_common import *
import node.node2webdb as webdb
import node.node2appmgr as am
#import node.node2statistic as statistic
import node.node2cs as cs



class AppCommentHandle(ModelHandle):

    def __call__(self, request, **kwargs):
        try:
            self.limit = int(kwargs.pop("limit"))
            self.offset = int(kwargs.pop("offset"))
        except:
            pass

        return super(AppCommentHandle, self).__call__(request, **kwargs)


    def query(self):
        return self.model.objects.filter(**self.kwargs).order_by("-time")[self.offset:self.offset+self.limit]


    def count(self, request, **kwargs):
        #kwargs["check"] = 1
        return HttpResponse(self.model.objects.filter(**kwargs).count())


class AppBasicInfoHandle(ModelHandle):

    def query(self):
        return self.model.objects.filter(**self.kwargs).order_by("-last_modify_time")


class AppNoticeHandle(ModelHandle):

    def query(self):
        return self.model.objects.filter(**self.kwargs).order_by("-time")


class AppBasicInfoLimitHandle(ModelHandle):

    def __call__(self, request, **kwargs):
        self.limit = int(kwargs.pop("limit"))
        self.offset = int(kwargs.pop("offset"))
        return super(AppBasicInfoLimitHandle, self).__call__(request, **kwargs)

    def query(self):
        #return self.model.objects.filter(**self.kwargs).order_by("-last_modify_time")[self.offset:self.offset+self.limit]
        return self.model.objects.raw("select * from app_info where istest = 0 order by last_modify_time desc limit %s,%s", [self.limit, self.offset])

    def count(self, request, **kwargs):
        return HttpResponse(self.model.objects.filter(**kwargs).count())


### POST ###


def batchCheckComment(**kwargs):
    ids = kwargs["ids"]
    c = int(kwargs["check"])
    AppComment.objects.filter(id__in=ids).update(check=c)
    return HttpResponse("true")


def openCloud(**kwargs):
    return HttpResponse(cs.enableCloudSave(int(kwargs["appid"])))


def addChlApp(**kwargs):
    print "addChlApp", kwargs
    return HttpResponse(am.addChlApp(int(kwargs["appid"]), int(kwargs["sid"]), kwargs["subsids"]))


def delChlApp(**kwargs):
    print "delChlApp", kwargs
    return HttpResponse(am.delChlApp(int(kwargs["appid"]), int(kwargs["sid"]), kwargs["subsids"]))


def addChlOldApp(**kwargs):
    return HttpResponse(am.addChlOldApps([int(kwargs["appid"])], int(kwargs["sid"])))


def delChlOldApp(**kwargs):
    return HttpResponse(am.delChlOldApps([int(kwargs["appid"])], int(kwargs["sid"])))


def addChlWhite(**kwargs):
    return HttpResponse(am.addChlWhite(int(kwargs["appid"]), int(kwargs["sid"])))


def delChlWhite(**kwargs):
    return HttpResponse(am.delChlWhite(int(kwargs["appid"]), int(kwargs["sid"])))


def removeAppFromChannel(**kwargs):
    return HttpResponse(am.removeAppFromChannel(kwargs["sid"], kwargs["appid"]))


def delApp(**kwargs):
    return HttpResponse(am.delApp(kwargs["appid"]))


def delVer(**kwargs):
    return HttpResponse(am.delVer(kwargs["appid"], kwargs["verid"]))


def addModifyVersion(**kwargs):
    appid = int(kwargs.pop("appid"))
    return HttpResponse(am.addModifyVersion(appid, **kwargs))


### GET ###


def countBasicInfoSlice_iac(request, **kwargs):
    tp_istest = filterMultiParamByKw(kwargs["istest"], True)
    tp_carry_able = filterMultiParamByKw(kwargs["carry_able"], True)
    cursor = connections["appmanager"].cursor()
    s = "select count(*) from app_info\
            where istest in %s " % tp_istest\
            + " and app_attrib = %s" % kwargs["app_attrib"]\
            + " and carry_able in %s" % tp_carry_able
    cursor.execute(s)
    row = cursor.fetchone()
    return HttpResponse(row)


def countBasicInfoSlice_iarr(request, **kwargs):
    tp_istest = filterMultiParamByKw(kwargs["istest"], True)
    tp_reserve1 = filterMultiParamByKw(kwargs["reserve1"], True)
    r2 = int(kwargs["reserve2"])
    r2 = "" if r2 == 0 else " and reserve2 = %s" % r2
    cursor = connections["appmanager"].cursor()
    s = "select count(*) from app_info\
            where istest in %s " % tp_istest\
            + " and app_attrib = %s" % kwargs["app_attrib"]\
            + " and reserve1 in %s" % tp_reserve1\
            + r2
    cursor.execute(s)
    row = cursor.fetchone()
    return HttpResponse(row)


def getBasicInfoSlice_iac(request, **kwargs):
    tp_istest = filterMultiParamByKw(kwargs["istest"], True)
    tp_carry_able = filterMultiParamByKw(kwargs["carry_able"], True)
    lt = AppBasicInfo.objects.raw("select * from app_info\
            where istest in %s " % tp_istest\
            + " and app_attrib = %s"\
            + " and carry_able in %s" % tp_carry_able\
            + " order by last_modify_time desc limit %s,%s",\
            (kwargs["app_attrib"],  int(kwargs["offset"]), int(kwargs["limit"])))
    jn = serializers.serialize("json", lt)
    return HttpResponse(jn, mimetype="application/json")


def getBasicInfoSlice_iarr(request, **kwargs):
    tp_istest = filterMultiParamByKw(kwargs["istest"], True)
    tp_reserve1 = filterMultiParamByKw(kwargs["reserve1"], True)
    r2 = int(kwargs["reserve2"])
    r2 = "" if r2 == 0 else " and reserve2 = %s" % r2
    lt = AppBasicInfo.objects.raw("select * from app_info\
            where istest in %s " % tp_istest\
            + " and app_attrib = %s"\
            + " and reserve1 in %s" % tp_reserve1\
            + r2\
            + " order by last_modify_time desc limit %s,%s",\
            (kwargs["app_attrib"], int(kwargs["offset"]), int(kwargs["limit"])))
    jn = serializers.serialize("json", lt)
    return HttpResponse(jn, mimetype="application/json")


def countBasicInfoSlice_ic(request, **kwargs):
    tp_istest = filterMultiParamByKw(kwargs["istest"], True)
    tp_carry_able = filterMultiParamByKw(kwargs["carry_able"], True)
    cursor = connections["appmanager"].cursor()
    cursor.execute("select count(*) from app_info\
            where istest in %s " % tp_istest\
            + "and carry_able in %s" % tp_carry_able)
    row = cursor.fetchone()
    return HttpResponse(row)


def countBasicInfoSlice_ir(request, **kwargs):
    tp_istest = filterMultiParamByKw(kwargs["istest"], True)
    tp_reserve1 = filterMultiParamByKw(kwargs["reserve1"], True)
    cursor = connections["appmanager"].cursor()
    cursor.execute("select count(*) from app_info\
            where istest in %s " % tp_istest\
            + "and reserve1 in %s" % tp_reserve1)
    row = cursor.fetchone()
    return HttpResponse(row)


def getBasicInfoSlice_ic(request, **kwargs):
    tp_istest = filterMultiParamByKw(kwargs["istest"], True)
    tp_carry_able = filterMultiParamByKw(kwargs["carry_able"], True)
    lt = AppBasicInfo.objects.raw("select * from app_info \
            where istest in %s " % tp_istest\
            + " and carry_able in %s" % tp_carry_able\
            + " order by last_modify_time desc limit %s,%s",
            (int(kwargs["offset"]), int(kwargs["limit"])))
    jn = serializers.serialize("json", lt)
    return HttpResponse(jn, mimetype="application/json")


def getBasicInfoSlice_ir(request, **kwargs):
    tp_istest = filterMultiParamByKw(kwargs["istest"], True)
    tp_reserve1 = filterMultiParamByKw(kwargs["reserve1"], True)
    lt = AppBasicInfo.objects.raw("select * from app_info \
            where istest in %s " % tp_istest\
            + " and reserve1 in %s" % tp_reserve1\
            + " order by last_modify_time desc limit %s,%s",
            (int(kwargs["offset"]), int(kwargs["limit"])))
    jn = serializers.serialize("json", lt)
    return HttpResponse(jn, mimetype="application/json")


def getAvgScore(request, **kwargs):
    tp = filterMultiParamByKw(kwargs["appid__in"], True)
    ret = AppScore.objects.avgScore(tp)
    dt = {}
    for k, v in ret:
        dt[k] = float(v)
    return HttpResponse(json.dumps(dt), mimetype="application/json")


def getDeveloperApps(request, **kwargs):
    dis = get_list_or_404(AppDevInfo, developer=kwargs["uid"])
    try:
        bis = [AppBasicInfo.objects.get(pk=di.appid) for di in dis]
    except:
        raise Http404
    jn = serializers.serialize("json", bis+dis)
    return HttpResponse(jn, mimetype="application/json")


def validateOw(request, **kwargs):
    return HttpResponse(int(webdb.validateOwner(kwargs["channel"], kwargs["uid"])))


def getChlRoles(request, **kwargs):
    lt = filter(lambda x:x, kwargs["roles"].split("/"))
    return HttpResponse(json.dumps(webdb.getChlRoles(kwargs["uid"], lt)))


def getYyIdByUid(request, **kwargs):
    return HttpResponse(webdb.getImidByUid(kwargs["uid"]))


def getUid(request, **kwargs):
    return HttpResponse(webdb.getUid(kwargs["passport"]))


# closure for searchApp and getLatelyApp
def extractIconUrl(tp):
    dt = json.loads(tp[0])
    n =  dt.get("iconBName") or dt.get("iconSName") or ""
    l = []
    l.append(dt["iconPath"] + n)
    l.extend(tp[1:])
    return l


def searchApp(request, **kwargs):
    lt = AppBasicInfo.objects.filter(istest=0, am_appname__icontains=kwargs["name"])[:10].values_list(\
                                    "expand", "am_appid", "app_attrib", "am_appname")
    return HttpResponse(json.dumps(map(extractIconUrl, lt)))


def getLatelyApp(request, **kwargs):
    count = int(kwargs["count"])
    #lt = AppBasicInfo.objects.filter(~Q(istest=1)).order_by("last_modify_time")[:count].values_list(\
    #                            "expand", "am_appid", "am_appname")
    # because of the goddamn myshard, you can't use "~Q".
    lt = AppBasicInfo.objects.filter(istest=0).order_by("-last_modify_time")[:count].values_list(\
                                "expand", "am_appid", "am_appname")
    return HttpResponse(json.dumps(map(extractIconUrl, lt)))


def getAllReleaseApp(request, **kwargs):
    if request.GET.has_key("istest"):
        t = int(request.GET["istest"])
    else:
        t = 0

    lt = AppBasicInfo.objects.filter(istest=t).values_list("am_appid")
    appids = map(lambda x:x[0], lt)
    if request.GET.has_key("new"):
        for i in appids[:]:
            if i < 100000:  # 小于六位数的为新app
                appids.remove(i)
    return HttpResponse(json.dumps(appids))


def getAppTopnSids(request, **kwargs):
    params = filterMultiParamByKw(kwargs["appid"])
    sids = map(lambda x:int(x), params)
    #直连需要dumps一次
    #return HttpResponse(json.dumps(statistic.getAppTopnSidsFromCache(sids, int(kwargs["n"]))))
    return HttpResponse(statistic.getAppTopnSidsFromCache(sids, int(kwargs["n"])))


def getSubSessionsInfo(request, **kwargs):
    return HttpResponse(json.dumps(webdb.getSubSessionsInfo(kwargs["sid"], kwargs["subsid"])))


def getSidByAsid(request, **kwargs):
    return HttpResponse(webdb.getSidByAsid(kwargs["sid"]))


def batchGetSessionInfo(request, **kwargs):
    params = filterMultiParamByKw(kwargs["sids"])
    return HttpResponse(json.dumps(webdb.batchGetSessionInfo(params)))


def batchGetSessionLogoUrl(request, **kwargs):
    params = filterMultiParamByKw(kwargs["sids"])
    return HttpResponse(json.dumps(webdb.batchGetSessionLogoUrl(params)))


def getChannelApps(request, **kwargs):
    ret = SidappFlag.objects.filter(topsid=kwargs["sid"]).values_list("appid")
    return HttpResponse(json.dumps([x[0] for x in ret]))


def isChannelAppInWhilelist(request, **kwargs):
    #get_object_or_404(ChnAppWhitelist, **kwargs)
    ret = ChnAppWhitelist.objects.filter(**kwargs).exists()
    if not ret:
        return HttpResponse("false")
    return HttpResponse("true")


def getChannelAppWhitelist(request, **kwargs):
    offset = kwargs["offset"]
    limit = kwargs["limit"]
    channel_id = kwargs["channel_id"]
    ret = ChnAppWhitelist.objects.raw("select * from chn_app_whitelist where channel_id = %s limit %s,%s"%\
            (channel_id, offset, limit))
    r = []
    for m in ret:
        r.append(m.app_id)
    return HttpResponse(json.dumps(r))


def getChannelAppWhitelistCount(request, **kwargs):
    return HttpResponse(ChnAppWhitelist.objects.filter(**kwargs).count())


def getChannelNonfreeApps(request, **kwargs):
    ret = ChnAppWhitelist.objects.filter(channel_id=kwargs["channel_id"]).values_list("app_id")
    lt = [i[0] for i in ret]
    if lt:
        nfa = Appcheckinfo.objects.filter(appid__in=lt, free_flag=0).values_list("appid")
        nfa = [i[0] for i in nfa]
    else:
        nfa = []
    return HttpResponse(json.dumps(nfa))


def batchGetUserInfo(request, **kwargs):
    params = filterMultiParamByKw(kwargs["sids"])
    return HttpResponse(json.dumps(webdb.batchGetUserInfo(params)))


def batchGetSessionAsid(request, **kwargs):
    params = filterMultiParamByKw(kwargs["sids"])
    return HttpResponse(json.dumps(webdb.batchGetSessionAsid(params)))


def checkChlPrivileges(request, **kwargs):
    return HttpResponse(am.checkChlPrivileges(int(kwargs["appid"]), int(kwargs["sid"])))


def getSubChannelApp(request, **kwargs):
    ret = Channelapp.objects.filter(parentsid=kwargs["parentsid"]).values_list("channelid", "appid")
    return HttpResponse(json.dumps(list(ret)))


def setAutoApp(**kwargs):
    return HttpResponse(am.setAutoApp(int(kwargs["appid"]), int(kwargs["sid"]), kwargs["subsids"]))


def delAutoApp(**kwargs):
    return HttpResponse(am.delAutoApp(int(kwargs["appid"]), int(kwargs["sid"]), kwargs["subsids"]))


def getAutoApp(request, **kwargs):
    ret = AppAttrib.objects.filter(**kwargs).values_list("channelid", "front_appid")
    return HttpResponse(json.dumps(list(ret)))


def setReleaseCount(**kwargs):
    appid = kwargs.pop("appid")
    return HttpResponse(am.setReleaseCount(appid, **kwargs))


def test(request, *args, **kwargs):
    request.user.is_authenticated
    return redirect("/")


