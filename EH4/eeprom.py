import smbus
import time

Device_Address= 0b1010111

EEPROM = smbus.SMBus(1)

def read_24C64_byte(EEPROM_Memory_Address):
    a1 = int(EEPROM_Memory_Address/256)
    a0 = int(EEPROM_Memory_Address % 256)
    EEPROM.write_i2c_block_data(Device_Address, a1, [a0])
    return EEPROM.read_byte(Device_Address);

def write_24C64_byte(EEPROM_Address, value):
    a1 = int(EEPROM_Address/256)
    a0 = int(EEPROM_Address % 256)
    EEPROM.write_i2c_block_data(Device_Address, a1, [a0, value])
    time.sleep(0.003) # Erprobte Mindestwartezeit für time.sleep: 0,003
    return;

for i in range ( 0, 8193 ):
    if i <= 100:
        #write_24C64_byte(i, i )
        write_24C64_byte(i, 12 )
        #print (i)
    else:
        write_24C64_byte(i, 0 )
        #write_24C64_byte(i, i % 100)
        #print( i % 100)
print(" Schreiben beendet ")

for i in range ( 0, 8193 ) :
    j = read_24C64_byte(i)
    if j > 0:
        print( i, j)
print( "Lesen beendet ")
