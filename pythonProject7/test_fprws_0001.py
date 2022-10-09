import os
import re
from base_api import BaseApi, Sftp
import datetime
import time
import random

def test_fprws_0001():
    #检查fprws及redis状态
    host = BaseApi.read_y("fprws", "host")
    port = BaseApi.read_y("fprws", "port")
    user = BaseApi.read_y("fprws", "user")
    password = BaseApi.read_y("fprws", "password")
    fprws = BaseApi(host, port, user, password)
    channel = fprws.transport_connect()[1]
    time.sleep(1)
    ret1 = fprws.send('ps -ef|grep redis',channel)
    ret2 = fprws.send('ps -ef|grep fprws',channel)
    result1 = re.findall(r'redis\S*server',ret1)
    result2 = re.findall(r'fprws\S*jar',ret2)
    if not result1:
        fprws.send('cd /home/aisddi/redis6379/redis',channel)
        fprws.send('./redis.sh start', channel)
    if not result2:
        fprws.send('cd /home/aisddi/fprws',channel)
        fprws.send('''nohup java -jar fprws.jar --spring.config.location=/home/aisddi/fprws/application.yml,/home/aisddi/fprws/application-druid.yml --server.port=8080 > nohup1.out 2>&1 &''', channel)
        time.sleep(10)
    fprws.transport_disconnect()

    index = str(random.randint(1000, 9999))
    local_filename = '''YMCZ_210_''' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '_' + index + '.log'
    path_local = '''D:/YMCZ_210_''' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '_' + index + '.log'
    host_access = BaseApi.read_y("access_log", "host")
    fp = open(path_local, 'w')
    for i in range(1, 10):
        print('''{"disposeTime":0,"expireTime":"2099-12-31 23:59:59","issueTime":"''' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '''","serverIp":"''' + host_access + '''","operationType":1,"contentType":1,"content":"wangkang''' + str(i) + '''.test50m.com"}''', file=fp)
    fp.close()
    time.sleep(2)
    host1 = BaseApi.read_y("order_log", "host")
    port1 = BaseApi.read_y("order_log", "port")
    user1 = BaseApi.read_y("order_log", "user")
    password1 = BaseApi.read_y("order_log", "password")
    path = BaseApi.read_y("order_log", "path")
    remotedirtmp = os.path.join(path, local_filename)
    localdirtmp = os.path.join('D:/', local_filename)
    order = Sftp(host1, port1, user1, password1)
    order.sftp_put(localdirtmp,remotedirtmp)