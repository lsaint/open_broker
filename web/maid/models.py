from django.db import models

# Create your models here.
class MaidInfo(models.Model):
    uid = models.IntegerField(primary_key=True)
    appid = models.IntegerField(primary_key=True)
    #service_level = models.IntegerField()
    #service_score = models.BigIntegerField()
    #total_s_time = models.BigIntegerField()
    #total_s_cnt = models.BigIntegerField()
    #points = models.BigIntegerField()
    #price = models.IntegerField()
    #status = models.IntegerField()
    #start_time = models.DateTimeField()
    #yb = models.IntegerField()
    #yb_price = models.IntegerField()
    class Meta:
        db_table = u'maid_info'
