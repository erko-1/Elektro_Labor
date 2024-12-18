import time
import board
import busio
import wiringpi as wpi
import FreeSimpleGUI as sg

i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_mcp4725
dac = adafruit_mcp4725.MCP4725(i2c)

layout = [[sg.Text('Spannung (V):'), sg.Input(key='input'), sg.Button('ok'), sg.Button('Beenden')]]
window = sg.Window('Spannung dac', layout)

while True:
    event, values = window.read(timeout=500)
    if event == 'ok':
        input_value = float(values['input'])
        abc = input_value/3.3
        dac.normalized_value = abc
        print(input_value)
    
    if event == sg.WINDOW_CLOSED or event == 'Beenden':
        break
    
window.close()
    
