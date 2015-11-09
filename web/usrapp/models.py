from django.db import models


class Userapp(models.Model):
    userid = models.IntegerField(primary_key=True)
    appid = models.IntegerField(primary_key=True)
    oper = models.CharField(max_length=96, blank=True)
    create_time = models.DateTimeField()
    modify_time = models.DateTimeField()
    app_status = models.IntegerField()
    app_ranking = models.IntegerField()
    groupid = models.IntegerField()
    expand = models.TextField(blank=True)
    reserve1 = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'userapp'



class ChannelUserappConfig(models.Model):
    sid = models.IntegerField()
    parentsid = models.IntegerField()
    subsid = models.IntegerField(primary_key=True)
    #oper = models.CharField(max_length=96, blank=True)
    #create_time = models.DateTimeField()
    #modify_time = models.DateTimeField()
    userapp_switch = models.IntegerField()
    #expand = models.TextField(blank=True)
    #reserve1 = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'channel_userapp_config'


