#/usr/bin/python
import socket
import re
import os
import time

#block.list
#allowed.list
def set_ID():
	ID = 1
	if os.path.isfile("/var/LPF-server/Client-gen/registered.list"):
		chk= open("/var/LPF-server/Client-gen/registered.list","r")
		reg_list= chk.read().split('\n')
		i= len(reg_list)-1
		while i>=0:
			if reg_list[i] != '':
				info= reg_list[i].decode('base64','strict')
				j= info.split(':')
				if int(j[0])>= 0:
					ID = int(j[0]) + 1
					break
			else:
				pass
			i=i-1
	#print "ID = "+str(ID)
	return ID

def REGISTER_CLI(IP):
	agent_id = set_ID()
	log = open("/var/LPF-server/LPF-data/lpf.log",'a+')
	rfile = open("/var/LPF-server/Client-gen/registered.list",'a+')
	cmd = 'mkdir /var/LPF-server/Received-logs/' + IP
	os.system(cmd)
	reg_val=str(agent_id)+":"+IP
	reg_write=reg_val.encode('base64','strict')
	rfile.write(reg_write)
	msg = "REGISTERED:"+IP+":"+str(agent_id)
	log.write(str(time.asctime(time.localtime(time.time())))+" New client registered: "+IP+"\n")
	rfile.close()
	return msg

def REGISTER(IP):
	if os.path.isfile("/var/LPF-server/Client-gen/registered.list"):
		check=open("/var/LPF-server/Client-gen/registered.list",'r')
		ip_check=check.read().split('\n')
		flag=0
		for i in range(len(ip_check)):
			ip_decode=ip_check[i].decode('base64','strict')
			match=re.search(r"\d+:(\d+\.\d+\.\d+\.\d+)",ip_decode)
			if match:
				if match.group(1) == IP:
					flag = 1
					msg = "Agent already registered"
			else:
				pass
		if flag==0:
			msg=REGISTER_CLI(IP)
	else:
		msg=REGISTER_CLI(IP)
	print msg
	return msg
if __name__=='__main__':
	REGISTER('192.168.1.14')
