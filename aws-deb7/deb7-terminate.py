#!/usr/bin/python

import boto.ec2

conn = boto.ec2.connect_to_region('ap-northeast-1')
res = conn.get_all_instances()

instance = res[0].instances[0]

print "terminating Debian 7 on AWS ap-northeast-1..."
instance.terminate()

ip_address = conn.get_all_addresses()
ip = ip_address[0].public_ip
print "releasing EIP: %s" % ip
conn.release_address(ip)

