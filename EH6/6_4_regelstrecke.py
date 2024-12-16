import wiringpi as wpi
import FreeSimpleGUI as sg
import threading
import pyscreenshot as ImageGrab
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
R1 = 88000 
R0 = 100000
B = 4600
T0 = 298

tist= 0
vout = 0
graphx=0
run =0
untc=0





# Fensterlayout
graph = sg.Graph(canvas_size=(700, 200),
                 graph_bottom_left=(0, 0),
                 graph_top_right=(700, 200),
                 background_color='white')
                 

layout = [[sg.Output(size=(97,15))],
          [graph],
          [sg.Text("Tist: "),sg.Text(size=(8,1),key='-TIST-')],
          [sg.Text("Vout"),sg.Slider(range=(0,3.3), orientation='h', default_value=0, resolution=0.1, key = 'VOUT')],
          [sg.Button('Start'), sg.Button('Stop'), sg.Button('Exit'), sg.Button('Screenshot')]  ]

window = sg.Window('Streckencharakterisierung', layout)

while True:             # Event Loop ++++++++++++++++++++++++++++++++++++++++
    event, values = window.read(timeout=500)
    
    vout=(values["VOUT"])/3.3 # Umrechnung auf 'normalized_value'
    dac.normalized_value=vout
    #hier messen der Temperatur einbauen ------------------------------------
    untc = chan1.voltage
    #print(U_ntc) #in VOLT
    U1 = 5 - untc
    I = U1/R1
    R_T = untc/I
    tist = 1/((np.log(R_T/R0)/B)+1/T0) - 273
    #untc=chan1.voltage
    
    print('UNTC= ',untc,' V')
    #tist=round(vout*100,2) #dummy-Funktion zum Testen
    
    #------------------------------------------------------------------------
    
    window['-TIST-'].update(str(tist))  
    if(run==1):
        print('Messung läuft \n')
        window['-TIST-'].update(str('tist'))
        graph.draw_point([graphx,tist*2], size=2,color="black")
        graphx=graphx+1
        if graphx>700:
            graphx=0
            graph.erase()
    
    if event == sg.WIN_CLOSED or event == 'Exit':
        
        #dac.normalized_value=0 Lampe ausschalten
        
        break 
    
    if event == 'Start':
        run=1
        graphx=0
        graph.erase()
        
        #hier die Ausgabe der Ausgangsspannung
        #dacnormalized_value=vout    (Lampe ein)
    
    elif event== 'Stop':
        run=0
        print('Messung gestoppt \n')
        #dac.normalized_value=0    (Lampe aus)
        
    elif event == 'Screenshot':
        widget = graph.Widget
        box = (widget.winfo_rootx(),
        widget.winfo_rooty(),
        widget.winfo_rootx() + widget.winfo_width(),
        widget.winfo_rooty() + widget.winfo_height()
        )
        
        grab = ImageGrab.grab(bbox=box)
        grab.save('test.jpg')
        
window.close()