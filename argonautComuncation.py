# Authors: John Purviance and Debarati Basu
# Date: 9/11/14
# LEWAS Lab 
# Near real time Argonaut SW communication and data logging program.

##########
# pySerial python library
import serial 
##########

import sys 
import time 
import datetime
import MySQLdb
  
##########
# Writes a command to the argonaut (except 'start' or 'exit', see their specific functions).
# Also appends '\r', the carriage return command as a pseudo end of transmission command. 
# Finally it checks to see if the command was successfully received and 
# displays the response in the terminal.
# @param command 
#		type: string
#		message to be sent to the device
def comunicate(command):
	argonaut.write(command+'\r')
	unsuccessfulArgWrite(command) 
	readArgonaut()  

##########
# Starts data collection and processing, specifically no data is stored locally on Argonaut.
# Also appends '\r', the carriage return command as a pseudo end of start command. 
# Checks for successfull transmission of start command. 
# If unsucessful log is updated with "ARGONAUT COMMAND FAILED! NO DATA COLLECTION"
# Program terminates after data collection
def start():  
	argonaut.write('start\r')
	#if not unsuccessfulArgWrite('start'):
	seconds=raw_input('Enter the number of seconds (as a non-comma seperated number) for data collection to take place: ')
	#try: 
	goTill=time.time()+int(seconds) # Get the current hour.
	#except Exception as e:
		#sys.stdout.write('\nThat was not formated right format it like this: 36000')
		#seconds=raw_input('\nEnter the number of seconds (as a non-comma seperated number) for data collection to take place: ')
		#goTill=time.time()+int(seconds)
	time.sleep(70) # wait for data to be avalable to be read.
	readBogo() # Ignore insignifficant return data. 
	while time.time()<goTill: # Run until next hour.
		time.sleep(70)
		readStart()
	exit()
	#else:
		# Failed transmission handelling
		#log.write('\nARGONAUT COMMAND FAILED! NO DATA COLLECTION\n')
		#exit()

#########
# Deligates actions for 'start', 'exit' and all other commands.
def control():
	sys.stdout.write('\nEnter a command\n')
	command=raw_input('Command: ') 

	# Run until 'exit', preform start() if command is 'start'
	while(command!='exit'):
		if command=='start':
			start()
		else:
			comunicate(command)
			command=raw_input('\nCommand: ')
	exit()


########################################################333
class Cell:
	def __init__(self, dataLine):
		self.dataPoints=dataLine.split()
		self.cellNum=self.dataPoints[0]

##########
# Prosses output of Argonaut. Parses average data diffrent from cell data.
# Writes data to the log file. 
# Terminates program if data cannot be parsed. 
def readStart():
	for line in argonaut:
		year=time.strftime("%Y") # current year
		try:

			# Handels dates for this year and last (data collected last year).
			if (line[0:4]==str(year)) or (line[0:4]==str(int(year)-1)): 
				averageDataWrite(line)
			else:

				# Parses data for each cell. 
				#log.write('\nCell number: '+line[0:2]+' Velocity X: '+line[3:9]+' Velocity Y: '+line[10:16]+'\n')
				#log.write('Standard error X: '+line[17:20]+' Standard error Y: '+line[21:24]+'\n') 

###################################################################
				cell=Cell(line)
				sql="INSERT INTO CELL"+str(cell.cellNum)+"(XVelocity, YVelocity, STDerrorX, STDerrorY, Beam1strength, Beam2strength) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"%(cell.dataPoints[1], cell.dataPoints[2], cell.dataPoints[3], cell.dataPoints[4], cell.dataPoints[5], cell.dataPoints[6])
				cursor.execute(sql)
				db.commit()
#####################################################################

		# Data parssing error handeling.
		except Exception as e:
			log.write('\nERROR IN PARSING DATA\n')
			argonaut.close()
			sys.exit("Error in prossesing or writing data.")

