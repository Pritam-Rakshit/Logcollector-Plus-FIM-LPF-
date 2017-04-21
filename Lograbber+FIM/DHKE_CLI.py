#!/usr/bin/python
import re
import time
import socket
import random
import os.path
from random import randint

class DHE:
	def __init__(self,root,prime,recv_key):
		self.root=root
#		print("Root: -->"+str(self.rp_val))
		self.prime=prime
#		print("Prime: -->"+str(self.root_prime[self.rp_val]))
		#return self.root , self.prime
		self.recv_key=recv_key
	def key_gen(self):
		range_start = 10**(7-1)
		range_end = (10**7)-1
		self.key = randint(range_start, range_end)
	def shared_key(self):
		mod=(self.root**self.key) % self.prime
		return str(mod)
# To be built
	def secret_key(self):
		sec_key=(self.recv_key**self.key) % self.prime
		return sec_key

		
def DHKE_CLI(server_ip,agent_ip):
	host = server_ip
	port = 8844
	IP=agent_ip
	err=open("error.log",'a+')
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the server
	server_address = (host, port)
	kfile=open('agent.key','w')
	print "Connecting to %s port %s" % server_address
	sock.connect(server_address)
	try:
		message="START_NEGOTIATION-"+str(IP)
		msg= message.encode('base64','strict')
		sock.send(msg)
		data=sock.recv(4096)
		print "Negotiating secret key with the server...."
		if data:
			dataDecode=data.decode('base64')
			pattern=re.search(r"(\d+):(\d+):(\d+)-(\d+\.\d+\.\d+\.\d+)",dataDecode)
			if pattern:
				root=int(pattern.group(1))
				prime=int(pattern.group(2))
				recv_key=int(pattern.group(3))
				DHO=DHE(root,prime,recv_key)
				DHO.key_gen()
				share_key=DHO.shared_key()
				message1="SHARED_KEY-"+IP+"-"+share_key
				msg1=message1.encode('base64','strict')
				sock.send(msg1)
				key=DHO.secret_key()
				write_key=pow(root,key)
				kfile.write(IP+':'+str(write_key).encode('base64','strict'))
				kfile.close()
	except socket.errno, e:
		print "Socket error: %s" %str(e)
		err.write("Connection failure - Socket error: %s" %str(e))
	except Exception, e:
		print "Other exception: %s" %str(e)
		err.write("Connection failure - Other exception: %s" %str(e))
	finally:
		#Let the server add key at its end
		time.sleep(20)
		print "Key added...."
		sock.close()
def key_check(server_ip,agent_ip):
	if os.path.isfile("agent.key"):
		chk=open("agent.key","r")
		value=chk.read()
		if value == '' or value == '\n':
			DHKE_CLI(server_ip,agent_ip)
		else:
			val_split=value.split(':')
			if str(val_split[0]) == agent_ip:
				print "Key already exists"
				return 0

	else:
		DHKE_CLI(server_ip,agent_ip)

if __name__=='__main__':
	DHKE_CLI('127.0.0.1','127.0.0.1')
