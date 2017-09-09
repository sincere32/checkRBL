#!/usr/bin/env python

# imports
import sys
import ipaddress

rbllist = []
ctr = 0
IP = ""

with open("rbllist.txt", "r") as rbltext:
    for line in rbltext:
        rbllist.append(line.strip())
rbltext.close()

def validateIP(ipaddr):
    if ipaddress.ip_address(ipaddr):
        if ipaddress.IPv4Address(ipaddr):
            return 1
        elif ipaddress.IPv6Address(ipaddr):
            return 1
        else:
            return 0
    else:
        return 0

if len(sys.argv) < 2:
    print ("Enter at least one IP")
elif len(sys.argv) > 2:
    print ("Enter only one IP")
else:
    print (sys.argv[1])
    IP = sys.argv[1]
    if validateIP(IP):
        print ("checking now")
    else:
        print ("incorrect input")

