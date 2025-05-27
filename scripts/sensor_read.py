import sys

if sys.platform.startswith("linux"):
    import board
    import busio
    import digitalio
    import adafruit_max31865

    # Shared SPI bus
    spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

    # Chip select pins for both sensors
    cs1 = digitalio.DigitalInOut(board.D5)
    cs2 = digitalio.DigitalInOut(board.D6)

    # Create sensor instances (PT100, 3-wire config)
    sensor1 = adafruit_max31865.MAX31865(spi, cs1, rtd_nominal=100.0, ref_resistor=430.0, wires=3)
    sensor2 = adafruit_max31865.MAX31865(spi, cs2, rtd_nominal=100.0, ref_resistor=430.0, wires=3)

    def read_sensor(sensor):
        try:
            temp = sensor.temperature
            fault = sensor.fault
            if fault:
                print(f"Sensor fault code: {fault}")
                sensor.clear_faults()
                return None
            return temp
        except Exception as e:
            print(f"Sensor error: {e}")
            return None

    def get_average_temperature():
        temps = []
        for i, s in enumerate([sensor1, sensor2], start=1):
            temp = read_sensor(s)
            if temp is not None:
                temps.append(temp)
            else:
                print(f"Sensor {i} failed or returned invalid data.")

        if temps:
            return sum(temps) / len(temps)
        else:
            print("Both sensors failed.")
            return None

else:
    # Simulated environment
    import random
    def get_average_temperature():
        return sum([random.uniform(25, 35) for _ in range(2)]) / 2
