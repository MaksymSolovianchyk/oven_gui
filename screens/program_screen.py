from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import csv

upladder_mode_temp = 20
downladder_mode_temp = 40
heating_mode_temp = 80

upladder_mode_time = 12
downladder_mode_time = 14
heating_mode_time = 16

class ProgramScreen(Screen):
    upladder_mode_temp_text = StringProperty(str(upladder_mode_temp))
    downladder_mode_temp_text = StringProperty(str(downladder_mode_temp))
    heating_mode_temp_text = StringProperty(str(heating_mode_temp))
    upladder_mode_time_text = StringProperty(str(upladder_mode_time))
    downladder_mode_time_text = StringProperty(str(downladder_mode_time))
    heating_mode_time_text = StringProperty(str(heating_mode_time))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.upladder_mode_temp_text = str(upladder_mode_temp)
        self.upladder_mode_time_text = str(upladder_mode_time)
        self.downladder_mode_temp_text = str(downladder_mode_temp)
        self.downladder_mode_time_text = str(downladder_mode_time)
        self.heating_mode_time_text = str(heating_mode_time)
        self.heating_mode_temp_text = str(heating_mode_temp)

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'second'
