#!/usr/bin/python
from multiprocessing import Process
import DataReceiveUDP
import DHKE_SERV
import os.path
import re
import sys
#start services
def start_serv():
	server_ip='0.0.0.0'
	if os.path.isfile("/var/LPF-server/NLPF-server.conf"):
		opt=open("/var/LPF-server/NLPF-server.conf",'r')
		print "Reading configs....."
		options=opt.read().split("\n")
		#Fetch config options
		for i in range(0,len(options)):
			pattern = re.search(r"^#.*",str(options[i]))
			pattern1 = re.search(r"^server-ip(.*)",str(options[i]))
			if pattern:
				continue
			elif pattern1:
				IP_Str=re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',pattern1.group(1))
				if IP_Str:
					server_ip=str(IP_Str.group(1))
				else:
					err_log=open("/var/LPF-server/LPF-data/lpf.log",'a')
					print "Wrong Server-IP pattern in conf.....exiting!!!"
					err_log.write("Wrong IP pattern in conf.....exiting!!! \n")
					err_log.close()
					sys.exit()
	proc_lst=[]
	p1 = Process(target=DHKE_SERV.DHKE_main, args=(server_ip,))
	proc_lst.append(p1)
	p2 = Process(target=DataReceiveUDP.main)
	proc_lst.append(p2)
#Start processes in proc_lst
	for p in proc_lst:
		p.start()
#wait for the processes to end
	for p in proc_lst:
		p.join()

if __name__=='__main__':
	start_serv()

