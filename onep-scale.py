#!/usr/bin/python

# *------------------------------------------------------------------
# * onep-scale.py
# *
# * Simple script to check VLAN scale threshold
# *
# * Cisco ONE-P Python SDK
# *
# * Copyright (c) 2011-2014 by Cisco Systems, Inc.
# * All rights reserved.
# *------------------------------------------------------------------
# *
#
# Must have a Cisco device capable of communicating with ONE-P APIs.
# Network Element must also have onep configured with the socket
# transport and have the correct onep services activated.
# Depending on OnePK SDK release, supported tranport type could be
# TIPC and TLS. Check on device using the following CLIs:
# conf t --> onep --> transport  type ?
#
# A network interface must be configured with a valid IP address and
# pingable.
#
# To use this script you should:
# 1) Copy the file to a server with OpePK SDK
# 2) setup the variables in the section below
# 3) run the script: python onep-scale.py
#

from onep.element.NetworkElement import NetworkElement
from onep.element.SessionConfig import SessionConfig
from onep.interfaces.InterfaceStatistics import InterfaceStatistics
from onep.interfaces.InterfaceFilter import *
from onep.vty.VtyService import VtyService

import string
import re
import sys

#####################################################################
# Variables to be changed
#
# transport- Transport type: either TIPC or TLS
#            check tranport types supported on your image by
#            conf t --> onep --> transport  type ?
# cert     - certificate to be used for authentication in cse of TLS
#            transport
# switchIP - management Switch IP address
# appName  - OnePK application Name
# user     - switch userID
# pswd     - switch password
#
# maxVlans - Max VLAN threshold
#
transport= 'TLS'
cert     = '<path>/cacert.pem'
switchIP1 = "<ip1>"
appName1  = "scale1"
user1     = "<user1>"
pswd1     = "<pswd1>"

switchIP2 = "<ip2>"
appName2  = "scale2"
user2     = "<user2>"
pswd2     = "<pswd1>"

maxVlans  = "2"
#####################################################################

global vty

switches = [[switchIP1,appName1,user1,pswd1],
            [switchIP2,appName2,user2,pswd2]]

scale_limits = {"max_vlans" : maxVlans}

def scaleNotification():

    for switch in switches:
        switchIP = switch[0]
        appName  = switch[1]
        user     = switch[2]
        pswd     = switch[3]

        #
        # Set up session connection configuration and connect to the switch
        #
        ne = NetworkElement(switchIP, appName)
        if  transport == 'TLS':
            session_config = SessionConfig(SessionConfig.SessionTransportMode.TLS)
            session_config.ca_certs = cert
            ne.connect(user, pswd, session_config)
        elif transport == 'TIPC':
            session_config = SessionConfig(SessionConfig.SessionTransportMode.TIPC)
            ne.connect(user, pswd, session_config)
        else:
            print "Please set-up a valid transport type: TIPC or TLS"
            exit(0)

        vty = VtyService(ne)
        vty.open()
        vlan_summary = vty.write("sh vlan summary")
        vty.close()

        vlan_sum = re.search('(?<=vlansum-all-vlan\t)(.*)',vlan_summary)

        if int(vlan_sum.group(0)) > int(scale_limits["max_vlans"]):
            string_print = "Vlan scale exceeded. Max vlan recommended:",scale_limits["max_vlans"],"vlan being used :", vlan_sum.group(0)
            print string_print
            ne.create_syslog_message (ne.OnepSyslogSeverity.ONEP_SYSLOG_CRITICAL,
                                      str(string_print));
        print "Disconnecting from NE: ",switchIP
        ne.disconnect()

if __name__=='__main__':
    scaleNotification()
