import PySimpleGUI as sg
import os
import can   #Paket python-can

from datetime import datetime, timezone

os.system('sudo ip link set can0 type can bitrate 100000')
os.system('sudo ifconfig can0 up')

can0 = can.ThreadSafeBus(channel = 'can0', bustype = 'socketcan_ctypes', receive_own_messages=True)

T1=1
RH1=11
T2=2
RH2=22
T3=3
RH3=33

layout = [
        [sg.Text("Tisch"), sg.Text("Temp:"),sg.Text("RH:")],
        [sg.Text("    1    "), sg.Text("",size=(6,1),key="-T1-"),sg.Text("", size=(8,1), key="-RH1-"),
            sg.Text("", size=(20,1), key="-TIME1-")],
        [sg.Text("    2    "), sg.Text("",size=(6,1),key="-T2-"),sg.Text("", size=(8,1), key="-RH2-"),
            sg.Text("", size=(20,1), key="-TIME2-")],
        [sg.Text("    3    "), sg.Text("",size=(6,1),key="-T3-"),sg.Text("", size=(8,1), key="-RH3-"),
            sg.Text("", size=(20,1), key="-TIME3-")],
        [sg.Text("    4    "), sg.Text("",size=(6,1),key="-T4-"),sg.Text("", size=(8,1), key="-RH4-"),
            sg.Text("", size=(20,1), key="-TIME4-")],
        [sg.Text("    5    "), sg.Text("",size=(6,1),key="-T5-"),sg.Text("", size=(8,1), key="-RH5-"),
            sg.Text("", size=(20,1), key="-TIME5-")],
        [sg.Text("    6    "), sg.Text("",size=(6,1),key="-T6-"),sg.Text("", size=(8,1), key="-RH6-"),
            sg.Text("", size=(20,1), key="-TIME6-")],
        [sg.Text("    7    "), sg.Text("",size=(6,1),key="-T7-"),sg.Text("", size=(8,1), key="-RH7-"),
            sg.Text("", size=(20,1), key="-TIME7-")],
        [sg.Text("    8    "), sg.Text("",size=(6,1),key="-T8-"),sg.Text("", size=(8,1), key="-RH8-"),
            sg.Text("", size=(20,1), key="-TIME8-")],
        ]
window = sg.Window('T/RH', layout)

while True:             
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED:
        break
    msg = can0.recv(3.0) # Timeout von 3s
    if msg is None:
        print('Timeout, no message') # wenn lange keine Botschaft empfangen wurde --> Timeout
    else:
        # Ausgabe der empfangenen Daten        
        msg_daten = msg.data
        print (msg_daten)     
        # Ausgabe der arbitration_id und der CAN-Botschaft        
        arbid = msg.arbitration_id
        #zeitstempel = 0
        #zeitstempel = msg.timestamp
        zeitstempel = datetime.fromtimestamp(msg.timestamp)
        print(datetime.fromtimestamp(msg.timestamp))
        #temperatur = ( (msg.data[0] << 8 ) + (msg.data[1]))/10
        temperatur = (msg.data[0] + (msg.data[1])/10)
        feuchtigkeit = msg.data[2]
        print(arbid, msg, temperatur, " °C", feuchtigkeit, " %rH")
        if arbid == 1:
            RH1=feuchtigkeit
            T1=temperatur
            window['-RH1-'].update(str(RH1))
            window['-T1-'].update(str(T1))
            window['-TIME1-'].update(str(zeitstempel))
        elif arbid == 2:
            RH2=feuchtigkeit
            T2=temperatur
            window['-RH2-'].update(str(RH2))
            window['-T2-'].update(str(T2))   
            window['-TIME2-'].update(str(zeitstempel))
        elif arbid == 3:
            RH3=feuchtigkeit
            T3=temperatur
            window['-RH3-'].update(str(RH3))
            window['-T3-'].update(str(T3))
            window['-TIME3-'].update(str(zeitstempel))
        elif arbid == 4:
            RH4=feuchtigkeit
            T4=temperatur
            window['-RH4-'].update(str(RH4))
            window['-T4-'].update(str(T4))   
            window['-TIME4-'].update(str(zeitstempel))
        elif arbid == 5:
            RH5=feuchtigkeit
            T5=temperatur
            window['-RH5-'].update(str(RH5))
            window['-T5-'].update(str(T5))
            window['-TIME5-'].update(str(zeitstempel))
        elif arbid == 6:
            RH6=feuchtigkeit
            T6=temperatur
            window['-RH6-'].update(str(RH6))
            window['-T6-'].update(str(T6))   
            window['-TIME6-'].update(str(zeitstempel))
        elif arbid == 7:
            RH7=feuchtigkeit
            T7=temperatur
            window['-RH7-'].update(str(RH7))
            window['-T7-'].update(str(T7))
            window['-TIME7-'].update(str(zeitstempel))
        elif arbid == 8:
            RH8=feuchtigkeit
            T8=temperatur
            window['-RH8-'].update(str(RH8))
            window['-T8-'].update(str(T8))   
            window['-TIME8-'].update(str(zeitstempel))
window.close()
