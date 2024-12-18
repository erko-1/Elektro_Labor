import minimalmodbus
import time
import os
import can

os.system('sudo ip link set can0 type can bitrate 100000')
os.system('sudo ifconfig can0 up')
can0 = can.ThreadSafeBus(channel= 'can0', bustype='socketcan_ctypes', receive_own_messages=True)

instrument =minimalmodbus.Instrument('/dev/serial0',1)
instrument.serial.baudrate=9600
instrument.serial.timeout=0.5

RSP5_TEMP  = 0x001

while True:
    temperature=0
    humidity=0
    try:
        temperature=instrument.read_register(1,1,4)
    except minimalmodbus.NoResponseError:
        print("Modbus timeout")
    time.sleep(1)
    try:
        humidity=instrument.read_register(2,1,4)
    except minimalmodbus.NoResponseError:
        print("modbus timeout")
    time.sleep(1)
    print( 'Temperatur: ', temperature, ' °C Feuchtigkeit: ', humidity, '%RH')
    #byte_0 = temperature >> 8
    #byte_1 = temperature & 0x00FF
    byte_0 = int(temperature)
    byte_1 = int(10*(temperature%int(temperature)))
    byte_2 = int(humidity)
    print(byte_0, byte_1, byte_2)
    msg=can.Message(arbitration_id=RSP5_TEMP, data=[byte_0,byte_1,byte_2,3,4,5,6,7], extended_id=False)
    #msg=can.Message(arbitration_id=0x321, data=[0,1,2,3,4,5,6,7], extended_id=False)
    can0.send(msg)

#os.system('sudo ifconfig can0 down')

