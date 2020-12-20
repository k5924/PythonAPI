import paramiko
import getpass
import socket
import os
import time
import scp

os.system("clear")
# command to clear screen

host = input('Enter the IP of the remote machine: ')
port = 22
username = input("Enter the username for the remote machine: ")
password = getpass.getpass()
# variables to store host, port, username and password

try:
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(host, port, username, password)
	# connect to target machine via SSH

	while True:
		print("Scripts in Current Directory: ")
		for line in os.popen("ls *.sh").readlines():
			print(line)
		# prints list of all script files from the current directory on manager vm

		command = input("> ")
		start_time = time.time()
		# store start time when command is executed

		if (command.lower() == "quit") or (command.lower() == "exit"):
			break
			# close program if command entered equals quit or exit
		else:
			file = scp.SCPClient(ssh.get_transport())
			values = command.split(" ")
			# splits the command on every space

			file.put(f"{values[0]}", ".")
			# copies script by name from manager to worker vm

			stdin, stdout, stderr = ssh.exec_command(f"sh ./{command}")
			# runs scripts from manager vm to worker vm

			if stdout:
				for line in stdout.readlines():
					print(line)
				# prints output of running script
			if stderr:
				for line in stderr.readlines():
					print(line)
				# prints errors while running the script

			print(f"Task took {time.time() - start_time} seconds to execute\n")
			# prints total time to execute each command/task

			stdin, stdout, stderr = ssh.exec_command(f"rm {values[0]}")
			# deletes copied script from worker vm

except paramiko.ssh_exception.NoValidConnectionsError:
	print(f"Couldn't find machine with IP: {host}")
	# print error if can't find IP at specified host address

except TimeoutError:
	print("Connection timed out, please recheck the connection details you provided")
	# print error if connection times out

except socket.gaierror:
	print(f"IP: {host} is not in the correct format")
	# print error if IP entered isnt in the correct format

except paramiko.ssh_exception.AuthenticationException:
	print(f"Authentication failed for IP: {host}")
	# print error if username or password entered is incorrect

except FileNotFoundError:
	print("Script doesnt exist, please enter a valid script")
	# print error is script entered isnt found
