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

    def __init__(self, gain=1):
        self._hardware_initialized = False
        self._requests_filled = 0
        self._latest_payload = None
        self._stop = False
        if busio is None or board is None or ADS is None or AnalogIn is None:
            return
        i2c = busio.I2C(board.SCL, board.SDA)
        self._adc = ADS.ADS1115(i2c)
        self._channel = AnalogIn(self._adc, ADS.P0)
        self._adc.gain = gain
        self._hardware_initialized = True

    def read_adc(self, requests, delay) -> str:
        ''' Send request to ADC. '''
        if not self._hardware_initialized:
            return 'ERR'
        if not self._stop:
            for _ in range(requests):
                try:
                    value = self._channel.value
                    self._latest_payload = value
                    self._requests_filled += 1
                    time.sleep(delay)
                    # return f'{value:.2f}' if f'{value:.2f}' != '-0.00' else '0.00'
                    return value
                except IOError:
                    return 'ERR'
                if self._stop:
                    break

    def stop(self) -> int:
        ''' Stop the ADC. '''
        total_payload_size = self._requests_filled
        self._stop = True
        return total_payload_size

    def get_latest_payload(self) -> str:
        ''' Get the latest payload. '''
        return self._latest_payload

    def get_requests_filled(self) -> int:
        ''' Get the requests filled. '''
        return self._requests_filled