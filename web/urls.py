# -*- coding:utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from web.view_common import MethodDispatch, ModelHandle
from web.ctrl.models import *
from web.ctrl.views import *
from web.appid_getter.views import genReleaseAppid
from web.usrapp.models import *
from web.usrapp.views import *
from web.maid.models import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^web/', include('web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/ctrl/admin_tools/$', 'web.ctrl.admin_tools.AdminTools'),
    url(r'^admin/', include(admin.site.urls)),

	url(r'^getdeveloperapps/uid/(?P<uid>\d+)/$', getDeveloperApps),
	url(r'^getchlroles/uid/(?P<uid>\d+)/roles/(?P<roles>.*)/$', getChlRoles),
	url(r'^validateow/channel/(?P<channel>\d+)/uid/(?P<uid>\d+)/$', validateOw),
	url(r'^getyyid/uid/(?P<uid>\d+)/$', getYyIdByUid),
	url(r'^getuid/passport/(?P<passport>.*)/$', getUid),
	url(r'^searchapp/name/(?P<name>.*)/$', searchApp),
	url(r'^getlatelyapp/count/(?P<count>\d+)/$', getLatelyApp),
	url(r'^getallreleaseapp/$', getAllReleaseApp),
	url(r'^getapptopnsids/appids/(?P<appid>.*)/n/(?P<n>\d+)/$', getAppTopnSids),
	url(r'^getsubsessionsinfo/channel/(?P<sid>\d+)/sub/(?P<subsid>\d+)/$', getSubSessionsInfo),
	url(r'^getsidbyasid/channel/(?P<sid>\d+)/$', getSidByAsid),
	url(r'^batchgetasid/channels/(?P<sids>.*)/$', batchGetSessionAsid),
	url(r'^batchgetsessioninfo/channels/(?P<sids>.*)/$', batchGetSessionInfo),
	url(r'^batchgetsessionlogourl/channels/(?P<sids>.*)/$', batchGetSessionLogoUrl),
	url(r'^getchannelapps/channel/(?P<sid>\d+)/$', getChannelApps),
	url(r'^ischannelappwhitelist/channel/(?P<channel_id>\d+)/appid/(?P<app_id>\d+)/$', isChannelAppInWhilelist),
	url(r'^getchannelappwhitelist/channel/(?P<channel_id>\d+)/offset/(?P<offset>\d+)/limit/(?P<limit>\d+)/$', getChannelAppWhitelist),
	url(r'^getchannelappwhitelist/channel/(?P<channel_id>\d+)/count/$', getChannelAppWhitelistCount),
	url(r'^getchannelnonfreeapps/channel/(?P<channel_id>\d+)/$', getChannelNonfreeApps),
	url(r'^batchgetuserinfo/uids/(?P<sids>.*)/$', batchGetUserInfo),
	url(r'^checkchlprivileges/appid/(?P<appid>\d+)/channel/(?P<sid>\d+)/$', checkChlPrivileges),
	url(r'^getsubchannelapp/channel/(?P<parentsid>\d+)/$', getSubChannelApp),
	url(r'^checkusrappprivileges/uid/(?P<uid>\d+)/appid/(?P<appid>\d+)/$',  checkUsrAppPrivileges),
    url(r'^getautoapp/parentsid/(?P<parentsid>\d+)/$', getAutoApp),

	url(r'^appversion/appid/(?P<am_appid>\d+)/$', ModelHandle(AppVersion)),

	url(r'^developer/uid/(?P<uid>\d+)/$', ModelHandle(Developer)),
	url(r'^developer/yy/(?P<yy_num>\d+)/$', ModelHandle(Developer)),
	url(r'^developer/nick_name/(?P<nick_name>.*)/$', ModelHandle(Developer)),
	url(r'^developer/real_name/(?P<real_name>.*)/$', ModelHandle(Developer)),
	url(r'^developer/phone/(?P<phone>\d+)/$', ModelHandle(Developer)),
	url(r'^developer/email/(?P<email>.*)/$', ModelHandle(Developer)),
	url(r'^developer/reg_time_start/(?P<reg_time__gt>.*)/reg_time_end/(?P<reg_time__lt>.*)/$', ModelHandle(Developer)),

	url(r'^appcheckinfo/appid/(?P<appid>\d+)/$', ModelHandle(Appcheckinfo)),
	url(r'^appcheckinfo/appids/(?P<appid__in>.*)/$', ModelHandle(Appcheckinfo)),

	url(r'^appbasicinfo/appid/(?P<am_appid>\d+)/$', ModelHandle(AppBasicInfo)),
	url(r'^appbasicinfo/appname/(?P<am_appname__icontains>.*)/$', AppBasicInfoHandle(AppBasicInfo)),
	url(r'^appbasicinfo/istest/(?P<istest>\d+)/appattrib/(?P<app_attrib>\d+)/carry_able/(?P<carry_able__in>.*)/$', AppBasicInfoHandle(AppBasicInfo)),
	url(r'^appbasicinfo/istest/(?P<istest>\d+)/appattrib/(?P<app_attrib>\d+)/reserve1/(?P<reserve1_in>.*)/$', AppBasicInfoHandle(AppBasicInfo)),
	url(r'^appbasicinfo/istest/(?P<istest>.*)/carry_able/(?P<carry_able>.*)/appattrib/(?P<app_attrib>\d+)/count/$', countBasicInfoSlice_iac),
	url(r'^appbasicinfo/istest/(?P<istest>.*)/reserve1/(?P<reserve1>.*)/reserve2/(?P<reserve2>\d+)/appattrib/(?P<app_attrib>\d+)/count/$', countBasicInfoSlice_iarr),
	url(r'^appbasicinfo/istest/(?P<istest>.*)/carry_able/(?P<carry_able>.*)/appattrib/(?P<app_attrib>\d+)/offset/(?P<offset>\d+)/limit/(?P<limit>\d+)/$', getBasicInfoSlice_iac),
	url(r'^appbasicinfo/istest/(?P<istest>.*)/reserve1/(?P<reserve1>.*)/reserve2/(?P<reserve2>\d+)/appattrib/(?P<app_attrib>\d+)/offset/(?P<offset>\d+)/limit/(?P<limit>\d+)/$', getBasicInfoSlice_iarr),
	url(r'^appbasicinfo/istest/(?P<istest>\d+)/reserve1/(?P<reserve1>\d+)/$', AppBasicInfoHandle(AppBasicInfo)),
	url(r'^appbasicinfo/istest/(?P<istest>.*)/carry_able/(?P<carry_able>.*)/count/$', countBasicInfoSlice_ic),
	url(r'^appbasicinfo/istest/(?P<istest>.*)/reserve1/(?P<reserve1>.*)/count/$', countBasicInfoSlice_ir),
	url(r'^appbasicinfo/istest/(?P<istest>.*)/carry_able/(?P<carry_able>.*)/offset/(?P<offset>\d+)/limit/(?P<limit>\d+)/$', getBasicInfoSlice_ic),
	url(r'^appbasicinfo/istest/(?P<istest>.*)/reserve1/(?P<reserve1>.*)/offset/(?P<offset>\d+)/limit/(?P<limit>\d+)/$', getBasicInfoSlice_ir),
	url(r'^appbasicinfo/istest/(?P<istest>\d+)/$', AppBasicInfoHandle(AppBasicInfo)),
	url(r'^appbasicinfo/istest/(?P<istest>\d+)/pos/(?P<app_pos_type>\d+)/$', AppBasicInfoHandle(AppBasicInfo)),
	url(r'^appbasicinfo/appids/(?P<am_appid__in>.*)/$', ModelHandle(AppBasicInfo)),
	url(r'^appbasicinfo/add_time_start/(?P<add_time__gt>.*)/add_time_end/(?P<add_time__lt>.*)/$', ModelHandle(AppBasicInfo)),

	url(r'^appdevinfo/appid/(?P<appid>\d+)/$', ModelHandle(AppDevInfo)),
	url(r'^appdevinfo/status/(?P<status>\d+)/$', ModelHandle(AppDevInfo)),
	url(r'^appdevinfo/check_status/(?P<check_status>\d+)/$', ModelHandle(AppDevInfo)),

    url(r'^appnotice/id/(?P<id>\d+)/$', ModelHandle(AppNotice)),
    url(r'^appnotice/uid/(?P<uid>\d+)/$', ModelHandle(AppNotice)),
    url(r'^appnotice/appid/(?P<appid>\d+)/$', AppNoticeHandle(AppNotice)),
    url(r'^appnotice/$', ModelHandle(AppNotice)),

    url(r'^appscore/id/(?P<id>\d+)/$', ModelHandle(AppScore)),
    url(r'^appscore/uid/(?P<uid>\d+)/$', ModelHandle(AppScore)),
    url(r'^appscore/uid/(?P<uid>\d+)/appid/(?P<appid>\d+)/$', ModelHandle(AppScore)),
    url(r'^appscore/appid/(?P<appid>\d+)/$', ModelHandle(AppScore)),
    url(r'^appscore/appids/(?P<appid__in>.*)/$', getAvgScore),
    url(r'^appscore/appid/(?P<appid>\d+)/count/$', ModelHandle(AppScore).count),
    url(r'^appscore/$', ModelHandle(AppScore)),

    url(r'^appcomment/ids/(?P<id__in>.*)/$', ModelHandle(AppComment)),
    url(r'^appcomment/uid/(?P<uid>\d+)/$', ModelHandle(AppComment)),
    url(r'^appcomment/appid/(?P<appid>\d+)/check/(?P<check>\d+)/offset/(?P<offset>\d+)/limit/(?P<limit>\d+)/$', AppCommentHandle(AppComment)),
    url(r'^appcomment/appid/(?P<appid>\d+)/check/(?P<check>\d+)/count/$', AppCommentHandle(AppComment).count),
    url(r'^appcomment/$', ModelHandle(AppComment)),
	url(r'^appcomment/appid/(?P<appid>\d+)/time_start/(?P<time__gt>.*)/time_end/(?P<time__lt>.*)/$', ModelHandle(AppComment)),
    url(r'^kvconfig/$',                  ModelHandle(KvConfig)),
    url(r'^kvconfig/key/(?P<key>\w+)/$', ModelHandle(KvConfig)),

    url(r'^userapp/uid/(?P<userid>\d+)/offset/(?P<offset>\d+)/limit/(?P<limit>\d+)/$', UserappHandle(Userapp)),
    url(r'^userapp/uid/(?P<userid>\d+)/count/$', UserappHandle(Userapp).count),
    url(r'^userapp/uid/(?P<userid>\d+)/appid/(?P<appid>\d+)/$', UserappHandle(Userapp)),

    url(r'^channeluserappconfig/subsid/(?P<subsid>\d+)/$', ModelHandle(ChannelUserappConfig)),

	url(r'^batchcheckcomment/$',    MethodDispatch("POST", batchCheckComment)),
	url(r'^genappid/$',             MethodDispatch("POST", genReleaseAppid)),
	url(r'^opencloud/$',            MethodDispatch("POST", openCloud)),
	url(r'^addchlapp/$',            MethodDispatch("POST", addChlApp)),
	url(r'^delchlapp/$',            MethodDispatch("DELETE", delChlApp)),
	url(r'^addchloldapp/$',         MethodDispatch("POST", addChlOldApp)),
	url(r'^delchloldapp/$',         MethodDispatch("DELETE", delChlOldApp)),
	url(r'^addchlwhite/$',          MethodDispatch("POST", addChlWhite)),
	url(r'^delchlwhite/$',          MethodDispatch("DELETE", delChlWhite)),
	url(r'^removeappfromchannel/$', MethodDispatch("DELETE", removeAppFromChannel)),

	url(r'^addusrapp/$',            MethodDispatch("POST", addUsrApp)),
	url(r'^delusrapp/$',            MethodDispatch("DELETE", delUsrApp)),
	url(r'^setsidusrappswitch/$',   MethodDispatch("POST", setSidUsrAppSwitch)),

	url(r'^setautoapp/$',   MethodDispatch("POST", setAutoApp)),
	url(r'^delautoapp/$',   MethodDispatch("DELETE", delAutoApp)),

	url(r'^delapp/$',   MethodDispatch("DELETE", delApp)),
	url(r'^delver/$',   MethodDispatch("DELETE", delVer)),

	url(r'^setreleasecount/$',    MethodDispatch("POST", setReleaseCount)),
	url(r'^addmodifyversion/$',   MethodDispatch("POST", addModifyVersion)),

	url(r'^maidinfo/uid/(?P<uid>\d+)/$', ModelHandle(MaidInfo)),

	url(r'^admintest/$', test),
)


#urlpatterns += patterns('web.ctrl.views',
#	url(r'^genappid/$', 'postDispatch'),
#
#	url(r'^applist/(\d+)/$', 'getDeveloperApps'),
#	url(r'^validateow/(\d+)/(\d+)/$', 'validateOw'),
#	url(r'^getyyidbyuid/(\d+)/$', 'getYyIdByUid'),
#)

