import sys

if sys.platform.startswith("linux"):
    # Raspberry Pi likely
    import board
    import busio
    import digitalio
    import adafruit_max31856

    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs = digitalio.DigitalInOut(board.D5)
    max31856 = adafruit_max31856.MAX31856(spi, cs)

    def get_temperature():
        try:
            return max31856.temperature
        except Exception as e:
            print(f"Sensor error: {e}")
            return None
else:
    # Development mode on Mac/Windows
    import random

    def get_temperature():
        return random.uniform(25, 35)  # Simulated temperature

print(get_temperature())