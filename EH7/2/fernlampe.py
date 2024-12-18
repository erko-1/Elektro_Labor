import FreeSimpleGUI as sg
import time
import threading
import can   #Paket python-can
import wiringpi as wpi
import os

wpi.wiringPiSetupGpio()

wpi.pinMode( 17, 1 )
wpi.digitalWrite( 17, 0 )

os.system('sudo ip link set can0 type can bitrate 100000')
os.system('sudo ifconfig can0 up')

can0 = can.ThreadSafeBus(channel = 'can0', bustype = 'socketcan', receive_own_messages=True)

# der Einfachheit halber verwenden wir hier globale Variablen.
# ist zwar nicht best practise, aber funktioniert

runthread=0
eigener_tisch = 3

# mit dieser Funktion wird der thread  gestartet
def listen_to_CAN():
    threading.Thread(target=switch_lamp, args=(window,), daemon=True).start()

# in dieser Funktion lesen wir die CAN-Messages und schalten bei Bedarf die Lampe 
def switch_lamp(window):
    
    
    while(runthread==1):
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # hier den code einfügen, der die eingehenden CAN-Messages untersucht, und gegebenenfalls die Lampe schaltet
        msg = can0.recv(3.0) # Timeout von 3s
        if msg is None:
            print('Timeout, no message') # wenn lange keine Botschaft empfangen wurde --> Timeout
        else:
            msg_daten = msg.data
            
            if len(msg_daten) > 5:
            # Ausgabe der empfangenen Daten        
                print ("msg_daten:", msg_daten)     
            # Ausgabe der arbitration_id und der CAN-Botschaft        
                arbid = msg.arbitration_id
            #temperatur = ( (msg.data[0] << 8 ) + (msg.data[1]))/10
                tisch_id = msg.data[4]
                lampe_einaus = msg.data[5]
                print(tisch_id, lampe_einaus)
                
                if tisch_id == eigener_tisch:
                    print("Folgender Tisch bitte", eigener_tisch)
                    if lampe_einaus == 255:
                        wpi.digitalWrite( 17, 0 )
                    else:
                        wpi.digitalWrite( 17, 1 )
            else:
                pass
                    
            #temperatur = (msg.data[0] + (msg.data[1])/10)
            #feuchtigkeit = msg.data[2]
            #print(arbid, msg, temperatur, " °C", feuchtigkeit, " %rH")
      
        #time.sleep(1)
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
        wpi.digitalWrite(17 , 1 )
        break # hier auch die Lampe ausschalten
    
    if event == 'Start listening':
        runthread=1
        print('\nlistening started \n')
        
        listen_to_CAN() #start des threads 
    
    elif event== 'Stop listening':
        runthread=0
        
    elif event == 'SEND': # hier den Code zum Senden einfügen
        #pass
        if values["-1-"] == True:
            if values['-ON-'] == True:
                msg=can.Message(arbitration_id=eigener_tisch, data=[1,2,3,4,1,255,6])
            else:
                msg=can.Message(arbitration_id=eigener_tisch, data=[1,2,3,4,1,0,6])
        elif values["-2-"] == True:
            if values['-ON-'] == True:
                msg=can.Message(arbitration_id=eigener_tisch, data=[1,2,3,4,2,255,6])
            else:
                msg=can.Message(arbitration_id=eigener_tisch, data=[1,2,3,4,2,0,6])
        elif values["-3-"] == True:
            if values['-ON-'] == True:
                msg=can.Message(arbitration_id=eigener_tisch, data=[1,2,3,4,3,255,6])
            else:
                msg=can.Message(arbitration_id=eigener_tisch, data=[1,2,3,4,3,0,6])
        elif values["-4-"] == True:
            if values['-ON-'] == True:
                msg=can.Message(arbitration_id=eigener_tisch, data=[1,2,3,4,4,255,6])
            else:
                msg=can.Message(arbitration_id=eigener_tisch, data=[1,2,3,4,4,0,6])
        elif values["-5-"] == True:
            if values['-ON-'] == True:
                msg=can.Message(arbitration_id=eigener_tisch, data=[1,2,3,4,5,255,6])
            else:
                msg=can.Message(arbitration_id=eigener_tisch, data=[1,2,3,4,5,0,6])
        elif values["-6-"] == True:
            if values['-ON-'] == True:
                msg=can.Message(arbitration_id=eigener_tisch, data=[1,2,3,4,6,255,6])
            else:
                msg=can.Message(arbitration_id=eigener_tisch, data=[1,2,3,4,6,0,6])
        elif values["-7-"] == True:
            if values['-ON-'] == True:
                msg=can.Message(arbitration_id=eigener_tisch, data=[1,2,3,4,7,255,6])
            else:
                msg=can.Message(arbitration_id=eigener_tisch, data=[1,2,3,4,7,0,6])
        elif values["-8-"] == True:
            if values['-ON-'] == True:
                msg=can.Message(arbitration_id=eigener_tisch, data=[1,2,3,4,8,255,6])
            else:
                msg=can.Message(arbitration_id=eigener_tisch, data=[1,2,3,4,8,0,6])
        can0.send(msg)              
        # jeder radiobutton (Tisch 1-6) hat einen eigenen Key, die abgefragt werden müssen
        # für On/Off ist nur der Key'-ON-' (true/false) notwendig
        # sinnvoll ist es auch auch mit print die Message auszugeben
        pass
        print(msg)
        #print("\nXSend: arbid,255,0,0,0,0,0,0,0\n") #Beispiel
    
    elif event == '-THREAD STOP-':
        print('\nlistening stopped \n')
    
    print(event, values)
window.close()

