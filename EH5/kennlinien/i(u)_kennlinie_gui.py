import board
import busio
import FreeSimpleGUI as sg

# initialize i2c
i2c = busio.I2C(board.SCL, board.SDA)

#initialize DAC
import adafruit_mcp4725
dac = adafruit_mcp4725.MCP4725(i2c)

#initialize ADC
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1015(i2c)

#define ADC channel 0,2; channel0 misst Uges und channel2 misst den widerstand an den unbekannten widerstand und GND bzw LED und GND
chan0 = AnalogIn(ads, ADS.P0)
chan2 = AnalogIn(ads, ADS.P2)

#Vorbereitung Spannungswerte für DAC -> raw_value, d.h. 0 bis 4095
steps = 20
stepsize = 4095 / steps

#layout des grafikobjektes
graph = sg.Graph(canvas_size=(800, 400),
                 graph_bottom_left=(-100,-100),
                 graph_top_right=(3000, 6000),
                 background_color = 'white',
                 key='graph')

# Fensterlayout
layout = [
    [graph],
    [sg.Button('Start'), sg.Button('Exit')]
    ]
window = sg.Window('LED i(u) Kennlinie', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    if event == 'Start':
        # zeichne die I(U) kennlinie
        graph.erase()
        graph.draw_text('I', (10, 5500), color = 'black')
        graph.draw_text('U', (2500, 10), color = 'black')
        graph.draw_line((1, 0), (1, 6000), color = 'black') # y-achse

        graph.draw_line((0, 2), (3000, 2), color = 'black') # x-achse
        #graph.draw_line((0, 3), (3000, 3), color = 'black')
        
        for i in range(steps+1):
            #dac -> spannungen ausgeben -> gesamtspannung bei jedem Schritt erhöhen
            dac.raw_value = int(i*stepsize)
            #spannungen am adc einlesen (in V): a0=u_gesamt und a2=u_r
            adc_a0 = chan0.voltage
            adc_a2 = chan2.voltage
            
            #strom berechnen am Vorwiderstad (wir haben eine serielle schaltung und somit ist der gesamte strom gleich an alle andere teile)
            I = (adc_a0 - adc_a2) / 220
            print(adc_a0, adc_a2, I)
            
            # U * 1000, I * 1000000 -> d.h. U in mV, I in mikroAmpere
            # mann muss dann später bei der berechnung von R aus der steigung die Einheiten wieder in V und A umrechnen
            I = int(I*1000000)
            U_ges = int(adc_a0 * 1000)
            U_LED = int(adc_a2 * 1000)
            
            graph.draw_point((U_LED, I), size=30, color='black')
    
            #spannung auf Null setzen
            dac.raw_value = 0
window.close()
