import PySimpleGUI as sg
import wiringpi as wpi

led_pins = [17, 18, 27, 22, 23, 24, 25, 4]

wpi.wiringPiSetup()

for pin in led_pins:
    wpi.pinMode(pin, wpi.OUTPUT)
    
#define window's contents
layout = [[sg.Text("What's your name?")]
            [sg.Input(key='-INPUT-')]
        [sg.Text(size=(40.1), key='-OUTPUT-')]
        [sg.Button('ok'), sg.Button('quit')]]
        
#create window
window = sg.Window('Text input', layout)

#Display and interact
while True:
    event, values = window.read()
    
    number = int(values['-INPUT-'])
    
    led_num = int(number)
    if 1 <= led_num <= 8:
                # Ermitteln den Index für LED
        led_index = led_num - 1
                # Aktualisiere den Zustand der ausgewählten LED
        led_states[led_index] = 1 - led_states[led_index]
                # Aktualisiere den physikalischen Zustand der LEDs
        wpi.digitalWrite(led_pins[led_index], led_states[led_index])
                #print(f"LED {led_num} wurde {'eingeschaltet' if led_states[led_index] else 'ausgeschaltet'}")
    else:
        print("Ungültige Eingabe. Geben Sie eine Zahl zwischen 1 und 8 ein.")
    #
    if event == sg.WINDOW_CLOSED or event == 'quit':
        break
    #
    window['-OUTPUT-'].update('Hello' + values['-INPUT-'])
    
# Finish
window.close()
