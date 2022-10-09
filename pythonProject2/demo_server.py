#!/usr/bin/env python

# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA.

import base64
from binascii import hexlify
import os
import socket
import sys
import threading
import traceback
import time
import paramiko
from paramiko.py3compat import b, u, decodebytes
# now connect

# setup logging
paramiko.util.log_to_file("demo_server.log")

host_key = paramiko.RSAKey(filename="test_rsa.key")
# host_key = paramiko.DSSKey(filename='test_dss.key')

print("Read key: " + u(hexlify(host_key.get_fingerprint())))

class Server(paramiko.ServerInterface):
    # 'data' is the output of base64.b64encode(key)
    # (using the "user_rsa_key" files)
    data = (
        b"AAAAB3NzaC1yc2EAAAABIwAAAIEAyO4it3fHlmGZWJaGrfeHOVY7RWO3P9M7hp"
        b"fAu7jJ2d7eothvfeuoRFtJwhUmZDluRdFyhFY/hFAh76PJKGAusIqIQKlkJxMC"
        b"KDqIexkgHAfID/6mqvmnSJf0b5W8v5h2pI/stOSwTQ+pxVhwJ9ctYDhRSlF0iT"
        b"UWT10hcuO4Ks8="
    )
    good_pub_key = paramiko.RSAKey(data=decodebytes(data))

    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == "huawei") and (password == "Root@123"):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        print("Auth attempt with key: " + u(hexlify(key.get_fingerprint())))
        if (username == "huawei") and (key == self.good_pub_key):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_gssapi_with_mic(
            self, username, gss_authenticated=paramiko.AUTH_FAILED, cc_file=None
    ):
        """
        .. note::
            We are just checking in `AuthHandler` that the given user is a
            valid krb5 principal! We don't check if the krb5 principal is
            allowed to log in on the server, because there is no way to do that
            in python. So if you develop your own SSH server with paramiko for
            a certain platform like Linux, you should call ``krb5_kuserok()`` in
            your local kerberos library to make sure that the krb5_principal
            has an account on the server and is allowed to log in as a user.

        .. seealso::
            `krb5_kuserok() man page
            <http://www.unix.com/man-page/all/3/krb5_kuserok/>`_
        """
        if gss_authenticated == paramiko.AUTH_SUCCESSFUL:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_gssapi_keyex(
            self, username, gss_authenticated=paramiko.AUTH_FAILED, cc_file=None
    ):
        if gss_authenticated == paramiko.AUTH_SUCCESSFUL:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def enable_auth_gssapi(self):
        return True

    def get_allowed_auths(self, username):
        return "gssapi-keyex,gssapi-with-mic,password,publickey"

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(
            self, channel, term, width, height, pixelwidth, pixelheight, modes
    ):
        return True

DoGSSAPIKeyExchange = True

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("10.21.178.243", 2200))
except Exception as e:
    print("*** Bind failed: " + str(e))
    traceback.print_exc()
    sys.exit(1)
try:
    sock.listen(100)
    print("Listening for connection ...")
except Exception as e:
    print("*** Listen failed: " + str(e))
    traceback.print_exc()
    sys.exit(1)

