#!/usr/bin/python

import boto.ec2
from time import sleep
import os

conn = boto.ec2.connect_to_region('ap-northeast-1')
res = conn.get_all_instances()

instance = res[0].instances[0]

print "starting Debian 7 on AWS ap-northeast-1..."
instance.start()

ip_address = conn.allocate_address()
eip = ip_address.public_ip
while instance.state !=  u'running':
    sleep(2)
    instance.update()
    
print "associating ip address %s to instance" % eip
conn.associate_address(instance.id, eip) 

def write_ssh_script(ip):
    file_name = '/opt/repo/admin/scripts/deb7'
    f = file(file_name, 'w')
    f.write('ssh -i /opt/repo/admin/credentials/aws-ap-ne-1.pem admin@%s \n' %ip)
    f.close()
    os.system('chmod +x %s' %file_name)

write_ssh_script(eip)
#add eip to known hosts
os.system('ssh-keyscan -H %s >> ~/.ssh/known_hosts' %eip)
print
print "type deb7 to ssh into ec2 box"
