# -*- coding: utf-8 -*-

tables_appmgr = ('app_info', 'appcheckinfo', 'appidmutilversion', 'appidmvchannel',
                    'chn_app_whitelist', 'sidapp_flag', 'channelapp', 'sid_appattrib')

tables_usrapp = ('userapp', 'channel_userapp_config')

tables_maid = ('maid_info',)

class DbRouter(object):

    def db_for_read(self, model, **hints):
        if model._meta.db_table in tables_appmgr:
            return 'appmanager'

        if model._meta.db_table in tables_usrapp:
            return 'usrapp'

        if model._meta.db_table in tables_maid:
            return 'maid'

    ## for test
    #def db_for_write(self, model, **hints):
    #    if model._meta.db_table in tables_appmgr:
    #        return 'appmanager'

    #def allow_syncdb(self, db, model):
    #    "Make sure the myapp app only appears on the 'other' db"
    #    if db == 'appmanager':
    #        return False
    #    elif model._meta.db_table  in ('app_info', 'appcheckinfo'):
    #        return False

