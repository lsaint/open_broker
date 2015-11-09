# -*- coding:utf-8 -*-
import syslog

from django.db import models,connection
from django.db.models.signals import post_save
from django.core.signals import request_finished
from django.dispatch import receiver




@receiver(request_finished)
def debugRequestFinished(sender, **kwargs):
    from conf import conf
    if not conf.DEBUG:return
    from django.db import connections
    #q = connections["usrapp"].queries
    #q = connections["default"].queries
    q = connections["appmanager"].queries
    if q:
        print "sql............................"
        print q



class Developer(models.Model):
    uid = models.IntegerField(primary_key=True)
    dev_type = models.SmallIntegerField()
    com_name = models.CharField(max_length=40, blank=True)
    nick_name = models.CharField(max_length=12)
    real_name = models.CharField(max_length=10)
    phone = models.BigIntegerField()
    email = models.EmailField()
    id_card = models.CharField(max_length=18, blank=True)
    address = models.CharField(max_length=50)
    yy_num = models.BigIntegerField()
    dev_url = models.URLField(blank=True)
    licence_img = models.CharField(max_length=100, blank=True)
    authorization = models.CharField(max_length=100, blank=True)
    reg_time = models.DateTimeField()

    #class Meta:
    #    db_table = u'operation_developer2'



@receiver(post_save, sender=Developer)
def developerPostSave(sender, **kwargs):
    if kwargs["created"]:
        syslog.syslog("OPEN_S_SYSTEM,2,5,%s,,,,,,,,1" % kwargs["instance"].uid)




class AppDevInfo(models.Model):
    appid = models.IntegerField(primary_key=True)
    developer = models.IntegerField()
    channels = models.CharField(max_length=64)  # models.IntegerField()
    doc = models.CharField(max_length=100, blank=True)
    test_time = models.DateTimeField(blank=True, null=True)
    show_pics = models.CharField(max_length=512, blank=True)
    change_log = models.CharField(max_length=512, blank=True)
    status = models.SmallIntegerField(default=1)
    check_ret = models.CharField(max_length=100, blank=True)
    check_status = models.SmallIntegerField(default=0)
    frequency = models.SmallIntegerField(default=1)

    #class Meta:
    #    db_table = u'operation_appdevinfo2'




class AppComment(models.Model):
    uid = models.IntegerField(db_index=True)
    appid = models.IntegerField(db_index=True)
    comment = models.CharField(max_length=2000)
    time = models.DateTimeField(auto_now_add=True)
    check = models.SmallIntegerField(default=0)


class ScoreManager(models.Manager):

    def avgScore(self, appids):
        cursor = connection.cursor()
        cursor.execute("select appid, avg(score) from ctrl_appscore where appid in %s group by appid" % str(appids))
        return cursor.fetchall()



class AppScore(models.Model):
    uid = models.IntegerField(db_index=True)
    appid = models.IntegerField(db_index=True)
    version = models.IntegerField()
    score = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    objects = ScoreManager()


class AppNotice(models.Model):
    uid = models.IntegerField(db_index=True)
    appid = models.IntegerField(db_index=True)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=5000)
    time = models.DateTimeField(auto_now_add=True)



class KvConfig(models.Model):
    key = models.CharField(max_length=20, db_index=True)
    value = models.CharField(max_length=200)



### ### ### ### ### ### ### ###
### appmgr database ### ### ###
### trunk/apps/appcachem_d/sql
### ### ### ### ### ### ### ###



class AppBasicInfo(models.Model):
    am_appid = models.IntegerField(primary_key=True)
    passwd = models.CharField(max_length=192)
    am_appname = models.CharField(max_length=384)
    app_filename = models.CharField(max_length=384, blank=True)
    am_description = models.CharField(max_length=768, blank=True)
    am_recommend_ver = models.IntegerField()
    delayflag = models.IntegerField()
    istest = models.IntegerField()
    issubsidapp = models.IntegerField()
    app_pos_type = models.IntegerField()
    app_binary_type = models.IntegerField()
    app_attrib = models.IntegerField()
    app_data_dis_type = models.IntegerField()
    add_time = models.DateTimeField()
    last_modify_time = models.DateTimeField()
    need_yy_lbs = models.IntegerField()
    expand = models.TextField(blank=True)
    carry_able = models.SmallIntegerField(default=0)
    reserve1 = models.IntegerField(default=0)
    reserve2 = models.IntegerField(default=0)
    reserve3 = models.IntegerField(default=0)

    class Meta:
        #db_table = u'operation_appbasicinfo2'
        db_table = u'app_info'

    def save(self, force_insert=False, force_update=False, using=None):
        print "appbasicinfo save", force_insert, force_update
        import node.node2appmgr as appmgr
        if not appmgr.createModifyApp(self.__dict__):
            raise Exception("Exception: post create AppBasicInfo error")



