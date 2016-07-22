#!/usr/bin/env python
import Adafruit_GPIO.I2C as i2c#Imports adafruit library for sensors
import requests # imports web library
from time import sleep, time # Imports time and sleep


requests.packages.urllib3.disable_warnings() # handles warnings from requests

address = 0x27 # Device Address
try:
	device = i2c.get_i2c_device(address)# get device address
	print('PI Temperature Sensor Running')
	while True:
		try:
			read_results = device.readList(0,4)#read results
			temp = (64.0*int(read_results[2])+int(read_results[3])/4)/(2**14-1)*165-40#Converts temp to C
			hum = ((256.0*int(read_results[0])+int(read_results[1]))/(2**14-1)%1)*100# Gets humindity 
			#url = "http://178.62.91.44:3001/sensor/1?temp_value="+str(temp)+"&hum_value="+str(hum)+"&time="+str(int(time()))#declare uri template and format
			url = "http://178.62.91.44:30002/sensor/1?value="+str(temp)+"&time="+str(int(time()))
			r = requests.put(url,verify=False)#sends data to server via requests
			print ('Sending Temp: ' + '%.2f'%round(temp,2)) #prints temp
			sleep(60)#Update EveryMinute
			#if r.status_code == 200:
			#	print ('Success')
		except:
			print('An Error Sending data has occurred, Check Server, Trying again in 30 seconds')
			sleep(30)
except:
	print("An Error Has Occured With the Sensor Configuration")
	
	
