# -*- coding: utf-8 -*-

#import os, sys
#path = os.path.abspath(".")
#sys.path.insert(0, path)
#os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'

import json, socket, struct, time, datetime
from node_common import *

from web.ctrl.models import AppDevInfo, AppVersion

g_create_modify_app = {
    "oper"      : "lSaint",
    "appinfo"   : "",
    "expand"    : "",
    "uri"       : URI_CREATE_MODIFY_APP,
}


g_appinfo = {
    "postype"    :0,   # 0 三栏 1 盒子
    "appattrib"  :0,   # 应用类型，如游戏类，管理类，频道类
    "bintype"    :2,   # js:1 exe:2 dll:3 flash:4
    "subsidapp"  :1,   # 是否支持子频道应用
    "istest"     :1,   # 
    "delayflag"  :1 ,  # 延迟下载
    "recommand_v":0 ,  # 推荐版本
    "name"       :"" ,
    "passwd"     :"356a192b7913b04c54574d18c28d46e6395428ab", # sha1 1
    "file_name"  :"" ,
    "desc"       :"" ,
    "addtime"    :"" ,
    #"modtime"    :"" ,
    "disp_type"  :0,   # 是否需要yy链路做数据透传
    "need_lbs"   :0 ,  # 负载均衡
    "expand"     :"", 
#    "appinfo"    : "" , # 
    "appid"      :0 ,
#    "protogw_chn": "" ,
}

g_appinfo_expand = {
        "iconPath"   : "",  #图标url
        "iconBName"  : "",  #大图标文件名
        "iconSName"  : "",  #小图标文件名
        "partVApp"   : "1",  #是否属于虚拟应用,外部应用目前都填是
        "useCloud"   : "",  #是否使用云存储(暂未使用)
}

# 

g_app_ver_item = {
    "verurl"    : "",
    "vermd5"    : "",
    "vbinmd5"   : "L",
    "yymax"     : 85536,
    "yymin"     : 65544,
}


def setReleaseCount(appid, **kw):
    d = datetime.datetime.now()
    expand = {}
    expand["m_chk_year"]        = d.year
    expand["m_chk_month"]       = d.month
    expand["m_chk_date"]        = d.day
    expand["m_chk_hour"]        = d.hour + 1
    expand["m_chk_flag"]        = 0 # 0不限 2人气 4白名单
    expand["m_chk_ollower"]     = 0 # 人气需求  仅flag2有效
    expand["m_chk_daylimit"]    = 0 # 每天上限
    expand["m_chk_totallimit"]  = 0 # 总量
    expand["chk_free"]          = 1 # 1免费 0收费 
    expand["chk_r1"]            = 0 
    expand.update(kw)

    c = {}
    c["uri"]       = URI_RELEASE_COUNT
    c["appid"]     = appid
    c["uid"]       = 37
    c["expand"]    = json.dumps(expand)

    jn = json.dumps(c)
    print "jn release count", jn

    ret = json.loads(sendMsgToAppmgr(jn)[LEN_HEAD:])
    print "setReleaseCount", ret
    return ret.get("status") == 0


def addModifyVersion(appid, model=None, **kwargs):
    print "addModifyVersion ============== "
    item = {}
    item.update(g_app_ver_item)
    if model:
        item["appid"]   =   model["am_appid"]
        item["verid"]   =   model["am_appver"]
        item["verurl"]  =   model["am_appurl"]
        item["vermd5"]  =   model["am_appmd5"]
        item["vbinmd5"] =   model["am_exemd5"]
        item["yymax"]   =   model["am_vmax"]
        item["yymin"]   =   model["am_vmin"]
    else:
        item.update(kwargs)
    ver = {}
    ver["appid"] = appid
    ver["vinfo"] = json.dumps(item)
    ver["uri"] = URI_ADD_MODIFY_VER

    ver = json.dumps(ver)
    print "send ver ...", ver
    ret = sendMsgToAppmgr(ver)
    jn = json.loads(struct.unpack("I%ds"%(len(ret)-LEN_HEAD), ret)[1])
    print "AddModifyVersion", jn
    return jn["status"] == 0


@resultDecorator(False)
def createModifyApp(model, **kwargs):
    print "createModifyApp ============== "
    appinfo = {}
    appinfo.update(g_appinfo)
    create_modify_app = {}
    create_modify_app.update(g_create_modify_app)

    appinfo["appid"]       = model["am_appid"]
    appinfo["name"]        = model["am_appname"]
    appinfo["appattrib"]   = model["app_attrib"]
    appinfo["bintype"]     = model["app_binary_type"]
    appinfo["subsidapp"]   = model["issubsidapp"]
    appinfo["desc"]        = model["am_description"]
    appinfo["istest"]      = model["istest"]
    appinfo["recommand_v"] = model["am_recommend_ver"]
    appinfo["file_name"]   = model["app_filename"]
    appinfo["addtime"]     = str(model["add_time"])
    appinfo["modtime"]     = str(datetime.datetime.now())[:-7]
    appinfo["passwd"]      = model["passwd"]
    appinfo["postype"]     = model["app_pos_type"]

    expand = json.loads(model["expand"])
    #expand["CarryAble"] = model["carry_able"]
    #expand["Reserve1"]  = model["reserve1"]
    #expand["Reserve2"]  = model["reserve2"]
    #expand["Reserve3"]  = model["reserve3"]
    appinfo["expand"]   = json.dumps(expand)

    create_modify_app["appinfo"] = json.dumps(appinfo)
    create_modify_app = json.dumps(create_modify_app)
    print "create_modify_app ", create_modify_app
    ret = sendMsgToAppmgr(create_modify_app)
    print "sendMsgToAppmgr ret", ret
    jn = json.loads(struct.unpack("I%ds"%(len(ret)-LEN_HEAD), ret)[1])
    return jn["status"] == 0



