#/usr/bin/python
import hashlib
import os
import time
import re
import fileinput


class fimcheck:
	def __init__(self, fileloc_s = [], fileloc_l= []):
		self.fileloc_s = fileloc_s
		self.fileloc_l = fileloc_l
	def comp_fim(self):
		hasher = hashlib.sha1()
		for i in range(len(self.fileloc_s)):			
			with open(r''+str(self.fileloc_s[i]), 'rb') as afile:
				buf = afile.read()
				hasher.update(buf)
			stat_file=open('fim_db','a+') #read previous hash values
			flag=0 #file entry not found in DB if flag changes to 1
			cflag=0 #cflag=0
			for line in stat_file:
				#print "sds"+line
				if line != '':
					find=line.split("--")
					pattern=re.search(r''+str(self.fileloc_s[i]),str(find[0]))
					if pattern: #Check and update hash
						change_log=open("/var/log/fim_alert.log",'a+')
						flag=0
						stat_file.close()
						for line in fileinput.FileInput("fim_db",inplace=1):
							sline=line.strip().split("--")
							if sline[0] != '' and line != "\n":#if fileinput faces unwanted input
								if sline[0].startswith(str(self.fileloc_s[i])) and sline[2] != str(hasher.hexdigest()):
									change_log.write("File integrity changed"+"--"+str(sline[0])+"--"+str(time.asctime(time.localtime(time.time())))+" --NEW Value: "+str(hasher.hexdigest())+" --OLD VALUE: "+str(sline[2])+"\n")
									sline[2]= str(hasher.hexdigest())
									line=str(sline[0])+"--"+str(time.asctime(time.localtime(time.time())))+"--"+str(sline[2])
									print(line)
								else:
									line=str(sline[0])+"--"+str(sline[1])+"--"+str(sline[2])
									print(line)
							else:
								pass
						change_log.close()
						break
					else:
						flag=1
				else:
					stat_file=open('fim_db','a+')
					stat_file.write(str(self.fileloc_s[i])+"--"+str(time.asctime(time.localtime(time.time())))+"--"+str(hasher.hexdigest())+"\n")
					stat_file.close()
					break


			if flag==1:
				stat_file=open('fim_db','a+')
				stat_file.write(str(self.fileloc_s[i])+"--"+str(time.asctime(time.localtime(time.time())))+"--"+str(hasher.hexdigest())+"\n")
				flag=0
				stat_file.close()			
			
	def sliced_fim(self):
		BLOCKSIZE = 524288
		hasher = hashlib.sha1()
		for i in range(len(self.fileloc_l)):
			with open(r''+str(self.fileloc_l[i]), 'rb') as afile:
				buf = afile.read(BLOCKSIZE)
				while len(buf) > 0:
					hasher.update(buf)
					buf = afile.read(BLOCKSIZE)
            #print buf
			#print(str(self.fileloc_l[i])+"--"+str(time.asctime(time.localtime(time.time())))+"--"+str(hasher.hexdigest())+"\n")
			stat_file=open('fim_db','a+') #read previous hash values
			flag=0 #file entry not foound in DB if flag changes to 1
			for line in stat_file:
				#print "sds"+line
				if line != '':
					find=line.split("--")
					pattern=re.search(r''+str(self.fileloc_l[i]),str(find[0]))
					if pattern: #Check and update hash
						change_log=open("fim_alert.log",'a+')
						flag=0
						stat_file.close()
						for line in fileinput.FileInput("fim_db",inplace=1):
							sline=line.strip().split("--")
							if sline[0] != '' and line != '\n':#if fileinput faces unwanted input
								if sline[0].startswith(str(self.fileloc_l[i])) and sline[2] != str(hasher.hexdigest()):
									change_log.write("File integrity changed"+"--"+str(sline[0])+"--"+str(time.asctime(time.localtime(time.time())))+" --NEW Value: "+str(hasher.hexdigest())+" --OLD VALUE: "+str(sline[2])+"\n")
									sline[2]= str(hasher.hexdigest())
									line=str(sline[0])+"--"+str(sline[1])+"--"+str(sline[2])
									print(line)
								else:
									line=str(sline[0])+"--"+str(sline[1])+"--"+str(sline[2])
									print(line)
							else:
								pass
						change_log.close()
						break
					else:
						flag=1
				else:
					stat_file=open('fim_db','a+')
					stat_file.write(str(self.fileloc_l[i])+"--"+str(time.asctime(time.localtime(time.time())))+"--"+str(hasher.hexdigest())+"\n")
					stat_file.close()
					#break


			if flag==1:
				stat_file=open('fim_db','a+')
				stat_file.write(str(self.fileloc_l[i])+"--"+str(time.asctime(time.localtime(time.time())))+"--"+str(hasher.hexdigest())+"\n")
				flag=0
				stat_file.close()			

def FimInitiate(Interval, fimlocs = []):
	i=len(fimlocs)
	fimloc_s=[]
	fimloc_l=[]
	while i > 0:
		size=os.path.getsize(fimlocs[i-1])
		if size <= 52488: #Files lesser that 512KB will be done in one shot
			fimloc_s.append(fimlocs[i-1])
		elif size > 52488:
			fimloc_l.append(fimlocs[i-1])
		i=i-1		
	checksum = fimcheck(fimloc_s,fimloc_l)
	i= 'True'
	while i=='True':
		cmd='cat fim_db'
		check=os.popen(cmd).read()
		if check == '' or check == '\n':
			os.system('echo > fim_db')
		checksum.comp_fim()
		checksum.sliced_fim()
		time.sleep(Interval)

	
		
if __name__=="__main__":
	FimInitiate(6 ,['/etc/openvpn/prakshit.conf','/etc/apache2/apache2.conf','/var/log/cchids.log'])
	
	
#Built by - Pritam Rakhit - 2017
