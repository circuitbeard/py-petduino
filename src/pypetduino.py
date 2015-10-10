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

import serial

from cmdmessenger import CmdMessenger
from serialmonitor import SerialMonitor

class Petduino(object):

    # Actions
    SET_STATE_ACTION             = 0
    GET_STATE_ACTION             = 1
    SET_LED_ACTION               = 2
    TOGGLE_LED_ACTION            = 3
    GET_LED_ACTION               = 4
    GET_TEMPERATURE_ACTION       = 5
    GET_LIGHT_LEVEL_ACTION       = 6
    SET_DATA_ACTION              = 7

    # Events
    STATE_EVENT                  = 0
    LED_EVENT                    = 1
    TEMPERATURE_EVENT            = 2
    LIGHT_LEVEL_EVENT            = 3
    BUTTON_1_EVENT               = 4
    BUTTON_2_EVENT               = 5

    # Private
    _callbacks = {}

    # Constructor
    def __init__(self, port, baudrate):
        # Initialize the serial / command messenger connection
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=0)
        self.cm = CmdMessenger(self.ser)

        # attach callbacks
        self.cm.attach(self._onUnknownCommand)

        # Start serial monitor
        self.sm = SerialMonitor(self.ser, self.cm)
        self.sm.start()

    def close(self):
        # Stop the serial monitor
        self.sm.stop()

        # Close the command messenger connection
        self.cm.close()

    # Actions
    def setState(self, val):
        self.cm.send_cmd(self.SET_STATE_ACTION, val)

    def getState(self):
        self.cm.send_cmd(self.GET_STATE_ACTION)

    def setLed(self, val):
        self.cm.send_cmd(self.SET_LED_ACTION, val)

    def toggleLed(self):
        self.cm.send_cmd(self.TOGGLE_LED_ACTION)

    def getLed(self, val):
        self.cm.send_cmd(self.GET_LED_ACTION, val)

    def getTemperature(self):
        self.cm.send_cmd(self.GET_TEMPERATURE_ACTION)

    def getLightLevel(self):
        self.cm.send_cmd(self.GET_LIGHT_LEVEL_ACTION)

    def setData(self, val):
        self.cm.send_cmd(self.SET_DATA_ACTION, val)

    # Events
    def _onUnknownCommand(self, received_command, *args, **kwargs):
        print "Command without attached callback received: ", received_command

    def onState(self, callback):
        self._setCallback(callback, self._onIntArgCmd, self.STATE_EVENT)

    def onLed(self, callback):
        self._setCallback(callback, self._onIntArgCmd, self.LED_EVENT)

    def onTemperature(self, callback):
        self._setCallback(callback, self._onFloatArgCmd, self.TEMPERATURE_EVENT)

    def onLightLevel(self, callback):
        self._setCallback(callback, self._onIntArgCmd, self.LIGHT_LEVEL_EVENT)

    def onBtn1(self, callback):
        self._setCallback(callback, self._onBoolArgCmd, self.BUTTON_1_EVENT)

    def onBtn2(self, callback):
        self._setCallback(callback, self._onBoolArgCmd, self.BUTTON_2_EVENT)

    # Private event handlers
    def _onIntArgCmd(self, received_command, *args, **kwargs):
        if received_command in self._callbacks:
            self._callbacks[received_command](int(args[0][0]))

    def _onFloatArgCmd(self, received_command, *args, **kwargs):
        if received_command in self._callbacks:
            self._callbacks[received_command](float(args[0][0]))

    def _onBoolArgCmd(self, received_command, *args, **kwargs):
        if received_command in self._callbacks:
            self._callbacks[received_command](args[0][0] in ['true', '1', 'y'])

    # TODO: Maybe make attach / detach explicit?
    def _setCallback(self, callback, callbackProxy, evt):
        if(callback is None):
            if evt in self._callbacks:
                self.cm.detach(evt)
                self._callbacks.pop(evt)
        else:
            self._callbacks[evt] = callback;
            self.cm.attach(callbackProxy, evt)
    