#########
# Ignores lines of text formt the Argonaut that are not data. 
# Functioning but still under devlopment.
# Does not yet handel hardware errors yet, only software.
def readBogo():
	for line in argonaut:
		year=time.strftime("%Y")
		try:

			# Handels dates for this year and last (data collected last year).
			if (line[0:4]==str(year)) or (line[0:4]==str(int(year)-1)):
				averageDataWrite(line)
				break
			else:
				{
					# Ignore lines that are not data. 
				}

		# Data parssing error handeling.
		except Exception as e:
			log.write('\nERROR IN PARSING DATA\n')
			argonsaut.close()
			sys.exit("Error in prossesing or writing data.")

##########
# Read line character by line character from Argonaut.
# Ignores new command promt
def readArgonaut():
	for line in argonaut:
		if line[0]!='>':
			sys.stdout.write(line)
		else:
			{
				# ignore lines with the '>' prompt.
			}
##########
# Terminates program and ends comunication with Argonaut.
# If current Argonaut actions cannot be stoped log file is updated with Argonaut command fail.
def exit():

	# Send 'stop' or enter command mode message. Not to be confused with comunicate() or control().
	argonaut.sendBreak(800)
	# normal file clean up. 
	log.write('\nEND OF DATA COLLECTION\n')
	argonaut.close()
	log.close()
	sys.exit("Argonaut Closed")


#################################################################
class Average:
	def __init__(self, dataLine):
		self.data=dataLine.split()
		self.year=self.data[0]
		self.month=self.data[1]
		self.day=self.data[2]
		self.hour=self.data[3]
		self.min=self.data[4]
		self.sec=self.data[5]
		self.begin=self.data[26]
		sefl.end=self.data[27]
######################################################################

##########
# Parse text data for the minute average.
# @param data 
#		type: string
#		data to be parsed
def averageDataWrite(data):
	#log.write('\nYear: '+data[0:4]+' Month: '+data[5:7]+' Day: '+data[8:10]+' Hour '+data[11:13]+' Minute: '+data[14:16]+' Second: '+data[17:19]+'\n')
	#log.write('Velocity X: '+data[20:26]+' Velocity Y: '+data[27:33]+' Water Level: '+data[34:40]+'\n')
	#log.write('Standard error x: '+data[41:44]+' Standard error y: '+data[45:48]+' Standard error water level: '+data[49:52]+'\n')
	#log.write('Heading: '+data[69:73]+' Pitch: '+data[74:77]+ ' Roll: '+data[78:81]+'\n')
	#log.write('Mean Temperature: '+data[94:100]+' Input voltage: '+data[118:121]+' Starting water depth: '+data[122:125]+' Ending water depth: '+data[126:130]+'\n')

	#sql="INSERT INTO ArgAVG"

##########
# Checks serial transmission echos for succesfull or failed transmissions of commands.
# Cleans up0 and terminates program if failed transmission.  
# @param message 
#		type: string
#		message to look for.
#@ return bollean
# 		type boolean
#		returns true for failed transmission, false for all others. 
def unsuccessfulArgWrite(message):
	recived=argonaut.readline()
	#for char in recived:
		#log.write(char)
	# removes newline and carraige return characters and looks for the message in the Argonaut response. 
	if message!=recived[:-2]:
		sys.stdout.write(recived)
		# filed transmission
		argonaut.write('+++\r')
		argonaut.close()
		argonaut.open()
		sys.stdout.write("Argonaut command failed!")
		return True
	else:

		# succseful transmission.
		return False


##########
# Starts program, not done yet.
with open("test.log", 'a' , buffering=1) as log:
	argonaut=serial.Serial('/dev/Blue')  
	argonaut.parity=serial.PARITY_NONE 
	argonaut.bytesize=serial.EIGHTBITS 
	argonaut.stopbits=serial.STOPBITS_ONE 
	argonaut.timeout=2
	argonaut.sendBreak(800)  
	
	##internal local database connection settings
	db=MySQLdb.coonect("localhost", "root", "mysql", "LEWAS")
	cursor=db.cursor()


	readArgonaut()
	control()

# needs to hadel opening and closing of the log.