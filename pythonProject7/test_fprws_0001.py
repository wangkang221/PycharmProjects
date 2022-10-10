#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import os
import re
from base_api import BaseApi, Sftp
import datetime
import time
import random
print("江苏移动反诈404-指令数据接收")
def test_fprws_0001_prepare():
    print("检查fprws及redis状态")
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
        time.sleep(10)#等待fprws程序启动
    fprws.transport_disconnect()

    print("指令数据构造")
    index = str(random.randint(1000, 9999))
    global local_filename
    local_filename = '''YMCZ_210_''' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '_' + index + '.log'
    path_local = '''D:/YMCZ_210_''' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '_' + index + '.log'
    host_access = BaseApi.read_y("access_log", "host")
    fp = codecs.open(path_local,'w','utf-8')
    #1、指令封堵-重定向serverip非配置内targetIp
    print('''{"disposeTime":0,"expireTime":"2099-12-31 23:59:59","issueTime":"''' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '''","serverIp":"''' + "192.168.1.2" + '''","operationType":1,"contentType":1,"content":"wangkang1.test50m.com"}''',file=fp)
    #2、指令封堵-type=3时IP数据类型开关addressEnabled测试，serverip为targetIp
    print('''{"disposeTime":0,"expireTime":"2099-12-31 23:59:59","issueTime":"''' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '''","serverIp":"''' + host_access + '''","operationType":1,"contentType":3,"content":"192.168.100.100"}''',file=fp)
    #3、指令封堵-type=1时域名数据类型测试，serverip为targetIp
    print('''{"disposeTime":0,"expireTime":"2099-12-31 23:59:59","issueTime":"''' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '''","serverIp":"''' + host_access + '''","operationType":1,"contentType":1,"content":"wangkang3.test50m.com"}''',file=fp)
    #4、指令封堵-type=2时网址数据类型测试，serverip为targetIp
    print('''{"disposeTime":0,"expireTime":"2099-12-31 23:59:59","issueTime":"''' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '''","serverIp":"''' + host_access + '''","operationType":1,"contentType":2,"content":"http://wangkang4.test50m.com/abc"}''',file=fp)
    print('''{"disposeTime":0,"expireTime":"2099-12-31 23:59:59","issueTime":"''' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '''","serverIp":"''' + host_access + '''","operationType":1,"contentType":2,"content":"https://wangkang4.test50m.com/def"}''',file=fp)
    #5、ipv6指令入库及删除测试
    print('''{"disposeTime":0,"expireTime":"2099-12-31 23:59:59","issueTime":"''' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '''","serverIp":"''' + host_access + '''","operationType":1,"contentType":3,"content":"2000::1"}''',file=fp)
    #6、中文域名
    print('''{"disposeTime":0,"expireTime":"2099-12-31 23:59:59","issueTime":"''' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '''","serverIp":"''' + host_access + '''","operationType":1,"contentType":1,"content":"亚信.com"}''',file=fp)
    #7、局点异常网址
    print('''{"disposeTime":0,"expireTime":"2099-12-31 23:59:59","issueTime":"''' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '''","serverIp":"''' + host_access + '''","operationType":1,"contentType":2,"content":"10010002.com/index.php/product/532^10010002.com"}''',file=fp)
    fp.close()
    time.sleep(1)

    print("指令数据放入404目录")
    global host1
    global port1
    global user1
    global password1
    global path
    host1 = BaseApi.read_y("order_log", "host")
    port1 = BaseApi.read_y("order_log", "port")
    user1 = BaseApi.read_y("order_log", "user")
    password1 = BaseApi.read_y("order_log", "password")
    path = BaseApi.read_y("order_log", "path")
    remotedirtmp = os.path.join(path, local_filename)
    localdirtmp = os.path.join('D:/', local_filename)
    order = Sftp(host1, port1, user1, password1)
    order.sftp_put(localdirtmp,remotedirtmp)

    print("登录redis检查数据")
    host = BaseApi.read_y("redis", "host")
    port = BaseApi.read_y("redis", "port")
    user = BaseApi.read_y("redis", "user")
    password = BaseApi.read_y("redis", "password")
    auth =  BaseApi.read_y("redis", "auth")
    path_redis = BaseApi.read_y("redis", "path")
    db = BaseApi.read_y("redis", "db")
    global redis
    global channel_redis
    redis = BaseApi(host, port, user, password)
    channel_redis = redis.transport_connect()[1]
    redis.send('cd '+path_redis+"bin",channel_redis)
    redis.send("./redis-cli -h 127.0.0.1 -p 6379 -a "+auth,channel_redis)
    redis.send("SELECT "+str(db),channel_redis)

