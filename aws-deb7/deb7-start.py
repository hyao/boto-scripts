#!/usr/bin/python

import boto.ec2
from time import sleep
import os

conn = boto.ec2.connect_to_region('ap-northeast-1')

print "starting Debian 7 on AWS ap-northeast-1..."
res = conn.run_instances('ami-9dd8529c', 
          key_name='aws-ap-ne-1',
          instance_type='t1.micro',
          security_groups=['quicklaunch-0'])
          #make sure only 1 instance is launched even if run multiple times 
          #return reservation if instance already exists
          #client_token='aws-ne-1-deb7-0')

instance = res.instances[0]
instance.add_tag('Name', 'AWS-Deb7')

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
os.system('ssh-keyscan -H ' + eip + ' >> ~/.ssh/known_hosts')
print
print "type deb7 to ssh into ec2 box"
