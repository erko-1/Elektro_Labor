import smbus  # smbus is used for I2C communication
import time

DEV_TEMP_ADDRESS = 0b1001111  # 7-bit I2C address of the temperature IC (DS1631)
READ_TEMP = 0xAA  # Register address to read temperature data

twibus = smbus.SMBus(1)  # I2C bus number 1 (pins BCM2/BCM3 on Raspberry Pi)

# Sending command to start temperature conversion (0x51)
twibus.write_byte(DEV_TEMP_ADDRESS, 0x51)

while True:
    time.sleep(1)  # Wait for the conversion to complete

    # Read the 16-bit temperature data
    temperatur_word = twibus.read_word_data(DEV_TEMP_ADDRESS, READ_TEMP)
    
    # The DS1631 returns the temperature as a 16-bit word.
    # The upper byte contains the integer part, and the lower byte contains the fractional part.
    vorkomma = temperatur_word & 0xFF  # Extract the lower 8 bits (integer part)
    nachkomma = (temperatur_word >> 8) & 0x0F  # Extract the upper 4 bits (fractional part)
    nachkomma = nachkomma / 16.0  # Convert fractional part to decimal (divide by 16)

    temperatur = vorkomma + nachkomma  # Combine integer and fractional part
    print(temperatur)  # Print the temperature value
