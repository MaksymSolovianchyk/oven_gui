# sensor_read.py

import sys
import threading
from kivy.clock import Clock

if sys.platform.startswith("linux"):
    import board
    import busio
    import digitalio
    import adafruit_max31865

    spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs1 = digitalio.DigitalInOut(board.D5)
    cs2 = digitalio.DigitalInOut(board.D6)

    sensor1 = adafruit_max31865.MAX31865(spi, cs1, rtd_nominal=100.0, ref_resistor=430.0, wires=3)
    sensor2 = adafruit_max31865.MAX31865(spi, cs2, rtd_nominal=100.0, ref_resistor=430.0, wires=3)
else:
    import random
    sensor1 = "SimulatedSensor1"
    sensor2 = "SimulatedSensor2"

def random_temperature():
    return random.uniform(25, 35)

# Sensor activity flags
sensor1_active = True
sensor2_active = True

def read_sensor(sensor):
    global sensor1_active, sensor2_active

    if sensor == sensor1 and not sensor1_active:
        print("Sensor 1 is turned off.")
        return None
    if sensor == sensor2 and not sensor2_active:
        print("Sensor 2 is turned off.")
        return None

    try:
        if sys.platform.startswith("linux"):
            temp = sensor.temperature
            print('Temp:{0:0.3f}C '.format(temp))
            print(sensor.resistance)
            fault = sensor.fault

            if temp < -200 or temp > 850:
                print(f"{sensor}: Temperature out of range: {temp:.2f}C")

            if any(fault):
                print(f"Sensor fault code: {fault}")
                sensor.clear_faults()
                return None
            return temp
        else:
            return random_temperature()
    except Exception as e:
        print(f"Sensor error: {e}")
        return None

def read_sensors_threaded(callback):
    def task():
        temps = []
        for i, s in enumerate([sensor1, sensor2], start=1):
            temp = read_sensor(s)
            if temp is not None:
                temps.append(temp)
            else:
                print(f"Sensor {i} failed or returned invalid data.")
        average = sum(temps) / len(temps) if temps else 0.0
        Clock.schedule_once(lambda dt: callback(average), 0)

    threading.Thread(target=task, daemon=True).start()

def get_average_temperature():
    # Legacy sync version (used for testing or blocking use)
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
        return 0.0
