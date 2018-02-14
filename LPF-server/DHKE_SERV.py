#!/usr/bin/python
import random
import socket
from random import randint
import re
import Agent_registry
import os.path

#Diffie-Hellman key exchange initializer - server side
#remove IP_lst[] , check for multiple tries at same time, increase backlog to 15, work on data buffering
class DHE:
	def __init__(self):
		self.root_prime={2:11,3:7,3:17,5:23,5:37,5:73}
		self.rp_val=random.choice(self.root_prime.keys())
	def send_params(self):
		self.root=self.rp_val
		self.prime=self.root_prime[self.rp_val]
		return self.root , self.prime
	def key_gen(self):
		range_start = 10**(7-1)
		range_end = (10**7)-1
		self.key = randint(range_start, range_end)
	def shared_key(self):
		mod=(self.rp_val**self.key) % self.prime
		return str(mod)
# To be built
	def secret_key(self,recv_key):
		sec_key=(recv_key**self.key) % self.prime
		return sec_key


def DHKE_main(server_ip):
	host = ''
	port = 8844
	IP = server_ip
	kfile=open('/var/LPF-server/Client-gen/Client.keys','a')
	data_payload = 4096
	backlog = 20 #Max no. of queued connection
	sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_address= (host,port)
	sock.bind(server_address)
	sock.listen(backlog)
	IP_lst = [ ]
	print("N-LPF: Waiting to receive request from client....")
	while True:
		client , address=sock.accept()
#		client , address=sock.accept()
		data = client.recv(data_payload)
		#print("Client_data: "+data)
		if data:
			data1=data.decode('base64','strict')
			pattern=re.search(r"START_NEGOTIATION-(\d+\.\d+\.\d+\.\d+)",data1)
			if pattern:
				print("N-LPF: Received a registration request: "+str(pattern.group(1)))
				REGISTER=Agent_registry.REGISTER(pattern.group(1))
				client.send(REGISTER.encode('base64','strict'))
				DHO=DHE()
				l=DHO.send_params()
				k=DHO.key_gen()
				sk=DHO.shared_key()
				shared_data=str(l[0])+':'+str(l[1])+':'+sk+'-'+IP
				shared_dataEn = shared_data.encode('base64','strict')
				IP_lst.append(str(pattern.group(1)))
				client.send(shared_dataEn)
				data2= client.recv(data_payload)
				if data2:
					dataDecode=data2.decode('base64','strict')
					pattern2=re.search(r"SHARED_KEY-(\d+\.\d+\.\d+\.\d+)-(\d+)",dataDecode)					
					if pattern2:
						for i in range(0, len(IP_lst)):
							if IP_lst[i]==pattern2.group(1):
								recv_key=int(pattern2.group(2))
								key=DHO.secret_key(recv_key)
								write_key=pow(l[0],int(key))
								kfile.write(pattern2.group(1)+':'+str(write_key).encode('base64','strict'))
								IP_lst.remove(pattern2.group(1))
								kfile.close()
								kfile=open('/var/LPF-server/Client-gen/Client.keys','a')
								print("N-LPF: New client key added....")
			else:
				pattern=re.search(r"REGISTER-LPF-AGENT-(\d+\.\d+\.\d+\.\d+)",data1)
				if pattern:
					msg=Agent_registry.REGISTER(pattern.group(1))
					client.send(msg.encode('base64','strict'))
				else:
					pass

		else:
			continue #pattern didn't matched write a log


if __name__=='__main__':
	DHKE_main()
