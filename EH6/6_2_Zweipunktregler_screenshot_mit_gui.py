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

wpi.wiringPiSetupGpio()

pin_out=17
wpi.pinMode(pin_out, wpi.OUTPUT)
R1 = 88000
R0 = 100000
B = 4600
T0 = 298
tsoll = 0 #kelvin
tist = 0
hysterese = 1
runthread = 0
graphx = 10

def regelung_thread(window):
    global tsoll
    global tist
    global hysterese
    global runthread
    wpi.digitalWrite(pin_out, 0)
    while(runthread == 1):
        U_ntc = chan1.voltage
        #print(U_ntc) #in VOLT
        U1 = 5 - U_ntc
        I = U1/R1
        R_T = U_ntc/I
        tist = 1/((np.log(R_T/R0)/B)+1/T0) - 273
        #zweipunktregelung
        #wenn über 51°C, dann ausschalten
        if tist >= (tsoll + hysterese):
            wpi.digitalWrite(pin_out, 1)
        #wenn unter 49°C dann einschalten
        if tist <= (tsoll - hysterese):
            wpi.digitalWrite(pin_out, 0)
        print('Spannung am NTC:', U_ntc)
        print('Widerstand des NTC:', R_T)
        print('Isttemperatur:', tist, '\n')
        window.write_event_value('-UPDATE-','')
        time.sleep(1)
    window.write_event_value('-THREAD STOPPED-','')
def regelung():
    threading.Thread(target=regelung_thread, args=(window,), daemon=True).start()
graph = sg.Graph(canvas_size=(700,200),
                 graph_bottom_left=(0, 0),
                 graph_top_right=(700, 200),
                 background_color='white')
layout = [[sg.Output(size=(97,15))],
          [graph],
          [sg.Text("Tsoll         "),sg.Slider(range=(20,70), orientation='h', default_value=30, key = '-TSOLL-'),sg.Text("Tist: "),sg.Text(size=(8,1),key='-TIST-')],
          [sg.Text("Hysterese"),sg.Slider(range=(0.5,2), orientation='h', default_value=1, resolution=0.1, key = '-HYSTERESE-')],
          [sg.Button('Start'), sg.Button('Stop'),sg.Button('Apply'), sg.Button('Exit'), sg.Button('Screenshot')]  ]

window = sg.Window('2-Punkt-Regler', layout)

while True:             # Event Loop ++++++++++++++++++++++++++++++++++++++++
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break # hier auch die Lampe ausschalten
    
    if event == 'Start':
        tsoll=(values['-TSOLL-'])
        hysterese=(values['-HYSTERESE-'])
        window['Start'].update(disabled=True) #Start Button ausschalten, um keinen 2. Thread starten zu können
        print('\nRegelung gestartet \n')
        runthread=1
        graphx=0
        graph.erase()
        regelung() #Aufruf der Funktion zum Start des Regelungs-threads
    
    elif event== 'Stop':
        runthread=0
        window['Start'].update(disabled=False) #Start-Button wieder freigeben
        
    elif event == 'Apply': # erst durch apply werden die Werte der Slider in die Variablen übertragen
        tsoll=(values['-TSOLL-'])
        hysterese=(values['-HYSTERESE-'])
        
    elif event == '-UPDATE-': # wenn von Regelthread ein 'update' gesendet wird, kann man die Isttemperatur updaten
        window['-TIST-'].update(str(tist))  
        graph.draw_point([graphx,tist*2], size=2,color="black")
        graph.draw_point([graphx,tsoll*2], size=2,color="red")
        graphx=graphx+1
        if graphx>700:
            graphx=0
            graph.erase()
    
    elif event == '-THREAD STOPPED-':
        print('\nRegelung gestoppt \n')
    
    
    elif event == 'Screenshot':
        widget = graph.Widget
        box = (widget.winfo_rootx(),
        widget.winfo_rooty(),
        widget.winfo_rootx() + widget.winfo_width(),
        widget.winfo_rooty() + widget.winfo_height()
        )
        
        grab = ImageGrab.grab(bbox=box)
        grab.save('test.jpg')
        
    #print(event, values)    
window.close()

