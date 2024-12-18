import time
import board
import busio
import wiringpi as wpi
import PySimpleGUI as sg


i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_mcp4725
dac = adafruit_mcp4725.MCP4725(i2c)

def generate_triangle_wave():
    amplitude = 3.3
    frequency = 1.0
    period = 1 / frequency
    samples_per_cycle = 100
    interval = period / samples_per_cycle
    
    while True:
        for i in range(samples_per_cycle):
            value = (amplitude / 2) + ((amplitude / 2) * (2 * i / samples_per_cycle - 1))
            normalized_value = value / amplitude
            normalized_value = max(0, min(1, normalized_value))
            dac.normalized_value = int(normalized_value * 4095)
            time.sleep(interval)
            
generate_triangle_wave()
