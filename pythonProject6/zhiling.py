import datetime
import time
import random
path = '''D:/YMCZ_210_''' + time.strftime('%Y-%m-%d',time.localtime(time.time())) + '_' + str(random.randint(1000, 9999)) + '.log'
fp = open(path,'w')
for i in range(1,10):
    print('''{"disposeTime":0,"expireTime":"2099-12-31 23:59:59","issueTime":"''' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '''","serverIp":"10.21.41.76","operationType":1,"contentType":1,"content":"wangkang'''+str(i)+'''.test50m.com"}''',file=fp)
fp.close()



