import wiringpi as wpi

led_pins = [17, 18, 27, 22, 23, 24, 25, 4]

wpi.wiringPiSetupGpio()

for pin in led_pins:
    wpi.pinMode(pin, wpi.OUTPUT)
    
#Variable zum Speichern des aktuellen Zustands der LEDs
led_states = [0, 0, 0, 0, 0, 0, 0, 0]

try:
    while True:
        user_input = input("Geben Sie die Nummer der LED (1-8 oder 0-7) ein:")
        
        try:
            led_num = int(user_input)
            if 1 <= led_num <= 8:
                # Ermitteln den Index für LED
                led_index = led_num - 1
                # Aktualisiere den Zustand der ausgewählten LED
                led_states[led_index] = 1 - led_states[led_index]
                # Aktualisiere den physikalischen Zustand der LEDs
                wpi.digitalWrite(led_pins[led_index], led_states[led_index])
                #print(f"LED {led_num} wurde {'eingeschaltet' if led_states[led_index] else 'ausgeschaltet'}")
            else:
                print("Ungültige Eingabe. Geben Sie eine Zahl zwischen 1 und 8 ein.")
        except ValueError:
            print("Ungültige Eingabe. Geben Sie eine Zahl zwischen 1 und 8 ein.")
            
except KeyboardInterrupt:
    # Beim Beenden das GPIO-Cleanup durchführen.
    for pin in led_pins:
        wpi.digitalWrite(pin, wpi.LOW)