class AppVersion(models.Model):
    am_appid = models.IntegerField(primary_key=True)
    am_appver = models.IntegerField()
    am_appurl = models.CharField(max_length=768, blank=True)
    am_appmd5 = models.CharField(max_length=96, blank=True)
    am_exemd5 = models.CharField(max_length=96, blank=True)
    am_vmax = models.IntegerField()
    am_vmin = models.IntegerField()
    expand = models.TextField(blank=True)

    class Meta:
        db_table = u'appidmutilversion'


    def save(self, force_insert=False, force_update=False, using=None):
        print "AppVersion save sucess"
        import node.node2appmgr as appmgr
        if not appmgr.addModifyVersion(self.am_appid, self.__dict__):
            raise Exception("Exception: post addModifyVersion error")



class Appcheckinfo(models.Model):
    appid = models.IntegerField(primary_key=True)
    date_num = models.IntegerField(null=True, blank=True)
    day_count = models.IntegerField(null=True, blank=True)
    online_lower = models.IntegerField(null=True, blank=True)
    open_time = models.IntegerField(null=True, blank=True)
    day_quota = models.IntegerField(null=True, blank=True)
    day_rest = models.IntegerField(null=True, blank=True)
    add_limit = models.IntegerField(null=True, blank=True) # 总开放额度
    add_rest = models.IntegerField(null=True, blank=True)  # 总开放剩额
    chk_flag = models.IntegerField(null=True, blank=True)
    free_flag = models.IntegerField(default=0)
    reserve1 = models.IntegerField(default=0)
    expand = models.TextField(blank=True)


    class Meta:
        db_table = u"appcheckinfo"



class SidappFlag(models.Model):
    topsid = models.IntegerField(primary_key=True)
    appid = models.IntegerField(primary_key=True)
    added_flag = models.IntegerField()
    expand = models.TextField(blank=True)
    class Meta:
        db_table = u'sidapp_flag'



class ChnAppWhitelist(models.Model):
    channel_id = models.IntegerField(primary_key=True)
    app_id = models.IntegerField()
    operator = models.CharField(max_length=768)
    op_time = models.DateTimeField()
    class Meta:
        db_table = u'chn_app_whitelist'



class Appidmvchannel(models.Model):
    am_appid = models.IntegerField(primary_key=True)
    am_appver = models.IntegerField(primary_key=True)
    am_appchn = models.IntegerField(primary_key=True)
    expand = models.TextField(blank=True)

    class Meta:
        db_table = u'appidmvchannel'
        unique_together = (("am_appid", "am_appver", "am_appchn"),)

    def save(self, force_insert=False, force_update=False, using=None):
        import node.node2appmgr as appmgr
        if not appmgr.setTestAppToChannel(self.am_appid, self.am_appver, self.am_appchn):
            raise Exception("Exception: post setTestAppToChannel error")
        print "Appidmvchannel save sucess"



class Channelapp(models.Model):
    channelid = models.IntegerField(primary_key=True)
    appid = models.IntegerField(primary_key=True)
    createdate = models.DateTimeField()
    parentsid = models.IntegerField()
    groupid = models.IntegerField()
    expand = models.TextField(blank=True)
    class Meta:
        db_table = u'channelapp'


class AppAttrib(models.Model):
    channelid = models.IntegerField(primary_key=True)
    parentsid = models.IntegerField()
    front_appid = models.IntegerField()
    createdate = models.DateTimeField()
    expand = models.TextField(blank=True)
    class Meta:
        db_table = u"sid_appattrib"