### ### ### ### ### ### ### ### 

get_appid_dt = {
    "oper"      : "lSaint",
    "expand"    : "",
    "uri"       : (1032 << 8) | 133,
}


@resultDecorator(0)
def getAppId(is_test_app=False):
    get_appid_dt["uri"] = (URI_GET_APP_ID, URI_GET_TEST_APP_ID)[is_test_app]
    get_appid = json.dumps(get_appid_dt)
    ret = sendMsgToAppmgr(get_appid)
    return json.loads(struct.unpack("I%ds" % (len(ret) - LEN_HEAD), ret)[1])["appid"]



### PBatchAddChannelApp2

g_add_chl_app = {
    "oper"  : "lSaint",
    "appid" : None,
    "sid": None,
    "subsids"  : None,
    "seq"   : 0xFFFFFFFF,
    "expand": "",
    "uri"   : URI_ADD_CHL_APP,
}


def handleChlApp(appid, sid, subsids, is_add):
    c = {}
    c.update(g_add_chl_app) if is_add else c.update(g_del_chl_app)
    c["appid"] = appid
    c["sid"] = sid
    c["subsids"] = json.dumps(subsids)
    jn = json.dumps(c)

    ret = json.loads(sendMsgToAppmgr(jn)[LEN_HEAD:])
    print "handleChlApp", is_add, ret
    return ret.get("failssids") is None


def addChlApp(appid, sid, subsids):
    return handleChlApp(appid, sid, subsids, True)


### PBatchDelChannelApp2

g_del_chl_app = {
    "oper"  : "lSaint",
    "appid" : None,
    "topsid": None,
    "subsids"  : None,
    "seq"   : 0xFFFFFFFF,
    "expand": "",
    "uri"   : URI_DEL_CHL_APP,
}


def delChlApp(appid, sid, subsids):
    return handleChlApp(appid, sid, subsids, False)


### PSetAppTheSidVersion


g_set_test_app = {
    "appid":None,
    "verid":None,
    "sid":None,
    "oper":"lSaint",
    "expand":"",
    "uri"   : URI_SET_TEST_APP,
}

def setTestAppToChannel(appid, version, sid):
    print "setTestAppToChannel..."
    c = {}
    c.update(g_set_test_app)
    c["appid"] = appid
    c["verid"] = version
    c["sid"] = sid
    jn = json.dumps(c)

    ret = sendMsgToAppmgr(jn)
    print "SetTestAppToChannel", appid, version, sid
    return json.loads(ret[LEN_HEAD:])["status"] == 1


### PAddChnWhiteToAppid
### PDelChnWhiteToAppid2

def handleWhite(appid, sid, uri):
    c = {}
    c["appid"] = appid
    c["oper"] = "lSaint"
    c["sid"] = sid
    c["uri"] = uri
    jn = json.dumps(c)
    ret = json.loads(sendMsgToAppmgr(jn)[LEN_HEAD:])
    print "handleWhite", uri, ret
    return ret["status"] == "OK"

def addChlWhite(appid, sid):
    return handleWhite(appid, sid, URI_ADD_CHL_WHITE )

def delChlWhite(appid, sid):
    return handleWhite(appid, sid, URI_DEL_CHL_WHITE )



# PCheckChnPrivileges

def checkChlPrivileges(appid, sid, test_flag=1):
    ''' 0-pass,1-need active code, 3-fail,4-sid in whitelist '''
    c = {}
    c["appid"] = appid
    c["sid"] = sid
    c["test_flag"] = test_flag
    c["uri"] = URI_CHECK_CHL_PRI
    jn = json.dumps(c)
    ret = sendMsgToAppmgr(jn)
    print "ret", ret
    return ret[LEN_HEAD:]


# PYyopenAddThredApps
# PYyopenDelThredApps
# (10003, 10012, 10009, 10004, 10008, 10005, 20010)

@resultDecorator(False)
def handleOldApps(appids, sid, uri):
    c = {}
    c["appids"] = json.dumps(appids)
    c["sid"] = sid
    c["uri"] = uri
    jn = json.dumps(c)
    ret = sendMsgToAppmgr(jn)
    print "handleOldApps return", ret
    return json.loads(ret[LEN_HEAD:])["status"] == 1


def addChlOldApps(appids, sid):
    return handleOldApps(appids, sid, URI_ADD_THRED_APP)

