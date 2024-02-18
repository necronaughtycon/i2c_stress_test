#!/usr/bin/env python3

'''
====================================
                ADC
====================================
--------------
Usage Example:
--------------

from adc_config import ADC

# Create an instance of the ADC class with delay.
adc = ADC(delay=0.1)
'''

import threading
import time

try:
    import board
    import busio
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn
except (ImportError, NotImplementedError):
    busio = None
    board = None
    ADS = None
    AnalogIn = None


class ADC:
    '''
    This class is used to interface with the ADS1115 Analog-to-Digital Converter.
    '''

    def __init__(self, gain=1, delay=0.1):
        self.payload = None
        self.requests_filled = 0
        self.delay = delay
        self.start_time = None
        self.end_time = None
        self._thread = None
        self._stop_event = threading.Event()
        self._hardware_initialized = False
        if busio is None or board is None or ADS is None or AnalogIn is None:
            return
        i2c = busio.I2C(board.SCL, board.SDA)
        self._adc = ADS.ADS1115(i2c)
        self._channel = AnalogIn(self._adc, ADS.P0)
        self._adc.gain = gain
        self._hardware_initialized = True
        self._thread = threading.Thread(target=self._read_adc_continuous)
        self._thread.start()

    def _read_adc_continuous(self):
        ''' Continuously read ADC until stop event is set. '''
        self.start_time = time.time()
        while not self._stop_event.is_set():
            self.read_adc()
            self.requests_filled += 1
            time.sleep(self.delay)
            self.end_time = time.time()

    def read_adc(self) -> str:
        ''' Send request to ADC. '''
        if not self._hardware_initialized:
            self.payload = None
        try:
            self.payload = self._channel.value
        except IOError:
            self.payload = None

    def get_requests_filled(self) -> int:
        ''' Get the amount of requests filled. '''
        return self.requests_filled
    
    def get_payload(self) -> str:
        ''' Get the payload from the ADC. '''
        return str(self.payload)

    def stop(self):
        ''' Stop the ADC reading thread. '''
        self._stop_event.set()
        self.end_time = time.time()
        if self._thread is not None:
            self._thread.join()

    def get_duration(self) -> float:
        ''' Get the duration of the ADC test. '''
        if self.start_time is not None and self.end_time is not None:
            return self.end_time - self.start_time
        return 0.0