import os
import can
import time

os.system('sudo ip link set can0 type can bitrate 100000')
os.system('sudo ifconfig can0 up')

#can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')
can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')

RSP10_LED = 0x007

for i in range(0,256,1):
    #msg = can.Message(arbitration_id=RSP10_LED, data=[0,1,2,3,4,5,6,7], extended_id=False)
    msg = can.Message(arbitration_id=RSP10_LED, data=[0,1,2,3,4,5,6,i], extended_id=False)
    can0.send(msg)
    print(i)
    time.sleep(1)

print ("Ende")
#os.system('sudo ifconfig can0 down')
