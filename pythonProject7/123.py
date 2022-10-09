import re
ret1 = '''


Welcome to 3.10.0-1160.59.1.el7.x86_64

System information as of time: 	2022-10-09 10:37:58

System load: 	0.04
Processes: 	746
Cpu idle: 	99.7%
Memory used: 	14.4%
Swap used: 	0.0%
Usage On: 	24%
IP address: 	10.21.17.20
Users online: 	2


-bash: export: `//修改成实际安装路径': not a valid identifier
-bash: export: `//修改成实际安装路径': not a valid identifier
[root@computer20 ~]# ps -ef|grep redis
root      5887     1  0 Sep21 ?        03:34:48 bin/redis-server 0.0.0.0:6379
root     28787 28727  0 10:37 pts/1    00:00:00 grep --color=auto redis
[root@computer20 ~]#'''

ret2 = '''ps -ef|grep fprws
root     12643     1  1 09:19 ?        00:01:03 java -jar fprws.jar --spring.config.location=/home/aisddi/fprws/application.yml,/home/aisddi/fprws/application-druid.yml --server.port=8080
root     28789 28727  0 10:37 pts/1    00:00:00 grep --color=auto fprws
[root@computer20 ~]# '''

result1 = ret1.find('redis-server')
result2 = re.findall(r'fprws\.jar', ret2)
print(result1)
print(result2)