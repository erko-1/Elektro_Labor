import wiringpi as wpi

led_pins = [17, 18, 27, 22, 23, 24, 25, 4]

wpi.wiringPiSetupGpio()

for pin in led_pins:
    wpi.pinMode(pin, wpi.OUTPUT)
    
try:
    while True:
        # Aufwärtslauf
        for i in range(8):
            wpi.digitalWrite(led_pins[i], wpi.HIGH)
            wpi.delayMicroseconds(250000) #verzögerung 250 ms
            wpi.digitalWrite(led_pins[i], wpi.LOW)
            
        # Abwärtslauf
        for i in range(7, -1, -1):
            wpi.digitalWrite(led_pins[i], wpi.HIGH)
            wpi.delayMicroseconds(250000) #verzögerung 250 ms
            wpi.digitalWrite(led_pins[i], wpi.LOW)
            
        print("Light show!")

except KeyboardInterrupt:
    # Beim Beenden das GPIO-Cleanup durchführen.
    for pin in led_pins:
        wpi.digitalWrite(pin, wpi.LOW)