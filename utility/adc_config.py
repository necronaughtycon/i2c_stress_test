#!./venv/bin/python

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
                    time.sleep(delay)
                    return str(value)
                    # return f'{value:.2f}' if f'{value:.2f}' != '-0.00' else '0.00'
                except IOError:
                    return 'ERR'
                if self._stop:
                    break

    def stop(self):
        ''' Stop the ADC. '''
        self._stop = True