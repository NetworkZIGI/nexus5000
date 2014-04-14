#! /usr/bin/env python

# *------------------------------------------------------------------
# * onep-element_property.py
# *
# * Simple script to show switch system information
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
# TCP and TLS. Check on device using the following CLIs:
# conf t --> onep --> transport  type ?
#
# A network interface must be configured with a valid IP address and
# pingable.
#
# To use this script you should:
# 1) Copy the file to a server with OpePK SDK
# 2) setup the variables in the section below
# 3) run the script:
#    Usage: python onep-element_property.py -a <address or FQDN> [-t <transport>] [-C <client cert file>] \n [-K <client private key file>] \n [-R <root certificates file>]"
# Examples:
#   python onep-element_property.py -a 10.29.176.178
#   python onep-element_property.py -a 10.29.176.178 -t tls -R /root/onePK-sdk-python-rel-1.1.0.115/cacert.pem

import logging
import getopt
import sys
import getpass
from onep.element.NetworkElement import NetworkElement
from onep.element.SessionConfig import SessionConfig
from onep.core.util.HostIpCheck import HostIpCheck
from onep.core.exception.OnepIllegalArgumentException import OnepIllegalArgumentException

#####################################################################
# Variables to be changed
#
# transport        - Transport type: either TCP or TLS
#                    check tranport types supported on your image by
#                    conf t --> onep --> transport  type ?
# root_cert_path   - Root certificate to be used for authentication in cse of TLS
#                    transport. Can be changed by -R option
# client_cert_path - Client certificate to be used for authentication in cse of TLS
#                    transport. Can be configured by -R option
# client_key_path  - Client Key to be used for authentication in cse of TLS
#                    transport. Can be configured by -R option
#
transport= 'TLS'
root_cert_path     = '<path>/cacert.pem'
client_cert_path = None
client_key_path = None
switchIP = "<ip>"
user     = "<user>"
pswd     = "<pswd>"
#####################################################################
logging.basicConfig(level=logging.WARNING)

def parse_command_line(args):
    """
    Parse the command line options. If the required argument "-a" for element address or FQDN is not provided,
    this method displays the proper usage information and calls sys.exit(1).

    @param args  The args string passed into the main(...) method.

    @return true if parsing the command line succeeds, false otherwise.
    """
    try:
        opts, args = getopt.getopt(args[1:],"ha:t:R:C:K:",["address=","transport=", "rootcert=", "clientcert=", "key="])
    except getopt.GetoptError as err:
        print str(err)
        logger.info(get_usage())
        sys.exit(2)


    """
     * options:
     *       -a, --address <network element address or FQDN>
     *       -t, --transport <transport type> default is tls
     *       -C, --clientcert <client certificate file>
     *       -K, --clientkey <client private key file>
     *       -R, --rootcert <root certificates file>
    """
    for option, arg in opts:
        if option == '-h':
            logger.info(get_usage())
            sys.exit()
        elif option in ("-a", "--address"):
            global switchIP
            switchIP = arg
        elif option in ("-t", "--transport"):
            global transport
            transport = arg
        elif option in ("-R", "--rootcert"):
            global root_cert_path
            root_cert_path = arg
        elif option in ("-C", "--clientcert"):
            global client_cert_path
            client_cert_path = arg
        elif option in ("-K", "--key"):
            global client_key_path
            client_key_path = arg
    global username
    username = raw_input('Enter Username : ')
    global password
    password = getpass.getpass('Enter Password : ')

    if(switchIP==None):
        logger.error(get_usage())
        return False

    return True
def get_usage():
        return " Usage: -a <address or FQDN> [-t <transport>] [-C <client cert file>] \n [-K <client private key file>] \n [-R <root certificates file>]"

def sampleapp():
    appname = raw_input('Enter name of application : ')

    session_config = SessionConfig(SessionConfig.SessionTransportMode.TLS) #default is TLS
    if transport.lower() == "tipc" or transport == 2:
        session_config = SessionConfig(SessionConfig.SessionTransportMode.TIPC)
    session_config.ca_certs = root_cert_path
    session_config.certfile = client_cert_path
    session_config.keyfile = client_key_path

    ne = NetworkElement(switchIP, appname)
    con = ne.connect(username, password, session_config)
    print 'Connected to host'

    print "System Name:            ", ne.properties.sys_name
    print "System Uptime:          ", ne.properties.sys_uptime
    print "Total System Memory:    ", ne.total_system_memory
    print "Free System Memory:     ", ne.free_system_memory
    print "System CPU Utilization: ", ne.system_cpu_utilization, "%\n"
    print "System Connect Time:    ", ne.get_connect_time()
    print "System Disonnect Time:  ", ne.get_disconnect_time()
    print "System __str__ Method:  ", ne
    print "Host Content String:\n",   ne.properties.content_string

    ne.disconnect()

if __name__=='__main__':
    logger = logging.getLogger('onep')
    logger.setLevel(logging.INFO)
    if not parse_command_line(sys.argv):
        logger.error("Error in parsing arguments")
        sys.exit(1)
    sampleapp()
