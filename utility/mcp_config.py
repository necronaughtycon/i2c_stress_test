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
        self.pins = {
            'motor': self._mcp.get_pin(0),
            'v1': self._mcp.get_pin(1),
            'v2': self._mcp.get_pin(2),
            'v5': self._mcp.get_pin(3),
            'shutdown': self._mcp.get_pin(4),
            'tls': self._mcp.get_pin(8),
            'panel_power': self._mcp.get_pin(10)
        }
        self.setup_pins()
        self.cycle_thread = None

    def setup_pins(self):
        ''' Setup the MCP23017 pins. '''
        if self._hardware_initialized:
            for pin in ['motor', 'v1', 'v2', 'v5', 'shutdown']:
                self.pins[pin].direction = Direction.OUTPUT
            for pin in ['tls', 'panel_power']:
                self.pins[pin].direction = Direction.INPUT

    def set_delay(self, delay):
        ''' Set the delay between each cycle. '''
        self.delay = delay

    def set_mode(self, mode):
        ''' Set the pins for the specified mode. '''
        modes = {
            'run': {'motor': True, 'v1': True, 'v2': False, 'v5': True},
            'rest': {'motor': False, 'v1': False, 'v2': False, 'v5': False},
            'purge': {'motor': True, 'v1': False, 'v2': True, 'v5': False},
            'burp': {'motor': False, 'v1': False, 'v2': False, 'v5': True}
        }
        if mode in modes:
            for pin, value in modes[mode].items():
                self.pins[pin].value = value
        else:
            print(f'Invalid mode: {mode}')

    def set_sequence(self, sequence):
        ''' Set the pins for the specified sequence. '''
        for mode in sequence:
            self.set_mode(mode)
            time.sleep(self.delay)

    def thread_sequence(self, sequence):
        ''' Run the specified sequence in a new thread. '''
        self.cycle_thread = threading.Thread(target=self.set_sequence, args=(sequence,))
        self.cycle_thread.start()

    def display_pin_values(self):
        ''' Display the current pin values. '''
        if self.cycle_thread and self.cycle_thread.is_alive():
            while self.cycle_thread.is_alive():
                print('\n')
                for pin, pin_object in self.pins.items():
                    print(f'{pin}: {pin_object.value}')
                time.sleep(self.delay)

    def get_values(self):
        ''' Thread the display_pin_values method. '''
        display_thread = threading.Thread(target=self.display_pin_values)
        display_thread.start()

    def run_cycle(self):
        ''' Set the sequence for a run cycle. '''
        self.thread_sequence(
            ['run', 'rest'] + ['purge', 'burp'] * 6 + ['rest']
        )

    def functionality_test(self):
        ''' Set the sequence for a functionality test. '''
        self.thread_sequence(
            ['run', 'purge'] * 5 + ['rest']
        )