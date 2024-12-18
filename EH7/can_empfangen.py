import os
import can
import wiringpi as wpi




os.system('sudo ip link set can0 type can bitrate 100000')
os.system('sudo ifconfig can0 up')

#can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')
can0 = can.ThreadSafeBus(channel = 'can0', bustype = 'socketcan')

while True:
    msg = can0.recv(3.0) # Timeout von 3s
    if msg is None:
        print('Timeout, no message')
    else:
        msg_daten = msg.data
        #print (msg_daten)
       
        temperatur = ( (msg.data[0]) + (msg.data[1]/10))
        humidity = int(msg.data[2])
        print(temperatur, " °C", humidity, " %RH")
        arbid = msg.arbitration_id
        print (arbid)
        print (msg)
       

os.system('sudo ifconfig can0 down')
