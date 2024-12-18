import wiringpi as wpi

led_pins = [17, 18, 27, 22, 23, 24, 25, 4]
button_pin = 9

wpi.wiringPiSetupGpio()

for pin in led_pins:
    wpi.pinMode(pin, wpi.OUTPUT)
    
wpi.pinMode(button_pin, wpi.INPUT)


# Variable zum Verefolgen des Tasterzustands
#button_state = False

# Interrupt-Routine, die aufgerufen wird, wenn der taster gedrückt wird
def button_interrupt():
    print("yes")
    for pin in led_pins:
        wpi.digitalWrite(pin, wpi.HIGH)
    wpi.delayMicroseconds(1000000)
    #global button_state
    #if wpi.digitalRead(button_pin) == 0:
        #button_state = True
     
    for pin in led_pins:
        wpi.digitalWrite(pin, wpi.LOW)

        
# Registrieren Sie die Interrupt-Routine
wpi.wiringPiISR(button_pin, wpi.INT_EDGE_RISING, button_interrupt)

while True:
    pass
