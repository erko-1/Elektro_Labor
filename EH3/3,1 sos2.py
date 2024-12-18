import time
import wiringpi as wpi

wpi.wiringPiSetupGpio()
wpi.pinMode(17, 1)

morse_code_dict = { 'S': '...', 'O': '-----', ' ': ' '}

def morse_code(message):
    for char in message:
        if char.upper() in morse_code_dict:
            morse_sequence = morse_code_dict[char.upper()]
            for symbol in morse_sequence:
                if symbol == '.':
                    wpi.digitalWrite(17, 1)
                    time.sleep(0.1)
                elif symbol == '-':
                    wpi.digitalWrite(17, 1)
                    time.sleep(0.3)
                wpi.digitalWrite(17, 0)
                time.sleep(0.1)
                
            time.sleep(0.3)
        else:
            time.sleep(1)

while True:
    morse_code("SOS")
    time.sleep(2)