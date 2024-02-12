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

from smbus2 import SMBus, i2c_msg


class ADC2:
    '''
    This class is used to interface with the ADS1115 Analog-to-Digital Converter.
    '''

    def __init__(self, gain=1):
        self._hardware_initialized = False
        try:
            self._bus = SMBus(1)  # 1 indicates /dev/i2c-1.
            self._address = 0x48  # Default i2c address for the ADS1115.
            self._gain = gain
            self._hardware_initialized = True
        except (ValueError, FileNotFoundError) as e:
            print(f'Failed to initialize hardware: {e}')

    def read_adc(self, channel=0):
        ''' Read data from ADC. '''
        if not self._hardware_initialized:
            return 'ERR'
        try:
            # Write configuration to ADC
            config = [0x01, 0xC3 | (channel & 0x07), 0x83]  # Adjust as needed
            self._bus.write_i2c_block_data(self._address, config[0], config[1:])

            # Read data from ADC
            data = self._bus.read_i2c_block_data(self._address, 0x00, 2)
            value = (data[0] << 8) | data[1]
            if value & 0x8000 != 0:  # If the sign bit is set
                value -= 0x10000  # Convert to negative value

            # Scale the value to the range 0-32767
            value = (value + 32768) / 2

            return f'{value:.2f}' if f'{value:.2f}' != '-0.00' else '0.00'
        except IOError as io_error:
            print(f'Failed to read from ADC: {io_error}')
            return 'ERR'