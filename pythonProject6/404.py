import random
import datetime
import time
def random_num1():
    num = random.randint(1, 254)
    return num
def random_num2():
    num = random.randint(0, 255)
    return num
def random_ip():
    ip = str(random_num1()) + '.' + str(random_num2()) + '.' + str(random_num2()) + '.' + str(random_num2())
    return ip
curr_time = datetime.datetime.now()
http = ['http','https']
fp = open('D:/access.log', 'w')
for j in range(1,11):
   for i in range(1,50001):
       print('''{"remoteAddr": "'''+random_ip()+'''","remotePort": "'''+str(random.randint(49152,65535))+'''","requestUrl": "wangkang'''+str(i)+'''.test50m.com","request": "/","requestTime": "2022-09-23T'''+datetime.datetime.strftime(curr_time,'%H:%M:%S')+'''+08:00","requestProtocol": "'''+str(random.sample(http,1)[0])+'''","status": "200","httpReferer": "-","userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36","serverIp": "10.21.41.76"}''',file=fp)
fp.close()