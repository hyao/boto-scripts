#!/usr/bin/python

import boto.ec2

conn = boto.ec2.connect_to_region('ap-northeast-1')
res = conn.get_all_instances()

instance = res[0].instances[0]

print 'AWS deb7 instance is currently %s' % instance.state

if instance.state == u'running':
    print "deb7 ip: %s" % instance.ip_address
