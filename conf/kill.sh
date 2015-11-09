supervisorctl stop uwsgi
supervisorctl stop haproxy
#supervisorctl shutdown
#cat /var/run/haproxy.pid | xargs kill -9
#ps ax | grep [s]tati_d.py | awk {'print $1'} | xargs kill -9

#ps ax | grep "[s]upervisord" | awk {'print $1'} | xargs kill -9
#ps ax | grep  "[h]aproxy" | awk {'print $1'} | xargs kill -9
#ps ax | grep  "[s]tati_d" | awk {'print $1'} | xargs kill -9
#ps ax | grep -e "broker$" -e "broker_master" | grep -v grep | awk {'print $1'} | xargs kill -9
