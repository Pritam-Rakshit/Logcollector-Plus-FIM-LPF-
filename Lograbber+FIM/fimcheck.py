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
	def comp_fim_compute(self,hashloc_s):
		hasher = hashlib.sha1()
		buf='NULL'			
		with open(r''+str(hashloc_s), 'rb') as afile:
			buf = afile.read()
			hasher.update(buf)
		hashvalue= str(hasher.hexdigest())
		return hashvalue
	def sliced_fim_compute(self,hashloc_l):
		BLOCKSIZE = 524288
		hasher = hashlib.sha1()
		buf='NULL'			
		with open(r''+str(hashloc_l), 'rb') as afile:
			buf = afile.read(BLOCKSIZE)
			while len(buf) > 0:
					hasher.update(buf)
					buf = afile.read(BLOCKSIZE)
		Hashvalue= str(hasher.hexdigest())
		return Hashvalue
	def comp_fim(self):
		for i in range(len(self.fileloc_s)):
			hashloc_s=self.fileloc_s[i].strip()
			hashval=str(self.comp_fim_compute(hashloc_s))
			stat_file=open('fim_db','a+') #read previous hash values
			flag=0 #file entry not found in DB if flag changes to 1
			for line in stat_file:
				if line != '':
					hashcheck=line.split("--")
					pattern=re.search(r''+str(self.fileloc_s[i]),str(hashcheck[0]))
					if pattern: #Check and update hash
						flag=0
						stat_file.close()
						change_log=open("/var/log/fim_alert.log",'a+')
						if hashval != hashcheck[2].strip():
							change_log.write("File integrity changed"+"--"+str(hashcheck[0])+"--"+str(time.asctime(time.localtime(time.time())))+" --NEW Value: "+hashval+" --OLD VALUE: "+str(hashcheck[2]))
							for line in fileinput.FileInput("fim_db",inplace=1):
								sline=line.strip().split("--")
								if sline[0] != '' and line != "\n":
									if sline[0].startswith(str(self.fileloc_s[i])) and sline[2] != hashval:
										sline[2]= hashval
										line=str(sline[0])+"--"+str(time.asctime(time.localtime(time.time())))+"--"+str(sline[2])
										print(line)
									else:
										line=str(sline[0])+"--"+str(sline[1])+"--"+str(sline[2])
										print(line)
								else:
									pass
							change_log.close()
							break
						elif hashval == hashcheck[2]:
							change_log.close()
							break
						else:
							change_log.close()
							break

					else:
						flag=1
				else:
					print("FIM Engine: First entry being made to DB -->"+ (str(self.fileloc_s[i])))
					stat_file.write(str(self.fileloc_s[i])+"--"+str(time.asctime(time.localtime(time.time())))+"--"+hashval+"\n")
					stat_file.close()
					break
			if flag==1:
				print("FIM Engine: New file added to DB -->"+ (str(self.fileloc_s[i])))
				stat_file.write(str(self.fileloc_s[i])+"--"+str(time.asctime(time.localtime(time.time())))+"--"+hashval+"\n")
				flag=0
				stat_file.close()			
			
	def sliced_fim(self):
		for i in range(len(self.fileloc_l)):
			hashloc_l=self.fileloc_l[i].strip()
			hashval=str(self.sliced_fim_compute(hashloc_l))
			stat_file=open('fim_db','a+') #read previous hash values
			flag=0 #file entry not foound in DB if flag changes to 1
			for line in stat_file:
				if line != '':
					hashcheck=line.split("--")
					pattern=re.search(r''+str(self.fileloc_l[i]),str(hashcheck[0]))
					if pattern: #Check and update hash
						flag=0
						stat_file.close()
						change_log=open("/var/log/fim_alert.log",'a+')
						if hashval != hashcheck[2].strip():
							change_log.write("File integrity changed"+"--"+str(hashcheck[0])+"--"+str(time.asctime(time.localtime(time.time())))+" --NEW Value: "+hashval+" --OLD VALUE: "+str(hashcheck[2]))
							for line in fileinput.FileInput("fim_db",inplace=1):
								sline=line.strip().split("--")
								if sline[0] != '' and line != "\n":
									if sline[0].startswith(str(self.fileloc_l[i])) and sline[2] != hashval:
										sline[2]= hashval
										line=str(sline[0])+"--"+str(time.asctime(time.localtime(time.time())))+"--"+str(sline[2])
										print(line)
									else:
										line=str(sline[0])+"--"+str(sline[1])+"--"+str(sline[2])
										print(line)
								else:
									pass
							change_log.close()
							break
						elif hashval == hashcheck[2]:
							change_log.close()
							break
						else:
							change_log.close()
							break

					else:
						flag=1
				else:
					print("FIM Engine: First entry being to DB -->"+ (str(self.fileloc_l[i])))
					stat_file.write(str(self.fileloc_l[i])+"--"+str(time.asctime(time.localtime(time.time())))+"--"+hashval+"\n")
					stat_file.close()
					break
			if flag==1:
				print("FIM Engine: New file adding to DB -->"+ (str(self.fileloc_l[i])))
				stat_file.write(str(self.fileloc_l[i])+"--"+str(time.asctime(time.localtime(time.time())))+"--"+hashval+"\n")
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
		if os.path.isfile('fim_db'):
			cmd='cat fim_db'
			check=os.popen(cmd).read()
			if check == '' or check == '\n':
				os.system('echo > fim_db')
		else:
			pass
		checksum.comp_fim()
		checksum.sliced_fim()
		time.sleep(Interval)

	
		
if __name__=="__main__":
	FimInitiate(12 ,['/var/log/anaconda/journal.log','/etc/passwd','/var/log/audit/audit.log'])
