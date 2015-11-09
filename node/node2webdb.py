# -*- coding: utf-8 -*-

import os, sys
path = os.path.abspath(".")
sys.path.insert(0, path)

from  node_common import *


@socketDecorator(connectImwebdb)
def getImidByUid(uid):
    return getImwebConn().imweb_get_imid_by_uid(uid)


@socketDecorator(connectWebdb)
def validateOwner(sid, uid):
    return getWebdbConn().validate_session_owner(sid, uid, 2)


@socketDecorator(connectWebdb)
def getChlRoles(uid, roles):
    return getWebdbConn().batch_get_session_list_by_role(uid, roles, "type", False, 2)


@socketDecorator(connectWebdb)
def getUid(passport):
    return getWebdbConn().get_uid_by_passport(passport.encode("utf8"), 2)


@socketDecorator(connectWebdb)
def getSubSessionsInfo(sid, subsid):
    return getWebdbConn().batch_get_sub_sessions_info(sid, subsid, ["sid", "name", "sort"], False, 2).dataset


@socketDecorator(connectWebdb)
def getSidByAsid(sid):
    return getWebdbConn().get_sid_by_asid(sid, 2)


@socketDecorator(connectWebdb)
def batchGetSessionInfo(sids):
    return getWebdbConn().batch_get_session_info(sids, ["sid", "name", "logo_index"], 2).dataset


@socketDecorator(connectWebdb)
def batchGetSessionLogoUrl(sids):
    return getWebdbConn().batch_get_session_logo_url(sids, 2).dataset


@socketDecorator(connectWebdb)
def batchGetUserInfo(uids):
    return getWebdbConn().batch_get_user_info(uids, ["nick", "sex"], 2).dataset


@socketDecorator(connectWebdb)
def batchGetSessionAsid(sids):
    return getWebdbConn().batch_get_session_asid(sids, 2).dataset


#print getUid("《微微笑》".decode("utf8"))
#print batchGetSessionAsid(["23995943"])
#print batchGetUserInfo(["10593000"])
#print getImidByUid("10593000")
#print validateOwner("1640285", "10593000")
#print g_webdb_client.batch_get_sub_sessions_info("1640285","1640285", ["sid", "pid", "name", "sort"], True, 0)
#print getSubSessionsInfo("1640285").dataset
#print getSidByAsid("300")
#print batchGetSessionInfo(["90962674"])
#print batchGetSessionLogoUrl(["90962674"])
