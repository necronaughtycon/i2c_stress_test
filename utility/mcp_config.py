#!/usr/bin/env python3

'''
====================================
                MCP
====================================
'''

import threading
import time
try:
    import board
    import busio
    from digitalio import Direction
    from adafruit_mcp230xx.mcp23017 import MCP23017
except (ImportError, NotImplementedError):
    busio = None
    board = None
    MCP23017 = None


class MCP:
    '''
    This class is used to interface with the MCP23017 I/O Expander.
    '''

    def __init__(self):
        self.delay = None
        self._hardware_initialized = False
        if busio is None or board is None or MCP23017 is None:
            return
        i2c = busio.I2C(board.SCL, board.SDA)
        self._mcp = MCP23017(i2c)
        self._hardware_initialized = True
        self.motor = self._mcp.get_pin(0)
        self.v1 = self._mcp.get_pin(1)
        self.v2 = self._mcp.get_pin(2)
        self.v5 = self._mcp.get_pin(3)
        self.shutdown = self._mcp.get_pin(4)
        self.tls = self._mcp.get_pin(8)
        self.panel_power = self._mcp.get_pin(10)
        self.setup_pins()

    def setup_pins(self):
        ''' Setup the MCP23017 pins. '''
        if self._hardware_initialized:
            self.motor.direction = Direction.OUTPUT
            self.v1.direction = Direction.OUTPUT
            self.v2.direction = Direction.OUTPUT
            self.v5.direction = Direction.OUTPUT
            self.shutdown.direction = Direction.OUTPUT
            self.tls.direction = Direction.INPUT
            self.panel_power.direction = Direction.INPUT

    def set_delay(self, delay):
        ''' Set the delay between each cycle. '''
        self.delay = delay

    def relay_on(self, relay):
        ''' Turn on the specified relay. '''
        relay.value = True

    def relay_off(self, relay):
        ''' Turn off the specified relay. '''
        relay.value = False

    def run(self):
        ''' Set the pins for run mode. '''
        self.relay_on(self.motor)
        self.relay_on(self.v1)
        self.relay_off(self.v2)
        self.relay_on(self.v5)

    def rest(self):
        ''' Set the pins for rest mode. '''
        self.relay_off(self.motor)
        self.relay_off(self.v1)
        self.relay_off(self.v2)
        self.relay_off(self.v5)

    def purge(self):
        ''' Set the pins for purge mode. '''
        self.relay_on(self.motor)
        self.relay_off(self.v1)
        self.relay_on(self.v2)
        self.relay_off(self.v5)

    def burp(self):
        ''' Set the pins for burp mode. '''
        self.relay_off(self.motor)
        self.relay_off(self.v1)
        self.relay_off(self.v2)
        self.relay_on(self.v5)

    def set_sequence(self, sequence):
        ''' Set the pins for the specified sequence. '''
        for mode in sequence:
            if hasattr(self, mode):
                getattr(self, mode)()
                time.sleep(self.delay)
            else:
                print(f'Invalid mode: {mode}')