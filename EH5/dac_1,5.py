import time
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_mcp4725
dac = adafruit_mcp4725.MCP4725(i2c)

while True:
    dac.raw_value = int((4095*1.5)/3.3)