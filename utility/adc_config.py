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
        self._hardware_initialized = False
        self._latest_payload = None
        self._delay = delay
        self._stop_event = threading.Event()
        i2c = busio.I2C(board.SCL, board.SDA)
        self._adc = ADS(i2c)
        self._channel = AnalogIn(self._adc, ADS.P0)
        self._adc.gain = gain
        self._hardware_initialized = True
        self._thread = threading.Thread(target=self._read_adc_continuous)
        self._thread.start()

    def _read_adc_continuous(self):
        ''' Continuously read ADC until stop event is set. '''
        while not self._stop_event.is_set():
            self.read_adc()
            time.sleep(self._delay)

    def read_adc(self) -> str:
        ''' Send request to ADC. '''
        if not self._hardware_initialized:
            return 'ERR'
        try:
            value = self._channel.value
            self._latest_payload = value
            self._requests_filled += 1
        except IOError:
            return 'ERR'

    def get_latest_payload(self) -> str:
        ''' Get the latest payload. '''
        return str(self._latest_payload)

    def get_requests_filled(self) -> int:
        ''' Get the requests filled. '''
        return self._requests_filled

    def stop(self):
        ''' Stop the ADC thread. '''
        self._stop_event.set()
        self._thread.join()