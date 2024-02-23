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
        self.pin_delay = None
        self.cycle_delay = None
        self.mode = None
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
        self.mode_thread = None
        self.cycle_thread = None
        self._stop_mode_thread = threading.Event()
        self._stop_cycle_thread = threading.Event()
        self.setup_pins()
        self.set_mode('rest')

    def set_pin_delay(self, pin_delay):
        ''' Set the delay between each pin setup.'''
        self.pin_delay = pin_delay

    def set_cycle_delay(self, cycle_delay):
        ''' Set the delay between each cycle. '''
        self.cycle_delay = cycle_delay

    def sleep_with_check(self, delay):
        ''' Sleep for the specified delay, checking for a stop event. '''
        total_time = 0
        while total_time < delay and not self._stop_cycle_thread.is_set():
            time.sleep(0.01)
            total_time += 0.01

    def setup_pins(self):
        ''' Setup the MCP23017 pins. '''
        if self._hardware_initialized:
            for pin in ['motor', 'v1', 'v2', 'v5', 'shutdown']:
                self.pins[pin].direction = Direction.OUTPUT
            for pin in ['tls', 'panel_power']:
                self.pins[pin].direction = Direction.INPUT

    def thread_mode(self, mode):
        ''' Run the mode in a new thread. '''
        self._stop_mode_thread.clear()
        self.mode_thread = threading.Thread(target=self.set_mode, args=(mode,))
        self.mode_thread.start()

    def set_mode(self, mode):
        ''' Set the pins for the specified mode. '''
        modes = {
            'run': {'motor': True, 'v1': True, 'v2': False, 'v5': True},
            'rest': {'motor': False, 'v1': False, 'v2': False, 'v5': False},
            'purge': {'motor': True, 'v1': False, 'v2': True, 'v5': False},
            'burp': {'motor': False, 'v1': False, 'v2': False, 'v5': True},
            'bleed': {'motor': False, 'v1': False, 'v2': True, 'v5': True},
            'leak': {'motor': False, 'v1': True, 'v2': True, 'v5': True}
        }
        if mode in modes:
            self.mode = mode
            for pin, value in modes[mode].items():
                if self._stop_cycle_thread.is_set():
                    break
                self.pins[pin].value = value
                if self.pin_delay:
                    self.sleep_with_check(self.pin_delay)
        else:
            print(f'Invalid mode: {mode}')

    def set_sequence(self, sequence):
        ''' Set the pins for the specified sequence. '''
        try:
            for mode in sequence:
                if self._stop_cycle_thread.is_set():
                    break
                self.thread_mode(mode)
                if self.cycle_delay:
                    self.sleep_with_check(self.cycle_delay)
        except KeyboardInterrupt:
            self.set_mode('rest')
        finally:
            self.set_mode('rest')
            self.mode = 'Complete'

    def thread_sequence(self, sequence):
        ''' Run the specified sequence in a new thread. '''
        if not self._hardware_initialized:
            self.mode = None
        self._stop_cycle_thread.clear()
        self.cycle_thread = threading.Thread(target=self.set_sequence, args=(sequence,))
        self.cycle_thread.start()

    def get_values(self) -> str:
        ''' Return the values of the motor, v1, v2, and v5 pins. '''
        motor = self.pins['motor'].value
        v1 = self.pins['v1'].value
        v2 = self.pins['v2'].value
        v5 = self.pins['v5'].value
        return motor, v1, v2, v5

    def get_mode(self) -> str:
        ''' Return the current mode. '''
        return self.mode

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

    def test_mode(self):
        ''' Set the sequence for a test mode. '''
        self.thread_sequence(
            ['run', 'rest'] * 2 + ['purge', 'bleed']
        )

    def leak_test(self):
        ''' Set the sequence for a leak test. '''
        self.thread_sequence(
            ['leak']
        )

    def stop_cycle(self):
        ''' Stop the current sequence. '''
        print('Stopping sequence')
        if self.cycle_thread and self.cycle_thread.is_alive():
            self._stop_cycle_thread.set()
            self.cycle_thread.join()
            self.cycle_thread = None
        self.stop_mode()
        self.set_mode('rest')

    def stop_mode(self):
        ''' Stop the current mode. '''
        if self.mode_thread and self.mode_thread.is_alive():
            self._stop_mode_thread.set()
            self.mode_thread.join()
            self.cycle_thread = None