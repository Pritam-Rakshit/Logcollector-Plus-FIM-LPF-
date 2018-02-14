#/usr/bin/python
import os
import sys
import time
import socket
def keepalive(server_ip , agent_ip):
	#status check
	server = server_ip
	port = 8888
	processes=os.popen("ps -elf |grep netra | grep -v grep | grep -v 'netra-service-stop' | awk '{print $4}'").read()
	proc_lst=processes.split("\n")
	if len(proc_lst) > 2:
		localtime = time.asctime( time.localtime(time.time()) )
		craft_msg =	str(agent_ip)+" : keepalive : " + str(localtime) + " - LPF services are active\n"
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock.sendto(craft_msg, (server, port))
			sock.close()
		except socket.error, msg:
			print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()
	else:
		pass
def keepalive_start(server_ip,agent_ip):
	while 1:
		keepalive(server_ip,agent_ip)
		time.sleep(300)
		

#https://www.tutorialspoint.com/python/python_date_time.htm
