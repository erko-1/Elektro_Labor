import wiringpi as wpi

switch_pins = [12, 13, 14, 15, 16, 19, 20, 21]
led_pins = [17, 18, 27, 22, 23, 24, 25, 4]

wpi.wiringPiSetupGpio()

for pin in switch_pins:
    wpi.pinMode(pin, wpi.INPUT)
    
for pin in led_pins:
    wpi.pinMode(pin, wpi.OUTPUT)
    
try:
    while True:
        switch_states = [wpi.digitalRead(pin) for pin in switch_pins]
        
        for i in range(8):
            wpi.digitalWrite(led_pins[i], switch_states[i])
    
except KeyboardInterrupt:
    for pin in led_pins:
        wpi.digitalWrite(pin, wpi.LOW)