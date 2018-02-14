#!/usr/bin/python
import re
import time

def delist():
	delist_IP=raw_input("Enter the IP to be removed:")
	match=re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",delist_IP)
	if match:
		reg=open("/var/LPF-server/Client-gen/registered.list",'r')
		lines=reg.readlines()
		reg.close()
		r_flag=0
		c_flag=0
		reg=open("/var/LPF-server/Client-gen/registered.list",'w')
		for line in lines:
			pattern=re.search(r"(\d+)\:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",line.decode('base64','strict'))
			if pattern:
				if pattern.group(2) != delist_IP:
					reg.write(line)
				elif pattern.group(2) == delist_IP:
					r_flag=1
					log=open("/var/LPF-server/LPF-data/lpf.log",'a')
					log.write(str(time.asctime(time.localtime(time.time()))) +" ID: "+pattern.group(1)+", IP: "+delist_IP+" has been delisted. \n")
					log.close()
			else:
				pass
		reg.close()

		cli=open("/var/LPF-server/Client-gen/Client.keys",'r')
		lines=cli.readlines()
		cli.close()
		cli=open("/var/LPF-server/Client-gen/Client.keys",'w')
		for line in lines:
			pattern=re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\:",line)
			if pattern:
				if pattern.group(1) != delist_IP:
					cli.write(line)
				elif pattern.group(1) == delist_IP:
					c_flag=1
					log=open("/var/LPF-server/LPF-data/lpf.log",'a')
					log.write(str(time.asctime(time.localtime(time.time()))) +" IP: "+delist_IP+" - Encryption/Decryption key removed. \n")
					log.close()
			else:
				pass
		cli.close()
		
		if c_flag == 0 and r_flag == 0:
			print "Error: The IP:"+delist_IP+" not found in registry. Please enter a registered agent IP...."
		if r_flag == 1 and c_flag == 1:
			print "Registry value removed...."
			print "Encryption/Decryption key removed...."
			print "***Please restart LPF-server for the changes to take effect***"
		if r_flag == 1 and c_flag == 0:
			print "Registry value removed...."
			print "***Please restart LPF-server for the changes to take effect***"
			
		
	else:
		print "Error: Wrong IP format."
		exit()
if __name__ == "__main__":
	delist()
