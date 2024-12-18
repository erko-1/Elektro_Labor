import PySimpleGUI as sg
import RPi.GPIO as GPIO

LAMPE_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LAMPE_PIN, GPIO.OUT)

layout = [
    [sg.Text(" "), sg.Radio('ON', "RADIO1", default=False, key="-IN1-", enable_events=True)],
    [sg.Text(" "), sg.Radio('OFF', "RADIO1", default=True, enable_events=True)]
    ]

window = sg.Window('Lampe', layout)

lamp_state = False

while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED:
        GPIO.cleanup()
        break
    elif values["-IN1-"] == True and not lamp_state:
        GPIO.output(LAMPE_PIN, GPIO.HIGH)
        lamp_state = True
    elif values["-IN1-"] == False and lamp_state:
        GPIO.output(LAMPE_PIN, GPIO.LOW)
        lamp_state = False
        
window.close()