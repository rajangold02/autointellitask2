import os
import time
import sys
import pandas as pd
import paramiko
from pypsexec.client import Client

# Read data from csv 
data = pd.read_csv("demo.csv", sep = "\t")

for index,row in data.iterrows():
	host = row["Hostname"]
	username = row["Username"]
	password = row["password"]
	try:
		#Windows Login
		c = Client(host, username=username, password=password, encrypt=False, port=3389)
		c.connect()
		try:
			stdout = c.run_executable("cmd.exe", arguments="systeminfo")
		finally:
			c.disconnect()
		output = []
		output = stdout[0].decode("utf-8")
		print(output.split("\r\n")[1:3])
	except:
	
		#Linux Login
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname=host, username=username, password=password)
		shell = ssh.invoke_shell()
		stdin,stdout,stderr = ssh.exec_command('lsblk | grep vda && vmstat' )
		print (stdout.readlines())
	finally:	
		ssh.close()
		