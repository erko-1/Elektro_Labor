import RPi.GPIO as GPIO
import serial

EN_485=4
GPIO.setmode(GPIO.BCM)
GPIO.setup(EN_485,GPIO.OUT)
GPIO.output(EN_485,GPIO.LOW)

print("vor serial")
#ser = serial.Serial("/dev/serial1",115200,timeout=1)
ser = serial.Serial("/dev/ttyS0",115200,timeout=1)

while 1:
    str=ser.readall()
    if str:
        print (str)
