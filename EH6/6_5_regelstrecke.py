import wiringpi as wpi
import FreeSimpleGUI as sg
import threading
import pyscreenshot as ImageGrab
import time
import board
import busio
import numpy as np

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)

# DAC setup
import adafruit_mcp4725
dac = adafruit_mcp4725.MCP4725(i2c)

# ADC setup
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1015(i2c)

chan1 = AnalogIn(ads, ADS.P1)

# Constants
R1 = 91000  # Vorwiderstand: 91kOhm
R0 = 100000  # Referenzwiderstand
B = 4600  # Materialkonstante des NTC
T0 = 298  # Referenztemperatur (Kelvin)

# Variables
tist = 0
vout = 0
graphx = 0
run = 0
untc = 0
tout_line = None  # Variable to store the red line for T_out

# Fensterlayout
graph = sg.Graph(canvas_size=(700, 200),
                 graph_bottom_left=(0, 0),
                 graph_top_right=(700, 200),
                 background_color='white')

layout = [
    [sg.Output(size=(97, 15))],
    [graph],
    [sg.Text("Tist: "), sg.Text(size=(8, 1), key='-TIST-')],
    [sg.Text("Tout: "), sg.Slider(range=(-50, 150), orientation='h', default_value=25, resolution=1, key='TOUT')],
    [sg.Text("Vout: "), sg.Text(size=(8, 1), key='-VOUT-')],
    [sg.Button('Start'), sg.Button('Stop'), sg.Button('Exit'), sg.Button('Screenshot')]
]

window = sg.Window('Streckencharakterisierung', layout)

while True:  # Event Loop ++++++++++++++++++++++++++++++++++++++++
    event, values = window.read(timeout=500)

    # Tout from slider
    tout = values["TOUT"]  # Tout in Celsius
    
    # Read NTC voltage
    untc = chan1.voltage

    # Calculate NTC resistance
    u1 = 5 - untc
    i = u1 / R1
    r_t = untc / i

    # Calculate Tist in Celsius
    tist = 1 / ((np.log(r_t / R0) / B) + 1 / T0) - 273

    # Calculate Vout using the formula
    vout = (20 / 29) * (tout - tist) + 2

    # Set DAC output
    dac.normalized_value = max(0, min(1, vout / 3.3))

    print(f"UNTC= {untc:.3f} V, Tist= {tist:.2f} C, Tout= {tout:.2f} C, Vout= {vout:.3f} V")

    # Update GUI elements
    window['-TIST-'].update(f"{tist:.2f} C")
    window['-VOUT-'].update(f"{vout:.3f} V")

    # Draw the red line for T_out
    if tout_line:
        graph.delete_figure(tout_line)
    tout_line_y = tout * 2  # Scale the graph to fit the temperature range
    tout_line = graph.draw_line((0, tout_line_y), (700, tout_line_y), color='red')

    if run == 1:
        print('Messung läuft \n')
        graph.draw_point([graphx, tist * 2], size=2, color="black")
        graphx = graphx + 1
        if graphx > 700:
            graphx = 0
            graph.erase()

    if event == sg.WIN_CLOSED or event == 'Exit':
        dac.normalized_value = 0  # Lampe ausschalten
        break

    if event == 'Start':
        run = 1
        graphx = 0
        graph.erase()

    elif event == 'Stop':
        run = 0
        print('Messung gestoppt \n')
        dac.normalized_value = 0  # Lampe aus

    elif event == 'Screenshot':
        widget = graph.Widget
        box = (widget.winfo_rootx(),
               widget.winfo_rooty(),
               widget.winfo_rootx() + widget.winfo_width(),
               widget.winfo_rooty() + widget.winfo_height())

        grab = ImageGrab.grab(bbox=box)
        grab.save('test.jpg')

window.close()
