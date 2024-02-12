from utility import ADC, ADC2

adc = ADC()
adc2 = ADC2()
print(f'SMBus2: {adc.read_adc()}')
print(f'Adafruit: {adc2.read_adc()}')
