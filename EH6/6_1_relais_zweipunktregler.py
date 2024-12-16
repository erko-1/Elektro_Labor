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

R1 = 88000 #wir haqben 88kOhm berecchnet aber wir verwendet ein 91kOhm Vorwiderstand
R0 = 100000
B = 4600
T0 = 298
T_soll = 323 #kelvin

wpi.digitalWrite(pin_out, 0)

for n in range(120):
    U_ntc = chan1.voltage
    print(U_ntc) #in VOLT
    U1 = 5 - U_ntc
    I = U1/R1
    R_T = U_ntc/I
    T_now = 1/((np.log(R_T/R0)/B)+1/T0)
    #zweipunktregelung
    #wenn über 51°C, dann ausschalten
    if T_now >= (T_soll + 1):
        wpi.digitalWrite(pin_out, 1)
    #wenn unter 49°C dann einschalten
    if T_now <= (T_soll - 1):
        wpi.digitalWrite(pin_out, 0)
    #sonst nix machen

    print(T_now-273) #printet in grad celsius
    time.sleep(1)
    if n== 120:
        wpi.digitalWrite(pin_out, 1)
        break
