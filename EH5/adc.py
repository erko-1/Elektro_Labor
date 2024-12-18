import time
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1015(i2c)

chan3 = AnalogIn(ads, ADS.P3)

while True:
    print(chan3.voltage)
    time.sleep(1)