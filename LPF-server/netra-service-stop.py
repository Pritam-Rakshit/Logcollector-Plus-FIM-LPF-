#!/usr/bin/python
import os
import sys

def kill_switch():
        #status check
        processes=os.popen("ps -elf |grep 'netra-' | grep -v grep | grep -v 'netra-service-stop' | awk '{print $4}'").read()
        proc_lst=processes.split("\n")
        i= len(proc_lst) -1
        if i > 0:
                cmd='kill -9'
                while i >= 0:
                        cmd= cmd + ' ' +str(proc_lst[i])
                        i=i-1
                print "N-LPF: Stopping Netra services....."
                stat=os.system(cmd)
                if stat == 0:
                        print "N-LPF: Services has been stopped....."
                sys.exit()
        else:
                print "N-LPF: Services not running....."
if __name__=='__main__':
        kill_switch()
