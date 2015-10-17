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

import time

from pypetduino import Petduino

# Petduino settings
pet_port = "/dev/ttyUSB0"
pet_baud_rate = 9600

# Declare event handlers
def onLed(val):
    print "Petduino Led: ", val

# Declare min process
if __name__ == '__main__':

    # Open connection to petduino
    pet =  Petduino(pet_port, pet_baud_rate)

    # Hookup event handlers
    pet.onLed(onLed)

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