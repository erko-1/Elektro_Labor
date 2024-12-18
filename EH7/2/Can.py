import PySimpleGUI as sg
import time
import threading

# der Einfachheit halber verwenden wir hier globale Variablen.
# ist zwar nicht best practise, aber funktioniert

runthread=0

# mit dieser Funktion wird der thread  gestartet
def listen_to_CAN():
    threading.Thread(target=switch_lamp, args=(window,), daemon=True).start()

# in dieser Funktion lesen wir die CAN-Messages und schalten bei Bedarf die Lampe 
def switch_lamp(window):
    
    
    while(runthread==1):
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # hier den code einfügen, der die eingehenden CAN-Messages untersucht, und gegebenenfalls die Lampe schaltet
        
        time.sleep(5)
        window.write_event_value('-Lamp switched-',"") # schreibe ein Update-event, wenn die Lampe geschaltet wurde
        
        
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    window.write_event_value('-THREAD STOP-', '')
    

# Fensterlayout

layout = [[sg.Output(size=(90,20))],
          [sg.Radio('Tisch 1', 1, default=False, key="-1-"),sg.Radio('Tisch 2', 1, default=True, key="-2-"),sg.Radio('Tisch 3', 1, default=False, key="-3-"),
           sg.Radio('Tisch 4', 1, default=False, key="-4-"),sg.Radio('Tisch 5', 1, default=False, key="-5-"),sg.Radio('Tisch 6', 1, default=False, key="-6-")    ],
          [sg.Radio('ON', 2, default=False, key="-ON-"),sg.Radio('OFF', 2, default=True)],
          [sg.Button('Start listening'), sg.Button('Stop listening'),sg.Button('SEND'), sg.Button('Exit')]  ]

window = sg.Window('Fernschaltung über CAN', layout)

while True:             # Event Loop ++++++++++++++++++++++++++++++++++++++++
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break # hier auch die Lampe ausschalten
    
    if event == 'Start listening':
        runthread=1
        print('\nlistening started \n')
        
        listen_to_CAN() #start des threads 
    
    elif event== 'Stop listening':
        runthread=0
        
    elif event == 'SEND': # hier den Code zum Senden einfügen
        pass
        # jeder radiobutton (Tisch 1-6) hat einen eigenen Key, die abgefragt werden müssen
        # für On/Off ist nur der Key'-ON-' (true/false) notwendig
        # sinnvoll ist es auch auch mit print die Message auszugeben
        print("\nSend: arbid,255,0,0,0,0,0,0,0\n") #Beispiel
    
    elif event == '-THREAD STOP-':
        print('\nlistening stopped \n')
    
    print(event, values)
window.close()
