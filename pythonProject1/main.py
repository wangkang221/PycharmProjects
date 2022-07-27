import re
transPattern = re.compile("([0-9]+)\\s+packet\\(s\\)\\s+transmitted")
receivedPattern = re.compile("([0-9]+)\\s+packet\\(s\\)\\s+received")
lossPattern = re.compile("([0-9]+\\.[0-9]+)\\%\\s+packet\\s+loss")
rttPattern = re.compile("(min.*?ms)")
strs = '''[~HUAWEI]ping ipv6 vpn-instance b 2000::1
  PING 2000::1 : 56  data bytes, press CTRL_C to break
    Reply from 2000::1
    bytes=56 Sequence=1 hop limit=64 time=7 ms
    Reply from 2000::1
    bytes=56 Sequence=2 hop limit=64 time=5 ms
    Reply from 2000::1
    bytes=56 Sequence=3 hop limit=64 time=6 ms
    Reply from 2000::1
    bytes=56 Sequence=4 hop limit=64 time=6 ms
    Reply from 2000::1
    bytes=56 Sequence=5 hop limit=64 time=5 ms

  --- 2000::1 ping statistics---
    5 packet(s) transmitted
    5 packet(s) received
    0.00% packet loss
    round-trip min/avg/max=5/5/7 ms

[~HUAWEI]'''

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
