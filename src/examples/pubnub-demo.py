#!/usr/bin/python
# Copyright (c) 2015, Matt Brailsford, aka Circuitbeard <hi@circuitveard.co.uk>   
#  
# Permission to use, copy, modify, and/or distribute this software for  
# any purpose with or without fee is hereby granted, provided that the  
# above copyright notice and this permission notice appear in all copies.  
#  
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL  
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED  
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR  
# BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES  
# OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,  
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,  
# ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS  
# SOFTWARE. 

# Add parent directory to sys path to allow importing
# modules from parent directory
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import time, threading

from pypetduino import Petduino
from pubnub import Pubnub

# Petduino settings
pet_connected = False
pet_port = "/dev/ttyUSB0"
pet_baud_rate = 9600

# Pubnub settings
pn_connected = False
pn_channel = ""
pn_publish_key = ""
pn_subscribe_key = ""

# Declare event handlers
def onState(val):
	print "Petduino State: ", val
	if(pn_connected):
		pn.publish(channel=pn_channel, message={"type":"event", "name":"state", "value":val})

def onLed(val):
	print "Petduino Led: ", val
	if(pn_connected):
		pn.publish(channel=pn_channel, message={"type":"event", "name":"led", "value":val})

def onTemperature(val):
	print "Petduino Temperature: ", val
	if(pn_connected):
		pn.publish(channel=pn_channel, message={"type":"event", "name":"temperature", "value":val})

def onLightLevel(val):
	print "Petduino Light Level: ", val
	if(pn_connected):
		pn.publish(channel=pn_channel, message={"type":"event", "name":"lightLevel", "value":val})

def onBtn1(val):
	print "Petduino Btn1: ", val
	if(pn_connected):
		pn.publish(channel=pn_channel, message={"type":"event", "name":"btn1", "value":val})

def onBtn2(val):
	print "Petduino Btn1: ", val
	if(pn_connected):
		pn.publish(channel=pn_channel, message={"type":"event", "name":"btn2", "value":val})

def onPubnubMessage(data, channel):
	if(pet_connected):
		if channel == pn_channel:
			print data
			if "type" in data and  data["type"] == "action":
				if data["name"] == "setState":
					pet.setState(data["value"])		
				elif data["name"] == "getState":
					pet.getState()
				elif data["name"] == "setLed":
					pet.setLed(data["value"])
				elif data["name"] == "toggleLed":
					pet.toggleLed()
				elif data["name"] == "getLed":
					pet.getLed()
				elif data["name"] == "getTemperature":
					pet.getTemperature()
				elif data["name"] == "getLightLevel":
					pet.getLightLevel()
				elif data["name"] == "setData":
					pet.setData(data["value"])

def connectPetduino():
	global pet_connected, pet
 	try:
		pet = Petduino(pet_port, pet_baud_rate)

		# Hookup event handlers
		pet.onState(onState)
		pet.onLed(onLed)
		pet.onTemperature(onTemperature)
		pet.onLightLevel(onLightLevel)
		pet.onBtn1(onBtn1)
		pet.onBtn2(onBtn2)	

		# Flag initialized
		print "Connected to Petduino on port:", pet_port
		pet_connected = True

	except Exception, e:
		print "Unable to connect to Petduino, retrying..."
		time.sleep(5)
		connectPetduino()

def connectPubnub():
	global pn_connected, pn
 	try:
		# Setup pubnub channel
		pn = Pubnub(publish_key=pn_publish_key, subscribe_key=pn_subscribe_key)

		# Setup pubunb listener
		pn.subscribe(channels=pn_channel, callback=onPubnubMessage)

		# Flag initialized
		print "Connected to Pubnub channel:", pn_channel
		pn_connected = True

	except Exception, e:
		print "Unable to connect to Pubnub, retrying..."
		time.sleep(5)
		connectPubnub()

def killAllThreads():
    for thread in threading.enumerate():
        if thread.isAlive():
            thread._Thread__stop()

# Declare min process
if __name__ == '__main__':

	# Start processes
	connectPubnub()
	connectPetduino()

	# Wait for keyboard interrupt
	try:
		print "Running..."
		while True:
			time.sleep(0)

	except KeyboardInterrupt:
		print 'Exiting...'

		if(pet_connected):
			pet.close()

		if(pn_connected):
			pn.unsubscribe(channel=pn_channel)

		killAllThreads()
