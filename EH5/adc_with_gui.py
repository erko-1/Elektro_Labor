import time
import board
import busio
import wiringpi as wpi
import FreeSimpleGUI as sg

i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1015(i2c)

chan3 = AnalogIn(ads, ADS.P3)

layout = [[sg.Text('Spannung (V):'), sg.Text('', size=(50,1), key='1')]]
window = sg.Window('Spannung Potentiometer', layout)

while True:
    spannung = chan3.voltage
    
    event, values = window.read(timeout=500)
    if event == sg.WIN_CLOSED:
        break
    
    window['1'].update(str(spannung))
    time.sleep(1)
    
window.close()