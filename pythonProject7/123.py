import re
ret1 = '''127.0.0.1:6379[6]> hgetall order:info:192.168.100.100
1) "69b737b8-2c83-4651-9dae-c32c049a9184"
2) "{\"content\":\"192.168.100.100\",\"contentType\":3,\"disposeTime\":0,\"expireTime\":\"2099-12-31 23:59:59\",\"issueTime\":\"2022-10-10 14:15:08\",\"operationType\":1,\"serverIp\":\"10.21.41.76\"}"
3) "c5ac9096-1162-4e40-9276-5f8df2bc9b1a"
4) "{\"content\":\"192.168.100.100\",\"contentType\":3,\"disposeTime\":0,\"expireTime\":\"2099-12-31 23:59:59\",\"issueTime\":\"2022-10-10 14:12:49\",\"operationType\":1,\"serverIp\":\"10.21.41.76\"}"
5) "d35d57c5-4cdc-40aa-9f20-1c29cae37d23"
6) "{\"content\":\"192.168.100.100\",\"contentType\":3,\"disposeTime\":0,\"expireTime\":\"2099-12-31 23:59:59\",\"issueTime\":\"2022-10-10 14:06:35\",\"operationType\":1,\"serverIp\":\"10.21.41.76\"}"
127.0.0.1:6379[6]> '''

print(re.findall(r'''"{\"content\":\"192.168.100.100\",\"contentType\":3''',ret1))