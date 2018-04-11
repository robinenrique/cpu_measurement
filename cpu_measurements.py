#!/usr/bin/env/	python
'''
	MODULE TO MEASURE CPU AND MEMORY USAGE STATS AND SEND
	AN EMAIL TO YOUR CHOICE IF THEY ARE TOO HIGH.

	CREATED BY: Robin Gonzalez Valero
'''

import psutil, smtplib
from smtplib import SMTPException
# import psutil for CPU and memory measurements
# import smtplib for sending emails within Python

SENDER = 'serveralert@email.com'
RECEIVER = 'alerts@email.com'

def printCPU(overloadCPU):
	#MESSAGE = "From: CPU Notification Center <serveralert@email.com>
	#To: Alerts <serveralert@email.com>
	#Subject: CPU and Memory Usage are Overloaded
	MESSAGE1_CPU = "Subject: CPU Overloaded\n"
	MESSAGE2_CPU = "The CPU in the production server is currently overloaded at " + str(overloadCPU) + ". \nPlease restart the system to continue.\n\nServer Alert Notifications"

	return MESSAGE1_CPU + MESSAGE2_CPU

def printMemory(overloadMEM):
	MESSAGE1_MEM = "Subject: Memory Overloaded\n"
	MESSAGE2_MEM = "The memories (RAM) in the production server is currently overloaded at " + str(overloadMEM) + ". \nPlease contact your system administrator to proceed accordingly.\n\nServer Alert Notifications"

	return MESSAGE1_MEM + MESSAGE2_MEM

'''
	THIS FUNCTION RETURNS BOTH THE CPU AND MEMORY MEASUREMENT
	ACCORDING TO THE PSUTIL UNIX TOOL. 
'''
def cpuMeasurement():
	cpuUsage = 0						# initialize and reset cpu_counter
	memUsage = 0						# initialize and reset mem_counter
	psutil.cpu_times()
	for x in range(60):					# check cpu_usage every 60 seconds
		cpuUsage += psutil.cpu_percent(interval=1)	# increase the CPU counter every second
		memUsage += memMeasurement()			# increase percentage
	return cpuUsage/60, memUsage/60				# divide memUsage/60 to obtain overall percentage

# mem has the following fields: total, available, percent, used, free, active, inactive   
def memMeasurement():
	usage = 0					# initialize and reset mem_counter
	mem = psutil.virtual_memory()			# obtain mem data structure
	return mem.percent				# return percentage of memory being used

'''
	THIS FUNCTION CONNECTS TO A SMTP CLIENT TO SEND EMAIL
	IF CPU USAGE IS OVER 80% OR MEM_PERCENTAGE IS OVER 80%.
	THE FUNCTION USES THE STANDARD SMTP PROTOCOL TO SEND
	THE EMAIL
'''
def sendMail(overload, indicator):
	try:	
		server = smtplib.SMTP('smtp.gmail.com', 587)		# standard SMTP protocol communication
		server.ehlo()
		server.starttls()
		server.login("your_email@email.com", "password_here")
		if indicator == 1:
			MESSAGE = printCPU(overload)
		elif indicator == 2:
			MESSAGE = printMemory(overload)
		server.sendmail(SENDER, RECEIVER, MESSAGE)		
		print "Successfully sent email"
		server.quit()
	except SMTPException, exc:
		print "mail failed; %s" % str(exc)		

def main():
	cpuUsage, memUsage = cpuMeasurement()
	if cpuUsage >= 80:
		sendMail(cpuUsage, 1)
	elif memUsage >= 95:
		print "HELLO"
		#sendMail(memUsage, 2)				
main()
