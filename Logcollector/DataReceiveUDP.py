#!/usr/bin/python
import socket
import sys
import time
import os.path
from Crypto.Cipher import ARC4

#Python dictionary to store key values
def key_stack():
	key_ring={}
	if os.path.isfile("Client.keys"):
		key=open('Client.keys','r')
		key_read=key.read()
		key_ext=key_read.split('\n')
	for i in range(0,len(key_ext)):
		if key_ext[i] != '' and key_ext[i] != '\n':
			store_key=key_ext[i].split(':')
			key_ring[store_key[0]]=store_key[1]
	return key_ring
def main():
	HOST = ''   # Symbolic name meaning all available interfaces
	PORT = 8888 # Arbitrary non-privileged port
	localtime=time.localtime(time.time())
	date = str(localtime[0])+"-"+str(localtime[1])+"-"+str(localtime[2])
	try :
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		print 'Starting LPF server.....'
	except socket.error, msg :
		print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()


	# Bind socket to local host and port
	try:
		s.bind((HOST, PORT))
	except socket.error , msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	print 'Listening for incoming syslog events........'
	#now keep talking with the client
	while 1:
		filename="Events-"+date+".log"
		file=open(filename,'a')
		# receive data from client (data, addr)
		d = s.recvfrom(8192)
		data = d[0]
		addr = d[1]
		enc_check=data.split(':')
		#print enc_check
		if enc_check[1] == ' en ':
			#Extract IP from log data to take d_key from keyring
			keys=key_stack()
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
				en_log=open("encrypted.log",'a+')
				en_log.write('Message[' + addr[0] + ':' + str(addr[1]) + '] : ' +enc_check[0]+':'+enc_check[1]+': ' + data + '\n')
		else:
			#print 'Message[' + addr[0] + ':' + str(addr[1]) + '] : ' + data.strip() +'\n'
			file.write('Message[' + addr[0] + ':' + str(addr[1]) + '] : ' + data.strip()+ '\n')
		
		file.close()
	s.close()
if __name__=='__main__':
	main()
