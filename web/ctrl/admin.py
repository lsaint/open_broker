# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.forms.widgets import RadioSelect

from web.ctrl.models import *
from common import *


STATUS_RADIO_TYPE = ((APP_STATUS_DEVELOP,"开发" ), (APP_STATUS_TEST, "测试"),\
                        (APP_STATUS_READY, "就位"),(APP_STATUS_PUBLISH, "发布"),)


CHECK_STATUS_RADIO_TYPE = ( (CS_NULL, "空"),\
                            (CS_TESTING, "测试中"), (CS_TEST_PASS, "测试通过"), \
                            (CS_TEST_FAIL, "测试失败"), (CS_CHECKING_PUB, "发布审核中"), \
                            (CS_CHECK_PUB_PASS, "发布审核通过"), (CS_CHECK_PUB_FAIL, "发布审核失败"), )


class DeveloperAdmin(admin.ModelAdmin):
    list_display = search_fields =  ("uid", "nick_name", "real_name")



class AppBasicAdminForm(forms.ModelForm):
    am_description  = forms.CharField(widget=forms.Textarea)


class AppBasicInfoAdmin(admin.ModelAdmin):
    form = AppBasicAdminForm
    search_fields = ("am_appid", "am_appname", )
    list_display = ("am_appid", "am_appname", "add_time")
    ordering = ('-add_time',)



class AppDevAdminForm(forms.ModelForm):
    status = forms.ChoiceField(widget=RadioSelect, choices=STATUS_RADIO_TYPE)
    check_status = forms.ChoiceField(widget=RadioSelect, choices=CHECK_STATUS_RADIO_TYPE)
    change_log = forms.CharField(widget=forms.Textarea, required=False)

class AppDevInfoAdmin(admin.ModelAdmin):
    form = AppDevAdminForm
    search_fields = ("appid", "developer", )
    list_display = ("appid", "developer", "status", "check_status", "test_time")


class AppVersionAdmin(admin.ModelAdmin):
    list_display = ("am_appid", "am_appver", "am_appurl", "am_appmd5")
    search_fields = ("am_appid", "am_appver")


class AppcheckinfoAdmin(admin.ModelAdmin):
    search_fields = ("appid", )
    list_display = ("appid", "add_limit", "add_rest")


class AppidmvchannelAdmin(admin.ModelAdmin):
    search_fields = ("am_appchn",  "am_appid")
    list_display = ("am_appchn",  "am_appid", "am_appver", )


class SidappFlagAdmin(admin.ModelAdmin):
    list_display = search_fields = ("topsid", "appid", )



class AppCommentAdminForm(forms.ModelForm):
    comment  = forms.CharField(widget=forms.Textarea)

class AppCommentAdmin(admin.ModelAdmin):
    form = AppCommentAdminForm
    list_display = ("appid", "uid", "comment")
    search_fields = ("appid", "uid", )
    list_filter = ("time", )


class AppScoreAdmin(admin.ModelAdmin):
    search_fields = ("appid", "uid")
    list_display = ("appid", "uid", "score", "version")
    list_filter = ("time", )



class AppNoticeAdminForm(forms.ModelForm):
    content  = forms.CharField(widget=forms.Textarea)

class AppNoticeAdmin(admin.ModelAdmin):
    form = AppNoticeAdminForm
    search_fields = ("appid", "uid")
    list_display = ("appid", "uid", "title")
    list_filter = ("time", )
    date_hierarchy = "time"


#class ChnAppWhitelistAdmin(admin.ModelAdmin):
#    search_fields = ("channel_id", )
#    list_display = ("channel_id", "app_id", "operator")



admin.site.register(Developer, DeveloperAdmin)
admin.site.register(AppBasicInfo, AppBasicInfoAdmin)
admin.site.register(AppDevInfo, AppDevInfoAdmin)
admin.site.register(AppVersion, AppVersionAdmin)
admin.site.register(Appcheckinfo, AppcheckinfoAdmin)
admin.site.register(Appidmvchannel, AppidmvchannelAdmin)
admin.site.register(SidappFlag, SidappFlagAdmin)
admin.site.register(AppComment, AppCommentAdmin)
admin.site.register(AppScore, AppScoreAdmin)
admin.site.register(AppNotice, AppNoticeAdmin)

# 这2个表在myshard不支持直接count(*) 无法显示
#admin.site.register(ChnAppWhitelist, ChnAppWhitelistAdmin)
#admin.site.register(Channelapp)
#admin.site.register(AppAttrib)

