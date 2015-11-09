# -*- coding: utf-8 -*-

DEBUG = True

### node

STATISTIC_ADDR = ("127.0.0.1", 16410)
#STATISTIC_ADDR = ("58.215.46.92", 16410)
#CLOUND_ADDR = ("111.178.146.46", 18927)
CLOUND_ADDR = ("119.97.153.177", 18927)

#APPMGR_ADDR = ("121.14.241.43", 7720)
APPMGR_ADDR = ("127.0.0.1", 7720)

#WEBDB_ADDR = ("222.88.95.117", 8090)
WEBDB_ADDR = ("127.0.0.1", 8090)
# webdb 亚太访问较快 121.14.47.200 8090
# webdb 洛阳访问较快 222.88.95.117 8090
# webdb 备用 59.151.23.92 8090


### Django


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'opbak',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '111333',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }, 

    'appmanager': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'appmanager',                      # Or path to database file if using sqlite3.
        'USER': 'myshard',                      # Not used with sqlite3.
        'PASSWORD': 'myshard',                  # Not used with sqlite3.
        #'HOST': '222.186.49.42',
        #'HOST': '111.178.146.46',
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '8889',                      # Set to empty string for default. Not used with sqlite3.
    },

    'usrapp': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'userapp_manager',
        'USER': 'myshard',
        'PASSWORD': 'myshard',
        #'HOST': '111.178.146.46',
        'HOST': '127.0.0.1',
        'PORT': '6208',
    },

    'maid': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'maid_service',
        'USER': 'lsaint',
        'PASSWORD': 'lsaint',
        'HOST': '111.178.146.46',
        'PORT': '6208',
    }
}


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/home/lsaint/trunk/projs/yy_web/src/broker/web/templates",
    "/Users/lsaint/Envs/dj13/broker/web/templates",
)

