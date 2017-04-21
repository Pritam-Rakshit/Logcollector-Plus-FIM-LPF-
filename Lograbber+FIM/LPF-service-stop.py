#!/usr/bin/python
import os
import sys
import time
def kill_switch():
	#status check
	processes=os.popen("ps -elf |grep 'LPF-' | grep -v grep | grep -v 'LPF-service-stop' | awk '{print $4}'").read()
	proc_lst=processes.split("\n")
	i= len(proc_lst) -1 
	cmd='kill -9'
	while i >= 0:
		cmd= cmd + ' ' +str(proc_lst[i])
		i=i-1
	print "Stopping Netra services....."
	stat=os.system(cmd)
	if stat == 0:
		print "Service having been stopped...."
	sys.exit()				
if __name__=='__main__':
	kill_switch()
