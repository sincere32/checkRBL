#!/usr/bin/env python

# imports
import sys
import ipaddress
import dns.resolver
from timeit import default_timer as timer
import argparse

rbllist = []
ctr = 0
IP = ""
dnsrecords = []

def read_rbl_list():

    with open("rbllist.txt", "r") as rbltext:
        for line in rbltext:
            rbllist.append(line.strip())
    rbltext.close()

def validateIP(ipaddr):
    try:
        ipaddress.ip_address(ipaddr)
        if ipaddress.IPv4Address(ipaddr):
           return 1
        elif ipaddress.IPv6Address(ipaddr):
            return 1
        else:
            return 0
    except ValueError as e:
        print (e.args[0])

def networkIP (ipaddr):
    if ipaddress.ip_address(ipaddr).is_private:
        print (ipaddr + " is a Private IP. Exiting..")
        sys.exit()
    else:
        return ipaddr

def revIP (ipaddr):
    reverseIP = '.'.join((ipaddr).split(".")[::-1])
    return (reverseIP)

def rbl_lookup(ip):
    start = timer()
    errlist = []
    for rbl in rbllist:
        query_string = ip + "." + rbl
        
        dnsResolver = dns.resolver.Resolver()
        dnsResolver.timeout = 1
        dnsResolver.lifetime = 1
        try:
            dnsAnswer = dnsResolver.query(query_string, "A")
            if len(dnsAnswer) > 0:
                dnsrecords.append(ipaddr)
                dnsrecords.append(rbl)
                txtAnswer = dnsResolver.query(query_string, "TXT")
                for rdata in txtAnswer:
                    dnsrecords.append(rdata)
        except Exception as e:
            errlist.append(rbl)
            errlist.append(e)
    end = timer()
    print(end - start) 
    print(dnsrecords)
#    print (errlist)

def checkRBL (ipaddr):
    rev_ipaddr = revIP(ipaddr)
    read_rbl_list()

    rbl_lookup(rev_ipaddr)

def main():
    """
    Main function.
    Checks command-line arguments and calls the relevant function.
    """
    cli_argparser = argparse.ArgumentParser(description='')
    cli_argparser.add_argument('-i', '--ip', help="Enter the IP address to be checked", required=False)
    cli_argparser.add_argument('-d', '--domain', help="Enter the domain name to be checked", required=False)
    cli_args = cli_argparser.parse_args()

    if (cli_args.domain and cli_args.ip):
        print ("Invalid input. Enter either the IP address or the Domain name")
    elif (cli_args.ip):
        if validateIP(cli_args.ip):
            if networkIP(cli_args.ip):
                checkRBL(cli_args.ip)
    elif (cli_args.domain):
        print ("Domain")
        # Reverse look up domain and then test the IP
    else:
        print (cli_argparser.print_help())

if __name__ == '__main__':
    sys.exit(main())
