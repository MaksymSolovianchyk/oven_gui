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

    def go_to_ladder_screen(self, mode):
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

        up_screen = self.manager.get_screen('up_ladder_screen')
        up_screen.temp_text = str(temp)
        up_screen.time_text = str(time)
        up_screen.graph_source = graph  # Set image

        self.manager.transition.direction = 'left'
        self.manager.current = 'up_ladder_screen'