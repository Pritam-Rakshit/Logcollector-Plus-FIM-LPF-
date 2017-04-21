#!/usr/bin/python
import DataSendUDP
import sys
import time
import re
import os.path
from Crypto.Cipher import ARC4

#function to tail read a file
def tail(log_loc,server_ip,en_status,agent_ip,key_val):
	err=open("error.log",'a')
	if os.path.isfile(str(log_loc)):
		sysread=open(str(log_loc),'r')
		file_pointer=sysread.tell()
		#Build offset file
		start_string=re.search(r"^/\w+/\w+/(\w+)",log_loc)
		if start_string:
			filename="offsets/"+str(start_string.group(1))+"_offset"
			offset=open(filename,'a+')
			seek_loc=offset.readline() #store and read offset from file
			offset.close()
			if seek_loc=='':
				seek_loc=0
			offset=open(filename,'w')
			read="start"
			try:
				sysread.seek(int(seek_loc),0)
				while read !='':
					read=sysread.readline()
					#Not to send blank packets
					if read != '' and read != '\n' and en_status == 1:
						enc = ARC4.new(key_val)
						text = str(read)
						cipher_text = enc.encrypt(text)
						msg = str(agent_ip)+" : en :"+cipher_text
						DataSendUDP.datasend(msg,server_ip)
					elif read != '' and read != '\n' and en_status == 0:
						msg = str(agent_ip)+" : un :"+read
						DataSendUDP.datasend(msg,server_ip)
				file_pointer=sysread.tell()
				offset.write(str(file_pointer))
				offset.close()
			except KeyboardInterrupt:
				file_pointer=sysread.tell()
				offset.write(file_pointer)
				offset.close()
				sys.exit()
		else: 
			#print "Unable to find offset file....exiting!!!"
			#err.write(filename+" :Unable to read offset file. \n")
			return 0
	else:
		return 0

def tail_call(log_loc,server_ip,enc,agent_ip):
#call file tail 5 secs after every cycle
	err=open("error.log",'a')
	if os.path.isfile("agent.key"):
		key=open('agent.key','r')
		key_read=key.readline()
		if key_read != '':
			key_ext=key_read.split(':')
			key_val=key_ext[1].decode('base64','strict')
		else:
			key_val=''
			enc=0
			err.write('Key value not found for agent. Kindly remove the "agent.key" file and restart client service. Make sure port 8844 (TCP) of '+server_ip+' is reachable from here')
		while 1:
			time.sleep(5)
			tail(log_loc,server_ip,enc,agent_ip,key_val)
	else:
		key_val=''
		while 1:
			time.sleep(5)
			tail(log_loc,server_ip,enc,agent_ip,key_val)
	err.close()
	return 0
if __name__=='__main__':
	tail_call()

#Built by - Pritam Rakshit - 2017
