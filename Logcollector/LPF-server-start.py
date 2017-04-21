#!/usr/bin/python
from multiprocessing import Process
import DataReceiveUDP
import DHKE_SERV

#start services
def start_serv():

	proc_lst=[]
	p1 = Process(target=DHKE_SERV.DHKE_main)
	proc_lst.append(p1)
	p2 = Process(target=DataReceiveUDP.main)
	proc_lst.append(p2)
#Start processes in proc_lst
	for p in proc_lst:
		p.start()
#wait for the processes to end
	for p in proc_lst:
		p.join()

if __name__=='__main__':
	start_serv()

