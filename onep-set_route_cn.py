#! /usr/bin/env python

# *------------------------------------------------------------------
# * onep-set_route_cn.py
# *
# * Simple script to set a new route
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
# 3) run the script: python onep-set_route_cn.py
#

from onep.element.NetworkElement import NetworkElement
from onep.element.SessionConfig import SessionConfig
from onep.interfaces.InterfaceStatistics import InterfaceStatistics
from onep.interfaces.InterfaceFilter import *

from onep.routing.RoutingClass import *
from onep.routing.L3UnicastNextHop import *
from onep.routing.L3UnicastRoute import *
from onep.routing.L3UnicastRouteOperation import *
from onep.interfaces.NetworkPrefix import *

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
appName  = "set_route"
switchIP = "<ip>"
user     = "<user>"
pswd     = "<pswd>"

prefix_addr    = "200.10.11.0"
prefix_mask    = 24
#next_hop_intf = "Ethernet1/5"
next_hop_intf  = "loopback0"
next_hop_addr  = "10.15.1.1"

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


#Get a routing instance associated with a network element
routing = Routing.get_instance(ne)

#Get RIB information
#rib = routing.rib

approutetable=routing.app_route_table
scope = L3UnicastScope("", L3UnicastScope.AFIType.IPV4, L3UnicastScope.SAFIType.UNICAST, "base")
prefix = NetworkPrefix(prefix_addr, prefix_mask)

intf = ne.get_interface_by_name(next_hop_intf)
nexthop_list = list()
nexthop_list.append(L3UnicastNextHop(intf, next_hop_addr,scope))

route1 = L3UnicastRoute(prefix,nexthop_list,7,None,2,16)

routeop1 = L3UnicastRouteOperation(RouteOperation.RouteOperationType.ADD,route1)
oplist1 = list()
oplist1.append(routeop1)

#update routing table
added_routes = approutetable.update_routes(scope,oplist1)

#print the added route
for route_op in added_routes:
   print route_op.route

raw_input("Press Enter to Remove Route and Stop Application")

print ("Disconnecting from the NE")
ne.disconnect()
