


#import struct, json
#
#name = "lsaint"
#json_get_appid = { 
#    "oper"      : struct.pack("%ds" % (len(name)),  name),
#    "expand"    : "",
#    "uri" : struct.pack("I", (1032 << 8) | 133), 
#}
#
#
#print json.dumps(json_get_appid)
#
#print struct.pack("I", (1032 << 8) | 133)
#

import os,sys,json

from django.core.management import setup_environ
import settings
setup_environ(settings)

from op.operation.models import *

from op.webdb import *


DOMAIN = "http://open.yy.com/"

#------------------------------------------- 
# create index idx_uid_name_passport on uid_name(passport);
def genUidNameTable():
    passports = []
    for d in Developer.objects.all():
        passports.append(d.user.username)

    for name in passports:
        uid = g_webdb_client.get_uid_by_passport(name, 2)
        try:
            int(uid)
        except:
            print "name", name, "uid", uid
            continue
        UidName.objects.create(uid=uid, passport=name)
#------------------------------------------- 


#error
#40543573
#307773201
#575982752
#376482063
#4502277
#76267641
#732074954
#355585868
#502184547
#303579475
#4352859
#dnfkk5025706822
#568148222
#138088214
#314267807
#745548400
#19862952
#3300784
#305558926
#320059
#553142964
#112014423
#373046429
#657493896
#443626705
#key_garmin
#380602139
#aldebaranzx
#
#error
#


def switch2NewDeveloper():
    for d in Developer.objects.all():
        try:
            uid = UidName.objects.get(passport=d.user.username).uid
        except:
            print d.user.username
            continue
        Developer2.objects.create(\
            uid             =       uid,
            dev_type        =       d.dev_type,
            com_name        =       d.com_name,
            nick_name       =       d.nick_name,
            real_name       =       d.real_name,
            phone           =       d.phone,
            email           =       d.email,
            id_card         =       d.id_card,
            address         =       d.address,
            yy_num          =       d.yy_num,
            dev_url         =       d.dev_url,
            licence_img     =       d.licence_img,
            authorization   =       d.authorization,
            reg_time        =       d.reg_time
        )


def switch2AppDevInfo():
    bis = AppBasicInfo.objects.all()
    
    for bi in bis:
        name = bi.developer.user.username
        try:
            uid = UidName.objects.get(passport=name).uid
        except:
            print name, bi.app_id
            continue
            
        pi = bi.apppublishinfo
        
        show_pics_json = []
        for i in range(1, 6):
            show_pics_json.append(eval("pi.show_pic%d" % i).name)
        show_pics_json = json.dumps(show_pics_json)

        AppDevInfo2.objects.create(\
                appid           =       bi.app_id,
                developer       =       uid,
                dev_yy_channel  =       bi.dev_yy_channel,
                doc             =       bi.doc,
                test_time       =       pi.test_time,
                show_pics       =       show_pics_json,
                change_log      =       pi.change_log,
                status          =       pi.status,
                check_ret       =       pi.check_ret,
                check_status    =       pi.check_status,
                #frequency              ???
        )

#
#| am_appid          | int(11)      | NO   | PRI | NULL    |       |
#| passwd            | varchar(192) | NO   |     | NULL    |       |
#| am_appname        | varchar(384) | NO   |     | NULL    |       |
#| app_filename      | varchar(384) | NO   |     | NULL    |       |
#| am_description    | varchar(768) | NO   |     | NULL    |       |
#| am_recommend_ver  | int(11)      | NO   |     | NULL    |       |
#| delayflag         | int(11)      | NO   |     | NULL    |       |
#| istest            | int(11)      | NO   |     | NULL    |       |
#| issubsidapp       | int(11)      | NO   |     | NULL    |       |
#| app_pos_type      | int(11)      | NO   |     | NULL    |       |
#| app_binary_type   | int(11)      | NO   |     | NULL    |       |
#| app_attrib        | int(11)      | NO   |     | NULL    |       |
#| app_data_dis_type | int(11)      | NO   |     | NULL    |       |
#| add_time          | datetime     | NO   |     | NULL    |       |
#| last_modify_time  | datetime     | NO   |     | NULL    |       |
#| need_yy_lbs       | int(11)      | NO   |     | NULL    |       |
#| expand            | longtext     | NO   |     | NULL    |       |
#+-------------------+--------------+------+-----+---------+-------+



def switch2AppInfo():
    bis = AppBasicInfo.objects.all()

    for bi in bis:
        pi = bi.apppublishinfo

        jn = {}
        jn["iconPath"]  = DOMAIN 
        jn["useCloud"]  = int(bi.clound_saving)
        jn["iconSName"] = bi.icon.name
        jn["iconBName"] = pi.logo.name
        jn["partVApp"]  = "1"

        AppBasicInfo2.objects.create(\
            am_appid        =       bi.app_id,
            passwd          =       "356a192b7913b04c54574d18c28d46e6395428ab",
            am_appname      =       bi.name,
            app_filename    =       bi.file_name,
            am_description  =       bi.desc,
            am_recommend_ver=       pi.version,
            delayflag       =       1,
            istest          =       1,
            issubsidapp     =       0,
            app_pos_type    =       0,
            app_binary_type =       bi.bin_type,
            app_attrib      =       bi.app_type,
            app_data_dis_type=      0,
            add_time        =       bi.create_time,
            last_modify_time=       bi.create_time,
            need_yy_lbs     =       0,
            expand          =       json.dumps(jn),
        )

switch2AppInfo()
#
#    |  m_appid  | int(11)      | NO   | PRI | NULL    |       |
#    | am_appver | int(11)      | NO   | PRI | NULL    |       |
#    | am_appurl | varchar(256) | NO   |     | NULL    |       |
#    | am_appmd5 | varchar(32)  | NO   |     | NULL    |       |
#    | am_exemd5 | varchar(32)  | NO   |     | NULL    |       |
#    | am_vmax   | int(11)      | NO   |     | NULL    |       |
#    | am_vmin   | int(11)      | NO   |     | NULL    |       |
#    | expand    | text         | YES  |     | NULL    |       |
#
def switch2AppVersions():
    #from op.helper import *
    pis = AppPublishInfo.objects.filter(status__gt=1)

    for pi in pis:
        bi = pi.app_basic_info
        Appidmutilversion2.objects.create(\
            am_appid        =       bi.app_id,
            am_appver       =       pi.test_version,
            am_appurl       =       DOMAIN + pi.test_exe_file.name if pi.test_exe_file.name else "",
                                    #pi.GetMd5ByFile(pi.test_exe_file),
            am_appmd5       =       "md5",
            am_exemd5       =       "",
            am_vmax         =       85536,
            am_vmin         =       65536,
            expand          =       "",
    )


#switch2AppVersions()
