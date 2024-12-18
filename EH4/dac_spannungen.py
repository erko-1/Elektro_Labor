import wiringpi as wpi

wpi.wiringPiSPISetup(0, 500000)
def str_to_bytes(dac_a_v = 1500, dac_b_v = 3300):
    byte1 = dac_a_v>>4
    byte2_1 = dac_a_v & 0b000000001111
    byte2_2 = dac_b_v >> 8
    byte2 = (byte2_1 << 4) + byte2_2
    byte3 = dac_b_v & 0b000011111111
    #print(byte1, byte2, byte3)
    return byte1,byte2,byte3

c1, c2, c3 = str_to_bytes()
print(f'{c1:12b}\n{c2:12b}\n{c3:12b}')

# Main loop to send data continuously
while True:
     
    # Send data over SPI
    d1, d2 = wpi.wiringPiSPIDataRW(0, bytes([c1,c2,c3]))

