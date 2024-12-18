import wiringpi as wpi
import time

wpi.wiringPiSPISetup(1, 500000)

while True:
    adu_werte_0, adu_werte_1 = wpi.wiringPiSPIDataRW(1, bytes([0b00000110, 0b01000000, 0b0]))
    spannungswert = int.from_bytes(adu_werte_1, byteorder = 'big')
    spannungswert = ( spannungswert * 5000) / 4096
    print ('Spannung:' , spannungswert, 'mV' )
    time.sleep(0.5)
    adu_werte_0, adu_werte_1 = wpi.wiringPiSPIDataRW(1,bytes([0b00000110, 0b10000000, 0b0]))
    spannungswert = int.from_bytes(adu_werte_1, byteorder = 'big')
    spannungswert = ( spannungswert * 5000) / 4096
    print ('Spannung:' , spannungswert, 'mV' )
    time.sleep(0.5)