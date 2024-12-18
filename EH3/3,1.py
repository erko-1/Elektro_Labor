import time

import wiringpi as wpi
wpi.wiringPiSetupGpio()

wpi.pinMode(17, 1)

while True:
    time.sleep(1)
    wpi.digitalWrite(17, 1)
    time.sleep(1)
    wpi.digitalWrite(17, 0)