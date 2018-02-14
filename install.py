#!/usr/bin/python
import os
import re
import sys
import py_compile

def inputs():
	choice = input("Select the module to be installed: \n 1. LPF-server (Enter 1) \n 2. LPF-client (Enter 2) \n :")
	if choice == 1:
		print "N-LPF: Server module selected....."
		dir = raw_input("Do you want us to install server @ --> /var/LPF-server? \n This may modify the directory content if it already exists. \n Enter yes or no: ")
		if dir == "yes" or dir == 'y':
			os.system("mkdir /var/LPF-server")
			chk=build_conf(choice)
			if chk == 1:
				print "N-LPF: Copying  files to location....."
				os.system("cp LPF-server/*.pyc /var/LPF-server")
				os.system("mkdir /var/LPF-server/Client-gen")
				os.system("mkdir /var/LPF-server/LPF-data")
				os.system("mkdir /var/LPF-server/Received-logs")
				print "Done"
		else:
			print "Permission not granted....exiting!!!"
	elif choice == 2:
		print "N-LPF: Client module selected....."
		dir = raw_input("Do you want us to install server @ --> /var/LPF-client? \n This may modify the directory content if it already exists. \n Enter yes or no:")
		if dir == "yes" or dir =='y':
			os.system("mkdir /var/LPF-client")
			chk=build_conf(choice)
			if chk == 1:
				print "N-LPF: Copying  files to location....."
				os.system("cp LPF-client/*.pyc /var/LPF-client")
				os.system("mkdir /var/LPF-client/keystore")
				os.system("mkdir /var/LPF-client/offsets")
				os.system("mkdir /var/LPF-client/T_stamp_dir")
				print "Done"
		else:
			print "Permission not granted....exiting!!!"


def build_conf(choice):
	if choice == 1:
		configs = open('/var/LPF-server/NLPF-server.conf','w')
		configs.write('###----------Netra LPF v1.1----------###\n')
		server_ip = raw_input("Enter server IP {default: 0.0.0.0}:")
		match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",server_ip)
		if match:
			configs.write("server-ip="+server_ip+"\n")
		else:
			print "Wrong IP format. Setting default value \'0.0.0.0\' in config"
			config.write("server-ip=0.0.0.0\n")
		configs.write("\n#TCP logging feature yet to be added \n")
		configs.write("#protocol=udp/tcp \n")
		configs.close()
		try:
			print "N-LPF: compiling modules...."
			py_compile.compile('LPF-server/netra-server-start.py')
			py_compile.compile('LPF-server/netra-service-stop.py')
			py_compile.compile('LPF-server/status_check.py')
			py_compile.compile('LPF-server/delist_client.py')
			py_compile.compile('LPF-server/DataReceiveUDP.py')
			py_compile.compile('LPF-server/DHKE_SERV.py')
			py_compile.compile('LPF-server/Agent_registry.py')
			py_compile.compile('LPF-server/DataReceiveUDP.py')
			return 1
		except:
			print "Error: File or folder not found --> install.py and directory \'LPF-server\' should be in same folder."
			return 0
			
	elif choice == 2:
		configs = open('/var/LPF-client/NLPF-client.conf','w')
		configs.write('###----------Netra LPF v1.1----------###\n')
		server_ip = raw_input("Enter server IP {default: 127.0.0.1}:")
		match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",server_ip)
		if match:
			configs.write("server-ip="+server_ip+"\n")
		else:
			print "Wrong IP format. Setting default value \'127.0.0.1\' in config. Makes correct entry in file --> /var/LPF-client/NLPF-client.conf"
			configs.write("server-ip=127.0.0.1\n")
		
		os_type = input("Select the Operating system to set default log tracking locations: \n 1. CentOS/RedHat/Fedora (Enter 1) \n 2. Ubuntu/Debian (Enter 2) \n 3. Other Linux/Unix\n :")
		configs.write("\n\n#input log file locations, sample -- location=/var/log/syslog,/var/log/maillog\n")
		
		if os_type == 1:
			configs.write("location=/var/log/messages,/var/log/secure,/var/log/fim_alert.log\n")
		elif os_type == 2:
			configs.write("location=/var/log/syslog,/var/log/faillog,/var/log/fim_alert.log,/var/log/auth.log\n")
		elif os_type == 3:
			locations = raw_input("Enter system log file locations , \n Example: /var/log/maillog,/var/log/syslog \n :")
			configs.write("location=/var/log/fim_alert.log,"+locations+"\n")
		else:
			print "Wrong input"
			sys.exit()
		configs.write("\n#FIM file locations\n")
		configs.write("FIMloc=/etc/passwd,/etc/shadow,/etc/sudoers\n")
		configs.write("Interval=300\n")
		configs.write("\n#Data Encryption options -- on/off\n")
		encryption = raw_input("Do you want to send logs encrypted to the LPF-server? \n This takes extra CPU cycle \n Enter yes or no?")
		if encryption == 'yes' or encryption == 'y':
			configs.write("Encryption=on\n")
		else:
			configs.write("Encryption=off\n")
		
		configs.write("\n#Agent-IP : IP of interface through which logs should pass\n")
		server_ip = raw_input("Enter local system IP {default: 127.0.0.1}:")
		match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",server_ip)
		if match:
			configs.write("agent-ip="+server_ip+"\n")
		else:
			print "Wrong IP format. Setting default value \'127.0.0.1\' in config. Makes correct entry in file --> /var/LPF-client/NLPF-client.conf"
			configs.write("agent-ip=127.0.0.1\n")
		configs.close()
		try:
			print "N-LPF: compiling modules...."
			py_compile.compile('LPF-client/delist.py')
			py_compile.compile('LPF-client/Agent_reg.py')
			py_compile.compile('LPF-client/chk_rotate.py')
			py_compile.compile('LPF-client/DataSendUDP.py')
			py_compile.compile('LPF-client/DHKE_CLI.py')
			py_compile.compile('LPF-client/fimcheck_final.py')
			py_compile.compile('LPF-client/KeepAlive.py')
			py_compile.compile('LPF-client/DynamicRead.py')
			py_compile.compile('LPF-client/netra-service-start.py')
			py_compile.compile('LPF-client/netra-service-stop.py')
			return 1
		except:
			print "Error: File or folder not found --> install.py and directory \'LPF-server\' should be in same folder."
			return 0
inputs()

