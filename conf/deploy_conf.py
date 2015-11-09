# -*- coding: utf-8 -*-

DEBUG = False

### node

STATISTIC_ADDR = ("127.0.0.1", 16410)
CLOUND_ADDR = ("119.97.153.177", 18927)

#APPMGR_ADDR = ("121.14.36.25", 7720)
#APPMGR_ADDR = ("58.215.46.93", 7720)
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
        'NAME': 'open_broker',                      # Or path to database file if using sqlite3.
        'USER': 'open_broker',                      # Not used with sqlite3.
        'PASSWORD': 'dzpwNt38SqM',                  # Not used with sqlite3.
        'HOST': '58.215.46.92',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '6302',                      # Set to empty string for default. Not used with sqlite3.
    }, 

    'appmanager': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'appmanager',                      # Or path to database file if using sqlite3.
        'USER': 'myshard',                      # Not used with sqlite3.
        'PASSWORD': 'myshard',                  # Not used with sqlite3.
        #'HOST': '222.186.49.42',                      # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '8899',                      # Set to empty string for default. Not used with sqlite3.
    },

    'usrapp': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'userapp_manager',
        'USER': 'open_myshard',
        'PASSWORD': 'sxeUD,DM8b',
        'HOST': '58.215.46.93',
        'PORT': '6306',
    }, 

    'maid': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'maid_service',
        'USER': 'open_maid_test',
        'PASSWORD': '47x.123,$',
        'HOST': '113.107.237.52',
        #'HOST': '127.0.0.1',
        'PORT': '6301',
    }
}


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/opt/broker/web/templates",
)

