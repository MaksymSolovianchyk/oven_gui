from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import StringProperty
from kivy.clock import Clock
from scripts import sensor_read

class SensorStatusScreen(Screen):
    temp1 = StringProperty("0.0")
    temp2 = StringProperty("0.0")
    last_string_screen = StringProperty("")

    def __init__(self, **kwargs):
        super(SensorStatusScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_temps, 1)

    def parse_last_screen(self, last_screen):
        self.last_string_screen = last_screen

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = self.last_string_screen

    def update_temps(self, dt):
        t1 = sensor_read.read_sensor(sensor_read.sensor1)
        t2 = sensor_read.read_sensor(sensor_read.sensor2)

        self.temp1 = f"{t1:.2f}" if t1 is not None else "--"
        self.temp2 = f"{t2:.2f}" if t2 is not None else "--"

        avg = sensor_read.get_average_temperature()
        print(f"Average Temperature: {avg:.2f}" if avg else "No valid sensors.")

    def toggle_sensor1(self, active):
        sensor_read.sensor1_active = active

    def toggle_sensor2(self, active):
        sensor_read.sensor2_active = active