def test_fprws_0001_step1():
    print("\n1、指令封堵-重定向serverip非配置内targetIp	指令数据不入redis")
    time.sleep(15)  # 等待fprws处理指令入库
    rs = redis.send("hgetall order:info:wangkang1.test50m.com",channel_redis)
    assert re.findall("empty list or set",rs)

def test_fprws_0001_step2():
    print("\n2、指令封堵-type=3时IP数据类型开关addressEnabled测试，serverip为targetIp	开关为true接收IP类型数据")
    rs = redis.send("hgetall order:info:192.168.100.100",channel_redis)
    assert re.findall(r'''"{\\"content\\":\\"192.168.100.100\\",\\"contentType\\":3''',rs)

def test_fprws_0001_step3():
    print("\n3、指令封堵-type=1时域名数据类型测试，serverip为targetIp	指令数据入redis ")
    rs = redis.send("hgetall order:info:wangkang3.test50m.com",channel_redis)
    assert re.findall(r'''"{\\"content\\":\\"wangkang3.test50m.com\\",\\"contentType\\":1''',rs)

def test_fprws_0001_step4():
    print("\n4、指令封堵-type=2时网址数据类型测试，serverip为targetIp    指令数据入redis")
    rs = redis.send("hgetall order:info:wangkang4.test50m.com",channel_redis)
    assert re.findall(r'''"{\\"content\\":\\"http://wangkang4.test50m.com/abc\\",\\"contentType\\":2''',rs)
    assert re.findall(r'''"{\\"content\\":\\"https://wangkang4.test50m.com/def\\",\\"contentType\\":2''', rs)

def test_fprws_0001_step5():
    print("\n5、ipv6指令入库及删除测试 类型3时ipv6入库及删除正常")
    rs = redis.send("hgetall order:info:42535295865117307932921825928971026433",channel_redis)
    assert not re.findall(r"empty list or set",rs)

def test_fprws_0001_step6():
    print("\n6、中文入库正常")
    rs = redis.send("hgetall order:info:xn--jlqy4a.com",channel_redis)
    assert not re.findall(r"empty list or set",rs)

def test_fprws_0001_step7():
    print("\n7、局点异常网址入库正常")
    rs = redis.send("hgetall order:info:10010002.com",channel_redis)
    assert re.findall(r'''10010002.com/index.php/product/532\^10010002.com''',rs)

def test_fprws_0001_change():
    print("\n修改order_log文件内operationType为0删除redis入库指令")
    global order1
    global channel1
    order1 = BaseApi(host1, port1, user1, password1)
    channel1 = order1.transport_connect()[1]
    order1.send("cd "+path,channel1)
    order1.send(r'''sed -i "s/\"operationType\"\:1/\"operationType\"\:0/g" '''+local_filename,channel1)

def test_fprws_0001_step8():
    time.sleep(15)  # 等待redis库删除数据
    print("\n8、入库指令全部删除")
    rs = redis.send("hgetall order:info:192.168.100.100", channel_redis)
    assert re.findall(r"empty list or set", rs)
    rs = redis.send("hgetall order:info:wangkang3.test50m.com", channel_redis)
    assert re.findall(r"empty list or set", rs)
    rs = redis.send("hgetall order:info:wangkang4.test50m.com", channel_redis)
    assert re.findall(r"empty list or set", rs)
    rs = redis.send("hgetall order:info:42535295865117307932921825928971026433", channel_redis)
    assert re.findall(r"empty list or set", rs)
    rs = redis.send("hgetall order:info:xn--jlqy4a.com", channel_redis)
    assert re.findall(r"empty list or set", rs)
    rs = redis.send("hgetall order:info:10010002.com", channel_redis)
    assert re.findall(r"empty list or set", rs)

def test_fprws_0001_cleanup():
    order1.send("rm -rf "+local_filename,channel1)
    order1.transport_disconnect()
    redis.transport_disconnect()