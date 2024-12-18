import os
import can
import PySimpleGUI as sg

# CAN-Bus Setup
os.system('sudo ip link set can0 type can bitrate 100000')
os.system('sudo ifconfig can0 up')

can0 = can.ThreadSafeBus(channel='can0', bustype='socketcan')

# GUI Layout
layout = [
    [sg.Text(f"Teilnehmer {i}", size=(15, 1)), 
     sg.Text("Temp: --- °C", key=f"TEMP_{i}", size=(15, 1)), 
     sg.Text("RH: --- %", key=f"RH_{i}", size=(15, 1))]
    for i in range(9)
] + [[sg.Button("Beenden")]]

window = sg.Window("Temperatur- und Luftfeuchteanzeige", layout)

# Datenstruktur zur Speicherung der aktuellen Werte
data = {i: {"temp": "---", "humidity": "---"} for i in range(9)}

try:
    while True:
        event, _ = window.read(timeout=100)  # Aktualisierung alle 100ms

        if event == sg.WINDOW_CLOSED or event == "Beenden":
            break

        # CAN-Nachricht empfangen
        msg = can0.recv(0.1)  # Timeout von 0.1s
        if msg is not None:
            try:
                arbid = msg.arbitration_id
                if 0 <= arbid <= 8:  # Nur Teilnehmer 0–8 beachten
                    temperatur = (msg.data[0]) + (msg.data[1] / 10)
                    humidity = int(msg.data[2])
                    
                    # Werte aktualisieren
                    data[arbid]["temp"] = f"{temperatur:.1f}"
                    data[arbid]["humidity"] = f"{humidity}"

                    # GUI aktualisieren
                    window[f"TEMP_{arbid}"].update(f"Temp: {data[arbid]['temp']} °C")
                    window[f"RH_{arbid}"].update(f"RH: {data[arbid]['humidity']} %")
            except (IndexError, ValueError):
                print("Fehler beim Verarbeiten der Nachricht:", msg)

finally:
    window.close()
    os.system('sudo ifconfig can0 down')
