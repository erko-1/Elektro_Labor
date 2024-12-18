import time
import board
import busio
import wiringpi as wpi
import FreeSimpleGUI as sg


i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_mcp4725
dac = adafruit_mcp4725.MCP4725(i2c)

# ADC brauchen wir hier eignetlich nicht
#import adafruit_ads1x15.ads1015 as ADS
#from adafruit_ads1x15.analog_in import AnalogIn

steps = 20
stepsize = 1/steps

while True:
    #dreiecksignal
    dac.normalized_value = 0
    
    #aufwärtsrampe
    for i in range(1, steps+1, 1):
        dac.normalized_value = stepsize * i
        time.sleep(0.1)
        
    #abwärtsrampe
    for i in range(steps, 1, -1):
        dac.normalized_value = stepsize * i
        time.sleep(0.1)