def deal(sock,addr):
     try:
         t = paramiko.Transport(client, gss_kex=DoGSSAPIKeyExchange)
         t.set_gss_host(socket.getfqdn(""))
         try:
             t.load_server_moduli()
         except:
             print("(Failed to load moduli -- gex will be unsupported.)")
             raise
         t.add_server_key(host_key)
         server = Server()
         try:
             t.start_server(server=server)
         except paramiko.SSHException:
             print("*** SSH negotiation failed.")
             sys.exit(1)
         # wait for auth
         chan = t.accept(20)
         if chan is None:
             print("*** No channel.")
             sys.exit(1)
         print("Authenticated!")

         server.event.wait(10)
         if not server.event.is_set():
             print("*** Client never asked for a shell.")
             sys.exit(1)

         chan.send("\r\n\r\nWelcome to the device echo simulator!\r\n\r\n")
         chan.send("Source code: paramiko\r\n")
         chan.send("Adaptation: wangkang\r\n\r\n")
         version = """Huawei Versatile Routing Platform Software\r\nVRP (R) software, Version 8.210 (CX600 V800R011C00SPCc00)\r\nCopyright (C) 2012-2021 Huawei Technologies Co., Ltd.\r\nHUAWEI CX600-X8A uptime is 90 days, 9 hours, 14 minutes \r\nPatch Version: V800R011SPH087\r\n\r\nCX600-X8A version information:\r\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\r\nBKP  version information:\r\nPCB         Version : CR57BKP08F REV A\r\nMPU  Slot  Quantity : 0\r\nSRU  Slot  Quantity : 2\r\nSFU  Slot  Quantity : 2\r\nLPU  Slot  Quantity : 8\r\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \r\nMPU version information:\r\n\r\nMPU (Master) 9 : uptime is 90 days, 9 hours, 13 minutes\r\nStartupTime 2022/03/31   00:45:34\r\nSDRAM Memory Size   : 16384 M bytes\r\nFLASH Memory Size   : 16 M bytes\r\nNVRAM Memory Size   : 512 K bytes\r\nCFCARD Memory Size  : 7681 M bytes\r\nMPU CX6D0SRUAG12 version information\r\nPCB         Version : CR56RPUC REV D\r\nEPLD        Version : 103\r\nFRA version information\r\nPCB         Version : CR57FRA480B REV A\r\nFPGA        Version : 008\r\nBootROM     Version : 06.15\r\nBootLoad    Version : 06.15\r\nMonitorBUS version information:\r\nSoftware    Version : 38.8\r\n\r\nMPU (Slave) 10 : uptime is 90 days, 9 hours, 12 minutes\r\nStartupTime 2022/03/31   00:46:41\r\nSDRAM Memory Size   : 16384 M bytes\r\nFLASH Memory Size   : 16 M bytes\r\nNVRAM Memory Size   : 512 K bytes\r\nCFCARD Memory Size  : 7681 M bytes\r\nMPU CX6D0SRUAG12 version information\r\nPCB         Version : CR56RPUC REV D\r\nEPLD        Version : 103\r\nFRA version information\r\nPCB         Version : CR57FRA480B REV A\r\nFPGA        Version : 008\r\nBootROM     Version : 06.15\r\nBootLoad    Version : 06.15\r\nMonitorBUS version information:\r\nSoftware    Version : 38.8\r\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \r\nLPU/SPU version information:\r\n\r\nLPU 1 : uptime is 90 days, 9 hours, 10 minutes\r\nStartupTime 2022/03/31   00:48:10\r\nHost processor :\r\nSDRAM Memory Size   : 16384 M bytes\r\nFlash Memory Size   : 128 M bytes\r\nLPU CX6DISUFM310 version information:\r\nPCB Version         : CR57LPUF480K REV D\r\nEPLD Version        : 107\r\nFPGA1 Version       : 101\r\nFPGA2 Version       : 101\r\nNP Version          : 100\r\nTM Version          : 100\r\nBootROM Version     : 08.15\r\nNSE version information:\r\nPCB Version         : NSE REV A\r\nPIC0:CX6DE2NBFM10 version information\r\nStartupTime         : 2022/03/31    00:48:31\r\nPCB Version         : CR57E4VBC REV A\r\nFPGA Version        : 112\r\nFPGA2 Version       : 135\r\nCHIP Version        : 100\r\nBOM Version         : 003\r\nMonitorBUS version information:\r\nSoftware Version : 40.21\r\nConfigure license items:\r\nNULL\r\n\r\nLPU 2 : uptime is 90 days, 9 hours, 10 minutes\r\nStartupTime 2022/03/31   00:48:10\r\nHost processor :\r\nSDRAM Memory Size   : 16384 M bytes\r\nFlash Memory Size   : 128 M bytes\r\nLPU CX6DISUFM310 version information:\r\nPCB Version         : CR57LPUF480K REV D\r\nEPLD Version        : 107\r\nFPGA1 Version       : 101\r\nFPGA2 Version       : 101\r\nNP Version          : 100\r\nTM Version          : 100\r\nBootROM Version     : 08.15\r\nNSE version information:\r\nPCB Version         : NSE REV A\r\nPIC0:CX6DE2NBFM10 version information\r\nStartupTime         : 2022/03/31    00:48:31\r\nPCB Version         : CR57E4VBC REV A\r\nFPGA Version        : 112\r\nFPGA2 Version       : 135\r\nCHIP Version        : 100\r\nBOM Version         : 003\r\nMonitorBUS version information:\r\nSoftware Version : 40.21\r\nConfigure license items:\r\nNULL\r\n\r\nLPU 3 : uptime is 90 days, 9 hours, 11 minutes\r\nStartupTime 2022/03/31   00:48:07\r\nHost processor :\r\nSDRAM Memory Size   : 16384 M bytes\r\nFlash Memory Size   : 128 M bytes\r\nLPU CX6DISUFM310 version information:\r\nPCB Version         : CR57LPUF480K REV D\r\nEPLD Version        : 107\r\nFPGA1 Version       : 101\r\nFPGA2 Version       : 101\r\nNP Version          : 100\r\nTM Version          : 100\r\nBootROM Version     : 08.15\r\nNSE version information:\r\nPCB Version         : NSE REV A\r\nPIC0:CX6D0LFXFM10 version information\r\nStartupTime         : 2022/03/31    00:48:44\r\nPCB Version         : CR57LFXFJ REV A\r\nFPGA Version        : 101\r\nCHIP Version        : 100\r\nCHIP2 Version       : 100\r\nBOM Version         : 003\r\nMonitorBUS version information:\r\nSoftware Version : 40.21\r\nConfigure license items:\r\nNULL\r\n\r\nLPU 4 : uptime is 90 days, 9 hours, 11 minutes\r\nStartupTime 2022/03/31   00:47:56\r\nHost processor :\r\nSDRAM Memory Size   : 16384 M bytes\r\nFlash Memory Size   : 128 M bytes\r\nLPU CX6DISUFM310 version information:\r\nPCB Version         : CR57LPUF480K REV D\r\nEPLD Version        : 107\r\nFPGA1 Version       : 101\r\nFPGA2 Version       : 101\r\nNP Version          : 100\r\nTM Version          : 100\r\nBootROM Version     : 08.15\r\nNSE version information:\r\nPCB Version         : NSE REV A\r\nPIC0:CX6D0LFXFM10 version information\r\nStartupTime         : 2022/03/31    00:48:34\r\nPCB Version         : CR57LFXFJ REV A\r\nFPGA Version        : 101\r\nCHIP Version        : 100\r\nCHIP2 Version       : 100\r\nBOM Version         : 003\r\nMonitorBUS version information:\r\nSoftware Version : 40.21\r\nConfigure license items:\r\nNULL\r\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \r\nSFU version information:\r\n\r\nSFU 11 : uptime is 79 days, 6 hours, 19 minutes\r\nStartupTime 2022/04/11   03:38:33\r\nSDRAM Memory Size   : 1024 M bytes\r\nFlash Memory Size   : 64 M bytes\r\nSFU CX6DSFUIT21F version information:\r\nPCB         Version : CR57SFU480D REV A\r\nEPLD        Version : 100\r\nBootROM     Version : 03.49\r\nMonitorBUS version information:\r\nSoftware Version : 40.21\r\n\r\nSFU 12 : uptime is 90 days, 9 hours, 11 minutes\r\nStartupTime 2022/03/31   00:47:42\r\nSDRAM Memory Size   : 1024 M bytes\r\nFlash Memory Size   : 64 M bytes\r\nSFU CX6DSFUIT21F version information:\r\nPCB         Version : CR57SFU480D REV A\r\nEPLD        Version : 100\r\nBootROM     Version : 03.49\r\nMonitorBUS version information:\r\nSoftware Version : 40.21\r\n\r\nSFU 13 : uptime is 90 days, 9 hours, 11 minutes\r\nStartupTime 2022/03/31   00:47:27\r\nSDRAM Memory Size   : 1024 M bytes\r\nFlash Memory Size   : 64 M bytes\r\nSFU CX6D0SRUAG12 version information:\r\nPCB         Version : CR57FRA480B REV A\r\nEPLD        Version : 100\r\nBootROM     Version : 03.49\r\nMonitorBUS version information:\r\nSoftware Version : 38.8\r\n\r\nSFU 14 : uptime is 90 days, 9 hours, 11 minutes\r\nStartupTime 2022/03/31   00:47:45\r\nSDRAM Memory Size   : 1024 M bytes\r\nFlash Memory Size   : 64 M bytes\r\nSFU CX6D0SRUAG12 version information:\r\nPCB         Version : CR57FRA480B REV A\r\nEPLD        Version : 100\r\nBootROM     Version : 03.49\r\nMonitorBUS version information:\r\nSoftware Version : 38.8\r\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \r\nCLK version information:\r\n\r\nCLK 15 : uptime is 90 days, 9 hours, 13 minutes\r\nStartupTime 2022/03/31   00:45:44\r\nFPGA     Version : 003\r\nDSP      Version : 10205017\r\n\r\nCLK 16 : uptime is 90 days, 9 hours, 12 minutes\r\nStartupTime 2022/03/31   00:46:54\r\nFPGA     Version : 003\r\nDSP      Version : 10205017\r\n\r\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \r\nPower version information: \r\n\r\nPOWER 17 MonitorBUS version information:\r\nPM 1 version information:\r\nPCB      Version : PAH-3000WA REV A\r\nSoftware Version : 1.37\r\nPM 2 version information:\r\nPCB      Version : PAH-3000WA REV A\r\nSoftware Version : 1.37\r\nPM 3 version information:\r\nPCB      Version : PAH-3000WA REV A\r\nSoftware Version : 1.37\r\nPM 4 version information:\r\nPCB      Version : PAH-3000WA REV A\r\nSoftware Version : 1.37\r\n\r\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \r\nFAN version information: \r\n\r\nFAN 19 MonitorBUS version information:\r\nPCB      Version : CR56FCBJ REV D\r\nSoftware Version : 5.12\r\n\r\nFAN 20 MonitorBUS version information:\r\nPCB      Version : CR56FCBJ REV D\r\nSoftware Version : 5.12\r\n\r\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \r\nPMU version information: \r\n\r\nPMU 22 MonitorBUS version information:\r\nPCB      Version : CR56PMUB REV C\r\nSoftware Version : 31.3\r\n\r\nPMU 23 MonitorBUS version information:\r\nPCB      Version : CR56PMUB REV C\r\nSoftware Version : 31.3"""
         # device = """CX600-X8A's Device status:\r\n-------------------------------------------------------------------------------\r\nSlot #   Type    Online     Register     Status     Role   LsId   Primary      \r\n-------------------------------------------------------------------------------\r\n1        LPU     Present    Registered   Normal     LC     0      NA           \r\n2        LPU     Present    Registered   Normal     LC     0      NA           \r\n3        LPU     Present    Registered   Normal     LC     0      NA           \r\n4        LPU     Present    Registered   Normal     LC     0      NA           \r\n9        MPU     Present    Registered   Normal     MMB    0      Master       \r\n10       MPU     Present    Registered   Normal     MMB    0      Slave        \r\n11       SFU     Present    Registered   Normal     OTHER  0      NA           \r\n12       SFU     Present    Registered   Normal     OTHER  0      NA           \r\n13       SFU     Present    Registered   Normal     OTHER  0      NA           \r\n14       SFU     Present    Registered   Normal     OTHER  0      NA           \r\n15       CLK     Present    Registered   Normal     OTHER  0      Master       \r\n16       CLK     Present    Registered   Normal     OTHER  0      Slave        \r\n17       PWR     Present    Registered   Normal     OTHER  0      NA           \r\n19       FAN     Present    Registered   Normal     OTHER  0      NA           \r\n20       FAN     Present    Registered   Normal     OTHER  0      NA           \r\n22       PMU     Present    Registered   Normal     OTHER  0      Slave        \r\n23       PMU     Present    Registered   Normal     OTHER  0      Master       \r\n-------------------------------------------------------------------------------"""
         # device_pic = """Pic-status information :\r\n--------------------------------------------------------------------------------\r\nPic#    Status       Type                      Port_count Init_result Logic_down\r\n--------------------------------------------------------------------------------\r\n1/0     Registered   ETH_4x50GB_CARD           4          SUCCESS     SUCCESS   \r\n2/0     Registered   ETH_4x50GB_CARD           4          SUCCESS     SUCCESS   \r\n3/0     Registered   LAN_WAN_24x10GF_CARD      24         SUCCESS     SUCCESS   \r\n4/0     Registered   LAN_WAN_24x10GF_CARD      24         SUCCESS     SUCCESS   \r\n--------------------------------------------------------------------------------"""

         device = """CX600-X8A's Device status:\r\n-------------------------------------------------------------------------------\r\nSlot #   Type    Online     Register     Status     Role   LsId   Primary      \r\n-------------------------------------------------------------------------------\r\n1        LPU     Present    Registered   Normal     LC     0      NA           \r\n2        LPU     Present    Registered   Null       LC     0      NA           \r\n3        LPU     Present    Registered   Forbidden  LC     0      NA           \r\n4        LPU     Present    Registered   Autofind   LC     0      NA           \r\n9        MPU     Present    Registered   Config     MMB    0      Master       \r\n10       MPU     Present    Registered   Offline    MMB    0      Slave        \r\n11       SFU     Present    Registered   Abnormal   OTHER  0      NA           \r\n12       SFU     Present    Registered   Versionerr  OTHER  0      NA           \r\n13       SFU     Present    Registered   Autoload    OTHER  0      NA           \r\n14       SFU     Present    Registered   Outofservice  OTHER  0      NA           \r\n15       CLK     Present    Registered   Graceful   OTHER  0      Master       \r\n16       CLK     Present    Registered   Shutdown   OTHER  0      Slave        \r\n17       PWR     Present    Registered   Energysavingshutdown     OTHER  0      NA           \r\n19       FAN     Present    Registered   Hightempshutdown   OTHER  0      NA           \r\n20       FAN     Present    Registered   Manualshutdown   OTHER  0      NA           \r\n22       PMU     Present    Registered   Mismatch     OTHER  0      Slave        \r\n23       PMU     Present    Registered   Acoffshutdown     OTHER  0      Master       \r\n-------------------------------------------------------------------------------"""
         device_pic = """Pic-status information :\r\n--------------------------------------------------------------------------------\r\nPic#    Status       Type                      Port_count Init_result Logic_down\r\n--------------------------------------------------------------------------------\r\n1/0     Registered   ETH_4x50GB_CARD           4          SUCCESS     SUCCESS   \r\n2/0     Registered   ETH_4x50GB_CARD           4          SUCCESS     SUCCESS   \r\n3/0     Unregistered   LAN_WAN_24x10GF_CARD      24         SUCCESS     SUCCESS   \r\n4/0     Unregistered   LAN_WAN_24x10GF_CARD      24         SUCCESS     SUCCESS   \r\n4/1     Unregistered   LAN_WAN_24x10GF_CARD      24         SUCCESS     SUCCESS   \r\n--------------------------------------------------------------------------------"""

         ip_routing_tablie = """Route Flags: R - relay, D - download to fib, T - to vpn-instance, B - black hole route\r\n------------------------------------------------------------------------------\r\nRouting Table : _public_\r\nSummary Count : 2\r\n\r\nDestination/Mask    Proto   Pre  Cost        Flags NextHop         Interface\r\n\r\n0.0.0.0/0   EBGP    10   0             RD  202.97.31.104   100GE1/2/1/0\r\n           EBGP    10   0             RD  202.97.31.104   100GE1/9/1/0\r\n           EBGP    10   0             RD  202.97.31.105   100GE1/10/0/0\r\n           EBGP    10   0             RD  202.97.31.105   100GE1/3/1/0\r\n"""
         bgp_routing_tablie = """BGP local router ID : 219.141.128.144\r\nLocal AS number : 4847\r\nPaths:   4 available, 1 best, 2 select, 0 best-external, 0 add-path\r\nBGP routing table entry information of 136.32.0.0/11:\r\nFrom: 202.97.31.104 (202.97.31.104)  \r\nRoute Duration: 223d04h06m51s\r\nDirect Out-interface: 100GE1/0/0\r\nOriginal nexthop: 202.97.31.104\r\nQos information : 0x0            \r\nCommunity: <4134:9>\r\nAS-path 4134 6453 16591, origin igp, MED 95000, pref-val 0, valid, external, best, select, pre 10\r\nAdvertised to such 16 peers:\r\n219.141.128.8\r\n219.141.128.37\r\n202.97.31.105\r\n115.169.96.190\r\n115.169.97.191\r\n115.168.32.161\r\n115.168.32.162\r\n211.156.196.254\r\n106.39.147.70\r\n106.38.13.70\r\n218.30.25.40\r\n220.181.0.243\r\n219.141.149.179\r\n219.142.13.142\r\n36.112.213.88\r\n\r\nBGP routing table entry information of 136.32.0.0/11:\r\nFrom: 202.97.31.105 (202.97.31.105)  \r\nRoute Duration: 110d03h59m35s\r\nDirect Out-interface: 100GE2/0/0\r\nOriginal nexthop: 202.97.31.105\r\nQos information : 0x0            \r\nCommunity: <4134:9>\r\nAS-path 4134 6453 16591, origin igp, MED 95000, pref-val 0, valid, external, select, pre 10, not preferred for router ID\r\nNot advertised to any peer yet\r\n\r\nBGP routing table entry information of 136.32.0.0/11:\r\nFrom: 219.141.128.37 (219.141.128.37)  \r\nRoute Duration: 196d14h56m03s\r\nRelay IP Nexthop: 36.112.223.46\r\nRelay IP Out-Interface: 100GE10/1/1\r\nOriginal nexthop: 219.141.128.45      \r\nAS-path 4134 6453 16591, origin igp, MED 95000, localpref 100, pref-val 0, valid, internal, pre 200, IGP cost 100, not preferred for peer type\r\nOriginator: 219.141.128.45\r\nCluster list: 219.141.128.37\r\nNot advertised to any peer yet\r\n\r\nBGP routing table entry information of 136.32.0.0/11:\r\nFrom: 219.141.128.8 (219.141.128.8)  \r\nRoute Duration: 224d10h28m25s\r\nRelay IP Nexthop: 36.112.223.41\r\nRelay IP Out-Interface: 100GE11/0/1\r\nOriginal nexthop: 219.141.128.70\r\nQos information : 0x0            \r\nCommunity: <4134:9>\r\nAS-path 4134 6453 16591, origin igp, MED 95000, localpref 100, pref-val 0, valid, internal, pre 200, IGP cost 100, not preferred for router ID\r\nOriginator: 219.141.128.70\r\nCluster list: 219.141.128.8\r\nNot advertised to any peer yet\r\n"""
         ipv6_routing_tablie = """Routing Table : _public_\r\nSummary Count : 1\r\n\r\nDestination  : 240E:604:0:6::34                        PrefixLength : 127\r\nNextHop      : FE80::AE4E:91FF:FE5C:F571               Preference   : 150\r\nCost         : 3000                                    Protocol     : ISIS-L2\r\nRelayNextHop : ::                                      TunnelID     : 0x0\r\nInterface    : GigabitEthernet2/1/10                   Flags        : D\r\n"""
         bgpv6_routing_tablie = """BGP local router ID : 219.141.128.144\r\nLocal AS number : 4847\r\nPaths:   1 available, 1 best, 1 select, 0 best-external, 0 add-path\r\nBGP routing table entry information of 240E:604::/31:\r\nNetwork route.\r\nFrom: :: (0.0.0.0)  \r\nRoute Duration: 977d17h10m28s\r\nDirect Out-interface: NULL0\r\nOriginal nexthop: ::\r\nQos information : 0x0            \r\nAS-path Nil, origin igp, MED 0, pref-val 0, valid, local, best, select, pre 254\r\nAdvertised to such 9 peers:\r\n240E:0:0:EEEE::104\r\n240E:0:0:EEEE::105\r\n240E:28:2000::111\r\n240E:28:2000::211\r\n240E:0:8000:103::23\r\n240E:0:8000::202\r\n240E:0:8000::402\r\n240E:604:0:7::9\r\n240E:204:4::FFFF:FFFF:FFFF:FFF9\r\n"""
         cfg = """cfg test\r\n"""

         while True:
             chan.send("\r\n" + "<HUAWEI>")
             f = chan.makefile("rU")
             re = f.readline().strip("\r\n")
             chan.send(re)
             if "display version" in re:
                 chan.send("\r\n" + version)
             elif "display device" == re:
                 chan.send("\r\n" + device)
             elif "display device pic-status" in re:
                 chan.send("\r\n" + device_pic)
             elif "display ip routing-table" in re:
                 chan.send("\r\n" + ip_routing_tablie)
             elif "display bgp routing-table" in re:
                 chan.send("\r\n" + bgp_routing_tablie)
             elif "display ipv6 routing-table" in re:
                 chan.send("\r\n" + ipv6_routing_tablie)
             elif "display bgp ipv6 routing-table" in re:
                 chan.send("\r\n" + bgpv6_routing_tablie)
             elif "DIS current-configuration" in re:
                 chan.send("\r\n" + cfg)
             elif "exit" == re or "quit" == re:
                 chan.close()

     except Exception as e:
         print("*** Caught exception: " + str(e.__class__) + ": " + str(e))
         try:
             print('用户异常退出')
         except:
             pass

while True:
    client, addr = sock.accept()
    print("Got a connection!")
    xd = threading.Thread(target=deal,args=(client,addr))
    xd.start()

