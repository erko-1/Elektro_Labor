import wiringpi as wpi

import time
import board
import busio
import numpy as np

i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_mcp4725
dac = adafruit_mcp4725.MCP4725(i2c)

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1015(i2c)

chan1= AnalogIn(ads, ADS.P1)

wpi.wiringPiSetupGpio()

U_dac = 0.5

while True:
    dac.normalized_value = U_dac
    print(chan1.voltage)
    time.sleep(5)
