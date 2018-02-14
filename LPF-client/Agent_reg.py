#!/usr/bin/python
import socket
from random import randint
import re
import os.path



def REGISTER_CLI(server_ip,agent_ip):
	host = server_ip
	port = 8844
	IP=agent_ip
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the server
	server_address = (host, port)
	rfile=open('/var/LPF-client/keystore/agent.status','w')
	print "Connecting to %s port %s" % server_address

	try:
		sock.connect(server_address)
		message="REGISTER-LPF-AGENT-"+str(IP)
		msg= message.encode('base64','strict')
		sock.send(msg)
		data=sock.recv(2048)
		if data:
			dataDecode=data.decode('base64')
			pattern=re.search(r"REGISTERED:(\d+\.\d+\.\d+\.\d+):(\d+)",dataDecode)
			if pattern:
				if pattern.group(1) == IP:
					rfile.write(dataDecode)
					print "LPF client registered successfully...."
				else:
					print "Negotiation with server failed..."
	except socket.errno, e:
		print "Socket error hola: %s" %str(e)
	except Exception, e:
		print "Other exception: %s" %str(e)
	finally:
		print "Closing connection to the server"
		sock.close()

#If already registered condition here ***Add if val == 0
def reg_check(server_ip,agent_ip):
	if os.path.isfile("agent.status"):
		chk=open("/var/LPF-client/keystore/agent.status","r")
		value=chk.read()
		if value == '' or value == '\n':
			REGISTER_CLI(server_ip,agent_ip)
		else:
			val_split=value.split(':')
			if str(val_split[1]) == agent_ip:
				print "Client already registered"
				return 0
			else:
				REGISTER_CLI(server_ip,agent_ip)
	else:
		REGISTER_CLI(server_ip,agent_ip)

if __name__=='__main__':
	reg_check('127.0.0.1','192.168.1.91')