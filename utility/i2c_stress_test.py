import time
import busio
import board
from adafruit_ads1x15.ads1115 import ADS1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_mcp230xx.mcp23017 import MCP23017
from digitalio import Direction

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

def ads_test(duration_seconds=10):
    adc = ADS(i2c)
    channel = AnalogIn(adc, ADS.P0)
    start_time = time.time()
    read_count = 0
    errors = 0

    while time.time() - start_time < duration_seconds:
        try:
            value = channel.value
            read_count += 1
        except Exception as e:
            print(f"Error on read {read_count}: {e}")
            errors += 1

    print(f"Completed {read_count} reads in {duration_seconds} seconds with {errors} errors.")

def mcp_test(duration_seconds=10):
    mcp = MCP23017(i2c)
    pins = {
        'outputs': [mcp.get_pin(i) for i in range(4)] + [mcp.get_pin(5), mcp.get_pin(4)],
        'inputs': [mcp.get_pin(8), mcp.get_pin(10)]
    }
    for pin in pins['outputs']:
        pin.direction = Direction.OUTPUT
    for pin in pins['inputs']:
        pin.direction = Direction.INPUT

    start_time = time.time()
    toggle_count = 0

    while time.time() - start_time < duration_seconds:
        for pin in pins['outputs']:
            pin.value = not pin.value  # Toggle pin
            toggle_count += 1

    print(f"Completed {toggle_count} toggles in {duration_seconds} seconds.")


if __name__ == "__main__":
    main()

