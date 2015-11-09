# -*- coding: utf-8 -*-

import json, socket, struct, time, random

from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.transport import THttpClient
from thrift.protocol import TBinaryProtocol
from webdb_service.server.webdb.gateway import *
from webdb_statement.server.webdb.gateway import *
from webdb_exception.server.webdb.gateway import *
from server.imweb import imweb_service

import conf.conf as conf

LEN_HEAD = 4
RECV_BUF_SIZE = 1024 * 5
MAX_RETRY = 3
TIME_OUT = 10

URI_GET_APP_ID = (1032 << 8) | 133
URI_GET_TEST_APP_ID = (1034 << 8) | 133
URI_CREATE_MODIFY_APP = (1001 << 8) | 133
URI_ADD_MODIFY_VER = (1005 << 8) | 133
URI_SET_TEST_APP = (1044 << 8) | 133
URI_ADD_CHL_APP = (1020 << 8) | 210
URI_DEL_CHL_APP = (1023 <<8 ) | 210
URI_ADD_CHL_WHITE = (11 << 8) | 18
URI_DEL_CHL_WHITE = (13 << 8) | 18
URI_CHECK_CHL_PRI = (15 << 8) | 18
URI_ADD_THRED_APP = (45 << 8) | 24
URI_DEL_THRED_APP = (47 << 8) | 24
#URI_MANAGE_USR_APP = (1306 << 8) | 210
URI_CHECK_USR_APP_PRI = (31 << 8) | 18
URI_ADD_USR_APP = (33 << 8) | 18
URI_DEL_USR_APP = (35 << 8) | 18
URI_SET_SID_USR_APP_SWITCH = (1304 << 8) | 210
URI_DEL_APP = (1003 << 8) | 133
URI_DEL_VER = (1007 << 8) | 133
URI_RM_APP_FROM_CHL = (1039 << 8) | 210
URI_AUTO = (1026 << 8) | 210
URI_RELEASE_COUNT = 268933


STATISTIC_ADDR  =  conf.STATISTIC_ADDR
APPMGR_ADDR     =  conf.APPMGR_ADDR   
CLOUND_ADDR     =  conf.CLOUND_ADDR   
WEBDB_ADDR      =  conf.WEBDB_ADDR    


g_conn_stati = None
g_conn_appmgr = None
g_conn_cloud = None
g_webdb_client = None
g_imweb_client = None

socket.setdefaulttimeout(TIME_OUT)


def createConnection(remote):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(remote)
        print "%s connected" % str(remote)
    except socket.error, e:
        print "connect to %s failed" % remote, e
        s.close()
    finally:
        return s


def connectStati():
    global g_conn_stati
    print "connecting to stati"
    g_conn_stati = createConnection(STATISTIC_ADDR)


def connectAppMgr():
    global g_conn_appmgr
    print "connecting to appmgr"
    g_conn_appmgr = createConnection(APPMGR_ADDR)


def connectCloud():
    global g_conn_cloud
    print "connecting to cloud"
    g_conn_cloud = createConnection(CLOUND_ADDR)


def initConnect():
    connectStati()
    #connectAppMgr()
    #connectCloud()
    connectImwebdb()
    connectWebdb()


def socketDecorator(reconnect_func):
    def checker(fun):
        def wrapper(*args, **kwargs):
            for i in range(MAX_RETRY):
                try:
                    return fun(*args, **kwargs)
                except (socket.error, AttributeError), e:
                    print "socketDecorator exception:", e
                    print "retrying ...... %d" % (i+1)
                    reconnect_func()
                    #time.sleep(random.uniform(2, 4))
                except Exception, e:
                    print "exception:", e
        return wrapper
    return checker


def packHead(msg, is_include_head):
    if is_include_head is None:
        head = ""
    else:
        head = struct.pack("I", len(msg) + (LEN_HEAD if is_include_head else 0))
    return head


def sendMsg(conn, msg, is_include_head):
    head = packHead(msg, is_include_head)
    conn.send("%s%s" % (head, msg))
    data = conn.recv(RECV_BUF_SIZE)
    if not data:
        raise socket.error("recv 0")
    return data


def sendMsgEx(conn, msg, is_include_head):
    head = packHead(msg, is_include_head)
    conn.send("%s%s" % (head, msg))

    data = ""
    while True:
        data = "%s%s" % (data, conn.recv(RECV_BUF_SIZE))
        if not data:
            raise socket.error("recv 0")
        if len(data) < LEN_HEAD:
            continue
        (length,)  = struct.unpack_from('I', data)
        if len(data) < length + LEN_HEAD:
            continue
        body = data[LEN_HEAD:length+LEN_HEAD]
        return body


def resultDecorator(err_ret):
    def checker(fun):
        def wrapper(*args, **kwargs):
            try:
                return fun(*args, **kwargs)
            except TypeError, e: 
                print "resultDecorator exception:", e
                return err_ret
        return wrapper
    return checker


@socketDecorator(connectStati)
def sendMsgToStatic(msg):
    return sendMsgEx(g_conn_stati, msg, False)


@socketDecorator(connectAppMgr)
def sendMsgToAppmgr(msg):
    return sendMsg(g_conn_appmgr, msg, True)


@socketDecorator(connectCloud)
def sendMsgToCloud(msg):
    return sendMsg(g_conn_cloud, msg, None)


### ### ### ### webdb ### ### ### ### 

def getProtocol():
    socket = TSocket.TSocket(*WEBDB_ADDR)
    socket.setTimeout(TIME_OUT * 1000)
    transport = TTransport.TFramedTransport(socket)
    transport.open() # may be after connect
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    return protocol


def connectWebdb():
    global g_webdb_client
    try:
        protocol = getProtocol()
        g_webdb_client = webdb_gateway_service.Client(protocol)
        print "webdb connected"
    except Exception, e:
        print "connectWebdb error", e
        g_webdb_client = None


def getWebdbConn():
    return g_webdb_client


def connectImwebdb():
    global g_imweb_client
    try:
        protocol = getProtocol()
        g_imweb_client = imweb_service.Client(protocol)
        print "conneted g_imweb_client ", g_imweb_client
        print "imweb connected"
    except Exception, e:
        print "connectimwebdb error", e
        g_imweb_client = None


def getImwebConn():
    return g_imweb_client


#initConnect()

