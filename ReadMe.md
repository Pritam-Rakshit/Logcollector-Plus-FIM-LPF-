          =============================Netra LPF: Logcollector Plus FIM v1.1=========================

Hi, This tool is meant to do log collection at a centralized location and also to perform FIM(File Integrity monitoring) check over a number of specified files. It will work on Linux/Unix systems that supports Python 2.6 or above with pyCrypto module installed. Salient features of the tool are as follows:

1) On demand log encryption - Encrypt syslog events on the go while sending events to remote centralized logcollector.
2) Reliable FIM engine - Trigger alert logs on file integrity change and send it to the centralized server for better analysis.
3) Multiprocessing/Multithreading - Better use of multiprocessing and multithreading modules available with Python to distribute load accross the processing units.
4) It's easy to set it up.

How to set it up?

1) Python 2.6.x or 2.7.x should be configured with pyCrypto module where the tool is intended to be used. Please note without pyCrypto you will not be able to use the log encryption feature.
   To install pyCrypto you can use 'pip'. Command: 'pip install pycrypto'
   You may need to install 'build essentials' packages and python-dev packages before using pip module - 'apt-get install python-dev'.
   
2) LPF-server module (i.e. Logcollector):

This module should be configured on a box that is intended to be used as a storage server for the logs and FIM alerts. The box should be a Linux system. Ubuntu/Debian systems are recommended to be used as a logcollector VM in this case. 

Tested on: Ubuntu, Debian and CentOS
	
	Steps:
	a) Run the installer (install.py) , select option 1 to install the LPF-server:
		command: # python install.py
			 Select the module to be installed:
 			  1. LPF-server (Enter 1)
 			  2. LPF-client (Enter 2)
 			  :1		

	b) Follow the onscreen instructions and provide the server IP & other details. Once done the packages will be compiled and placed in "/var/LPF-server" directory. To start the server use below command: 
		 Command: # python /var/LPF-server/netra-server-start.pyc &
					Or,
			  # /usr/bin/python  /var/LPF-server/netra-server-start.pyc &
			  N-LPF: Starting LPF server.....
			  N-LPF: Listening for incoming syslog events........
			  N-LPF: Waiting to receive request from client....

		Voila! your logcollector module should be started if python(with pyCrypto) is there. You will see onscreen messages saying the server has started.

	c) Received logs will be written to a file in the directory "/var/LPF-server/Received-logs"  in format 'Events-dd-mm-yyyy.log'. Log files will be created on a daily basis so that one can better keep track of logs and gzip them when required.
	
3) LPF-client (i.e. Lograbber+FIM module module):
	
This module is to be configured on the servers where you want to run the FIM service and grab logs from them for safe keeping or analysis. This module has been tested on Ubuntu, Debian and CentOS.

	Steps:
	
	**Open the below firewall rules for the client to communicate with the server:
			Client_IP:Any --> Server_IP:8888 (UDP - for incoming logs)
			Client_IP:any <-- --> Server_IP:8844 (TCP -  for key negotiation)
			
	a) Run the installer (install.py) , select option 2 to install the LPF-client:
		command: # python install.py
			 Select the module to be installed:
 			  1. LPF-server (Enter 1)
 			  2. LPF-client (Enter 2)
 			  :2
	b) Set the input parameters like server-ip, agent-ip, operating system type during installation. Once done, the setup will place the complied files at "/var/LPF-client" and build a client config for you. Open the 'NLPF-client.conf' file unsing a text editor like 'vi', 'nano' or 'gedit' and do a walkthrough for understanding the configs.
	
		**First entry is the 'server-ip' where you will enter the IP of the system where the Logcollector (Server module) is running.
		e.g., say the Logcollector is running on IP 192.168.1.33 then the entry will be --> server-ip=192.168.1.33

		**Second entry will be of the log file locations you want to track i.e. location of the logs to be sent to the server.
		e.g., for an ubuntu system the entries will be as stated below
			  location=/var/log/fim_alert.log,/var/log/syslog,/var/log/auth.log

		Note: /var/log/fim_alert.log is the file where the FIM alerts are stored. Any new addition to the file should be sent to the centralized server.
		
		**Third entry will be of the locations of the files over which you would like to do FIM. Generally, these are meant to be config files like apache2.conf, nginx.conf or other static system files over which only priviledged users can make changes. Keeping a track on these files can help us keep track of any mischievious entries or tampering with access rights.
		e.g.,
		FIMloc=/etc/passwd,/etc/shadow,/etc/sudoers
		Interval=300

		**Enable or disable data encryption options. Make sure port 8844 of the Server is reachable from your client system. The client will try to negotitate key with the server once the option is set to 'on'.
		e.g.,
		#Data Encryption options -- on/off
		Encryption=off

		**Provide the IP of the agent from where logs are to be sent
		e.g.,
		#Agent-IP : IP of interface through which logs should pass
		agent-ip=192.168.1.63
		
	c) Start the client service using 'netra-service-start.pyc' if everything is done correctly you will see your system logs pouring into your server side(/var/LPF-server/Receuved-logs) at server side in this case). Keep track of error logs in case of any error.
	
		 Command: # python /var/LPF-client/netra-service-start.pyc &


	d) Use 'netra-service-stop.pyc' to stop all the LPF services.
	Command: # python /var/LPF-client/netra-service-stop.pyc 
				or
		 # python /var/LPF-server/netra-service-stop.pyc
	
This is an underdevelopment project with futher modifications to be added in near future. Kindly do a proper testing before brining any of these into a production environment. 

###Built by Pritam Rakshit, SOC 
###Supported by Rahul Arya, IT Infra and Gautam Rakshit, .Net Developer###
