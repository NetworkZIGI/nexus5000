#! /usr/bin/env python

# *------------------------------------------------------------------
# * onep-intf_properties_cn.py
# *
# * Simple script to check CRC errors on all interfaces and shut down
# * the interfaces with errors greater than a given threshold
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
# 3) run the script: python onep-intf_properties_cn.py
#

from onep.element.NetworkElement import NetworkElement
from onep.element.SessionConfig import SessionConfig
from onep.interfaces.InterfaceStatistics import InterfaceStatistics
from onep.interfaces.InterfaceFilter import *


#####################################################################
# Variables to be changed
#
# transport- Transport type: either TIPC or TLS
#            check tranport types supported on your image by
#            conf t --> onep --> transport  type ?
# cert     - certificate to be used for authentication in cse of TLS
#            transport
# appName  - OnePK application Name
# switchIP - management Switch IP address
# user     - switch userID
# pswd     - switch password
#
transport= 'TLS'
cert     = '<path>/cacert.pem'
appName  = "intf_properties_cn"
switchIP = "<ip>"
user     = "<user>"
pswd     = "<pswd>"

#####################################################################

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


RX_BYTES = InterfaceStatistics.InterfaceStatisticsParameter.ONEP_IF_STAT_RX_BYTES
FILTER =  InterfaceFilter(None, NetworkInterface.InterfaceTypes.ONEP_IF_TYPE_ETHERNET)

print "Getting Interface Statistics on", switchIP

intf_list_ne = ne.get_interface_list(FILTER)

for intf in intf_list_ne:
    try:
        int = ne.get_interface_by_name(intf.name)
        int_stats =  int.get_statistics()
        r_bytes=int_stats.get_param(RX_BYTES)
        if r_bytes > 0:
            print "Interface",intf.name,"RX_BYTES",r_bytes
    except:
        continue

ne.disconnect();
