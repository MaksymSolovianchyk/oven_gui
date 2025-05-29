# sensor_read.py

import sys
import threading
import time
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

sensor1_active = True
sensor2_active = True

_latest_temp = 0.0
_temp_lock = threading.Lock()

def read_sensor(sensor):
    global sensor1_active, sensor2_active

    if sensor == sensor1 and not sensor1_active:
        return None
    if sensor == sensor2 and not sensor2_active:
        return None

    try:
        if sys.platform.startswith("linux"):
            temp = sensor.temperature
            fault = sensor.fault

            if temp < -200 or temp > 850:
                return None

            if any(fault):
                sensor.clear_faults()
                return None
            return temp
        else:
            return random_temperature()
    except Exception as e:
        print(f"Sensor error: {e}")
        return None

def _sensor_loop():
    global _latest_temp
    while True:
        temps = []
        for sensor in [sensor1, sensor2]:
            temp = read_sensor(sensor)
            if temp is not None:
                temps.append(temp)
        avg = sum(temps) / len(temps) if temps else 0.0

        with _temp_lock:
            _latest_temp = avg

        time.sleep(0.5)

def start_sensor_thread():
    thread = threading.Thread(target=_sensor_loop, daemon=True)
    thread.start()

def get_average_temperature():
    with _temp_lock:
        return _latest_temp
