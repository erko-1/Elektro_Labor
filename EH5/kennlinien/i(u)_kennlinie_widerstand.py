import board
import busio

# initialize i2c
i2c = busio.I2C(board.SCL, board.SDA)

#initialize DAC
import adafruit_mcp4725
dac = adafruit_mcp4725.MCP4725(i2c)

#initialize ADC
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1015(i2c)

#define ADC channel 0,2; channel0 misst Uges und channel2 misst den widerstand an den unbekannten widerstand und GND bzw LED und GND
chan0 = AnalogIn(ads, ADS.P0)
chan2 = AnalogIn(ads, ADS.P2)

#Vorbereitung Spannungswerte für DAC -> raw_value, d.h. 0 bis 4095
steps = 20
stepsize = 4095 / steps

#file öffnen
file = open('/home/epr/Desktop/einheit5/i(u)_kennlinie_R.csv', 'w')

for i in range(steps+1):
    #dac -> spannungen ausgeben -> gesamtspannung bei jedem Schritt erhöhen
    dac.raw_value = int(i*stepsize)
    #spannungen am adc einlesen (in V): a0=u_gesamt und a2=u_r
    adc_a0 = chan0.voltage
    adc_a2 = chan2.voltage
    
    #strom berechnen am Vorwiderstad (wir haben eine serielle schaltung und somit ist der gesamte strom gleich an alle andere teile)
    I = (adc_a0 - adc_a2) / 220
    print(adc_a0, adc_a2, I)
    
    # U * 1000, I * 1000000 -> d.h. U in mV, I in mikroAmpere
    I = int(I*1000000)
    U_ges = int(adc_a0 * 1000)
    U_unbekannt = int(adc_a2 * 1000)
    
    #ins file schreiben
    file.write(str(I) + ',')
    file.write(str(U_unbekannt) + ',')
    file.write(str(U_ges) + '\n')

#datei schließen
file.close()
#spannung auf Null setzen
dac.raw_value = 0