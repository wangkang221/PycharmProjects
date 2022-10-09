import re
transPattern = re.compile("type=([0-9]+)")
receivedPattern = re.compile("([0-9]+)\\s+packet\\(s\\)\\s+received")
lossPattern = re.compile("([0-9]+\\.[0-9]+)\\%\\s+packet\\s+loss")
rttPattern = re.compile("(min.*?ms)")
strs = '''[dnsId=2017081799952033032, type=93, cmdUuid=20220930134958, resultCode=2, msgInfo=指令执行状态：7]'''

strs1 = '''BJ-BJ-HCYYT-DSW-1.MAN.S4608#ping 106.120.252.110
 Pinging 106.120.252.110 with 64 bytes of data:
 Reply from 106.120.252.110: bytes=64 time=0ms TTL=64 icmp_seq=1
 Reply from 106.120.252.110: bytes=64 time=0ms TTL=64 icmp_seq=2
 Reply from 106.120.252.110: bytes=64 time=0ms TTL=64 icmp_seq=3
 Reply from 106.120.252.110: bytes=64 time=0ms TTL=64 icmp_seq=4
 Reply from 106.120.252.110: bytes=64 time=0ms TTL=64 icmp_seq=5

Ping statistics for 106.120.252.110 : 
       Packets:Send = 5,  Received = 5 , Lost = 0 (0% loss), 
Approximate round trip times in milli-seconds: 
       Minimum = 0ms,  Maximum = 0ms , Average = 0ms'''


result1 = transPattern.findall(strs)
result2 = receivedPattern.findall(strs)
result3 = lossPattern.findall(strs)
result4 = rttPattern.findall(strs)

print(result1)
print(result2)
print(result3)
print(result4)
