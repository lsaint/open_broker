from django.db import models, connections


class LockManager(models.Manager):

    connection = connections["default"]

    def lock(self):
        cursor = self.connection.cursor()
        table = self.model._meta.db_table
        cursor.execute("LOCK TABLES %s WRITE" % table)
        row = cursor.fetchone()
        return row


    def unlock(self):
        cursor = self.connection.cursor()
        table = self.model._meta.db_table
        cursor.execute("UNLOCK TABLES")
        row = cursor.fetchone()
        return row


    def genAppid(self, is_test=False):
        try:
            self.lock()
            item = self.all()[0]
            if is_test:
                item.test_appid += 1
                item.save()
                return item.test_appid
            else:
                item.release_appid += 1
                item.save()
                return item.release_appid
        finally:
            self.unlock()



class CurAppid(models.Model):
    release_appid = models.IntegerField()
    test_appid = models.IntegerField()

    objects = LockManager()

    class Meta:
        db_table  = "curappid"

