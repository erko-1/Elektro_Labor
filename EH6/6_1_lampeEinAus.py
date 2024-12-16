import time
import wiringpi as wpi


wpi.wiringPiSetupGpio()
wpi.pinMode(17, 1) 

wpi.digitalWrite(17, 0)

