# -*- coding: utf8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django import forms
from django.forms.widgets import Select

from node.node2appmgr import *
from node.node2cs import *

# admin tools form
ATF_CLOUND = "1"
ATF_ADDAPP = "2"
ATF_DELCHLAPP = "3"
ATF_ADDWHITE = "4"
ATF_DELWHITE = "5"
ATF_SETTES = "6"
ATF_DELAPP = "7"
ATF_ADDMOD = "8"



def exceptDecorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception, e:
            print func.func_name, "---", e
            return HttpResponse(str(e))
    return wrapper


## admin tools ###

class FormEnableClound(forms.Form):
    tool_type = forms.IntegerField(widget=forms.HiddenInput(attrs={'value':ATF_CLOUND}))
    app_id = forms.IntegerField()


class FormAddChlApp(forms.Form):
    tool_type = forms.IntegerField(widget=forms.HiddenInput(attrs={'value':ATF_ADDAPP}))
    app_id = forms.IntegerField()
    channel = forms.IntegerField()


class FormDelChlApp(forms.Form):
    tool_type = forms.IntegerField(widget=forms.HiddenInput(attrs={'value':ATF_DELCHLAPP}))
    app_id = forms.IntegerField()
    channel = forms.IntegerField()



class FormDelChlWhite(forms.Form):
    tool_type = forms.IntegerField(widget=forms.HiddenInput(attrs={'value':ATF_DELWHITE}))
    app_id = forms.IntegerField()
    channel = forms.IntegerField()


class FormAddChlWhite(forms.Form):
    tool_type = forms.IntegerField(widget=forms.HiddenInput(attrs={'value':ATF_ADDWHITE}))
    app_id = forms.IntegerField()
    channel = forms.IntegerField()


class FormDelApp(forms.Form):
    tool_type = forms.IntegerField(widget=forms.HiddenInput(attrs={'value':ATF_DELAPP}))
    app_id = forms.IntegerField()


#radio_select_test = ((1, "测试版"), (0, "正式版"))
#class FormCreateModifyApp(forms.Form):
#    tool_type = forms.IntegerField(widget=forms.HiddenInput(attrs={'value':ATF_CREATE}))
#    app_id = forms.IntegerField()
#    is_test = forms.ChoiceField(widget=Select, choices=radio_select_test, initial=1)
#


class FormSetTestApp(forms.Form):
    tool_type = forms.IntegerField(widget=forms.HiddenInput(attrs={'value':ATF_SETTES}))
    app_id = forms.IntegerField()
    version = forms.IntegerField()
    channel = forms.IntegerField()


class FormAddModifyVer(forms.Form):
    tool_type = forms.IntegerField(widget=forms.HiddenInput(attrs={'value':ATF_ADDMOD}))
    app_id = forms.IntegerField()
    version = forms.IntegerField()
    url     = forms.CharField()
    md5     = forms.CharField()


def onAddModifyVersion(request, app_id):
    print "request.POST", request.POST, app_id
    ret = addModifyVersion(app_id, None,\
                    **{"verurl":request.POST["url"],\
                    "vermd5":request.POST["md5"], "verid":int(request.POST["version"])})
    return HttpResponse(ret)


def onEnableClound(request, app_id):
    ret = enableCloudSave(app_id)
    return HttpResponse("%d %s" % (app_id, ret))


@exceptDecorator
def onAddChlApp(request, app_id):
    chl = int(request.POST["channel"])
    ret = addChlApp(app_id, chl, [chl])
    return HttpResponse("%d %d %s" % (app_id, chl, ret))


@exceptDecorator
def onDelChlApp(request, app_id):
    chl = int(request.POST["channel"])
    ret = delChlApp(app_id, chl, [chl])
    return HttpResponse("%d %d %s" % (app_id, chl, ret))


@exceptDecorator
def onAddChlWhite(request, app_id):
    chl = int(request.POST["channel"])
    ret = addChlWhite(app_id, chl)
    return HttpResponse(ret)


@exceptDecorator
def onDelChlWhite(request, app_id):
    chl = int(request.POST["channel"])
    ret = delChlWhite(app_id, chl)
    return HttpResponse(ret)


@exceptDecorator
def onSetTestAppToChannel(request, app_id):
    version = request.POST.get("version")
    channel = request.POST.get("channel")
    ret = setTestAppToChannel(app_id, int(version), int(channel))
    return HttpResponse("%d %s" % (app_id, ret))


@exceptDecorator
def onDelApp(request, app_id):
    return HttpResponse(delApp(app_id))

#### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ## 


L = ( ("FormEnableClound", ATF_CLOUND, onEnableClound),
        ("FormAddChlApp", ATF_ADDAPP, onAddChlApp),
        ("FormDelChlApp", ATF_DELCHLAPP, onDelChlApp),
        ("FormAddChlWhite", ATF_ADDWHITE, onAddChlWhite),
        ("FormDelChlWhite", ATF_DELWHITE, onDelChlWhite),
        ("FormSetTestApp", ATF_SETTES, onSetTestAppToChannel),
        ("FormDelApp", ATF_DELAPP, onDelApp),
        ("FormAddModifyVer", ATF_ADDMOD, onAddModifyVersion),
    )

@staff_member_required
def AdminTools(request):
    if request.method == 'POST':
        t = request.POST["tool_type"]
        try:
            app_id = int(request.POST["app_id"])
        except:
            return HttpResponse("缺少app_id")
    else:
        t = None

    render_dt = {}

    for tp in L:
        form_ins = tp[0].lower()
        form_class_name = tp[0]
        atf = tp[1]
        callback = tp[2]

        exec("%s = %s()" % (form_ins, form_class_name)) 

        if t == atf:    return callback(request, app_id)

        exec("render_dt['%s'] = %s" % (form_ins, form_ins))

    return render_to_response(
            "admin/ctrl/admin_tools.html",
            render_dt,
            context_instance=RequestContext(request))

