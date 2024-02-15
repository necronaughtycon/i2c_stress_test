#!/usr/bin/env python3

'''
====================================
                ADC
====================================
--------------
Usage Example:
--------------

from adc_config import ADC

# Create an instance of the ADC class with custom amount and held values
adc = ADC(amount=100, held=10)

# Now you can use the adc instance to request data
data = adc.request_data()
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
        while not self._stop_event.is_set():
            self.read_adc()
            time.sleep(self.delay)

    def read_adc(self) -> str:
        ''' Send request to ADC. '''
        if not self._hardware_initialized:
            self.payload = 'ERR'
        try:
            self.payload = self._channel.value
            self.requests_filled += 1
            print(self.requests_filled)
            print(self.payload)
        except IOError:
            self.payload = 'ERR'

    def get_requests_filled(self):
        ''' Get the amount of requests filled. '''
        return self.requests_filled

    def stop(self):
        ''' Stop the ADC reading thread. '''
        self.requests_filled = 0
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join()