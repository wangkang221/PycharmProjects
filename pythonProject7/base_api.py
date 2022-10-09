import os
from time import sleep
import paramiko
import yaml
import re

class BaseApi:
    def __init__(self,host,port,user,password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
    def read_y(n,k):
        data = yaml.safe_load(open('./config.yaml', encoding="utf-8"))
        try:
            if n in data.keys():
                return data[n][k]
            else:
                print(f"n：{n}不存在")
        except Exception as e:
            print(f"key值{e}不存在")

    def transport_connect(self):
        self._transport = paramiko.Transport((self.host, self.port))  # 建立一个加密的管道
        self._transport.start_client()
        # 用户名密码方式
        self._transport.auth_password(self.user, self.password)
        # 打开一个通道
        self._channel = self._transport.open_session()
        self._channel.settimeout(7200)
        # 获取一个终端
        self._channel.get_pty()
        # 激活器
        self._channel.invoke_shell()
        return self._transport,self._channel
    #断开连接
    def transport_disconnect(self):
        if self._channel:
            self._channel.close()
        if self._transport:
            self._transport.close()

    def send(self,cmd,channel):
        commod = cmd
        cmd += '\r'
        # 通过命令执行提示符来判断命令是否执行完成
        p = re.compile(r']#')
        result = ''
        # 发送要执行的命令
        channel.send(cmd)
        # 回显很长的命令可能执行较久，通过循环分批次取回回显
        while True:
            sleep(0.2)
            ret = channel.recv(65535)
            try:
                ret = ret.decode('utf-8')
            except:
                ret = ret.decode('gbk')
            result += ret
            print(ret)
            if p.search(ret):
                break
        # print(commod+'结束')
        return result

    #命令执行到一半需要输入信息，输入完成后继续
    def sendMiddle(self,cmd,channel):
        commod = cmd
        cmd += '\r'
        # 通过命令执行提示符来判断命令是否执行完成
        # 发送要执行的命令
        channel.send(cmd)
        # 回显很长的命令可能执行较久，通过循环分批次取回回显
        sleep(0.5)
        ret = channel.recv(65535)
        try:
            ret = ret.decode('utf-8')
        except:
            ret = ret.decode('gbk')
        # printLine(commod + '结束')
        print(ret)
        return ret

# 定义一个类，表示一台远端linux主机
class Sftp(object):
    # 通过IP, 用户名，密码，超时时间初始化一个远程Linux主机
    def __init__(self, ip, port,username, password, timeout=30):
        self.ip = ip
        self.username = username
        self.port = port
        self.password = password
        self.timeout = timeout
        # transport和chanel
        self.t = ''
        self.chan = ''
        # 链接失败的重试次数
        self.try_times = 3

    # 调用该方法连接远程主机
    def connect(self):
         pass

    # 断开连接
    def close(self):
        pass

    # 发送要执行的命令
    def send(self, cmd):
        pass

    # get单个文件
    def sftp_get(self, remotefile, localfile):
        t = paramiko.Transport(sock=(self.ip, self.port))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(remotefile, localfile)
        t.close()

    # put单个文件
    def sftp_put(self, localfile, remotefile):
        t = paramiko.Transport(sock=(self.ip, self.port))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(localfile, remotefile)
        t.close()

