import wiringpi as wpi

wpi.wiringPiSetupGpio()

led_pin = 17

wpi.pinMode(led_pin, wpi.OUTPUT)
try:
    while True:
        user_input = input("Geben Sie 'e' für Ein und 'a' für aus ein: ")
        
        if user_input == 'e':
            wpi.digitalWrite(led_pin, wpi.HIGH)
        elif user_input == 'a':
            wpi.digitalWrite(led_pin, wpi.LOW)
        else:
            print("Ungültige Eingabe. Bitte 'e' oder 'a' eingeben.")
    
except KeyboardInterrupt:
    wpi.digitalWrite(led_pin, wpi.LOW)
    wpi.pinMode(led_pin, wpi.INPUT)
    