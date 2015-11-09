# -*- coding: utf-8 -*-



#DOMAIN = "http://myopen.yy.com/"
DOMAIN = "http://172.16.61.217:9000/"
def domain(request):
    return { "DOMAIN": DOMAIN }

#WEBDB_HOST = "121.11.65.153"
WEBDB_HOST = "222.88.95.117"
WEBDB_PORT = 8090
WEBDB_TIME_OUT = 7000

#APPMGR_HOST = "121.14.36.25"
#APPMGR_HOST = ("121.14.36.25", "58.249.116.89", "58.215.46.93", "122.97.254.93")
APPMGR_HOST = "111.178.146.46"
APPMGR_PORT = 7720

CLOUND_SAVE_HOST = "111.178.146.46"
#CLOUND_SAVE_HOST = "117.25.132.157"
CLOUND_SAVE_PORT = 18927


URL_BBS = "http://bbs.duowan.com/forum-1348-1.html"
PRE_BBS = "http://bbs.duowan.com/"
TOPICS_KEY = "topics"
TIME_TOPICS_CACHE = 60 


DEV_TYPE_PER = 1
DEV_TYPE_COM = 2

APP_TYPE = {
    1: "工具",
    2: "娱乐",
    3: "游戏",
    4: "其它",
    5: "视频",
    6: "教育",
    7: "社交",
    8: "生活",
    9: "购物",
}

BIN_NONE = 0
BIN_JS = 1
BIN_EXE = 2
BIN_DLL = 3
BIN_FLASH = 4
BIN_QTDLL = 5
BIN_WEB = 6

BIN_TYPE = {
    BIN_NONE: "",
    BIN_EXE: "exe",
    BIN_DLL: "dll",
    BIN_FLASH: "flash",
    BIN_WEB: "web",
}

# 操作状态 
APP_STATUS_DEVELOP  = 1
APP_STATUS_TEST     = 2
APP_STATUS_READY    = 3
APP_STATUS_PUBLISH  = 4
#APP_STATUS_RELEASE  = 5

# 审核/测试 状态
CS_NULL = 0
CS_TESTING = 1
CS_TEST_PASS = 2
CS_TEST_FAIL = 3
CS_CHECKING_PUB = 4
CS_CHECK_PUB_PASS = 5
CS_CHECK_PUB_FAIL = 6


APP_STATUS = {
    APP_STATUS_DEVELOP  : "开发",
    APP_STATUS_TEST     : "测试",
    APP_STATUS_READY    : "就位",
    APP_STATUS_PUBLISH  : "发布",
    #APP_STATUS_RELEASE  : "运行",
}


RES_MD5WRONG = "2"
RES_SUCESS = "1"
RES_FAILED = "0"


# 测试持续秒数
#CHECK_DURATION = 3 * 24 * 3600 
CHECK_DURATION = 60 #3 * 24 * 3600 

UDB_APPID = "9999"
UDB_APPKEY = "2C7B9D99572FAC91CB62352CAEE4F05A"


MAX_DEV_APP_COUNT = 5
