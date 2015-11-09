
import os

CONF_PATH = os.path.abspath(".") + "/conf"

os.chdir(CONF_PATH)

os.system("cp deploy_conf.py conf.py")
os.system("cp deploy_uwsgi.xml uwsgi.xml")
os.system("cp deploy_haproxy.cfg haproxy.cfg")
os.system("cp deploy_supervisord.conf ./supervisord.conf")

print "L' conf done"
