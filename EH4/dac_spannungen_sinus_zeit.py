import wiringpi as wpi
import math
import time

wpi.wiringPiSPISetup(0, 500000)  


def create_sin_wave(s=20):
    sin_wave = []
    for i in range(s):
        sin_value = int((math.sin(2 * math.pi * i / s) + 1) * 2047.5)  # Skaliert auf 0-4095
        sin_wave.append(sin_value)
    return sin_wave

def to_bytes(A, B):
    byte1 = A >> 4
    byte2_1 = A & 0b000000001111
    byte2_2 = B >> 8
    byte2 = (byte2_1 << 4) + byte2_2
    byte3 = B & 0b000011111111
    return byte1, byte2, byte3

#sin_wave = create_sin_wave()

# Festlegen der Sinus-Signalperiode in Sekunden
frequency = 400  
start_time = wpi.micros() / 1000000  # Startzeit in Sekunden

try:
    while True:
        t = (wpi.micros() / 1000000) - start_time
#        sin_samples = int((t / period))
        value = int(math.sin(2*math.pi*frequency * t)*2047+2047)
        c1, c2, c3 = to_bytes(A=value, B=0)
        

        wpi.wiringPiSPIDataRW(0, bytes([c1, c2, c3]))

     #   time.sleep(0.01)
        
except KeyboardInterrupt:
    print("Programm wurde beendet.")