def delChlOldApps(appids, sid):
    return handleOldApps(appids, sid, URI_DEL_THRED_APP)


#PManageUserApp
def manageUsrApp(uid, appid, is_add):
    c = {}
    if is_add:
        c["uri"] = URI_ADD_USR_APP
    else:
        c["uri"] = URI_DEL_USR_APP
    c["cid"] = 0
    c["oper"] = "lSaint"
    c["userid"] = uid
    c["appid"] = appid
    c["expand"] = ""
    jn = json.dumps(c)
    ret = json.loads(sendMsgToAppmgr(jn)[LEN_HEAD:])
    print " manageUsrApp", is_add, ret
    return ret["status"] == 0


#PSetSidUserappSwitch
def setSidUsrAppSwitch(sid, parentsid, subsid, sw):
    c = {}
    c["uri"] = URI_SET_SID_USR_APP_SWITCH
    c["sid"] = sid
    c["parentsid"] = parentsid
    c["subsid"] = subsid
    c["switch_status"] = sw
    c["oper"] = "lSaint"
    c["expand"] = ""
    jn = json.dumps(c)
    ret = sendMsgToAppmgr(jn)
    return json.loads(ret[LEN_HEAD:])["status"] == 0


#PCheckUserappPrivileges
def checkUsrAppPrivileges(uid, appid):
    c = {}
    c["uri"] = URI_CHECK_USR_APP_PRI
    c["appid"] = int(appid)
    c["userid"] = int(uid)
    c["expand"] = ""
    c["cid"] = 0
    jn = json.dumps(c)
    ret = sendMsgToAppmgr(jn)
    #return json.loads(ret[LEN_HEAD:])["status_code"] == 0
    return ret[LEN_HEAD:]


###
#PRemoveAppFromChannel
def removeAppFromChannel(sid, appid): 
    c = {}
    c["uri"] = URI_RM_APP_FROM_CHL
    c["oper"] = "lSaint"
    c["expand"] = ""
    c["sid"] = sid
    c["appid"] = appid
    jn = json.dumps(c)
    ret = sendMsgToAppmgr(jn)
    return json.loads(ret[LEN_HEAD:])["status"] == 0



###


def delVer(appid, verid):
    c = {}
    c["uri"] = URI_DEL_VER
    c["oper"] = "lSaint"
    c["appid"] = int(appid)
    c["verid"] = int(verid)
    jn = json.dumps(c)
    ret = sendMsgToAppmgr(jn)
    print "delApp ret", ret
    return json.loads(ret[LEN_HEAD:])["status"] == 0



def delApp(appid):
    c = {}
    c["uri"] = URI_DEL_APP
    c["oper"] = "lSaint"
    c["appid"] = int(appid)
    c["expand"] = json.dumps({1:"Luo said: if the msg's len <64 then would get some mistake."})
    jn = json.dumps(c)
    ret = json.loads(sendMsgToAppmgr(jn)[LEN_HEAD:])
    print "delApp ret", ret
    if ret["status"] == 0:
        AppDevInfo.objects.filter(appid=appid).delete()
        vers = AppVersion.objects.filter(am_appid=appid)
        for ver in vers:
            delVer(ver.am_appid, ver.am_appver)
        return True
    return False


def handleAutoApp(appid, sid, subsids, isAdd):
    c = {}
    c["uri"] = URI_AUTO
    c["appid"] = appid
    c["sid"] = sid
    c["autoflag"] = 1 if isAdd else 0
    c["subsids"] = subsids
    c["oper"] = "lSaint"
    c["expand"] = ""
    c["seq"] = 0
    jn = json.dumps(c)
    ret = json.loads(sendMsgToAppmgr(jn)[LEN_HEAD:])
    return ret["status"] == 0


def setAutoApp(appid, sid, subsids):
    return handleAutoApp(appid, sid, subsids, True)


def delAutoApp(appid, sid, subsids):
    return handleAutoApp(appid, sid, subsids, False)


#print setAutoApp(101010, 1640285, [1640285])
#print delVer(102031, 1)
#print delApp(102125)
#print checkUsrAppPrivileges(50090300, 20101)
#print setSidUsrAppSwitch(1640285, 1640285, 1640285, 1)
#print manageUsrApp(50002080, 10004, False)
#print delChlOldApps([10003], 1640285)
#print addChlOldApps([10003], 1640285)
#print checkChlPrivileges(10001, 1640285, 0)
#print delChlWhite(10001, 1640285)
#print addChlWhite(10001, 1640285)
#print getAppId(True)
#print getAppId(False)
#print createModifyApp({"iconBName":"AK47"}, appid=90909, bintype=3)
#print EnableCloundSave(50027)
#print addModifyVersion(50027, verid=1, vermd5="2", verurl="3")
#print setTestAppToChannel(759511, 1, 1640285)
#print addChlApp(1640285, 123123, [123123])
#print delChlApp(1640285, 123123, [123123])
#print setReleaseCount(108781, **{"m_chk_daylimit":1, "m_chk_totallimit":2})
