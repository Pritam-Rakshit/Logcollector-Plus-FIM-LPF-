#!/usr/bin/python
import socket
import sys
import time
import os.path
from Crypto.Cipher import ARC4

#Production ready just copy paste
#Python dictionary to store key values
def key_stack():
	key_ring={}
	if os.path.isfile("/var/LPF-server/Client-gen/Client.keys"):
		key=open('/var/LPF-server/Client-gen/Client.keys','r')
		key_read=key.read()
		key_ext=key_read.split('\n')
		for i in range(0,len(key_ext)):
			if key_ext[i] != '' and key_ext[i] != '\n':
				store_key=key_ext[i].split(':')
				key_ring[store_key[0]]=store_key[1]	
		key.close()
	return key_ring

def reg_IP_list():
#	reg_open=open('/var/LPF-server/Client-gen/registered.list','r')
	ip_lst=[]
	if os.path.isfile("/var/LPF-server/Client-gen/registered.list"):
		reg_open=open('/var/LPF-server/Client-gen/registered.list','r')
		for line in reg_open:
			IP_id = line.decode('base64')
			IP = IP_id.split(':')[1]
			ip_lst.append(IP)

	return ip_lst

def main():
	HOST = ''   # Symbolic name meaning all available interfaces
	PORT = 8888 # Arbitrary non-privileged port
	err_log=open("/var/LPF-server/LPF-data/lpf.log",'a')
	en_log=open("/var/LPF-server/LPF-data/encrypted.log",'a')
	keep_alive=open("/var/LPF-server/LPF-data/agent_status.log",'a')
	err_count = 0
	localtime=time.localtime(time.time())
	date = str(localtime[0])+"-"+str(localtime[1])+"-"+str(localtime[2])
	try :
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		print 'N-LPF: Starting LPF server.....'
	except socket.error, msg :
		print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	# Bind socket to local host and port
	try:
		s.bind((HOST, PORT))
	except socket.error , msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	print 'N-LPF: Listening for incoming syslog events........'
	#now keep talking with the client
	while 1:
		keys=key_stack()
		reg_IP_chk = reg_IP_list()
		err_log=open("/var/LPF-server/LPF-data/lpf.log",'a')
		en_log=open("/var/LPF-server/LPF-data/encrypted.log",'a')
		keep_alive=open("/var/LPF-server/LPF-data/agent_status.log",'a')
		# receive data from client (data, addr)
		d = s.recvfrom(8192)
		data = d[0]
		addr = d[1]
		enc_check=data.split(':')
		#print enc_check
		if enc_check[0].strip() in reg_IP_chk:
			filename="/var/LPF-server/Received-logs/"+enc_check[0].strip()+"/Events-"+date+".log"
			file=open(filename,'a+')
			if enc_check[1] == ' en ':
				#Extract IP from log data to take d_key from keyring
				key_val = enc_check[0].strip()
				try:
					d_key = keys[str(key_val)].decode('base64','strict')
					decrypt_msg = ARC4.new(str(d_key))
					assemble=enc_check[2]
					if len(enc_check) > 3:
						for i in range(3,len(enc_check)):
							assemble = assemble + ":" + enc_check[i]
					data = decrypt_msg.decrypt(assemble)
					#print 'Message[' + addr[0] + ':' + str(addr[1]) + '] : ' +enc_check[0]+':'+enc_check[1]+': '+ data.strip() +'\n'
					file.write('Message[' + addr[0] + ':' + str(addr[1]) + '] : ' +enc_check[0]+':'+enc_check[1]+': ' + data.strip() + '\n')
				except KeyError:
					en_log.write('Message[' + addr[0] + ':' + str(addr[1]) + '] : ' + data.strip()+ '\n')
			elif enc_check[1] == ' keepalive ':
				#print 'Message[' + addr[0] + ':' + str(addr[1]) + '] : ' + data.strip() +'\n'
				keep_alive.write('Message[' + addr[0] + ':' + str(addr[1]) + '] : ' + data.strip()+ '\n')
			
			else:
				#print 'Message[' + addr[0] + ':' + str(addr[1]) + '] : ' + data.strip() +'\n'
				file.write('Message[' + addr[0] + ':' + str(addr[1]) + '] : ' + data.strip()+ '\n')
			file.close()
		else:
			if err_count == 0 or err_count % 1000 == 0:
				err_log.write("Unregistered IP trying to send logs - "+ enc_check[0].strip() + " ,Hits dropped - " + str(err_count+1) +" \n")
				err_count = err_count + 1
			else:
				err_count = err_count + 1
		keep_alive.close()
		en_log.close()
	s.close()
if __name__=='__main__':
	main()
