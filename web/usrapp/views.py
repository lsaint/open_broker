# -*- coding: utf-8 -*-

# Create your views here.

import json

from django.http import *
from django.shortcuts import *
from django.core import serializers

from web.view_common import *
import node.node2appmgr as am



class UserappHandle(ModelHandle):

    def __call__(self, request, **kwargs):
        try:
            self.limit = int(kwargs.pop("limit"))
            self.offset = int(kwargs.pop("offset"))
        except:
            self.limit = None
        kwargs["app_status__gte"] = 16 # 大于等于16表示存在 小于16的标记为已删除
        return super(UserappHandle, self).__call__(request, **kwargs)


    def query(self):
        if self.limit is None:
            return self.model.objects.filter(**self.kwargs)
        else:
            return self.model.objects.filter(**self.kwargs)[self.offset:self.offset+self.limit]


    def count(self, request, **kwargs):
        return HttpResponse(self.model.objects.filter(**kwargs).count())


def addUsrApp(**kwargs):
    return HttpResponse(am.manageUsrApp(kwargs["uid"], kwargs["appid"], True))


def delUsrApp(**kwargs):
    return HttpResponse(am.manageUsrApp(kwargs["uid"], kwargs["appid"], False))


def setSidUsrAppSwitch(**kwargs):
    return HttpResponse(am.setSidUsrAppSwitch(kwargs["sid"], kwargs["parentsid"], kwargs["subsid"], kwargs["sw"]))


# get

def checkUsrAppPrivileges(request, **kwargs):
    return HttpResponse(am.checkUsrAppPrivileges(kwargs["uid"], kwargs["appid"]))

