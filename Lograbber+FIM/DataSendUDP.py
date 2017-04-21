#!/usr/bin/python
import socket   #for sockets
import sys  #for exit

def datasend(msg,ip): 
	# create dgram udp socket
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	except socket.error:
		print 'Failed to create socket'
		sys.exit()
 
	host = ip
	port = 8888
     
	try :
		#Set the whole string
		s.sendto(msg, (host, port))
     		s.close()
	except socket.error, msg:
		print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
#if __name__=="__main__":
	#datasend(msg)

