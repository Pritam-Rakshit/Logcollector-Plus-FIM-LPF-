#!/usr/bin/python
import os
import time
import re
import os.path
#Check if log files have been rotated. Set file read offset to zero - 0 if found true.
def chk_status(log_loc = []):
	month={"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
	localtime=time.localtime(time.time())
	for i in range(len(log_loc)):
		if os.path.isfile(log_loc[i]):
			start_string=re.search(r"^/\w+/\w+/(\w+)",log_loc[i])
			filename="/var/LPF-client/T_stamp_dir/T_stamp_"+str(start_string.group(1))
			T_stamp_store=open(filename,'a+')
			T_val_chk = T_stamp_store.read()
			T_stamp_store.close()
			T_stamp_raw=os.popen("head -1 "+log_loc[i]).read()
			T_stamp=re.search(r"(\w+)\s+(\d+)\s+(\d+:\d+:\d+)",T_stamp_raw)
			if T_stamp:
				T_val=T_stamp.group(2)+"/"+month[T_stamp.group(1)]+"/"+str(localtime[0])+":"+T_stamp.group(3)
			else:
				T_val = 'None'
			if T_val_chk != T_val:
				T_stamp_store=open(filename,'w')
				T_stamp_store.write(T_val)
				print("N-LPF: Setting file pointers to default: "+log_loc[i]+": "+T_val)
				T_stamp_store.close()
				cmd="echo '0' > " + "/var/LPF-client/offsets/"+str(start_string.group(1))+"_offset"
				os.system(cmd)
			else:
				pass
		else:
			log=open("error.log",'a')
			log.write("N-LPF: File does not exist - "+log_loc[i]+"\n")
			log.close()
def chk_status_run(interval, log_loc = []):
	while 1:
		chk_status(log_loc)
		time.sleep(interval)
if __name__=='__main__':
	chk_status_run(['/var/log/syslog','/var/log/auth.log']) 
