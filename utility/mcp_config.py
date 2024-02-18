import board
import busio
from digitalio import Direction
from adafruit_mcp230xx.mcp23017 import MCP23017


i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)

motor = mcp.get_pin(0)
v1 = mcp.get_pin(1)
v2 = mcp.get_pin(2)
v5 = mcp.get_pin(3)
shutdown = mcp.get_pin(4)
tls = mcp.get_pin(8)
panel_power = mcp.get_pin(10)

motor.direction = Direction.OUTPUT
v1.direction = Direction.OUTPUT
v2.direction = Direction.OUTPUT
v5.direction = Direction.OUTPUT
shutdown.direction = Direction.OUTPUT
tls.direction = Direction.INPUT
panel_power.direction = Direction.INPUT
