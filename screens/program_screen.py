from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


upladder_mode_temp = 20
downladder_mode_temp = 40
heating_mode_temp = 80

upladder_mode_time = 12
downladder_mode_time = 14
heating_mode_time = 16
temp = int
time = int

upladder= False
downladder = False
heating = False


class ProgramScreen(Screen):
    upladder_mode_temp_text = StringProperty(str(upladder_mode_temp))
    downladder_mode_temp_text = StringProperty(str(downladder_mode_temp))
    heating_mode_temp_text = StringProperty(str(heating_mode_temp))
    upladder_mode_time_text = StringProperty(str(upladder_mode_time))
    downladder_mode_time_text = StringProperty(str(downladder_mode_time))
    heating_mode_time_text = StringProperty(str(heating_mode_time))

    current_mode = StringProperty("")  # Store the current mode here

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

    def go_to_ladder_screen(self, mode):
        self.current_mode = mode  # Set the current mode to the selected one

        if mode == 'up_ladder':
            temp = upladder_mode_temp
            time = upladder_mode_time
            graph = 'logos/up_ladder.png'
        elif mode == 'down_ladder':
            temp = downladder_mode_temp
            time = downladder_mode_time
            graph = 'logos/donw_ladder.png'
        elif mode == 'heating_ladder':
            temp = heating_mode_temp
            time = heating_mode_time
            graph = 'logos/heating_mode.png'

        # Pass the mode to the next screen (UpLadderScreen)
        up_screen = self.manager.get_screen('up_ladder_screen')
        up_screen.set_mode(mode, temp, time, graph)  # Set the mode and temp/time/graph for the next screen

        self.manager.transition.direction = 'left'
        self.manager.current = 'up_ladder_screen'