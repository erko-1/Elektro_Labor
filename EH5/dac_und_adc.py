import time
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_mcp4725
dac = adafruit_mcp4725.MCP4725(i2c)

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1015(i2c)

chan0 = AnalogIn(ads, ADS.P0)

v = 2
u = (4095*v)/3.3

while True:
    dac.raw_value = int(u)
    time.sleep(0.5)
    print(f'Spannung in V: {chan0.voltage}')