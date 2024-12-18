import wiringpi as wpi
import time
import PySimpleGUI as sg

# SPI-Setup
wpi.wiringPiSPISetup(1, 500000)

# GUI-Layout
layout = [
    [sg.Text("Spannung Kanal 0:", size=(20, 1)), sg.Text("", key="spannungswert_0", size=(10, 1))],
    [sg.Text("Spannung Kanal 1:", size=(20, 1)), sg.Text("", key="spannungswert_1", size=(10, 1))],
    [sg.Button("Beenden")]
]

# Fenster erstellen
window = sg.Window("Spannungsanzeige", layout)

# Hauptschleife
try:
    while True:
        # Ereignisse abfragen
        event, values = window.read(timeout=500)
        
        # Beenden, wenn der Button gedrückt wurde oder das Fenster geschlossen wird
        if event == sg.WINDOW_CLOSED or event == "Beenden":
            break
        
        # Spannung von Kanal 0 lesen
        adu_werte_0, adu_werte_1 = wpi.wiringPiSPIDataRW(1, bytes([0b00000110, 0b01000000, 0b0]))
        spannungswert_0 = int.from_bytes(adu_werte_1, byteorder='big')
        spannungswert_0 = (spannungswert_0 * 5000) / 4096  # Umrechnung in mV

        # Spannung von Kanal 1 lesen
        adu_werte_0, adu_werte_1 = wpi.wiringPiSPIDataRW(1, bytes([0b00000110, 0b10000000, 0b0]))
        spannungswert_1 = int.from_bytes(adu_werte_1, byteorder='big')
        spannungswert_1 = (spannungswert_1 * 5000) / 4096  # Umrechnung in mV

        # GUI-Elemente mit neuen Werten aktualisieren
        window["spannungswert_0"].update(f"{spannungswert_0:.2f} mV")
        window["spannungswert_1"].update(f"{spannungswert_1:.2f} mV")

        # Kurze Pause für die Aktualisierungsfrequenz
        time.sleep(0.5)

finally:
    window.close()
