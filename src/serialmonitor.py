#!/usr/bin/python
# Copyright (c) 2015, Matt Brailsford, aka Circuitbeard <hi@circuitveard.co.uk> 
#
# Adapted from code by Adrien Emery <https://github.com/adrienemery>
# -- (https://github.com/Davideddu/python-cmdmessenger/issues/2#issuecomment-147005194)
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

from threading import Thread

class SerialMonitor(Thread):

    def __init__(self, serial_object, cmd_messenger):
        super(SerialMonitor, self).__init__()
        self.is_running = False
        self.serial_object = serial_object
        self.cmd_messenger = cmd_messenger

    def stop(self):
        self.is_running = False

    def run(self):
        self.is_running = True
        while(self.is_running):
            self.cmd_messenger.feed_in_data()