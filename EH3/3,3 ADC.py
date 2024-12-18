import wiringpi as wpi
import numpy as np
import time

# Setup GPIO pins
wpi.wiringPiSetupGpio()

# Raspberry Pi verwendete Pins angeben
pins_out = [17, 18, 27, 22, 23, 24, 25, 4]
pin_in = 12  # Pin für den Eingang

# Pins als Output/Input definieren
for pin in pins_out:
    wpi.pinMode(pin, wpi.OUTPUT)
wpi.pinMode(pin_in, wpi.INPUT)

# Konstanten für Temperaturberechnung
B = 4600
R_0 = 100000
T_0 = 298  # Kelvin (25°C)

while True:
    # Successive Approximation Algorithm
    low = 0
    high = 255

    while low <= high:
        mid = (low + high) // 2
        wpi.digitalWriteByte(mid)  # Ausgabe von mid auf DAC
        time.sleep(0.01)  # Kurze Wartezeit für Stabilität
        
        if wpi.digitalRead(pin_in) == 1:
            # Berechnungen, wenn der Vergleichspoint erreicht wurde
            U_2 = mid * 12.9 * 10**(-3)
            R_2 = U_2 / (5 - U_2) * 220000
            T = B * T_0 / (np.log(R_2 / R_0) * T_0 + B)
            print(f"Gemessene Temperatur: {T - 273.15:.2f}°C")
            break
        else:
            high = mid - 1 if wpi.digitalRead(pin_in) == 1 else mid + 1

    time.sleep(1)