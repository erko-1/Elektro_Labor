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
print("1")
chan1= AnalogIn(ads, ADS.P1)

wpi.wiringPiSetupGpio()

pin_out=17
wpi.pinMode(pin_out, wpi.OUTPUT)

R1 = 88000
R0 = 100000
B = 4600
T0 = 298
i=0
wpi.digitalWrite(pin_out, 0)
    
while True:
    U_ntc = chan1.voltage
    print(U_ntc) #in VOLT
    U1 = 5 - U_ntc
    I = U1/R1
    R_T = U_ntc/I
    T_now = 1/((np.log(R_T/R0)/B)+1/T0)
    print(T_now-273) #printet in grad celsius
    time.sleep(1)
    i=i+1
    if i==10:
        wpi.digitalWrite(pin_out, 1)
        break
        