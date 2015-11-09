# -*- coding:utf-8 -*-

import json

from django.http import *
from django.shortcuts import *
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


REP_SUCESS = "1"
REP_ERROR  = "0"


def filterMultiParam(v):
    lt = v.split("/")
    lt = map(lambda x:str(x), lt)
    return filter(lambda x:x, lt)


def filterMultiParamByKw(s, to_str=False):
    #v = kwargs.values()[0]
    lt = filterMultiParam(s)
    if to_str:
        tp = tuple(lt)
        if len(tp) == 1:
            tp = str(tp)[:-2] + ")" # 去掉逗号
        tp = str(tp)
        return tp
    return lt


def genUtf8Dict(dt):
    utf8_dt = {}
    for k, v in dt.items():
        if type(v) == type(u""):
            utf8_dt[k.encode('utf-8')] = v.encode('utf-8') 
        elif type(v) == type([]):
            lt = []
            #utf8_dt[k.encode('utf-8')] = [x.encode('utf-8') for x in v if type(x) != type(0)]
            for x in v:
                if type(x) != type(0):
                    lt.append(x.encode('utf-8'))
                else:
                    lt.append(x)
            utf8_dt[k.encode('utf-8')] = lt
        else:
            utf8_dt[k.encode('utf-8')] = v
    return utf8_dt



class ModelHandle(object):

    csrf_exempt = True

    def __init__(self, model):
        self.model = model


    def __call__(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs

        for k, v in self.kwargs.items():
            if k.endswith("__in"):
                self.kwargs[k] = filterMultiParam(v)

        try:
            handle = getattr(self, "do%s" % request.method)
        except AttributeError:
            return HttpResponseBadRequest()

        return handle()


    def doGET(self):
        if not self.kwargs:
            raise Http404

        ins = self.query()
        jn = serializers.serialize("json", ins)
        return HttpResponse(jn, mimetype="application/json")


    def query(self):
        return self.model.objects.filter(**self.kwargs)


    # create
    def doPOST(self):
        print "create -- raw_post_data", self.request.raw_post_data
        jn = json.loads(self.request.raw_post_data)
        jn2 = genUtf8Dict(jn)
        self.model.objects.create(**jn2)
        return HttpResponse(REP_SUCESS)


    # update
    def doPUT(self):
        print "put -- raw_post_data", self.request.raw_post_data
        deserialized = list(serializers.deserialize("json", self.request.raw_post_data))
        [x.object.save() for x in deserialized]
        return HttpResponse(REP_SUCESS)


    def doDELETE(self):
        if not self.kwargs:
            return HttpResponseBadRequest()
        ins = self.query()
        ins.delete()
        return HttpResponse(REP_SUCESS)


    def count(self, request, **kwargs):
        return HttpResponse(self.model.objects.filter(**kwargs).count())



class MethodDispatch(object):

    csrf_exempt = True

    def __init__(self, method, handle):
        self.handle = handle
        self.method = method


    def __call__(self, request):
        if request.method != self.method:
            return HttpResponseBadRequest()

        try:
            print "request.raw_post_data", request.raw_post_data
            kwargs = json.loads(request.raw_post_data)
            kwargs = genUtf8Dict(kwargs)
            print "post kwargs", kwargs
            return self.handle(**kwargs)
        except Exception, e:
            print "MethodDispatch exception", e
            return HttpResponseBadRequest()

