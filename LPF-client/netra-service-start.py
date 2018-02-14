#!/usr/bin/python
import os
import sys
import re
import time
import threading
import DynamicRead
import DHKE_CLI
import fimcheck_final
import chk_rotate
import Agent_reg
import KeepAlive
from multiprocessing import Process

#Remember to design a kill switch

def main():
#Thread module - subclass
	class myThread (threading.Thread):
	    def __init__(self, log_loc, server_ip, enc, agent_ip):
	        threading.Thread.__init__(self)
	        self.log_loc = log_loc
	        self.server_ip = server_ip
		self.enc = enc
		self.agent_ip = agent_ip
	    def run(self):
	        DynamicRead.tail_call(self.log_loc, self.server_ip, self.enc, self.agent_ip)
	Thrd_lst=[]
	#Check and fetch details from config file
	err=open("error.log",'a')
	ip=''
	if os.path.isfile("/var/LPF-client/NLPF-client.conf"):
		opt=open("/var/LPF-client/NLPF-client.conf",'r')
		print "N-LPF: Reading configs....."
		options=opt.read().split("\n")
		#Fetch config options
		for i in range(0,len(options)):
			pattern=re.search(r"^#.*",str(options[i]))
			pattern2=re.search(r"^server-ip=(.*)",str(options[i]))
			pattern3=re.search(r'^location=(\S+)',str(options[i]))
			pattern4=re.search(r'^FIMloc=(\S+)',str(options[i]))
			pattern5=re.search(r'^Interval=(\d+)',str(options[i]))
			pattern6=re.search(r'^Encryption=(\S+)',str(options[i]))
			pattern7=re.search(r"^agent-ip=(.*)",str(options[i]))
			if pattern:	
				continue
			elif pattern2:
				IP_Str=re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',pattern2.group(1))
				if IP_Str:
					server_ip=IP_Str.group(1)
				else:
					print "Wrong Server-IP pattern in conf.....exiting!!!"
					err.write("Wrong IP pattern conf.....exiting!!! \n")
					sys.exit()
			elif pattern3:
				log_loc=pattern3.group(1).split(',')
			elif pattern4:
				fim_loc=pattern4.group(1).split(',')
			elif pattern5:
				if pattern5.group(1) != '' and pattern5.group(1) != 0:
					fim_interval=int(pattern5.group(1))
				else:
					fim_interval=1200
			elif pattern6:
				if str(pattern6.group(1))=='on':
					enc = 1
					print "Encryption value set : on"
				else:
					enc = 0
			elif pattern7:
				#pass agent IP to dynamicread.py for appending to syslog messages
				IP_Str=re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',pattern7.group(1))
				if IP_Str:
					agent_ip=IP_Str.group(1)
				else:
					print "Wrong agent-IP pattern in conf.....exiting!!!"
					err.write("Wrong IP pattern in conf.....exiting!!! \n")
					sys.exit()
		#start services and threads
		print("N-LPF: Setting up encryption parameters with the server......")
		if enc==1:
			p1 = Process(target=DHKE_CLI.key_check,args=(server_ip,agent_ip)) #make changes in DHKE_CLI to not to negotiate key if already done
			p1.start()
			p1.join()
		elif enc==0:
			p1 = Process(target=Agent_reg.reg_check,args=(server_ip,agent_ip)) #make changes in DHKE_CLI to not to negotiate key if already done
			p1.start()
			p1.join()
		else:
			pass
		time.sleep(7)
		print("N-LPF: Starting FIM engine.....")
		p2 = Process(target=fimcheck_final.FimInitiate, args=(fim_interval,fim_loc))
		p2.start()
		p3 = Process(target=chk_rotate.chk_status_run, args=(3600,log_loc))
		p3.start()
		p4 = Process(target=KeepAlive.keepalive_start, args=(server_ip,agent_ip))
		p4.start()		
		T_count=0
		print("N-LPF: Starting logcollector instances....")
		for i in range(0,len(log_loc)):
			# Create new threads per log location
			MyT = myThread(log_loc[i],server_ip,enc,agent_ip)
			Thrd_lst.append(MyT)
		for i in Thrd_lst:
			T_count=T_count+1
			i.start()
		for i in Thrd_lst:
			i.join()
		p2.join()
		p3.join()
		p4.join()


	else:
		print "Config file not found...exiting!!!"
		err.write("Config file not found...exiting!!! \n")
		sys.exit()
if __name__=="__main__":
	main()
	
