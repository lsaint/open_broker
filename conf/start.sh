#!/bin/bash

pid=`ps ax | grep [s]upervisord | awk {'print $1'}`
if [ x$pid != "x" ]; then
    echo "found supervisord"
else
    if [ x$1 = "x" ]; then
        echo "please enter supervistor's conf file path"
        exit
    fi
    echo "starting supervisord with conf", $1
    supervisord -c $1
    if [ x$1 != "x0" ]; then
        supervisorctl start uwsgi_log
    fi
fi
supervisorctl start haproxy
supervisorctl start uwsgi

tail -f /data/broker/broker.log



#haproxy -f haproxy.cfg
#uwsgi -x uwsgi.xml -d ../log/broker.log
#python ../node/stati_d.py
#supervisord -c supervisord.conf

