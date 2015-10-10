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

import time

from pypetduino import Petduino

# Declare event handlers
def onState(val):
    print "Petduino state: ", val

def onLed(val):
    print "Petduino LED: ", val

def onBtn1(val):
    print "Petduino BTN1: ", val
    if val:
        pet.setState(1)

def onBtn2(val):
    print "Petduino BTN2: ", val

# Declare min process
if __name__ == '__main__':

    # Open connection to petduino
    pet =  Petduino("COM16", 9600)

    # Hookup event handlers
    pet.onState(onState)
    pet.onLed(onLed)
    pet.onBtn1(onBtn1)
    pet.onBtn2(onBtn2)

    try:
        print 'Press Ctrl+C to exit...'
        while True:
            # Do stuff
            pet.toggleLed()
            time.sleep(1)
            pet.getTemperature()
            time.sleep(1)

    except KeyboardInterrupt:
        # Stop procesing
        print 'Exiting...'
        pet.close()