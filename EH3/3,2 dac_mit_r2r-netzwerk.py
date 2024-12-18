import wiringpi as wpi

wpi.wiringPiSetupGpio()

#am raspi verwendete pins angebgen
pins_out = [17, 18, 27, 22, 23, 24, 25, 4]

#pins als output/input definieren

for pin in pins_out:
    wpi.pinMode(pin, wpi.OUTPUT)
    
try:
    while True:
        for i in range(256):
            wpi.digitalWriteByte(i)
            #wpi.delay(20) #miliseconds
            
    
except KeyboardInterrupt:
    #alle ausschalten
    [wpi.digitalWrite(pin, 0) for pin in pins_out]
    quit()