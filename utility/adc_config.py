#!./venv/bin/python

'''
====================================
                ADC
====================================
'''

from collections import deque


class ADC:
    '''
    ADC
    ---
    This class is used to interface with the ADS1115 Analog-to-Digital Converter.
    '''
    _warnings = {'board': False, 'busio': False, 'ads': False}

    def __init__(self, amount=60, held=1, adc_zero=15422.0, gain=1):
        self._initialize_hardware()
        if self._hardware_available:
            i2c = busio.I2C(board.SCL, board.SDA)
            self._adc = ADS.ADS1115(i2c)
            self._channel = AnalogIn(self._adc, ADS.P0)
            self._adc.gain = gain
            self.adc_zero = adc_zero
        self.requests = amount
        self.requests_stored = deque(maxlen=held)

    @classmethod
    def _initialize_hardware(cls):
        try:
            import board
            cls._hardware_available = True
        except ImportError as e:
            print(f'Board library not available: {e}')
            cls._warnings['board'] = True
        try:
            import busio
            cls._hardware_available = True
        except ImportError as e:
            print(f'Busio library not available: {e}')
            cls._warnings['busio'] = True
        try:
            import adafruit_ads1x15.ads1115 as ADS
            cls._hardware_available = True
            from adafruit_ads1x15.analog_in import AnalogIn
        except ImportError as e:
            print(f'ADS1x15 library not available: {e}')
            cls._warnings['ads'] = True
        if any(cls._warnings):
            _cls_hardware_available = False

    @staticmethod
    def _calculate_average(readings):
        ''' Calculate the average of the readings. '''
        if len(readings) > 2:
            readings = sorted(readings)
            return sum(readings[1:-1]) / (len(readings) - 2)
        return sum(readings) / len(readings)

    @staticmethod
    def map_value(x, in_min, in_max, out_min, out_max):
        ''' Map a value from one range to another. '''
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def request_data(self) -> str:
        ''' Send request to ADC. '''
        if not self._hardware_available:
            return 'ERR'
        try:
            for _ in range(self.requests):
                value = self._channel.value
                result = round(self.map_value(value, self.adc_zero, 22864.0, 0.0, 20.8), 2)
                self.requests_stored.append(result)
            avg_result = self._calculate_average(self.requests_stored)
            return f'{avg_result:.2f}' if f'{avg_result:.2f}' != '-0.00' else '0.00'
        except IOError:
            return 'ERR'