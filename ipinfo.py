__author__ = 'Network ZIGI - Ko Jae Sung' 
 
# 2014.07.19. First Version 
#Example Result)
#NX-OS# python ipinfo.py 10.10.10.11
# ================================================ 
#      IP Info : NetworkZIGI   2014.07.19 
#================================================ 
#IP-Address      : 10.0.0.1 
#Mac-Address     : 0012.3456.abcd 
#Vlan            : 11 
#Interface       : Eth14/2 
#Description     : NetworkZIGI Blog Server 
 
# Blog : http://ThePlmingspace.tistory.com 
# 
# Tested : Cisco Nexus 5548  : 6.0(2)N2(4) 
 
import argparse 
import sys 
import cisco 
 
IP = 'IP-Address' 
MAC = 'Mac-Address' 
Vlan = 'Vlan' 
Int = 'Interface' 
Desc = 'Description' 
 
IP_info = {IP:'None', MAC:'None', Vlan:'None', Int:'None', Desc:'None'}   
 
def get_ARP_Table(ipaddr): 
    arpCmd = 'sh ip arp ' + ipaddr 
    arpCmdResult = CLI(arpCmd, False) 
    arpCmdResultList = arpCmdResult.get_output() 
    for arp in arpCmdResultList: 
        if (-1<arp.find(args.ip)): 
            return arp 
    else: 
        print ' %s : Not found IP Address Infomation' % args.ip 
        sys.exit() 
 
def get_IP_MAC_info(info): 
    info_list = info.split() 
    IP_info[IP] = info_list[0] 
    IP_info[MAC] = info_list[2] 
    IP_info[Vlan] = info_list[3][4:] 
 
  
def get_Interface_info(): 
    macCmd = 'sh mac address-table addr ' + IP_info[MAC] 
    macCmdResult = CLI(macCmd, False) 
    macCmdResultList = macCmdResult.get_output() 
    if (len(macCmdResultList) > 6):                                                 
        IP_info[Int] = macCmdResultList[5][58:] 
        get_Description_info(IP_info[Int]) 
 
def get_Description_info(iInfo): 
    if(iInfo.find('Eth') == 0 or iInfo.find('Po')==0):  
        intCmd = 'sh int desc | inc ' + iInfo 
        intCmdResult = CLI(intCmd, False) 
        intCmdResultList = intCmdResult.get_output() 
        IP_info[Desc] = intCmdResultList[0][25:] 
 
  
def show_IP_info(): 
    print '================================================' 
    print '             IP Info : NetworkZIGI              ' 
    print '================================================' 
    print '%-15s : %s' % (IP,IP_info[IP]) 
    print '%-15s : %s' % (MAC,IP_info[MAC]) 
    print '%-15s : %s' % (Vlan, IP_info[Vlan]) 
    print '%-15s : %s' % (Int, IP_info[Int]) 
    print '%-15s : %s' % (Desc,IP_info[Desc]) 
 
 
parser = argparse.ArgumentParser('Args',description='Args Desc') 
parser.add_argument('ip') 
args = parser.parse_args() 
 
iparp = get_ARP_Table(args.ip) 
get_IP_MAC_info(iparp) 
get_Interface_info() 
show_IP_info() 
