from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.button import Button

low_mode_temp = 20
default_mode_temp = 40
high_mode_temp = 80

low_mode_time = 12
default_mode_time = 14
high_mode_time = 16

class ProgramScreen(Screen):
    low_mode_temp_text = StringProperty(str(low_mode_temp))
    default_mode_temp_text = StringProperty(str(default_mode_temp))
    high_mode_temp_text = StringProperty(str(high_mode_temp))
    low_mode_time_text = StringProperty(str(low_mode_time))
    default_mode_time_text = StringProperty(str(default_mode_time))
    high_mode_time_text = StringProperty(str(high_mode_time))
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.low_mode_temp_text = str(low_mode_temp)
        self.low_mode_time_text = str(low_mode_time)
        self.default_mode_temp_text = str(default_mode_temp)
        self.default_mode_time_text = str(default_mode_time)
        self.high_mode_time_text = str(high_mode_time)
        self.high_mode_temp_text = str(high_mode_temp)

    # Action functions for each button press
    def go_back(self):
        self.manager.transition.direction = 'right'  # Example transition direction
        self.manager.current = 'previous_screen'  # Replace with your previous screen name

    def reorder(self):
        # Implement reorder functionality here
        print("Reordering...")

    def start_simple_mode(self):
        # Logic for simple mode
        print("Starting Simple Mode with Temperature: 190°C and Duration: 12 mins")

    def start_extended_mode(self):
        # Logic for extended mode
        print("Starting Extended Mode with Temperature: 50°C and Duration: 20 mins")

    def start_low_temp_mode(self):
        # Logic for low temperature mode
        print("Starting Low Temp Mode with Temperature: 20°C and Duration: 3 mins")