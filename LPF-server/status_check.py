#!/usr/bin/python
import re
import time
import datetime
def status_check():
	#file_check=open('/var/LPF-server/LPF-data/agent_status.log','r')
	agent_list_un=open('/var/LPF-server/Client-gen/registered.list','r')
#	agent_list_en=open('/var/LPF-server/Client-gen/Client.keys','r')
	check_limit=500
	checklist={}
	disconnected=[]
	ip=''
	i=0
	line=agent_list_un.read()
	if line != '\n' and line != '':
		line_ext=line.split('\n')
		#Iterate each entry and fetch into dictionary
		for j in range(0,len(line_ext)):
			if line_ext[j] != '' and line_ext[j] != '\n':
				data=line_ext[j].decode('base64','strict')
				data_ext=data.split(':')
				checklist[data_ext[0]]=data_ext[1]
				i=int(data_ext[0])
	month={"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
	localtime = time.localtime(time.time())
	today = datetime.date.today()
	print "-------------Netra LPF v1.1 client status check--------------"
	for key in checklist:
		ip=checklist[key]
		flag=0
		j=0
		for line_check in reversed(open("/var/LPF-server/LPF-data/agent_status.log").readlines()):
			if j > check_limit:
				break
			j=j+1
			#print line
			match=re.search(r"(\d+\.\d+\.\d+\.\d+)\s+:\s+keepalive.*?(\w\w\w)\s+(\d+)\s+\d+:\d+:\d+",line_check)
			if match:
				log_date_lst=[localtime[0],month[str(match.group(2))],match.group(3)]
				LOG_CURRENT_DATE= datetime.date(int(log_date_lst[0]),int(log_date_lst[1]),int(log_date_lst[2]))
				distance= today - LOG_CURRENT_DATE
				if match.group(1) == ip and int(distance.days) < 1:
					print "		"+str(key)+" : "+ip+" : Active"
					flag=0
					break
				else:
					flag=1
		if flag == 1:
			print "		"+str(key)+" : "+ip+" : Disconnected"

if __name__ == "__main__":
	status_check()
